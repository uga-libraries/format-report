# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 15:54:06 2020

@author: hansona
"""

# Get format type and standardized format name from another csv file.
# Testing separately but will integrate into csv_merge.py

import csv

# Variables
formats = 'H:/ARCHive-formats/archive_formats_2020-02.csv'
standardization = 'H:/ARCHive-formats/standardize_formats.csv'


def standardize_formats(format, standard):
    """Find the format within the standardized formats csv.
    Return the standard format name and format type.
    Assumes there will be a match because update_normalized.py is run first."""
      
    #Read the standardized formats csv.
    with open(standard) as standard_list:
        read_standard_list = csv.reader(standard_list)
            
        #Skip the header.
        next(read_standard_list)
        
        #Check each row for the format. When there is a match, return the name and type.
        # Matching lowercase versions of the format names to account for variations in capitalization. 
        for row in read_standard_list:
            if format.lower() == row[0].lower():
                return row[0], row[1], row[2]


# =============================================================================
# This part is already in csv_merge.py except for calling the findNorm function.

# Read the format report csv
with open(formats) as format_list:
    read_format_list = csv.reader(format_list)
    
    # Skip the header
    next(read_format_list)
    
    # Get the format name from each row.    
    for row in read_format_list:
        formatName = row[4]
    
        # Get the format name (for testing to check accuracy), standardized name, and format type for that format.
        # Print the results to review.
        name, standard, formattype = standardize_formats(formatName, standardization)

        with open('scriptresult.txt', 'a') as result:
            result.write(f'{name}|{standard}|{formattype}\n')
    
    