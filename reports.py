"""Calculates subtotals of collection, AIP, and file_id counts for different categories: groups, format types,
format standardized names, format identifications, and combinations of those. File size subtotals will be added once
that information is added to the ARCHive group format reports. The results are saved to Excel workbooks
(Frequency, Group-Overlap, and Ranges) to use for analyzing formats in ARCHive.

The script uses information from three sources, all CSVs. The usage report is downloaded from ARCHive. Both archive
format reports are made from the ARCHive group format reports using the merge_format_reports script.
    * usage report: the amount ingested (AIP count and size) for each group and each user in a group.
    * archive_formats_by_aip report: Organized by AIP and format. Has group, collection, aip id, and format information.
    * archive_formats_by_group report: Organized by group and format. Has group, file_id count, and format information.

Definition of terms:
    * Group: ARCHive group name, which is the department or departments responsible for the content.
    * Format type: category of the format, for example audio, image, or text.
    * Format standardized name: a simplified version of the name, removing details to group related formats together.
    * Format identification: a combination of the format name, version, and registry key (usually PRONOM).

Unlike Excel, pandas does not merge difference of capitalization, e.g. MPEG Video and MPEG video, when subtotaling.
"""

# Before running this script, run update_standardization.py and merge_format_reports.py
# Usage: python path/reports.py report_folder
# Report folder should contain the usage report and both archive format reports.

import csv
import numpy as np
import os
import pandas as pd
import sys
from update_standardization import check_argument


def archive_overview(df_aip, df_group, usage):
    """Uses the data from the usage report and both ARCHive format reports to calculate statistics for each group and
    the ARCHive total. Includes counts of TBs, collections, AIPs, file_ids, file types, format standardized names,
    and format identifications. Returns a dataframe. """

    # Gets the size (in TB) per group from the usage report.
    size_by_group = size_in_tb(usage)

    # Gets the size (in GB) from the dataframe to show the difference between unique (from usage)
    # and inflated by multiple identifications for individual files.
    size_inflated = round(df_group.groupby('Group')['Size_GB'].sum(), 2)

    # Gets the number of collections per group from the archive_formats_by_aip report.
    # Only counts collections with AIPs, which may result in a difference between this count and the ARCHive interface.
    # Additionally, dlg-hargrett collections in ARCHive that are part of turningpoint are counted as dlg.
    collections_by_group = df_aip.groupby('Group')['Collection'].nunique()

    # Gets the number of AIPs per group from the archive_formats_by_aip report.
    # Not using data from usage report since each version of an AIP is counted separately.
    aips_by_group = df_aip.groupby('Group')['AIP'].nunique()

    # Gets the number of format types per group from the archive_formats_by_aip report.
    types_by_group = df_aip.groupby('Group')['Format_Type'].nunique()

    # Gets the number of file_ids per group from the archive_formats_by_group report.
    # These numbers are inflated by files with more than one format identification.
    files_by_group = df_group.groupby('Group')['File_IDs'].sum()

    # Gets the number of format standardized names per group from the archive_formats_by_aip report.
    formats_by_group = df_aip.groupby('Group')['Format_Standardized_Name'].nunique()

    # Gets the number of format identifications per group from the archive_formats_by_group report.
    format_ids_by_group = df_group.groupby('Group')['Format_Identification'].nunique()

    # Combines the series with all the counts into a single dataframe.
    group_stats = pd.concat([size_by_group, size_inflated, collections_by_group, aips_by_group, files_by_group,
                             types_by_group, formats_by_group, format_ids_by_group], axis=1)

    # Renames the dataframe columns to be more descriptive.
    rename = {"Size": "Size_TB", "Size_GB": "Size_GB_Inflated", "Collection": "Collections", "AIP": "AIPs",
              "Format_Type": "Format_Types", "Format_Standardized_Name": "Format_Standardized_Names",
              "Format_Identification": "Format_Identifications"}
    group_stats = group_stats.rename(columns=rename)

    # Replace cells without values (one group has no files yet) with 0.
    group_stats = group_stats.fillna(0)

    # Adds the column totals as a row in the dataframe.
    group_stats.loc["total"] = [group_stats['Size_TB'].sum(), group_stats['Size_GB_Inflated'].sum(),
                                group_stats['Collections'].sum(), group_stats['AIPs'].sum(),
                                group_stats['File_IDs'].sum(), df_group['Format_Type'].nunique(),
                                df_group['Format_Standardized_Name'].nunique(),
                                df_group['Format_Identification'].nunique()]

    # Returns the information in a dataframe. Row index is the group_code and columns are Size (TB), Collections,
    # AIPs, File_IDs, Format Types, Format Standardized Names, and Format Identifications.
    return group_stats


def file_count_ranges(category, df_group):
    """Uses the data from the archive_formats_by_group report to calculate the number of instances of the category
    within each range of file_ids (1-9, 10-99, 100-999, etc.). Returns a dataframe. """

    # Makes a series with the number of file_ids for each instance of the category, regardless  of group.
    df_cat = df_group.groupby(df_group[category])['File_IDs'].sum()

    # Makes series with the subset of the archive_formats_by_group report data with the specified numbers of file_ids.
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


def format_id_frequency(totals, df_group):
    """Uses the data from the archive_formats_by_group report to calculate the frequency for every format
    identification (name, version, registry key), which includes the file_id count, percentage of file_ids, size in GB,
    and percentage of size. Returns a dataframe sorted largest to smallest by file_id count since the items of most
    interest are the most common formats. """

    # Make series for file_id counts and file_id percentages.
    format_count = df_group.groupby(df_group['Format_Identification'])['File_IDs'].sum()
    format_percentage = (format_count / totals['Files']) * 100
    format_percentage = round(format_percentage, 2)
    format_percentage = format_percentage.rename('File_IDs_Percentage')

    # Make series for total size and size percentages.
    size = df_group.groupby(df_group['Format_Identification'])['Size_GB'].sum()
    size_percentage = (size / totals['Size']) * 100
    size_percentage = round(size_percentage, 2)
    size_percentage = size_percentage.rename('Size_GB_Percentage')

    # Combine all the series into a single dataframe and sort largest to smallest by file_ids.
    format_ids = pd.concat([format_count, format_percentage, size, size_percentage], axis=1)
    format_ids = format_ids.sort_values(by='File_IDs', ascending=False)

    # Returns the dataframe. Row index is the file_ids and columns are the four frequency measures.
    return format_ids


def get_report_paths(report_folder_path):
    """Finds the path to the three reports used as script input.
    Returns the three paths and a list of any missing files."""

    # Makes variables to store the paths, if found.
    formats_by_aip_path = None
    formats_by_group_path = None
    usage_path = None

    # Searches the report folder for the expected files, and if found updates the variable with the file name.
    # These files include dates, so the entire file name cannot be predicted by the script.
    for file in os.listdir(report_folder_path):
        if file.startswith("archive_formats_by_aip") and file.endswith(".csv"):
            formats_by_aip_path = os.path.join(report_folder_path, file)
        elif file.startswith("archive_formats_by_group") and file.endswith(".csv"):
            formats_by_group_path = os.path.join(report_folder_path, file)
        elif file.startswith("usage_report_") and file.endswith(".csv"):
            usage_path = os.path.join(report_folder_path, file)

    # Tests if all three paths were found, and if not adds the missing ones to a list.
    missing_list = []
    if not formats_by_aip_path:
        missing_list.append("archive_formats_by_aip.csv")
    if not formats_by_group_path:
        missing_list.append("archive_formats_by_group.csv")
    if not usage_path:
        missing_list.append("usage_report.csv")

    # Returns the results. The errors list is empty if all three files were found.
    return formats_by_aip_path, formats_by_group_path, usage_path, missing_list


def group_overlap(category, df_group):
    """Uses the data from the archive_formats_by_group report to calculate the number of groups and
    a list of the groups which have each instance of the category, for example format type. Returns a dataframe. """

    # Makes a series with a list of group names for each instance of the category.

    groups_list = df_group.groupby(df_group[category])['Group'].unique()
    groups_list = groups_list.rename('Group_List')

    # Makes a series with the number of groups for each instance of the category.
    groups_count = groups_list.str.len()
    groups_count = groups_count.rename('Groups')

    # Converts the list from a list to a comma-separated string for easier readability in Excel.
    # Wait to do this until after groups_count so that the count is correct.
    groups_list = groups_list.apply(", ".join)

    # Combines the count and the list series into a single dataframe.
    # Had to do these separately to get the counts for each instance separately.
    groups_per_category = pd.concat([groups_count, groups_list], axis=1)

    # Sorts the values by the number of groups, largest to smallest.
    # The primary use for this data is to see what the most groups have in common.
    groups_per_category = groups_per_category.sort_values(by='Groups', ascending=False)

    # Returns the dataframe. Row index is the category and columns are Groups, Group List.
    return groups_per_category


def groupby_risk(df_group, groupby_list):
    """Makes a dataframe with the number of file ids, size in GB, and format identifications
    for each instance of the column or columns included in the groupby_list.
    Returns the dataframe."""

    # Calculates the totals.
    # File IDs and Size (GB) are sums; Format Identification is the number of unique values.
    # The index is reset so that the groupby_list columns are maintained as columns and don't become the index.
    aggregation_methods = {'File_IDs': 'sum', 'Size_GB': 'sum', 'Format_Identification': 'nunique'}
    df = df_group.groupby(groupby_list).agg(aggregation_methods).reset_index()

    # Renames one of the columns, to reflect it being a total.
    # The other column names worked equally well as labels for the individual or aggregate data.
    df.rename(columns=({'Format_Identification': 'Format_Identifications'}), inplace=True)

    # Rounds Size (GB) to 2 decimal places to make it easier to read.
    df['Size_GB'] = round(df['Size_GB'], 2)

    return df


def one_category(category, totals, df_aip, df_group):
    """Uses the data from both ARCHive format reports to calculate subtotals of collection, AIP, and file_id counts
    and size in GB per each instance of the category, for example format type. Returns a dataframe. """

    # Creates a series for each count type (collections, AIPs, and file_ids) and size for each instance of the category.
    collections = df_aip.groupby(category)['Collection'].nunique()
    aips = df_aip.groupby(category)['AIP'].nunique()
    files = df_group.groupby(category)['File_IDs'].sum()
    size = df_group.groupby(category)['Size_GB'].sum()

    # Creates a series for the percentage of each count type and size for each instance of the category.
    # The percentage is rounded to two decimal places.
    # Also renames the series to be more descriptive.

    collections_percent = (collections / totals['Collections']) * 100
    collections_percent = round(collections_percent, 2)
    collections_percent = collections_percent.rename('Collections_Percentage')

    aips_percent = (aips / totals['AIPs']) * 100
    aips_percent = round(aips_percent, 2)
    aips_percent = aips_percent.rename('AIPs_Percentage')

    files_percent = (files / totals['Files']) * 100
    files_percent = round(files_percent, 2)
    files_percent = files_percent.rename('File_IDs_Percentage')

    size_percent = (size / totals['Size']) * 100
    size_percent = round(size_percent, 2)
    size_percent = size_percent.rename('Size_GB_Percentage')

    # Combines all the count and percentage series into a single dataframe.
    result = pd.concat([collections, collections_percent, aips, aips_percent, files, files_percent, size, size_percent],
                       axis=1)

    # Renames Collection and AIP columns to plural to be more descriptive.
    result = result.rename({'Collection': 'Collections', 'AIP': 'AIPs'}, axis=1)

    # Returns the dataframe. Row index is the category and columns are Collections, Collections Percentage, AIPs,
    # AIPs Percentage, File_IDs, File_IDs Percentage.
    return result


def size_ranges(category, df_group):
    """Uses the data from the archive_formats_by_group report to calculate the number of instances of the category
    within each range of total size (0-249 GB, 250-499 GB, etc.). Returns a dataframe. """

    # Makes a series with the total size for each instance of the category, regardless of group.
    df_cat = df_group.groupby(df_group[category])['Size_GB'].sum()

    # Makes series with the subset of the archive_formats_by_group report data with the specified numbers of file_ids.
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


def spreadsheet_frequency(df_aip, df_group, usage, output_folder):
    """
    Calculates summaries based on counts and percentages of different categories
    and saves them to a spreadsheet named ARCHive-Formats-Analysis_Frequency.xlsx.
    """
    # Makes the ARCHive overview dataframe (summary statistics by group).
    overview = archive_overview(df_aip, df_group, usage)

    # Saves totals to a dictionary for calculating percentages in other dataframes.
    # Use these totals each time so collection and AIP counts aren't inflated by multiple identifications.
    # Counts for file and size are inflated because don't have file name in the data and therefore can't deduplicate.
    totals_dict = {'Collections': overview['Collections']['total'],
                   'AIPs': overview['AIPs']['total'],
                   'Files': overview['File_IDs']['total'],
                   'Size': overview['Size_GB_Inflated']['total']}

    # Makes the format type summary (collection, AIP, file_id, and size counts and percentages).
    format_types = one_category("Format_Type", totals_dict, df_aip, df_group)

    # Makes the format standardized name summary (collection, AIP, file_id, and size counts and percentages).
    format_names = one_category("Format_Standardized_Name", totals_dict, df_aip, df_group)

    # Makes a format identifications summary (file_id and size count and percentage).
    format_ids = format_id_frequency(totals_dict, df_group)

    # Saves each summary as a separate sheet in an Excel spreadsheet.
    with pd.ExcelWriter(os.path.join(output_folder, f"ARCHive-Formats-Analysis_Frequency.xlsx")) as results:
        overview.to_excel(results, sheet_name="Group Overview", index_label="Group")
        format_types.to_excel(results, sheet_name="Format Types")
        format_names.to_excel(results, sheet_name="Format Names")
        format_ids.to_excel(results, sheet_name="Format IDs")


def spreadsheet_group_overlap(df_group, output_folder):
    """
    Calculates the groups which contain the same instances of different categories
    (format type, format name, format ids) and saves them to a spreadsheet named
    ARCHive-Formats Analysis_Group_Overlap.xlsx.
    """
    # Makes a dataframe with the number of groups and list of groups that have each format type.
    groups_per_type = group_overlap("Format Type", df_group)

    # Makes a dataframe with the number of groups and list of groups that have each format standardized name.
    groups_per_name = group_overlap("Format Standardized Name", df_group)

    # Makes a dataframe with the number of groups and list of groups that have each format identification.
    groups_per_id = group_overlap("Format Identification", df_group)

    # Saves each dataframe as a separate sheet in an Excel spreadsheet.
    with pd.ExcelWriter(os.path.join(output_folder, f"ARCHive-Formats-Analysis_Group-Overlap.xlsx")) as results:
        groups_per_type.to_excel(results, sheet_name="Groups per Type")
        groups_per_name.to_excel(results, sheet_name="Groups per Name")
        groups_per_id.to_excel(results, sheet_name="Groups per Format ID")


def spreadsheet_ranges(df_group, output_folder):
    """
    Calculates the the number of instances of format types and format standardized names
    within predetermined ranges of file id counts or size and saves them to a spreadsheet named
    ARCHive-Formats Analysis_Ranges.xlsx.
    """
    # Makes dataframes with the number of format standardized names within different ranges of file_id counts and sizes.
    format_name_ranges = file_count_ranges("Format Standardized Name", df_group)
    format_name_sizes = size_ranges("Format Standardized Name", df_group)

    # Makes dataframes with the number of format identifications within different ranges of file_id counts and sizes.
    format_id_ranges = file_count_ranges("Format Identification", df_group)
    format_id_sizes = size_ranges("Format Identification", df_group)

    # Saves each dataframe as a separate sheet in an Excel spreadsheet.
    with pd.ExcelWriter(os.path.join(output_folder, f"ARCHive-Formats-Analysis_Ranges.xlsx")) as results:
        format_name_ranges.to_excel(results, sheet_name="Format Name Ranges", index_label="File_ID Count Range")
        format_name_sizes.to_excel(results, sheet_name="Format Name Sizes", index_label="Size Range")
        format_id_ranges.to_excel(results, sheet_name="Format ID Ranges", index_label="File_ID Count Range")
        format_id_sizes.to_excel(results, sheet_name="Format ID Sizes", index_label="Size Range")


def spreadsheet_risk(df_group, output_folder):
    """
    Calculates different measures of the amount at each of the four NARA risk levels,
    No Match, High, Moderate, and Low,
    and saves them to a spreadsheet named ARCHive-Formats-Analysis_Risk.xlsx.
    """
    # Assigns an order to the NARA risk categories, so results are in order of increasing risk.
    risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
    df_group['NARA_Risk Level'] = pd.Categorical(df_group['NARA_Risk Level'], risk_order, ordered=True)

    # Makes a new column to classify the type of NARA preservation action plan.
    conditions = [(df_group['NARA_Proposed Preservation Plan'].notnull()) &
                  (df_group['NARA_Proposed Preservation Plan'].str.startswith("Depends on version")),
                  (df_group['NARA_Proposed Preservation Plan'].notnull()) &
                  (df_group['NARA_Proposed Preservation Plan'].str.startswith("Further research is required")),
                  df_group['NARA_Proposed Preservation Plan'].isnull(),
                  df_group['NARA_Proposed Preservation Plan'] == "Retain",
                  (df_group['NARA_Proposed Preservation Plan'].notnull()) &
                  (df_group['NARA_Proposed Preservation Plan'].str.startswith("Retain ")),
                  (df_group['NARA_Proposed Preservation Plan'].notnull()) &
                  (df_group['NARA_Proposed Preservation Plan'].str.startswith("Transform"))]
    plan_type = ["Depends on version", "Further research required", "No plan", "Retain", "Retain but act", "Transform"]
    df_group["NARA_Plan_Type"] = np.select(conditions, plan_type)

    # Calculates the dataframe for each risk summary.
    # The first four are the amount at each NARA risk level for different categories of data
    # and the last is the match method between format identifications and NARA risk.
    archive_risk = groupby_risk(df_group, ['NARA_Risk Level'])
    dept_risk = groupby_risk(df_group, ['Group', 'NARA_Risk Level'])
    type_risk = groupby_risk(df_group, ['Format Type', 'NARA_Risk Level'])
    plan_risk = groupby_risk(df_group, ['NARA_Plan_Type', 'NARA_Risk Level'])
    match = groupby_risk(df_group, ['NARA_Match_Type'])

    # Saves each dataframe as a separate sheet in an Excel spreadsheet.
    with pd.ExcelWriter(os.path.join(output_folder, "ARCHive-Formats-Analysis_Risk.xlsx")) as results:
        archive_risk.to_excel(results, sheet_name="ARCHive Risk Overview", index=False)
        dept_risk.to_excel(results, sheet_name="Department Risk Overview", index=False)
        type_risk.to_excel(results, sheet_name="Format Type Risk", index=False)
        plan_risk.to_excel(results, sheet_name="NARA Plan Type Risk", index=False)
        match.to_excel(results, sheet_name="NARA Match Types", index=False)


if __name__ == '__main__':

    # Verifies the required argument is present and the path is valid.
    # If there was an error, prints the error and exits the script.
    report_folder, error_message = check_argument(sys.argv)
    if error_message:
        print(error_message)
        print("Script usage: python path/reports.py report_folder")
        sys.exit(1)

    # Gets paths of the three reports to be analyzed, which are in report_folder.
    # If any were not found (missing is not empty), prints the missing one(s) and exits the script.
    formats_by_aip_report, formats_by_group_report, usage_report, missing = get_report_paths(report_folder)
    if len(missing) > 0:
        for file_name in missing:
            print(f"Could not find {file_name} in '{report_folder}'.")
        print("Please add the missing report(s) to the report folder and run this script again.")
        sys.exit(1)

    # Makes dataframes from both ARCHive format reports.
    df_formats_by_aip = pd.read_csv(formats_by_aip_report)
    df_formats_by_group = pd.read_csv(formats_by_group_report)

    # Makes a spreadsheet in the folder with the ARCHive reports
    # with summaries based on counts and percentages of collection, AIP, file ids, and/or size.
    spreadsheet_frequency(df_formats_by_aip, df_formats_by_group, usage_report, report_folder)

    # Makes a spreadsheet in the folder with the ARCHive reports
    # with summaries of group overlap for each instance of format type, format name, and format id.
    spreadsheet_group_overlap(df_formats_by_group, report_folder)

    # Makes a spreadsheet in the folder with the ARCHive reports
    # with summaries of the number of instances within predetermined ranges of file id counts or size.
    spreadsheet_ranges(df_formats_by_group, report_folder)

    # Makes a spreadsheet in the folder with the ARCHive reports
    # with summaries of the amount of content at different NARA risk levels.
    spreadsheet_risk(df_formats_by_group, report_folder)
