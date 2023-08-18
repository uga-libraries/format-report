"""
Tests for the function group_overlap(),
which calculates the number of groups and a list of groups
that share each instance of a category.
"""

import os
import pandas as pd
import unittest
from reports import group_overlap


class MyTestCase(unittest.TestCase):

    def test_group_per_id(self):
        """
        Test for group overlap of format identifications.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        df_formats = pd.read_csv(os.path.join("group_overlap", "archive_formats_id.csv"))
        groups_per_id = group_overlap("Format Identification", df_formats)
        result = [groups_per_id.columns.tolist()] + groups_per_id.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Groups", "Group List"],
                    ["Matroska|NO VALUE|NO VALUE", 3, "bmac, dlg, hargrett"],
                    ["JPEG File Interchange Format|1|fmt/42", 2, "dlg, hargrett"],
                    ["JPEG 2000 JP2|NO VALUE|x-fmt/392", 1, "dlg"],
                    ["Wave|NO VALUE|NO VALUE", 1, "bmac"]]
        self.assertEqual(result, expected, "Problem with test for group per id")

    def test_group_per_name(self):
        """
        Test for group overlap of format standardized names.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        df_formats = pd.read_csv(os.path.join("group_overlap", "archive_formats_name.csv"))
        groups_per_name = group_overlap("Format Standardized Name", df_formats)
        result = [groups_per_name.columns.tolist()] + groups_per_name.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Groups", "Group List"],
                    ["TIFF", 3, "bmac, dlg, hargrett"],
                    ["Matroska", 2, "bmac, dlg"],
                    ["JP2", 1, "dlg"]]
        self.assertEqual(result, expected, "Problem with test for group per name")

    def test_group_per_type(self):
        """
        Test for group overlap of format type.groups_per_id
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        df_formats = pd.read_csv(os.path.join("group_overlap", "archive_formats_type.csv"))
        groups_per_type = group_overlap("Format Type", df_formats)
        result = [groups_per_type.columns.tolist()] + groups_per_type.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Groups", "Group List"],
                    ["image", 3, "bmac, dlg, hargrett"],
                    ["audio", 2, "bmac, dlg"],
                    ["video", 2, "bmac, dlg"],
                    ["web_archive", 1, "hargrett"]]
        self.assertEqual(result, expected, "Problem with test for group per type")


if __name__ == '__main__':
    unittest.main()
