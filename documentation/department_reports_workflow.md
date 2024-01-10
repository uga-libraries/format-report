# Instructions for creating a department spreadsheet report

## Overview and Purpose

Typically, the Head of Digital Stewardship makes all department reports every three years,
as part of regularly monitoring the content in ARCHive for emerging risk.

These instructions use the same scripts to create a report for one department (or a subset of departments) at any time.
Some departments have content that is more prone to risk and may want to run the analysis more frequently.

## Workflow

1. Download the file format report(s) for the relevant department(s) from ARCHive.


2. Run the update_standardization.py script to check for new formats.
   The script has one argument, report_folder, which is the path to archive_reports on your local machine.


3. Add any new formats to standardize_formats.csv, using the [standardizing guidelines](standardize_formats_guidelines.md).


4. Run the merge_format_reports.py script to add the NARA risk data.
   The script has two arguments, report_folder, which is the path to the folder with the file format report(s), 
   and nara_csv, which is the path to NARA's Digital Preservation Plan Spreadsheet.


5. Use the [Match Guidelines](archive_nara_match_guidelines.md) to refine the NARA risk data in the "by_aip" report.


6. Get the "by_aip" report from a previous analysis and delete other departments if present.


7. Run the department_reports.py script to make the department spreadsheet report(s).
   The script has two arguments, current_formats_csv, which is the path to the by_aip merged report from this year,
   and previous_formats_csv, which is the path to the by_aip merged report from a previous year.


8. If desired, use the [department narrative report instructions](department_narrative_report_instructions.md)
   to summarize the data in the spreadsheet.