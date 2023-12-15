"""Make a list of any formats from the ARCHive group format archive_reports that are new since the last format analysis

These new formats need to be added to standardize_formats.csv,
the spreadsheet which has the format standardized name and format type for every format name
within the UGA Libraries' digital preservation system (ARCHive)
before merging and analyzing the ARCHive group format archive_reports.

Parameters:
    report_folder : the path to the folder which contains ARCHive's group file format reports

Returns:
      File new_formats.txt, saved to the report_folder, that contains every new format name
      Prints a message to the terminal if there are new formats
"""

import csv
import os
import sys


def check_argument(argument_list):
    """Check that the required argument report_folder is present and correct

    Parameters:
        argument_list : list from sys.argv, with the script arguments

    Returns:
        report_path : path to the report_path, if provided, or None
        error : string with the error message, if any, or None
    """

    # Makes variables with default values to store the results of the function.
    report_path = None
    error = None

    # Verifies that the required argument (report_folder) is present,
    # and if it is present that it is a valid directory.
    if len(argument_list) > 1:
        report_path = argument_list[1]
        if not os.path.exists(report_path):
            error = f"Report folder '{report_path}' does not exist"
    else:
        error = "Required argument report_folder is missing"

    # Returns the results.
    return report_path, error


def format_check(report_folder_path):
    """Check if every format name from every format report is in standardize_format.csv

    Parameters:
        report_folder_path : the path to the folder which contains ARCHive's group file format reports

    Returns:
        formats_dictionary : dictionary with the format names for keys and values of "Found" or "Missing"
    """

    # Makes a dictionary for storing the results.
    formats_dictionary = {}

    # Gets each file in the report folder, skipping it if it is not a format report.
    for format_report in os.listdir(report_folder_path):
        if not format_report.startswith("file_formats_"):
            continue

        # Reads the data from each ARCHive group format report, which is a CSV with a header row.
        with open(os.path.join(report_folder_path, format_report), encoding="utf-8") as formats:
            read_formats = csv.reader(formats)
            next(read_formats)

            # Gets the format name from each row, skipping it if it is blank (IndexError).
            # If it is not already in the dictionary, compares it to the formats in standardize_formats.csv.
            for row in read_formats:
                try:
                    format_name = row[3]
                except IndexError:
                    continue
                if format_name not in formats_dictionary:
                    match_status = in_standard(format_name)
                    formats_dictionary[format_name] = match_status

    return formats_dictionary


def in_standard(format_to_check):
    """Check if a single format name is in standardize_format.csv

    Parameters:
        format_to_check : the name of a format

    Returns:
        The string "Found" if the format name is in standardize_format.csv,
        or the string "Missing" if it is not.
    """

    # If the format is an undetected error from FITS (a format identification tool),
    # return "Missing" so it is included in new_formats.txt and the archivist sees the error.
    if format_to_check.startswith("ERROR: cannot read"):
        return "Missing"

    # Path to standardize_formats.csv, which is in the script repo.
    standardize_formats_csv = os.path.join(sys.path[1], "standardize_formats.csv")

    # Reads standardize_formats.csv and compares the format to every format in the CSV.
    # If it matches (case insensitive), returns "Found".
    with open(standardize_formats_csv, encoding="utf-8") as open_standard:
        read_standard = csv.reader(open_standard)
        for standardize_row in read_standard:
            if format_to_check.lower() == standardize_row[0].lower():
                return "Found"

    # Returns "Missing" if the format is not in standardize_formats.csv
    # (it did not match any rows in the previous code block).
    return "Missing"


def new_formats_txt(format_matches, report_folder_path):
    """Save format names to new_formats.txt if they are missing from standardize_formats.csv

    Parameters:
        format_matches : dictionary with the format names for keys and values of "Found" or "Missing"
        report_folder_path : the path to the folder which contains ARCHive's group file format reports

    Returns:
        new : Boolean if there are any new formats (True) or not (False),
        so the script can print a message if there are new formats.
    """

    # Makes a variable to track if there are any new formats.
    new = False

    # Makes a list of formats that are not already in standardize_formats.csv.
    # They have a value of "Missing" in the format_matches dictionary.
    new_formats_list = []
    for key in format_matches:
        if format_matches[key] == "Missing":
            new_formats_list.append(key)

    # If there are any new format names, updates the value of new and
    # saves the new format names to a text file named "new_formats.txt" in the report folder.
    # Each format name is on a separate line to make it easy to add as a new row to update standardize_formats.csv.
    if len(new_formats_list) > 0:
        new = True
        with open(os.path.join(report_folder_path, "new_formats.txt"), "w") as new_file:
            for new_format_name in new_formats_list:
                new_file.write(f"{new_format_name}\n")

    # Returns if there are new files so the script can print a status message.
    return new


if __name__ == '__main__':

    # Verifies the required argument is present and the path is valid.
    # If there was an error, prints the error and exits the script.
    report_folder, error_message = check_argument(sys.argv)
    if error_message:
        print(error_message)
        print("Script usage: python path/update_standardization.py report_folder")
        sys.exit(1)

    # Increases the size of csv fields to handle long AIP lists.
    # Gets the maximum size that doesn't give an overflow error.
    while True:
        try:
            csv.field_size_limit(sys.maxsize)
            break
        except OverflowError:
            sys.maxsize = int(sys.maxsize / 10)

    # Makes a dictionary with a unique set of formats from the format archive_reports as the key
    # and 'Found' or 'Missing' for the value to indicate if it is in the standardize_formats.csv.
    formats_checked = format_check(report_folder)

    # Saves any formats that are no in standardize_formats.csv to a file in the report folder.
    # Prints a message if there were new formats so the archivist knows to check for the file.
    new_formats = new_formats_txt(formats_checked, report_folder)
    if new_formats:
        print("New formats were found: check new_formats.txt in report_folder")
