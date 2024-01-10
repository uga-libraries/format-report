# Instructions for creating the ARCHive narrative report

## Overview and Purpose

Create a summary and visualizations of ARCHive format data.
It provides DCWG with an overview of our holdings and is a record of change to our holdings over time.
It is supplemented by department-specific reports with more detail. 

## Data Source

Use Excel and the data from the ARCHive Format Analysis spreadsheets to make charts and graphs of the data. 
Use the previous analysis' report as a template for the new report.

The spreadsheets will be in the Teams folder for this year's Format Analysis, in the "ARCHive Format Report" folder. 
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

- Colors for Risk
  - No Match is blue
  - High Risk is dark red
  - Moderate Risk is orange
  - Low Risk is green

- Bar Graph
  - Always include a title
  - Include x-axis and/or y-axis labels if it is not clear from other data
  - Include data labels, unless it is by percentage
  - Widen the graph so that the text stays horizontal (rather than angling), if possible
  - Widen the bars by decrease gap width to 75%

- Pie Chart
   - If labels fit, use Quick Layout 1 to add value and percentage data labels.
   - If labels don't fit, use a legend on the left.
   - Reduce the space between the pie and the legend.
   - If there are multiple pie charts with the same legend, only have the legend on the first one
     and make them small enough to be side by side. 
     Very small wedges will not show and that is ok, since the goal is to see trends.
   - Adjust the colors if there is not enough contrast.
   - Crop the image after pasting charts into the narrative report to remove extra white space. 

- Table
  - Header row is bold and filled with blue.
  - Underscores are removed from the header row, if present.
  - Resize column widths to be relatively even, but it is ok to have some a little wider to limit text wrapping.
  - All cells are outlined.
  - Numbers have a comma if 1,000 or more.

## Analysis

In addition to the section-specific instructions below,
review the entire report for any contextual information that has changed.

### Report Summary

This summary should have all key points from the report, in case this is all that someone reads.

Update the statistics and common format information within the paragraphs using the data sources listed below,
update the links and dates, and use the previous analysis report to evaluate the change since last time.

- Number of TB and files in ARCHive: "Group_Overview" in Frequency spreadsheet.
- Most common format types: "Format_Types" in Frequency spreadsheet.
- Most common format standardized names: "Format_Names" in Frequency spreadsheet.
- Formats at high risk and not matched: "ARCHive_Risk_Overview" in Risk spreadsheet and department reports.
- Group overlap: Group Overlap spreadsheet.

### Background and Method

- Update the links and dates
- Update the number of types and standardized names from the standardize_formats.csv
- Update any changes in the data or the method

### ARCHive Overview

Update the number of groups with AIPs in ARCHive (excluding Emory and Test) 
and note any group ingesting for the first time since the last analysis.

Make the table.

1. Copy the data from "Group_Overview" in the Frequency spreadsheet.
2. Delete the Size_GB_Inflated column.
3. Remove the underscores in the column names.
4. Reformat the table following the Formatting Guide (above).
5. Add a blank row before the total row.

Make the pie charts. For all three, use data from "Group_Overview" in the Frequency spreadsheet.
Use them and the results from the previous analysis report to update the text above them.

1. Highlight the Group and AIPs columns (skipping the "total" row) and insert a pie chart.
2. Highlight the Group and Size_TB columns (skipping the "total" row) and insert a pie chart.
3. Highlight the Group and Files (skipping the "total" row) and insert a pie chart.
4. Reformat the pie charts following the Formatting Guide (above).
5. Paste the pie charts into the report. Start with a height of 2" to get them to fit next to each other.

### Format Risk

Update the text about the format risk analysis if anything has changed.

#### Risk in ARCHive

Make the pie charts, using the data in each of the three columns in "ARCHive_Risk_Overview" in the Risk spreadsheet,
and use them to update the text above them.

1. Highlight the NARA_Risk_Level column and one of the other three columns.
2. Insert a pie chart.
3. Update the title to Number of Files, Size (GB), or Format Identifications.
4. Reformat following the Formatting Guide (above).

Use "ARCHive_Risk_Overview" and "Format_Type_Risk" in the Risk spreadsheet to update the text below the charts.

#### Risk by Group

Make the graph using the data in "Department_Risk_Overview" in the Risk spreadsheet,
and then use it to update the text above it.

1. Highlight the data and insert a pivot table with Rows = Group, Columns = NARA_Risk_Level, 
   and Values = Sum of Format_Identifications. 
2. Copy and paste the values of the pivot table, so it can be edited.
3. Delete the total column and row, and move the High Risk column between Moderate and No Match to be in risk order.
4. Highlight the edited pivot table and insert a 100% stacked column graph.
5. Update the title to Percentage of Formats at NARA Risk Levels by Group.
6. Reformat following the Formatting Guide (above).

#### Risk by Format Type

Make the "Risk by Format Type" graph using the data in "Format_Type_Risk" in the Risk spreadsheet,
and then use it to update the text above it.

1. Highlight the data and insert a pivot table with Rows = Type, Columns = NARA_Risk_Level, 
   and Values = Sum of Format_Identifications. 
2. Copy and paste the values of the pivot table, so it can be edited.
3. Delete the total column and row, and move the High Risk column between Moderate and No Match to be in risk order.
4. Highlight the edited pivot table and insert a 100% stacked column graph.
5. Update the title to Percentage of Formats at NARA Risk Levels by Type.
6. Reformat following the Formatting Guide (above).

### Common Formats

#### Format Type

Make the table using the data from "Format_Types" in the Frequency spreadsheet,
and then use it and the previous analysis report to update the text above it.

1. Make a table in the report with 4 columns and 6 rows.
2. In the first row, put "Collections", "AIPs", "Files", and "Size".
3. For each of the four columns:
   1. Sort the column in Format_Types for that frequency measure (e.g., Collections) largest to smallest.
   2. Put the five most frequent types in the column for that frequency measure.
   3. Add the count in parentheses after each type in the table. For size, convert to TB if over 1,000 GB.
4. Reformat following the Formatting Guide (above).

#### Format Standardized Name 

Make the table using data from "Format_Names" in the Frequency spreadsheet,
and then use it and the previous analysis report to update the text above it.

1. Make a table in the report with 4 columns and 6 rows.
2. In the first row, put "Collections", "AIPs", "Files", and "Size".
3. For each of the four columns:
   1. Sort the column in Format_Names for that frequency measure (e.g., Collections) largest to smallest.
   2. Put the five most frequent names in the column for that frequency measure.
   3. Add the count in parentheses after each name in the table. For size, convert to TB if over 1,000 GB.
4. Reformat following the Formatting Guide (above).

Make the Number of per Standardized Format Name graph, and then use it to update the text above it.
To calculate the percentage, use the total number of format standardized names from the intro of this section.

1. Highlight the data in "Format_Name_Ranges" in the Ranges spreadsheet and insert a Clustered Column graph.
2. Rename the title to "Number of Files per Standardized Format Name".
3. Reformat following the Formatting Guide (above).

Make the Size per Standardized Format Name graph, and then use them to update the text above it.
To calculate the percentage, use the total number of format standardized names from the intro of this section.

1. Highlight the data in "Format_Name_Sizes" in the Ranges spreadsheet and insert a Clustered Column graph.
2. Rename the title to "Size per Standardized Format Name".
3. Reformat following the Formatting Guide (above).

#### Format Identifications

Update the first paragraph using the data in "Group_Overview" in the Frequency spreadsheet 
and the previous analysis report.

Make the table based on the size of files using the data in "Fomrat_IDs" in the Frequency spreadsheet,
and then use it and the previous analysis report to update the text above it.
To get the percentage, use total of the "Size (TB)" column made for this table.

1. Sort the column "Size_GB" largest to smallest.
2. Make a new column "Size (TB)" by dividing "Size_GB" by 1000.
3. Decide on the smallest number to include. Ain for 10 or fewer formats.
5. Copy the Format_Identification and Size (TB) columns to the report, leaving them sorted by size.
6. Replace the first pipe with " version " and the second with ", PUID ". Delete "NO VALUE".

Make the table based on number of files using the data in "Format_IDs" in the Frequency spreadsheet, 
and then use it and the previous analysis report to update the text above it. 
To get the percentage, use total of the "Files" column.

1. Sort the column "Files" largest to smallest.
2. Decide on the smallest number to include. Aim for 10 or fewer formats.
3. Copy the Format_Identification and Files columns to the report, leaving them sorted by files.
4. Replace the first pipe with " version " and the second with ", PUID ". Delete "NO VALUE".
5. Reformat following the Formatting Guide (above)

### Group Overlap

Update the link.

Make the pie charts using the data in each of the three tabs in the Group-Overlap spreadsheet,
and then use them and the data from the spreadsheet to update the text above them.

For each tab in the spreadsheet:

1. Make a unique list of the values in the Groups column.
2. Use countif to calculate the number of times each Group value is present and paste as values.
3. Sort the number of groups from smallest to largest.
4. Replace the number of groups with words (e.g., One instead of 1).
5. Highlight the resulting table and insert a pie chart.
6. Reformat following the Formatting Guide (above).

