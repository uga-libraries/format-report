"""
Tests for the function csv_to_dataframe(),
which reads the CSVs with data needed for the analysis into dataframes,
handles encoding errors if encountered, and edits column names for one of them.
"""

import os
import unittest
from merge_format_reports import csv_to_dataframe


class MyTestCase(unittest.TestCase):

    def test_by_aip(self):
        """
        Test for reading the archive_formats_by_aip spreadsheet.
        """
        # Runs the function being tested and converts the resulting dataframe into a list, including the column names.
        df = csv_to_dataframe(os.path.join("csv_to_dataframe", "archive_formats_by_aip.csv"))
        result = [df.columns.to_list()] + df.values.tolist()

        # Tests that the resulting dataframe contains the correct information.
        expected = [["Group", "Collection", "AIP", "Format Type", "Format Standardized Name", "Format Identification",
                     "Format Name", "Format Version", "Registry Name", "Registry Key", "Format Note"],
                    ["dlg", "dlg_vsbg", "dlg_vsbg_jaj001", "image", "DNG", "Digital Negative|NO VALUE|fmt/436",
                     "Digital Negative", "NO VALUE", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/436",
                     "NO VALUE"],
                    ["dlg", "dlg_vsbg", "dlg_vsbg_jaj002", "image", "DNG", "Digital Negative|NO VALUE|fmt/436",
                     "Digital Negative", "NO VALUE", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/436",
                     "NO VALUE"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0006", "structured_text", "HTML", "HTML|1.0|fmt/102",
                     "HTML", "1.0", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/102", "NO VALUE"]]
        self.assertEqual(result, expected, "Problem with By AIP CSV")

    def test_by_group(self):
        """
        Test for reading the archive_formats_by_group spreadsheet.
        """
        # Runs the function being tested and converts the resulting dataframe into a list, including the column names.
        df = csv_to_dataframe(os.path.join("csv_to_dataframe", "archive_formats_by_group.csv"))
        result = [df.columns.to_list()] + df.values.tolist()

        # Tests that the result dataframe contains the correct information.
        expected = [["Group", "File_IDs", "Size (GB)", "Format Type", "Format Standardized Name",
                     "Format Identification", "Format Name", "Format Version", "Registry Name", "Registry Key",
                     "Format Note"],
                    ["dlg", "300", "20", "image", "DNG", "Digital Negative|NO VALUE|fmt/436", "Digital Negative",
                     "NO VALUE", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/436", "NO VALUE"],
                    ["hargrett", "90", "0.04", "structured_text", "HTML", "HTML|1.0|fmt/102", "HTML", "1.0",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/102", "NO VALUE"]]
        self.assertEqual(result, expected, "Problem with By Group CSV")

    def test_nara(self):
        """
        Tests for reading the NARA risk spreadsheet (NARA_PreservationActionPlan_FileFormats.csv).
        Result for testing is the number of rows in the dataframe and the column names are correct.
        Not testing the exact values since there is a lot of data and may be updated for other tests.
        """
        # Runs the function being tested.
        df = csv_to_dataframe("NARA_PreservationActionPlan_FileFormats_test.csv")

        # Tests that the number of rows in the dataframe is correct.
        result_rows = len(df.index)
        self.assertEqual(result_rows, 63, "Problem with NARA, row count")

        # Tests that the columns in the dataframe, which were renamed by the function, are correct.
        result_columns = df.columns.to_list()
        expected_columns = ["NARA_Format Name", "NARA_File Extension(s)", "NARA_PRONOM URL", "NARA_Risk Level",
                            "NARA_Preservation Action", "NARA_Proposed Preservation Plan",
                            "NARA_Description and Justification",
                            "NARA_Preferred Processing and Transformation Tool(s)"]
        self.assertEqual(result_columns, expected_columns, "Problem with NARA, column names")

    def test_encoding_error(self):
        """
        Test for reading a spreadsheet with an encoding error.
        Result for testing is the df returned by the function, converted to a list for an easier comparison.
        """
        # Runs the function being tested and converts the resulting dataframe into a list, including the column names.
        # NOTE: the function prints an error message to the terminal if it is working correctly.
        df = csv_to_dataframe(os.path.join("csv_to_dataframe", "archive_formats_encoding_error.csv"))
        result = [df.columns.to_list()] + df.values.tolist()

        # Tests that the result dataframe contains the correct information.
        expected = [["Group", "File_IDs", "Size (GB)", "Format Type", "Format Standardized Name",
                     "Format Identification", "Format Name", "Format Version", "Registry Name", "Registry Key",
                     "Format Note"],
                    ["dlg", "300", "20", "image", "DNG", "Digital Negative|NO VALUE|fmt/436", "Digital Negative",
                     "NO VALUE", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/436", "NO VALUE"],
                    ["hargrett", "90", "0.04", "structured_text", "HTML", "HTML|1.0|fmt/102", "HTML", "1.0",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/102", "NO VALUE"]]
        self.assertEqual(result, expected, "Problem with encoding error")


if __name__ == "__main__":
    unittest.main()
