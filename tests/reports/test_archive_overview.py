"""
Test for the function archive_overview(),
which summarizes group counts.
"""

import os
import pandas as pd
import unittest
from reports import archive_overview


class MyTestCase(unittest.TestCase):

    def test_archive_overview(self):
        """
        Test for the function working correctly.
        There is no error handling or variations of input to test.
        """
        # Runs the function being tested.
        df_formats_by_aip = pd.read_csv(os.path.join("correct_input", "archive_formats_by_aip_2023-08.csv"))
        df_formats = pd.read_csv(os.path.join("correct_input", "archive_formats_2023-08.csv"))
        usage_report = os.path.join("correct_input", "usage_report_20171101_20211101.csv")
        overview = archive_overview(df_formats_by_aip, df_formats, usage_report)

        # Converts overview from a dataframe to a list for easier comparison.
        result = [overview.columns.tolist()] + overview.reset_index().values.tolist()

        # Tests if overview has the expected values.
        expected = [["Size (TB)", "Size (GB) Inflated", "Collections", "AIPs", "File_IDs", "Format Types",
                     "Format Standardized Names", "Format Identifications"],
                    ["bmac", 554.0, 326822.42, 1.0, 20.0, 6607.0, 2.0, 2.0, 2.0],
                    ["dlg", 10.6, 3231.06, 9.0, 29.0, 264332, 3.0, 5.0, 8.0],
                    ["hargrett", 0.15, 143.97, 2.0, 47.0, 5507, 2.0, 3.0, 6.0],
                    ["total", 564.75, 330197.44999999995, 12.0, 96.0, 276446, 4.0, 7.0, 12.0]]
        self.assertEqual(result, expected, "Problem with test for archive overview")


if __name__ == '__main__':
    unittest.main()
