"""
Test for the function size_ranges(),
which calculates the number of instances of a category
with sizes within seven specified ranges.
"""

import os
import pandas as pd
import unittest
from reports import size_ranges


class MyTestCase(unittest.TestCase):

    def test_format_id_ranges(self):
        """
        Test for making the format identification size ranges.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        df_formats = pd.read_csv(os.path.join("size_ranges", "archive_formats_id.csv"))
        format_id_sizes = size_ranges("Format Identification", df_formats)
        result = [format_id_sizes.columns.tolist()] + format_id_sizes.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Total Size (Format Identification)"],
                    ["0-9 GB", 3], ["10-99 GB", 1], ["100-499 GB", 0], ["500-999 GB", 1],
                    ["1-9 TB", 2], ["10-49 TB", 0], ["50+ TB", 1]]
        self.assertEqual(result, expected, "Problem with test for format id ranges")

    def test_format_name_ranges(self):
        """
        Test for making the format standardized name size ranges.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        df_formats = pd.read_csv(os.path.join("size_ranges", "archive_formats_name.csv"))
        format_name_sizes = size_ranges("Format Standardized Name", df_formats)
        result = [format_name_sizes.columns.tolist()] + format_name_sizes.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Total Size (Format Standardized Name)"],
                    ["0-9 GB", 1], ["10-99 GB", 1], ["100-499 GB", 1], ["500-999 GB", 3],
                    ["1-9 TB", 0], ["10-49 TB", 0], ["50+ TB", 1]]
        self.assertEqual(result, expected, "Problem with test for format name ranges")


if __name__ == '__main__':
    unittest.main()
