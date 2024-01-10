# ARCHive to NARA Risk Match Refinement Guidelines

## Overview

The merge_format_reports.py script attempts to automatically match our format identifications to NARA's risk spreadsheet.
This is fairly effective for format ids with PRONOM IDs, but rarely matches otherwise due to format name variations.
Use these guidelines to get as many matches to NARA as possible.

First update the by_group version of the CSV, and then copy the information to the by_aip version of the CSV.
We expect to automate the updating of by_aip in the future (Issue 65).
Open the CSVs in Excel to use filtering and filling for making the updates, and then convert back to CSV.
Errors from Excel automatically formatting version numbers will be fixed in the next step of the workflow.

## Add New NARA Matches

Start with strategies for more confident matching, but ultimately get as many reasonable matches as possible.
It may be helpful to temporarily add a column to describe how the match is made, for improving the automated process,
but make the NARA_Match_Type "Manual" since the strategies overlap.

### Format IDs with PUID matched and without PUID did not

We have format identifications with the same name and version, but one has a PUID and one does not.
If the one with PUID matched NARA, the same match can be used for the one without the PUID.

To find, use conditional formatting to highlight duplicates in the Format_Name column, 
and look for some that are matched and some that are not.
Make sure the version number is matching what NARA has.

### Format IDs with multiple PUID

Use PRONOM to determine which PUID is correct, and then try to match to NARA with the correct PUID.

### Format Names

Alphabetize the format identifications by the Format_Standardized_Name column, which tends to match NARA best,
and scan through the NARA spreadsheet (also alphabetized by name) looking for matches.
There are often differences in how acronyms and version numbers are included,
but it is clear that they are the same format.

When possible, match exactly to the format version.
If NARA does not have the same format version, use the closest (oldest, if available) version in NARA
to give us an approximate risk value.

### Relying on previous work

These are a few past decisions for matching that can be repeated, for anything that has not matched yet at this stage.

* Match any kind of executable or source to NARA "executable"
* Match any ASCII, other than a source file, to NARA "ASCII"
* Match any icon to NARA "Icon file format"
* Match Adobe Flash to NARA "Macromedia Flash"
* Match MXF to Material Exchange Format
* Match NEF EXIF to "Nikon Electronic Format RAW Image (NEF)"

### Research Formats

Search the NARA spreadsheet, in case the term shows up in a description or other column.

Look at the previous analysis and see what we matched it to. 
Confirm that is still in NARA and still appears to be a good match.

Look up a format in PRONOM or do a Google search, 
which can give additional information (e.g., acronym, extension) to search for in the NARA spreadsheet.

## Remove Extra NARA Matches

Look for multiple possible NARA matches to the same format identification and remove extra ones.
This typically happens when there is more than one version of a format with the same PUID.

### Finding Extra Matches

Format ids are also duplicated in the spreadsheet from being in multiple ARCHive groups.
To find duplicates due to multiple NARA matches:

1. Use conditional formatting to highlight duplicates in the Format_Identification column.
2. Sort the Format_Identification column alphabetically.
3. Filter the NARA_Match_Type column to everything except "No NARA Match".
4. Scan down the spreadsheet looking for identical department, file count, size, and format id.

### Addressing Extra Matches

Guidance for narrowing:

* If the format id has no version, and it matched all versions in NARA, keep the match to unspecified version.
* If multiple format names have the same PRONOM ID, keep the match to the one closest to our format name.
* If multiple format versions have the same PRONOM ID, and our format id includes a version not in NARA, change to No NARA Match.
* If multiple format names match, and it isn't clear which is closest to our format name, 
  if NARA has a more generic option (Excel vs Excel for Windows), match to the generic option.

If a better match can be made, delete the extra rows 
and change the NARA_Match_Type to "Manual (Narrowed)" for the row(s) kept.
This needs to be done separately for each group that has the same format id.

There are also cases where multiple matches need to be kept, such as names which are too different to narrow down 
and cases where our format identification gives a range of versions and NARA lists each separately.

When doing this in the by_aip version of the CSV, need to delete once per AIP to make sure it is really duplication,
and not caused by being in multiple groups or AIPs. To streamline the process:

1. Filter for a single format identification that needs to be narrowed.
2. Confirm that each instance of the format identification is matching the same thing in NARA (generally true).
3. If NARA matches are the same, filter for all the versions to delete and delete the rows at once.
4. Give the remaining matches the match type "Manual (Narrowed)"

## Quality Control

This process is a little prone to error, since the same format identification may be in multiple groups,
and also in the by_group and by_aip CSV.

Before copying the information to by_aip, confirm that it is correct in by_group.

1. Make a deduplicated list of Format_Identification and NARA_Risk_Level, 
   and make sure that there are no format ids with a different risk levels.
2. Compare the Format_Identification and NARA_Format_Name columns and look for any that don't make sense.
3. Filter for each NARA_Match_Type and look for any that don't make sense, like No NARA Match where there is one.

After copying the information to the by_aip CSV, confirm that it matches what is in by_group
by comparing a deduplicated list of the Format_Identification and NARA_Risk_Level in each CSV.