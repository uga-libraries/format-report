"""Makes a summary of the current holdings of ARCHive (number of collections, AIPs, and TB), overall and by group,
using information from the ARCHive format reports and the usage report. """
# TODO: use the AIP count from the usage report and the collection list from the merged report instead.

import csv
import os
import re
import sys

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

# Makes a CSV for the summary named archive_summary.csv.
# TODO: reconsider having the date in the report. Means have to run soon after download to be accurate, but if want to
#  save these for a record over time need to know when they are from.
with open(f'archive_summary.csv', 'w', newline='') as summary:
    summary_csv = csv.writer(summary)

    # Adds a header to the summary report.
    summary_csv.writerow(['Group', 'Collections', 'AIPs', 'Size (TBs)'])

    # Gets a collection count for each group from the archive formats CSV. First stores a unique list of collections
    # by group in a dictionary and then counts the results.
    # TODO: this is probably long enough to be better as a function.
    collections_by_group = {}
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
            if group not in collections_by_group:
                collections_by_group[group] = collection_list
            else:
                # TODO: could wait to do set() until have the final dictionary and are about to count.
                # Combines the list of collections in the dictionary with the list of collections from this row.
                combined_collections = collections_by_group[group] + collection_list
                # Changing the list to a set automatically removes duplicates.
                collections_without_duplicates = set(combined_collections)
                # Changes the set back to a list and updates the dictionary with that list.
                collections_by_group[group] = list(collections_without_duplicates)

        # Gets the final count of unique collections per group and saves to the summary report.
        for group in collections_by_group:
            summary_csv.writerow([group, len(collections_by_group[group])])




    # # Gets each format report.
    # for report in os.listdir(report_folder):
    #     if report.startswith('file_formats'):
    #
    #         # Gets the ARCHive group from the filename.
    #         regex = re.match('file_formats_\d{8}_(.*).txt', report)
    #         archive_group = regex.group(1)
    #
    #         # Gets the data from the report, which is a tab-delimited text file.
    #         report_open = open(report, 'r')
    #         report_info = csv.reader(report_open, delimiter='\t')
    #
    #         # Gets a list of unique AIP IDs.
    #         aips = aip_list(report_info)
    #
    #         # Calculates the collection number for each AIP ID and saves the group, collection id, and AIP id to the
    #         # teporary file.
    #         for aip in aips:
    #             collection = collection_from_aip(aip, archive_group)
    #             aiplistcsv.writerow([archive_group, collection, aip])
    #
    #         report_open.close()
    #
    #     # Ignore anything else in this folder.
    #     # TODO: I don't think this is necessary.
    #     else:
    #         continue
