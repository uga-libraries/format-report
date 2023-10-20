"""
Tests for the function groupby_risk(),
which makes a dataframe with the number of file ids, size in GB, and format identifications
for each instance of the column or columns included in the groupby_list.
Returns the dataframe.

Test input is read from a CSV instead of being made in the test to be as close to production as possible.
"""
import os
import pandas as pd
import unittest
from reports import groupby_risk


class MyTestCase(unittest.TestCase):

    def test_archive_all_levels_dup_ids(self):
        """
        Test for when some format identifications are repeated.
        All four NARA risk levels are present.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        # In production, the order of NARA_Risk Level is set in the spreadsheet_risk() function.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2010-01.csv"))
        risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
        df_group['NARA_Risk Level'] = pd.Categorical(df_group['NARA_Risk Level'], risk_order, ordered=True)

        # Runs the function being tested.
        archive_risk = groupby_risk(df_group, ['NARA_Risk Level'])

        # Tests if archive_risk has the expected values.
        result = [archive_risk.columns.tolist()] + archive_risk.values.tolist()
        expected = [["NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["Low Risk", 3507, 39915.92, 8],
                    ["Moderate Risk", 29822, 257532.89, 5],
                    ["High Risk", 343, 140.25, 7],
                    ["No Match", 219, 138.1, 2]]
        self.assertEqual(result, expected, "Problem with test for ARCHive, all risk levels and duplicate format ids")

    def test_archive_all_levels_unique_ids(self):
        """
        Test for when all format identifications are unique.
        All four NARA risk levels are present.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        # In production, the order of NARA_Risk Level is set in the spreadsheet_risk() function.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2010-02.csv"))
        risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
        df_group['NARA_Risk Level'] = pd.Categorical(df_group['NARA_Risk Level'], risk_order, ordered=True)

        # Runs the function being tested.
        archive_risk = groupby_risk(df_group, ['NARA_Risk Level'])

        # Tests if archive_risk has the expected values.
        result = [archive_risk.columns.tolist()] + archive_risk.values.tolist()
        expected = [["NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["Low Risk", 5859, 41406.76, 7],
                    ["Moderate Risk", 35487, 604509.15, 10],
                    ["High Risk", 1964, 140.74, 10],
                    ["No Match", 249, 2.28, 6]]
        self.assertEqual(result, expected, "Problem with test for ARCHive, all risk levels and unique format ids")

    def test_archive_some_levels(self):
        """
        Test for when two of the four NARA risk levels are present.
        All format identifications are unique.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        # In production, the order of NARA_Risk Level is set in the spreadsheet_risk() function.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2010-03.csv"))
        risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
        df_group['NARA_Risk Level'] = pd.Categorical(df_group['NARA_Risk Level'], risk_order, ordered=True)

        # Runs the function being tested.
        archive_risk = groupby_risk(df_group, ['NARA_Risk Level'])

        # Tests if archive_risk has the expected values.
        result = [archive_risk.columns.tolist()] + archive_risk.values.tolist()
        expected = [["NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["Low Risk", 9285, 41548.58, 18],
                    ["Moderate Risk", 0, 0, 0],
                    ["High Risk", 191, 0.01, 6],
                    ["No Match", 0, 0, 0]]
        self.assertEqual(result, expected, "Problem with test for ARCHive, some NARA risk levels")

    def test_dept_one(self):
        """
        Test for when there is one department (group).
        All NARA risk levels are present and all format identifications are unique.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        # In production, the order of NARA_Risk Level is set in the spreadsheet_risk() function.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2011-01.csv"))
        risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
        df_group['NARA_Risk Level'] = pd.Categorical(df_group['NARA_Risk Level'], risk_order, ordered=True)

        # Runs the function being tested.
        dept_risk = groupby_risk(df_group, ['Group', 'NARA_Risk Level'])

        # Tests if archive_risk has the expected values.
        result = [dept_risk.columns.tolist()] + dept_risk.values.tolist()
        expected = [["Group", "NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["hargrett", "Low Risk", 1327, 0.82, 4],
                    ["hargrett", "Moderate Risk", 949, 0.14, 5],
                    ["hargrett", "High Risk", 19, 0, 1],
                    ["hargrett", "No Match", 125, 0.02, 4]]
        self.assertEqual(result, expected, "Problem with the test for dept, one department")

    def test_dept_three_no_overlap(self):
        """
        Test for when there are three departments (groups) and no format is in more than one department.
        Not all NARA risk levels are present and all format identifications are unique.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        # In production, the order of NARA_Risk Level is set in the spreadsheet_risk() function.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2011-02.csv"))
        risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
        df_group['NARA_Risk Level'] = pd.Categorical(df_group['NARA_Risk Level'], risk_order, ordered=True)

        # Runs the function being tested.
        dept_risk = groupby_risk(df_group, ['Group', 'NARA_Risk Level'])

        # Tests if archive_risk has the expected values.
        result = [dept_risk.columns.tolist()] + dept_risk.values.tolist()
        expected = [["Group", "NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["bmac", "Low Risk", 122, 39775.16, 1],
                    ["bmac", "Moderate Risk", 0, 0, 0],
                    ["bmac", "High Risk", 0, 0, 0],
                    ["bmac", "No Match", 0, 0, 0],
                    ["dlg-magil", "Low Risk", 5854, 1629.09, 4],
                    ["dlg-magil", "Moderate Risk", 0, 0, 0],
                    ["dlg-magil", "High Risk", 0, 0, 0],
                    ["dlg-magil", "No Match", 0, 0, 0],
                    ["hargrett", "Low Risk", 1873, 140.22, 11],
                    ["hargrett", "Moderate Risk", 0, 0, 0],
                    ["hargrett", "High Risk", 19, 0, 1],
                    ["hargrett", "No Match", 399, 138.12, 6]]
        self.assertEqual(result, expected, "Problem with the test for dept, three departments, no overlap")

    def test_dept_three_overlap(self):
        """
        Test for when there are three departments (groups) and some formats are in more than one department.
        Not all NARA risk levels are present and some format identifications are repeated.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        # In production, the order of NARA_Risk Level is set in the spreadsheet_risk() function.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2011-03.csv"))
        risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
        df_group['NARA_Risk Level'] = pd.Categorical(df_group['NARA_Risk Level'], risk_order, ordered=True)

        # Runs the function being tested.
        dept_risk = groupby_risk(df_group, ['Group', 'NARA_Risk Level'])

        # Tests if archive_risk has the expected values.
        result = [dept_risk.columns.tolist()] + dept_risk.values.tolist()
        expected = [["Group", "NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["bmac", "Low Risk", 122, 39775.16, 1],
                    ["bmac", "Moderate Risk", 30235, 262809.42, 4],
                    ["bmac", "High Risk", 0, 0.0, 0],
                    ["bmac", "No Match", 0, 0.0, 0],
                    ["dlg-magil", "Low Risk", 5854, 1629.09, 4],
                    ["dlg-magil", "Moderate Risk", 0, 0.0, 0],
                    ["dlg-magil", "High Risk", 0, 0.0, 0],
                    ["dlg-magil", "No Match", 0, 0.0, 0],
                    ["hargrett", "Low Risk", 7000, 8.74, 10],
                    ["hargrett", "Moderate Risk", 476, 2.3, 14],
                    ["hargrett", "High Risk", 0, 0.0, 0],
                    ["hargrett", "No Match", 0, 0.0, 0]]
        self.assertEqual(result, expected, "Problem with the test for dept, three departments, overlap")

    def test_type_one(self):
        """
        Test for when there is one type.
        Not all NARA risk levels are present and all format identifications are unique.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        # In production, the order of NARA_Risk Level is set in the spreadsheet_risk() function.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2011-03.csv"))
        risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
        df_group['NARA_Risk Level'] = pd.Categorical(df_group['NARA_Risk Level'], risk_order, ordered=True)

        # Runs the function being tested.
        dept_risk = groupby_risk(df_group, ['Group', 'NARA_Risk Level'])

        # Tests if archive_risk has the expected values.
        result = [dept_risk.columns.tolist()] + dept_risk.values.tolist()
        expected = [["Format Type", "NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["bmac", "Low Risk", 122, 39775.16, 1],
                    ["bmac", "Moderate Risk", 30235, 262809.42, 4],
                    ["bmac", "High Risk", 0, 0.0, 0],
                    ["bmac", "No Match", 0, 0.0, 0],
                    ["dlg-magil", "Low Risk", 5854, 1629.09, 4],
                    ["dlg-magil", "Moderate Risk", 0, 0.0, 0],
                    ["dlg-magil", "High Risk", 0, 0.0, 0],
                    ["dlg-magil", "No Match", 0, 0.0, 0],
                    ["hargrett", "Low Risk", 7000, 8.74, 10],
                    ["hargrett", "Moderate Risk", 476, 2.3, 14],
                    ["hargrett", "High Risk", 0, 0.0, 0],
                    ["hargrett", "No Match", 0, 0.0, 0]]
        self.assertEqual(result, expected, "Problem with the test for dept, three departments, overlap")

    def test_type_multiple_one_risk(self):
        """
        Test for when there are three departments (groups) and some formats are in more than one department.
        All NARA risk levels are present and all format identifications are unique.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        # In production, the order of NARA_Risk Level is set in the spreadsheet_risk() function.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2011-03.csv"))
        risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
        df_group['NARA_Risk Level'] = pd.Categorical(df_group['NARA_Risk Level'], risk_order, ordered=True)

        # Runs the function being tested.
        dept_risk = groupby_risk(df_group, ['Group', 'NARA_Risk Level'])

        # Tests if archive_risk has the expected values.
        result = [dept_risk.columns.tolist()] + dept_risk.values.tolist()
        expected = [["Format Type", "NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["bmac", "Low Risk", 122, 39775.16, 1],
                    ["bmac", "Moderate Risk", 30235, 262809.42, 4],
                    ["bmac", "High Risk", 0, 0.0, 0],
                    ["bmac", "No Match", 0, 0.0, 0],
                    ["dlg-magil", "Low Risk", 5854, 1629.09, 4],
                    ["dlg-magil", "Moderate Risk", 0, 0.0, 0],
                    ["dlg-magil", "High Risk", 0, 0.0, 0],
                    ["dlg-magil", "No Match", 0, 0.0, 0],
                    ["hargrett", "Low Risk", 7000, 8.74, 10],
                    ["hargrett", "Moderate Risk", 476, 2.3, 14],
                    ["hargrett", "High Risk", 0, 0.0, 0],
                    ["hargrett", "No Match", 0, 0.0, 0]]
        self.assertEqual(result, expected, "Problem with the test for dept, three departments, overlap")

    def test_type_multiple_many_risk(self):
        """
        Test for when there are three departments (groups) and some formats are in more than one department.
        Not all NARA risk levels are present and some format identifications are repeated.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        # In production, the order of NARA_Risk Level is set in the spreadsheet_risk() function.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2011-03.csv"))
        risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
        df_group['NARA_Risk Level'] = pd.Categorical(df_group['NARA_Risk Level'], risk_order, ordered=True)

        # Runs the function being tested.
        dept_risk = groupby_risk(df_group, ['Group', 'NARA_Risk Level'])

        # Tests if archive_risk has the expected values.
        result = [dept_risk.columns.tolist()] + dept_risk.values.tolist()
        expected = [["Group", "NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["bmac", "Low Risk", 122, 39775.16, 1],
                    ["bmac", "Moderate Risk", 30235, 262809.42, 4],
                    ["bmac", "High Risk", 0, 0.0, 0],
                    ["bmac", "No Match", 0, 0.0, 0],
                    ["dlg-magil", "Low Risk", 5854, 1629.09, 4],
                    ["dlg-magil", "Moderate Risk", 0, 0.0, 0],
                    ["dlg-magil", "High Risk", 0, 0.0, 0],
                    ["dlg-magil", "No Match", 0, 0.0, 0],
                    ["hargrett", "Low Risk", 7000, 8.74, 10],
                    ["hargrett", "Moderate Risk", 476, 2.3, 14],
                    ["hargrett", "High Risk", 0, 0.0, 0],
                    ["hargrett", "No Match", 0, 0.0, 0]]
        self.assertEqual(result, expected, "Problem with the test for dept, three departments, overlap")
if __name__ == '__main__':
    unittest.main()
