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


# Gets the current date, formatted YYYYMM, to use in naming the results files.
today = datetime.datetime.now().strftime("%Y-%m")

# Makes two csv files for saving the combined format information in the same folder as the ARCHive format reports.
# archive_formats_YYYYMM.csv is organized by format name and then by group, and is used for analyzing file counts.
# archive_formats_by_aip.YYYYMM.csv is organized by AIP and then format name, and is used for collection and aip counts.
with open(f'archive_formats_{today}.csv', 'w', newline='') as by_format, open(f'archive_formats_by_aip_{today}.csv', 'w', newline='') as by_aip:
    by_format_csv = csv.writer(by_format)
    by_aip_csv = csv.writer(by_aip)

    # Adds a header to each csv file.
    by_format_csv.writerow(['Group', 'File_IDs', 'Format_Type', 'Format_Standardized_Name'])
    by_aip_csv.writerow(['Group', 'Collection', 'AIP', 'Format_Type', 'Format_Standardized_Name', 'Format_Name',
                         'Format_Version', 'Registry_Name', 'Registry_Key', 'Format_Note'])

    # Gets data from each group's format reports and calculates additional information based on that data.
    # The information is saved to both CSV files, organized in a different way.
    for report in os.listdir():

        # Skips the file if it is not a format report. The usage report and potentially other files are in this folder.
        if not report.startswith('file_formats'):
            continue

        # Prints the script progress since this script can be slow to run.
        print("\nStarting next report:", report)

        # Gets the ARCHive group from the format report filename.
        regex = re.match('file_formats_(.*).csv', report)
        archive_group = regex.group(1)

        # Gets the data from the report.
        with open(report, 'r') as open_report:
            report_info = csv.reader(open_report)

            # Skips the header.
            next(report_info)

            # Gets the data from each row in the report.
            for data in report_info:
                by_format_csv.writerow([archive_group, data[1], 'type', 'name'])
                by_aip_csv.writerow([archive_group, data[2]])



