"""Combines the ARCHive format archive_reports, which are one CSV per group, into single CSVs for analysis.

Parameters:
    report_folder : the path to the folder which contains ARCHive's group file format reports and usage report (all CSVs)
    nara_csv : the path to NARA's Digital Preservation Plan spreadsheet (CSV)

Returns:

    archive_formats_by_aip_YYYYMM.csv: organized by AIP and then by format identification.
    It includes the ARCHive group, collection identifier, AIP identifier, and format information (format type,
    format standardized name, format name, format version, registry name, registry key, and format note).
    It is used for aggregating the number of collections and AIPs.

    archive_formats_by_group_YYYYMM.csv: organized by group and then by format identification.
    It includes the ARCHive group, number of file_ids, and format information (format type,format standardized name,
    format name, format version, registry name, registry key, and format note)
    It is used for aggregating the number of file_ids.
    The numbers are inflated by files that have more than one possible format identification.
"""

import csv
import datetime
import numpy as np
import os
import pandas as pd
import re
import sys


def add_nara_risk(format_csv_path, nara_csv_path):
    """Add NARA risk information to one of the combined format reports

    Information included:
    - NARA Risk Level
    - NARA Proposed Preservation Plan
    - NARA format information (name and PUID), so that the accuracy of the match can be evaluated
    - The technique that produced the match (NARA_Match_Type), so the effective of match types can be evaluated.

    Parameters:
        format_csv_path : the path to one of the combined format reports made earlier in the script
        nara_csv_path : the path to NARA's Digital Preservation Plan spreadsheet

    Returns: none
    """

    # Reads the format CSV into a dataframe, ignoring encoding errors.
    df_format = csv_to_dataframe(format_csv_path)

    # Reads the NARA CSV into a dataframe, ignoring encoding errors.
    df_nara = csv_to_dataframe(nara_csv_path)

    # Adds NARA risk columns to the format dataframe.
    df_risk = match_nara_risk(df_format, df_nara)

    # Saves the format dataframe with NARA risk columns to the format CSV.
    # This replaces the information that was in the format CSV.
    df_risk.to_csv(format_csv_path, index=False)


def collection_from_aip(aip_id, group):
    """Determine the collection identifier based on groups' rules for constructing AIP identifiers

    Parameters:
        aip_id : AIP identifier, which contains the collection identifier (string)
        group : ARCHive group code, since each group has different rules for construction AIP identifiers (string)

    Returns:
        collection id : collection identifier (string), if calculated, or raises an error
    """

    # Brown Media Archives and Peabody Awards Collection
    if group == "bmac":

        try:
            if aip_id[5].isdigit():
                return "peabody"

            # The next four address errors with how the AIP ID was made.
            elif aip_id.startswith("har-ms"):
                coll_regex = re.match("(^har-ms[0-9]+)_", aip_id)
                return coll_regex.group(1)

            elif aip_id.startswith("bmac_bmac_wsbn"):
                return "wsbn"

            elif aip_id.startswith("bmac_wrdw_"):
                return "wrdw-video"

            elif aip_id.startswith("bmac_wsbn3"):
                return "wsbn"

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

            # Collection with dash as the delimiter instead of underscore.
            elif aip_id.startswith("ugalaw_lspc"):
                return "ugalaw_lspc"

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

            # College of Agriculture photographs
            elif aip_id.startswith("guan_caes_0004"):
                return "ua19-010"

            # All other identifiers
            else:
                coll_regex = re.match("^(.*)(er|-web)", aip_id)
                return coll_regex.group(1)

        except AttributeError:
            raise AttributeError

    # Map and Government Information Library
    # There is currently only one pattern of AIP ID, which has no related collection.
    # Testing if the AIP ID matches the pattern to catch any new patterns.
    elif group == "magil":
        if re.match("^magil-ggp-[0-9]{7}-[0-9]{4}-[0-9]{2}", aip_id):
            return "no-coll"
        else:
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


def check_arguments(argument_list):
    """Check the required arguments report_folder and nara_csv are present and correct

    Parameters:
        argument_list : list from sys.argv with the script parameters

    Returns:
        report_path : the path to the folder which contains ARCHive's group file format reports and usage report, or None
        nara_path : the path to NARA's Digital Preservation Plan spreadsheet, or None
        errors : the list of errors encountered, if any, or an empty list
    """

    # Makes variables with default values to store the results of the function.
    report_path = None
    nara_path = None
    errors = []

    # Verifies that the first required argument (report_folder) is present,
    # and if it is present that it is a valid directory.
    if len(argument_list) > 1:
        report_path = argument_list[1]
        if not os.path.exists(report_path):
            errors.append(f"Report folder '{report_path}' does not exist")
    else:
        errors.append("Required argument report_folder is missing")

    # Verifies that the second required argument (nara_csv) is present,
    # and if it is present that it is a valid directory.
    if len(argument_list) > 2:
        nara_path = argument_list[2]
        if not os.path.exists(nara_path):
            errors.append(f"NARA CSV '{nara_path}' does not exist")
    else:
        errors.append("Required argument nara_csv is missing")

    # Returns the results.
    return report_path, nara_path, errors


def csv_to_dataframe(csv_file):
    """Read a CSV file into a dataframe, dealing with special characters and renaming columns

    If special characters require the CSV to be read while ignoring encoding errors, it prints a warning.
    This function is based on https://github.com/uga-libraries/accessioning-scripts/blob/main/format_analysis_functions.py

    Parameters:
        csv_file : the path to a combined format report made earlier in this script
        or NARA's Digital Preservation PLan spreadsheet

    Returns:
        df : a dataframe with the contents of the CSV
    """

    # Reads the CSV into a dataframe, ignoring encoding errors from special characters if necessary.
    # Reads a string to allow better comparisons between dataframes.
    try:
        df = pd.read_csv(csv_file, dtype=str)
    except UnicodeDecodeError:
        print("UnicodeDecodeError when trying to read:", csv_file)
        print("The CSV was read by ignoring encoding errors, so those characters are omitted from the dataframe.")
        df = pd.read_csv(csv_file, dtype=str, encoding_errors="ignore")

    # Replaces any spaces in column names with underscores, and removes any parentheses.
    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.replace("(", "")
    df.columns = df.columns.str.replace(")", "")

    # Adds a prefix to the NARA dataframe columns that don't already start with NARA
    # so the source of the data is clear when the data is combined.
    if "NARA" in csv_file:
        df.rename(columns={"Format_Name": "NARA_Format_Name",
                           "File_Extensions": "NARA_File_Extensions",
                           "PRONOM_URL": "NARA_PRONOM_URL",
                           "Description_and_Justification": "NARA_Description_and_Justification"}, inplace=True)

    return df


def match_nara_risk(df_format, df_nara):
    """Match format identifications to NARA's Digital Preservation Plan spreadsheet

    The match techniques are applied in order of accuracy, and stop for each format when a match is found.

    This function is based on https://github.com/uga-libraries/accessioning-scripts/blob/main/format_analysis_functions.py

    Returns a dataframe with all the format data, the NARA Risk Level and Proposed Preservation Plan,
    and the name of the technique that produced the match (NARA_Match_Type).
    This is copied from
    and modified to work with ARCHive format identifications instead of FITS.

    Parameters:
        df_format : a dataframe with the information from one of the combined format reports made earlier in the script
        df_nara : a dataframe with the information from NARA's Digital Preservation Plan spreadsheet

    Returns:
        df_result : a dataframe with the format information and corresponding NARA risk information, if matched
    """

    # PART ONE: ADD TEMPORARY COLUMNS TO BOTH DATAFRAMES FOR BETTER MATCHING

    # Formats ARCHive version as a string to avoid type errors during merging.
    df_format['version_string'] = df_format['Format_Version'].astype(str)

    # Combines ARCHive format name and version, since NARA has that information in one column.
    # Removes " nan" from the combined column, which happens if there is no version.
    df_format['name_version'] = df_format['Format_Name'].str.lower() + " " + df_format['version_string']
    df_format['name_version'] = df_format['name_version'].str.replace("\sNO VALUE$", "")

    # Combines ARCHive registry name and registry key to make a PUID (PRONOM URI) that matches NARA's PUID formatting.
    # If the registry is not PRONOM (the only registry we use for NARA comparison), assigns "NO VALUE".
    df_format['puid'] = np.where(df_format['Registry_Name'] == "https://www.nationalarchives.gov.uk/PRONOM",
                                 "https://www.nationalarchives.gov.uk/pronom/" + df_format['Registry_Key'],
                                 "NO VALUE")

    # Makes ARCHive and NARA format names lowercase for case-insensitive matching.
    df_format['name_lower'] = df_format['Format_Name'].str.lower()
    df_nara['nara_format_lower'] = df_nara['NARA_Format_Name'].str.lower()

    # Makes a column with the NARA version, since ARCHive has that in a separate column.
    # The version is assumed to be anything after the last space in the format name, the most common pattern.
    # For ones that don't actually end in a version, it gets the last word, which does not interfere with matching.
    df_nara['nara_version'] = df_nara['NARA_Format_Name'].str.split(" ").str[-1]

    # List of relevant columns in the NARA dataframe.
    nara_columns = ["NARA_Format_Name", "NARA_PRONOM_URL", "NARA_Risk_Level", "NARA_Proposed_Preservation_Plan",
                    "nara_format_lower", "nara_version"]

    # For each matching technique, it makes a dataframe by merging NARA into ARCHive based on one or two columns
    # and creates two dataframes:
    #   one with files that matched (has a value in NARA_Risk Level after the merge)
    #   one with files that did not match (NARA_Risk Level is empty after the merge).
    # A column NARA_Match_Type is added to the matched dataframe with the matching technique name and
    # the entire dataframe is added to df_result, which is what the function will return.
    # The NARA columns are removed from the unmatched dataframe so they aren't duplicated in future merges.
    # The next technique is applied to just the files that are unmatched.
    # After all techniques are tried, default values are assigned to NARA columns for files that cannot be matched
    # and this is added to df_result as well.

    # PART TWO: FORMAT IDENTIFICATIONS THAT HAVE A PUID
    # If an ARCHive format id has a PUID, it should only match something in NARA with the same PUID or no PUID.

    # Makes dataframes needed for part two matches:

    # ARCHive identifications that have a PUID.
    df_format_puid = df_format[df_format['puid'] != "NO VALUE"].copy()

    # NARA identifications that do not have a PUID.
    df_nara_no_puid = df_nara[df_nara['NARA_PRONOM_URL'].isnull()]

    # Technique 1: PRONOM Identifier and Format Version are both a match.
    df_merge = pd.merge(df_format_puid, df_nara[nara_columns], left_on=['puid', 'version_string'],
                        right_on=['NARA_PRONOM_URL', 'nara_version'], how="left")
    df_result = df_merge[df_merge['NARA_Risk_Level'].notnull()].copy()
    df_result = df_result.assign(NARA_Match_Type="PRONOM and Version")
    df_unmatched = df_merge[df_merge['NARA_Risk_Level'].isnull()].copy()
    df_unmatched.drop(nara_columns, inplace=True, axis=1)

    # Technique 2: PRONOM Identifier and Format Name are both a match.
    df_merge = pd.merge(df_unmatched, df_nara[nara_columns], left_on=['puid', 'Format_Name'],
                        right_on=['NARA_PRONOM_URL', 'NARA_Format_Name'], how="left")
    df_matched = df_merge[df_merge['NARA_Risk_Level'].notnull()].copy()
    df_matched = df_matched.assign(NARA_Match_Type="PRONOM and Name")
    df_result = pd.concat([df_result, df_matched], ignore_index=True)
    df_unmatched = df_merge[df_merge['NARA_Risk_Level'].isnull()].copy()
    df_unmatched.drop(nara_columns, inplace=True, axis=1)

    # Technique 3: PRONOM Identifier is a match.
    df_merge = pd.merge(df_unmatched, df_nara[nara_columns], left_on='puid', right_on='NARA_PRONOM_URL', how="left")
    df_matched = df_merge[df_merge['NARA_Risk_Level'].notnull()].copy()
    df_matched = df_matched.assign(NARA_Match_Type="PRONOM")
    df_result = pd.concat([df_result, df_matched], ignore_index=True)
    df_unmatched = df_merge[df_merge['NARA_Risk_Level'].isnull()].copy()
    df_unmatched.drop(nara_columns, inplace=True, axis=1)

    # Technique 4: Format Name, and Format Version if it has one, are both a match.
    # This only works if the NARA Format Name is structured name[SPACE]version.
    df_merge = pd.merge(df_unmatched, df_nara_no_puid[nara_columns], left_on='name_version',
                        right_on='nara_format_lower', how="left")
    df_matched = df_merge[df_merge['NARA_Risk_Level'].notnull()].copy()
    df_matched = df_matched.assign(NARA_Match_Type="Format Name")
    df_result = pd.concat([df_result, df_matched], ignore_index=True)
    df_unmatched = df_merge[df_merge['NARA_Risk_Level'].isnull()].copy()
    df_unmatched.drop(nara_columns, inplace=True, axis=1)

    # Adds default text for risk and match type for any that are still unmatched.
    df_unmatched = df_unmatched.copy()
    df_unmatched['NARA_Format_Name'] = "No Match"
    df_unmatched['NARA_Risk_Level'] = "No Match"
    df_unmatched['NARA_Match_Type'] = "No NARA Match"
    df_result = pd.concat([df_result, df_unmatched], ignore_index=True)

    # PART THREE: FORMAT IDENTIFICATIONS THAT DO NOT HAVE A PUID
    # If an ARCHive format id has no PUID, it can match anything in NARA (has a PUID or no PUID).

    # Makes dataframes needed for part three matches:

    # FITS identifications that have no PUID.
    df_format_no_puid = df_format[df_format['puid'] == "NO VALUE"].copy()

    # Technique 4 (repeated with different format DF): Format Name, and Format Version if it has one, are both a match.
    # This only works if the NARA Format Name is structured name[SPACE]version.
    df_merge = pd.merge(df_format_no_puid, df_nara[nara_columns], left_on='name_version',
                        right_on='nara_format_lower', how="left")
    df_matched = df_merge[df_merge['NARA_Risk_Level'].notnull()].copy()
    df_matched = df_matched.assign(NARA_Match_Type="Format Name")
    df_result = pd.concat([df_result, df_matched], ignore_index=True)
    df_unmatched = df_merge[df_merge['NARA_Risk_Level'].isnull()].copy()
    df_unmatched.drop(nara_columns, inplace=True, axis=1)

    # Adds default text for risk and match type for any that are still unmatched.
    df_unmatched['NARA_Format_Name'] = "No Match"
    df_unmatched['NARA_Risk_Level'] = "No Match"
    df_unmatched['NARA_Match_Type'] = "No NARA Match"
    df_result = pd.concat([df_result, df_unmatched], ignore_index=True)

    # PART FOUR: CLEAN UP AND RETURN FINAL DATAFRAME

    # Removes the temporary columns used for better matching.
    df_result.drop(["version_string", "name_version", "name_lower", "puid", "nara_format_lower", "nara_version"],
                   inplace=True, axis=1)

    return df_result


def read_report(report_path):
    """Transform the data from an ARCHive group file format report into two lists

    Parameters:
        report_path : the path to the ARCHive group file format report

    Returns:
        aip_csv_rows : a list of lists, where each list is a row for the "by_aip" CSV
        group_csv_rows : a list of lists, where each list is a row for the "by_group" CSV
    """

    # Makes lists to store the rows of data to save to the CSV files.
    aip_csv_rows = []
    group_csv_rows = []

    # Gets the ARCHive group from the format report filename.
    regex = re.match(".*file_formats_(.*).csv", report_path)
    archive_group = regex.group(1)

    with open(report_path, "r", encoding="utf-8") as open_report:
        report_info = csv.reader(open_report)

        # Skips the header.
        next(report_info)

        # Gets the data from each row in the report.
        for row in report_info:
            aip_row_list, group_row = read_row(row, archive_group)

            # Adds the data to the archive_reports.
            # group_row is a list; aip_row_list is a list of lists, although it may only contain one list.
            aip_csv_rows.extend(aip_row_list)
            group_csv_rows.append(group_row)

    # Returns both lists of rows to be saved to the correct CSVs.
    return aip_csv_rows, group_csv_rows


def read_row(row_data, archive_group):
    """Transform the data for one format in an ARCHive group file format report into two lists

    In addition to putting the data in the desired order, it replaces blank cells with "NO VALUE",
    adds the format standardized name, format type, and format id,
    and for AIPs copies the data into a list for each separate AIP.

    Parameters:
        row_data : data from one row of an ARCHive group file format report, from reading with the csv library
        archive_group : ARCHive code for the group (string)

    Returns:
        aip_rows : a list of lists, where each list has the data for each AIP that contains the format
        group_row : a list with data for the format
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
    """Save rows to a specified CSV

    If the value of rows indicates a header, it uses the header information stored in this function.

    Parameters:
        csv_path : the path to the combined format report CSV
        rows : a list of lists with format data, or strings to indicate which header to add

    Returns: none
    """

    # Headers for the two different CSVs created by this script.
    aip_header = ["Group", "Collection", "AIP", "Format_Type", "Format_Standardized_Name",
                  "Format_Identification", "Format_Name", "Format_Version", "Registry_Name",
                  "Registry_Key", "Format_Note"]
    group_header = ["Group", "File_IDs", "Size_GB", "Format_Type", "Format_Standardized_Name",
                    "Format_Identification", "Format_Name", "Format_Version", "Registry_Name",
                    "Registry_Key", "Format_Note"]

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
    """Find the standardized format name and format type for a format in standardize_formats.csv

    These values reduce the data variability so the summaries are more useful.
    If there is no match, exits the script.

    Parameters:
        format_name : the name of a format (string)

    Returns:
        format standardized name : the standardized name of a format (string)
        format type : the type of a format (string)
    """

    # Checks if the format name is actually an error and if so, returns default value for name and type.
    if format_name.startswith("ERROR: cannot read"):
        return "IDENTIFICATION ERROR", "IDENTIFICATION ERROR"

    # Path to standardize_formats.csv, which is in the script repo.
    standardize_formats_csv = os.path.join(sys.path[1], "standardize_formats.csv")

    # Reads standardize_formats.csv and compares the format to every format in the CSV.
    # When there is a match (case-insensitive), returns the format standardized name and type.
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
    report_folder, nara_csv, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        print("Script usage: python path/merge_format_reports.py report_folder nara_csv")
        sys.exit(1)

    # Increases the size of CSV fields to handle long AIP lists.
    # Gets the maximum size that doesn't give an overflow error.
    while True:
        try:
            csv.field_size_limit(sys.maxsize)
            break
        except OverflowError:
            sys.maxsize = int(sys.maxsize / 10)

    # Makes the paths for the two CSVs files for the script output, in the archive_reports folder.
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

        # Gets a list of rows from the report to add to the CSVs.
        aip_report_list, group_report_list = read_report(os.path.join(report_folder, report))

        # Saves the rows to the CSVs.
        save_to_csv(aip_csv, aip_report_list)
        save_to_csv(group_csv, group_report_list)

    # Adds risk information from the NARA Preservation Action Plans CSV to both format CSVs.
    add_nara_risk(aip_csv, nara_csv)
    add_nara_risk(group_csv, nara_csv)
