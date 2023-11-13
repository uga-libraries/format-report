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
        file_path = os.path.join("spreadsheet_frequency", "ARCHive-Formats-Analysis_Frequency.xlsx")
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_spreadsheet_frequency(self):
        """
        Test for the function working correctly.
        There is no error handling or variations of input to test.
        """
        # Makes the variables used for function input.
        df_formats_by_aip = pd.read_csv(os.path.join("spreadsheet_frequency", "archive_formats_by_aip_2023-08.csv"))
        df_formats_by_group = pd.read_csv(os.path.join("spreadsheet_frequency", "archive_formats_by_group_2023-08.csv"))
        usage_report = os.path.join("spreadsheet_frequency", "usage_report_20171101_20211101.csv")

        # Runs the function being tested.
        spreadsheet_frequency(df_formats_by_aip, df_formats_by_group, usage_report, "spreadsheet_frequency")

        # Reads the entire Excel file into pandas, and then each sheet into a separate dataframe.
        # Reading all the sheets at once so the Excel file can be closed,
        # allowing it to be deleted even if there are errors during the tests.
        result = pd.ExcelFile(os.path.join("spreadsheet_frequency", "ARCHive-Formats-Analysis_Frequency.xlsx"))
        df_1 = pd.read_excel(result, "Group Overview")
        df_2 = pd.read_excel(result, "Format Types")
        df_3 = pd.read_excel(result, "Format Names")
        df_4 = pd.read_excel(result, "Format IDs")
        result.close()

        # Tests if the Group Overview sheet has the expected values.
        result_1 = [df_1.columns.tolist()] + df_1.values.tolist()
        expected_1 = [["Group", "Size_TB", "Size_GB_Inflated", "Collections", "AIPs", "File_IDs", "Format_Types",
                       "Format_Standardized_Names", "Format_Identifications"],
                      ["dlg", 10.6, 29.15, 1, 78, 78, 1, 1, 1],
                      ["hargrett", 0.15, 0.01, 2, 7, 231, 2, 2, 5],
                      ["russell", 35.8, 30.65, 29, 230, 22951, 4, 6, 15],
                      ["total", 46.55, 59.81, 32, 315, 23260, 4, 6, 16]]
        self.assertEqual(result_1, expected_1, "Problem with test for Group Overview")

        # Tests if the Format Types sheet has the expected values.
        result_2 = [df_2.columns.tolist()] + df_2.values.tolist()
        expected_2 = [["Format_Type", "Collections", "Collections_Percentage", "AIPs", "AIPs_Percentage", "File_IDs",
                       "File_IDs_Percentage", "Size_GB", "Size_GB_Percentage"],
                      ["archive", 13, 40.62, 47, 14.92, 292, 1.26, 2.057, 3.44],
                      ["audio", 19, 59.38, 163, 51.75, 854, 3.67, 53.499, 89.45],
                      ["database", 8, 25.00, 31, 9.84, 66, 0.28, 0.33, 0.55],
                      ["text", 10, 31.25, 97, 30.79, 22048, 94.79, 3.924, 6.56]]
        self.assertEqual(result_2, expected_2, "Problem with test for Format Types")

        # Tests if the Format Names sheet has the expected values.
        result_3 = [df_3.columns.tolist()] + df_3.values.tolist()
        expected_3 = [["Format_Standardized_Name", "Collections", "Collections_Percentage", "AIPs", "AIPs_Percentage",
                       "File_IDs", "File_IDs_Percentage", "Size_GB", "Size_GB_Percentage"],
                      ["MS DOS Compression format (KWAJ variant)", 1, 3.12, 1, 0.32, 53, 0.23, 0.001, 0.0],
                      ["Microsoft Access Database", 8, 25.0, 31, 9.84, 66, 0.28, 0.33, 0.55],
                      ["Microsoft Word", 10, 31.25, 97, 30.79, 22048, 94.79, 3.924, 6.56],
                      ["StuffIt Archive File", 1, 3.12, 2, 0.63, 2, 0.01, 0.002, 0.0],
                      ["Waveform Audio", 19, 59.38, 163, 51.75, 854, 3.67, 53.499, 89.45],
                      ["ZIP Format", 12, 37.50, 46, 14.60, 237, 1.02, 2.054, 3.43]]
        self.assertEqual(result_3, expected_3, "Problem with test for Format Names")

        # Tests if the Format IDs sheet has the expected values.
        result_4 = [df_4.columns.tolist()] + df_4.values.tolist()
        expected_4 = [["Format_Identification", "File_IDs", "File_IDs_Percentage", "Size_GB",
                       "Size_GB_Percentage"],
                      ["Microsoft Word Binary File Format|97-2003|fmt/40", 14677, 63.10, 2.552, 4.27],
                      ["Microsoft Word Binary File Format|NO VALUE|NO VALUE", 6987, 30.04, 1.369, 2.29],
                      ["Waveform Audio|NO VALUE|fmt/141", 407, 1.75, 20.717, 34.64],
                      ["Microsoft Word Binary File Format|4.0|x-fmt/64", 326, 1.4, 0.002, 0.0],
                      ["Waveform Audio|NO VALUE|fmt/142", 314, 1.35, 2.61, 4.36],
                      ["ZIP Format|2.0|x-fmt/263", 221, 0.95, 2.024, 3.38],
                      ["Waveform Audio|NO VALUE|NO VALUE", 78, 0.34, 29.147, 48.73],
                      ["Microsoft Access Database|NO VALUE|NO VALUE", 66, 0.28, 0.33, 0.55],
                      ["Microsoft Word Binary File Format|5.0|x-fmt/65", 58, 0.25, 0.001, 0.0],
                      ["MS DOS Compression format (KWAJ variant)|NO VALUE|fmt/469", 53, 0.23, 0.001, 0.0],
                      ["Waveform Audio|0 MPEG Encoding|fmt/142 fmt/706", 52, 0.22, 1.025, 1.71],
                      ["ZIP Format|1.0|x-fmt/263", 8, 0.03, 0.003, 0.01],
                      ["ZIP Format|NO VALUE|x-fmt/263", 7, 0.03, 0.027, 0.05],
                      ["Waveform Audio|NO VALUE|fmt/6", 3, 0.01, 0.0, 0.0],
                      ["StuffIt Archive|NO VALUE|NO VALUE", 2, 0.01, 0.002, 0.0],
                      ["ZIP Format|2.0|NO VALUE", 1, 0.0, 0.0, 0.0]]
        self.assertEqual(result_4, expected_4, "Problem with test for Format IDs")


if __name__ == '__main__':
    unittest.main()
