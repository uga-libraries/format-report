"""
Test for the function one_category(),
which calculates the number of collections, AIPs, file_ids, and GB for each instance of one category.

For input, tests use report folders in the repo for this script.
The names of the input CSVs do not follow the naming convention used in production
so that the variations can be saved to the same folder in the repo for easier organization.
"""

import os
import pandas as pd
import unittest
from reports import one_category


class MyTestCase(unittest.TestCase):

    def test_format_standardized_name(self):
        """
        Test for making the format standardized name subtotals.
        """
        # Makes the variables used for function input.
        totals_dict = {"Collections": 7, "AIPs": 11, "Files": 2545, "Size": 6100}
        df_formats_by_aip = pd.read_csv(os.path.join("one_category", "archive_formats_by_aip_2003-01.csv"))
        df_formats_by_group = pd.read_csv(os.path.join("one_category", "archive_formats_by_group_2003-01.csv"))

        # Runs the function being tested and converts the output into a list for easier comparison.
        format_names = one_category("Format Standardized Name", totals_dict, df_formats_by_aip, df_formats_by_group)
        result = [format_names.columns.tolist()] + format_names.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Collections", "Collections Percentage", "AIPs", "AIPs Percentage", "File_IDs",
                     "File_IDs Percentage", "Size (GB)", "Size (GB) Percentage"],
                    ["JP2", 1, 14.29, 2, 18.18, 190, 7.47, 776.817, 12.73],
                    ["JPEG", 1, 14.29, 2, 18.18, 340, 13.36, 40.898, 0.67],
                    ["Matroska", 2, 28.57, 2, 18.18, 555, 21.81, 3919.702, 64.26],
                    ["TIFF", 3, 42.86, 5, 45.45, 1160, 45.58, 874.539, 14.34],
                    ["WARC", 1, 14.29, 1, 9.09, 220, 8.64, 138.1, 2.26],
                    ["Waveform Audio", 1, 14.29, 1, 9.09, 80, 3.14, 290.147, 4.76]]
        self.assertEqual(result, expected, "Problem with test for format standardized name")

    def test_format_type(self):
        """
        Test for making the format type subtotals.
        """
        # Makes the variables used for function input.
        totals_dict = {"Collections": 7, "AIPs": 11, "Files": 2545, "Size": 6100}
        df_formats_by_aip = pd.read_csv(os.path.join("one_category", "archive_formats_by_aip_2003-02.csv"))
        df_formats_by_group = pd.read_csv(os.path.join("one_category", "archive_formats_by_group_2003-02.csv"))

        # Runs the function being tested and converts the output into a list for easier comparison.
        format_types = one_category("Format Type", totals_dict, df_formats_by_aip, df_formats_by_group)
        result = [format_types.columns.tolist()] + format_types.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Collections", "Collections Percentage", "AIPs", "AIPs Percentage", "File_IDs",
                     "File_IDs Percentage", "Size (GB)", "Size (GB) Percentage"],
                     ["audio", 1, 14.29, 1, 9.09, 80, 3.14, 290.147, 4.76],
                     ["image", 3, 42.86, 7, 63.64, 1690, 66.40, 1692.2540000000001, 27.74],
                     ["video", 2, 28.57, 2, 18.18, 555, 21.81, 3919.702, 64.26],
                     ["web_archive", 1, 14.29, 1, 9.09, 220, 8.64, 138.1, 2.26]]
        self.assertEqual(result, expected, "Problem with test for format type")


if __name__ == '__main__':
    unittest.main()
