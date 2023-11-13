"""
Test for the function format_id_frequency(),
which calculates the number and percentage of files and size for each format id.

For input, the test uses a file in the archive_reports folder of this script repo.
"""

import os
import pandas as pd
import unittest
from archive_reports import format_id_frequency


class MyTestCase(unittest.TestCase):

    def test_format_id_frequency(self):
        """
        Test for the function working correctly.
        There is no error handling or variations of input to test.
        """
        # Makes the variables used for function input.
        totals_dict = {"Collections": 7, "AIPs": 14, "Files": 2290, "Size": 3326.99}
        df_formats_by_group = pd.read_csv(os.path.join("format_id_frequency", "archive_formats_by_group_2023-08.csv"))

        # Runs the function being tested and converts the output into a list for easier comparison.
        format_ids = format_id_frequency(totals_dict, df_formats_by_group)
        result = [format_ids.columns.tolist()] + format_ids.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["File_IDs", "File_IDs_Percentage", "Size_GB", "Size_GB_Percentage"],
                    ["Tagged Image File Format|6|fmt/353", 735, 32.10, 1540.2, 46.29],
                    ["Matroska|NO VALUE|NO VALUE", 645, 28.17, 1487.702, 44.72],
                    ["JPEG EXIF|2.1|x-fmt/390", 195, 8.52, 130.0, 3.91]]
        self.assertEqual(result, expected, "Problem with test for format id frequency")


if __name__ == '__main__':
    unittest.main()
