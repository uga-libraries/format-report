"""
Converts merged ARCHive format reports into reports for individual departments.

Information included:
* A list of AIPs with format identifications and risk levels
* A summary of risk by collection
* A summary of formats by collection and AIP

Before running this script, run merge_format_reports.py
"""

# usage: python path/department_reports.py archive_formats_by_aip

import os
import pandas as pd
import sys


if __name__ == '__main__':

    # Verifies the required argument is present and the path is valid.

    # Makes a dataframe for each group (department) in archive_formats_by_aip.

    # For each department, makes an Excel spreadsheet with the risk data and data summaries.

        # Makes the department spreadsheet and adds risk data.

        # Makes a collection risk summary and adds to the department spreadsheet.

        # Makes a collection and AIP format summary and adds to the department spreadsheet.