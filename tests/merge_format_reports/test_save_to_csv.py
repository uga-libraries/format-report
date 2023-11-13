"""
Tests for the function save_to_csv(),
which save either header information or the provided rows to the specified CSV.
"""

import csv
import os
import unittest
from merge_format_reports import save_to_csv


def csv_to_list(csv_path):
    """
    Converts the information in a CSV to a list, where item is a list with one row's contents.
    Used to compare the script output to expected results.
    """
    with open(csv_path, newline="") as open_csv:
        read_csv = csv.reader(open_csv)
        row_list = list(read_csv)
    return row_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """
        Deletes the CSVs, if made by the tests.
        """
        if os.path.exists("archive_formats_by_aip_2023-08.csv"):
            os.remove("archive_formats_by_aip_2023-08.csv")
        if os.path.exists("archive_formats_by_group_2023-08.csv"):
            os.remove("archive_formats_by_group_2023-08.csv")

    def test_add_iteratively(self):
        """
        Test for adding multiple sets of rows to a CSV, first the header and then a list of 2 rows.
        """
        # Runs the function being tested, twice.
        save_to_csv("archive_formats_by_group_2023-08.csv", "group_csv_header")
        group_report_list = [["hargrett", "1474", "2.001", "image", "JPEG",
                              "JPEG File Interchange Format|1.02|fmt/44", "JPEG File Interchange Format", "1.02",
                              "https://www.nationalarchives.gov.uk/PRONOM", "fmt/44", "NO VALUE"],
                              ["hargrett", "48", "0.001", "text", "Plain Text File", "Plain text|NO VALUE|NO VALUE",
                               "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "For testing"]]
        save_to_csv("archive_formats_by_group_2023-08.csv", group_report_list)

        # Tests that the content of the CSV contains the correct information.
        result = csv_to_list("archive_formats_by_group_2023-08.csv")
        expected = [["Group", "File_IDs", "Size_GB", "Format_Type", "Format_Standardized_Name",
                     "Format_Identification", "Format_Name", "Format_Version", "Registry_Name",
                     "Registry_Key", "Format_Note"],
                    ["hargrett", "1474", "2.001", "image", "JPEG", "JPEG File Interchange Format|1.02|fmt/44",
                     "JPEG File Interchange Format", "1.02", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/44", "NO VALUE"],
                     ["hargrett", "48", "0.001", "text", "Plain Text File", "Plain text|NO VALUE|NO VALUE",
                      "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "For testing"]]
        self.assertEqual(result, expected, "Problem with test for one row")

    def test_aip_header(self):
        """
        Test for adding the header for the "by_aip" CSV.
        """
        # Runs the function being tested.
        save_to_csv("archive_formats_by_aip_2023-08.csv", "aip_csv_header")

        # Tests that the content of the CSV contains the correct information.
        result = csv_to_list("archive_formats_by_aip_2023-08.csv")
        expected = [["Group", "Collection", "AIP", "Format_Type", "Format_Standardized_Name",
                     "Format_Identification", "Format_Name", "Format_Version", "Registry_Name",
                     "Registry_Key", "Format_Note"]]
        self.assertEqual(result, expected, "Problem with test for aip header")

    def test_group_header(self):
        """
        Test for adding the header for the "by_group" CSV.
        """
        # Runs the function being tested.
        save_to_csv("archive_formats_by_group_2023-08.csv", "group_csv_header")

        # Tests that the content of the CSV contains the correct information.
        result = csv_to_list("archive_formats_by_group_2023-08.csv")
        expected = [["Group", "File_IDs", "Size_GB", "Format_Type", "Format_Standardized_Name",
                     "Format_Identification", "Format_Name", "Format_Version", "Registry_Name",
                     "Registry_Key", "Format_Note"]]
        self.assertEqual(result, expected, "Problem with test for group header")

    def test_one_row(self):
        """
        Test for adding a single row that is not the header to a CSV.
        """
        # Runs the function being tested.
        group_report_list = [["dlg", "17", "0.161", "image", "TIFF", "TIFF|NO VALUE|NO VALUE", "TIFF",
                              "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE"]]
        save_to_csv("archive_formats_by_group_2023-08.csv", group_report_list)

        # Tests that the content of the CSV contains the correct information.
        result = csv_to_list("archive_formats_by_group_2023-08.csv")
        self.assertEqual(result, group_report_list, "Problem with test for one row")

    def test_two_rows(self):
        """
        Test for adding a two rows at once to a CSV.
        """
        # Runs the function being tested.
        group_report_list = [["hargrett", "1474", "2.001", "image", "JPEG",
                              "JPEG File Interchange Format|1.02|fmt/44", "JPEG File Interchange Format", "1.02",
                              "https://www.nationalarchives.gov.uk/PRONOM", "fmt/44", "NO VALUE"],
                             ["hargrett", "48", "0.001", "text", "Plain Text File", "Plain text|NO VALUE|NO VALUE",
                              "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "For testing"]]
        save_to_csv("archive_formats_by_group_2023-08.csv", group_report_list)

        # Tests that the content of the CSV contains the correct information.
        result = csv_to_list("archive_formats_by_group_2023-08.csv")
        self.assertEqual(result, group_report_list, "Problem with test for one row")


if __name__ == '__main__':
    unittest.main()
