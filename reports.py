"""Calculates subtotals of collection, AIP, and file counts for different categories: format types, format standardized
names, groups, and combinations of those categories. The results are saved to an Excel file, one tab per subtotal.

This script uses the merged ARCHive formats CSV, which is created with the csv_merge.py script. This CSV is organized
by group and then by format name. Relevant columns for this analysis are Group, Collection_Count, AIP_Count,
File_Count, Format_Type, Format_Standardized_Name, and Format_Name.

Ideas for future development:
    * A report that lists the most common formats, however that is defined.
    * A report that compares the current report to a previous one to show change over time.
    * Have size as well as count included in the file formats reports so can summarize by size.
"""

# Usage: python /path/reports.py /path/formats_csv

import datetime
import os
import pandas as pd
import sys

# Makes a variable from the script argument, which is the path to the CSV with the format to be analyzed.
# If it is not present, prints an error message and quits the script.
try:
    formats = sys.argv[1]
except IndexError:
    print("Need to provide the path to the CSV with format information to be analyzed.")
    print("Script usage: python /path/reports.py /path/formats_csv")
    exit()

# Reads the data from the CSV into a pandas dataframe.
# If the path to the CSV is not valid, prints an error message and quits the script.
try:
    df = pd.read_csv(formats)
except FileNotFoundError:
    print("The path for the format CSV is not valid.")
    print("Script usage: python /path/reports.py /path/formats_csv")
    exit()

# For each field or field combination to analyze, uses pandas to calculate the collection count, AIP count, and file
# count for each instance of the field. Fields are:
#       Format type: category of the format, for example audio, image, or text.
#       Format standardized name: a simplified version of the name, for example removing version information.
#       Group: ARCHive group name, which is the department or departments responsible for the content.

format_type = df.groupby('Format_Type').sum()
name = df.groupby('Format_Standardized_Name').sum()
group = df.groupby('Group').sum()
format_type_then_group = df.groupby(['Format_Type', 'Group']).sum()
format_type_then_name = df.groupby(['Format_Type', 'Format_Standardized_Name']).sum()
name_then_group = df.groupby(['Format_Standardized_Name', 'Group']).sum()

# Gets the current date, formatted YYYY-MM, to use in naming the results spreadsheet.
today = datetime.datetime.now().strftime("%Y-%m")

# Gets the file path for where the formats CSV is saved, so the results spreadsheet can be saved there too.
output_directory = os.path.dirname(formats)

# Saves the counts for each field or field combination to a separate tab in the same Excel spreadsheet.
with pd.ExcelWriter(f'{output_directory}/format_analysis_{today}.xlsx') as writer:
    format_type.to_excel(writer, sheet_name='format type')
    name.to_excel(writer, sheet_name='format name')
    group.to_excel(writer, sheet_name='group')
    format_type_then_group.to_excel(writer, sheet_name='format type then group')
    format_type_then_name.to_excel(writer, sheet_name='format type then name')
    name_then_group.to_excel(writer, sheet_name='format name then group')
