# This is an experiment. What if the merged CSV was organized by AIP instead of by format?
# Would that make for easier analysis and seeing where duplicates are?
# Would it let me switch to pandas for subtotals for everything?

import csv
import os
import re
import sys

# TODO: this runs csv_merge.py as well. It is ok to make the other merged reports but not really needed.
from csv_merge import collection_from_aip


def update_row(row, group):
    """Return a list of lists with all the new rows, reorganized to one row by AIP. Adds collection ID, format type,
    and format standardized name. Replaces empty cells with 'NO VALUE'. Final order is: group, collection id, AIP id,
    format type, format standardized name, format name, format version, registry name, registry key, and format note.
    """

    # Starts a list to hold the list of AIP rows.
    rows = []

    # For each AIP:
    aip_list = row[7].split('|')
    for aip in aip_list:

        # Get collection id
        collection_id = collection_from_aip(aip, group)

        # Get format type and format standardized name
        # Reads the standardized formats csv.
        format_name = "NO MATCH"
        format_type = "NO MATCH"
        with open(standard_csv) as standard_list:
            read_standard_list = csv.reader(standard_list)

            # Skips the header.
            next(read_standard_list)

            # Checks each row for the format. When there is a match, returns the standardized name and format type.
            # Matching lowercase versions of the format names to ignore variations in capitalization.
            # Note: considered just matching the start of the name for fewer results for formats that include file
            # size or other details in the name, but this caused too many errors from different formats that start with
            # the same string.
            for standard_row in read_standard_list:
                if row[2].lower() == standard_row[0].lower():
                    format_name = standard_row[1]
                    format_type = standard_row[2]

        # Make the row
        aip_row = [group, collection_id, aip, format_type, format_name, row[2], row[3], row[4], row[5], row[6]]

        # Fills all empty cells with 'NO VALUE' so it is easier to see where there is no data.
        aip_row = ['NO VALUE' if x == '' else x for x in aip_row]

        # Add the row to the rows list
        rows.append(aip_row)

    # Return the list of rows to add to the csv.
    return rows


# Makes the report folder (script argument) the current directory. Displays an error message and quits the script if
# the argument is missing or not a valid directory.
try:
    report_folder = sys.argv[1]
    os.chdir(report_folder)
except (IndexError, FileNotFoundError):
    print("The report folder path was either not given or is not a valid directory. Please try the script again.")
    print("Script usage: python /path/csv_merge_by_aip.py /path/reports [/path/standardize_formats.csv]")
    exit()

# Makes a variable with the file path for the standardize formats CSV. Uses the optional script argument if provided,
# or else uses the folder with this script as the default location.
try:
    standard_csv = sys.argv[2]
except IndexError:
    standard_csv = os.path.join(sys.path[0], 'standardize_formats.csv')

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

        # Skips the file if it is not a format report. The usage report and some script outputs are also in this folder.
        if not report.startswith('file_formats'):
            continue

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
                # Updates the row to add additional information and fill in blank cells using another function and saves
                # the updated row to the CSV.
                new_rows = update_row(data, archive_group)
                for row in new_rows:
                    result_csv.writerow(row)
