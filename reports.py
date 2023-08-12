"""Calculates subtotals of collection, AIP, and file_id counts for different categories: groups, format types,
format standardized names, format identifications, and combinations of those. File size subtotals will be added once
that information is added to the ARCHive group format reports. The results are saved to an Excel workbook,
with one spreadsheet per subtotal, to use for analyzing formats in ARCHive.

The script uses information from three sources, all CSVs. The usage report is downloaded from ARCHive. Both archive
format reports are made from the ARCHive group format reports using the merge_format_reports script.
    * usage report: the amount ingested (AIP count and size) for each group and each user in a group.
    * archive_formats report: Organized by format and group. Has group, file_id count, and format information.
    * archive_formats_by_aip report: Organized by AIP and format. Has group, collection, aip id, and format information.

Definition of terms:
    * Group: ARCHive group name, which is the department or departments responsible for the content.
    * Format type: category of the format, for example audio, image, or text.
    * Format standardized name: a simplified version of the name, removing details to group related formats together.
    * Format identification: a combination of the format name, version, and registry key (usually PRONOM).

Ideas for additional reports:
    * Map NARA and/or LOC risk assessments to the most common formats.
    * Compare the current report to a previous one to show change over time.
    * Add groups and type to common formats (risk analysis) for additional information.

Unlike Excel, pandas does not merge difference of capitalization, e.g. MPEG Video and MPEG video, when subtotaling.
"""

# Before running this script, run update_standardization.py and merge_format_reports.py
# Usage: python path/reports.py report_folder
# Report folder should contain the usage report and both archive format reports.

import csv
import datetime
import os
import pandas as pd
import sys


def archive_overview(df_aip, df, usage):
    """Uses the data from the usage report and both ARCHive format reports to calculate statistics for each group and
    the ARCHive total. Includes counts of TBs, collections, AIPs, file_ids, file types, format standardized names,
    and format identifications. Returns a dataframe. """

    # Gets the size (in TB) per group from the usage report.
    size_by_group = size_in_tb(usage)

    # Gets the size (in GB) from the dataframe to show the difference between unique (from usage)
    # and inflated by multiple identifications for individual files.
    size_inflated = round(df.groupby("Group")["Size (GB)"].sum(), 2)

    # Gets the number of collections per group from the archive_formats_by_aip report.
    # Only counts collections with AIPs, which may result in a difference between this count and the ARCHive interface.
    # Additionally, dlg-hargrett collections in ARCHive that are part of turningpoint are counted as dlg.
    collections_by_group = df_aip.groupby("Group")["Collection"].nunique()

    # Gets the number of AIPs per group from the archive_formats_by_aip report.
    # Not using data from usage report since each version of an AIP is counted separately.
    aips_by_group = df_aip.groupby("Group")["AIP"].nunique()

    # Gets the number of format types per group from the archive_formats_by_aip report.
    types_by_group = df_aip.groupby("Group")["Format Type"].nunique()

    # Gets the number of file_ids per group from the archive_formats report.
    # These numbers are inflated by files with more than one format identification.
    files_by_group = df.groupby("Group")["File_IDs"].sum()

    # Gets the number of format standardized names per group from the archive_formats_by_aip report.
    formats_by_group = df_aip.groupby("Group")["Format Standardized Name"].nunique()

    # Gets the number of format identifications per group from the archive_formats report.
    format_ids_by_group = df.groupby("Group")["Format Identification"].nunique()

    # Combines the series with all the counts into a single dataframe.
    group_stats = pd.concat([size_by_group, size_inflated, collections_by_group, aips_by_group, files_by_group,
                             types_by_group, formats_by_group, format_ids_by_group], axis=1)

    # Renames the dataframe columns to be more descriptive.
    rename = {"Size": "Size (TB)", "Size (GB)": "Size (GB) Inflated", "Collection": "Collections", "AIP": "AIPs",
              "Format Type": "Format Types", "Format Standardized Name": "Format Standardized Names",
              "Format Identification": "Format Identifications"}
    group_stats = group_stats.rename(columns=rename)

    # Replace cells without values (one group has no files yet) with 0.
    group_stats = group_stats.fillna(0)

    # Adds the column totals as a row in the dataframe.
    group_stats.loc["total"] = [group_stats["Size (TB)"].sum(), group_stats["Size (GB) Inflated"].sum(),
                                group_stats["Collections"].sum(), group_stats["AIPs"].sum(),
                                group_stats["File_IDs"].sum(), df["Format Type"].nunique(),
                                df["Format Standardized Name"].nunique(), df["Format Identification"].nunique()]

    # Returns the information in a dataframe. Row index is the group_code and columns are Size (TB), Collections,
    # AIPs, File_IDs, Format Types, Format Standardized Names, and Format Identifications.
    return group_stats


def check_argument(argument_list):
    """
    Verifies the required argument report_folder is present and valid.
    Returns the path for report_folder and the error (or None if no error).
    """
    # Makes a list for errors, so all errors can be tested before returning the result,
    # and default values for the two variables assigned from arguments.
    error = None
    report = None

    # Verifies that the required argument (report_folder) is present.
    # and if it is present that it is a valid directory.
    if len(argument_list) > 1:
        report = argument_list[1]
        if not os.path.exists(report):
            error = f"Report folder '{report}' does not exist"
    else:
        error = "Required argument report_folder is missing"

    # Returns the results.
    return report, error


def file_count_ranges(category, df):
    """Uses the data from the archive_formats report to calculate the number of instances of the category within each
    range of file_ids (1-9, 10-99, 100-999, etc.). Returns a dataframe. """

    # Makes a series with the number of file_ids for each instance of the category, regardless  of group.
    df_cat = df.groupby(df[category])["File_IDs"].sum()

    # Makes series with the subset of the archive_formats_by_aip report data with the specified numbers of file_ids.
    ones = df_cat[(df_cat < 10)]
    tens = df_cat[(df_cat >= 10) & (df_cat < 100)]
    hundreds = df_cat[(df_cat >= 100) & (df_cat < 1000)]
    thousands = df_cat[(df_cat >= 1000) & (df_cat < 10000)]
    ten_thousands = df_cat[(df_cat >= 10000) & (df_cat < 100000)]
    hundred_thousands_plus = df_cat[(df_cat >= 100000)]

    # Makes lists with the data for the dataframe: file_id ranges (for index) and the number of instances in each range.
    file_id_ranges = ["1-9", "10-99", "100-999", "1000-9999", "10000-99999", "100000+"]
    instances = [ones.count(), tens.count(), hundreds.count(), thousands.count(), ten_thousands.count(),
                 hundred_thousands_plus.count()]

    # Makes a dataframe from the lists.
    result = pd.DataFrame(instances, columns=[f"Number of Formats ({category})"], index=file_id_ranges)

    # Returns the dataframe. Row index is the file_id ranges and column is Number of Formats (category).
    return result


def format_id_frequency(totals, df):
    """Uses the data from the archive_formats report to calculate the frequency for every format identification (
    name, version, registry key), which includes the file_id count, percentage of file_ids, size in GB,
    and percentage of size. Returns a dataframe sorted largest to smallest by file_id count since the items of most
    interest are the most common formats. """

    # Make series for file_id counts and file_id percentages.
    format_count = df.groupby(df["Format Identification"])["File_IDs"].sum()
    format_percentage = (format_count / totals["Files"]) * 100
    format_percentage = round(format_percentage, 2)
    format_percentage = format_percentage.rename("File_IDs Percentage")

    # Make series for total size and size percentages.
    size = df.groupby(df["Format Identification"])["Size (GB)"].sum()
    size_percentage = (size / totals["Size"]) * 100
    size_percentage = round(size_percentage, 2)
    size_percentage = size_percentage.rename("Size (GB) Percentage")

    # Combine all the series into a single dataframe and sort largest to smallest by file_ids.
    format_ids = pd.concat([format_count, format_percentage, size, size_percentage], axis=1)
    format_ids = format_ids.sort_values(by="File_IDs", ascending=False)

    # Returns the dataframe. Row index is the file_ids and columns are the four frequency measures.
    return format_ids


def get_report_paths(report_folder_path):
    """Finds the path to the three reports used as script input.
    Returns the three paths and a list of any missing files."""

    # Makes variables to store the paths, if found.
    formats_by_aip_path = None
    formats_path = None
    usage_path = None

    # Searches the report folder for the expected files, and if found updates the variable with the file name.
    # These files include dates, so the entire file name cannot be predicted by the script.
    for file in os.listdir(report_folder_path):
        if file.startswith("archive_formats_by_aip") and file.endswith(".csv"):
            formats_by_aip_path = os.path.join(report_folder_path, file)
        elif file.startswith("archive_formats_") and file.endswith(".csv"):
            formats_path = os.path.join(report_folder_path, file)
        elif file.startswith("usage_report_") and file.endswith(".csv"):
            usage_path = os.path.join(report_folder_path, file)

    # Tests if all three paths were found, and if not adds the missing ones to a list.
    missing_list = []
    if not formats_by_aip_path:
        missing_list.append("archive_formats_by_aip.csv")
    if not formats_path:
        missing_list.append("archive_formats.csv")
    if not usage_path:
        missing_list.append("usage_report.csv")

    # Returns the results. The errors list is empty if all three files were found.
    return formats_by_aip_path, formats_path, usage_path, missing_list


def group_overlap(category, df):
    """Uses the data from the archive_formats report to calculate the number of groups and a list of the groups which
    have each instance of the category, for example format type. Returns a dataframe. """

    # Makes a series with a list of group names for each instance of the category.

    groups_list = df.groupby(df[category])["Group"].unique()
    groups_list = groups_list.rename("Group List")

    # Makes a series with the number of groups for each instance of the category.
    groups_count = groups_list.str.len()
    groups_count = groups_count.rename("Groups")

    # Converts the list from a list to a comma-separated string for easier readability in Excel.
    # Wait to do this until after groups_count so that the count is correct.
    groups_list = groups_list.apply(", ".join)

    # Combines the count and the list series into a single dataframe.
    # Had to do these separately to get the counts for each instance separately.
    groups_per_category = pd.concat([groups_count, groups_list], axis=1)

    # Sorts the values by the number of groups, largest to smallest.
    # The primary use for this data is to see what the most groups have in common.
    groups_per_category = groups_per_category.sort_values(by="Groups", ascending=False)

    # Returns the dataframe. Row index is the category and columns are Groups, Group List.
    return groups_per_category


def one_category(category, totals, df_aip, df):
    """Uses the data from both ARCHive format reports to calculate subtotals of collection, AIP, and file_id counts
    and size in GB per each instance of the category, for example format type. Returns a dataframe. """

    # Creates a series for each count type (collections, AIPs, and file_ids) and size for each instance of the category.
    collections = df_aip.groupby(category)["Collection"].nunique()
    aips = df_aip.groupby(category)["AIP"].nunique()
    files = df.groupby(category)["File_IDs"].sum()
    size = df.groupby(category)["Size (GB)"].sum()

    # Creates a series for the percentage of each count type and size for each instance of the category.
    # The percentage is rounded to two decimal places.
    # Also renames the series to be more descriptive.

    collections_percent = (collections / totals["Collections"]) * 100
    collections_percent = round(collections_percent, 2)
    collections_percent = collections_percent.rename("Collections Percentage")

    aips_percent = (aips / totals["AIPs"]) * 100
    aips_percent = round(aips_percent, 2)
    aips_percent = aips_percent.rename("AIPs Percentage")

    files_percent = (files / totals["Files"]) * 100
    files_percent = round(files_percent, 2)
    files_percent = files_percent.rename("File_IDs Percentage")

    size_percent = (size / totals["Size"]) * 100
    size_percent = round(size_percent, 2)
    size_percent = size_percent.rename("Size (GB) Percentage")

    # Combines all the count and percentage series into a single dataframe.
    result = pd.concat([collections, collections_percent, aips, aips_percent, files, files_percent, size, size_percent],
                       axis=1)

    # Renames Collection and AIP columns to plural to be more descriptive.
    result = result.rename({"Collection": "Collections", "AIP": "AIPs"}, axis=1)

    # Returns the dataframe. Row index is the category and columns are Collections, Collections Percentage, AIPs,
    # AIPs Percentage, File_IDs, File_IDs Percentage.
    return result


def size_count_ranges(category, df):
    """Uses the data from the archive_formats report to calculate the number of instances of the category within each
    range of total size (0-249 GB, 250-499 GB, etc.). Returns a dataframe. """

    # Makes a series with the total size for each instance of the category, regardless of group.
    df_cat = df.groupby(df[category])["Size (GB)"].sum()

    # Makes series with the subset of the archive_formats_by_aip report data with the specified numbers of file_ids.
    tier_one = df_cat[(df_cat < 10)]
    tier_two = df_cat[(df_cat >= 10) & (df_cat < 100)]
    tier_three = df_cat[(df_cat >= 100) & (df_cat < 500)]
    tier_four = df_cat[(df_cat >= 500) & (df_cat < 1000)]
    tier_five = df_cat[(df_cat >= 1000) & (df_cat < 10000)]
    tier_six = df_cat[(df_cat >= 10000) & (df_cat < 50000)]
    tier_seven = df_cat[(df_cat >= 50000)]

    # Makes lists with the data for the dataframe: file_id ranges (for index) and the number of instances in each range.
    size_ranges = ["0-9 GB", "10-99 GB", "100-499 GB", "500-999 GB", "1-9 TB", "10-49 TB", "50+ TB"]
    instances = [tier_one.count(), tier_two.count(), tier_three.count(), tier_four.count(), tier_five.count(),
                 tier_six.count(), tier_seven.count()]

    # Makes a dataframe from the lists.
    result = pd.DataFrame(instances, columns=[f"Total Size ({category})"], index=size_ranges)

    # Returns the dataframe. Row index is the size ranges and column is Total Size (category).
    return result


def size_in_tb(usage):
    """Uses data from the usage report to calculate the size in TB each group. Returns a dataframe. """

    # Group Names maps the human-friendly version of group names from the usage report to the ARCHive group code
    # which is used in both archive format reports and in ARCHive metadata generally.
    group_names = {"Brown Media Archives": "bmac", "Digital Library of Georgia": "dlg",
                   "DLG & Hargrett": "dlg-hargrett", "DLG & Map and Government Information Library": "dlg-magil",
                   "Hargrett Library": "hargrett", "Map and Government Information Library": "magil",
                   "Richard B. Russell Library": "russell"}

    # Makes a dictionary for the size for each group, gathering all data before converting it to a dataframe.
    group_size = {}

    # Gets the data from each row of the usage report.
    # A row can have data on a group, an individual user, or be blank.
    with open(usage, 'r') as usage_open:
        usage_read = csv.reader(usage_open)
        for row in usage_read:

            # Parses data (group name, size, and size unit of measurement)from each group's row,
            # identified by not being blank and having a group name at row[0].
            if row and row[0] in group_names:
                group = group_names[row[0]]
                size, unit = row[2].split()

                # Converts the size to TB, rounded to two decimal places.
                # If it encounters a unit of measurement that wasn't anticipated, the script prints a warning message.
                conversion = {"Bytes": 1000000000000, "KB": 1000000000, "MB": 1000000, "GB": 1000, "TB": 1}
                try:
                    size = float(size) / conversion[unit]
                    size = round(size, 2)
                except KeyError:
                    size = 0
                    print("WARNING! Unexpected unit type:", unit)

                # Adds the results for this group to the dictionary.
                group_size[group] = size

    # Makes the dictionary into a dataframe so it can be combined with the collection and file_id counts.
    sizes = pd.DataFrame.from_dict(group_size, orient="index", columns=["Size"])

    # Returns the dataframe. Row index is the group_code and the column is Size.
    return sizes


def two_categories(category1, category2, df_aip, df):
    """Uses data from both ARCHive format reports to calculate subtotals of collection, AIP, and file_id counts and
    size in GB for each instance of two categories, for example format type and group. Returns a dataframe. """

    # Uses the archive_formats_by_aip report data to get counts of unique collections and unique AIPs.
    result = df_aip[[category1, category2, "Collection", "AIP"]].groupby([category1, category2]).nunique()

    # Renames the column headings to be plural (Collections, AIPs) to be more descriptive.
    result = result.rename({"Collection": "Collections", "AIP": "AIPs"}, axis=1)

    # Uses the archive_formats report data to get counts of file_ids and adds to the dataframe.
    # The counts are inflated by files with multiple possible format identifications.
    files_result = df.groupby([category1, category2])["File_IDs"].sum()
    result = pd.concat([result, files_result], axis=1)

    # Uses the archive_formats report data to get size in GB and adds to the dataframe.
    size_result = df.groupby([category1, category2])["Size (GB)"].sum()
    result = pd.concat([result, size_result], axis=1)

    # Returns the dataframe. Row index is the two categories and columns are the counts and size.
    # Deletes extra columns named with the categories before returning.
    #result = result.drop([category1, category2], axis=1)
    return result


if __name__ == '__main__':

    # Verifies the required argument is present and the path is valid.
    # If there was an error, prints the error and exits the script.
    report_folder, error_message = check_argument(sys.argv)
    if error_message:
        print(error_message)
        print("Script usage: python path/reports.py report_folder")
        sys.exit(1)

    # Gets paths of the three reports to be analyzed, which are in report_folder.
    # If any where not found (missing is not empty), prints the missing one(s) and exits the script.
    formats_by_aip_report, formats_report, usage_report, missing = get_report_paths(report_folder)
    if len(missing) > 0:
        for file_name in missing:
            print(f"Could not find {file_name} in '{report_folder}'.")
        print("Please add the missing report(s) to the report folder and run this script again.")
        sys.exit(1)

    # Makes dataframes from both ARCHive format reports.
    df_formats_by_aip = pd.read_csv(formats_by_aip_report)
    df_formats = pd.read_csv(formats_report)

    # GENERATE A DATAFRAME OR SERIES FOR EACH TYPE OF ANALYSIS.

    # Makes the ARCHive overview dataframe (summary statistics by group).
    overview = archive_overview(df_formats_by_aip, df_formats, usage_report)

    # Saves the ARCHive collection, AIP, file, and size totals to a list for calculating percentages in other dataframes.
    # Not calculating totals in those dataframes so collection and AIP counts aren't inflated by multiple identifications.
    # Counts for file and size are inflated because don't have file name in the data and therefore can't deduplicate.
    totals_dict = {"Collections": overview["Collections"]["total"], "AIPs": overview["AIPs"]["total"],
                   "Files": overview["File_IDs"]["total"], "Size": overview["Size (GB) Inflated"]["total"]}

    # Makes the format type dataframe (collection, AIP, and file_id counts and percentages).
    format_types = one_category("Format Type", totals_dict, df_formats_by_aip, df_formats)

    # Makes the format standardized name dataframe (collection, AIP, and file_id counts and percentages).
    # And makes a dataframe with any in this dataframe with over 100 file_id counts to use for risk analysis.
    format_names = one_category("Format Standardized Name", totals_dict, df_formats_by_aip, df_formats)
    common_formats = format_names[format_names.File_IDs >= 100]
    common_formats = common_formats.sort_values(by="File_IDs", ascending=False)

    # Makes a dataframe with collection, AIP, and file_id subtotals, first by format type and then subdivided by group.
    type_by_group = two_categories("Format Type", "Group", df_formats_by_aip, df_formats)

    # Makes a dataframe with collection, AIP, and file_id subtotals, first by format type and then subdivided by format
    # standardized name.
    type_by_name = two_categories("Format Type", "Format Standardized Name", df_formats_by_aip, df_formats)

    # Makes a dataframe with collection, AIP, and file_id subtotals, first by format standardized name and then by group.
    name_by_group = two_categories("Format Standardized Name", "Group", df_formats_by_aip, df_formats)

    # Makes a dataframe with the file_id count and percentage for every format identification (name, version, registry key).
    # The dataframe is sorted largest to smallest since the items of most interest are the most common formats.
    format_ids = format_id_frequency(totals_dict, df_formats)

    # Makes a dataframe with the number of groups and list of groups that have each format type.
    groups_per_type = group_overlap("Format Type", df_formats)

    # Makes a dataframe with the number of groups and list of groups that have each format standardized name.
    groups_per_name = group_overlap("Format Standardized Name", df_formats)

    # Makes a dataframe with the number of groups and list of groups that have each format identification.
    groups_per_id = group_overlap("Format Identification", df_formats)

    # Makes dataframes with the number of format standardized names within different ranges of file_id counts and sizes.
    format_name_ranges = file_count_ranges("Format Standardized Name", df_formats)
    format_name_sizes = size_count_ranges("Format Standardized Name", df_formats)

    # Makes dataframes with the number of format identifications within different ranges of file_id counts and sizes.
    format_id_ranges = file_count_ranges("Format Identification", df_formats)
    format_id_sizes = size_count_ranges("Format Identification", df_formats)

    # Saves each dataframe or series as a spreadsheet in an Excel workbook.
    # The workbook filename includes today's date, formatted YYYYMM, and is saved in the report folder.
    today = datetime.datetime.now().strftime("%Y-%m")
    with pd.ExcelWriter(os.path.join(report_folder, f"ARCHive Formats Analysis_{today}.xlsx")) as results:
        overview.to_excel(results, sheet_name="Group Overview", index_label="Group")
        format_types.to_excel(results, sheet_name="Format Types")
        format_names.to_excel(results, sheet_name="Format Names")
        format_name_ranges.to_excel(results, sheet_name="Format Name Ranges", index_label="File_ID Count Range")
        format_name_sizes.to_excel(results, sheet_name="Format Name Sizes", index_label="Size Range")
        common_formats.to_excel(results, sheet_name="Risk Analysis")
        type_by_group.to_excel(results, sheet_name="Type by Group")
        type_by_name.to_excel(results, sheet_name="Type by Name")
        name_by_group.to_excel(results, sheet_name="Name by Group")
        format_ids.to_excel(results, sheet_name="Format ID")
        format_id_ranges.to_excel(results, sheet_name="Format ID Ranges", index_label="File_ID Count Range")
        format_id_sizes.to_excel(results, sheet_name="Format ID Sizes", index_label="Size Range")
        groups_per_type.to_excel(results, sheet_name="Groups per Type")
        groups_per_name.to_excel(results, sheet_name="Groups per Name")
        groups_per_id.to_excel(results, sheet_name="Groups per Format ID")

    # Future development: would like to adjust the default formatting in Excel.
    # Experimented with xlsxwriter. Did not find examples where index and header are reformatted.
