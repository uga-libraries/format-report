"""Makes a summary of the current holdings of ARCHive, the UGA Libraries digital preservation system. The summary is
a csv with the number of terabytes, AIPs, and collections, by group and the overall total. It is created using
information from the merged ARCHive format report and the ARCHive usage report.

To make the merged format report, download each group's format report from ARCHive and run the csv_merge.py script.
To make the usage report, generate and download the usage report in ARCHive from ARCHive start date to the date the
format reports were downloaded.

Usage: python /path/archive_capacity.py /path/merged_format_report /path/usage_report /path/output_folder"""

import csv
import datetime
import os
import sys


def read_usage():
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
        usage_read = csv.reader(usage, delimiter="\t")

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
        for group in group_data:
            total_size += group_data[group][1]
            total_aips += group_data[group][2]
        group_data['total'] = ['total', total_size, total_aips]

        # Returns the dictionary. The keys are group_code and the values are [group_code, size, aip_count].
        return group_data


def collections_count():
    """Calculates the number of unique collections for each group using the merged ARCHive summary report and the
    total number of collections in ARCHive using the group totals. Returns a dictionary with the group codes as the
    keys and collection counts as the values. """

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
            group = row[0]
            collection_list = row[11].split(', ')

            # For Russell, remove the dash from collection identifiers, since there can be two id formats for the same
            # collection, rbrl-### and rbrl###. If both variations are present, just want to count it once.
            if group == 'russell':
                collection_list = [collection.replace('-', '') for collection in collection_list]

            # If this is the first time the group is encountered, adds it to the dictionary.
            # Otherwise, adds any new collections to the list of collections for that group already in the dictionary.
            # TODO: remove dups in case the russell cleanup introduced one.
            if group not in group_collections:
                group_collections[group] = collection_list
            else:
                # Combines the list of collections already in the dictionary with the list of collections from this
                # row. Transforms the combined list to a set to remove duplicates and then back to a list since that
                # is the type the script expects.
                combined_collections = group_collections[group] + collection_list
                collections_without_duplicates = set(combined_collections)
                group_collections[group] = list(collections_without_duplicates)

        # Counts the number of collections in dlg that should be in dlg-hargrett (any collection starting with
        # "guan_", which is caused by an error in ARCHive data. Used to correct the counts in the next step.
        wrong_group_count = 0
        for collection in group_collections['dlg']:
            if collection.startswith('guan_'):
                wrong_group_count += 1

        # Calculates the final count of unique collections per group by getting the length of each collection list
        # and then making adjustments for collections that are in dlg instead of dlg-hargrett.
        for group in group_collections:
            group_collections[group] = len(group_collections[group])
        group_collections['dlg-hargrett'] += wrong_group_count
        group_collections['dlg'] -= wrong_group_count

        # Calculates the total number of collections across all groups and adds to the dictionary.
        total_collections = 0
        for group in group_collections:
            total_collections += group_collections[group]
        group_collections['total'] = total_collections

        # Returns the dictionary. Keys are group codes and values are collection counts.
        return group_collections


# Makes variables for the input of the script.
formats_report = sys.argv[1]
usage_report = sys.argv[2]
report_folder = sys.argv[3]

# Makes the report folder the current directory.
os.chdir(report_folder)

# Gets the size (TB) and number of AIPs per group from the usage report.
group_usage = read_usage()

# Gets the number of collections per group from the merged ARCHive formats CSV and adds to the group_usage dictionary.
collections_by_group = collections_count()
for group, count in collections_by_group.items():
    group_usage[group].append(count)

# Makes a CSV in the output folder for the summary data named archive_summary_date.csv.
# Gets the current date, formatted YYYY-MM, to use in naming the summary file.
today = datetime.datetime.now().strftime("%Y-%m")
with open(f'archive_summary_{today}.csv', 'w', newline='') as summary:
    summary_csv = csv.writer(summary)

    # Adds a header to the summary report.
    summary_csv.writerow(['Group', 'Size (TBs)', 'AIPs', 'Collections'])

    # Saves the information for each group, and the ARCHive total, to the summary report.
    # The information for each group is saved as a list in the group_usage dictionary with the group code as the key.
    for group in group_usage:
        summary_csv.writerow(group_usage[group])







