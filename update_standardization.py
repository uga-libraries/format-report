"""Makes a list of any formats from the ARCHive group format reports that are new since the last format analysis and
therefore are not yet in standardize_formats.csv, the spreadsheet which has the format standardized name and format
type for every format identification (name, version, and registry key) within the UGA Libraries' digital preservation
system (ARCHive). These new formats need to be added to standardize_formats.csv before merging and analyzing the
ARCHive group format reports.

Prior to running the script, download all the ARCHive group format reports (one CSV file per group) from the
ARCHive interface and save them to a single folder (report_folder)."""

# Usage: python /path/update_standardization.py /path/report_folder [/path/standardize_formats.csv]

import csv
import os
import sys


def check_arguments(argument_list):
    """
    Verifies the required argument is present and argument paths are valid.
    If no errors, returns the paths for report_folder and standardize_formats.csv.
    If there are errors, prints the errors and exits the script.
    """
    # Makes a list for errors, so all errors can be tested before printing the result,
    # and default values for the two variables assigned from arguments.
    errors = []
    report = None
    standard_csv = os.path.join(sys.path[1], "standardize_formats.csv")

    # Verifies that the required argument (report_folder) is present.
    # and if it is present that it is a valid directory.
    if len(argument_list) > 1:
        report = argument_list[1]
        if not os.path.exists(report):
            errors.append(f"Report folder '{report}' does not exist")
    else:
        errors.append("Required argument report_folder is missing")

    # If the optional second argument is present, replaces the default location (script repo) with the argument value.
    if len(argument_list) > 2:
        standard_csv = argument_list[2]

    # Verifies that standard_csv path is a valid path.
    if not os.path.exists(standard_csv):
        errors.append(f"Standardize Formats CSV '{standard_csv}' does not exist")

    # Returns results.
    return report, standard_csv, errors


def in_standard(standard, format_to_check):
    """Searches for a format name within the standardize formats CSV.
       Returns "Found" if it is present and "Missing" if it is there not."""

    # Reads the standardize formats csv.
    with open(standard, encoding="utf-8") as open_standard:
        read_standard = csv.reader(open_standard)

        # Checks each row in the standardize formats csv. row[0] is the format name.
        for standardize_row in read_standard:

            # If the format is an undetected error from FITS (the format identification tool), return "Missing"
            # so it is included in the new_formats.txt spreadsheet and staff see the error.
            if format_to_check.startswith("ERROR: cannot read"):
                return "Missing"

            # If the format name is in the CSV, returns "Found" and stops searching the CSV.
            # Matching lowercase versions of the format names to ignore variations in capitalization.
            if format_to_check.lower() == standardize_row[0].lower():
                return "Found"

    # If the format is not in the standardize formats csv (meaning the previous code block did not return anything so
    # this code runs), returns "Missing".
    return "Missing"


def new_formats_txt(format_matches, report_folder_path):
    """
    Locates formats that did not match and saves them to a file (new_formats.txt) in the reports_folder.
    Returns if there were any new formats or not (Boolean) so a script status message may be printed.
    """

    # Makes a variable to track if there are any new formats.
    new = False

    # Makes a list of formats that are not already in standardize_formats.csv
    # They have a value of "Missing" in the format_matches dictionary.
    new_formats_list = []
    for key in format_matches:
        if format_matches[key] == "Missing":
            new_formats_list.append(key)

    # If there are any new format names, updates the value of new and
    # saves the new format names to a text file named "new_formats.txt" in the report folder.
    # Each format name is on a separate line to make it easy to add as a new row to updating standardize_formats.csv.
    if len(new_formats_list) > 0:
        new = True
        with open(os.path.join(report_folder_path, "new_formats.txt"), "w") as new_file:
            for new_format_name in new_formats_list:
                new_file.write(f"{new_format_name}\n")

    # Returns if there are new files so the script can print a status message.
    return new


if __name__ == '__main__':

    # Verifies the required argument is present and argument paths are valid.
    # If no errors, returns the path for standardize_formats.csv. Otherwise, prints the error(s) and exits the script.
    report_folder, standardize_formats_csv, errors_list = check_arguments(sys.argv)

    # If there were errors, prints the errors and exits the scripts.
    if len(errors_list) > 0:
        print("The following errors were detected:")
        for error in errors_list:
            print(f"\t* {error}")
        print("Script usage: python path/update_standardization.py path/report_folder [path/standardize_formats.csv]")
        exit()

    # Increases the size of csv fields to handle long AIP lists.
    # Gets the maximum size that doesn't give an overflow error.
    while True:
        try:
            csv.field_size_limit(sys.maxsize)
            break
        except OverflowError:
            sys.maxsize = int(sys.maxsize / 10)

    # Makes a dictionary for storing every format name checked, and if it was in standardize_formats.csv or not,
    # so that each format is only checked once. Formats may be repeated thousands of times in the ARCHive group reports.
    formats_checked = {}

    # Gets each file in the report folder.
    for format_report in os.listdir(report_folder):

        # Skips it if the document is not an ARCHive group format report.
        if not format_report.startswith("file_formats_"):
            continue

        # Reads the data from the ARCHive group format report, which is a CSV.
        with open(os.path.join(report_folder, format_report)) as formats:
            read_formats = csv.reader(formats)

            # Skips the header row.
            next(read_formats)

            # Iterates over every row in the report.
            for row in read_formats:

                # Gets the format name from the 4th column.
                # Skips it if there is no value in the 4th column. Reports may download with a blank row at the end.
                try:
                    format_name = row[3]
                except IndexError:
                    continue

                # Checks if the script has already searched for this format in standardize_formats.csv. If it hasn't,
                # searches for the format and records the result in the formats_checked dictionary.
                if format_name not in formats_checked:
                    found = in_standard(standardize_formats_csv, format_name)
                    formats_checked[format_name] = found

    # Saves any formats that are no in standardize_formats.csv to a file in the report folder.
    # Prints a message if there were new formats so the archivist knows to check for the file.
    new_formats = new_formats_txt(formats_checked, report_folder)
    if new_formats:
        print("New formats were found: check new_formats.txt in report_folder")
