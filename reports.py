"""EXPLANATION and prior to running instructions. Explain what the format and usage reports are."""

# Usage: python /path/reports.py ????
# TODO: before delete any previous scripts, read through one more time for ideas for future work.
# TODO: consider making a by-AIP CSV as merge. Would eliminate huge cells so might make easier to aggregate.

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
                    # TODO: rework so the group code doesn't need to be in both places. It isn't hard to use get keys.
                    # group_code is repeated in the value list to make it easy to include the group in the output.
                    group_data[group_code] = ([group_code, size, aip_count])

            # Calculates the total size and total number of AIPs across all groups and adds to the dictionary.
            total_size = 0
            total_aips = 0
            for group_code in group_data:
                total_size += group_data[group_code][1]
                total_aips += group_data[group_code][2]
            group_data['total'] = ['total', total_size, total_aips]

            # Returns the dictionary. The keys are group_code and the values are [group_code, size, aip_count].
            return group_data

    def collections_count():
        """Calculates the number of unique collections for each group using the formats report, and then calculates
        the total number of unique collections in ARCHive from the group totals. Returns a dictionary with the group
        codes as the keys and collection counts as the values.

        NOTE: if there are any AIPs where the collection was not calculated, each one of those AIPs will count as a
        separate collection, inflating the numbers. However, these errors generally will have been addressed prior to
        running this script. """
        # TODO: add error handling in case AIPs without collections calculated remain in the formats report?

        # Makes a dictionary for storing the collection totals.
        group_collections = {}

        # Gets the data from the formats report.
        with open(formats_report, 'r') as formats:
            formats_read = csv.reader(formats)

            # Skips the header row.
            next(formats_read)

            # Gets the data from each row in the report, which has information about a single format for that group.
            # A collection will only be in a single row once, but may be in multiple rows.
            # row[0] is group, row[11] is collection ids (a comma separated string).
            for row in formats_read:
                group_code = row[0]
                collection_list = row[11].split(', ')

                # For Russell, remove the dash from collection identifiers, since there can be two id formats_report
                # for the same collection, rbrl-### and rbrl###. If both variations are present, just count it once.
                if group_code == 'russell':
                    collection_list = [collection.replace('-', '') for collection in collection_list]
                    # Transforms the list to a set to remove duplicates and back to a list since that is the type the
                    # script expects. May have introduced duplicates by normalizing the collection id formatting.
                    collection_list = list(set(collection_list))

                # If this is the first time the group is encountered, adds it to the dictionary.
                # Otherwise, adds new collections to the list of collections for that group already in the dictionary.
                if group_code not in group_collections:
                    group_collections[group_code] = collection_list
                else:
                    # Combines the list of collections already in the dictionary with the list of collections from this
                    # row. Transforms the combined list to a set to remove duplicates and then back to a list since that
                    # is the type the script expects.
                    combined_collections = group_collections[group_code] + collection_list
                    group_collections[group_code] = list(set(combined_collections))

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
    group_information = size_and_aips_count()

    # Gets the number of collections per group from the formats report.
    # Only counts collections with AIPs, which may result in a difference between this count and ARCHive's count.
    collections_by_group = collections_count()

    # Adds the collection counts to the lists in the group_information dictionary for each group.
    # If the group does not have a collection count, supplies a value of zero.
    for group in group_information:
        try:
            group_information[group].append(collections_by_group[group])
        except KeyError:
            group_information[group].append(0)

    # Return the information
    return group_information


def collection_subtotals():
    """Returns a dictionaries with counts of unique collections by format type and normalized format name."""
    type_count = {}
    name_count = {}

    # Gets the data from the formats report.
    with open(formats_report, 'r') as formats:
        formats_read = csv.reader(formats)

        # Skips the header row.
        next(formats_read)

        # Gets the data from each row in the report, which has information about a single format for that group.
        # row[0] is group.
        # row[4] is format type.
        # row[11] is collection ids (a comma separated string).
        for row in formats_read:

            # Format the collections as a list.
            collection_list = row[11].split(', ')

            # For Russell, remove the dash from collection identifiers, since there can be two id formats for the same
            # collection, rbrl-### and rbrl###. If both variations are present, just want to count it once.
            if row[0] == 'russell':
                collection_list = [collection.replace('-', '') for collection in collection_list]

            # Adds each collection to a dictionary. Key is format type and value is a list of collection ids.
            for collection in collection_list:
                try:
                    type_count[row[4]].append(collection)
                except KeyError:
                    type_count[row[4]] = [collection]

            # Adds each collection to a dictionary. Key is standardized format name and value is a list of collection ids.
            for collection in collection_list:
                try:
                    name_count[row[5]].append(collection)
                except KeyError:
                    name_count[row[5]] = [collection]

        # Convert the list of collections in each dictionary to the count of unique collections.
        # Makes a set to remove duplicates before converting to a count with len().
        for key, value in type_count.items():
            type_count[key] = len(set(value))

        for key, value in name_count.items():
            name_count[key] = len(set(value))

        # Returns both dictionaries
        return type_count, name_count


def aip_subtotals():
    """Returns a dictionaries with counts of unique AIPs by format type and normalized format name."""

    # Starts dictionaries for storing the results.
    type_count = {}
    name_count = {}

    # Gets the data from the formats report.
    with open(formats_report, 'r') as formats:
        formats_read = csv.reader(formats)

        # Skips the header row.
        next(formats_read)

        # Gets the data from each row in the report, which has information about a single format for that group.
        # row[4] is format type.
        # row[5] is format standardized name.
        # row[12] is AIP ids (a pipe separated string).
        for row in formats_read:

            # Format the aips as a list.
            aip_list = row[12].split('|')

            # Adds each aip to a dictionary with format type as the key and a list of aip ids as the value.
            for aip in aip_list:
                try:
                    type_count[row[4]].append(aip)
                except KeyError:
                    type_count[row[4]] = [aip]

            # Adds each aip to a dictionary with format name as the key and a list of aip ids as the value.
            for aip in aip_list:
                try:
                    name_count[row[5]].append(aip)
                except KeyError:
                    name_count[row[5]] = [aip]

    # Convert the list of collections in each dictionary to the count of unique collections.
    # Making a set removes duplicates.
    for key, value in type_count.items():
        type_count[key] = len(set(value))

    for key, value in name_count.items():
        name_count[key] = len(set(value))

    # Returns both dictionaries
    return type_count, name_count


def file_subtotals():
    """File subtotals are inflated by formats with multiple possible identifications.
    Just does type right now. Not sure if I can get this merged into the dictionary correctly"""
    df = pd.read_csv(formats_report)
    format_type = df.groupby('Format_Type').sum()
    return format_type[['File_Count']]


# START OF SCRIPT BODY

# Makes the report folder (script argument) the current directory. Displays an error message and quits the script if
# the argument is missing or not a valid directory.
try:
    report_folder = sys.argv[1]
    os.chdir(report_folder)
except (IndexError, FileNotFoundError):
    print("The report folder path was either not given or is not a valid directory. Please try the script again.")
    print("Script usage_report: python /path/csv_merge.py /path/reports [/path/standardize_formats.csv]")
    exit()

# Gets paths for the archive formats_report csv (combines all the group format information) and usage_report report.
# Both should be in the report folder. If either is not found, prints an error and quits the script.
formats_report = False
usage_report = False

for file in os.listdir('.'):
    if file.startswith('archive_formats_') and file.endswith('.csv'):
        formats_report = file
    elif file.startswith('usage_report_') and file.endswith('.csv'):
        usage_report = file

if not formats_report:
    print("Could not find archive formats_report csv in the report folder.")
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

# Makes a spreadsheet to save results to.
# TODO: Making a tab, adding a header, and saving all the results of calling a function is repeating. Own function?
# TODO: can I sort? Bold the first row? Add a chart? What else can I do besides save to a tab?
wb = openpyxl.Workbook()

# Makes the ARCHive overview report (TBS, AIPs, and Collections by group) and saves to the report spreadsheet.
# TODO Add estimated file count from format report.
# Renames the sheet made when starting a workbook to ARCHive Overview.
ws1 = wb.active
ws1.title = "ARCHive Overview"

# Adds a header row to the sheet.
ws1.append(['Group', 'Size (TBs)', 'AIPs', 'Collections'])

# Gets the data and adds every entry in the dictionary as its own row in the spreadsheet.
overview = archive_overview()
for key in overview:
    ws1.append(overview[key])

"""Creates two dictionaries, one for format type and one for format standardized name.
Key is the type or name, value is a list with the collection, aip, and file counts.
Collection and AIP counts are generated by this script and remove duplicates.
File count comes from the format report and includes duplicates for formats with multiple possible identifications."""
# TODO: add percentages? If know total at this point, could add to the list in the dictionaries.

# Starts with the collection counts.
type_counts, name_counts = collection_subtotals()

# Gets the AIP counts.
aip_type, aip_name = aip_subtotals()

# Adds the AIP type counts to the type_counts dictionary.
# Changes the value from a single integer to a list of integers.
for key, value in type_counts.items():
    type_counts[key] = [value, aip_type[key]]

# Adds the AIP format standardized name counts to the name_counts dictionary.
# Changes the value from a single integer to a list of integers.
for key, value in name_counts.items():
    name_counts[key] = [value, aip_name[key]]

# Gets the file counts.
file_type = file_subtotals()

# Adds the file type counts to the type_counts dictionary.
# index = type
# row has the count, name, and data type.
for index, row in file_type.iterrows():
    type_counts[index].append(row['File_Count'])

# # Saves the data from each dictionary to its own sheet in the report.
# # Adds the key to the first position in the list with the counts first.
# ws2 = wb.create_sheet(title="type_counts")
# ws2.append(['Format Type', 'Collection Count', 'AIP Count', 'File Count'])
# for key, value in type_counts.items():
#     value.insert(0, key)
#     ws2.append(value)
#
# ws3 = wb.create_sheet(title="name_counts")
# ws3.append(['Format Standardized Name', 'Collection Count', 'AIP Count', 'File Count'])
# for key, value in name_counts.items():
#     value.insert(0, key)
#     ws3.append(value)
#
#
# # Can save after each tab if want. Do not save, change the tab, and re-save or it will overwrite.
# wb.save("ARCHive Format Report.xlsx")

# TODO: Reports I was making with pandas. Has collection aip, and file count (not deduplicated)
# Are these helpful or would we just go back to the main spreadsheet?
# Format type then by group
# Format type then by name
# Format name then by group

# TODO: ideas for future development
# A tab with the most common formats, however that is defined.
# A way to compare one spreadsheet to another to show change since the last report.
# Adding in size, if Shawn can update the format report.
# Calculate the number of individual formats in a name or type grouping?
