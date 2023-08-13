"""
Test for the function two_categories(),
which calculates the number of collections, AIPs, file_ids, and GB for each combination of two categories.
"""

import os
import pandas as pd
import unittest
from reports import two_categories


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """
        Calculates the values of variables used for function input.
        """
        self.df_formats_by_aip = pd.read_csv(os.path.join("two_categories", "archive_formats_by_aip_2023-08.csv"))
        self.df_formats = pd.read_csv(os.path.join("two_categories", "archive_formats_2023-08.csv"))

    def test_name_by_group(self):
        """
        Test for making the format standardized name by group subtotals.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        name_by_group = two_categories("Format Standardized Name", "Group", self.df_formats_by_aip, self.df_formats)
        result = [name_by_group.columns.tolist()] + name_by_group.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Collections", "AIPs", "File_IDs", "Size (GB)"],
                    ["JP2", "dlg", 1, 1, 20, 40],
                    ["TIFF", "dlg", 1, 1, 15, 30],
                    ["TIFF", "hargrett", 1, 1, 10, 20],
                    ["WARC", "hargrett", 1, 1, 5, 10]]
        self.assertEqual(result, expected, "Problem with test for name by group")

    def test_type_by_group(self):
        """
        Test for making the format type by group subtotals.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        type_by_group = two_categories("Format Type", "Group", self.df_formats_by_aip, self.df_formats)
        result = [type_by_group.columns.tolist()] + type_by_group.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Collections", "AIPs", "File_IDs", "Size (GB)"],
                    ["image", "dlg", 2, 2, 35, 70],
                    ["image", "hargrett", 1, 1, 10, 20],
                    ["web_archive", "hargrett", 1, 1, 5, 10]]
        self.assertEqual(result, expected, "Problem with test for type by group")

    def test_type_by_name(self):
        """
        Test for making the format type by format standardized name subtotals.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        type_by_name = two_categories("Format Type", "Format Standardized Name",
                                      self.df_formats_by_aip, self.df_formats)
        result = [type_by_name.columns.tolist()] + type_by_name.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Collections", "AIPs", "File_IDs", "Size (GB)"],
                    ["image", "JP2", 1, 1, 20, 40],
                    ["image", "TIFF", 2, 2, 25, 50],
                    ["web_archive", "WARC", 1, 1, 5, 10]]
        self.assertEqual(result, expected, "Problem with test for type by name")


if __name__ == '__main__':
    unittest.main()
