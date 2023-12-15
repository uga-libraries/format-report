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

### Testing

There are unit tests for all functions of each script, and for running each of the scripts in their entirety.

Tests use files stored in the repository for input data, so these need to be updated to sync with changes
to the NARA Digital Preservation Plan spreadsheet, or the output of merge_format_reports.py, 
which is used as input for other scripts. 

## Workflow
 
For the full analysis, use the [ARCHive reports workflow](documentation/archive_reports_workflow.md).

To generate a report for a specific department, use the 
[department report workflow](documentation/department_reports_workflow.md).

## Author

Adriane Hanson - Head of Digital Stewardship at the University of Georgia Libraries

## History

The first analysis was in 2020. 
It was repeated in 2021, but since there was not much change we adjusted the schedule to every two years. 
In both years, risk was evaluated by manually comparing the most common standardized format names to the
NARA Digital Preservation Plan spreadsheet and only the ARCHive reports were created.

The third analysis was in 2023. The comparison to the NARA spreadsheet was partially automated, 
allowing us to compare every format version to NARA, and the department reports were added.
This gives us more nuanced, actionable risk data.
