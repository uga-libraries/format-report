"""
Summarizing the current holdings of ARCHive, total and by group:
    *How many collections?
    *How many aips?
    *How many TB? 
"""

import csv
import datetime
import os
import pandas as pd
import re
import sys

from csv_merge import collection_from_aip

#Variables
report_folder = 'H:/ARCHive-formats/capacity-test'
today = datetime.datetime.now().strftime("%Y-%m-%d")

os.chdir(report_folder)


def aip_list(report_info):
    
    aip_list = []
    
    next(report_info)
    
    for row in report_info:
        aips = row[7].split('|')
        for aip in aips:
            if aip not in aip_list:
                aip_list.append(aip)
                
    return aip_list

# Increase size of csv fields to handle long aip lists.
# Gets the maximum size that doesn't give an overflow error.
while True:
    try:
        csv.field_size_limit(sys.maxsize)
        break
    except OverflowError:
        sys.maxsize = int(sys.maxsize/10)


# Make a file for results named archive_summary_date.csv.
# Get each row from each report, update it, and save to the results file.
with open(f'archive_aiplist_{today}.csv', 'w', newline='') as aiplist:
    aiplistcsv = csv.writer(aiplist)
    
    # Add a header to the aiplist file.
    aiplistcsv.writerow(['Group', 'Collection', 'AIP'])

    #Get each report
    for report in os.listdir(report_folder):
    
        #Get aip list from each format report and transform
        if report.startswith('file_formats'):
            
            # Get ARCHive group from the filename.
            regex = re.match('file_formats_\d{8}_(.*).txt', report)
            archive_group = regex.group(1)

            # Get data from the report.
            report_open = open(report, 'r')
            report_info = csv.reader(report_open, delimiter='\t')
        
            # Get a list of unique aip ids and write to the results file.
            aips = aip_list(report_info)
            for aip in aips:
                collection = collection_from_aip(aip, archive_group)                
                aiplistcsv.writerow([archive_group,collection,aip])
                
            report_open.close()
        
        #Ignore anything else in this folder
        else:
            continue
 
#NOPE - permission denied to the aiplist   
##Read the data from the csv.
#df = pd.read_csv(f'archive_aiplist{today}.csv')
#
##Format type.
#aip_totals = df.groupby('Group').count()
#aip_totals.to_csv(f'aip_total.csv')
