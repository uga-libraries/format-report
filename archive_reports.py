"""Summarize the format data from ARCHive into four spreadsheets

The script uses information from three sources, all CSVs. The usage report is downloaded from ARCHive. Both archive
format archive_reports are made from the ARCHive group format archive_reports using the merge_format_reports script.
    * usage report: the amount ingested (AIP count and size) for each group and each user in a group.
    * archive_formats_by_aip report: Organized by AIP and format. Has group, collection, aip id, and format information.
    * archive_formats_by_group report: Organized by group and format. Has group, file_id count, and format information.

Definition of terms:
    * Group: ARCHive group name, which is the department or departments responsible for the content.
    * Format type: category of the format, for example audio, image, or text.
    * Format standardized name: a simplified version of the name, removing details to group related formats together.
    * Format identification: a combination of the format name, version, and registry key (usually PRONOM).

Unlike Excel, pandas does not merge difference of capitalization, e.g. MPEG Video and MPEG video, when subtotaling.

Parameters:
    report_folder : the path to the folder which contains ARCHive's group file format reports,
    the combined format reports made by the merge_format_reports.py script, and usage report (all CSVs)

Returns:
    ARCHive-Formats-Analysis_Frequency.xlsx : the amount of collections, AIPs, files, and/or size
    by group, type, standardized format name, and format identification

    ARCHive-Formats-Analysis_Group-Overlap.xlsx : the number of groups and list of groups
    which have each format type, standardized format name, and format identification

    ARCHive-Formats-Analysis_Ranges.xlsx : the number of formats (by format standardized name or format identification),
    which are in each specified range of number of files or size

    ARCHive-Formats-Analysis_Risk.xlsx : the number of files, GB, and format identifications at each NARA risk level
    for ARCHive, each department, each format type, and each NARA plan type, as well the number for each NARA match type
"""

import csv
import numpy as np
import os
import pandas as pd
import sys
from update_standardization import check_argument


def archive_overview(df_aip, df_group, usage):
    """Calculate statistics for each ARCHive group using the usage report and both ARCHive format reports

    Parameters:
        df_aip : a dataframe with the information from archive_formats_by_aip.csv
        df_group : a dataframe with the information from archive_formats_by_group.csv
        usage : the path to the ARCHive usage report

    Returns:
        group_stats : a dataframe with row by group and columns with the Size (TB and GB) and number of
        Collections, AIPs, File_IDs, Format Types, Format Standardized Names, and Format Identifications.
    """

    # Gets the size (in TB) per group from the usage report.
    size_by_group = size_in_tb(usage)

    # Gets the size (in GB) from the dataframe to show the difference between unique (from usage)
    # and inflated by multiple identifications for individual files.
    size_inflated = round(df_group.groupby('Group')['Size_GB'].sum(), 2)

    # Gets the number of collections per group from the archive_formats_by_aip report.
    # Only counts collections with AIPs, which may result in a difference between this count and the ARCHive interface.
    # Additionally, dlg-hargrett collections in ARCHive that are part of turningpoint are counted as dlg.
    collections_by_group = df_aip.groupby('Group')['Collection'].nunique()

    # Gets the number of AIPs per group from the archive_formats_by_aip report.
    # Not using data from usage report since each version of an AIP is counted separately.
    aips_by_group = df_aip.groupby('Group')['AIP'].nunique()

    # Gets the number of format types per group from the archive_formats_by_aip report.
    types_by_group = df_aip.groupby('Group')['Format_Type'].nunique()

    # Gets the number of file_ids per group from the archive_formats_by_group report.
    # These numbers are inflated by files with more than one format identification.
    files_by_group = df_group.groupby('Group')['File_IDs'].sum()

    # Gets the number of format standardized names per group from the archive_formats_by_aip report.
    formats_by_group = df_aip.groupby('Group')['Format_Standardized_Name'].nunique()

    # Gets the number of format identifications per group from the archive_formats_by_group report.
    format_ids_by_group = df_group.groupby('Group')['Format_Identification'].nunique()

    # Combines the series with all the counts into a single dataframe.
    group_stats = pd.concat([size_by_group, size_inflated, collections_by_group, aips_by_group, files_by_group,
                             types_by_group, formats_by_group, format_ids_by_group], axis=1)

    # Renames the dataframe columns to be more descriptive.
    rename = {"Size": "Size_TB", "Size_GB": "Size_GB_Inflated", "Collection": "Collections", "AIP": "AIPs",
              "Format_Type": "Format_Types", "Format_Standardized_Name": "Format_Standardized_Names",
              "Format_Identification": "Format_Identifications"}
    group_stats = group_stats.rename(columns=rename)

    # Replace cells without values (one group has no files yet) with 0.
    group_stats = group_stats.fillna(0)

    # Adds the column totals as a row in the dataframe.
    group_stats.loc["total"] = [group_stats['Size_TB'].sum(), group_stats['Size_GB_Inflated'].sum(),
                                group_stats['Collections'].sum(), group_stats['AIPs'].sum(),
                                group_stats['File_IDs'].sum(), df_group['Format_Type'].nunique(),
                                df_group['Format_Standardized_Name'].nunique(),
                                df_group['Format_Identification'].nunique()]

    # Returns the information in a dataframe. Row index is the group_code and columns are Size (TB), Collections,
    # AIPs, File_IDs, Format Types, Format Standardized Names, and Format Identifications.
    return group_stats


def file_count_ranges(category, df_group):
    """Calculate the number of instances of the category within each range of number of files (1-9, 10-99, etc.)

    Parameters:
        category : the column to subtotal on
        df_group : a dataframe with the information from archive_formats_by_group.csv

    Returns:
        result : a dataframe with rows by range and column Number of Formats (CATEGORY)
    """

    # Makes a series with the number of file_ids for each instance of the category, regardless  of group.
    df_cat = df_group.groupby(df_group[category])['File_IDs'].sum()

    # Makes series with the subset of the archive_formats_by_group report data with the specified numbers of file_ids.
    ones = df_cat[(df_cat < 10)]
    tens = df_cat[(df_cat >= 10) & (df_cat < 100)]
    hundreds = df_cat[(df_cat >= 100) & (df_cat < 1000)]
    thousands = df_cat[(df_cat >= 1000) & (df_cat < 10000)]
    ten_thousands = df_cat[(df_cat >= 10000) & (df_cat < 100000)]
    hundred_thousands_plus = df_cat[(df_cat >= 100000)]

    # Makes lists with the data for the dataframe: file_id ranges (for index) and the number of instances in each range.
    file_id_ranges = ["1-9", "10-99", "100-999", "1000-9999", "10000-99999", "100000+"]
    instances = [ones.count(), tens.count(), hundreds.count(), thousands.count(), ten_thousands.count(),
                 hundred_thousands_plus.count()]

    # Makes a dataframe from the lists.
    result = pd.DataFrame(instances, columns=[f"Number of Formats ({category})"], index=file_id_ranges)

    # Returns the dataframe. Row index is the file_id ranges and column is Number of Formats (category).
    return result


def format_id_frequency(totals, df_group):
    """Calculate the frequency for every format identification (name, version, registry key) by different measures

    The resulting dataframe is sorted largest to smallest by file_id count
    since the items of most interest are the most common formats.

    Parameters:
        totals : a dictionary with the total number of collections, AIPs, files, and size in ARCHive
        df_group : a dataframe with the information from archive_formats_by_group.csv

    Returns:
        format_ids : a dataframe with rows by format identification and
        columns with the number and percentage of file id counts and size,
        sorted largest to smallest by file id count
    """

    # Make series for file_id counts and file_id percentages.
    format_count = df_group.groupby(df_group['Format_Identification'])['File_IDs'].sum()
    format_percentage = (format_count / totals['Files']) * 100
    format_percentage = round(format_percentage, 2)
    format_percentage = format_percentage.rename('File_IDs_Percentage')

    # Make series for total size and size percentages.
    size = df_group.groupby(df_group['Format_Identification'])['Size_GB'].sum()
    size_percentage = (size / totals['Size']) * 100
    size_percentage = round(size_percentage, 2)
    size_percentage = size_percentage.rename('Size_GB_Percentage')

    # Combine all the series into a single dataframe and sort largest to smallest by file_ids.
    format_ids = pd.concat([format_count, format_percentage, size, size_percentage], axis=1)
    format_ids = format_ids.sort_values(by='File_IDs', ascending=False)

    # Returns the dataframe. Row index is the file_ids and columns are the four frequency measures.
    return format_ids


def get_report_paths(report_folder_path):
    """Get the path to the three archive_reports used as script input and check for missing files

    Parameters:
        report_folder_path : the path to the folder given as the script parameter, where the reports should be

    Returns:
        formats_by_aip_path : the path to the archive_formats_by_aip.csv, or None
        formats_by_group_path : the path to the archive_formats_by_group.csv, or None
        usage_path : the path to the ARCHive usage report, or None
        missing_list : a list of missing reports, if any, or an empty list
    """

    # Makes variables to store the paths, if found.
    formats_by_aip_path = None
    formats_by_group_path = None
    usage_path = None

    # Searches the report folder for the expected files, and if found updates the variable with the file name.
    # These files include dates, so the entire file name cannot be predicted by the script.
    for file in os.listdir(report_folder_path):
        if file.startswith("archive_formats_by_aip") and file.endswith(".csv"):
            formats_by_aip_path = os.path.join(report_folder_path, file)
        elif file.startswith("archive_formats_by_group") and file.endswith(".csv"):
            formats_by_group_path = os.path.join(report_folder_path, file)
        elif file.startswith("usage_report_") and file.endswith(".csv"):
            usage_path = os.path.join(report_folder_path, file)

    # Tests if all three paths were found, and if not adds the missing ones to a list.
    missing_list = []
    if not formats_by_aip_path:
        missing_list.append("archive_formats_by_aip.csv")
    if not formats_by_group_path:
        missing_list.append("archive_formats_by_group.csv")
    if not usage_path:
        missing_list.append("usage_report.csv")

    # Returns the results. The errors list is empty if all three files were found.
    return formats_by_aip_path, formats_by_group_path, usage_path, missing_list


def group_overlap(category, df_group):
    """Calculate the number of groups and a list of the groups which have each instance of the category

    Parameters:
        category : the column, for example Format Type, to subtotal on
        df_group : a dataframe with the information from archive_formats_by_group.csv

    Returns:
        groups_per_category : a dataframe with rows by instance of the category and columns Group_List and Groups.
    """

    # Makes a series with a list of group names for each instance of the category.

    groups_list = df_group.groupby(df_group[category])['Group'].unique()
    groups_list = groups_list.rename('Group_List')

    # Makes a series with the number of groups for each instance of the category.
    groups_count = groups_list.str.len()
    groups_count = groups_count.rename('Groups')

    # Converts the list from a list to a comma-separated string for easier readability in Excel.
    # Wait to do this until after groups_count so that the count is correct.
    groups_list = groups_list.apply(", ".join)

    # Combines the count and the list series into a single dataframe.
    # Had to do these separately to get the counts for each instance separately.
    groups_per_category = pd.concat([groups_count, groups_list], axis=1)

    # Sorts the values by the number of groups, largest to smallest.
    # The primary use for this data is to see what the most groups have in common.
    groups_per_category = groups_per_category.sort_values(by='Groups', ascending=False)

    # Returns the dataframe. Row index is the category and columns are Groups, Group List.
    return groups_per_category


def groupby_risk(df_group, groupby_list):
    """Calculate the number of file ids, size in GB, and format identifications for the groupby_list column(s)

    Parameters:
        df_group : a dataframe with the information from archive_formats_by_group.csv
        groupby_list : a list of the column or columns to subtotal on

    Returns:
        df : a dataframe with rows by instance of the category or categories and
        columns File_IDs, Size_GB, and Format_Identifications
    """

    # Calculates the totals.
    # File IDs and Size (GB) are sums; Format Identification is the number of unique values.
    # The index is reset so that the groupby_list columns are maintained as columns and don't become the index.
    aggregation_methods = {'File_IDs': 'sum', 'Size_GB': 'sum', 'Format_Identification': 'nunique'}
    df = df_group.groupby(groupby_list).agg(aggregation_methods).reset_index()

    # Renames one of the columns, to reflect it being a total.
    # The other column names worked equally well as labels for the individual or aggregate data.
    df.rename(columns=({'Format_Identification': 'Format_Identifications'}), inplace=True)

    # Rounds Size (GB) to 2 decimal places to make it easier to read.
    df['Size_GB'] = round(df['Size_GB'], 2)

    return df


def one_category(category, totals, df_aip, df_group):
    """Calculate subtotals of collection, AIP, and file_id counts and size in GB per each instance of a category

    Parameters:
        category : the column (e.g., Format Type) to subtotal on
        totals : a dictionary with the total number of collections, AIPs, files, and size in ARCHive
        df_aip : a dataframe with the information from archive_formats_by_aip.csv
        df_group : a dataframe with the information from archive_formats_by_group.csv

    Returns:
        result : a dataframe with rows by instance of the category and
        columns Collections, Collections Percentage, AIPs, AIPs Percentage, File_IDs, File_IDs Percentage
    """

    # Creates a series for each count type (collections, AIPs, and file_ids) and size for each instance of the category.
    collections = df_aip.groupby(category)['Collection'].nunique()
    aips = df_aip.groupby(category)['AIP'].nunique()
    files = df_group.groupby(category)['File_IDs'].sum()
    size = df_group.groupby(category)['Size_GB'].sum()

    # Creates a series for the percentage of each count type and size for each instance of the category.
    # The percentage is rounded to two decimal places.
    # Also renames the series to be more descriptive.

    collections_percent = (collections / totals['Collections']) * 100
    collections_percent = round(collections_percent, 2)
    collections_percent = collections_percent.rename('Collections_Percentage')

    aips_percent = (aips / totals['AIPs']) * 100
    aips_percent = round(aips_percent, 2)
    aips_percent = aips_percent.rename('AIPs_Percentage')

    files_percent = (files / totals['Files']) * 100
    files_percent = round(files_percent, 2)
    files_percent = files_percent.rename('File_IDs_Percentage')

    size_percent = (size / totals['Size']) * 100
    size_percent = round(size_percent, 2)
    size_percent = size_percent.rename('Size_GB_Percentage')

    # Combines all the count and percentage series into a single dataframe.
    result = pd.concat([collections, collections_percent, aips, aips_percent, files, files_percent, size, size_percent],
                       axis=1)

    # Renames Collection and AIP columns to plural to be more descriptive.
    result = result.rename({'Collection': 'Collections', 'AIP': 'AIPs'}, axis=1)

    # Returns the dataframe. Row index is the category and columns are Collections, Collections Percentage, AIPs,
    # AIPs Percentage, File_IDs, File_IDs Percentage.
    return result


def size_ranges(category, df_group):
    """Calculate the number of instances of the category within each range of total size (0-249 GB, 250-499 GB, etc.)

    Parameters:
        category : the column to subtotal on
        df_group : a dataframe with the information from archive_formats_by_group.csv

    Returns:
        result : a dataframe with rows by size range and column Total Size (CATEGORY)
    """

    # Makes a series with the total size for each instance of the category, regardless of group.
    df_cat = df_group.groupby(df_group[category])['Size_GB'].sum()

    # Makes series with the subset of the archive_formats_by_group report data with the specified numbers of file_ids.
    tier_one = df_cat[(df_cat < 10)]
    tier_two = df_cat[(df_cat >= 10) & (df_cat < 100)]
    tier_three = df_cat[(df_cat >= 100) & (df_cat < 500)]
    tier_four = df_cat[(df_cat >= 500) & (df_cat < 1000)]
    tier_five = df_cat[(df_cat >= 1000) & (df_cat < 10000)]
    tier_six = df_cat[(df_cat >= 10000) & (df_cat < 50000)]
    tier_seven = df_cat[(df_cat >= 50000)]

    # Makes lists with the data for the dataframe: file_id ranges (for index) and the number of instances in each range.
    size_ranges = ["0-9 GB", "10-99 GB", "100-499 GB", "500-999 GB", "1-9 TB", "10-49 TB", "50+ TB"]
    instances = [tier_one.count(), tier_two.count(), tier_three.count(), tier_four.count(), tier_five.count(),
                 tier_six.count(), tier_seven.count()]

    # Makes a dataframe from the lists.
    result = pd.DataFrame(instances, columns=[f"Total Size ({category})"], index=size_ranges)

    # Returns the dataframe. Row index is the size ranges and column is Total Size (category).
    return result


def size_in_tb(usage):
    """Use data from the usage report to calculate the size in TB each group

    Parameters:
        usage : the path to the ARCHive usage report

    Returns:
        sizes : a dataframe with rows by group and column Size
    """

    # Group Names maps the human-friendly version of group names from the usage report to the ARCHive group code
    # which is used in both archive format archive_reports and in ARCHive metadata generally.
    group_names = {"Brown Media Archives": "bmac", "Digital Library of Georgia": "dlg",
                   "DLG & Hargrett": "dlg-hargrett", "DLG & Map and Government Information Library": "dlg-magil",
                   "Hargrett Library": "hargrett", "Map and Government Information Library": "magil",
                   "Richard B. Russell Library": "russell"}

    # Makes a dictionary for the size for each group, gathering all data before converting it to a dataframe.
    group_size = {}

    # Gets the data from each row of the usage report.
    # A row can have data on a group, an individual user, or be blank.
    with open(usage, 'r') as usage_open:
        usage_read = csv.reader(usage_open)
        for row in usage_read:

            # Parses data (group name, size, and size unit of measurement)from each group's row,
            # identified by not being blank and having a group name at row[0].
            if row and row[0] in group_names:
                group = group_names[row[0]]
                size, unit = row[2].split()

                # Converts the size to TB, rounded to two decimal places.
                # If it encounters a unit of measurement that wasn't anticipated, the script prints a warning message.
                conversion = {"Bytes": 1000000000000, "KB": 1000000000, "MB": 1000000, "GB": 1000, "TB": 1}
                try:
                    size = float(size) / conversion[unit]
                    size = round(size, 2)
                except KeyError:
                    size = 0
                    print("WARNING! Unexpected unit type:", unit)

                # Adds the results for this group to the dictionary.
                group_size[group] = size

    # Makes the dictionary into a dataframe so it can be combined with the collection and file_id counts.
    sizes = pd.DataFrame.from_dict(group_size, orient="index", columns=["Size"])

    # Returns the dataframe. Row index is the group_code and the column is Size.
    return sizes


def spreadsheet_frequency(df_aip, df_group, usage, output_folder):
    """Save counts and percentages of different categories to a spreadsheet named ARCHive-Formats-Analysis_Frequency.xlsx

    Parameters:
        df_aip : a dataframe with the information from archive_formats_by_aip.csv
        df_group : a dataframe with the information from archive_formats_by_group.csv
        usage : the path to the ARCHive usage report
        output_folder : the path to a folder for saving script output, which is also the folder with the script inputs

    Returns: none
    """

    # Makes the ARCHive overview dataframe (summary statistics by group).
    overview = archive_overview(df_aip, df_group, usage)

    # Saves totals to a dictionary for calculating percentages in other dataframes.
    # Use these totals each time so collection and AIP counts aren't inflated by multiple identifications.
    # Counts for file and size are inflated because don't have file name in the data and therefore can't deduplicate.
    totals_dict = {'Collections': overview['Collections']['total'],
                   'AIPs': overview['AIPs']['total'],
                   'Files': overview['File_IDs']['total'],
                   'Size': overview['Size_GB_Inflated']['total']}

    # Makes the format type summary (collection, AIP, file_id, and size counts and percentages).
    format_types = one_category("Format_Type", totals_dict, df_aip, df_group)

    # Makes the format standardized name summary (collection, AIP, file_id, and size counts and percentages).
    format_names = one_category("Format_Standardized_Name", totals_dict, df_aip, df_group)

    # Makes a format identifications summary (file_id and size count and percentage).
    format_ids = format_id_frequency(totals_dict, df_group)

    # Saves each summary as a separate sheet in an Excel spreadsheet.
    with pd.ExcelWriter(os.path.join(output_folder, f"ARCHive-Formats-Analysis_Frequency.xlsx")) as results:
        overview.to_excel(results, sheet_name="Group_Overview", index_label="Group")
        format_types.to_excel(results, sheet_name="Format_Types")
        format_names.to_excel(results, sheet_name="Format_Names")
        format_ids.to_excel(results, sheet_name="Format_IDs")


def spreadsheet_group_overlap(df_group, output_folder):
    """Save groups with the same instances of different categories to a spreadsheet named ARCHive-Formats Analysis_Group_Overlap.xlsx

    Parameters:
        df_group : a dataframe with the information from archive_formats_by_group.csv
        output_folder : the path to a folder for saving script output, which is also the folder with the script inputs

    Returns: none
    """

    # Makes a dataframe with the number of groups and list of groups that have each format type.
    groups_per_type = group_overlap('Format_Type', df_group)

    # Makes a dataframe with the number of groups and list of groups that have each format standardized name.
    groups_per_name = group_overlap('Format_Standardized_Name', df_group)

    # Makes a dataframe with the number of groups and list of groups that have each format identification.
    groups_per_id = group_overlap('Format_Identification', df_group)

    # Saves each dataframe as a separate sheet in an Excel spreadsheet.
    with pd.ExcelWriter(os.path.join(output_folder, f"ARCHive-Formats-Analysis_Group-Overlap.xlsx")) as results:
        groups_per_type.to_excel(results, sheet_name="Groups_per_Type")
        groups_per_name.to_excel(results, sheet_name="Groups_per_Name")
        groups_per_id.to_excel(results, sheet_name="Groups_per_Format_ID")


def spreadsheet_ranges(df_group, output_folder):
    """Save the number of formats within predetermined ranges to a spreadsheet named ARCHive-Formats Analysis_Ranges.xlsx

    Parameters:
        df_group : a dataframe with the information from archive_formats_by_group.csv
        output_folder : the path to a folder for saving script output, which is also the folder with the script inputs

    Returns: none
    """

    # Makes dataframes with the number of format standardized names within different ranges of file_id counts and sizes.
    format_name_ranges = file_count_ranges('Format_Standardized_Name', df_group)
    format_name_sizes = size_ranges('Format_Standardized_Name', df_group)

    # Makes dataframes with the number of format identifications within different ranges of file_id counts and sizes.
    format_id_ranges = file_count_ranges('Format_Identification', df_group)
    format_id_sizes = size_ranges('Format_Identification', df_group)

    # Saves each dataframe as a separate sheet in an Excel spreadsheet.
    with pd.ExcelWriter(os.path.join(output_folder, f"ARCHive-Formats-Analysis_Ranges.xlsx")) as results:
        format_name_ranges.to_excel(results, sheet_name="Format_Name_Ranges", index_label="File_ID Count Range")
        format_name_sizes.to_excel(results, sheet_name="Format_Name_Sizes", index_label="Size Range")
        format_id_ranges.to_excel(results, sheet_name="Format_ID_Ranges", index_label="File_ID Count Range")
        format_id_sizes.to_excel(results, sheet_name="Format_ID_Sizes", index_label="Size Range")


def spreadsheet_risk(df_group, output_folder):
    """Save different measures of the NARA risk levels to a spreadsheet named ARCHive-Formats-Analysis_Risk.xlsx

    Parameters:
        df_group : a dataframe with the information from archive_formats_by_group.csv
        output_folder : the path to a folder for saving script output, which is also the folder with the script inputs

    Returns: none
    """

    # Assigns an order to the NARA risk categories, so results are in order of increasing risk.
    risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
    df_group['NARA_Risk_Level'] = pd.Categorical(df_group['NARA_Risk_Level'], risk_order, ordered=True)

    # Makes a new column to classify the type of NARA preservation action plan.
    conditions = [(df_group['NARA_Proposed_Preservation_Plan'].notnull()) &
                  (df_group['NARA_Proposed_Preservation_Plan'].str.startswith("Depends on version")),
                  (df_group['NARA_Proposed_Preservation_Plan'].notnull()) &
                  (df_group['NARA_Proposed_Preservation_Plan'].str.startswith("Further research is required")),
                  df_group['NARA_Proposed_Preservation_Plan'].isnull(),
                  df_group['NARA_Proposed_Preservation_Plan'] == "Retain",
                  (df_group['NARA_Proposed_Preservation_Plan'].notnull()) &
                  (df_group['NARA_Proposed_Preservation_Plan'].str.startswith("Retain ")),
                  (df_group['NARA_Proposed_Preservation_Plan'].notnull()) &
                  (df_group['NARA_Proposed_Preservation_Plan'].str.startswith("Transform"))]
    plan_type = ["Depends on version", "Further research required", "No plan", "Retain", "Retain but act", "Transform"]
    df_group["NARA_Plan_Type"] = np.select(conditions, plan_type)

    # Calculates the dataframe for each risk summary.
    # The first four are the amount at each NARA risk level for different categories of data
    # and the last is the match method between format identifications and NARA risk.
    archive_risk = groupby_risk(df_group, ['NARA_Risk_Level'])
    dept_risk = groupby_risk(df_group, ['Group', 'NARA_Risk_Level'])
    type_risk = groupby_risk(df_group, ['Format_Type', 'NARA_Risk_Level'])
    plan_risk = groupby_risk(df_group, ['NARA_Plan_Type', 'NARA_Risk_Level'])
    match = groupby_risk(df_group, ['NARA_Match_Type'])

    # Saves each dataframe as a separate sheet in an Excel spreadsheet.
    with pd.ExcelWriter(os.path.join(output_folder, "ARCHive-Formats-Analysis_Risk.xlsx")) as results:
        archive_risk.to_excel(results, sheet_name="ARCHive_Risk_Overview", index=False)
        dept_risk.to_excel(results, sheet_name="Department_Risk_Overview", index=False)
        type_risk.to_excel(results, sheet_name="Format_Type_Risk", index=False)
        plan_risk.to_excel(results, sheet_name="NARA_Plan_Type_Risk", index=False)
        match.to_excel(results, sheet_name="NARA_Match_Types", index=False)


if __name__ == '__main__':

    # Verifies the required argument is present and the path is valid.
    # If there was an error, prints the error and exits the script.
    report_folder, error_message = check_argument(sys.argv)
    if error_message:
        print(error_message)
        print("Script usage: python path/archive_reports.py report_folder")
        sys.exit(1)

    # Gets paths of the three archive_reports to be analyzed, which are in report_folder.
    # If any were not found (missing is not empty), prints the missing one(s) and exits the script.
    formats_by_aip_report, formats_by_group_report, usage_report, missing = get_report_paths(report_folder)
    if len(missing) > 0:
        for file_name in missing:
            print(f"Could not find {file_name} in '{report_folder}'.")
        print("Please add the missing report(s) to the report folder and run this script again.")
        sys.exit(1)

    # Makes dataframes from both ARCHive format archive_reports.
    df_formats_by_aip = pd.read_csv(formats_by_aip_report)
    df_formats_by_group = pd.read_csv(formats_by_group_report)

    # Makes a spreadsheet in the folder with the ARCHive archive_reports
    # with summaries based on counts and percentages of collection, AIP, file ids, and/or size.
    spreadsheet_frequency(df_formats_by_aip, df_formats_by_group, usage_report, report_folder)

    # Makes a spreadsheet in the folder with the ARCHive archive_reports
    # with summaries of group overlap for each instance of format type, format name, and format id.
    spreadsheet_group_overlap(df_formats_by_group, report_folder)

    # Makes a spreadsheet in the folder with the ARCHive archive_reports
    # with summaries of the number of instances within predetermined ranges of file id counts or size.
    spreadsheet_ranges(df_formats_by_group, report_folder)

    # Makes a spreadsheet in the folder with the ARCHive archive_reports
    # with summaries of the amount of content at different NARA risk levels.
    spreadsheet_risk(df_formats_by_group, report_folder)
