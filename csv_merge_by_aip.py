"""Combines the format reports (csv files) for all groups from the UGA Libraries' digital preservation system (
ARCHive) into a single csv for analysis. There is one row of data per AIP and format, so an AIP will be repeated if
it contains more than one format. All data is copied from the format reports. Columns are also added for the group
name, collection id, format type, and standardized format name.

Prior to running this script, all format reports should be downloaded from ARCHive and saved to a folder.

The hope is this will expand our data analysis potential."""

# Usage: python /path/csv_merge_by_aip.py /path/reports [/path/standard_csv]
#       /path/reports is the folder with the ARCHive format reports
#       /path/standard_csv is optional. Default is to use the csv in the same folder as this script.

import csv
import os
import re
import sys

# TODO: this runs csv_merge.py script as well, making a merged report organized by format still.
# It is ok to make the other merged reports but not really needed.
from csv_merge import collection_from_aip


def update_row(row, group):
    """Returns a list of lists with all the new rows, reorganized to one row per AIP and format. For each row,
    adds collection ID, format type and format standardized name, and replaces empty cells with 'NO VALUE'. The final
    order is: group, collection id, AIP id, format type, format standardized name, format name, format version,
    registry name, registry key, and format note."""

    # Starts a list to hold the lists of new AIP rows.
    aip_rows = []

    # Gets all the AIPs, which are in a pipe separated string in row[7], and makes the new row for each one.
    aip_list = row[7].split('|')
    for aip in aip_list:

        # Calculates the collection id from the AIP id.
        collection_id = collection_from_aip(aip, group)

        # Gets the format type and format standardized name from the standardized formats csv.
        format_name = "NO MATCH"
        format_type = "NO MATCH"
        with open(standard_csv) as standard_list:
            read_standard_list = csv.reader(standard_list)

            # Skips the header.
            next(read_standard_list)

            # Checks each row for the format name. When there is a match, returns the standardized name and format type.
            # Matching the lowercase versions of the format names to ignore variations in capitalization.
            for standard_row in read_standard_list:
                if row[2].lower() == standard_row[0].lower():
                    format_name = standard_row[1]
                    format_type = standard_row[2]

        # Makes the list with the row data for this AIP.
        aip_row = [group, collection_id, aip, format_type, format_name, row[2], row[3], row[4], row[5], row[6]]

        # Fills all empty cells with 'NO VALUE' so it is easier to see where there is no data.
        aip_row = ['NO VALUE' if x == '' else x for x in aip_row]

        # Adds the AIP row to the list of new AIP rows.
        aip_rows.append(aip_row)

    # Return the list of new AIP rows.
    return aip_rows


# Makes the report folder (script argument) the current directory. Displays an error message and quits the script if
# the argument is missing or not a valid directory.
try:
    report_folder = sys.argv[1]
    os.chdir(report_folder)
except (IndexError, FileNotFoundError):
    print("The report folder path was either not given or is not a valid directory. Please try the script again.")
    print("Script usage: python /path/csv_merge_by_aip.py /path/reports [/path/standardize_formats.csv]")
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

# TODO: include the date as part of the filename again?
# Makes a CSV file for the merged reports named archive_formats_by_aip.csv in the same folder as the ARCHive reports.
with open('archive_formats_by_aip.csv', 'w', newline='') as result:
    result_csv = csv.writer(result)

    # Adds a header to the results file.
    result_csv.writerow(
        ['Group', 'Collection', 'AIP', 'Format_Type', 'Format_Standardized_Name', 'Format_Name', 'Format_Version',
         'Registry_Name', 'Registry_Key', 'Format_Note'])

    # Finds the format reports in the report folder.
    for report in os.listdir():

        # Skips the file if it is not a format report. Other files, including the usage report, may be in this folder.
        if not report.startswith('file_formats'):
            continue

        # Prints the script progress since this script can be slow to run.
        print("Starting next report:", report)

        # Gets the ARCHive group from the format report filename.
        regex = re.match('file_formats_(.*).csv', report)
        archive_group = regex.group(1)

        # Gets the data from the report.
        with open(report, 'r') as open_report:
            report_info = csv.reader(open_report)

            # Skips the header.
            next(report_info)

            # Gets each row from the format report. Updates the row to split it to one row per AIP (if more than
            # one), add additional information, and fill in blank cells. Saves each updated row to the results CSV.
            for data in report_info:
                new_rows = update_row(data, archive_group)
                for row in new_rows:
                    result_csv.writerow(row)
