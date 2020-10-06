"""Combines the format reports (tab delimited text files) for all groups from the UGA Libraries' digital preservation
system (ARCHive) into a single csv for analysis. All data is copied from the format reports except the AIP list,
which is converted into a collection list. A column is also added for the group name.

Usage: python /path/csv_merge.py /path/report_folder /path/standard_csv"""

import csv
import datetime
import os
import re
import sys

# Makes variables from script arguments
#    report_folder is the directory with the ARCHive format reports to be analyzed.
#    standardize_csv has the path to the csv document with current standardization rules.
# TODO: add error handling
# TODO: standard_csv is in the same folder as the script. Can it reference the csv without a path?
report_folder = sys.argv[1]
standard_csv = sys.argv[2]

# Make current directory the report folder.
os.chdir(report_folder)


def collection_from_aip(aip, group):
    """Determine the collection id based on the aip id."""

    if group == 'bmac':

        if aip[5].isdigit():
            return 'peabody'

        # The next three address errors with how aip id was made.
        elif aip.startswith('har-ms'):
            coll_regex = re.match('(^har-ms[0-9]+)_', aip)
            return coll_regex.group(1)

        elif aip.startswith('bmac_bmac_wsbn'):
            return 'wsbn'

        elif aip.startswith('bmac_wrdw_'):
            return 'wrdw-video'

        else:
            coll_regex = re.match('^bmac_([a-z0-9-]+)_', aip)
            return coll_regex.group(1)

    elif group == 'dlg':

        # Everything in turningpoint is also in another collection, which is the one we want.
        if aip.startswith('dlg_turningpoint'):

            # This one is from an error in the aip id.
            if aip == 'dlg_turningpoint_ahc0062f-001':
                return 'geh_ahc-mss820f'

            elif aip.startswith('dlg_turningpoint_ahc'):
                coll_regex = re.match('dlg_turningpoint_ahc([0-9]{4})([a-z]?)-', aip)
                number = int(coll_regex.group(1))
                if coll_regex.group(2) == 'v':
                    return f'geh_ahc-vis{number}'
                else:
                    return f'geh_ahc-mss{number}{coll_regex.group(2)}'

            elif aip.startswith('dlg_turningpoint_ghs'):
                coll_regex = re.match('dlg_turningpoint_ghs([0-9]{4})([a-z]*)', aip)
                if coll_regex.group(2) == 'bs':
                    return f'g-hi_ms{coll_regex.group(1)}-bs'
                else:
                    return f'g-hi_ms{coll_regex.group(1)}'

            elif aip.startswith('dlg_turningpoint_harg'):
                coll_regex = re.match('dlg_turningpoint_harg([0-9]{4})([a-z]?)', aip)
                number = int(coll_regex.group(1))
                return f'guan_ms{number}{coll_regex.group(2)}'

            else:
                return 'turningpoint no match'

        elif aip.startswith('batch_gua_'):
            return 'dlg_ghn'

        else:
            coll_regex = re.match('^([a-z0-9-]*_[a-z0-9-]*)_', aip)
            return coll_regex.group(1)

    elif group == 'dlg-hargrett':
        coll_regex = re.match('^([a-z]{3,4}_[a-z0-9]{4})_', aip)
        return coll_regex.group(1)

    elif group == 'hargrett':
        coll_regex = re.match('^(.*)er', aip)
        return coll_regex.group(1)

    elif group == 'russell':
        coll_regex = re.match('^rbrl-?[0-9]{3}', aip)
        return coll_regex.group()

    else:
        return 'new group'


def update_row(row, group):
    """Calculate and add new data, replace the aip list with a collection list, and fill in empty cells.
       New data is group name, collection count, standardized version of the format name, and format type."""

    def collection_list(aip_list):
        """Change aip list to a unique list of collections.
           Return a string with comma-separated collection ids and a count of the number of collections."""

        # Split aip_list (a string) into a list. Items are divided by a pipe.
        aips = aip_list.split('|')

        collections_list = []

        # Extract collection id from aip id.
        # Put in error message if the pattern is new so it can be fixed.
        for aip in aips:
            try:
                collection = collection_from_aip(aip, group)
            except AttributeError:
                print('Check for collection errors in merged csv')
                collection = f"Collection not calculated for {aip}"

            # Make a unique list of collections.
            if collection not in collections_list:
                collections_list.append(collection)

        # Convert the list of collections to a string with each collection separated by a comma.
        collections_string = ', '.join(map(str, collections_list))

        # Return both the string with the collections and a count of the number of collections.
        return collections_string, len(collections_list)

    def standardize_formats(format_name, standard):
        """Find the format name within the standardized formats csv and return the standard (simplified) format name and
        format type. Using a standardized name and assigning a format type reduces some of the data variability so
        summaries are more useful. Can rely on there being a match because update_normalized.py is run first.

        Standard format name is based on PRONOM, although sometimes truncated to group more names together. For
        formats not in PRONOM, either truncated the name or left it as it was. Occasionally researched the most
        common form of the name.

        Format type is based on mimetypes, with additional local categories used where more nuance was needed for
        meaningful results, e.g. application and text. """

        # Reads the standardized formats csv.
        with open(standard) as standard_list:
            read_standard_list = csv.reader(standard_list)

            # Skips the header.
            next(read_standard_list)

            # Checks each row for the format. When there is a match, return the name and type. Matching lowercase
            # versions of the format names to ignore variations in capitalization. Note: considered just matching the
            # start of the name for fewer results for formats that include file size or other details in the name,
            # but this caused too many errors and false positives from different formats that start with the same
            # string.
            for standard_row in read_standard_list:
                if format_name.lower() == standard_row[0].lower():
                    return standard_row[1], standard_row[2]

    # Gets standard name for format and format type.
    format_standard, format_type = standardize_formats(row[2], standard_csv)

    # Gets list of collections from the aip ids and
    collections, number_collections = collection_list(row[7])

    # Replaces the aip list with the collection list.
    row[7] = collections

    # Adds the group and number of collections at the beginning of the row.
    # Adds the format type and standardized format name before the format name.
    row.insert(0, group)
    row.insert(1, number_collections)
    row.insert(4, format_type)
    row.insert(5, format_standard)

    # Fills all empty cells with 'NO VALUE'
    row = ['NO VALUE' if x == '' else x for x in row]

    # Returns the updated version of the row.
    return row


# Increase size of csv fields to handle long aip lists.
# Gets the maximum size that doesn't give an overflow error.
while True:
    try:
        csv.field_size_limit(sys.maxsize)
        break
    except OverflowError:
        sys.maxsize = int(sys.maxsize / 10)

# Gets the current date, formatted YYYYMM, to use in naming the result file.
# TODO: is this necessary? Is this meaningful? Not necessarily doing the merge the month of the download.
today = datetime.datetime.now().strftime("%Y-%m")

# Make a file for results named archive_formats_date.csv.
# Get each row from each report, update it, and save to the results file.
with open(f'archive_formats_{today}.csv', 'w', newline='') as result:
    result_csv = csv.writer(result)

    # Add a header to the results file.
    result_csv.writerow(
        ['Group', 'Collection_Count', 'AIP_Count', 'File_Count', 'Format_Type', 'Format_Standard_Name', 'Format_Name',
         'Format_Version', 'Registry_Name', 'Registry_Key', 'Format_Note', 'Collection_List'])

    for report in os.listdir():

        # Skip if it is the results file. Should not process itself.
        if report == f'archive_formats_{today}.csv':
            continue

        # Get ARCHive group from the filename.
        regex = re.match('file_formats_(.*).txt', report)
        archive_group = regex.group(1)

        # Get data from the report.
        report_info = csv.reader(open(report, 'r'), delimiter='\t')

        # Skip the header.
        next(report_info)

        # Get data from each row in the report.
        for data in report_info:
            # Update the row to add additional information and fill in blank cells.
            # Save to the results csv.
            new_row = update_row(data, archive_group)
            result_csv.writerow(new_row)
