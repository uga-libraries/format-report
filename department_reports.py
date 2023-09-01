"""
Converts merged ARCHive format reports into reports for individual departments.

Information included:
* A list of AIPs with format identifications and risk levels
* A summary of risk by collection
* A summary of formats by collection and AIP

Before running this script, run merge_format_reports.py
"""

# usage: python path/department_reports.py archive_formats_by_aip

import numpy as np
import os
import pandas as pd
import sys


def check_argument(argument_list):
    """
    Verifies the required argument format_csv is present, the path is valid,
    and the CSV has the expected data based on the filename.
    """
    # Makes variables with default values to store the results of the function.
    csv_path = None
    errors = []

    # Verifies that the required argument (format_csv) is present,
    # and if it is present that it is a valid directory and has the expected filename.
    if len(argument_list) > 1:
        csv_path = argument_list[1]
        if not os.path.exists(csv_path):
            errors.append(f"Format CSV '{csv_path}' does not exist")
        csv_name = os.path.basename(csv_path)
        if not csv_name.startswith("archive_formats_by_aip"):
            errors.append(f"Format CSV '{csv_path}' is not the correct type (should be by_aip)")
    else:
        errors.append("Required argument format_csv is missing")

    # Returns the results.
    return csv_path, errors


def csv_to_dataframes(csv_file):
    """
    Reads the format csv into a dataframe, including error handling for encoding errors,
    cleans up the data, and splits it into separate dataframes for each group.
    Returns a list of the dataframes.

    """
    # Reads the CSV into a dataframe, ignoring encoding errors from special characters if necessary.
    # Reads a string to allow better comparisons between dataframes.
    try:
        df = pd.read_csv(csv_file, dtype=str)
    except UnicodeDecodeError:
        print("UnicodeDecodeError when trying to read:", csv_file)
        print("The CSV was read by ignoring encoding errors, so those characters are omitted from the dataframe.")
        df = pd.read_csv(csv_file, dtype=str, encoding_errors="ignore")

    # Makes a new column (PUID) by combining Registry Name and Registry Key, if Registry Name is PRONOM.
    df["PRONOM URL"] = np.where(df["Registry Name"] == "https://www.nationalarchives.gov.uk/PRONOM",
                                "https://www.nationalarchives.gov.uk/pronom/" + df["Registry Key"], "NO VALUE")

    # Removes unwanted columns.
    df = df.drop(["Format Type", "Format Standardized Name", "Format Identification", "Registry Name",
                  "Registry Key", "Format Note"], axis=1)

    # Splits the dataframe into a list of dataframes, with one dataframe per group.
    df_list = [d for _, d in df.groupby(['Group'])]
    return df_list


if __name__ == '__main__':

    # Verifies the required argument is present and the path is valid.
    format_csv, errors_list = check_argument(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        print("Script usage: python path/department_reports.py archive_formats_by_aip")
        sys.exit(1)

    # Makes a list of dataframes, one for each group (department), in archive_formats_by_aip.
    department_dfs = csv_to_dataframes(format_csv)

    # For each department, makes an Excel spreadsheet with the risk data and data summaries.

        # Makes the department spreadsheet and adds risk data.

        # Makes a collection risk summary and adds to the department spreadsheet.

        # Makes a collection and AIP format summary and adds to the department spreadsheet.