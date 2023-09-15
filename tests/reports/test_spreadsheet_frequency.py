"""
Test for the function spreadsheet_frequency(),
which makes a spreadsheet with summaries of counts and percentages
for group, format type, format standardized name, and format id.
"""
import os
import pandas as pd
import unittest
from reports import spreadsheet_frequency


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the Excel spreadsheet produced by the function, if it is made by the test."""
        file_path = os.path.join("correct_input", "ARCHive-Formats-Analysis_Frequency.xlsx")
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_spreadsheet_frequency(self):
        """
        Test for the function working correctly.
        There is no error handling or variations of input to test.
        """
        # Makes the variables used for function input.
        df_formats_by_aip = pd.read_csv(os.path.join("correct_input", "archive_formats_by_aip_2023-08.csv"))
        df_formats_by_group = pd.read_csv(os.path.join("correct_input", "archive_formats_by_group_2023-08.csv"))
        usage_report = os.path.join("correct_input", "usage_report_20171101_20211101.csv")

        # Runs the function being tested.
        spreadsheet_frequency(df_formats_by_aip, df_formats_by_group, usage_report, "correct_input")

        # Reads the entire Excel file into pandas, and then each sheet into a separate dataframe.
        # Reading all the sheets at once so the Excel file can be closed,
        # allowing it to be deleted even if there are errors during the tests.
        result = pd.ExcelFile(os.path.join("correct_input", "ARCHive-Formats-Analysis_Frequency.xlsx"))
        df_1 = pd.read_excel(result, "Group Overview")
        df_2 = pd.read_excel(result, "Format Types")
        df_3 = pd.read_excel(result, "Format Names")
        df_4 = pd.read_excel(result, "Format IDs")
        result.close()

        # Tests if the Group Overview sheet has the expected values.
        result_1 = [df_1.columns.tolist()] + df_1.values.tolist()
        expected_1 = [["Group", "Size (TB)", "Size (GB) Inflated", "Collections", "AIPs", "File_IDs", "Format Types",
                       "Format Standardized Names", "Format Identifications"],
                      ["bmac", 554, 326822.42, 1, 20, 6607, 2, 2, 2],
                      ["dlg", 10.6, 3231.06, 9, 29, 264332, 3, 5, 8],
                      ["hargrett", 0.15, 143.97, 2, 47, 5507, 2, 3, 6],
                      ["total", 564.75, 330197.45, 12, 96, 276446, 4, 7, 12]]
        self.assertEqual(result_1, expected_1, "Problem with test for Group Overview")

        # Tests if the Format Types sheet has the expected values.
        result_2 = [df_2.columns.tolist()] + df_2.values.tolist()
        expected_2 = [["Format Type", "Collections", "Collections Percentage", "AIPs", "AIPs Percentage", "File_IDs",
                       "File_IDs Percentage", "Size (GB)", "Size (GB) Percentage"],
                      ["audio", 2, 16.67, 15, 15.62, 1240, 0.45, 1093.53, 0.33],
                      ["image", 8, 66.67, 40, 41.67, 269542, 97.5, 2545.081, 0.77],
                      ["video", 2, 16.67, 11, 11.46, 5446, 1.97, 326420.736, 98.86],
                      ["web_archive", 1, 8.33, 30, 31.25, 218, 0.08, 138.1, 0.04]]
        self.assertEqual(result_2, expected_2, "Problem with test for Format Types")

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
        self.assertEqual(result_3, expected_3, "Problem with test for Format Names")

        # Tests if the Format IDs sheet has the expected values.
        result_4 = [df_4.columns.tolist()] + df_4.values.tolist()
        expected_4 = [["Format Identification", "File_IDs", "File_IDs Percentage", "Size (GB)",
                       "Size (GB) Percentage"],
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
        self.assertEqual(result_4, expected_4, "Problem with test for Format IDs")


if __name__ == '__main__':
    unittest.main()
