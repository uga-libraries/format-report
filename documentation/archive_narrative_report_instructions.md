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

- Bar Graph
  - Always include a title
  - Include x-axis and/or y-axis labels if it is not clear from other data
  - Include data labels
  - Widen the graph so that the text stays horizontal (rather than angling)
  - Widen the bars by decrease gap width to 75%

- Pie Chart
   - If they fit, use Quick Layout 1 to add value and percentage data labels.
   - If labels don't fit, use a legend on the left.
   - Reduce the space between the pie and the legend.
   - If there are multiple pie charts with the same legend, only have the legend on the first one.
   - Adjust the colors if there is not enough contrast.
   - Crop the image after pasting charts into the narrative report to remove extra white space. 

- Table
  - Header row or column is bold and fill with a light color.
  - Resize column widths to be relatively even, but it is ok to have some a little wider to limit text wrapping.
  - Title in bold and centered over the table to explain what it is

## Analysis

In addition to the section-specific instructions below,
review the entire report for any contextual information that has changed.

### Report Summary

There are no visuals in this section.
Update the statistics and common format information within the paragraphs using the data sources listed below,
and use the previous analysis report to evaluate the change since last time.

- Number of TB and files in ARCHive: "Group_Overview" in Frequency spreadsheet
- Most common format types: "Format_Types" in Frequency spreadsheet
- Most common format standardized names: "Format_Names" in Frequency spreadsheet
- Formats at high risk: Department reports

### Background and Method

There are no visuals in this section.
Update the number of types and standardized names from the standardize_formats.csv

### ARCHive Overview

Make the table.

1. Copy the data from "Group_Overview" in the Frequency spreadsheet.
2. Delete the Size_GB_Inflated column.
3. Remove the underscores in the column names.
4. Give the first row (column names) a blue background.
5. Put outlines around all cells.
6. Add a blank row before the total row.
7. Resize columns to a width of 0.9" and then adjust if needed to fit.
8. Reformat the numbers to use commas.

Make the pie charts. For all three, use data from "Group_Overview" in the Frequency spreadsheet.

1. Highlight the Group and AIPs columns (skipping the "total" row) and insert a pie chart.
2. Highlight the Group and Size_TB columns (skipping the "total" row) and insert a pie chart.
3. Highlight the Group and Files (skipping the "total" row) and insert a pie chart.
4. Reformat the pie charts following the Formatting Guide (above).
5. Paste the pie charts into the report.

Update the statistics within the narrative portion of the text and compare to the previous analysis report.

### Format Type

Use data from "Format_Types" in the Frequency spreadsheet.

1. Make a table in the report with 6 columns and 4 rows.
2. In the first column, put "Collections", "AIPs", "Files", and "Size".
3. In Format_Types, for each of the frequency measures (Collections, AIPs, Files, Size_GB):
   1. Sort the column in Format_Types largest to smallest.
   2. Put the five most frequent types in the row for that frequency measure.
   3. Add the count in parentheses after each type in the table. For size, convert to TB if over 1,000 GB.
   
Also update the number and list of format types, from standardize_formats.csv,
summarize the most common types based on all the measures,
and compare the results to the previous analysis report.

### Format Standardized Name

Use data from "Format_Names" in the Frequency spreadsheet to make the table.

1. Make a table in the report with 6 columns and 4 rows.
2. In the first column, put "Collections", "AIPs", "Files", and "Size".
3. In Format_Names, for each of the frequency measures (Collections, AIPs, Files, Size_GB):
   1. Sort the column in Format_Names largest to smallest.
   2. Put the five most frequent names in the row for that frequency measure.
   3. Add the count in parentheses after each name in the table. For size, convert to TB if over 1,000 GB.
   
Also update the number of format standardized names, from standardize_formats.csv,
summarize the most common names based on all the measures,
and compare the results to the previous analysis report.

Make the graphs.

1. Highlight the data in "Format_Name_Ranges" in the Ranges spreadsheet and insert a Clustered Column graph.
2. Rename the title to "Number of Files per Standardized Format Name".
3. Repeat steps 1-2 using "Format_Name_Sizes" and the title "Size per Standardized Format Name".
4. Reformat the graphs following the Formatting Guide (above).

Also update the number and percentage of formats with less than 10 files or 10 GB,
which is the smallest range in "Format_Name_Ranges" and "Format_Size_Ranges".
To calculate the percentage, use the total number of format standardized names from the intro of this section.

### Format Identification by File Count

Make the graph.

1. Highlight the data in "Format_ID_Ranges" in the Ranges spreadsheet and insert a Clustered Column graph.
2. Rename the title to "Number of Files per Unique Format".
3. Reformat following the Formatting Guide (above).

Also update the total number of format identification in ARCHive currently, from "Group_Overview" in the Frequency spreadsheet,
and the number from the previous analysis report.

Make the table.

1. Use the data in "Format_IDs" in the Frequency spreadsheet.
2. If it isn't already, sort the column Files largest to smallest.
3. Decide on the smallest number to include. Aim for 10 or fewer formats, and a number where there is a bigger gap between it and the next smallest 
   compared to the gaps between the larger numbers. It was 70,000 in 2021 and 2023.
4. Copy the Format_Identification and Files columns to the report, leaving them sorted by Files.
5. Replace the first pipe with " version " and the second with ", PUID ". Delete "NO VALUE".

Also update the number and percentage of format identifications that appear fewer than 10 times,
which is the smallest range in "Format_ID_Ranges", and compare the results to the previous analysis report.
To get the percentage, divide the number in that range by the sum of the total column, multiply by 100, and round to a whole number.

### Format Identification by Size

Make the graph.

1. Highlight the data in "Format_ID_Sizes" in the Ranges spreadsheet and insert a Clustered Column graph.
2. Rename the title to "Size per Unique Format".
3. Reformat following the Formatting Guide (above).

Also update the number and percentage of format identifications that have fewer than 10 GB, which is the smallest range in "Format_ID_Sizes", 
and the number and percentage with more than 10 TB, which combines the two largest ranges in "Format_ID_Sizes".
To get the percentage, divide the number in that range by the sum of the total column, multiply by 100, and round to a whole number.

Make the table.

1. Use the data in "Format_IDs" in the Frequency spreadsheet.
2. Sort the column Size_GB largest to smallest.
3. Copy the Format_Identification and Size_GB columns to the report, leaving them sorted by Size_GB.
4. Replace the first pipe with " version " and the second with ", PUID ". Delete "NO VALUE".

### Group Overlap

Make the pie charts. Use the data in each of the three tabs in the Group-Overlap spreadsheet to make a different pie chart.

1. Make a unique list of the values in the Groups column.
2. Use countif to calculate the number of times each Group value is present and paste as values.
3. Sort the number of groups from smallest to largest.
4. Replace the number of groups with words (e.g., One instead of 1).
5. Highlight the resulting table and insert a pie chart.
6. Reformat following the Formatting Guide (above).

Also update the number and percentage held by two or more groups.

### Format Risk

TBD: update now that all formats have risk and there are additional summaries.

Make pie charts of the risk based on the number of files, size, and formats ("ARCHive_Risk_Overview" in the Risk spreadsheet).
Make a bar graph of the risk from previous year(s) compared to now. Decide on which measure; do not do all three.
Do something with if NARA recommends to transform or retain?
Do something with which types are the most at risk?
Summarize the formats that are high risk.
Summarize the formats that did not match.
Summarize the formats with increased risk.

Also update the percentage of formats at each NARA risk level and compare the results to the previous analysis report.