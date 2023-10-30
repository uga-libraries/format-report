# Instructions for creating a department report

## Overview and Purpose

Create a summary and visualizations of the department's format data, prioritizing risk information.
It orients the department to the information in the spreadsheet and highlights areas of higher risk. 
The spreadsheet is created using ARCHive format data and the department_reports.py script.


## Analysis

Use Excel and the data from the department report spreadsheet to make graphs of the data. 
In some cases, the data must be summarized further.
Use the example department report as a template for the new report.

### Overview

Update the date with the date that the ARCHive format report was downloaded for this analysis.

Calculate the number of collections: TBD  
Calculate the number of AIPs: TBD  
Calculate the number of format versions: TBD  
Calculate the number of formats: TBD  
Calculate the range of versions for individual formats: TBD

### Risk Profile

A pie chart with the percentage of formats at each risk level for the entire department.
1. Make a copy of the Department Risk Levels sheet.
2. Remove the percentage from the risk column labels.
3. Highlight the four risk level column labels and data row.
4. Insert a pie chart.
5. Change the chart title to "Format Risk Profile"
6. Use the quick layout (under Design) of percentage in slice and TOC on right

### Risk Change

A bar chart with the number of formats at each risk level from the previous analysis and current analysis, 
and the number of formats only present in one of the two analyses.
1. Copy the Department Risk Levels sheet from this analysis and the previous analysis. How should this look??? Where to get new format info???
2. Remove the percentage from the risk column labels.
3. Highlight ????
4. Insert a clustered column chart.
5. Change the chart title to "Format Risk Profile Change".
6. Use Quick Layout 2.


### Risk by Collection

A bar chart with the percentage of each collection's formats at each risk level.
1. Make a copy of the Collection Risk Levels sheet.
2. Remove the percentage from the risk column labels.
3. Highlight the four risk level column labels and data rows.
4. Insert a stacked column chart.
5. Change the chart title to "Risk by Collection"

### AIP Format Variation

A histogram with the number of AIPs with the same number of formats.  
1. From AIP Risk Data, copy the AIP, Format_Name, and Format_Version columns.
2. Remove duplicates across all three columns.
3. Sort by AIP. Is this necessary???
4. Insert a pivot table with AIP as ROWS and Count of AIP as VALUES.
5. Copy the pivot table and paste the values to be able to use as input for the histogram.
6. Rename Row Labels to AIP ID and Count of AIP to Number of Formats.
7. Sort Number of Formats, smallest to largest.
8. Highlight the AIP ID and Number of Formats column labels and data rows.
9. Insert a histogram (under Statistics Chart)
10. Change the bin size
    1. Click on chart and then the Plus to get “Chart Elements” 
    2. Highlight axes to make the arrow appear 
    3. Click on the arrow arrow and then More Axis Options 
    4. Click on the bar chart icon and click Axis Options to get the Bins list 
    5. Select a Bin width of a small number (2 or 3)
11. Also in the Chart Elements, check data lebels to get counts per bing.
12. Change the chart title to "Number of formats in an AIP"


Also update the numbers in the second paragraph:
* The total number of AIPs
* The number and percentage of AIPs in the lowest bin
* The number and percentage of AIPs in the highest bins (long tail) 
* The highest number of formats in an AIP