"""
Test for the function file_count_ranges(),
which calculates the number of instances of a category
with file counts within seven specified ranges.

For input, tests use files in the reports folder of this script repo.
The names of the input CSV do not follow the naming convention used in production
so that the variations can be saved to the same folder in the repo for easier organization.
"""

import os
import pandas as pd
import unittest
from reports import file_count_ranges


class MyTestCase(unittest.TestCase):

    def test_format_id_ranges(self):

        """
        Test for making the format identification file count ranges.
        """
        # Makes the variable used for function input.
        df_formats_by_group = pd.read_csv(os.path.join("file_count_ranges", "archive_formats_by_group_2000-01.csv"))

        # Runs the function being tested and converts the output into a list for easier comparison.
        format_id_ranges = file_count_ranges('Format_Identification', df_formats_by_group)
        result = [format_id_ranges.columns.tolist()] + format_id_ranges.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Number of Formats (Format_Identification)"],
                    ["1-9", 1], ["10-99", 1], ["100-999", 0], ["1000-9999", 3], ["10000-99999", 2], ["100000+", 1]]
        self.assertEqual(result, expected, "Problem with test for format id ranges")

    def test_format_name_ranges(self):
        """
        Test for making the format standardized name file count ranges.
        """
        # Makes the variable used for function input.
        df_formats_by_group = pd.read_csv(os.path.join("file_count_ranges", "archive_formats_by_group_2000-02.csv"))

        # Runs the function being tested and converts the output into a list for easier comparison.
        format_name_ranges = file_count_ranges('Format_Standardized_Name', df_formats_by_group)
        result = [format_name_ranges.columns.tolist()] + format_name_ranges.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Number of Formats (Format_Standardized_Name)"],
                    ["1-9", 3], ["10-99", 0], ["100-999", 0], ["1000-9999", 2], ["10000-99999", 1], ["100000+", 1]]
        self.assertEqual(result, expected, "Problem with test for format name ranges")


if __name__ == '__main__':
    unittest.main()
