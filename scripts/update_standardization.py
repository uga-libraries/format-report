"""Makes a list of any formats from the ARCHive reports that aren't in standardize_formats.csv. These formats need to
be added to standardize_formats.csv before merging the reports.

Usage: python /path/update_standardization /path/reports"""

import csv
import os
import sys

# Variables
#    report_folder is the directory with the ARCHive format reports to be analyzed.
#    standardize_csv has the path to the csv document with current standardization rules.
#    new_formats stores the formats which need to be added to standardize_formats.csv
report_folder = sys.argv[1]
standard_csv = 'H:/ARCHive-formats/standardize_formats.csv'
new_formats = []

# Makes the report folder the current directory.
os.chdir(report_folder)


def in_standard(standard_csv, format):
    """Search for a format name in the column with format names.
       Return True if there is a match and False if there is not."""
       
    # Variable to track if the format is found.
    format_match = False
            
    # Reads the csv file with the standardization rules.
    with open(standard_csv) as standard:
        read_standard = csv.reader(standard)
        
        # Checks each row in the normalization list csv file.
        for row in read_standard:
            
            # If the format name is in the csv, updates the format_match variable and stops searching for that format.
            # Matching lowercase versions of the format names to account for variations in capitalization. 
            if format.lower() == row[0].lower():
                format_match = True
                break
    
    # Returns the matching result, True or False.
    return format_match


# Increases the size of csv fields to handle long AIP lists.
# Gets the smallest maximum size that doesn't give an overflow error.
while True:
    try:
        csv.field_size_limit(sys.maxsize)
        break
    except OverflowError:
        sys.maxsize = int(sys.maxsize/10)
        

# Gets each format report in the format folder.
for format_report in os.listdir(report_folder):
    
    # Skips if the document is not a format report.
    if not format_report.startswith('file_formats_'):
        continue
    
    # Reads the data from the report, which is a tab delimited file.
    with open(format_report) as formats:
        read_formats = csv.reader(formats, delimiter='\t')
        
        # Skips the header row.
        next(read_formats)
            
        # Iterates over every row in the file.
        for row in read_formats:
            
            # Gets the format name from the 3rd column.
            format = row[2]
            
            # Makes a unique list of formats that are not already in standardize_formats.csv.
            present = in_standard(standard_csv, format)
            if present == False and format not in new_formats:
                new_formats.append(format)


# Writes the new format names, if any, to a text file to use for updating standardize_formats.csv.
# Each format name is on its own line so it can be pasted into the csv, one row per format.
if len(new_formats) > 0:
    with open('new_formats.txt', 'w') as newfile:
        for format in new_formats:
            newfile.write(f'{format}\n')
else:
    print('No new formats to add!')