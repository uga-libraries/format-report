"""
Combines the ARCHive format reports, which are one CSV per group, into single CSVs for analysis.

One CSV (archive_formats_YYYYMM.csv) has the information organized by group and then by unique format. It includes
the ARCHive group, number of file identifications, format type, and format standardized name. It is used for
aggregating the number of file identifications. The numbers are inflated by files that have more than one possible
format identification.

The other CSV (archive_formats_by_aip_YYYYMM.csv) has the information organized by AIP and then by unique format. It
includes the ARCHive group, collection identifier, AIP identifier, and format information (format type,
format standardized name, format name, format version, registry name, registry key, and format note). It is used for
aggregating the number of collections and AIPs.

Before running this script, run update_standardization.py
"""

# Usage: python /path/merge_format_reports.py /path/report_folder [/path/standardize_formats.csv]
# Report folder should contain the ARCHive format reports. Script output is saved to this folder as well.
# A default value for the path to the standardize formats csv is used if one is not provided as an argument.

import csv
import datetime
import os
import re
import sys


def standardize_formats(format_name, standard):
    """Finds the format name within the standardized formats csv and returns the standard (simplified) format
    name and the format type. Using a standardized name and assigning a format type reduces some of the data
    variability so summaries are more useful."""

    # Reads the standardized formats csv.
    with open(standard) as standard_list:
        read_standard_list = csv.reader(standard_list)

        # Skips the header.
        next(read_standard_list)

        # Checks each row for the format. When there is a match, returns the standardized name and format type.
        # Matches lowercase versions of the format names to ignore variations in capitalization.
        for standard_row in read_standard_list:
            if format_name.lower() == standard_row[0].lower():
                return standard_row[1], standard_row[2]

        # If there was no match (meaning the previous code block did not return a result so the function keeps
        # running), prints an error message and quits the script.
        print(f'Could not match the format name "{format_name}" in standardize_formats.csv.')
        print('Update that CSV using update_standardization.py and run this script again.')
        exit()


def collection_from_aip(aip_id, group):
    """Returns the collection id. The collection id is extracted from the AIP id based on each group's rules for
    constructing AIP ids, all of which include the collection id. If the pattern does not match any known rules,
    the function returns None and the error is caught where the function is called."""

    # Brown Media Archives and Peabody Awards Collection
    if group == 'bmac':

        if aip_id[5].isdigit():
            return 'peabody'

        # The next three address errors with how the AIP ID was made.
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
        # The collection number is changed to an integer to remove leading zeros.
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

    # At the time of writing this script, there were no AIPs in dlg-magil.
    elif group == 'dlg-magil':
        return None

    # Hargrett Rare Book and Manuscript Library
    elif group == 'hargrett':
        coll_regex = re.match('^(.*)(er|-web)', aip_id)
        return coll_regex.group(1)

    # Richard B. Russell Library for Research and Studies.
    # The same collection can be formatted rbrl-### or rbrl###, so normalizing all IDs to rbrl### to avoid duplicates.
    elif group == 'russell':
        coll_regex = re.match('^rbrl-?([0-9]{3})', aip_id)
        coll_id = f'rbrl{coll_regex.group(1)}'
        return coll_id

    # This would catch a new group.
    else:
        return None


# Makes the report folder (a script argument) the current directory. If the argument is missing or not a valid
# directory, displays an error message and quits the script.
try:
    report_folder = sys.argv[1]
    os.chdir(report_folder)
except (IndexError, FileNotFoundError):
    print("The report folder path was either not given or is not a valid directory. Please try the script again.")
    print("Script usage: python /path/merge_format_reports.py /path/format_reports [/path/standardize_formats.csv]")
    exit()

# Makes a variable with the file path for the standardized formats csv. Uses the optional script argument if provided,
# or else uses the folder with this script as the default location for that CSV.
try:
    standard_csv = sys.argv[2]
except IndexError:
    standard_csv = os.path.join(sys.path[0], 'standardize_formats.csv')

# Increases the size of CSV fields to handle long AIP lists.
# Gets the maximum size that doesn't give an overflow error.
while True:
    try:
        csv.field_size_limit(sys.maxsize)
        break
    except OverflowError:
        sys.maxsize = int(sys.maxsize / 10)

# Gets the current date, formatted YYYYMM, to use in naming the script outputs.
today = datetime.datetime.now().strftime("%Y-%m")

# Makes two CSV files for saving the combined format information in the same folder as the ARCHive format reports.
# archive_formats_YYYYMM.csv is organized by format name and then by group, and is used for analyzing file counts.
# archive_formats_by_aip.YYYYMM.csv is organized by AIP and then format name, and is used for collection and aip counts.
with open(f'archive_formats_{today}.csv', 'w', newline='') as by_format, open(f'archive_formats_by_aip_{today}.csv',
                                                                              'w', newline='') as by_aip:
    by_format_csv = csv.writer(by_format)
    by_aip_csv = csv.writer(by_aip)

    # Adds a header to each CSV.
    by_format_csv.writerow(['Group', 'File_IDs', 'Format_Type', 'Format_Standardized_Name'])
    by_aip_csv.writerow(['Group', 'Collection', 'AIP', 'Format_Type', 'Format_Standardized_Name', 'Format_Name',
                         'Format_Version', 'Registry_Name', 'Registry_Key', 'Format_Note'])

    # Gets data from each group's format report and calculates additional information based on that data.
    # The information is saved to one or both CSV files.
    for report in os.listdir():

        # Skips the file if it is not a format report. The usage report and potentially other files are in this folder.
        if not report.startswith('file_formats'):
            continue

        # Gets the ARCHive group from the format report filename. Will be saved to both CSVs.
        regex = re.match('file_formats_(.*).csv', report)
        archive_group = regex.group(1)

        # Gets the data from the report.
        with open(report, 'r') as open_report:
            report_info = csv.reader(open_report)

            # Skips the header.
            next(report_info)

            # Gets the data from each row in the report.
            for row in report_info:

                # Gets the standard name and format type for the format. Will be saved to both CSVs.
                format_standard, format_type = standardize_formats(row[2], standard_csv)

                # Writes the group, file id count, format type, and format standardized name to the by format csv.
                by_format_csv.writerow([archive_group, row[1], format_type, format_standard])

                # Gets a list of AIPs in this row, calculates the row information for each AIP, and saves the AIP
                # rows to the by aip csv. The values are saved to a variable (aip_row) before writing them to the CSV
                # so that empty values can be replaced with 'NO VALUE' and make it more clear where there is no data.
                aip_list = row[7].split('|')
                for aip in aip_list:
                    collection_id = collection_from_aip(aip, archive_group)
                    # Prints a warning if the script was unable to calculate a collection id.
                    if collection_id is None:
                        print("Could not calculate collection id for", aip)
                    aip_row = [archive_group, collection_id, aip, format_type, format_standard, row[2], row[3], row[4],
                               row[5], row[6]]
                    aip_row = ['NO VALUE' if x == '' else x for x in aip_row]
                    by_aip_csv.writerow(aip_row)
