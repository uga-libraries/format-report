"""Makes a summary of the current holdings of ARCHive, the UGA Libraries digital preservation system. The summary is
a csv with the number of terabytes, AIPs, and collections, by group and the overall total. It is created using
information from the merged ARCHive format report and the ARCHive usage report.

To make the merged format report, download each group's format report from ARCHive and run the csv_merge.py script.
To make the usage report, generate and download the usage report in ARCHive from ARCHive start date to the date the
format reports were downloaded."""

# Usage: python /path/archive_capacity.py /path/merged_format_report /path/usage_report /path/output_folder

import csv
import datetime
import os
import sys


def size_and_aips_count():
    """Gets the size in TB and AIP count for each group from the usage report and calculates the total size and AIP
    count for all groups combined. Returns a dictionary with the group code as the keys and lists with the group
    code, size, and number of AIPs as the values. """

    # Group Names is used to map the human-friendly version of group names from the usage report to the ARCHive group
    # code which is used in the format report and in ARCHive metadata generally.
    group_names = {'Brown Media Archives': 'bmac', 'Digital Library of Georgia': 'dlg',
                   'DLG & Hargrett': 'dlg-hargrett', 'DLG & Map and Government Information Library': 'dlg-magil',
                   'Hargrett': 'hargrett', 'Russell': 'russell'}

    # Makes a dictionary for storing data for each group that will later be saved to the summary CSV.
    group_data = {}

    # Gets the data from the usage report. It is a tab-delimited text file that has rows with the group information,
    # individual user information, and blank rows used for formatting.
    with open(usage_report, 'r') as usage:
        usage_read = csv.reader(usage)

        # Skips the header row.
        next(usage_read)

        # Gets data from each row. A row can have data on a group, an individual user, or be blank.
        for row in usage_read:

            # Skips empty rows. Blank rows are used for formatting the usage report to be easier to read.
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
                # group_code is the key and in the value list to make it easy to include the group in the summary CSV.
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
    """Calculates the number of unique collections for each group using the merged ARCHive summary report and the
    total number of collections in ARCHive using the group totals. Returns a dictionary with the group codes as the
    keys and collection counts as the values.

    NOTE: if there are any AIPs where the collection was not calculated, each one of those AIPs will count as a
    separate collection, inflating the numbers. However, these errors generally will have been addressed prior to
    running this script. """

    # Makes a dictionary for storing the collection totals.
    group_collections = {}

    # Gets the data from the merged ARCHive formats report.
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

            # For Russell, remove the dash from collection identifiers, since there can be two id formats for the same
            # collection, rbrl-### and rbrl###. If both variations are present, just want to count it once.
            if group_code == 'russell':
                collection_list = [collection.replace('-', '') for collection in collection_list]
                # Transforms the list to a set to remove duplicates and back to a list since that is the type the
                # script expects. May have introduced duplicates by normalizing the collection id formatting.
                unique_collections = set(collection_list)
                collection_list = list(unique_collections)

            # If this is the first time the group is encountered, adds it to the dictionary.
            # Otherwise, adds any new collections to the list of collections for that group already in the dictionary.
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


# Makes variables for the input of the script. If any are missing, prints an error and quits the script.
# TODO: Add error handling for if report paths exist or generate the paths with the script - are in the output folder.
try:
    formats_report = sys.argv[1]
    usage_report = sys.argv[2]
    output_folder = sys.argv[3]
except IndexError:
    print("At least one of the required script arguments is missing.")
    print("Usage: python /path/archive_capacity.py /path/merged_format_report /path/usage_report /path/output_folder")
    exit()

# Makes the report folder the current directory.
# If it is not a valid directlyr, prints and error and quits the script.
try:
    os.chdir(output_folder)
except FileNotFoundError:
    print("The output folder is not a valid directory.")
    print("Usage: python /path/archive_capacity.py /path/merged_format_report /path/usage_report /path/output_folder")
    exit()

# Gets the size (TB) and number of AIPs per group from the usage report.
group_information = size_and_aips_count()

# Gets the number of collections per group from the merged ARCHive formats CSV.
# Only counts collections with AIPs, which may result in a difference between this count and ARCHive's count.
collections_by_group = collections_count()

# Adds the collection counts to the lists in the group_information dictionary for each group.
# If the group does not have a collection count, supplies a value of zero.
for group in group_information:
    try:
        group_information[group].append(collections_by_group[group])
    except KeyError:
        group_information[group].append(0)

# Makes a CSV in the output folder for the summary data named archive_summary_date.csv.
# Gets the current date, formatted YYYY-MM, to use in naming the summary file.
today = datetime.datetime.now().strftime("%Y-%m")
with open(f'archive_summary_{today}.csv', 'w', newline='') as summary:
    summary_csv = csv.writer(summary)

    # Adds a header to the summary report.
    summary_csv.writerow(['Group', 'Size (TBs)', 'AIPs', 'Collections'])

    # Saves the information for each group, and the ARCHive total, to the summary report.
    # The information for each group is saved as a list in the group_usage dictionary with the group code as the key.
    for group in group_information:
        summary_csv.writerow(group_information[group])
