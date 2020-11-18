# This is an experiment to create the "by format" and "by aip then format" versions fo the csv.
# Need "by format" to do file counts but everything else is easier with "by aip then format".

import csv
import datetime
import os
import re
import sys


# THE FOLLOWING IS EVERYTHING BUT THE FUNCTIONS FROM THE TWO SEPARATE SCRIPTS.
# MOVE OVERLAPPING CONTENT, E.G. READING GROUP FORMAT REPORTS, TO FUNCTIONS BOTH CAN CALL.

# Makes the report folder (script argument) the current directory. Displays an error message and quits the script if
# the argument is missing or not a valid directory.
try:
    report_folder = sys.argv[1]
    os.chdir(report_folder)
except (IndexError, FileNotFoundError):
    print("The report folder path was either not given or is not a valid directory. Please try the script again.")
    print("Script usage: python /path/merge_format_reports.py /path/format_reports [/path/standardize_formats.csv]")
    exit()

# Makes a variable with the file path for the standardized formats CSV. Uses the optional script argument if provided,
# or else uses the folder with this script as the default location for that csv.
try:
    standard_csv = sys.argv[2]
except IndexError:
    standard_csv = os.path.join(sys.path[0], 'standardize_formats.csv')

# Increases the size of csv fields to handle long AIP lists.
# Gets the maximum size that doesn't give an overflow error.
while True:
    try:
        csv.field_size_limit(sys.maxsize)
        break
    except OverflowError:
        sys.maxsize = int(sys.maxsize / 10)

# Gets the current date, formatted YYYYMM, to use in naming the merged files.
today = datetime.datetime.now().strftime("%Y-%m")

# Makes a CSV file with all format information organized by format name and then by group.
# This file is used for analyzing file counts.
# The file is named archive_formats_YYYYMM.csv and saved in the same folder as the ARCHive format reports.
with open(f'archive_formats_{today}.csv', 'w', newline='') as result:
    result_csv = csv.writer(result)

    # Adds a header to the results file.
    result_csv.writerow(
        ['Group', 'Collection_Count', 'AIP_Count', 'File_IDs', 'Format_Type', 'Format_Standardized_Name',
         'Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'Format_Note', 'Collection_List',
         'AIP_List'])

    # for report in os.listdir():
    #
    #     # Skips the file if it is not a format report. The usage report and some script outputs are also in this folder.
    #     if not report.startswith('file_formats'):
    #         continue
    #
    #     # Gets the ARCHive group from the format report filename.
    #     regex = re.match('file_formats_(.*).csv', report)
    #     archive_group = regex.group(1)
    #
    #     # Gets the data from the report.
    #     with open(report, 'r') as open_report:
    #         report_info = csv.reader(open_report)
    #
    #         # Skips the header.
    #         next(report_info)
    #
    #         # Gets the data from each row in the report.
    #         for data in report_info:
    #             # Updates the row to add additional information and fill in blank cells using another function and saves
    #             # the updated row to the CSV.
    #             new_row = update_row(data, archive_group)
    #             result_csv.writerow(new_row)

# Makes a CSV file with all format information organized by AIP and then by format name.
# This file is used for analyzing collection and AIP counts. This structure makes it easier to remove duplicates.
# The file is named archive_formats_by_aip_YYYYMM.csv and saved in the same folder as the ARCHive format reports.
with open(f'archive_formats_by_aip_{today}.csv', 'w', newline='') as result:
    result_csv = csv.writer(result)

    # Adds a header to the results file.
    result_csv.writerow(
        ['Group', 'Collection', 'AIP', 'Format_Type', 'Format_Standardized_Name', 'Format_Name', 'Format_Version',
         'Registry_Name', 'Registry_Key', 'Format_Note'])

    # # Finds the format reports in the report folder.
    # for report in os.listdir():
    #
    #     # Skips the file if it is not a format report. Other files, including the usage report, may be in this folder.
    #     if not report.startswith('file_formats'):
    #         continue
    #
    #     # Prints the script progress since this script can be slow to run.
    #     print("Starting next report:", report)
    #
    #     # Gets the ARCHive group from the format report filename.
    #     regex = re.match('file_formats_(.*).csv', report)
    #     archive_group = regex.group(1)
    #
    #     # Gets the data from the report.
    #     with open(report, 'r') as open_report:
    #         report_info = csv.reader(open_report)
    #
    #         # Skips the header.
    #         next(report_info)
    #
    #         # Gets each row from the format report. Updates the row to split it to one row per AIP (if more than
    #         # one), add additional information, and fill in blank cells. Saves each updated row to the results CSV.
    #         for data in report_info:
    #             new_rows = update_row(data, archive_group)
    #             for row in new_rows:
    #                 result_csv.writerow(row)
