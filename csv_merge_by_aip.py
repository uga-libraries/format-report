# This is an experiment. What if the merged CSV was organized by AIP instead of by format?
# Would that make for easier analysis and seeing where duplicates are?
# Would it let me switch to pandas for subtotals for everything?

import csv
import os
import re
import sys

# TODO: importing not working - runs the csv_merge.py argument tests. Copied in this doc for now.
# from csv_merge import collection_from_aip


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
        coll_regex = re.match('^(.*)(er|-web)', aip)
        return coll_regex.group(1)

    # Richard B. Russell Library for Research and Studies.
    elif group == 'russell':
        coll_regex = re.match('^rbrl-?[0-9]{3}', aip)
        return coll_regex.group()


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
