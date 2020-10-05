# Combine format reports (tab delimited) for all groups with any files into a single csv.
# Add a column for group name and otherwise copy as is.

import csv
import datetime
import os
import re
import sys


# Variables
#    report_folder is the directory with the ARCHive format reports to be analyzed.
#    standardize_csv has the path to the csv document with current standardization rules.
#    today is the current date, formatted YYYYMM, for use in naming the result file.
#report_folder = sys.argv[1]
report_folder = 'H:/ARCHive-formats/2020-02-25'
standard_csv = 'H:/ARCHive-formats/standardize_formats.csv'
today = datetime.datetime.now().strftime("%Y-%m")

# Make current directory the report folder.
os.chdir(report_folder)

  
def collection_from_aip(aip, group):
    """Determine the collection id based on the aip id."""
    
    if group == 'bmac':
        
        if aip[5].isdigit():
            return 'peabody'
        
        #The next three address errors with how aip id was made.
        elif aip.startswith('har-ms'):
            regex = re.match('(^har-ms\d+)_', aip)
            return regex.group(1)
        
        elif aip.startswith('bmac_bmac_wsbn'):
            return 'wsbn'
        
        elif aip.startswith('bmac_wrdw_'):
            return 'wrdw-video'
        
        else:
            regex = re.match('^bmac_([a-z0-9-]+)_', aip)
            return regex.group(1)
    
    elif group == 'dlg':
        
        #Everything in turningpoint is also in another collection, which is the one we want.
        if aip.startswith('dlg_turningpoint'):
            
            #This one is from an error in the aip id.
            if aip == 'dlg_turningpoint_ahc0062f-001':
                return 'geh_ahc-mss820f'
            
            elif aip.startswith('dlg_turningpoint_ahc'):
                regex = re.match('dlg_turningpoint_ahc(\d{4})([a-z]?)-', aip)
                number = int(regex.group(1))
                if regex.group(2) == 'v':
                    return f'geh_ahc-vis{number}'
                else:
                    return f'geh_ahc-mss{number}{regex.group(2)}'
        
            elif aip.startswith('dlg_turningpoint_ghs'):
                regex = re.match('dlg_turningpoint_ghs(\d{4})([a-z]*)', aip)
                if regex.group(2) == 'bs':
                    return f'g-hi_ms{regex.group(1)}-bs'
                else:
                    return f'g-hi_ms{regex.group(1)}'
        
            elif aip.startswith('dlg_turningpoint_harg'):
                regex = re.match('dlg_turningpoint_harg(\d{4})([a-z]?)', aip)
                number = int(regex.group(1))
                return f'guan_ms{number}{regex.group(2)}'
        
            else:
                return 'turningpoint no match'
        
        elif aip.startswith('batch_gua_'):
            return 'dlg_ghn'
        
        else:
            regex = re.match('^([a-z0-9-]*_[a-z0-9-]*)_', aip)
            return regex.group(1)                

    elif group == 'dlg-hargrett':
        regex = re.match('^([a-z]{3,4}_[a-z0-9]{4})_', aip)
        return regex.group(1)
    
    elif group == 'hargrett':
        regex = re.match('^(.*)er', aip)
        return regex.group(1)
    
    elif group == 'russell':
        regex = re.match('^rbrl-?\d{3}', aip)
        return regex.group()
    
    else:
        return 'new group'  
    

def update_row(row, group):
    """Calculate and add new data, replace the aip list with a collection list, and fill in empty cells.
       New data is group name, collection count, standardized version of the format name, and format type."""  

    def collection_list(aip_list):
        """Change aip list to a unique list of collections.
           Return a string with comma-separated collection ids and a count of the number of collections."""
        
        #Split aip_list (a string) into a list. Items are divided by a pipe.
        aips = aip_list.split('|')
        
        colls = []
        
        #Extract collection id from aip id.
        #Put in error message if the pattern is new so it can be fixed.
        for aip in aips:
            try:
                coll = collection_from_aip(aip, group)
            except AttributeError:
                print('Check for collection errors in merged csv')
                coll = f"Collection not calculated for {aip}"
            
            #Make a unique list of collections.
            if coll not in colls:
                colls.append(coll)
    
        #Convert the list of collections to a string with each collection separated by a comma.
        collections =  ', '.join(map(str, colls))
        
        #Return both the string with the collections and a count of the number of collections.
        return collections, len(colls)


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
                    return row[1], row[2]
    
    #Get standard name for format and format type.
    format_standard, format_type = standardize_formats(row[2], standard_csv)
    
    #Get list of collections from the aip ids and 
    collections, number_collections = collection_list(row[7])
    
    #Replace the aip list with the collection list.
    row[7] = collections  
    
    #Add the group and number of collections at the beginning of the row.
    #Add the format type and standardized format name before the format name.
    row.insert(0, group)
    row.insert(1, number_collections)
    row.insert(4, format_type)
    row.insert(5, format_standard)
       
    #Fill all empty cells with 'NO VALUE'
    row = ['NO VALUE' if x=='' else x for x in row]

    #Return the updated version of the row.
    return row


# Increase size of csv fields to handle long aip lists.
# Gets the maximum size that doesn't give an overflow error.
while True:
    try:
        csv.field_size_limit(sys.maxsize)
        break
    except OverflowError:
        sys.maxsize = int(sys.maxsize/10)



# Make a file for results named archive_formats_date.csv.
# Get each row from each report, update it, and save to the results file.
with open(f'archive_formats_{today}.csv', 'w', newline='') as result:
    resultcsv = csv.writer(result)
    
    # Add a header to the results file.
    resultcsv.writerow(['Group', 'Collection_Count', 'AIP_Count', 'File_Count', 'Format_Type', 'Format_Standard_Name', 'Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'Format_Note', 'Collection_List'])
    
    for report in os.listdir():
        
        # Skip if it is the results file. Should not process itself.
        if report == f'archive_formats_{today}.csv':
            continue
        
        # Get ARCHive group from the filename.
        regex = re.match('file_formats_\d{8}_(.*).txt', report)
        archive_group = regex.group(1)

        # Get data from the report.
        report_info = csv.reader(open(report, 'r'), delimiter='\t')
        
        # Skip the header.
        next(report_info)
        
        # Get data from each row in the report.
        for row in report_info:
            
            # Update the row to add additional information and fill in blank cells.
            # Save to the results csv.
            newrow = update_row(row, archive_group)
            resultcsv.writerow(newrow)