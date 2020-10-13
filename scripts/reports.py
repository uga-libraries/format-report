"""Calculate various subtotal reports of the collection, aip, and file counts for format types, format standard
names, and groups. The reports are saved as csv files. """

# TODO: Sorts A-Z and then a-z. Can we sort case insensitive, or is sorting unnecessary since can sort in Excel?
# TODO: could save each report as a tab in an Excel file instead of individual CSVs.
# TODO: could combine totals and subtotals into the same report.
# TODO: could generate a text document with summary information.
# TODO: may have better analysis of "frequent" if include size as well. Shawn would need to add to the format report.

import datetime
import pandas as pd
import sys

# Makes variables from script arguments.
# formats is the path to the merged ARCHive formats report, which is the data to analyze.
# results is the folder to save reports generated by this script to.
# TODO: add any error handling?
formats = sys.argv[1]
results = sys.argv[2]

# Gets the current date, formatted YYYY-MM, to use in naming the reports.
today = datetime.datetime.now().strftime("%Y-%m")

# Read the data from the csv.
df = pd.read_csv(formats)

# For each report, uses pandas to calculate the collection count, AIP count, and file count for each instance of the
# type of information in the report, for example each format category. Then saves the result to a CSV in the results
# folder. A separate CSV is made for each report.

# Format type, for example audio, image, and text.
type = df.groupby('Format_Type').sum()
type.to_csv(f'{results}/type_{today}.csv')

# Format standardized name, which is a simplified version of the name to group related formats (e.g. different
# versions or subcategories of the same format) together.
name = df.groupby('Format_Standard_Name').sum()
name.to_csv(f'{results}/name_{today}.csv')

# ARCHive group, which is the department or departments responsible for the content.
# If a group is in ARCHive but does not have any AIPs yet, it will not be included in this report.
group = df.groupby('Group').sum()
group.to_csv(f'{results}/group_{today}.csv')

# Format type subdivided by group.
type_group = df.groupby(['Format_Type', 'Group']).sum()
type_group.to_csv(f'{results}/type_group_{today}.csv')

# Format type subdivided by format standardized name.
type_name = df.groupby(['Format_Type', 'Format_Standard_Name']).sum()
type_name.to_csv(f'{results}/type_name_{today}.csv')

# Format standardized name subdivided by group.
name_group = df.groupby(['Format_Standard_Name', 'Group']).sum()
name_group.to_csv(f'{results}/name_group_{today}.csv')

# # Save each of the subtotals to a tab in the same Excel spreadsheet.
# with pd.ExcelWriter(f'{results}/format_analysis.xlsx') as writer:
#     type_totals.to_excel(writer, sheet_name='format type')
#     name_totals.to_excel(writer, sheet_name='format name')