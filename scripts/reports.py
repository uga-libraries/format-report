"""Calculates subtotals of collection, AIP, and file_id counts for different categories: groups, format types,
format standardized names, and combinations of those. Once file size is added to the ARCHive format reports,
size subtotals will be added. The results are saved to an Excel workbook, with one spreadsheet per subtotal,
to use for analyzing formats in ARCHive.

The script uses information from three sources, all CSVs:
    * usage report: downloaded from ARCHive. Has the amount ingested (by file and size) for each group.
    * archive_formats report: Organized by format. Has group, file_id count, and format information.
    * archive_formats_by_aip report: For each AIP, has group, collection, aip id, and format information.

Definition of terms:
    * Group: ARCHive group name, which is the department or departments responsible for the content.
    * Format type: category of the format, for example audio, image, or text.
    * Format standardized name: a simplified version of the name, for example removing version information.
    * Format identification: a combination of the format name, version, and registry key (usually PRONOM).

Ideas for additional reports:
    * Map NARA and/or LOC risk assessments to the most common formats.
    * Compares the current report to a previous one to show change over time.
    * Add groups and type to common formats (risk analysis) for additional information.

# Unlike Excel, pandas does not merge difference of capitalization, e.g. MPEG Video and MPEG video, when subtotaling.
"""
# Before running this script, run update_standardization.py and merge_format_reports.py

# Usage: python /path/reports.py report_folder
# Report folder should contain the merged format CSVs and usage report. Script output is saved to this folder as well.

import csv
import datetime
import os
import pandas as pd
import sys

# TODO: explain input of the functions better.
# TODO: vocabulary check. Wasn't consistent about terms for format  name, format id, or the different input reports.


def archive_overview():
    """Gets TBs, AIPs, collections, and file_ids per group and the total for ARCHive using the usage and both archive
    format reports. Returns the information in a dataframe. """

    def size_and_aips_count():
        """Gets the size in TB and AIP count for each group from the usage report and calculates the total size and
        AIP count for all groups combined. Returns a dictionary with the group code as the keys and lists with the
        size and number of AIPs as the values."""

        # TODO: AIP count from usage isn't matching what get from formats. Which to use? From 10-26 data:
        """
        BMAC: 27728 usage, 27713 formats
        DLG: 18802 usage, 18759 formats
        DLG-Hargrett: 1650, 1649 formats
        Hargrett: same (45)
        Russell: 4286 usage, 4280 formats
        """

        # Group Names maps the human-friendly version of group names from the usage report to the ARCHive group code
        # which is used in both archive format reports and in ARCHive metadata generally.
        group_names = {'Brown Media Archives': 'bmac', 'Digital Library of Georgia': 'dlg',
                       'DLG & Hargrett': 'dlg-hargrett', 'DLG & Map and Government Information Library': 'dlg-magil',
                       'Hargrett': 'hargrett', 'Russell': 'russell'}

        # Makes a dictionary for storing data for each group.
        group_data = {}

        # Gets the data from the usage report.
        with open(usage_report, 'r') as usage:
            usage_read = csv.reader(usage)

            # Skips the header row.
            next(usage_read)

            # Gets data from each row. A row can have data on a group, an individual user, or be blank.
            for row in usage_read:

                # Processes data from each group. There is only one row per group in the report.
                # Skips any rows that are blank or are individuals rather than groups.
                # row[0] is group, row[1] is AIP count, and row[2] is size with the unit of measurement.
                if row and row[0] in group_names:

                    # Group code is fine as is.
                    group_code = group_names[row[0]]

                    # Changes AIP count from a string to an integer so the total across all groups can be calculated.
                    aip_count = int(row[1])

                    # Separates the size number from the unit of measurement by splitting the data at the space and
                    # converts the size to TB. Example: 100 GB becomes 0.1. All sizes are converted from a string to a
                    # float (decimal numbers) to do the necessary math and to round the result. If it encounters a unit
                    # of measurement that wasn't anticipated, the script prints a warning message.
                    size, unit = row[2].split()
                    if unit == 'Bytes':
                        size = float(size) / 1000000000000
                    elif unit == 'KB':
                        size = float(size) / 1000000000
                    elif unit == 'MB':
                        size = float(size) / 1000000
                    elif unit == 'GB':
                        size = float(size) / 1000
                    elif unit == 'TB':
                        size = float(size)
                    else:
                        size = 0
                        print("WARNING! Unexpected unit type:", unit)

                    # Rounds the size in TB to one decimal place so the number is easier to read.
                    size = round(size, 1)

                    # Adds the results for this group to the dictionary.
                    group_data[group_code] = ([size, aip_count])

        # Makes the dictionary into a dataframe so it can be combined with the collection and file_id counts.
        group_dataframe = pd.DataFrame.from_dict(group_data, orient='index', columns=['Size', 'AIPs'])

        # Returns the dataframe. Row index is the group_code and columns are the size in TBs and AIPs count.
        return group_dataframe

    # Gets the size (TB) and number of AIPs per group from the usage report.
    size_and_aips_by_group = size_and_aips_count()

    # Gets the number of collections per group from the archive_formats_by_aip report.
    # Only counts collections with AIPs, which may result in a difference between this count and ARCHive's count.
    # Additionally, dlg-hargrett collections in ARCHive that are part of Turningpoint are counted as dlg.
    collections_by_group = df_aip.groupby('Group')['Collection'].nunique()

    # Gets the number of format types per group from the archive_formats_by_aip report.
    types_by_group = df_aip.groupby('Group')['Format_Type'].nunique()

    # Gets the number of format standardized names per group from the archive_formats_by_aip report.
    formats_by_group = df_aip.groupby('Group')['Format_Standardized_Name'].nunique()

    # Gets the number of files per group from the archive_formats report.
    # These numbers are inflated by files with more than one format identification.
    files_by_group = df.groupby('Group')['File_IDs'].sum()

    # Gets the number of format identifications per group from the archive_formats report.
    format_ids_by_group = df.groupby('Group')[format_id].nunique()

    # Combines the dataframes into a single dataframe.
    group_frames = [size_and_aips_by_group["Size"], collections_by_group, size_and_aips_by_group["AIPs"],
                    files_by_group, types_by_group, formats_by_group, format_ids_by_group]
    group_combined = pd.concat(group_frames, axis=1)

    # Renames columns to be more accurate.
    rename = {"Size": "Size (TB)", "Collection": "Collections", "Format_Type": "Format_Types",
              "Format_Standardized_Name": "Format_Standardized_Names",
              "Format Identification (Name|Version|Key)": "Format Identifications (Name|Version|Key)"}
    group_combined = group_combined.rename(columns=rename)

    # Replace cells without values (one group has no files yet) with 0.
    group_combined = group_combined.fillna(0)

    # Adds the column totals.
    group_combined.loc['total'] = [group_combined['Size (TB)'].sum(), group_combined['Collections'].sum(),
                                   group_combined['AIPs'].sum(), group_combined['File_IDs'].sum(),
                                   df['Format_Type'].nunique(), df['Format_Standardized_Name'].nunique(),
                                   df[format_id].nunique()]

    # Makes all rows except size integers, since they are counts and therefore must be whole numbers.
    group_combined['Collections'] = group_combined['Collections'].astype(int)
    group_combined['AIPs'] = group_combined['AIPs'].astype(int)
    group_combined['File_IDs'] = group_combined['File_IDs'].astype(int)

    # Returns the information in a dataframe.
    return group_combined


def one_category(category, totals):
    """Makes and returns a dataframe with subtotals of collection, AIP, and file counts based on one criteria,
    for example Format Type or Format Standardized Name. """

    # Creates a series for each count type (collections, AIPs, and file ids) for each instance of the category.
    collections = df_aip.groupby(category)['Collection'].nunique()
    aips = df_aip.groupby(category)['AIP'].nunique()
    files = df.groupby(category)['File_IDs'].sum()

    # Creates a series for the percentage of each count type (collections, AIPs, and file ids) for each instance of
    # the category. The percentage is rounded to two decimal places. Renames the series to be more accurate.

    collections_percent = (collections / totals[0]) * 100
    collections_percent = round(collections_percent, 2)
    collections_percent = collections_percent.rename("Collections Percentage")

    aips_percent = (aips / totals[1]) * 100
    aips_percent = round(aips_percent, 2)
    aips_percent = aips_percent.rename("AIPs Percentage")

    files_percent = (files / totals[2]) * 100
    files_percent = round(files_percent, 2)
    files_percent = files_percent.rename("File_IDs Percentage")

    # Combines all six count and percentage series into a single dataframe.
    result = pd.concat([collections, collections_percent, aips, aips_percent, files, files_percent], axis=1)

    # Renames Collection and AIP columns to plural to be more accurate labels.
    result = result.rename({"Collection": "Collections", "AIP": "AIPs"}, axis=1)

    return result


def two_categories(category1, category2):
    """Makes and returns a dataframe with subtotals of collection, AIP, and file counts based on two criteria."""

    # Uses the archive_formats_by_aip report data to get counts of unique collections and unique AIPs.
    result = df_aip[[category1, category2, 'Collection', 'AIP']].groupby([category1, category2]).nunique()

    # Renames the column headings to be plural (Collections, AIPs) to be more accurate.
    result = result.rename({"Collection": "Collections", "AIP": "AIPs"}, axis=1)

    # Uses the archive_formats report data to get counts of file identifications. The counts are inflated by files
    # with multiple possible format identifications.
    files_result = df.groupby([category1, category2])['File_IDs'].sum()

    # Adds the file subtotal to the dataframe with the collection and AIP subtotals.
    result = pd.concat([result, files_result], axis=1)

    return result


def count_ranges(category):
    """Makes and returns a dataframe with the number of instances for the category with 1-9 file identifications,
    10-99, 100-999, etc. """

    # Makes a series with the number of file ids for each instance of the category, regardless  of group.
    df_cat = df.groupby(df[category])['File_IDs'].sum()

    # Makes series with the subset of the archive_formats_by_aip report data with the specified numbers of file ids.
    ones = df_cat[(df_cat < 10)]
    tens = df_cat[(df_cat >= 10) & (df_cat < 100)]
    hundreds = df_cat[(df_cat >= 100) & (df_cat < 1000)]
    thousands = df_cat[(df_cat >= 1000) & (df_cat < 10000)]
    ten_thousands = df_cat[(df_cat >= 10000) & (df_cat < 100000)]
    hundred_thousands_plus = df_cat[(df_cat >= 100000)]

    # Makes a dictionary with the range labels and the count of unique instances of the category in each range.
    counts = {"File_ID Count Range": ["1-9", "10-99", "100-999", "1000-9999", "10000-99999", "100000+"],
              f"Number of Formats ({category})": [ones.count(), tens.count(), hundreds.count(), thousands.count(),
                                                  ten_thousands.count(), hundred_thousands_plus.count()]}

    # Makes a dataframe out of the dictionary with the counts and returns that result.
    result = pd.DataFrame(counts, columns=["File_ID Count Range", f"Number of Formats ({category})"])
    return result


def group_overlap(category):
    """For each instance of the specified category, which might be format type, format standardized name,
    or format identification, makes a dataframe with the number of groups and a list of groups."""

    # Gets a series with a list of group names for each instance of the category.
    groups_list = df.groupby(df[category])['Group'].unique()

    # Makes a series with the number of groups for each instance of the category.
    groups_count = groups_list.str.len()

    # Combines the count and the list series into a single dataframe. Had to do separately to get the counts for each
    # instance separately.
    # TODO: there is probably a more streamlined way to do this.
    groups_per_category = pd.concat([groups_count, groups_list], axis=1)

    # Renames the columns to be more accurate. Without renaming, both are named Group.
    groups_per_category.columns = ['Groups', 'Group_List']

    # Sorts the values by the number of groups, largest to smallest. The primary use for this data is to see what the
    # most groups have in common.
    groups_per_category = groups_per_category.sort_values(by='Groups', ascending=False)

    # TODO: the group is formatted as a list and would prefer a string so it is easier to read in Excel.
    # This was from stackoverflow but doesn't make a change. Index ['Group_list'] also returns row label so maybe it
    # isn't really getting me to the value itself?
    # groups_per_category['Group_List'].apply(', '.join)
    # print(groups_per_category)

    return groups_per_category


# Makes the report folder (script argument) the current directory. Displays an error message and quits the script if
# the argument is missing or not a valid directory.
try:
    report_folder = sys.argv[1]
    os.chdir(report_folder)
except (IndexError, FileNotFoundError):
    print("The report folder path was either not given or is not a valid directory. Please try the script again.")
    print("Script usage_report: python /path/reports.py /path/reports [/path/standardize_formats.csv]")
    exit()

# Gets paths for the data files used in this script, which should be in the report folder.
# If any are not found, prints an error and quits the script.
formats_by_aip_report = False
formats_report = False
usage_report = False

for file in os.listdir('.'):
    # This CSV has one line per AIP and unique format.
    if file.startswith('archive_formats_by_aip') and file.endswith('.csv'):
        formats_by_aip_report = file
    # This CSV has one line per group and unique format.
    elif file.startswith('archive_formats_') and file.endswith('.csv'):
        formats_report = file
    # This CSV has user and group ingest information.
    elif file.startswith('usage_report_') and file.endswith('.csv'):
        usage_report = file

# Tests for if all reports were found, and if not prints an error and quits the script.
missing = []
if not formats_by_aip_report:
    missing.append("Could not find archive formats_by_aip_report csv in the report folder.")
if not formats_report:
    missing.append("Could not find archive formats_report csv in the report folder.")
if not usage_report:
    missing.append("Could not find usage_report report csv in the report folder.")

if len(missing) > 0:
    for message in missing:
        print(message)
    print("Please add the missing report(s) to the reports folder and run this script again.")
    exit()

# Makes dataframes from both format reports.
df = pd.read_csv(formats_report)
df_aip = pd.read_csv(formats_by_aip_report)

# Adds a column to the "by format" dataframe with name|version|registry_key, which is the format identification.
# Saves the column name to a variable since it is long and repeated several times in the script.
# TODO: three of the Hyptertext Markup Language entries have nothing in Format_Version instead of NO VALUE
#  (fmt/471, NO VALUE, and fmt/96) which means their format id is not made. Error in merging script?
format_id = 'Format Identification (Name|Version|Key)'
df[format_id] = df['Format_Name'] + "|" + df['Format_Version'] + "|" + df['Registry_Key']

# Generate a dataframe or series for each type of analysis. Each analysis will be saved as a separate sheet in Excel.

# Makes the ARCHive overview dataframe (TBS, AIPs, Collections, and Files by group).
overview = archive_overview()

# Saves the ARCHive collection, AIP, and file totals to a list for calculating percentages in other dataframes.
# Cannot just get the total of columns in those dataframes because that will over-count anything with multiple formats.
# TODO: have archive_overview() return the totals list?
totals_list = [overview['Collections']['total'], overview['AIPs']['total'], overview['File_IDs']['total']]

# Makes the format type dataframe (collection, AIP, and file_id counts and percentages).
format_types = one_category("Format_Type", totals_list)

# Makes the format standardized name dataframe (collection, AIP, and file_id counts and percentages).
format_names = one_category("Format_Standardized_Name", totals_list)

# Makes a dataframe with all standardized format names with over 500 file_id counts, to use for risk analysis.
common_formats = format_names[format_names.File_IDs > 500]

# Makes a dataframe with subtotals first by format type and then subdivided by group.
type_by_group = two_categories("Format_Type", "Group")

# Makes a dataframe with subtotals first by format type and then subdivided by format standardized name.
type_by_name = two_categories("Format_Type", "Format_Standardized_Name")

# Makes a dataframe with subtotals first by format standardized name and then by group.
name_by_group = two_categories("Format_Standardized_Name", "Group")

# Makes a series with the file_id count for every format identification (name, version, registry key).
# The dataframe is sorted largest to smallest since the items of most interest are the most common formats.
format_ids = df.groupby(df[format_id])['File_IDs'].sum()
format_ids = format_ids.sort_values(ascending=False)

# Makes a dataframe with the number of groups and list of groups that have each format type.
groups_per_type = group_overlap("Format_Type")

# Makes a dataframe with the number of groups and list of groups that have each format standardized name.
groups_per_name = group_overlap("Format_Standardized_Name")

# Makes a dataframe with the number of groups and list of groups that have each format identification.
groups_per_id = group_overlap(format_id)

# Makes a dataframe with the number of format standardized names within different ranges of file_id counts.
format_name_ranges = count_ranges("Format_Standardized_Name")

# Makes a dataframe with the number of format identifications within different ranges of file_id counts.
format_id_ranges = count_ranges("Format Identification (Name|Version|Key)")

# Saves each dataframe or series as a spreadsheet in an Excel workbook.
# The workbook filename includes today's date, formatted YYYYMM, and is saved in the reports folder.
# If the row label is just an automatically-supplied number, exclude from Excel with index=False.
today = datetime.datetime.now().strftime("%Y-%m")
with pd.ExcelWriter(f'ARCHive Formats Analysis_{today}.xlsx') as results:
    overview.to_excel(results, sheet_name="Group Overview")
    format_types.to_excel(results, sheet_name="Format Types")
    format_names.to_excel(results, sheet_name="Format Names")
    format_name_ranges.to_excel(results, sheet_name="Format Name Ranges", index=False)
    common_formats.to_excel(results, sheet_name="Risk Analysis")
    type_by_group.to_excel(results, sheet_name="Type by Group")
    type_by_name.to_excel(results, sheet_name="Type by Name")
    name_by_group.to_excel(results, sheet_name="Name by Group")
    format_ids.to_excel(results, sheet_name="Format ID")
    format_id_ranges.to_excel(results, sheet_name="Format ID Ranges", index=False)
    groups_per_type.to_excel(results, sheet_name="Groups per Type")
    groups_per_name.to_excel(results, sheet_name="Groups per Name")
    groups_per_id.to_excel(results, sheet_name="Groups per Format ID")
