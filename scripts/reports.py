"""Calculate various subtotal reports of the collection, aip, and file counts for format types, format standard
names, and groups. The reports are saved as csv files.

Usage: python /path/reports.py /path/formats_csv"""

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

type = df.groupby('Format_Type').sum()
name = df.groupby('Format_Standard_Name').sum()
group = df.groupby('Group').sum()
type_group = df.groupby(['Format_Type', 'Group']).sum()
type_name = df.groupby(['Format_Type', 'Format_Standard_Name']).sum()
name_group = df.groupby(['Format_Standard_Name', 'Group']).sum()

# Gets the current date, formatted YYYY-MM, to use in naming the results spreadsheet.
today = datetime.datetime.now().strftime("%Y-%m")

# Gets the file path for where the formats CSV is saved, so the results spreadsheet can be saved there too.
output_directory = os.path.dirname(formats)

# Saves the counts for each field or field combination to a separate tab in the same Excel spreadsheet.
with pd.ExcelWriter(f'{output_directory}/format_analysis_{today}.xlsx') as writer:
    type.to_excel(writer, sheet_name='format type')
    name.to_excel(writer, sheet_name='format name')
    group.to_excel(writer, sheet_name='group')
    type_group.to_excel(writer, sheet_name='format type then group')
    type_name.to_excel(writer, sheet_name='format type then name')
    name_group.to_excel(writer, sheet_name='format name then group')