"""
Converts the merged ARCHive format report organized by AIP (archive_formats_by_aip_date.csv)
into risk reports for individual departments.
The department reports are Excel spreadsheets and are saved the same folder as the format report.

Information included:
    * A list of AIPs with format identifications, risk levels, and risk change since the last analysis
    * A summary of risk by collection
    * A summary of risk by AIP
    * A summary of formats by collection and AIP

Use merge_format_reports.py to produce archive_formats_by_aip_date.csv.
"""

# usage: python path/department_reports.py current_formats_csv previous_formats_csv
# The arguments are paths to the archive_formats_by_aip_date.csv
# from the current year and from the last previous format analysis.

import datetime
import numpy as np
import os
import pandas as pd
import re
import sys


def check_arguments(argument_list):
    """
    Verifies that both required arguments are present, the paths are valid,
    and they have the expected data based on the filenames.
    Returns both arguments and a list of errors.
    """
    # Makes variables with default values to store the results of the function.
    current_path = None
    previous_path = None
    errors = []

    # Verifies that the first required argument (current_formats_csv) is present,
    # and if it is present that it is a valid directory and has the expected filename.
    if len(argument_list) > 1:
        current_path = argument_list[1]
        if not os.path.exists(current_path):
            errors.append(f"current_formats_csv '{current_path}' does not exist")
        current_filename = os.path.basename(current_path)
        if not (current_filename.startswith("archive_formats_by_aip") and current_filename.endswith(".csv")):
            errors.append(f"'{current_path}' is not the correct type (should be archive_formats_by_aip_date.csv)")
    else:
        errors.append("Required argument current_formats_csv is missing")

    # Verifies that the second required argument (previous_formats_csv) is present,
    # and if it is present that it is a valid directory and has the expected filename.
    if len(argument_list) > 2:
        previous_path = argument_list[2]
        if not os.path.exists(previous_path):
            errors.append(f"previous_formats_csv '{previous_path}' does not exist")
        previous_filename = os.path.basename(previous_path)
        if not (previous_filename.startswith("archive_formats_by_aip") and previous_filename.endswith(".csv")):
            errors.append(f"'{previous_path}' is not the correct type (should be archive_formats_by_aip_date.csv)")
    else:
        errors.append("Required argument previous_formats_csv is missing")

    # Returns the results. If both arguments are correct, errors is an empty list.
    return current_path, previous_path, errors


def csv_to_dataframe(csv_file):
    """
    Reads the previous or current archive_formats_by_aip_csv into a dataframe,
    including error handling for encoding errors, and cleans up the data.
    Returns the dataframe.
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
    # If there is no version, the column will have NO VALUE.
    # Format is used for summaries but removed before the risk information is saved to the department report.
    csv_df['Format'] = csv_df['Format Name'] + " " + csv_df['Format Version'] + " (" + csv_df['NARA_Risk Level'] + ")"
    csv_df['Format'] = csv_df['Format'].str.replace(" NO VALUE", "")

    # Makes a new column (PRONOM URL) by combining Registry Name and Registry Key, if Registry Name is PRONOM.
    # If the registry is not PRONOM, the column will be given the value "NO VALUE" instead.
    # PRONOM is the only registry that our format data currently contains.
    csv_df['PRONOM URL'] = np.where(csv_df['Registry Name'] == "https://www.nationalarchives.gov.uk/PRONOM",
                                    csv_df['Registry Name'] + "/" + csv_df['Registry Key'], "NO VALUE")

    # Makes the NARA_Risk Level column ordered categorical,
    # so risk levels can be compared and sorted.
    risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
    csv_df['NARA_Risk Level'] = pd.Categorical(csv_df['NARA_Risk Level'], risk_order, ordered=True)

    # Removes unwanted columns.
    # These are used for the ARCHive report but not department reports.
    csv_df.drop(['Format Type', 'Format Standardized Name', 'Registry Name', 'Registry Key', 'Format Note',
                 'NARA_Format Name', 'NARA_PRONOM URL', 'NARA_Match_Type'],
                axis=1, inplace=True)

    # Replaces spaces in column names with underscores.
    csv_df.columns = csv_df.columns.str.replace(" ", "_")

    # Adds the year the CSV data is from to NARA column names, to distinguish between current and previous data.
    # The year is parsed from the file name.
    regex = re.match(".*_([0-9]{4})-[0-9]{2}.csv", csv_file)
    year = regex.group(1)
    csv_df.rename(columns={'NARA_Risk_Level': f'{year}_NARA_Risk_Level',
                           'NARA_Proposed_Preservation_Plan': f'{year}_NARA_Proposed_Preservation_Plan'},
                  inplace=True)

    # Changes the order of the columns to group format information and risk information.
    # Otherwise, the PRONOM URL would be at the end.
    csv_df = csv_df[['Group', 'Collection', 'AIP', 'Format_Identification', 'Format', 'Format_Name', 'Format_Version',
                     'PRONOM_URL', f'{year}_NARA_Risk_Level', f'{year}_NARA_Proposed_Preservation_Plan']]

    return csv_df


def risk_change(current_df, previous_df):
    """
    Updates the current analysis dataframe with risk data from the previous analysis and
    the type of change between the previous analysis and current analysis.
    Returns the updated current dataframe.
    """
    # Gets the name of the NARA Risk Level column for each dataframe,
    # which includes the year and so is different each time the analysis is run.
    previous_risk = previous_df.columns.to_list()[8]
    current_risk = current_df.columns.to_list()[8]

    # Adds previous risk data to the current, matching on the AIP and Format_Identification columns.
    previous_columns = ['AIP', 'Format_Identification', previous_risk]
    current_df = pd.merge(current_df, previous_df[previous_columns], how="left")

    # Removes the Format_Identification column, which was only needed to align previous with current.
    current_df.drop(['Format_Identification'], axis=1, inplace=True)

    # Adds a column to current with the type of change from previous to current.
    conditions = [(current_df[previous_risk] != "No Match") & (current_df[previous_risk] > current_df[current_risk]),
                  (current_df[previous_risk] < current_df[current_risk]) & (current_df[current_risk] != "No Match"),
                  current_df[previous_risk].isnull(),
                  (current_df[previous_risk] == "No Match") & (current_df[current_risk] != "No Match"),
                  (current_df[previous_risk] != "No Match") & (current_df[current_risk] == "No Match"),
                  current_df[previous_risk] == current_df[current_risk]]
    change_type = ["Decrease", "Increase", "New Format", "New Match", "Unmatched", "Unchanged"]
    current_df['Risk_Level_Change'] = np.select(conditions, change_type)

    return current_df


def risk_levels(dept_df, index_column):
    """
    Calculates the percentage of formats at each risk level.
    Returns a dataframe.
    """
    # Calculates the number of formats at each risk level.
    # Including margins adds totals for each column and row.
    current_risk_column = dept_df.columns.to_list()[7]
    risk = pd.pivot_table(dept_df, index=index_column, columns=current_risk_column, values='Format',
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
    # Columns are in order from high-low risk.
    risk['No Match %'] = round(risk['No Match'] / risk['Formats'] * 100, 2)
    risk['High Risk %'] = round(risk['High Risk'] / risk['Formats'] * 100, 2)
    risk['Moderate Risk %'] = round(risk['Moderate Risk'] / risk['Formats'] * 100, 2)
    risk['Low Risk %'] = round(risk['Low Risk'] / risk['Formats'] * 100, 2)

    # Removes the columns with format counts, now that the percentages are calculated.
    risk.drop(['No Match', 'High Risk', 'Moderate Risk', 'Low Risk'], axis=1, inplace=True)

    return risk


if __name__ == '__main__':

    # Verifies that both required arguments are present, the paths are valid, and the filenames are correct.
    # If there are any errors, exits the script.
    current_formats_csv, previous_formats_csv, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        print("Script usage: python path/department_reports.py current_formats_csv previous_formats_csv")
        sys.exit(1)

    # Reads each CSV into a dataframe, with some data cleanup.
    current_format_df = csv_to_dataframe(current_formats_csv)
    previous_format_df = csv_to_dataframe(previous_formats_csv)

    # Adds the previous risk and the change in risk since the previous analysis to the current analysis data.
    current_format_df = risk_change(current_format_df, previous_format_df)

    # Calculates the directory the current_formats_csv is in. Department reports will be saved here.
    output_folder = os.path.dirname(current_formats_csv)

    # Calculates today's date, formatted YYYYMM, to include in the department report names.
    date = datetime.date.today().strftime("%Y%m")

    # Splits the dataframe into a list of dataframes, with one dataframe per ARCHive group.
    department_dfs = [d for _, d in current_format_df.groupby(['Group'])]

    # For each department, makes an Excel spreadsheet with the risk data and data summaries.
    for df in department_dfs:

        # Calculates the department, which is the value of the Group column in the first row.
        # The index is reset or else the first row is not always 0 because of how the original dataframe is split.
        df.reset_index(drop=True, inplace=True)
        dept = df.at[0, 'Group']

        # Calculates the percentage of formats at each risk level for the department.
        # Duplicates are removed so each format is counted once instead of once per AIP.
        dept_dedup = df.drop_duplicates(subset=['Format'])
        dept_risk = risk_levels(dept_dedup, 'Group')

        # Calculates the percentage of formats at each risk level for each collection.
        # Duplicates are removed so each format is counted once per collection instead of once per AIP.
        coll_dedup = df.drop_duplicates(subset=['Collection', 'Format'])
        collection_risk = risk_levels(coll_dedup, 'Collection')

        # Calculates the percentage of formats at each risk level for each AIP.
        # Duplicates are removed so a format is not counted twice, once with and once without a PUID,
        # which happens in legacy format data before we started cleaning up doubles like this automatically.
        aip_dedup = df.drop_duplicates(subset=['AIP', 'Format_Name', 'Format_Version'])
        aip_risk = risk_levels(aip_dedup, 'AIP')

        # Calculates which formats are in each collection and AIP, sorted first by risk level and then by format.
        current_risk_column = df.columns.to_list()[7]
        formats = pd.pivot_table(df, index=['Collection', 'AIP'], columns=[current_risk_column, 'Format'],
                                 values=['Format_Name'], aggfunc=len, fill_value=0).astype(bool)
        formats.sort_values([current_risk_column, 'Format'], ascending=[False, True], axis=1, inplace=True)
        df.drop(['Format'], axis=1, inplace=True)

        # Saves the results to the department risk report,
        # in the same folder as the CSV with ARCHive format data (current_formats_csv).
        dept_report_path = os.path.join(output_folder, f"{dept}_risk_report_{date}.xlsx")
        with pd.ExcelWriter(dept_report_path) as dept_report:
            df.sort_values(['Collection', 'AIP']).to_excel(dept_report, sheet_name="AIP Risk Data", index=False)
            dept_risk.to_excel(dept_report, sheet_name="Department Risk Levels")
            collection_risk.to_excel(dept_report, sheet_name="Collection Risk Levels")
            aip_risk.to_excel(dept_report, sheet_name="AIP Risk Levels")
            formats.to_excel(dept_report, sheet_name="Formats")
