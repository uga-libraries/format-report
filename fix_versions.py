"""
The CSV files created by merge_format_reports.py are opened in Excel to update risk matches,
but Excel automatically reformats version numbers to remove 0 from the end, which is an error.

The correct version is still part of Format_Identification.
This script updates the version column with the version from Format_Identification.
"""

# Usage: python path/fix_versions.py csv_path
#    path_csv is the path to either CSV created b merge_format_reports.py

import os
import pandas as pd
import sys


def check_argument(argument_list):
    """
    Verifies the required argument csv_path is present and valid,
    and the filename matches expected naming conventions.
    Returns the path and the error, if any.
    """
    # Makes variables with default values to store the results of the function.
    path = None
    error = None

    # Verifies that the required argument (csv_path) is present.
    if len(argument_list) > 1:
        path = argument_list[1]
        # Verifies that the argument path is valid.
        if os.path.exists(path):
            # Verifies that the argument is a file that matches the expected naming conventions.
            filename = os.path.basename(path)
            if not(filename.startswith("archive_formats_by") and filename.endswith(".csv")):
                error = f"CSV path '{path}' is not an expected merged ARCHive format report."
        else:
            error = f"CSV path '{path}' does not exist"
    else:
        error = "Required argument csv_path is missing"

    return path, error
