# Subtotal for AIPs is counting the same AIP many times.
# What do the numbers look like for format types if calculated by aip?

# Individual reports don't have type, so need to look up on the fly?

"""
Counts below are before and after deduplication with 10/26 data:



"""

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

# Reads the standardization csv, which need for mapping format name in the format report
with open(standard_csv, 'r') as standard:
    standard_read = csv.reader(standard)

    # Gets the data from each format report.
    for file in os.listdir(formats_report_folder):
        if file.startswith('file_formats'):
            print()
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

                    # Gets the type from the standardization spreadsheet.
                    # TODO: it isn't finding the types
                    format_type = 'NOT FOUND'
                    for standard_row in standard_read:
                        if row[2].lower() == standard_row[0].lower():
                            format_type = standard_row[2]

                    print(row[2], format_type)

                #     # Adds each aip to a dictionary with format type as the key and a list of aip ids as the value.
                #     for aip in aip_list:
                #         try:
                #             type_aip_id[row[4]].append(aip)
                #         except KeyError:
                #             type_aip_id[row[4]] = [aip]
                #
                # # Add pre-deduplication count to count dictionary.
                # for key, value in type_aip_id.items():
                #     type_aip_count[key] = [len(value)]
                #
                # # Changes each list in the dictionary to a set to remove duplicates.
                # for key, value in type_aip_id.items():
                #     type_aip_id[key] = set(value)
                #
                # # Add the post-deduplication count to count dictionary
                # for key, value in type_aip_id.items():
                #     type_aip_count[key].append(len(value))
                #
                # # Prints the results:
                # for key, value in type_aip_count.items():
                #     print(key, value)
