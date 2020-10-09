"""Makes a summary of the current holdings of ARCHive (number of collections, AIPs, and TB), overall and by group,
using information from the ARCHive format reports and the usage report. """
# TODO: use the AIP count from the usage report and the collection list from the merged report instead.

import csv
import os
import re
import sys

# TODO: argument error handling
# Makes variables for the input of the script.
formats_report = sys.argv[1]
usage_report = sys.argv[2]

# Makes the report folder the current directory.
report_folder = sys.argv[3]
os.chdir(report_folder)


# Increases the size of csv fields to handle long AIP lists.
# Gets the maximum size that doesn't give an overflow error.
while True:
    try:
        csv.field_size_limit(sys.maxsize)
        break
    except OverflowError:
        sys.maxsize = int(sys.maxsize / 10)

# Makes a temporary file for the aggregated information named archive_aiplist_date.csv.
with open(f'archive_aiplist_{today}.csv', 'w', newline='') as aiplist:
    aiplistcsv = csv.writer(aiplist)

    # Adds a header to the temporary file.
    aiplistcsv.writerow(['Group', 'Collection', 'AIP'])

    # Gets each format report.
    for report in os.listdir(report_folder):
        if report.startswith('file_formats'):

            # Gets the ARCHive group from the filename.
            regex = re.match('file_formats_\d{8}_(.*).txt', report)
            archive_group = regex.group(1)

            # Gets the data from the report, which is a tab-delimited text file.
            report_open = open(report, 'r')
            report_info = csv.reader(report_open, delimiter='\t')

            # Gets a list of unique AIP IDs.
            aips = aip_list(report_info)

            # Calculates the collection number for each AIP ID and saves the group, collection id, and AIP id to the
            # temporary file.
            for aip in aips:
                collection = collection_from_aip(aip, archive_group)
                aiplistcsv.writerow([archive_group, collection, aip])

            report_open.close()

        # Ignore anything else in this folder.
        # TODO: I don't think this is necessary.
        else:
            continue