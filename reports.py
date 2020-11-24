"""Calculates subtotals of collection, AIP, and file identification counts for different categories: format types,
format standardized names, groups, and combinations of those. Once file size is added to the ARCHive format reports,
size subtotals will be added. The results are saved to an Excel workbook, with one spreadsheet per subtotal,
to use for analyzing formats in ARCHive.

# The script uses information from three sources, all CSVs:
    * usage report: downloaded from ARCHive. Has the amount ingested (by file and size) for each group.
    * archive formats: Organized by unique format. Has group, file count, format type, and format standard name.
    * archive formats by aip: For each AIP, has group, collection, aip id, and format information.

Ideas for additional reports:
    * Map NARA and/or LOC risk assessments to the most common formats.
    * Compares the current report to a previous one to show change over time.
    * The number of unique formats for each standardized name, type, or group.
    * The average amount of format variety per collection or AIP.
    * Groups per type, name, and format id for overlap. Include number of groups and which groups.
    * Add number of types, standard formats and/or unique formats to the archive overview to show group variation.
    * Add groups and type to common formats (risk analysis) for additional information.
    * The number of standardized names with 1-9, 10-999, 100-999, etc. files.
    * Analyze the unique format identifications (name+version+PUID). List 500+ and file count ranges like previous idea.

Might be helpful to make a function for the each of the reports that are more than a few lines to organize better.
"""
# Before running this script, run update_standardization.py and merge_format_reports.py

# Usage: python /path/reports.py report_folder
# Report folder should contain the merged format CSVs and usage report. Script output is saved to this folder as well.

import csv
import datetime
import os
import pandas as pd
import sys


def archive_overview():
    """Gets TBs, AIPs, collections, and file ids per group and the total for ARCHive using the usage and format reports.
    Returns the information in a dataframe."""

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
        # which is used in the formats reports and in ARCHive metadata generally.
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

        # Makes the dictionary into a dataframe so it can be combined with the collection and file counts.
        group_dataframe = pd.DataFrame.from_dict(group_data, orient='index', columns=['Size', 'AIPs'])

        # Returns the dataframe. Row index is the group_code and columns are the size in TBs and AIPs count.
        return group_dataframe

    # Gets the size (TB) and number of AIPs per group from the usage report.
    size_and_aips_by_group = size_and_aips_count()

    # Gets the number of collections per group from the formats by AIP report.
    # Only counts collections with AIPs, which may result in a difference between this count and ARCHive's count.
    # Additionally, dlg-hargrett collections in ARCHive that are part of Turningpoint are counted as dlg.
    collections_by_group = df_aip.groupby('Group')['Collection'].nunique()

    # Gets the number of files per group from the other formats report.
    # These numbers are inflated by files with more than one format identification.
    files_by_group = df.groupby('Group')['File_IDs'].sum()

    # Combines the dataframes into a single dataframe.
    group_frames = [size_and_aips_by_group["Size"], collections_by_group, size_and_aips_by_group["AIPs"], files_by_group]
    group_combined = pd.concat(group_frames, axis=1)

    # Renames the Size and Collection columns.
    group_combined = group_combined.rename(columns={"Size": "Size (TB)", "Collection": "Collections"})

    # Replace cells without values (one group has no files yet) with 0.
    group_combined = group_combined.fillna(0)

    # Adds the column totals.
    group_combined.loc['total'] = [group_combined['Size (TB)'].sum(), group_combined['Collections'].sum(),
                                   group_combined['AIPs'].sum(), group_combined['File_IDs'].sum()]

    # Makes all rows except size integers, since they are counts and must be whole numbers.
    group_combined['Collections'] = group_combined['Collections'].astype(int)
    group_combined['AIPs'] = group_combined['AIPs'].astype(int)
    group_combined['File_IDs'] = group_combined['File_IDs'].astype(int)

    # Returns the information in a dataframe.
    return group_combined


def percentage(dataframe, total, new_name):
    """Makes a new dataframe that is the percent of each value in an existing dataframe.
    This is a short function but repeats in the code several times."""

    # Calculates the percentage. It is stored as a number and does not have % sign.
    new_df = (dataframe / total) * 100

    # Rounds the  percentage to two decimal places.
    new_df = round(new_df, 2)

    # Renames the column to the specified name. Otherwise, it will the same as the original dataframe.
    # Column names matter since they become the column header in the results Excel workbook.
    new_df = new_df.rename(new_name)

    return new_df


def two_categories(cat1, cat2):
    """Makes and returns a dataframe with subtotals of collection, AIP, and file counts based on two criteria. Not
    that long, but use this three times and makes it easy to add additional comparisons when needed."""

    # The collection and AIP subtotals come from df_aip to get counts of unique collections and unique AIPs.
    result = df_aip[[cat1, cat2, 'Collection', 'AIP']].groupby([cat1, cat2]).nunique()

    # Renames the column headings to be plural (Collections, AIPs) to be more accurate.
    result = result.rename({"Collection": "Collections", "AIP": "AIPs"}, axis=1)

    # The file subtotal comes from df and is inflated by files with multiple format identifications.
    files_result = df.groupby([cat1, cat2])['File_IDs'].sum()

    # Adds the file subtotal to the dataframe with the collection and AIP subtotals.
    result = pd.concat([result, files_result], axis=1)

    return result


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


# The rest of this script uses pandas to calculate the collection count, AIP count, and file count for different
# combinations of data categories. These categories are:
#   * Group: ARCHive group name, which is the department or departments responsible for the content.
#   * Format type: category of the format, for example audio, image, or text.
#   * Format standardized name: a simplified version of the name, for example removing version information.


# Makes the ARCHive overview report (TBS, AIPs, Collections, and Files by group).
overview = archive_overview()

# Saves the ARCHive collection, AIP, and file totals to use for calculating percentages in other dataframes.
# Cannot just get the total of columns in those dataframes because that will over-count anything with multiple formats.
collection_total = overview['Collections']['total']
aip_total = overview['AIPs']['total']
file_total = overview['File_IDs']['total']

# Makes the format types report (collection, AIP, and file counts and percentages). Creates dataframes for each count
# type and their percentages and combines all six dataframes into a single dataframe. Renames Collection and AIP
# columns to plural to be more accurate labels.
collection_type = df_aip.groupby('Format_Type')['Collection'].nunique()
collection_type_percent = percentage(collection_type, collection_total, "Collections Percentage")
aip_type = df_aip.groupby('Format_Type')['AIP'].nunique()
aip_type_percent = percentage(aip_type, aip_total, "AIPs Percentage")
file_type = df.groupby('Format_Type')['File_IDs'].sum()
file_type_percent = percentage(file_type, file_total, "File_IDs Percentage")
format_types = pd.concat([collection_type, collection_type_percent, aip_type, aip_type_percent, file_type, file_type_percent], axis=1)
format_types = format_types.rename({"Collection": "Collections", "AIP": "AIPs"}, axis=1)

# Makes the format standardized name report (collection, AIP, and file counts and percentages). Creates dataframes
# for each count type and their percentages and combines all six dataframes into a single dataframe.
collection_name = df_aip.groupby('Format_Standardized_Name')['Collection'].nunique()
collection_name_percent = percentage(collection_name, collection_total, "Collections Percentage")
aip_name = df_aip.groupby('Format_Standardized_Name')['AIP'].nunique()
aip_name_percent = percentage(aip_name, aip_total, "AIPs Percentage")
file_name = df.groupby('Format_Standardized_Name')['File_IDs'].sum()
file_name_percent = percentage(file_name, file_total, "File_IDs Percentage")
format_names = pd.concat([collection_name, collection_name_percent, aip_name, aip_name_percent, file_name, file_name_percent], axis=1)
format_names = format_names.rename({"Collection": "Collections", "AIP": "AIPs"}, axis=1)

# Makes a report with all standardized format names with over 500 instances, to use for risk analysis.
common_formats = format_names[format_names.File_IDs > 500]

# Makes a report with subtotals first by format type and then subdivided by group.
type_by_group = two_categories("Format_Type", "Group")

# Makes a report with subtotals first by format type and then subdivided by format standardized name.
type_by_name = two_categories("Format_Type", "Format_Standardized_Name")

# Makes a report with subtotals first by format standardized name and then by group.
name_by_group = two_categories("Format_Standardized_Name", "Group")

# Makes a report with the file identification count for every format identification (name, version, registry key).
# First adds a column to the "by format" dataframe with name|version|registry_key, which is the format identification.
# Then saves subtotals of file ids for each format identification to another dataframe.
# TODO: when I did by hand with Excel, it merged differences in capitalization while pandas keeps those separate. Ok with that or try to clean up?
df['Format Identification (Name|Version|Key)'] = df['Format_Name'] + "|" + df['Format_Version'] + "|" + df['Registry_Key']
format_id = df.groupby(df['Format Identification (Name|Version|Key)'])['File_IDs'].sum()
format_id = format_id.sort_values(ascending=False)

# Makes a report with the number of groups that have each format type.
# First gets a list of the group names for each format. Then gets the count of each of those lists. Then combine to
# one dataframe and rename the columns. Without the rename, both are 'Group' from the initial dataframe calculation.
# Had to make them separately because I couldn't figure out how to access the group list iteratively and make a new
# column from it.
groups_list = df.groupby(df['Format_Type'])['Group'].unique()
groups_count = groups_list.str.len()
groups_per_type = pd.concat([groups_count, groups_list], axis=1)
groups_per_type.columns = ['Groups', 'Group_List']
groups_per_type = groups_per_type.sort_values(by='Groups', ascending=False)

# TODO: would like to change the list to a string so it is easier to read in Excel.
# If figure this out, also add to the following two "groups per" reports.
# This was from stakeoverflow but doesn't make a change.
# groups_per_type['Group_List'].apply(', '.join)
# print(groups_per_type)

# Makes a report with the number of groups that have each format standardized name.
groups_list = df.groupby(df['Format_Standardized_Name'])['Group'].unique()
groups_count = groups_list.str.len()
groups_per_name = pd.concat([groups_count, groups_list], axis=1)
groups_per_name.columns = ['Groups', 'Group_List']
groups_per_name = groups_per_name.sort_values(by='Groups', ascending=False)

# Makes a report with the number of groups that have each format identification.
groups_list = df.groupby(df['Format Identification (Name|Version|Key)'])['Group'].unique()
groups_count = groups_list.str.len()
groups_per_id = pd.concat([groups_count, groups_list], axis=1)
groups_per_id.columns = ['Groups', 'Group_List']
groups_per_id = groups_per_id.sort_values(by='Groups', ascending=False)

# Saves each report as a spreadsheet in an Excel workbook.
# The workbook filename includes today's date, formatted YYYYMM, and is saved in the report folder.
today = datetime.datetime.now().strftime("%Y-%m")
with pd.ExcelWriter(f'ARCHive Formats Analysis_{today}.xlsx') as results:
    overview.to_excel(results, sheet_name="Group Overview")
    format_types.to_excel(results, sheet_name="Format Types")
    format_names.to_excel(results, sheet_name="Format Names")
    common_formats.to_excel(results, sheet_name="Risk Analysis")
    type_by_group.to_excel(results, sheet_name="Type by Group")
    type_by_name.to_excel(results, sheet_name="Type by Name")
    name_by_group.to_excel(results, sheet_name="Name by Group")
    format_id.to_excel(results, sheet_name="Format ID")
    groups_per_type.to_excel(results, sheet_name="Groups per Type")
    groups_per_name.to_excel(results, sheet_name="Groups per Name")
    groups_per_id.to_excel(results, sheet_name="Groups per Format ID")
