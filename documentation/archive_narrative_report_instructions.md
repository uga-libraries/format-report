# Instructions for creating the ARCHive narrative report

## Overview and Purpose

Create a summary and visualizations of ARCHive format data.
It provides DCWG with an overview of our holdings and is a record of change to our holdings over time.
It is supplemented by department-specific reports with more detail. 

## Data Source

Use Excel and the data from the ARCHive Format Analysis spreadsheets to make charts and graphs of the data. 
Use the previous analysis' report as a template for the new report.

The spreadsheets will be in the Teams folder for this year's Format Analysis, in the "ARCHive Format Reports" folder. 
Save the narrative report here as well. 

## Formatting Guide

In all visualizations, use these guidelines for a more readable result.

- Titles
   - Bold
   - Black
   - Move the box closer to the image if there is too much white space.
   
- Font
   - Size 11
   - Black (if on white background) or white (if on a colored background)

- Crop the image after pasting it into the narrative report to remove extra white space. 

## Analysis

In addition to the section-specific instructions below,
review the entire report for any contextual information that has changed.

### Report Summary

There are no visuals in this section.
Update the statistics and common format information within the paragraphs using the data sources listed below,
and use the previous analysis report to evaluate the change since last time.

- Number of TB and file format ids in ARCHive: "Group_Overview" in Frequency spreadsheet
- Most common format types: "Format_Types" in Frequency spreadsheet
- Most common format standardized names: "Format_Names" in Frequency spreadsheet
- Formats at high risk: TBD [currently only in the Department reports]

### Background and Method

There are no visuals in this section.
Update the number of types and standardized names from the standardize_formats.csv

### ARCHive Overview

Make the table.

1. Copy the data from "Group_Overview" in the Frequency spreadsheet.
2. Delete the Size_GB_Inflated column.
3. Remove the underscores in the column names.
4. Give the first row (column  names) a blue background.
5. Put outlines around all cells.
6. Add a blank row before the total row.
7. Resize columns to fit.

Make the pie charts. For all three, use data from "Group_Overview" in the Frequency spreadsheet.

1. Highlight the Group and AIPs columns (skipping the "total" row) and insert a pie chart.
2. Highlight the Group and Size_TB columns (skipping the "total" row) and insert a pie chart.
3. Highlight the Group and Format_Identifications (skipping the "total" row) and insert a pie chart.
4. Reformat the pie charts following the Formatting Guide (above).
5. Paste the pie charts into the report.

Update the statistics within the narrative portion of the text and compare to the previous analysis report.

### Format Type

Use data from "Format_Types" in the Frequency spreadsheet.

1. Make a table in the report with 6 columns and 4 rows.
2. In the first column, put "Collections", "AIPs", "File IDs", and "Size".
3. In Format_Types, for each of the frequency measures (Collections, AIPs, File_IDs, Size_GB):
   1. Sort the column in Format_Types largest to smallest.
   2. Put the five most frequent types in the row for that frequency measure.
   3. Add the count in parentheses after each type in the table.
   
Also update the number and list of format types, from standardize_formats.csv,
summarize the most common types based on all the measures,
and compare the results to the previous analysis report.

