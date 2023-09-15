"""
Test for the function spreadsheet_ranges(),
which makes a spreadsheet with the number of instances of format types and format standardized names
within predetermined ranges of file id counts or size.
"""
import os
import pandas as pd
import unittest
from reports import spreadsheet_ranges


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the Excel spreadsheet produced by the function, if it is made by the test."""
        file_path = os.path.join("correct_input", "ARCHive-Formats-Analysis_Ranges.xlsx")
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_spreadsheet_ranges(self):
        """
        Test for the function working correctly.
        There is no error handling or variations of input to test.
        """
        # Makes the dataframe used for function input.
        df_formats_by_group = pd.read_csv(os.path.join("correct_input", "archive_formats_by_group_2023-08.csv"))

        # Runs the function being tested.
        spreadsheet_ranges(df_formats_by_group, "correct_input")

        # Reads the entire Excel file into pandas, and then each sheet into a separate dataframe.
        # Reading all the sheets at once so the Excel file can be closed,
        # allowing it to be deleted even if there are errors during the tests.
        result = pd.ExcelFile(os.path.join("correct_input", "ARCHive-Formats-Analysis_Ranges.xlsx"))
        df_1 = pd.read_excel(result, "Format Name Ranges")
        df_2 = pd.read_excel(result, "Format Name Sizes")
        df_3 = pd.read_excel(result, "Format ID Ranges")
        df_4 = pd.read_excel(result, "Format ID Sizes")
        result.close()

        # Tests if the Format Name Ranges sheet has the expected values.
        result_1 = [df_1.columns.tolist()] + df_1.values.tolist()
        expected_1 = [["File_ID Count Range", "Number of Formats (Format Standardized Name)"],
                      ["1-9", 0], ["10-99", 1], ["100-999", 1], ["1000-9999", 3], ["10000-99999", 1], ["100000+", 1]]
        self.assertEqual(result_1, expected_1, "Problem with test for Format Name Ranges")

        # Tests if the Format Name Sizes sheet has the expected values.
        result_2 = [df_2.columns.tolist()] + df_2.values.tolist()
        expected_2 = [["Size Range", "Total Size (Format Standardized Name)"],
                      ["0-9 GB", 1], ["10-99 GB", 1], ["100-499 GB", 1], ["500-999 GB", 1], ["1-9 TB", 2],
                      ["10-49 TB", 0], ["50+ TB", 1]]
        self.assertEqual(result_2, expected_2, "Problem with test for Format Name Sizes")

        # Tests if the Format ID Ranges sheet has the expected values.
        result_3 = [df_3.columns.tolist()] + df_3.values.tolist()
        expected_3 = [["File_ID Count Range", "Number of Formats (Format Identification)"],
                      ["1-9", 0], ["10-99", 1], ["100-999", 3], ["1000-9999", 6], ["10000-99999", 1], ["100000+", 1]]
        self.assertEqual(result_3, expected_3, "Problem with test for correct input, Format ID Ranges")

        # Tests if the Format ID Sizes sheet has the expected values.
        result_4 = [df_4.columns.tolist()] + df_4.values.tolist()
        expected_4 = [["Size Range", "Total Size (Format Identification)"],
                      ["0-9 GB", 5], ["10-99 GB", 2], ["100-499 GB", 1], ["500-999 GB", 1], ["1-9 TB", 2],
                      ["10-49 TB", 0], ["50+ TB", 1]]
        self.assertEqual(result_4, expected_4, "Problem with test for Format ID Sizes")


if __name__ == '__main__':
    unittest.main()
