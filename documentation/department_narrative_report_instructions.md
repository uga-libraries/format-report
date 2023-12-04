# Instructions for creating a department narrative report

## Overview and Purpose

Create a summary and visualizations of the department's format data, prioritizing risk information.
It orients the department to the information in the spreadsheet and highlights areas of higher risk. 

## Analysis

Use Excel and the data from the department report spreadsheet to make graphs of the data. 
In some cases, the data must be edited first.
Use the example department report as a template for the new report.
When pasting a graph into the report document, right click and choose either "Embed Workbook" option. 

### Overview

Update the date with the date that the ARCHive format report was downloaded for this analysis.

Use copies of columns from the AIP_Risk_Data sheet to calculate the overview stats:
- Number of collections: remove duplicates from the Collection column and get the row count.  
- Number of AIPs: remove duplicates from the AIP column and get the row count.
- Format counts 
  - Number of versions: remove duplicates from the Format_Name and Format_Version columns and get the row count.
  - Range of versions: sort the Format_Name column of the deduplicated list just created, 
    get the subtotal of counts of Format_Name, and find the lowest and highest subtotal.
  - Number of formats: remove duplicates from another copy of the Format_Name column and get the row count.  
    
### Risk Profile

A pie chart with the percentage of formats at each risk level for the entire department.
1. Make a copy of the Department_Risk_Levels sheet and remove any columns with 0%.
2. Remove the percentage from the risk column labels.
3. Highlight the four risk level column labels and data row.
4. Insert a pie chart.
5. Change the chart title to "Format Risk Profile" and make it bold.
6. Use Quick Layout 1 (under Design) to label each slice with the risk level and percentage.
7. Adjust labels. Use font size 11, label position center, font color white.
8. Adjust colors by clicking on each slice and changing fill. High = red, moderate = orange, low = green. 
   Leave no match blue.
9. Reduce the white space around the chart, adjusting the label boxes if text gets cut off. 

### Risk Change

A bar chart with the number of formats at each risk level from the previous analysis and current analysis.
1. Copy the Department_Risk_Levels sheet from this analysis.
2. Add the Department_Risk_Levels percentages from the previous analysis in the row above.
3. Remove the percentage from the risk column labels.
4. Convert the percentages to numbers (divide by 100, multiply by the number of formats, and round to a whole number).
5. Add a column with the year to the left of the risk columns. Do not give it a label.   
6. Highlight the year column, risk column labels and data rows.
7. Insert a clustered column chart.
8. Change the chart title to "Format Risk Change".
9. Use Quick Layout 2 (under Design) to label each bar with the percentage and add a legend.
10. Update the number of formats only in one analysis in the sentence above the chart.  
    1. Only in previous: the number of unique formats in AIP_Risk_Data with risk change of "Unmatched".  
    2. Only in current: the number of unique formats in AIP_Risk_Data with risk change of "New Format".

If there was no change, do not make the bar chart.
Instead, indicate there was no change in risk between the two years, and the number of formats at each risk level.
    
### Risk by Collection

A bar chart with the percentage of each collection's formats at each risk level.
1. Make a copy of the Collection_Risk_Levels sheet without the Formats column or any risk level not in any collection.
2. Remove the "Collection" column label, and the percent from the risk column labels.
3. Sort each risk column Largest to Smallest, starting with Low risk and working up to No Match,
   so the collections are in order from most to least risk.
4. Highlight the collection column, four risk level column labels and data rows.
5. Insert a 100% stacked column chart.
6. Change the chart title to "Risk by Collection" 
7. Change the colors to match Risk Profile (no stays blue, high = red, moderate = orange, low = green) 
   by clicking on any bar of that level and changing the fill. 
8. Delete the collection ids if there are too many for all bars to be labeled.

### AIP Format Variation

A histogram with the number of AIPs with the same number of formats.  
1. From AIP_Risk_Data, copy the AIP, Format_Name, and Format_Version columns.
2. Remove duplicates across all three columns.
4. Insert a pivot table with AIP as ROWS and Count of AIP as VALUES.
5. Copy the pivot table and paste the values to be able to use as input for the histogram.
6. Rename Row Labels to AIP ID and Count of AIP to Number of Formats.
7. Sort Number of Formats, smallest to largest.
8. Highlight the AIP ID and Number of Formats column labels and data rows.
9. Insert a histogram (under Statistics Chart)
10. Change the bin size
    1. Click on the chart and then the Plus to get “Chart Elements” 
    2. Mouse over Axes to make the arrow appear, click on it, and then click More Axis Options 
    3. Click on the bar chart icon and click Axis Options to get the Bins list 
    4. Select a Bin width of a small number (1-3)
11. Also in the Chart Elements, check data labels to get counts per bin.
12. Change the chart title to "Number of formats in an AIP"

If there is too little variation for the histogram to make sense 
(e.g., the 1 format column is so big that no others are visible), 
insert a table with the number of AIPs with each number of formats instead.

Also update the numbers in the second paragraph:
* The total number of AIPs
* The number and percentage of AIPs in the lowest bin
* The number and percentage of AIPs in the highest bins (long tail) 
* The highest number of formats in an AIP