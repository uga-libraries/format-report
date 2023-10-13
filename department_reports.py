"""
Converts the merged ARCHive format report organized by AIP into risk reports for individual departments.
The reports are saved the same folder as the archive_formats_by_aip_csv.

Information included:
* A list of AIPs with format identifications and risk levels
* A summary of risk by collection
* A summary of formats by collection and AIP

Before running this script, run merge_format_reports.py
"""

# usage: python path/department_reports.py formats_current formats_previous
# The arguments are paths to the archive_formats_by_aip.csv
# from the current year and from the last previous format analysis.

import datetime
import numpy as np
import os
import pandas as pd
import sys


def check_arguments(argument_list):
    """
    Verifies that both required arguments are present, the paths are valid,
    and they have the expected data based on the filenames.
    """
    # Makes variables with default values to store the results of the function.
    current_path = None
    previous_path = None
    errors = []

    # Verifies that the first required argument (formats_current) is present,
    # and if it is present that it is a valid directory and has the expected filename.
    if len(argument_list) > 1:
        current_path = argument_list[1]
        if not os.path.exists(current_path):
            errors.append(f"formats_current '{current_path}' does not exist")
        current_filename = os.path.basename(current_path)
        if not (current_filename.startswith("archive_formats_by_aip") and current_filename.endswith(".csv")):
            errors.append(f"'{current_path}' is not the correct type (should be archive_formats_by_aip_date.csv)")
    else:
        errors.append("Required argument formats_current is missing")

    # Verifies that the second required argument (formats_previous) is present,
    # and if it is present that it is a valid directory and has the expected filename.
    if len(argument_list) > 2:
        previous_path = argument_list[2]
        if not os.path.exists(previous_path):
            errors.append(f"formats_previous '{previous_path}' does not exist")
        previous_filename = os.path.basename(previous_path)
        if not (previous_filename.startswith("archive_formats_by_aip") and previous_filename.endswith(".csv")):
            errors.append(f"'{previous_path}' is not the correct type (should be archive_formats_by_aip_date.csv)")
    else:
        errors.append("Required argument formats_previous is missing")

    # Returns the results.
    return current_path, previous_path, errors


def csv_to_dataframe(csv_file):
    """
    Reads the previous or current archive_formats_by_aip_csv into a dataframe,
    including error handling for encoding errors, and cleans up the data.
    Returns a dataframe.
    """
    # Reads the CSV into a dataframe, ignoring encoding errors from special characters if necessary.
    # Reads everything as a string to make actions taken on the dataframes predictable.
    try:
        csv_df = pd.read_csv(csv_file, dtype=str)
    except UnicodeDecodeError:
        print("UnicodeDecodeError when trying to read:", csv_file)
        print("The CSV was read by ignoring encoding errors, so those characters are omitted from the dataframe.")
        csv_df = pd.read_csv(csv_file, dtype=str, encoding_errors="ignore")

    # Adds a column with combined format name, version (if has one), and NARA risk level.
    # This is used for summaries but removed before the risk information is saved to the department report.
    csv_df['Format'] = csv_df['Format Name'] + " " + csv_df['Format Version'] + " (" + csv_df['NARA_Risk Level'] + ")"
    csv_df['Format'] = csv_df['Format'].str.replace(" NO VALUE", "")

    # Makes a new column (PRONOM URL) by combining Registry Name and Registry Key, if Registry Name is PRONOM.
    # If the registry is not PRONOM, the column will have NO VALUE.
    # PRONOM is the only possible registry that our format data currently contains.
    csv_df['PRONOM URL'] = np.where(csv_df['Registry Name'] == "https://www.nationalarchives.gov.uk/PRONOM",
                                    csv_df['Registry Name'] + "/" + csv_df['Registry Key'], "NO VALUE")

    # Makes the NARA_Risk Level column categorical, so it can be automatically sorted from high to low risk.
    risk_order = ["No Match", "High Risk", "Moderate Risk", "Low Risk"]
    csv_df['NARA_Risk Level'] = pd.Categorical(csv_df['NARA_Risk Level'], risk_order)

    # Removes unwanted columns.
    # These are used for the ARCHive report but not department reports.
    csv_df.drop(['Format Type', 'Format Standardized Name', 'Format Identification', 'Registry Name',
                 'Registry Key', 'Format Note', 'NARA_Format Name', 'NARA_PRONOM URL', 'NARA_Match_Type'],
                axis=1, inplace=True)

    # TODO: add current year to NARA columns. Year must be parsed from file name.

    # Replaces spaces in column names with underscores.
    csv_df.columns = csv_df.columns.str.replace(" ", "_")

    # Changes the order of the columns to group format information and risk information.
    # Otherwise, the PRONOM URL would be at the end.
    csv_df = csv_df[['Group', 'Collection', 'AIP', 'Format', 'Format_Name', 'Format_Version', 'PRONOM_URL',
                     'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan']]

    return csv_df


def risk_change(current_df, previous_df):
    """
    Calculates the type of change between the previous analysis and current analysis.
    Returns an updated current dataframe, with columns for previous risk level and risk change.
    """
    # TODO
    return current_df


def risk_levels(dept_df, index_column):
    """
    Calculates the percentage of formats at each risk level.
    Returns a dataframe.
        # Including margins adds totals for each row and renames from default All.
        # Adds columns for any risk level not present. Risk is ordered from high-low.
    """
    # Calculates the number of formats at each risk level.
    # Including margins adds totals for each column and row.
    risk = pd.pivot_table(dept_df, index=index_column, columns='NARA_Risk Level', values='Format',
                          margins=True, aggfunc=len, fill_value=0)

    # Renames the column of each row's totals from default All to Formats, to be more intuitive.
    # Removes the row of each column's totals, which also has the name All by default.
    risk.rename(columns={'All': 'Formats'}, inplace=True)
    risk.drop(['All'], axis='index', inplace=True)

    # Adds in columns for any of the four NARA risk levels that are not present in the dataframe,
    # with a default value of 0 for every row.
    for risk_level in ["No Match", "High Risk", "Moderate Risk", "Low Risk"]:
        if risk_level not in risk:
            risk[risk_level] = 0

    # Calculates the percentage of formats at each risk level for each row, rounded to 2 decimal places.
    risk['No Match %'] = round(risk['No Match'] / risk['Formats'] * 100, 2)
    risk['High Risk %'] = round(risk['High Risk'] / risk['Formats'] * 100, 2)
    risk['Moderate Risk %'] = round(risk['Moderate Risk'] / risk['Formats'] * 100, 2)
    risk['Low Risk %'] = round(risk['Low Risk'] / risk['Formats'] * 100, 2)

    # Removes the columns with format counts, now that the percentages are calculated.
    risk.drop(['No Match', 'High Risk', 'Moderate Risk', 'Low Risk'], axis=1, inplace=True)

    return risk


if __name__ == '__main__':

    # Verifies the required arguments are present and the paths are valid.
    # If there is an error, exits the script.
    current_format_csv, previous_format_csv, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        print("Script usage: python path/department_reports.py formats_current formats_previous")
        sys.exit(1)

    # Reads each CSV into a dataframe, with some data cleanup.
    current_format_df = csv_to_dataframe(current_format_csv)
    previous_format_df = csv_to_dataframe(previous_format_csv)

    # Adds information about change in risk from previous analysis to the current.
    current_format_df = risk_change(current_format_df, previous_format_df)

    # Calculates the directory that archive_formats_by_aip_csv is in.
    # Department risk reports will also be saved to this directory.
    output_folder = os.path.dirname(current_format_csv)

    # Calculates today's date, formatted YYYYMM, to include in the spreadsheet names.
    date = datetime.date.today().strftime("%Y%m")

    # Splits the dataframe into a list of dataframes, with one dataframe per group.
    department_dfs = [d for _, d in current_format_df.groupby(['Group'])]

    # For each department, makes an Excel spreadsheet with the risk data and data summaries.
    for df in department_dfs:

        # Calculates the department, which is the value of the Group column in the first row.
        # The index is reset first or else the first row is not always 0.
        df.reset_index(drop=True, inplace=True)
        dept = df.at[0, 'Group']

        # Calculates the percentage of formats at each risk level for each collection.
        # Duplicates are removed so each format is counted once per collection instead of once per AIP.
        df_dedup = df.drop_duplicates(subset=['Collection', 'Format'])
        collection_risk = risk_levels(df_dedup, 'Collection')

        # Calculates the percentage of formats at each risk level for each AIP.
        aip_risk = risk_levels(df, 'AIP')

        # Calculates which formats are in each collection and AIP,
        # sorted first by risk level and then by format.
        formats = pd.pivot_table(df, index=['Collection', 'AIP'], columns=['NARA_Risk Level', 'Format'],
                                 values=['Format Name'], aggfunc=len, fill_value=0).astype(bool)
        df.drop(['Format'], axis=1, inplace=True)

        # Saves the results to the department risk report,
        # in the same folder as the CSV with ARCHive format data (format_csv).
        xlsx_path = os.path.join(output_folder, f"{dept}_risk_report_{date}.xlsx")
        with pd.ExcelWriter(xlsx_path) as risk_report:
            df.sort_values(['Collection', 'AIP']).to_excel(risk_report, sheet_name="AIP Risk Data", index=False)
            collection_risk.to_excel(risk_report, sheet_name="Collection Risk Levels")
            aip_risk.to_excel(risk_report, sheet_name="AIP Risk Levels")
            formats.to_excel(risk_report, sheet_name="Formats")
