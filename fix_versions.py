"""Correct the version in a combined format report produced by merge_format_reports.py

The CSV files created by merge_format_reports.py are opened in Excel to update risk matches,
but Excel automatically reformats version numbers to remove 0 from the end, which is an error.
Form example, 1.0 becomes 1 and 2.10 becomes 2.1.

The correct version is still part of Format_Identification.
This script updates the version column with the version from Format_Identification.

Parameters:
    csv_path : the path to one of the combined format reports made by the merge_formats_report.py script (CSV)

Returns:
    Updated CSV file with the correct version information.
"""

import os
import pandas as pd
import sys


def check_argument(argument_list):
    """Verify the requirement argument csv_path is present and correct

    Parameters:
        argument_list :

    Returns:
        path : path to the CSV to be fixed, if provided, or None
        error : string with an error message, if any, or None
    """

    # Makes variables with default values to store the results of the function.
    path = None
    error = None

    # Verifies that the required argument (csv_path) is present.
    if len(argument_list) > 1:
        path = argument_list[1]
        # Verifies that the argument path is valid.
        if os.path.exists(path):
            # Verifies that the argument is a file that matches the expected naming conventions.
            filename = os.path.basename(path)
            if not(filename.startswith("archive_formats_by") and filename.endswith(".csv")):
                error = f"CSV path '{path}' is not an expected merged ARCHive format report."
        else:
            error = f"CSV path '{path}' does not exist"
    else:
        error = "Required argument csv_path is missing"

    return path, error


if __name__ == '__main__':

    # Verifies the required argument is present and correct.
    # If there was an error, prints the error and exits the script.
    csv_path, error_msg = check_argument(sys.argv)
    if error_msg:
        print(error_msg)
        sys.exit(1)

    # Replaces the values in the Format_Version column with the version information
    # in the Format_Identification column (formatted name|version|PUID).
    df = pd.read_csv(csv_path, dtype="string")
    df['Format_Version'] = df['Format_Identification'].str.split('|').str[1]

    # Removes blank rows introduced by Excel.
    df = df.dropna(how="all")

    # Updates the CSV.
    df.to_csv(csv_path, index=False)
