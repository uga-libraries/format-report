 # ARCHive Format Analysis Workflow
 
## Overview and Purpose

The Head of Digital Stewardship analyzes the formats in ARCHive every two years 
to monitor for preservation risks based on format.
The data is summarized across all our holdings and, starting in 2023, for each department.
The [NARA Digital Preservation Plan spreadsheet](https://github.com/usnationalarchives/digital-preservation) 
is used to assign risks to our formats.

## Data Gathering

Data is exported from ARCHive on or around November 1, at a time that no new content is being ingested into the system.

1. Create a folder in DCWG Teams [ARCHive > Format Analysis] named with the year for all documentation.
With the analysis year folder, make a folder named archive_reports_YYYY-MM-DD for the data.


2. From the Reports page in the ARCHive interface, download the File Formats report for every group,
except for Emory and Test AIP Group, and save them to the archive_reports folder.
It can take a long time to download, with DLG requiring multiple hours.


3. From the Reports page in the ARCHive interface, download the Usage report and save it to the archive_reports folder.
   - For the Start Date, click "Set to ARCHive start date"
   - For the End Date, use the date the file format reports were downloaded


4. From [NARA's GitHub](https://github.com/usnationalarchives/digital-preservation), 
download the CSV version of the most recent Digital_Preservation_Plan_Spreadsheet
and save it to the folder for this year's Format Analysis (but not in archive_reports). 


5. Download a copy of all the data to your local machine to run the scripts for the next steps.

## Format Standardization

In this step, find new formats since the last analysis and add them to the standardization spreadsheet.

Each format in ARCHive is assigned a format type and format name to better reveal trends.
Format type is based on MIME type and format name is based on PRONOM, with local rules to make them more useful.

1. Run the update_standardization.py script to generate a report (new_formats.txt) of formats that do not have standardization rules.
The script has one argument, report_folder, which is the path to archive_reports on your local machine.


2. Copy the contents of new_formats.txt to the Format_Name column of standardize_formats.csv in this repo.


3. Use the [guidelines for standardizing formats](standardize_formats_guidelines.md) to assign a type and name to each format
and record that in the appropriate columns of standardize_formats.csv.


4. Open standardize_formats.csv in a spreadsheet program and sort alphabetically by Format_Name.

## Combine Department Data

In this step, combine format data from all the ARCHive groups into one spreadsheet,
and add collections, standardized format type and name, and NARA preservation information.

1. Run the merge_format_reports.py script to generate two spreadsheets with combined format data.
The script has two arguments, report_folder, which is the path to archive_reports,
and nara_csv, which is the path to NARA's Digital Preservation Plan Spreadsheet. Script outputs:
   - archive_formats_by_aip_YYYYMM.csv has collection information
   - archive_formats_by_group_YYYYMM.csv has file counts and size in GB
   - Both reports have format information and NARA preservation information.


2. Review the NARA matches. 
If there were multiple possible matches to a single format, delete ones that do match as well.
If there was no automatic match to NARA due to differences in spelling and abbreviations, add the match.
When adding a match, in the NARA_Match_Type column use the same categories as the script but add (Manual) to the end.


3. Save a copy of both spreadsheets to the Format Analysis folder in Teams for this year.

## Create ARCHive Reports
 
## Create Department Reports
