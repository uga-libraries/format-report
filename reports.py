"""EXPLANATION and prior to running instructions. Explain what the format and usage reports are."""

# Usage: python /path/reports.py ????
# TODO: before delete any previous scripts, read through one more time for ideas for future work.

# TESTING: does this get simpler if using the merged csv organized by aip-format instead of by format? Can I do any
# additional types of analysis?

import csv
import datetime
import openpyxl
import os
import pandas as pd
import sys


def archive_overview():
    """Makes a report with the TBs, AIPs, and Collections per group and total for ARCHive."""

    def size_and_aips_count():
        """Gets the size in TB and AIP count for each group from the usage report and calculates the total size and AIP
        count for all groups combined. Returns a dictionary with the group code plus total as the keys and lists with
        the group code, size, and number of AIPs as the values. """

        # Group Names maps the human-friendly version of group names from the usage report to the ARCHive group
        # code which is used in the formats report and in ARCHive metadata generally.
        group_names = {'Brown Media Archives': 'bmac', 'Digital Library of Georgia': 'dlg',
                       'DLG & Hargrett': 'dlg-hargrett', 'DLG & Map and Government Information Library': 'dlg-magil',
                       'Hargrett': 'hargrett', 'Russell': 'russell'}

        # Makes a dictionary for storing data for each group that will later be saved to the summary CSV.
        group_data = {}

        # Gets the data from the usage report.
        with open(usage_report, 'r') as usage:
            usage_read = csv.reader(usage)

            # Skips the header row.
            next(usage_read)

            # Gets data from each row. A row can have data on a group, an individual user, or be blank.
            for row in usage_read:

                # Skips empty rows. Blank rows are used for formatting the usage_report report to be easier to read.
                # Have to do this before the next step or get an IndexError when checking the group name.
                if not row:
                    continue

                # Processes data from each group. There is only one row per group in the report.
                # row[0] is group, row[1] is AIP count, and row[2] is size with the unit of measurement.
                if row[0] in group_names:

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
                        print("WARNING! Unexpected unit type:", unit)

                    # Rounds the size in TB to three decimal places so the number is easier to read.
                    size = round(size, 3)

                    # Adds the results for this group to the dictionary.
                    group_data[group_code] = ([size, aip_count])

            # Calculates the total size and total number of AIPs across all groups and adds to the dictionary.
            total_size = 0
            total_aips = 0
            for group_code in group_data:
                total_size += group_data[group_code][0]
                total_aips += group_data[group_code][1]
            group_data['total'] = [total_size, total_aips]

            # Returns the dictionary. The keys are group_code and the values are [group_code, size, aip_count].
            return group_data

    def collections_count():
        """Calculates the number of unique collections for each group using the formats report, and then calculates
        the total number of unique collections in ARCHive from the group totals. Returns a dictionary with the group
        codes as the keys and collection counts as the values."""
        # TODO: add error handling in case AIPs without collections calculated remain in the formats report?

        # Makes a dictionary for storing the collection totals.
        group_collections = {}

        # Gets the data from the formats report.
        with open(formats_by_aip_report, 'r') as formats:
            formats_read = csv.reader(formats)

            # Skips the header row.
            next(formats_read)

            # Gets the data from each row in the report.
            # row[0] is group, row[1] is collection id.
            for row in formats_read:
                group_code = row[0]
                collection_id = row[1]

                # For Russell, remove the dash from collection identifiers, since there can be two id formats
                # for the same collection, rbrl-### and rbrl###. If both variations are present, just count it once.
                if group_code == 'russell':
                    collection_id = collection_id.replace('-', '')

                # If this is the first time the group is encountered, adds it to the dictionary.
                # Otherwise, adds the collection id to the list of collections for that group if it is not there yet.
                # If it is, nothing will happen.
                if group_code not in group_collections:
                    group_collections[group_code] = [collection_id]
                else:
                    if collection_id not in group_collections[group_code]:
                        group_collections[group_code].append(collection_id)

            # Counts the number of collections in dlg that should be in dlg-hargrett (any collection starting with
            # "guan_"), which is caused by an error in ARCHive data. Although the collection has a primary group of
            # hargrett-dlg, the AIP has a primary group of dlg so it is incorrectly counted as dlg. Used to correct the
            # counts in the next step.
            wrong_group_count = 0
            for collection in group_collections['dlg']:
                if collection.startswith('guan_'):
                    wrong_group_count += 1

            # Calculates the final count of unique collections per group by getting the length of each collection list
            # and then making adjustments for collections that are in dlg instead of dlg-hargrett.
            for group_code in group_collections:
                group_collections[group_code] = len(group_collections[group_code])
            group_collections['dlg-hargrett'] += wrong_group_count
            group_collections['dlg'] -= wrong_group_count

            # Calculates the total number of collections across all groups and adds to the dictionary.
            total_collections = 0
            for group_code in group_collections:
                total_collections += group_collections[group_code]
            group_collections['total'] = total_collections

            # Returns the dictionary. Keys are group codes and values are collection counts.
            return group_collections

    # Gets the size (TB) and number of AIPs per group from the usage report.
    # group_information = size_and_aips_count()

    # Gets the number of collections per group from the formats by AIP report.
    # Only counts collections with AIPs, which may result in a difference between this count and ARCHive's count.
    collections_by_group = df_aip.groupby('Group')['Collection'].nunique()

    # Calculates the number of collections starting 'guan_'. Those should be dlg-hargrett but are dlg.
    # Updates the values in the dataframe to correct for the error.
    # TODO: this isn't working right
    dlg = df_aip[df_aip.Group.eq('dlg')]
    print(dlg.Collection.str.count("guan_")).sum()

    # Gets the number of files per group from the other formats report.
    # These numbers are inflated by files with more than one format.
    files_by_group = df.groupby('Group')['File_Count'].sum()

    # Adds the collection counts to the lists in the group_information dictionary for each group.
    # If the group does not have a collection count, supplies a value of zero.
    # for group in group_information:
    #     try:
    #         group_information[group].append(collections_by_group[group])
    #     except KeyError:
    #         group_information[group].append(0)

    # # Adds the file counts to the lists in the group_information dictionary for each group.
    # # index = type
    # # row has the count, name, and data type.
    # for index, row in files_by_group.iteritems():
    #     group_information[index].append(row)
    #
    # # Adds zero for file count if no value there.
    # # TODO might be a way to do this with data frames.
    # for value in group_information.values():
    #     if len(value) == 3:
    #         value.append(0)

    # # Gets total for file count of all groups.
    # # TODO might be a way to do this with data frames. Should be total = df_aip['MyColumn'].sum()
    # total_files = 0
    # for key in group_information:
    #     if not key == 'total':
    #         total_files += group_information[key][3]
    # group_information['total'][3] = total_files
    #
    # # Return the information
    # return group_information


# Makes the report folder (script argument) the current directory. Displays an error message and quits the script if
# the argument is missing or not a valid directory.
try:
    report_folder = sys.argv[1]
    os.chdir(report_folder)
except (IndexError, FileNotFoundError):
    print("The report folder path was either not given or is not a valid directory. Please try the script again.")
    print("Script usage_report: python /path/csv_merge.py /path/reports [/path/standardize_formats.csv]")
    exit()

# Gets paths for the data files used in this script, which should be in the report folder.
# If any are not found, prints an error and quits the script.
formats_by_aip_report = False
formats_report = False
usage_report = False

for file in os.listdir('.'):
    # This CSV has one line per AIP and unique format. AIPs have multiple rows. Allows aggregating collection and AIP
    # format inforamtion without unpacking lists of ids.
    if file.startswith('archive_formats_by_aip') and file.endswith('.csv'):
        formats_by_aip_report = file
    # This CSV has one line per unique format. Allows aggregating file count information.
    elif file.startswith('archive_formats_') and file.endswith('.csv'):
        formats_report = file
    # This CSV has user and group ingest information.
    elif file.startswith('usage_report_') and file.endswith('.csv'):
        usage_report = file

if not formats_by_aip_report:
    print("Could not find archive formats_by_aip_report csv in the report folder.")
    if not usage_report:
        print("Could not find usage_report report csv in the report folder.")
    exit()

# Increases the size of csv fields to handle long aip lists.
# Gets the maximum size that doesn't give an overflow error.
while True:
    try:
        csv.field_size_limit(sys.maxsize)
        break
    except OverflowError:
        sys.maxsize = int(sys.maxsize / 10)

# Makes dataframes from both format reports.
df = pd.read_csv(formats_report)
df_aip = pd.read_csv(formats_by_aip_report)

# TODO: this replaces dash in all collection ids. Probably ok (not creating duplicates) but more than want to do.
# Updates collection ids to remove dash, since rbrl-### and rbrl### should be treated as one collection. This
# filters for russell collections: df_aip.loc[df_aip['Group'] == 'russell']['Collection'], but gives error if put it on
# left of = and if put on right for df_aip['Collection'] all other collection ids become NaN. russell_collections =
# russell_collections.str.replace('-', '')
df_aip['Collection'] = df_aip['Collection'].str.replace('-', '')

# Makes a spreadsheet to save results to.
# TODO: Making a tab, adding a header, and saving all the results of calling a function is repeating. Own function?
# TODO: can I sort? Bold the first row? Add a chart? What else can I do besides save to a tab?
wb = openpyxl.Workbook()

# # Makes the ARCHive overview report (TBS, AIPs, and Collections by group) and saves to the report spreadsheet.
# # Renames the sheet made when starting a workbook to ARCHive Overview.
# ws1 = wb.active
# ws1.title = "ARCHive Overview"
#
# # Adds a header row to the sheet.
# ws1.append(['Group', 'Size (TBs)', 'AIPs', 'Collections', 'Files (inflated)'])
#
# # Gets the data and adds every entry in the dictionary as its own row in the spreadsheet.
overview = archive_overview()
# for key, value in overview.items():
#     value.insert(0, key)
#     ws1.append(value)


# Makes the format types report and saves to the spreadsheet.
# Count of unique collections, unique AIPs, and (some inflation) files for each format type.

# Creates the subtotals by format type using dataframes and combines them into a single dataframe.
collection_type = df_aip.groupby('Format_Type')['Collection'].nunique()
aip_type = df_aip.groupby('Format_Type')['AIP'].nunique()
file_type = df.groupby('Format_Type')['File_Count'].sum()
type_frames = [collection_type, aip_type, file_type]
types_combined = pd.concat(type_frames, axis=1)

# TODO: add percentages?
# Adds the column totals to the format type dataframes.
types_combined.loc['total'] = [collection_type.sum(), aip_type.sum(), file_type.sum()]

# Converts the format standardized name dataframe to a list of lists, one list per row.
# reset_index() includes the index value (the type) and values.tolist() adds the counts.
# TODO: save directly to Excel from dataframe? See reports_pandas.py
type_rows = types_combined.reset_index().values.tolist()

# Adds the format type data to a tab in the results spreadsheet, with a header row.
ws2 = wb.create_sheet(title="type_counts")
ws2.append(['Format Type', 'Collection Count', 'AIP Count', 'File Count'])
for type_row in type_rows:
    ws2.append(type_row)


# Makes the format standardized name report and saves to the spreadsheet.
# Count of unique collections, unique AIPs, and (some inflation) files for each format standardized name.

# Creates the subtotals by format standardized name using dataframes and combines them into a single dataframe.
collection_name = df_aip.groupby('Format_Standardized_Name')['Collection'].nunique()
aip_name = df_aip.groupby('Format_Standardized_Name')['AIP'].nunique()
file_name = df.groupby('Format_Standardized_Name')['File_Count'].sum()
name_frames = [collection_name, aip_name, file_name]
names_combined = pd.concat(name_frames, axis=1)

# TODO: add percentages?
# Adds the column totals to the format standardized name dataframe.
names_combined.loc['total'] = [collection_name.sum(), aip_name.sum(), file_name.sum()]

# Converts the format standardized name dataframe to a list of lists, one list per row.
# reset_index() includes the index value (the type) and values.tolist() adds the counts.
name_rows = names_combined.reset_index().values.tolist()

# Adds the format standardized name data to a tab in the results spreadsheet, with a header row.
ws3 = wb.create_sheet(title="name_counts")
ws3.append(['Format Standardized Name', 'Collection Count', 'AIP Count', 'File Count'])
for name_row in name_rows:
    ws3.append(name_row)


# Gets the current date, formatted YYYYMM, to use in naming the merged file.
today = datetime.datetime.now().strftime("%Y-%m")

# Can save after each tab if want. Do not save, change the tab, and re-save or it will overwrite.
wb.save(f"ARCHive Format Report_{today}.xlsx")

# # TODO: Reports I was making with pandas that are not included here
# # Are these helpful or would we just go back to the main spreadsheet?
# # Format type then by group
# # Format type then by name
# # Format name then by group
#
# # TODO: ideas for future development
# # A tab with the most common formats, however that is defined.
# # A way to compare one spreadsheet to another to show change since the last report.
# # Adding in size, if Shawn can update the format report.
# # Calculate the number of individual formats in a name or type grouping?
# # Calculate the average amount of format variety in a collection or AIP?
