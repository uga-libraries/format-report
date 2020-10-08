"""Combines the format reports (tab delimited text files) for all groups from the UGA Libraries' digital preservation
system (ARCHive) into a single csv for analysis. All data is copied from the format reports except the AIP list,
which is converted into a collection list. Columns are also added for the group name, collection count, format type,
and standardized format name.

Usage: python /path/csv_merge.py /path/report_folder /path/standard_csv"""

import csv
import datetime
import os
import re
import sys

# Makes variables from script arguments:
#    - report_folder is the directory with the ARCHive format reports to be merged.
#    - standardize_csv is the path to the csv document with current standardization rules.
# TODO: add error handling
# TODO: standard_csv is in the same folder as the script. Can it reference the csv without a path?
report_folder = sys.argv[1]
standard_csv = sys.argv[2]

# Makes the report folder the current directory.
os.chdir(report_folder)


def collection_from_aip(aip, group):
    """Returns the collection id. The collection id is extracted from the AIP id based on the various rules each group
    has for constructing AIP ids for different collections. """

    # Brown Media Archives and Peabody Awards Collection
    if group == 'bmac':

        if aip[5].isdigit():
            return 'peabody'

        # The next three address errors with how AIP ID was made.
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

    # Digital Library of Georgia
    # TODO: verify if need the number = int() step, and if so does it need to be a separate variable?
    elif group == 'dlg':

        # Everything in turningpoint is also in another collection, which is the one we want.
        if aip.startswith('dlg_turningpoint'):

            # This one is from an error in the AIP ID.
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

            # Warning in output that pattern-matching of this function needs to be updated.
            else:
                return 'turningpoint no match'

        elif aip.startswith('batch_gua_'):
            return 'dlg_ghn'

        else:
            coll_regex = re.match('^([a-z0-9-]*_[a-z0-9-]*)_', aip)
            return coll_regex.group(1)

    # Digital Library of Georgia: Hargrett Rare Book and Manuscript Library
    elif group == 'dlg-hargrett':
        coll_regex = re.match('^([a-z]{3,4}_[a-z0-9]{4})_', aip)
        return coll_regex.group(1)

    # NOTE: At the time of writing this script, there were no AIPs in dlg-magil. This will need to be updated.
    # TODO: add a no match return to remind me to update

    # Hargrett Rare Book and Manuscript Library
    elif group == 'hargrett':
        coll_regex = re.match('^(.*)er', aip)
        return coll_regex.group(1)

    # Richard B. Russell Library for Research and Studies.
    elif group == 'russell':
        coll_regex = re.match('^rbrl-?[0-9]{3}', aip)
        return coll_regex.group()

    # Warning in output that pattern-matching of this function needs to be updated.
    else:
        return 'new group'


def update_row(row, group):
    """Calculates and adds new data, replaces the AIP list with a collection list, and fills in empty cells.
       New data is group name, collection count, standardized version of the format name, and format type."""

    def collection_list(aip_list):
        """Changes AIP list to a unique list of collections.
           Returns a string with comma-separated collection ids and a count of the number of collections."""

        # Splits the aip_list (a string) into a list. Items are divided by a pipe.
        # TODO: clarify this. Don't use list as part of the name if it isn't type list. Is aips a Python list?
        aips = aip_list.split('|')

        collections_list = []

        # Extracts the collection id from the AIP ID using another function.
        # Prints an error message and includes the error message in the collections list if the pattern is new.
        # TODO: why is collection_from_aip() its own function with collection_list() and standardize_formats() are within update_row()?
        for aip in aips:
            try:
                collection = collection_from_aip(aip, group)
            except AttributeError:
                print('Check for collection errors in merged csv')
                collection = f"Collection not calculated for {aip}"

            # Makes a unique list of collection ids.
            if collection not in collections_list:
                collections_list.append(collection)

        # Converts the list of collection ids to a string with each collection id separated by a comma.
        collections_string = ', '.join(map(str, collections_list))

        # Returns both the string with the collection ids and a count of the number of collections.
        return collections_string, len(collections_list)

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

    # Gets the standard name for the format and the format type. If there is no match, prints an error message and
    # quits the script. Use update_standardization.py to make sure that standardize_formats.csv will have a match for
    # all formats.
    try:
        format_standard, format_type = standardize_formats(row[2], standard_csv)
    except TypeError:
        print(f'Could not match {row[2]} in standardize_formats.csv. Update CSV and run this script again.')
        exit()

    # Gets a list of collection ids from the AIP ids and the number of collections.
    collections, number_collections = collection_list(row[7])

    # Replaces the AIP list with the collection list.
    row[7] = collections

    # Adds the group and number of collections at the beginning of the row.
    # Adds the format type and standardized format name before the format name.
    row.insert(0, group)
    row.insert(1, number_collections)
    row.insert(4, format_type)
    row.insert(5, format_standard)

    # Fills all empty cells with 'NO VALUE' so it is easier to see where there is no data.
    row = ['NO VALUE' if x == '' else x for x in row]

    # Returns the updated version of the row.
    return row


# Increases the size of csv fields to handle long aip lists.
# Gets the maximum size that doesn't give an overflow error.
while True:
    try:
        csv.field_size_limit(sys.maxsize)
        break
    except OverflowError:
        sys.maxsize = int(sys.maxsize / 10)

# Gets the current date, formatted YYYYMM, to use in naming the merged file.
today = datetime.datetime.now().strftime("%Y-%m")

# Makes a CSV file for the merged reports named archive_formats_date.csv in the same folder as the ARCHive reports.
# Gets each row from each group's format report, updates the row, and saves the updated row to the CSV.
with open(f'archive_formats_{today}.csv', 'w', newline='') as result:
    result_csv = csv.writer(result)

    # Adds a header to the results file.
    result_csv.writerow(
        ['Group', 'Collection_Count', 'AIP_Count', 'File_Count', 'Format_Type', 'Format_Standard_Name', 'Format_Name',
         'Format_Version', 'Registry_Name', 'Registry_Key', 'Format_Note', 'Collection_List'])

    for report in os.listdir():

        # Skips the file if it is the results file. Should not process itself.
        if report == f'archive_formats_{today}.csv':
            continue

        # Gets the ARCHive group from the format report filename.
        regex = re.match('file_formats_(.*).txt', report)
        archive_group = regex.group(1)

        # Gets the data from the report.
        report_info = csv.reader(open(report, 'r'), delimiter='\t')

        # Skips the header.
        next(report_info)

        # Gets the data from each row in the report.
        for data in report_info:
            # Updates the row to add additional information and fill in blank cells using another function and saves
            # the updated row to the CSV.
            new_row = update_row(data, archive_group)
            result_csv.writerow(new_row)
