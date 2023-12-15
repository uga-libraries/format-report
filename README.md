# Digital Preservation Format Report

## Overview

Analyze format information from the UGA Libraries' digital preservation system (ARCHive),
across the entire system and for individual departments, to monitor them for preservation risks.

The format data is either generated by FITS or MediaInfo and is consistently formatted in a CSV by ARCHive.
Risk is added from the US National Archive's (NARA) digital preservation risk data.

The analysis is accomplished with a series of scripts:
- archive_reports.py: make spreadsheets with summaries of the entire ARCHive holdings
- department_reports.py: make spreadsheets with summaries by department (ARCHive group)
- fix_versions.py: update version numbers in CSV files that are incorrectly altered by being opened in Excel
- merge_format_reports.py: combine group format reports (CSVs) into one CSV and add additional data
- update_standardization.py: identify new formats, which require new standardization rules
 
## Getting Started

### Dependencies

- numpy (https://numpy.org/) - categorize data and work with blanks in unit tests
- pandas (https://pandas.pydata.org/) - edit and summarize CSV data

### Installation

Download the latest version of NARA's Digital Preservation Plan spreadsheet (CSV version) from the 
[U.S. National Archives Digital Preservation GitHub Repo](https://github.com/usnationalarchives/digital-preservation).

From ARCHive, download every group's file format report, and the usage report (start of ARCHive - present),
and save all of them to a single folder. This is the report_folder that is an argument for most scripts. 

### Script Arguments

All script arguments are required.

archive_reports.py
- report_folder : the path to the folder which contains ARCHive's group file format reports, 
  the combined format reports made by the merge_format_reports.py script, and usage report (all CSVs)

department_reports.py
- current_formats_csv : the path to the "archive_formats_by_aip.csv" made by the merge_format_reports.py script 
  with data for the current year's analysis.
- previous_formats_csv: the path to the "archive_formats_by_aip.csv" made by the merge_format_reports.py script 
  with data from the previous year's analysis, to use for calculating the change in risk.

fix_version.py
- csv_path : the path to one of the combined format reports made by the merge_format_reports.py script (CSV)

merge_format_reports.py 
- report_folder : the path to the folder which contains ARCHive's group file format reports and usage report (all CSVs) 
- nara_csv : the path to NARA's Digital Preservation Plan spreadsheet (CSV)

update_standardization.py 
- report_folder : the path to the folder which contains ARCHive's group file format reports and usage report (all CSVs)



## Workflow
 
1. Download the format reports for each of the groups and the usage report (start of ARCHive - present) 
   from the digital preservation system (ARCHive). 
   Save the files to a single folder (report_folder).

 
2. Run the update standardization script to identify any formats that are not in the standardize_formats.csv, 
   which is used to add format types and format standardized names to the format data to allow 
   for easier analysis of trends.
 

3. If any new formats are found, the update standardization script produces a file called new_formats.txt. 
   Using the standardization guidelines, add the new formats to the standardize_formats.csv. 


3. Run the merge format reports script to make two versions of CSVs that combine format information 
   from all the group format reports and adds standardized information and NARA risk information. 
   One CSV is organized by group and then by format. The other csv is organized by AIP and then by format.    

 
4. Review the results of matching the format identifications to the NARA risk spreadsheet. 
   Remove extra matches, such as every version in NARA matching a singular format identification.
   Try to match additional format identifications to NARA.


5. Run the reports.py script to make an Excel workbook with analysis of the format data.


6. Run the department_reports.py script to make an Excel workbook with analysis of each department's format data.
   Can skip step 5 to only generate department reports.

       
