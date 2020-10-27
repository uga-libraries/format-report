"""EXPLANATION and prior to running instructions. Explain what the format and usage reports are."""

# Usage: python /path/reports.py ????

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
wb = openpyxl.Workbook()

# Makes the ARCHive overview report (TBS, AIPs, and Collections by group) and saves to the report spreadsheet.
overview = archive_overview()

ws1 = wb.active
ws1.title = "ARCHive Overview"
ws1.append(['Group', 'Size (TBs)', 'AIPs', 'Collections'])

for key in overview:
    ws1.append(overview[key])

# Saves the report spreadsheet. It overwrites existing tabs. Does it overwrite the full file?
wb.save("ARCHive Format Report.xlsx")
