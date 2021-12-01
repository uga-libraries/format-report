"""Combines the ARCHive format reports, which are one CSV per group, into single CSVs for analysis.

One CSV (archive_formats_YYYYMM.csv) has the information organized by group and then by format identification. It
includes the ARCHive group, number of file_ids, and format information (format type,format standardized name,
format name, format version, registry name, registry key, and format note) It is used for aggregating the number of
file_ids. The numbers are inflated by files that have more than one possible format identification.

The other CSV (archive_formats_by_aip_YYYYMM.csv) has the information organized by AIP and then by unique format. It
includes the ARCHive group, collection identifier, AIP identifier, and format information (format type,
format standardized name, format name, format version, registry name, registry key, and format note). It is used for
aggregating the number of collections and AIPs.

Before running this script, run update_standardization.py
"""

# Usage: python /path/merge_format_reports.py /path/report_folder [/path/standardize_formats.csv]
# Report folder should contain the ARCHive group format reports. Script output is saved to this folder as well.
# A default value for the path to the standardize formats csv is used if one is not provided as an argument.

import csv
import datetime
import os
import re
import sys


def standardize_formats(format_name, standard):
    """Finds the format name within the standardize formats csv and returns the standard (simplified) format
    name and the format type. These values reduce the data variability so summaries are more useful."""

    # Reads the standardize formats csv.
    with open(standard) as standard_list:
        read_standard_list = csv.reader(standard_list)

        # Skips the header.
        next(read_standard_list)

        # Checks if the format name is actually an error and if so, returns default value for name and type.
        if format_name.startswith("ERROR: cannot read"):
            return "IDENTIFICATION ERROR", "IDENTIFICATION ERROR"

        # Checks each row in the standardized formats csv for the format.
        # When there is a match, returns the format standardized name and format type.
        # Matches lowercase versions of the format names to ignore variations in capitalization.
        for standard_row in read_standard_list:
            if format_name.lower() == standard_row[0].lower():
                return standard_row[1], standard_row[2]

        # If there was no match (meaning the previous code block did not return a result so the function keeps
        # running), prints an error message and quits the script.
        print(f'Could not match the format name "{format_name}" in standardize_formats.csv.')
        print("Update that CSV using update_standardization.py and run this script again.")
        exit()


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

            elif aip_id.startswith("batch_gua_"):
                return "dlg_ghn"

            else:
                coll_regex = re.match("^([a-z0-9-]*_[a-z0-9-]*)_", aip_id)
                return coll_regex.group(1)

        except AttributeError:
            raise AttributeError

    # Digital Library of Georgia managing content for Hargrett Rare Book and Manuscript Library
    elif group == "dlg-hargrett":
        coll_regex = re.match("^([a-z]{3,4}_[a-z0-9]{4})_", aip_id)
        return coll_regex.group(1)

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


# Makes the report folder (a script argument) the current directory. If the argument is missing or not a valid
# directory, displays an error message and quits the script.
try:
    report_folder = sys.argv[1]
    os.chdir(report_folder)
except (IndexError, FileNotFoundError):
    print("The report folder path was either not given or is not a valid directory. Please try the script again.")
    print("Script usage: python /path/merge_format_reports.py /path/format_reports [/path/standardize_formats.csv]")
    exit()

# Makes a variable with the file path for the standardize formats csv. Uses the optional script argument if provided,
# or else uses the parent folder of the folder with this script as the default location for that CSV.
try:
    standard_csv = sys.argv[2]
except IndexError:
    standard_csv = os.path.join(os.path.dirname(sys.path[0]), "standardize_formats.csv")

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

# Makes two CSV files in the reports folder for script output.
# archive_formats_YYYYMM.csv is organized by format identification and then by group.
# archive_formats_by_aip.YYYYMM.csv is organized by AIP and then format identification.
with open(f"archive_formats_{today}.csv", "w", newline="") as by_format, open(f"archive_formats_by_aip_{today}.csv",
                                                                              "w", newline="") as by_aip:
    by_format_csv = csv.writer(by_format)
    by_aip_csv = csv.writer(by_aip)

    # Adds a header to each CSV.
    by_format_csv.writerow(["Group", "File_IDs", "Size (GB)", "Format Type", "Format Standardized Name",
                            "Format Identification", "Format Name", "Format Version", "Registry Name", "Registry Key",
                            "Format Note"])

    by_aip_csv.writerow(["Group", "Collection", "AIP", "Format Type", "Format Standardized Name",
                         "Format Identification", "Format Name", "Format Version", "Registry Name", "Registry Key",
                         "Format Note"])

    # Gets data from each ARCHive group format report and calculates additional information based on that data.
    # The information is saved to one or both CSV files.
    for report in os.listdir():

        # Skips the file if it is not a format report. The usage report and potentially other files are in this folder.
        if not report.startswith("file_formats"):
            continue

        # Gets the ARCHive group from the format report filename. Will be saved to both CSVs.
        regex = re.match("file_formats_(.*).csv", report)
        archive_group = regex.group(1)

        # Gets the data from the report.
        with open(report, "r") as open_report:
            report_info = csv.reader(open_report)

            # Skips the header.
            next(report_info)

            # Gets the data from each row in the report.
            for row in report_info:

                # Replaces any blank cells with "NO VALUE" to make it more clear when there is no data.
                row = ["NO VALUE" if x == "" else x for x in row]

                # Gets the format standardized name and format type for the format. Will be saved to both CSVs.
                format_standard, format_type = standardize_formats(row[3], standard_csv)

                # Calculates the format identification: name|version|registry_key. Will be saved to both CSVs.
                format_id = f"{row[3]}|{row[4]}|{row[6]}"

                # Writes the group, file_id count, and format information to the "by format" csv.
                by_format_csv.writerow([archive_group, row[1], row[2], format_type, format_standard, format_id,
                                        row[3], row[4], row[5], row[6], row[7]])

                # Gets a list of AIPs in this row, calculates the row information for each AIP, and saves the AIP
                # rows to the "by aip" csv.
                aip_list = row[8].split("|")
                for aip in aip_list:
                    # If the collection id could not be calculated, supplies a value for the id and prints a warning.
                    try:
                        collection_id = collection_from_aip(aip, archive_group)
                    except (ValueError, AttributeError):
                        print("Could not calculate collection id for", aip)
                        collection_id = "UNABLE TO CALCULATE"
                    by_aip_csv.writerow([archive_group, collection_id, aip, format_type, format_standard, format_id,
                                         row[3], row[4], row[5], row[6], row[7]])
