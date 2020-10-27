"""Calculates subtotals of collection, AIP, and file counts for different categories: format types, format standardized
names, groups, and combinations of those categories. The results are saved to an Excel file, one tab per subtotal.

This script uses the merged ARCHive formats CSV, which is created with the csv_merge.py script. This CSV is organized
by group and then by format name. Relevant columns for this analysis are Group, Collection_Count, AIP_Count,
File_Count, Format_Type, Format_Standardized_Name, and Format_Name."""

# Usage: python /path/reports.py ????

import csv
import datetime
import os
import pandas as pd
import sys

# Makes the report folder (script argument) the current directory. Displays an error message and quits the script if
# the argument is missing or not a valid directory.
try:
    report_folder = sys.argv[1]
    os.chdir(report_folder)
except (IndexError, FileNotFoundError):
    print("The report folder path was either not given or is not a valid directory. Please try the script again.")
    print("Script usage: python /path/csv_merge.py /path/reports [/path/standardize_formats.csv]")
    exit()

