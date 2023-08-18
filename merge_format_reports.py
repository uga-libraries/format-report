"""Combines the ARCHive format reports, which are one CSV per group, into single CSVs for analysis.

One CSV (archive_formats_by_aip_YYYYMM.csv) is organized by AIP and then by format identification. 
It includes the ARCHive group, collection identifier, AIP identifier, and format information (format type,
format standardized name, format name, format version, registry name, registry key, and format note). 
It is used for aggregating the number of collections and AIPs.

The other CSV (archive_formats_by_group_YYYYMM.csv) is organized by group and then by format identification. 
It includes the ARCHive group, number of file_ids, and format information (format type,format standardized name,
format name, format version, registry name, registry key, and format note) 
It is used for aggregating the number of file_ids. 
The numbers are inflated by files that have more than one possible format identification.

Before running this script, run update_standardization.py
"""

# Usage: python path/merge_format_reports.py report_folder
#     - report_folder contains the ARCHive group format reports. Script output is saved to this folder as well.

import csv
import datetime
import os
import re
import sys
from update_standardization import check_argument


def collection_from_aip(aip_id, group):
    """Returns the collection id. The collection id is extracted from the AIP id based on each group's rules for
    constructing AIP ids, all of which include the collection id. If the pattern does not match any known rules,
    the function raises a ValueError."""

    # Brown Media Archives and Peabody Awards Collection
    if group == "bmac":

        try:
            if aip_id[5].isdigit():
                return "peabody"

            # The next three address errors with how the AIP ID was made.
            elif aip_id.startswith("har-ms"):
                coll_regex = re.match("(^har-ms[0-9]+)_", aip_id)
                return coll_regex.group(1)

            elif aip_id.startswith("bmac_bmac_wsbn"):
                return "wsbn"

            elif aip_id.startswith("bmac_wrdw_"):
                return "wrdw-video"

            # AIPs for this collection can start bmac_walb or bmac_walb-video
            elif aip_id.startswith("bmac_walb"):
                return "walb"

            else:
                coll_regex = re.match("^bmac_([a-z0-9-]+)_", aip_id)
                return coll_regex.group(1)

        except AttributeError:
            raise AttributeError

    # Digital Library of Georgia
    elif group == "dlg":

        try:
            # Everything in turningpoint is also in another collection, which is the one we want.
            # The collection number is changed to an integer to remove leading zeros.
            if aip_id.startswith("dlg_turningpoint"):

                # This one is from an error in the AIP ID.
                if aip_id == "dlg_turningpoint_ahc0062f-001":
                    return "geh_ahc-mss820f"

                elif aip_id.startswith("dlg_turningpoint_ahc"):
                    coll_regex = re.match("dlg_turningpoint_ahc([0-9]{4})([a-z]?)-", aip_id)
                    if coll_regex.group(2) == "v":
                        return f"geh_ahc-vis{int(coll_regex.group(1))}"
                    else:
                        return f"geh_ahc-mss{int(coll_regex.group(1))}{coll_regex.group(2)}"

                elif aip_id.startswith("dlg_turningpoint_ghs"):
                    coll_regex = re.match("dlg_turningpoint_ghs([0-9]{4})([a-z]*)", aip_id)
                    if coll_regex.group(2) == "bs":
                        return f"g-hi_ms{coll_regex.group(1)}-bs"
                    else:
                        return f"g-hi_ms{coll_regex.group(1)}"

                elif aip_id.startswith("dlg_turningpoint_harg"):
                    coll_regex = re.match("dlg_turningpoint_harg([0-9]{4})([a-z]?)", aip_id)

                    return f"guan_ms{int(coll_regex.group(1))}{coll_regex.group(2)}"

                else:
                    raise AttributeError

            # Georgia Historic Newspapers. Have seen batch_gua_ and batch_gu_
            elif aip_id.startswith("batch_gu"):
                return "dlg_ghn"

            else:
                coll_regex = re.match("^([a-z0-9-]*_[a-z0-9-]*)_", aip_id)
                return coll_regex.group(1)

        except AttributeError:
            raise AttributeError

    # Digital Library of Georgia managing content for Hargrett Rare Book and Manuscript Library
    elif group == "dlg-hargrett":
        try:
            coll_regex = re.match("^([a-z]{3,4}_[a-z0-9]{4})_", aip_id)
            return coll_regex.group(1)
        except AttributeError:
            raise AttributeError

    # Digital Library of Georgia managing content for Map and Government Information Library
    elif group == "dlg-magil":
        try:
            coll_regex = re.match("^([a-z]+_[a-z]+)_", aip_id)
            return coll_regex.group(1)
        except AttributeError:
            raise AttributeError

    # Hargrett Rare Book and Manuscript Library
    elif group == "hargrett":
        try:
            # Oral histories
            if aip_id.startswith("har-"):
                coll_regex = re.match("^(har-ua[0-9]{2}-[0-9]{3})_", aip_id)
                return coll_regex.group(1)

            # All other identifiers
            else:
                coll_regex = re.match("^(.*)(er|-web)", aip_id)
                return coll_regex.group(1)

        except AttributeError:
            raise AttributeError

    # Richard B. Russell Library for Research and Studies.
    # The same collection can be formatted rbrl-### or rbrl###, so normalizing all IDs to rbrl### to avoid duplicates.
    elif group == "russell":
        try:
            coll_regex = re.match("^rbrl-?([0-9]{3})", aip_id)
            coll_id = f"rbrl{coll_regex.group(1)}"
            return coll_id
        except AttributeError:
            raise AttributeError

    # This would catch a new group.
    else:
        raise ValueError


def read_report(report_path):
    """
    Gets data from each ARCHive group format report and calculates additional information based on that data.
    Returns two lists with the rows of data to save to the CSV files.
    """
    # Makes lists to store the rows of data to save to the CSV files.
    aip_csv_rows = []
    group_csv_rows = []

    # Gets the ARCHive group from the format report filename.
    regex = re.match(".*file_formats_(.*).csv", report_path)
    archive_group = regex.group(1)

    with open(report_path, "r") as open_report:
        report_info = csv.reader(open_report)

        # Skips the header.
        next(report_info)

        # Gets the data from each row in the report.
        for row in report_info:
            aip_row_list, group_row = read_row(row, archive_group)

            # Adds the data to the reports.
            # group_row is a list; aip_row_list is a list of lists, although it may only contain one list.
            aip_csv_rows.extend(aip_row_list)
            group_csv_rows.append(group_row)

    # Returns both lists of rows to be saved to the correct CSVs.
    return aip_csv_rows, group_csv_rows


def read_row(row_data, archive_group):
    """
    Gets data from a row from an ARCHive format report and calculates additional information based on that data.
    Returns two lists to be added to group_csv_rows and aip_csv_rows.
    """
    # Replaces any blank cells with "NO VALUE" to make it more clear when there is no data.
    row = ["NO VALUE" if x == "" else x for x in row_data]

    # Gets the format standardized name and format type for the format. Will be saved to both CSVs.
    format_standard, format_type = standardize_format(row[3])

    # Calculates the format identification: name|version|registry_key. Will be saved to both CSVs.
    format_id = f"{row[3]}|{row[4]}|{row[6]}"

    # Adds the row for the "by group" csv to the list.
    # It includes the group, file_id count, and format information.
    group_row = [archive_group, row[1], row[2], format_type, format_standard, format_id] + row[3:8]

    # Gets a list of AIPs in this row, calculates the row information for each AIP,
    # and adds the row for the "by aip" csv to the list.
    # It includes the group, collection id, aip id, and format information.
    aip_rows = []
    aip_list = row[8].split("|")
    for aip in aip_list:
        # If the collection id could not be calculated, supplies a value for the id and prints a warning.
        try:
            collection_id = collection_from_aip(aip, archive_group)
        except (ValueError, AttributeError):
            print("Could not calculate collection id for", aip)
            collection_id = "UNABLE TO CALCULATE"
        aip_rows.append([archive_group, collection_id, aip, format_type, format_standard, format_id] + row[3:8])

    return aip_rows, group_row


def save_to_csv(csv_path, rows):
    """
    Saves rows to the specified CSV.
    If rows indicates a header, uses the header information stored in this function.
    """

    # Headers for the two different CSVs created by this script.
    aip_header = ["Group", "Collection", "AIP", "Format Type", "Format Standardized Name",
                  "Format Identification", "Format Name", "Format Version", "Registry Name",
                  "Registry Key", "Format Note"]
    group_header = ["Group", "File_IDs", "Size (GB)", "Format Type", "Format Standardized Name",
                    "Format Identification", "Format Name", "Format Version", "Registry Name",
                    "Registry Key", "Format Note"]

    # If rows is "group_csv_header" or "aip_csv_header", saves the correct header to the CSV.
    # Otherwise, saves the rows to the CSV.
    with open(csv_path, "a", newline="") as csv_open:
        csv_write = csv.writer(csv_open)
        if rows == "aip_csv_header":
            csv_write.writerow(aip_header)
        elif rows == "group_csv_header":
            csv_write.writerow(group_header)
        else:
            csv_write.writerows(rows)


def standardize_format(format_name):
    """
    Finds the format name within standardize_formats.csv
    and returns the standard (simplified) format name and the format type from the CSV for that format.
    These values reduce the data variability so the summaries are more useful.
    If there is no match, exits the script.
    """
    # Checks if the format name is actually an error and if so, returns default value for name and type.
    if format_name.startswith("ERROR: cannot read"):
        return "IDENTIFICATION ERROR", "IDENTIFICATION ERROR"

    # Path to standardize_formats.csv, which is in the script repo.
    standardize_formats_csv = os.path.join(sys.path[1], "standardize_formats.csv")

    # Reads standardize_formats.csv and compares the format to every format in the CSV.
    # When there is a match (case insensitive), returns the format standardized name and type.
    with open(standardize_formats_csv) as standard_list:
        read_standard_list = csv.reader(standard_list)
        for standard_row in read_standard_list:
            if format_name.lower() == standard_row[0].lower():
                return standard_row[1], standard_row[2]

        # If there was no match (meaning the previous code block did not return a result so the function keeps
        # running), prints an error message and quits the script.
        print(f'Could not match the format name "{format_name}" in standardize_formats.csv.')
        print("Update that CSV using update_standardization.py and run this script again.")
        sys.exit()


if __name__ == '__main__':

    # Verifies the required argument is present and the path is valid.
    # If there was an error, prints the error and exits the script.
    report_folder, error_message = check_argument(sys.argv)
    if error_message:
        print(error_message)
        print("Script usage: python path/merge_format_reports.py report_folder")
        sys.exit(1)

    # Increases the size of CSV fields to handle long AIP lists.
    # Gets the maximum size that doesn't give an overflow error.
    while True:
        try:
            csv.field_size_limit(sys.maxsize)
            break
        except OverflowError:
            sys.maxsize = int(sys.maxsize / 10)

    # Makes the paths for the two CSVs files for the script output, in the reports folder.
    today = datetime.datetime.now().strftime("%Y-%m")
    aip_csv = os.path.join(report_folder, f"archive_formats_by_aip_{today}.csv")
    group_csv = os.path.join(report_folder, f"archive_formats_by_group_{today}.csv")

    # Adds headers to the CSVs.
    save_to_csv(aip_csv, "aip_csv_header")
    save_to_csv(group_csv, "group_csv_header")

    # Gets data from each ARCHive group format report and calculates additional information based on that data.
    # The information is saved to one or both CSV files.
    for report in os.listdir(report_folder):

        # Skips the file if it is not a format report.
        # The usage report and potentially other files are in this folder.
        if not report.startswith("file_formats"):
            continue

        # Gets the a list of rows from the report to add to the CSVs.
        aip_report_list, group_report_list = read_report(os.path.join(report_folder, report))

        # Saves the rows to the CSVs.
        save_to_csv(aip_csv, aip_report_list)
        save_to_csv(group_csv, group_report_list)

