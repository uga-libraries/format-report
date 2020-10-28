# This is an experiment. What if the merged CSV was organized by AIP instead of by format?
# Would that make for easier analysis and seeing where duplicates are?
# Would it let me switch to pandas for subtotals for everything?

import csv
import os
import sys


def update_row(row, group):
    """Return a list of lists with all the new rows, reorganized by AIP"""
    # Goal: ['Group', 'Collection', 'AIP', 'Format_Type', 'Format_Standardized_Name', 'Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'Format_Note']

    # Will ultimately be the list of rows.
    rows = []

    # For each AIP:
    aip_list = row[7].split('|')
    for aip in aip_list:
        print(aip)

standard_csv = 'C:/users/amhan/Documents/GitHub/format-report/standardize_formats.csv'
report_folder = 'C:/users/amhan/Documents/GitHub/format-report/testing/2020-10-26_prod'
os.chdir(report_folder)

# Increases the size of csv fields to handle long aip lists.
# Gets the maximum size that doesn't give an overflow error.
while True:
    try:
        csv.field_size_limit(sys.maxsize)
        break
    except OverflowError:
        sys.maxsize = int(sys.maxsize / 10)

# Makes a CSV file for the merged reports named archive_formats_date.csv in the same folder as the ARCHive reports.
# Gets each row from each group's format report, updates the row, and saves the updated row to the CSV.
with open('archive_formats_by_aip.csv', 'w', newline='') as result:
    result_csv = csv.writer(result)

    # Adds a header to the results file.
    result_csv.writerow(
        ['Group', 'Collection', 'AIP', 'Format_Type', 'Format_Standardized_Name', 'Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'Format_Note'])

    for report in os.listdir():

        # # Skips the file if it is not a format report. The usage report and some script outputs are also in this folder.
        # if not report.startswith('file_formats'):
        #     continue

        # TODO: This is for testing. Switch back to combining reports.
        if not report == 'test_format.csv':
            continue

        # TODO: put back once done with testing
        archive_group = 'hargrett'
        # # Gets the ARCHive group from the format report filename.
        # regex = re.match('file_formats_(.*).csv', report)
        # archive_group = regex.group(1)

        # Gets the data from the report.
        with open(report, 'r') as open_report:
            report_info = csv.reader(open_report)

            # Skips the header.
            next(report_info)

            # Gets the data from each row in the report.
            for data in report_info:
                # Updates the row to add additional information and fill in blank cells using another function and saves
                # the updated row to the CSV.
                new_rows = update_row(data, archive_group)
                # for row in new_rows:
                #     result_csv.writerow(row)
