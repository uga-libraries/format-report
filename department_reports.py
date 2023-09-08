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
                  "Registry Key", "Format Note", "NARA_Format Name", "NARA_PRONOM URL", "NARA_Match_Type"], axis=1)

    # Changes the order of the columns to group format information and risk information.
    # Otherwise, the PRONOM URL would be at the end.
    df = df[["Group", "Collection", "AIP", "Format Name", "Format Version", "PRONOM URL",
             "NARA_Risk Level", "NARA_Proposed Preservation Plan"]]

    # Splits the dataframe into a list of dataframes, with one dataframe per group.
    df_list = [d for _, d in df.groupby(['Group'])]

    return df_list


if __name__ == '__main__':

    # Verifies the required argument is present and the path is valid.
    # If there is an error, exits the script.
    format_csv, errors_list = check_argument(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        print("Script usage: python path/department_reports.py archive_formats_by_aip")
        sys.exit(1)

    # Makes a list of dataframes, one for each group (department), in archive_formats_by_aip.
    department_dfs = csv_to_dataframes(format_csv)

    # Calculates the directory that format_csv is in, to use for saving script outputs.
    output_folder = os.path.dirname(format_csv)

    # For each department, makes an Excel spreadsheet with the risk data and data summaries.
    for dept_df in department_dfs:

        # Calculates the department, which is the value of the Group column in the first row.
        # The index is reset first or else the first row is not always 0.
        dept_df = dept_df.reset_index(drop=True)
        dept = dept_df.at[0, "Group"]

        # Calculates the number of AIPs with formats at each risk level for each collection.
        # The AIP is counted once for each format it contains that is at that risk level.
        # Including margins adds totals for each row and each column.
        collection_risk = pd.pivot_table(dept_df, index="Collection", columns="NARA_Risk Level", values="AIP",
                                         margins=True, aggfunc=len)
        collection_risk.fillna(0, inplace=True)
        collection_risk.rename(columns={"All": "AIPs"}, inplace=True)

        # Makes a summary of formats by collection and AIP.
        # For format, it combines the format name, version (if has one), and NARA risk level.
        dept_df["Format"] = dept_df['Format Name'] + " " + dept_df['Format Version'] + " (" + dept_df['NARA_Risk Level'] + ")"
        dept_df["Format"] = dept_df["Format"].str.replace(" NO VALUE", "")
        formats = pd.pivot_table(dept_df, index=["Collection", "AIP"], columns=["Format"], values=["Format Name"],
                                 aggfunc=len)
        formats.fillna(0, inplace=True)
        dept_df.drop(["Format"], axis=1, inplace=True)

        # Saves the results to the department risk report.
        xlsx_path = os.path.join(output_folder, f"{dept}_risk_report.xlsx")
        with pd.ExcelWriter(xlsx_path) as risk_report:
            dept_df.to_excel(risk_report, sheet_name="AIP Risk Data", index=False)
            collection_risk.to_excel(risk_report, sheet_name="Collection Risk Levels")
            formats.to_excel(risk_report, sheet_name="Formats")
