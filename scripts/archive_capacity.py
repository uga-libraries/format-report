"""Makes a summary of the current holdings of ARCHive (number of collections, AIPs, and TB), overall and by group,
using information from the ARCHive format reports and the usage report. """
# TODO: use the AIP count from the usage report and the collection list from the merged report instead.

import csv
import os
import re
import sys


def read_usage():
    # Gets the AIP count and size in TB from the usage report.
    with open(usage_report, 'r') as usage:
        usage_read = csv.reader(usage, delimiter="\t")

        # Skip header
        next(usage_read)

        # A row can have the group data, a staff person's data, or be blank.
        # For group rows, row[0] is the group, row[1] is the AIP count, and row[2] is the size.
        # Groups are written out rather than the code, e.g. Brown Media Archives instead of bmac.
        # AIP count is a string.
        # Size is # unit and the unit can can be MB, GB, TB, or 0 Bytes if none.

        # Group Names (used to find the rows to use in the report and convert to group codes used by format report)
        group_names = {'Brown Media Archives': 'bmac', 'Digital Library of Georgia': 'dlg',
                       'DLG & Hargrett': 'dlg-hargrett', 'DLG & Map and Government Information Library': 'dlg-magil',
                       'Hargrett': 'hargrett', 'Russell': 'russell'}

        # Makes a dictionary for storing data for each group, one list per group, that will be saved to the csv.
        group_data = {}

        # Get and transform data from each group row.
        for row in usage_read:

            # Skip empty rows. Have to do this before test for row[0] or get an IndexError.
            if not row:
                continue

            # Only want data from group rows, not individual staff rows.
            # There is only one row per group in the report.
            if row[0] in group_names:
                group_code = group_names[row[0]]
                aip_count = int(row[1])

                # Separates the size from the unit and converts the size to TB, e.g. 100 GB becomes 0.1.
                # If it encounters a unit of measurement that wasn't anticipated, prints a warning message.
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

                # Rounds the size in TB to three decimal places.
                size = round(size, 3)

                # Adds the results for this group to the dictionary.
                group_data[group_code] = ([group_code, size, aip_count])

        # Calculate the total size and total number of AIPs across all groups and add to the dictionary.
        total_size = 0
        total_aips = 0
        for group in group_data:
            total_size += group_data[group][1]
            total_aips += group_data[group][2]
        group_data['total'] = ['total', total_size, total_aips]

        # Returns the dictionary with key of group and value of [size, aip_count]
        return group_data


def collections_count():
    group_collections = {}

    with open(formats_report, 'r') as formats:
        formats_read = csv.reader(formats)

        # Skip header
        next(formats_read)

        # Each row is a single format for that group. Each collection may show up in multiple rows.
        # row[0] is the group, row[11] is the collections, which is a comma separated string.
        for row in formats_read:
            group = row[0]
            collection_list = row[11].split(', ')

            # If this is the first time the group is encountered, add it to the dictionary.
            # Otherwise, add new collections to the list of collections for that group already in the dictionary.
            if group not in group_collections:
                group_collections[group] = collection_list
            else:
                # TODO: could wait to do set() until have the final dictionary and are about to count.
                # Combines the list of collections in the dictionary with the list of collections from this row.
                combined_collections = group_collections[group] + collection_list
                # Changing the list to a set automatically removes duplicates.
                collections_without_duplicates = set(combined_collections)
                # Changes the set back to a list and updates the dictionary with that list.
                group_collections[group] = list(collections_without_duplicates)

        # Gets the final count of unique collections per group
        for group in group_collections:
            group_collections[group] = len(group_collections[group])

        # Calculates the total number of collections across all groups and adds to the dictionary.
        total_collections = 0
        for group in group_collections:
            total_collections += group_collections[group]
        group_collections['total'] = total_collections

        return group_collections


# TODO: argument error handling; maybe give option of formats and usage report using relative path from report folder?
# Makes variables for the input of the script.
formats_report = sys.argv[1]
usage_report = sys.argv[2]

# Makes the report folder the current directory.
report_folder = sys.argv[3]
os.chdir(report_folder)

# TODO: this may not be necessary since switched to reading collection list.
# Increases the size of csv fields to handle long AIP lists.
# Gets the maximum size that doesn't give an overflow error.
while True:
    try:
        csv.field_size_limit(sys.maxsize)
        break
    except OverflowError:
        sys.maxsize = int(sys.maxsize / 10)

# Gets the size (TB) and number of AIPs per group.
group_usage = read_usage()

# Gets collection count for each group from the archive formats CSV and adds to group_usage.
collections_by_group = collections_count()
for group, count in collections_by_group.items():
    group_usage[group].append(count)

# Makes a CSV for the summary named archive_summary.csv.
# TODO: reconsider having the date in the report. Means have to run soon after download to be accurate, but if want to
#  save these for a record over time need to know when they are from.
with open(f'archive_summary.csv', 'w', newline='') as summary:
    summary_csv = csv.writer(summary)

    # Adds a header to the summary report.
    summary_csv.writerow(['Group', 'Size (TBs)', 'AIPs', 'Collections'])

    for group in group_usage:
        summary_csv.writerow(group_usage[group])







