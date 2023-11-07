# Instructions for creating a department spreadsheet report

## Overview and Purpose

Typically, the Head of Digital Stewardship makes all department reports every two years,
as part of regularly monitoring the content in ARCHive for emerging risk.

These instructions use the same scripts to create a report for one department (or a subset of departments) at any time.
Some departments have content that is more prone to risk and may want to run the analysis more frequently.

## Workflow

1. Download the file format report(s) for the relevant department(s) from ARCHive.
2. Run the update_standardization.py script to check for new formats.
3. Add any new formats to standardize_formats.csv, using the [standardizing guidelines](standardize_formats_guidelines.md).
4. Run the merge_format_reports.py script to add the NARA risk data.
5. Add the "by_aip" report from a previous analysis (delete other departments if needed) to the same folder as the file format report(s) (step 1).
6. Run the department_reports.py script to make the department spreadsheet report(s).

If desired, use the [department narrative report instructions](department_narrative_report_instructions.md)
to summarize the data in the spreadsheet.