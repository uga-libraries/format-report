# Calculate the number of unique AIPs per format type and format standardized name. Because of how the data is
# normalized, the same AIP is counted multiple times if the counts in the archive formats csv are used, resulting in
# very inflated numbers. Numbers can be 2x bigger or more, with differences of 10,000+ at times.

# Usage: python /path/aip_analysis.py /path/archive_formats_csv

import csv
import os
import sys

# Gets the file paths for the report folder and the csv with the standardization rules from the script arguments.
# If either are missing, prints an error and quits the script.
try:
    standard_csv = sys.argv[1]
    formats_report_folder = sys.argv[2]
except IndexError:
    print("One or both of the required script arguments is missing: standardized csv and formats report folder.")
    exit()

# standard_csv = "C:/users/amhan/Documents/GitHub/format-report/standardize_formats.csv"
# formats_report_folder = "C:/users/amhan/Documents/GitHub/format-report/testing/2020-10-26_prod"
# If the provided path to the standardized csv does not exist, prints an error and quits the script.
if not os.path.exists(standard_csv):
    print("The provided standardized csv is not a valid path.")
    exit()

# Changes the current directory to the reports folder. If it does not exist, prints an error and quits the script.
try:
    os.chdir(formats_report_folder)
except FileNotFoundError:
    print("The provided formats report folder is not a valid path.")
    exit()

# Starts dictionaries for storing the results.
type_count = {}
name_count = {}

# Increases the size of csv fields to handle long aip lists.
# Gets the maximum size that doesn't give an overflow error.
while True:
    try:
        csv.field_size_limit(sys.maxsize)
        break
    except OverflowError:
        sys.maxsize = int(sys.maxsize / 10)

# Gets the data from each format report.
for file in os.listdir(formats_report_folder):
    if file.startswith('file_formats'):
        with open(file, 'r') as formats:
            formats_read = csv.reader(formats)

            # Skips the header row.
            next(formats_read)

            # Gets the data from each row in the report, which has information about a single format for that group.
            # row[2] is format name.
            # row[7] is aip ids (a pipe separated string).
            for row in formats_read:

                # Format the aips as a list.
                # I don't think I have to dedup russell, since each aip id is only formatted with a dash or without.
                aip_list = row[7].split('|')

                # Gets the type from the standardization spreadsheet. Open csv here or only accessed in first loop.
                format_type = 'NOT FOUND'
                with open(standard_csv, 'r') as standard:
                    standard_read = csv.reader(standard)
                    for standard_row in standard_read:
                        if row[2].lower() == standard_row[0].lower():
                            standard_name = standard_row[1]
                            format_type = standard_row[2]

                # Adds each aip to a dictionary with format type as the key and a list of aip ids as the value.
                for aip in aip_list:
                    try:
                        type_count[format_type].append(aip)
                    except KeyError:
                        type_count[format_type] = [aip]

                # Adds each aip to a dictionary with format name as the key and a list of aip ids as the value.
                for aip in aip_list:
                    try:
                        name_count[standard_name].append(aip)
                    except KeyError:
                        name_count[standard_name] = [aip]

# Convert the list of collections in each dictionary to the count of unique collections.
# Making a set removes duplicates.
for key, value in type_count.items():
    type_count[key] = len(set(value))

for key, value in name_count.items():
    name_count[key] = len(set(value))

# TODO: save to a report instead
# Prints the results.

print("\nAll Format Types")
for key, value in type_count.items():
    print(key, value)

print("\nStandardized Format Names if over 500 AIPs")
for key, value in name_count.items():
    if value > 500:
        print(key, value)
