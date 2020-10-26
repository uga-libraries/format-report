"""Combines the format reports (csv files) for all groups from the UGA Libraries' digital preservation
system (ARCHive) into a single csv for analysis. All data is copied from the format reports except the AIP list,
which is converted into a collection list. Columns are also added for the group name, collection count, format type,
and standardized format name.

Future development ideas: restructure the functions (they pass a lot of information to each other); add a test to
compare the original format reports to the merged one to verify script accuracy."""

# Usage: python /path/csv_merge.py /path/reports [/path/standard_csv]

import csv
import datetime
import os
import re
import sys

# Makes the report folder (script argument) the current directory. Displays an error message and quits the script if
# the argument is missing or not a valid directory.
try:
    report_folder = sys.argv[1]
    os.chdir(report_folder)
except (IndexError, FileNotFoundError):
    print("The report folder path was either not given or is not a valid directory. Please try the script again.")
    print("Script usage: python /path/csv_merge.py /path/reports [/path/standardize_formats.csv]")
    exit()

# Makes a variable with the file path for the standardize formats CSV. Uses the optional script argument if provided,
# or else uses the folder with this script as the default location.
try:
    standard_csv = sys.argv[2]
except IndexError:
    standard_csv = os.path.join(sys.path[0], 'standardize_formats.csv')


def collection_from_aip(aip, group):
    """Returns the collection id. The collection id is extracted from the AIP id based on the various rules each
    group has for constructing AIP ids for different collections. If the pattern does not match any known rules,
    the function returns None and the error is caught where the function is called. This function is imported into
    archive_capacity.py too."""

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
    elif group == 'dlg':

        # Everything in turningpoint is also in another collection, which is the one we want.
        # The collection number is made into an integer to remove leading zeros.
        if aip.startswith('dlg_turningpoint'):

            # This one is from an error in the AIP ID.
            if aip == 'dlg_turningpoint_ahc0062f-001':
                return 'geh_ahc-mss820f'

            elif aip.startswith('dlg_turningpoint_ahc'):
                coll_regex = re.match('dlg_turningpoint_ahc([0-9]{4})([a-z]?)-', aip)
                if coll_regex.group(2) == 'v':
                    return f'geh_ahc-vis{int(coll_regex.group(1))}'
                else:
                    return f'geh_ahc-mss{int(coll_regex.group(1))}{coll_regex.group(2)}'

            elif aip.startswith('dlg_turningpoint_ghs'):
                coll_regex = re.match('dlg_turningpoint_ghs([0-9]{4})([a-z]*)', aip)
                if coll_regex.group(2) == 'bs':
                    return f'g-hi_ms{coll_regex.group(1)}-bs'
                else:
                    return f'g-hi_ms{coll_regex.group(1)}'

            elif aip.startswith('dlg_turningpoint_harg'):
                coll_regex = re.match('dlg_turningpoint_harg([0-9]{4})([a-z]?)', aip)

                return f'guan_ms{int(coll_regex.group(1))}{coll_regex.group(2)}'

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
    elif group == 'dlg-magil':
        return None

    # Hargrett Rare Book and Manuscript Library
    elif group == 'hargrett':
        coll_regex = re.match('^(.*)(er|web)', aip)
        return coll_regex.group(1)

    # Richard B. Russell Library for Research and Studies.
    elif group == 'russell':
        coll_regex = re.match('^rbrl-?[0-9]{3}', aip)
        return coll_regex.group()


def collection_list(aips, group):
    """Changes AIP list to a unique list of collections.
       Returns a string with comma-separated collection ids and a count of the number of collections."""

    # Splits the aip_list (a string) into a list. Items are divided by a pipe.
    aip_list = aips.split('|')
    collections_list = []

    # Extracts the collection id from the AIP ID using another function. Prints an error message and includes the
    # error message in the collections list if the pattern is new, resulting in an error from the regular expression.
    for aip in aip_list:
        try:
            collection = collection_from_aip(aip, group)
        except AttributeError:
            print('Check for collection errors in merged csv')
            collection = f"Collection not calculated for {aip}"

        # If the AIP didn't match any known conditions, it returns None when collection_from_aip() is calculated.
        # Prints an error message and includes the error message in the collections list.
        if collection is None:
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

        # If there was no match (the previous code block did not return a result, which exits this function and keeps
        # this code block from running), prints an error message and quits the script. Run update_standardization.py to
        # make sure that standardize_formats.csv will have a match for all formats.
        print(f'Could not match the format name "{format_name}" in standardize_formats.csv.')
        print('Update that CSV and run this script again.')
        print('Note that the archive_formats CSV produced by the script only has formats up until this point.')
        exit()


def update_row(row, group):
    """Calculates and adds new data, replaces the AIP list with a collection list, and fills in empty cells.
       New data is group name, collection count, standardized version of the format name, and format type."""

    # Gets the standard name for the format and the format type.
    format_standard, format_type = standardize_formats(row[2], standard_csv)

    # Gets a list of collection ids from the AIP ids and the number of collections.
    collections, number_collections = collection_list(row[7], group)

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
        ['Group', 'Collection_Count', 'AIP_Count', 'File_Count', 'Format_Type', 'Format_Standardized_Name',
         'Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'Format_Note', 'Collection_List'])

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
                new_row = update_row(data, archive_group)
                result_csv.writerow(new_row)
