# Calculate the number of unique AIPs per format type and format standardized name. Because of how the data is
# normalized, the same AIP is counted multiple times if the counts in the archive formats csv are used, resulting in
# very inflated numbers. Numbers can be 2x bigger or more, with differences of 10,000+ at times.

# Usage: python /path/aip_analysis.py /path/archive_formats_csv

import csv
import os
import sys

standard_csv = "C:/users/amhan/Documents/GitHub/format-report/standardize_formats.csv"
formats_report_folder = "C:/users/amhan/Documents/GitHub/format-report/testing/2020-10-26_prod"

os.chdir(formats_report_folder)

type_aip_id = {}
type_aip_count = {}

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
        print(file)
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
                            format_type = standard_row[2]

                # Adds each aip to a dictionary with format type as the key and a list of aip ids as the value.
                for aip in aip_list:
                    try:
                        type_aip_id[format_type].append(aip)
                    except KeyError:
                        type_aip_id[format_type] = [aip]

# Add pre-deduplication count to count dictionary.
for key, value in type_aip_id.items():
    type_aip_count[key] = [len(value)]

# Changes each list in the dictionary to a set to remove duplicates.
for key, value in type_aip_id.items():
    type_aip_id[key] = set(value)

# Add the post-deduplication count to count dictionary
for key, value in type_aip_id.items():
    type_aip_count[key].append(len(value))

# Prints the results:
for key, value in type_aip_count.items():
    print(key, value)
