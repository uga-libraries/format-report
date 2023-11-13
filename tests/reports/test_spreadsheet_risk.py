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
        df_formats_by_group = pd.read_csv(os.path.join("spreadsheet_risk", "archive_formats_by_group_2010-01.csv"))

        # Runs the function being tested.
        spreadsheet_risk(df_formats_by_group, "spreadsheet_risk")

        # Reads the entire Excel file into pandas, and then each sheet into a separate dataframe.
        # Reading all the sheets at once so the Excel file can be closed,
        # allowing it to be deleted even if there are errors during the tests.
        result = pd.ExcelFile(os.path.join("spreadsheet_risk", "ARCHive-Formats-Analysis_Risk.xlsx"))
        archive_risk = pd.read_excel(result, "ARCHive Risk Overview")
        dept_risk = pd.read_excel(result, "Department Risk Overview")
        type_risk = pd.read_excel(result, "Format Type Risk")
        plan_risk = pd.read_excel(result, "NARA Plan Type Risk")
        match = pd.read_excel(result, "NARA Match Types")
        result.close()

        # Tests if the ARCHive Risk Overview sheet has the expected values.
        archive_result = [archive_risk.columns.tolist()] + archive_risk.values.tolist()
        archive_expected = [["NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                            ["Low Risk", 4593, 479.83, 10],
                            ["Moderate Risk", 37478, 605575.12, 11],
                            ["High Risk", 168, 0.59, 6],
                            ["No Match", 37, 0.01, 3]]
        self.assertEqual(archive_result, archive_expected, "Problem with the test for ARCHive Risk Overview")

        # Tests if the Department Risk Overview sheet has the expected values.
        dept_result = [dept_risk.columns.tolist()] + dept_risk.values.tolist()
        dept_expected = [["Group", "NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                         ["bmac", "Low Risk", 0, 0.0, 0],
                         ["bmac", "Moderate Risk", 36516, 605573.45, 6],
                         ["bmac", "High Risk", 0, 0.0, 0],
                         ["bmac", "No Match", 0, 0.0, 0],
                         ["dlg-magil", "Low Risk", 1832, 339.72, 3],
                         ["dlg-magil", "Moderate Risk", 0, 0.0, 0],
                         ["dlg-magil", "High Risk", 0, 0.0, 0],
                         ["dlg-magil", "No Match", 0, 0.0, 0],
                         ["hargrett", "Low Risk", 2761, 140.11, 8],
                         ["hargrett", "Moderate Risk", 962, 1.67, 6],
                         ["hargrett", "High Risk", 168, 0.59, 6],
                         ["hargrett", "No Match", 37, 0.01, 3]]
        self.assertEqual(dept_result, dept_expected, "Problem with the test for Department Risk Overview")

        # Tests if the Format Type Risk sheet has the expected values.
        type_result = [type_risk.columns.tolist()] + type_risk.values.tolist()
        type_expected = [["Format Type", "NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                         ["application", "Low Risk", 0, 0.0, 0],
                         ["application", "Moderate Risk", 47, 0.0, 3],
                         ["application", "High Risk", 66, 0.04, 1],
                         ["application", "No Match", 0, 0.0, 0],
                         ["archive", "Low Risk", 218, 138.1, 1],
                         ["archive", "Moderate Risk", 2, 0.0, 1],
                         ["archive", "High Risk", 0, 0.0, 0],
                         ["archive", "No Match", 0, 0.0, 0],
                         ["audio", "Low Risk", 0, 0.0, 0],
                         ["audio", "Moderate Risk", 1166, 1065.99, 1],
                         ["audio", "High Risk", 0, 0.0, 0],
                         ["audio", "No Match", 0, 0.0, 0],
                         ["image", "Low Risk", 3790, 341.73, 7],
                         ["image", "Moderate Risk", 935, 0.06, 2],
                         ["image", "High Risk", 2, 0.01, 1],
                         ["image", "No Match", 0, 0.0, 0],
                         ["spreadsheet", "Low Risk", 0, 0.0, 0],
                         ["spreadsheet", "Moderate Risk", 0, 0.0, 0],
                         ["spreadsheet", "High Risk", 2, 0.0, 1],
                         ["spreadsheet", "No Match", 0, 0.0, 0],
                         ["text", "Low Risk", 581, 0.0, 1],
                         ["text", "Moderate Risk", 0, 0.0, 0],
                         ["text", "High Risk", 63, 0.0, 1],
                         ["text", "No Match", 1, 0.0, 1],
                         ["video", "Low Risk", 4, 0.0, 1],
                         ["video", "Moderate Risk", 35328, 604509.06, 4],
                         ["video", "High Risk", 35, 0.54, 2],
                         ["video", "No Match", 36, 0.01, 2]]
        self.assertEqual(type_result, type_expected, "Problem with the test for Format Type Risk")

        # Tests if the NARA Plan Type Risk sheet has the expected values.
        plan_result = [plan_risk.columns.tolist()] + plan_risk.values.tolist()
        plan_expected = [["NARA_Plan_Type", "NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                         ["Further research required", "Low Risk", 1267, 339.72, 2],
                         ["Further research required", "Moderate Risk", 36539, 605575.06, 7],
                         ["Further research required", "High Risk", 168, 0.59, 6],
                         ["Further research required", "No Match", 0, 0.0, 0],
                         ["No plan", "Low Risk", 0, 0.0, 0],
                         ["No plan", "Moderate Risk", 0, 0.0, 0],
                         ["No plan", "High Risk", 0, 0.0, 0],
                         ["No plan", "No Match", 37, 0.01, 3],
                         ["Retain", "Low Risk", 3104, 2.01, 6],
                         ["Retain", "Moderate Risk", 6, 0.0, 2],
                         ["Retain", "High Risk", 0, 0.0, 0],
                         ["Retain", "No Match", 0, 0.0, 0],
                         ["Retain but act", "Low Risk", 218, 138.1, 1],
                         ["Retain but act", "Moderate Risk", 2, 0.0, 1],
                         ["Retain but act", "High Risk", 0, 0.0, 0],
                         ["Retain but act", "No Match", 0, 0.0, 0],
                         ["Transform", "Low Risk", 4, 0.0, 1],
                         ["Transform", "Moderate Risk", 931, 0.06, 1],
                         ["Transform", "High Risk", 0, 0.0, 0],
                         ["Transform", "No Match", 0, 0.0, 0]]
        self.assertEqual(plan_result, plan_expected, "Problem with the test for NARA PLan Type Risk")

        # Tests if the NARA Match Types sheet has the expected values.
        match_result = [match.columns.tolist()] + match.values.tolist()
        match_expected = [["NARA_Match_Type", "File_IDs", "Size (GB)", "Format Identifications"],
                          ["Manual (Test)", 37974, 605915.36, 15],
                          ["No NARA Match", 37, 0.01, 3],
                          ["PRONOM", 832, 138.12, 6],
                          ["PRONOM and Version", 3433, 2.06, 6]]
        self.assertEqual(match_result, match_expected, "Problem with the test for NARA Match Types")


if __name__ == '__main__':
    unittest.main()
