"""Convert the merged ARCHive format report (archive_formats_by_aip_date.csv) into risk reports for each department.

The department archive_reports are Excel spreadsheets and are saved the same folder as the format report.

Information included:
    * A list of AIPs with format identifications, risk levels, and risk change since the last analysis
    # The percentage of formats at each risk level for the entire department
    * The percentage of formats at each risk level for each collection
    * The percentage of formats at each risk level for each AIP
    * The formats, and their risk levels, for each collection

Parameters:
    current_formats_csv : the path to the "archive_formats_by_aip.csv" made by the merge_format_reports.py
    with data for the current year's analysis
    previous_formats_csv : the path to the "archive_formats_by_aip.csv" made by the merge_format_reports.py
    with data for the previous year's analysis

Returns:
    One spreadsheet per ARCHive group in the current_formats_csv
"""

import datetime
import numpy as np
import os
import pandas as pd
import re
import sys


def check_arguments(argument_list):
    """Check both required arguments are present and correct

    Parameters:
        argument_list : the list from sys.argv with the script parameters

    Returns:
        current_path : the path to archive_formats_by_aip.csv for the current year, or None
        previous_path : the path to archive_formats_by_aip.csv for the previous year, or None
        errors : the list of errors, if any, or an empty list
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
    """Read a CSV into a dataframe, reformat the data, and add additional data

    Parameters:
        csv_file : the path to one of the archive_by_formats_by_aip.csv files

    Returns:
        csv_df : a dataframe with the information from the CSV, reformatted and with additional data
    """

    # Reads the CSV into a dataframe, ignoring encoding errors from special characters if necessary.
    # Reads everything as a string to make actions taken on the dataframes predictable.
    try:
        csv_df = pd.read_csv(csv_file, dtype=str)
    except UnicodeDecodeError:
        print("UnicodeDecodeError when trying to read:", csv_file)
        print("The CSV was read by ignoring encoding errors, so those characters are omitted from the dataframe.")
        csv_df = pd.read_csv(csv_file, dtype=str, encoding_errors="ignore")

    # Makes a new column (PRONOM URL) by combining Registry Name and Registry Key, if Registry Name is PRONOM.
    # If the registry is not PRONOM, the column will be given the value "NO VALUE" instead.
    # PRONOM is the only registry that our format data currently contains.
    csv_df['PRONOM_URL'] = np.where(csv_df['Registry_Name'] == "https://www.nationalarchives.gov.uk/PRONOM",
                                    csv_df['Registry_Name'] + "/" + csv_df['Registry_Key'], "NO VALUE")

    # Makes the NARA_Risk Level column ordered categorical,
    # so risk levels can be compared and sorted.
    risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
    csv_df['NARA_Risk_Level'] = pd.Categorical(csv_df['NARA_Risk_Level'], risk_order, ordered=True)

    # Removes unwanted columns.
    # These are used for the ARCHive report but not department archive_reports.
    csv_df.drop(['Format_Type', 'Format_Standardized_Name', 'Registry_Name', 'Registry_Key', 'Format_Note',
                 'NARA_Format_Name', 'NARA_PRONOM_URL', 'NARA_Match_Type'],
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
    csv_df = csv_df[['Group', 'Collection', 'AIP', 'Format_Identification', 'Format_Name', 'Format_Version',
                     'PRONOM_URL', f'{year}_NARA_Risk_Level', f'{year}_NARA_Proposed_Preservation_Plan']]

    return csv_df


def formats_pivot(current_df):
    """Make a table with the formats, organized by decreasing risk, in each collection

    Parameters:
        current_df : a dataframe with the information from the archive_formats_by_aip.csv for the current year

    Returns:
        pivot : a dataframe with the pivot table values of risk and format by collection,
        with Boolean to indicate if the format is in that collection or not
    """

    # Gets the name fo the NARA Risk Level column,
    # which includes the year and so is different each time the analysis is run.
    current_risk_column = current_df.columns.to_list()[6]

    # Adds a column with combined format name and NARA risk level.
    # Format is a temporary, for naming format columns for this pivot table.
    # It includes the risk, even though that is also a separate row for this pivot table, for readability.
    current_df['Format'] = current_df['Format_Name'] + " (" + current_df[current_risk_column].astype(str) + ")"

    # Makes a pivot table with rows by collection and columns first by NARA risk level and then by Format.
    # Initially, the table has the number of formats in each AIP, but this is converted to True/False
    # since formats will always appear 0, 1, or 2 (legacy duplication from PUID and no PUID) in an AIP.
    pivot = pd.pivot_table(current_df, index=['Collection'], columns=[current_risk_column, 'Format'],
                           values=['Format_Name'], aggfunc=len, fill_value=0).astype(bool)

    # Orders the format columns first by risk (high to low) and then by format name.
    pivot.sort_values([current_risk_column, 'Format'], ascending=[False, True], axis=1, inplace=True)

    # Removes the temporary Format column.
    current_df.drop(['Format'], axis=1, inplace=True)

    return pivot


def risk_change(current_df, previous_df):
    """Update the current analysis dataframe with risk data from the previous analysis and the change between the two

    Parameters:
        current_df : a dataframe with the information from the archive_formats_by_aip.csv for the current year
        previous_df : a dataframe with the information from the archive_formats_by_aip.csv for the previous year

    Returns:
        current_df : a dataframe with the information from the archive_formats_by_aip.csv for the current year,
        the previous year, and the type of change between the two
    """

    # Gets the name of the NARA Risk Level column for each dataframe,
    # which includes the year and so is different each time the analysis is run.
    previous_risk = previous_df.columns.to_list()[7]
    current_risk = current_df.columns.to_list()[7]

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
    """Calculate the percentage of formats at each risk level

    Parameters:
        dept_df : a dataframe with the information for one ARCHive group from the archive_formats_by_aip.csv
        index_column : the name of the column (Group, Collection, or AIP) to subtotal the formats on

    Returns:
        risk : a dataframe with the percentage of formats at each risk level, ordered by highest to lowest risk
    """

    # Removes duplicate formats (based on name and version) from the dataframe
    # within the unit of analysis (index_column).
    # For example, with collections, a format should be counted once per collection.
    # Even the AIP analysis is deduplicated because of formats listed with and without a PUID.
    # If a format with and without a PUID present, the one with the PUID is kept during deduplication
    # since the NARA match is most likely to be accurate. It is the last one after sorting,
    # because the upper case "NO VALUE" for no PRONOM URL is sorted before the lowercase PRONOM URL.
    subset_list = [index_column] + ['Format_Name', 'Format_Version']
    df_dedup = dept_df.sort_values('PRONOM_URL').drop_duplicates(subset=subset_list, keep='last')

    # Calculates the number of formats at each risk level.
    # Including margins=True adds totals for each column and row.
    current_risk_column = df_dedup.columns.to_list()[6]
    risk = pd.pivot_table(df_dedup, index=index_column, columns=current_risk_column, values='Format_Name',
                          margins=True, aggfunc=len, fill_value=0)

    # Renames the column of each row's totals from default All to Formats, to be more intuitive.
    # Removes the row of each column's totals, which also has the name All,
    # since it is inflated from formats being in multiple AIPs.
    risk.rename(columns={'All': 'Formats'}, inplace=True)
    risk.drop(['All'], axis='index', inplace=True)

    # Adds in columns for any of the four NARA risk levels that are not present in the dataframe,
    # with a default value of 0 for every row.
    for risk_level in ["No Match", "High Risk", "Moderate Risk", "Low Risk"]:
        if risk_level not in risk:
            risk[risk_level] = 0

    # Calculates the percentage of formats at each risk level for each row, rounded to 2 decimal places.
    # Columns are in order from high-low risk.
    risk['No_Match_%'] = round(risk['No Match'] / risk['Formats'] * 100, 2)
    risk['High_Risk_%'] = round(risk['High Risk'] / risk['Formats'] * 100, 2)
    risk['Moderate_Risk_%'] = round(risk['Moderate Risk'] / risk['Formats'] * 100, 2)
    risk['Low_Risk_%'] = round(risk['Low Risk'] / risk['Formats'] * 100, 2)

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

    # Calculates variables used for naming and saving the department archive_reports.
    output_folder = os.path.dirname(current_formats_csv)
    date = datetime.date.today().strftime("%Y%m")

    # For each department, makes an Excel spreadsheet with the risk data and data summaries.
    for dept in current_format_df['Group'].unique().tolist():

        # Makes a dataframe with the data for the department.
        df = current_format_df[current_format_df['Group'] == dept].copy()

        # Calculates the percentage of formats at each risk level for the department, each collection, and each AIP.
        dept_risk = risk_levels(df, 'Group')
        collection_risk = risk_levels(df, 'Collection')
        aip_risk = risk_levels(df, 'AIP')

        # Calculates which formats are in each collection and AIP, sorted first by risk level and then by format.
        formats = formats_pivot(df)

        # Saves the results to the department risk report,
        # in the same folder as the CSV with ARCHive format data (current_formats_csv).
        dept_report_path = os.path.join(output_folder, f"{dept}_risk_report_{date}.xlsx")
        with pd.ExcelWriter(dept_report_path) as dept_report:
            df.sort_values(['Collection', 'AIP']).to_excel(dept_report, sheet_name="AIP_Risk_Data", index=False)
            dept_risk.to_excel(dept_report, sheet_name="Department_Risk_Levels")
            collection_risk.to_excel(dept_report, sheet_name="Collection_Risk_Levels")
            aip_risk.to_excel(dept_report, sheet_name="AIP_Risk_Levels")
            formats.to_excel(dept_report, sheet_name="Formats")
