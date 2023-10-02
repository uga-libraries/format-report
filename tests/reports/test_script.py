"""
Tests the entire script reports.py,
which makes summaries of data from combined ARCHive format reports and the usage report.

For input, tests use files in the reports folder of this script repo.
"""

import datetime
import numpy as np
import os
import pandas as pd
import subprocess
import unittest


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """
        Deletes the Excel spreadsheets produced by the script, if made by the test.
        """
        file_paths = [os.path.join("correct_input", f"ARCHive-Formats-Analysis_Frequency.xlsx"),
                      os.path.join("correct_input", f"ARCHive-Formats-Analysis_Group-Overlap.xlsx"),
                      os.path.join("correct_input", f"ARCHive-Formats-Analysis_Ranges.xlsx")]

        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_correct_input(self):
        """
        Test for running the script on a report_folder with all three expected reports,
        which results in data in all sheets of all three Excel spreadsheets.
        """
        # Runs the script.
        script_path = os.path.join("..", "..", "reports.py")
        subprocess.run(f"python {script_path} correct_input", shell=True)

        # Reads each Excel file into pandas, and then each sheet into a separate dataframe.
        # Reading everything into dataframes at once so the Excel files can be closed,
        # allowing them to be deleted even if there are errors during the tests.
        frequency = pd.ExcelFile(os.path.join("correct_input", "ARCHive-Formats-Analysis_Frequency.xlsx"))
        df_1 = pd.read_excel(frequency, "Group Overview")
        df_2 = pd.read_excel(frequency, "Format Types")
        df_3 = pd.read_excel(frequency, "Format Names")
        df_4 = pd.read_excel(frequency, "Format IDs")
        frequency.close()

        overlap = pd.ExcelFile(os.path.join("correct_input", "ARCHive-Formats-Analysis_Group-Overlap.xlsx"))
        df_5 = pd.read_excel(overlap, "Groups per Type")
        df_6 = pd.read_excel(overlap, "Groups per Name")
        df_7 = pd.read_excel(overlap, "Groups per Format ID")
        overlap.close()

        ranges = pd.ExcelFile(os.path.join("correct_input", "ARCHive-Formats-Analysis_Ranges.xlsx"))
        df_8 = pd.read_excel(ranges, "Format Name Ranges")
        df_9 = pd.read_excel(ranges, "Format Name Sizes")
        df_10 = pd.read_excel(ranges, "Format ID Ranges")
        df_11 = pd.read_excel(ranges, "Format ID Sizes")
        ranges.close()

        # Tests if the Group Overview sheet has the expected values.
        result_1 = [df_1.columns.tolist()] + df_1.values.tolist()
        expected_1 = [["Group", "Size (TB)", "Size (GB) Inflated", "Collections", "AIPs", "File_IDs", "Format Types",
                       "Format Standardized Names", "Format Identifications"],
                      ["bmac", 554, 326822.42, 1, 20, 6607, 2, 2, 2],
                      ["dlg", 10.6, 3231.06, 9, 29, 264332, 3, 5, 8],
                      ["hargrett", 0.15, 143.97, 2, 47, 5507, 2, 3, 6],
                      ["total", 564.75, 330197.45, 12, 96, 276446, 4, 7, 12]]
        self.assertEqual(result_1, expected_1, "Problem with test for correct input, Group Overview")

        # Tests if the Format Types sheet has the expected values.
        result_2 = [df_2.columns.tolist()] + df_2.values.tolist()
        expected_2 = [["Format Type", "Collections", "Collections Percentage", "AIPs", "AIPs Percentage", "File_IDs",
                       "File_IDs Percentage", "Size (GB)", "Size (GB) Percentage"],
                      ["audio", 2, 16.67, 15, 15.62, 1240, 0.45, 1093.53, 0.33],
                      ["image", 8, 66.67, 40, 41.67, 269542, 97.5, 2545.081, 0.77],
                      ["video", 2, 16.67, 11, 11.46, 5446, 1.97, 326420.736, 98.86],
                      ["web_archive", 1, 8.33, 30, 31.25, 218, 0.08, 138.1, 0.04]]
        self.assertEqual(result_2, expected_2, "Problem with test for correct input, Format Types")

        # Tests if the Format Names sheet has the expected values.
        result_3 = [df_3.columns.tolist()] + df_3.values.tolist()
        expected_3 = [["Format Standardized Name", "Collections", "Collections Percentage", "AIPs", "AIPs Percentage",
                       "File_IDs", "File_IDs Percentage", "Size (GB)", "Size (GB) Percentage"],
                      ["JP2", 1, 8.33, 5, 5.21, 190092, 68.76, 776.817, 0.24],
                      ["JPEG", 4, 33.33, 24, 25.0, 5240, 1.9, 4.665999999999999, 0.0],
                      ["Matroska", 2, 16.67, 11, 11.46, 5446, 1.97, 326420.736, 98.86],
                      ["TIFF", 4, 33.33, 12, 12.5, 74210, 26.84, 1763.598, 0.53],
                      ["WARC", 1, 8.33, 30, 31.25, 218, 0.08, 138.1, 0.04],
                      ["WAVE", 1, 8.33, 10, 10.42, 1162, 0.42, 1064.383, 0.32],
                      ["Waveform Audio", 1, 8.33, 5, 5.21, 78, 0.03, 29.147, 0.01]]
        self.assertEqual(result_3, expected_3, "Problem with test for correct input, Format Names")

        # Tests if the Format ID sheet has the expected values.
        result_4 = [df_4.columns.tolist()] + df_4.values.tolist()
        expected_4 = [["Format Identification", "File_IDs", "File_IDs Percentage", "Size (GB)", "Size (GB) Percentage"],
                      ["JPEG 2000 JP2|NO VALUE|x-fmt/392", 190092, 68.76, 776.817, 0.24],
                      ["Tagged Image File Format|5|NO VALUE", 71228, 25.77, 1693.088, 0.51],
                      ["Matroska|NO VALUE|NO VALUE", 5446, 1.97, 326420.736, 98.86],
                      ["Tagged Image File Format|6|fmt/353", 2812, 1.02, 69.2, 0.02],
                      ["JPEG EXIF|2.1|x-fmt/390", 1946, 0.7, 1.897, 0.0],
                      ["JPEG File Interchange Format|1.02|fmt/44", 1507, 0.55, 2.026, 0.0],
                      ["JPEG File Interchange Format|1.01|fmt/43", 1322, 0.48, 0.687, 0.0],
                      ["Wave|NO VALUE|NO VALUE", 1162, 0.42, 1064.383, 0.32],
                      ["JPEG File Interchange Format|1|fmt/42", 465, 0.17, 0.05600000000000001, 0.0],
                      ["WARC|NO VALUE|fmt/289", 218, 0.08, 138.1, 0.04],
                      ["Tagged Image File Format|NO VALUE|NO VALUE", 170, 0.06, 1.31, 0.0],
                      ["Waveform Audio|NO VALUE|NO VALUE", 78, 0.03, 29.147, 0.01]]
        self.assertEqual(result_4, expected_4, "Problem with test for correct input, Format ID")

        # Tests if the Groups per Type sheet has the expected values.
        result_5 = [df_5.columns.tolist()] + df_5.values.tolist()
        expected_5 = [["Format Type", "Groups", "Group List"],
                      ["audio", 2, "bmac, dlg"],
                      ["image", 2, "dlg, hargrett"],
                      ["video", 2, "bmac, dlg"],
                      ["web_archive", 1, "hargrett"]]
        self.assertEqual(result_5, expected_5, "Problem with test for correct input, Groups per Type")

        # Tests if the Groups per Name sheet has the expected values.
        result_6 = [df_6.columns.tolist()] + df_6.values.tolist()
        expected_6 = [["Format Standardized Name", "Groups", "Group List"],
                      ["JPEG", 2, "hargrett, dlg"],
                      ["Matroska", 2, "bmac, dlg"],
                      ["TIFF", 2, "dlg, hargrett"],
                      ["JP2", 1, "dlg"],
                      ["WARC", 1, "hargrett"],
                      ["WAVE", 1, "bmac"],
                      ["Waveform Audio", 1, "dlg"]]
        self.assertEqual(result_6, expected_6, "Problem with test for correct input, Groups per Name")

        # Tests if the Groups per Format ID sheet has the expected values.
        result_7 = [df_7.columns.tolist()] + df_7.values.tolist()
        expected_7 = [["Format Identification", "Groups", "Group List"],
                      ["JPEG File Interchange Format|1.02|fmt/44", 2, "dlg, hargrett"],
                      ["JPEG File Interchange Format|1|fmt/42", 2, "dlg, hargrett"],
                      ["Matroska|NO VALUE|NO VALUE", 2, "bmac, dlg"],
                      ["Tagged Image File Format|NO VALUE|NO VALUE", 2, "dlg, hargrett"],
                      ["JPEG 2000 JP2|NO VALUE|x-fmt/392", 1, "dlg"],
                      ["JPEG EXIF|2.1|x-fmt/390", 1, "hargrett"],
                      ["JPEG File Interchange Format|1.01|fmt/43", 1, "hargrett"],
                      ["Tagged Image File Format|5|NO VALUE", 1, "dlg"],
                      ["Tagged Image File Format|6|fmt/353", 1, "dlg"],
                      ["WARC|NO VALUE|fmt/289", 1, "hargrett"],
                      ["Waveform Audio|NO VALUE|NO VALUE", 1, "dlg"],
                      ["Wave|NO VALUE|NO VALUE", 1, "bmac"]]
        self.assertEqual(result_7, expected_7, "Problem with test for correct input, Groups per Format ID")

        # Tests if the Format Name Ranges sheet has the expected values.
        result_8 = [df_8.columns.tolist()] + df_8.values.tolist()
        expected_8 = [["File_ID Count Range", "Number of Formats (Format Standardized Name)"],
                      ["1-9", 0], ["10-99", 1],  ["100-999", 1], ["1000-9999", 3], ["10000-99999", 1], ["100000+", 1]]
        self.assertEqual(result_8, expected_8, "Problem with test for correct input, Format Name Ranges")

        # Tests if the Format Name Sizes sheet has the expected values.
        result_9 = [df_9.columns.tolist()] + df_9.values.tolist()
        expected_9 = [["Size Range", "Total Size (Format Standardized Name)"],
                      ["0-9 GB", 1], ["10-99 GB", 1], ["100-499 GB", 1], ["500-999 GB", 1], ["1-9 TB", 2],
                      ["10-49 TB", 0], ["50+ TB", 1]]
        self.assertEqual(result_9, expected_9, "Problem with test for correct input, Format Name Sizes")

        # Tests if the Format ID Ranges sheet has the expected values.
        result_10 = [df_10.columns.tolist()] + df_10.values.tolist()
        expected_10 = [["File_ID Count Range", "Number of Formats (Format Identification)"],
                       ["1-9", 0], ["10-99", 1], ["100-999", 3], ["1000-9999", 6], ["10000-99999", 1], ["100000+", 1]]
        self.assertEqual(result_10, expected_10, "Problem with test for correct input, Format ID Ranges")

        # Tests if the Format ID Sizes sheet has the expected values.
        result_11 = [df_11.columns.tolist()] + df_11.values.tolist()
        expected_11 = [["Size Range", "Total Size (Format Identification)"],
                       ["0-9 GB", 5], ["10-99 GB", 2], ["100-499 GB", 1], ["500-999 GB", 1], ["1-9 TB", 2],
                       ["10-49 TB", 0], ["50+ TB", 1]]
        self.assertEqual(result_11, expected_11, "Problem with test for correct input, Format ID Sizes")

    def test_missing_argument(self):
        """
        Test for running the script without the required argument.
        It will print a message and exit the script.
        """
        # Runs the script without the required argument and tests that the script exits.
        script_path = os.path.join("..", "..", "reports.py")
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {script_path}", shell=True, check=True)

        # Tests if the expected message was produced. In production, this is printed to the terminal.
        # Must run the script a second time because cannot capture output with self.assertRaises.
        output = subprocess.run(f"python {script_path}", shell=True, stdout=subprocess.PIPE)
        msg_result = output.stdout.decode("utf-8")
        msg_expected = "Required argument report_folder is missing\r\n" \
                       "Script usage: python path/reports.py report_folder\r\n"
        self.assertEqual(msg_result, msg_expected, "Problem with test for missing argument, message")

    def test_missing_input(self):
        """
        Test for running the script on a report_folder without the expected reports.
        It will print a message and exit the script.
        """
        # Runs the script with a report_folder that does not have the required reports and tests that the script exits.
        script_path = os.path.join("..", "..", "reports.py")
        report_folder = os.path.join("get_report_paths", "missing_input_all")
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {script_path} {report_folder}", shell=True, check=True)

        # Tests if the expected message was produced. In production, this is printed to the terminal.
        # Must run the script a second time because cannot capture output with self.assertRaises.
        output = subprocess.run(f"python {script_path} {report_folder}", shell=True, stdout=subprocess.PIPE)
        msg_result = output.stdout.decode("utf-8")
        msg_expected = "Could not find archive_formats_by_aip.csv in 'get_report_paths\\missing_input_all'.\r\n" \
                       "Could not find archive_formats_by_group.csv in 'get_report_paths\\missing_input_all'.\r\n" \
                       "Could not find usage_report.csv in 'get_report_paths\\missing_input_all'.\r\n" \
                       "Please add the missing report(s) to the report folder and run this script again.\r\n"
        self.assertEqual(msg_result, msg_expected, "Problem with test for missing input, message")


if __name__ == '__main__':
    unittest.main()
