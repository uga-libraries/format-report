"""
Test for the function spreadsheet_group_overlap(),
which makes a spreadsheet with the overlap between groups
for format type, format standardized name, and format id.
"""
import os
import pandas as pd
import unittest
from reports import spreadsheet_group_overlap


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the Excel spreadsheet produced by the function, if it was made by the test."""
        file_path = os.path.join("correct_input", "ARCHive-Formats-Analysis_Group-Overlap.xlsx")
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_spreadsheet_group_overlap(self):
        """
        Test for the function working correctly.
        There is no error handling or variations of input to test.
        """
        # Makes the dataframe used for function input.
        df_formats_by_group = pd.read_csv(os.path.join("spreadsheet_group_overlap",
                                                       "archive_formats_by_group_2023-08.csv"))

        # Runs the function being tested.
        spreadsheet_group_overlap(df_formats_by_group, "spreadsheet_group_overlap")

        # Reads the entire Excel file into pandas, and then each sheet into a separate dataframe.
        # Reading all the sheets at once so the Excel file can be closed,
        # allowing it to be deleted even if there are errors during the tests.
        result = pd.ExcelFile(os.path.join("spreadsheet_group_overlap", "ARCHive-Formats-Analysis_Group-Overlap.xlsx"))
        df_1 = pd.read_excel(result, "Groups per Type")
        df_2 = pd.read_excel(result, "Groups per Name")
        df_3 = pd.read_excel(result, "Groups per Format ID")
        result.close()

        # Tests if the Groups per Type sheet has the expected values.
        result_1 = [df_1.columns.tolist()] + df_1.values.tolist()
        expected_1 = [["Format Type", "Groups", "Group List"],
                      ["image", 4, "bmac, dlg, dlg-hargrett, dlg-magil"],
                      ["structured_text", 3, "dlg, hargrett, russell"],
                      ["design", 1, "russell"],
                      ["text", 1, "russell"]]
        self.assertEqual(result_1, expected_1, "Problem with test for Groups per Type")

        # Tests if the Groups per Name sheet has the expected values.
        result_2 = [df_2.columns.tolist()] + df_2.values.tolist()
        expected_2 = [["Format Standardized Name", "Groups", "Group List"],
                      ["HTML", 3, "dlg, hargrett, russell"],
                      ["TIFF", 3, "dlg, dlg-hargrett, dlg-magil"],
                      ["Adobe Illustrator", 1, "russell"],
                      ["Digital Moving Picture Exchange Bitmap", 1, "bmac"],
                      ["WordPerfect", 1, "russell"]]
        self.assertEqual(result_2, expected_2, "Problem with test for Groups per Name")

        # Tests if the Groups per Format ID sheet has the expected values.
        result_3 = [df_3.columns.tolist()] + df_3.values.tolist()
        expected_3 = [["Format Identification", "Groups", "Group List"],
                      ["Tagged Image File Format|5.0|fmt/353", 3, "dlg, dlg-hargrett, dlg-magil"],
                      ["Hypertext Markup Language|NO VALUE|NO VALUE", 2, "dlg, russell"],
                      ["Adobe Illustrator|5.0 / 5.5|fmt/420", 1, "russell"],
                      ["DPX|NO VALUE|NO VALUE", 1, "bmac"],
                      ["Hypertext Markup Language|NO VALUE|fmt/96", 1, "hargrett"],
                      ["Wordperfect Secondary File|5.0|x-fmt/42", 1, "russell"]]
        self.assertEqual(result_3, expected_3, "Problem with test for Groups per Format ID")


if __name__ == '__main__':
    unittest.main()
