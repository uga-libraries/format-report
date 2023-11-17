"""
The CSV files created by merge_format_reports.py are opened in Excel to update risk matches,
but Excel automatically reformats version numbers to remove 0 from the end, which is an error.

The correct version is still part of Format_Identification.
This script updates the version column with the version from Format_Identification.
"""

# Usage: python path/fix_versions.py path_csv
#    path_csv is the path to either CSV created b merge_format_reports.py

import os
import pandas as pd
import sys