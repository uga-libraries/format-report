"""Makes a list of any formats from the ARCHive reports that are new since the last format analysis and therefore are
not yet in standardize_formats.csv, the spreadsheet which has the standard format name and format type for every
format variant within the UGA Libraries' digital preservation system (ARCHive). These new formats need to be added to
standardize_formats.csv before merging and analyzing the format reports.

Prior to running the script, download all the ARCHive format reports (one tab-delimited text file per group) from the
ARCHive interface and save them to a single folder.

Usage: python /path/update_standardization /path/reports"""

import csv
import os
import sys

# Assign variables from arguments.
#    report_folder is the directory with the ARCHive format reports to be analyzed.
#    standard_csv has the path to the csv document with current standardization rules.
# TODO: add error handling for missing/incorrect arguments.
# TODO: standardize_formats.csv is in the same folder as the script. Any way to reference without a path?
report_folder = sys.argv[1]
standard_csv = sys.argv[2]

# Makes the report folder the current directory.
os.chdir(report_folder)


def in_standard(standard, format_to_check):
    """Searches for a format name within the standardize formats CSV.
       Returns True if it is present and False if it is there not."""

    # Makes a variable to track if the format is found.
    format_match = "Missing"

    # Reads the csv file with the standardization rules.
    with open(standard, encoding='utf-8') as open_standard:
        read_standard = csv.reader(open_standard)

        # Checks each row in the standardize formats CSV. row[0] is the format name in the CSV.
        for standardize_row in read_standard:

            # If the format name is in the CSV, updates the format_match variable and stops searching the CSV.
            # Matching lowercase versions of the format names to account for variations in capitalization. 
            if format_to_check.lower() == standardize_row[0].lower():
                format_match = "Present"
                break

    # Returns if the format is in the CSV already (Present) or if it is new (Missing).
    return format_match


# Increases the size of csv fields to handle long AIP lists.
# Gets the maximum size that doesn't give an overflow error.
while True:
    try:
        csv.field_size_limit(sys.maxsize)
        break
    except OverflowError:
        sys.maxsize = int(sys.maxsize / 10)

# Gets each format report in the format folder.
# Saves any new formats (formats that are not in the standardized formats csv) to a list.
formats_checked = {}
for format_report in os.listdir(report_folder):

    # Skips it if the document is not a format report.
    if not format_report.startswith('file_formats_'):
        continue

    # Reads the data from the format report, which is a tab delimited file.
    with open(format_report) as formats:
        read_formats = csv.reader(formats, delimiter='\t')

        # Skips the header row.
        next(read_formats)

        # Iterates over every row in the format report.
        for row in read_formats:

            # Gets the format name from the 3rd column.
            format_name = row[2]

            # Checks if the script has already searched for this format in the standardize formats CSV. If it hasn't,
            # searches for the format and records the result in the formats_checked dictionary.
            if format_name not in formats_checked:
                present = in_standard(standard_csv, format_name)
                formats_checked[format_name] = present

# Makes a list of formats that are not already in standardize_formats.csv (have a value of False in the dictionary).
new_formats = []
for key in formats_checked:
    if formats_checked[key] == "Missing":
        new_formats.append(key)

# Saves the new format names, if any, to a text file to use for updating the standardize formats CSV.
# Each format name is on its own line in the text file so it can be pasted into the CSV, one row per format.
if len(new_formats) > 0:
    with open('new_formats.txt', 'w') as new_file:
        for new_format_name in new_formats:
            new_file.write(f'{new_format_name}\n')
else:
    print('No new formats to add!')
