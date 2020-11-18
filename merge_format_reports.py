# This is an experiment to create the "by format" and "by aip then format" versions fo the csv.
# Need "by format" to do file counts but everything else is easier with "by aip then format".

import csv
import datetime
import os
import re
import sys


def standardize_formats(format_name, standard):
    """Finds the format name within the standardized formats csv and returns the standard (simplified) format
    name and the format type. Using a standardized name and assigning a format type reduces some of the data
    variability so summaries are more useful. Can rely on there being a match because update_normalized.py is run
    first.

    Standard format name is based on PRONOM, although sometimes the name truncated to group more names together. For
    formats not in PRONOM, we either truncated the name or left it as it was. Occasionally researched the most
    common form of the name.

    Format type is based on mimetypes, with additional local categories used where more nuance was needed for
    meaningful results, e.g. application and text. """

    # Reads the standardized formats csv.
    with open(standard) as standard_list:
        read_standard_list = csv.reader(standard_list)

        # Skips the header.
        next(read_standard_list)

        # Checks each row for the format. When there is a match, returns the standardized name and format type.
        # Matching lowercase versions of the format names to ignore variations in capitalization.
        # Note: considered just matching the start of the name for fewer results for formats that include file
        # size or other details in the name, but this caused too many errors from different formats that start with
        # the same string.
        for standard_row in read_standard_list:
            if format_name.lower() == standard_row[0].lower():
                return standard_row[1], standard_row[2]

        # If there was no match (the previous code block did not return a result, which exits this function and keeps
        # this code block from running), prints an error message and quits the script. Run update_standardization.py to
        # make sure that standardize_formats.csv will have a match for all formats.
        print(f'Could not match the format name "{format_name}" in standardize_formats.csv.')
        print('Update that CSV and run this script again.')
        print('Note that the archive_formats CSV produced by the script only has formats up until this point.')
        exit()


def collection_from_aip(aip_id, group):
    """Returns the collection id. The collection id is extracted from the AIP id based on the various rules each
    group has for constructing AIP ids for different collections. If the pattern does not match any known rules,
    the function returns None and the error is caught where the function is called."""

    # Brown Media Archives and Peabody Awards Collection
    if group == 'bmac':

        if aip_id[5].isdigit():
            return 'peabody'

        # The next three address errors with how AIP ID was made.
        elif aip_id.startswith('har-ms'):
            coll_regex = re.match('(^har-ms[0-9]+)_', aip_id)
            return coll_regex.group(1)

        elif aip_id.startswith('bmac_bmac_wsbn'):
            return 'wsbn'

        elif aip_id.startswith('bmac_wrdw_'):
            return 'wrdw-video'

        else:
            coll_regex = re.match('^bmac_([a-z0-9-]+)_', aip_id)
            return coll_regex.group(1)

    # Digital Library of Georgia
    elif group == 'dlg':

        # Everything in turningpoint is also in another collection, which is the one we want.
        # The collection number is made into an integer to remove leading zeros.
        if aip_id.startswith('dlg_turningpoint'):

            # This one is from an error in the AIP ID.
            if aip_id == 'dlg_turningpoint_ahc0062f-001':
                return 'geh_ahc-mss820f'

            elif aip_id.startswith('dlg_turningpoint_ahc'):
                coll_regex = re.match('dlg_turningpoint_ahc([0-9]{4})([a-z]?)-', aip_id)
                if coll_regex.group(2) == 'v':
                    return f'geh_ahc-vis{int(coll_regex.group(1))}'
                else:
                    return f'geh_ahc-mss{int(coll_regex.group(1))}{coll_regex.group(2)}'

            elif aip_id.startswith('dlg_turningpoint_ghs'):
                coll_regex = re.match('dlg_turningpoint_ghs([0-9]{4})([a-z]*)', aip_id)
                if coll_regex.group(2) == 'bs':
                    return f'g-hi_ms{coll_regex.group(1)}-bs'
                else:
                    return f'g-hi_ms{coll_regex.group(1)}'

            elif aip_id.startswith('dlg_turningpoint_harg'):
                coll_regex = re.match('dlg_turningpoint_harg([0-9]{4})([a-z]?)', aip_id)

                return f'guan_ms{int(coll_regex.group(1))}{coll_regex.group(2)}'

        elif aip_id.startswith('batch_gua_'):
            return 'dlg_ghn'

        else:
            coll_regex = re.match('^([a-z0-9-]*_[a-z0-9-]*)_', aip_id)
            return coll_regex.group(1)

    # Digital Library of Georgia: Hargrett Rare Book and Manuscript Library
    elif group == 'dlg-hargrett':
        coll_regex = re.match('^([a-z]{3,4}_[a-z0-9]{4})_', aip_id)
        return coll_regex.group(1)

    # NOTE: At the time of writing this script, there were no AIPs in dlg-magil. This will need to be updated.
    elif group == 'dlg-magil':
        return None

    # Hargrett Rare Book and Manuscript Library
    elif group == 'hargrett':
        coll_regex = re.match('^(.*)(er|-web)', aip_id)
        return coll_regex.group(1)

    # Richard B. Russell Library for Research and Studies.
    elif group == 'russell':
        coll_regex = re.match('^rbrl-?[0-9]{3}', aip_id)
        return coll_regex.group()


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
with open(f'archive_formats_{today}.csv', 'w', newline='') as by_format, open(f'archive_formats_by_aip_{today}.csv',
                                                                              'w', newline='') as by_aip:
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
        print("Starting next report:", report)

        # Gets the ARCHive group from the format report filename.
        regex = re.match('file_formats_(.*).csv', report)
        archive_group = regex.group(1)

        # Gets the data from the report.
        with open(report, 'r') as open_report:
            report_info = csv.reader(open_report)

            # Skips the header.
            next(report_info)

            # Gets the data from each row in the report.
            for row in report_info:

                # Gets the standard name and format type for the format. Used in both CSVs.
                format_standard, format_type = standardize_formats(row[2], standard_csv)

                # Writes group, file id count, format type, and format standardized name to by format CSV.
                by_format_csv.writerow([archive_group, row[1], format_type, format_standard])

                # Gets a list of AIPs in this row, calculates their collection, and saves each AIP to its own row in
                # the by aip CSV, with additional format information copied from the reports
                aip_list = row[7].split('|')
                for aip in aip_list:
                    collection_id = collection_from_aip(aip, archive_group)
                    aip_row = [archive_group, collection_id, aip, format_type, format_standard, row[2], row[3], row[4],
                               row[5], row[6]]
                    # Fills all empty cells with 'NO VALUE' so it is easier to see where there is no data.
                    aip_row = ['NO VALUE' if x == '' else x for x in aip_row]
                    by_aip_csv.writerow(aip_row)
