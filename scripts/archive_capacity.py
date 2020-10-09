"""Makes a summary of the current holdings of ARCHive (number of collections, AIPs, and TB), overall and by group,
using information from the ARCHive format reports and the usage report. """
# TODO: use the AIP count from the usage report and the collection list from the merged report instead.

import csv
import os
import re
import sys

# Imports a function for calculating the collection id based on the AIP ID.
# from csv_merge import collection_from_aip

# TODO: argument error handling
# Makes variables for the input of the script.
formats_report = sys.argv[1]
usage_report = sys.argv[2]

# Makes the report folder the current directory.
report_folder = sys.argv[3]
os.chdir(report_folder)

# def aip_list(report_info):
#     """Makes a unique list of AIPs from the report. """
#
#     # Makes a variable for storing the AIP IDs.
#     aip_list = []
#
#     # Skips the header row.
#     next(report_info)
#
#     # For each row, gets the AIP IDs (a string with each ID separated by a pipe) and converts to a list.
#     # Adds the AIP ID to the aip_list if it is not already in the list.
#     for row in report_info:
#         aips = row[7].split('|')
#         for aip in aips:
#             if aip not in aip_list:
#                 aip_list.append(aip)
#
#     # Returns the result: a unique list of AIP IDs from this report.
#     return aip_list
#
#
# # Increases the size of csv fields to handle long AIP lists.
# # Gets the maximum size that doesn't give an overflow error.
# while True:
#     try:
#         csv.field_size_limit(sys.maxsize)
#         break
#     except OverflowError:
#         sys.maxsize = int(sys.maxsize / 10)
#
# # Makes a temporary file for the aggregated information named archive_aiplist_date.csv.
# with open(f'archive_aiplist_{today}.csv', 'w', newline='') as aiplist:
#     aiplistcsv = csv.writer(aiplist)
#
#     # Adds a header to the temporary file.
#     aiplistcsv.writerow(['Group', 'Collection', 'AIP'])
#
#     # Gets each format report.
#     for report in os.listdir(report_folder):
#         if report.startswith('file_formats'):
#
#             # Gets the ARCHive group from the filename.
#             regex = re.match('file_formats_\d{8}_(.*).txt', report)
#             archive_group = regex.group(1)
#
#             # Gets the data from the report, which is a tab-delimited text file.
#             report_open = open(report, 'r')
#             report_info = csv.reader(report_open, delimiter='\t')
#
#             # Gets a list of unique AIP IDs.
#             aips = aip_list(report_info)
#
#             # Calculates the collection number for each AIP ID and saves the group, collection id, and AIP id to the
#             # temporary file.
#             for aip in aips:
#                 collection = collection_from_aip(aip, archive_group)
#                 aiplistcsv.writerow([archive_group, collection, aip])
#
#             report_open.close()
#
#         # Ignore anything else in this folder.
#         # TODO: I don't think this is necessary.
#         else:
#             continue
#
# # TODO: Creating a summary of the temp file. Or eliminate the temp file altogether.
# # ERROR: permission denied for the temporary file
#
# # Read the data from the temporary file.
# df = pd.read_csv(f'archive_aiplist{today}.csv')
#
# # Get the number of AIPs for each group.
# # This is just an example: need to make the summary report to save it to.
# aip_totals = df.groupby('Group').count()
# aip_totals.to_csv(f'aip_total.csv')
