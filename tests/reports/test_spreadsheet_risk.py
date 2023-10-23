"""
Test for the function spreadsheet_risk(),
which makes a spreadsheet with the amount of content at each NARA risk level.
"""
import os
import pandas as pd
import unittest
from reports import spreadsheet_risk


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the Excel spreadsheet produced by the function, if it was made by the test."""
        file_path = os.path.join("spreadsheet_risk", "ARCHive-Formats-Analysis_Risk.xlsx")
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_spreadsheet_risk(self):
        """
        Test for the function working correctly.
        There is no error handling or variations of input to test.
        Input variations are handled in the function groupby_risk(), which is called by this function.
        """
        # Makes the dataframe used for function input.
        # For now, only including one field in df_group beyond what need for this analysis and data is fake.
        df_formats_by_group = pd.read_csv(os.path.join("spreadsheet_risk", "archive_formats_by_group_2023-08.csv"))

        # Runs the function being tested.
        spreadsheet_risk(df_formats_by_group, "spreadsheet_risk")

        # Reads the entire Excel file into pandas, and then each sheet into a separate dataframe.
        # Reading all the sheets at once so the Excel file can be closed,
        # allowing it to be deleted even if there are errors during the tests.
        result = pd.ExcelFile(os.path.join("spreadsheet_risk", "ARCHive-Formats-Analysis_Risk.xlsx"))
        archive_risk = pd.read_excel(result, "ARCHive Risk Overview")
        dept_risk = pd.read_excel(result, "Department Risk Overview")
        type_risk = pd.read_excel(result, "Format Type Risk")
        match = pd.read_excel(result, "NARA Match Types")
        result.close()

        # Tests if the ARCHive Risk Overview sheet has the expected values.
        archive_result = [archive_risk.columns.tolist()] + archive_risk.values.tolist()
        archive_expected = [["NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                            ["Low Risk", 7, 70, 2],
                            ["Moderate Risk", 3, 30, 1],
                            ["High Risk", 4, 40, 1],
                            ["No Match", 5, 50, 1]]
        self.assertEqual(archive_result, archive_expected, "Problem with the test for ARCHive Risk Overview")

        # Tests if the Department Risk Overview sheet has the expected values.
        dept_result = [dept_risk.columns.tolist()] + dept_risk.values.tolist()
        dept_expected = [["Group", "NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                         ["A", "Low Risk", 3, 30, 1],
                         ["A", "Moderate Risk", 3, 30, 1],
                         ["A", "High Risk", 0, 0, 0],
                         ["A", "No Match", 5, 50, 1],
                         ["B", "Low Risk", 4, 40, 2],
                         ["B", "Moderate Risk", 0, 0, 0],
                         ["B", "High Risk", 4, 40, 1],
                         ["B", "No Match", 0, 0, 0]]
        self.assertEqual(dept_result, dept_expected, "Problem with the test for Department Risk Overview")

        # Tests if the Format Type Risk sheet has the expected values.
        type_result = [type_risk.columns.tolist()] + type_risk.values.tolist()
        type_expected = [["Format Type", "NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                         ["T1", "Low Risk", 7, 70, 2],
                         ["T1", "Moderate Risk", 0, 0, 0],
                         ["T1", "High Risk", 4, 40, 1],
                         ["T1", "No Match", 0, 0, 0],
                         ["T2", "Low Risk", 0, 0, 0],
                         ["T2", "Moderate Risk", 3, 30, 1],
                         ["T2", "High Risk", 0, 0, 0],
                         ["T2", "No Match", 5, 50, 1]]
        self.assertEqual(type_result, type_expected, "Problem with the test for Format Type Risk")

        # Tests if the NARA Match Types sheet has the expected values.
        match_result = [match.columns.tolist()] + match.values.tolist()
        match_expected = [["NARA_Match_Type", "File_IDs", "Size (GB)", "Format Identifications"],
                          ["Extension", 7, 70, 2],
                          ["Name", 2, 20, 1],
                          ["No NARA Match", 5, 50, 1],
                          ["PUID", 5, 50, 1]]
        self.assertEqual(match_result, match_expected, "Problem with the test for NARA Match Types")


if __name__ == '__main__':
    unittest.main()
