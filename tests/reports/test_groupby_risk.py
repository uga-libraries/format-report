"""
Tests for the function groupby_risk(),
which makes a dataframe with the number of file ids, size in GB, and format identifications
for each instance of the column or columns included in the groupby_list.
Returns the dataframe.

Test input is read from a CSV instead of being made in the test to be as close to production as possible.
"""
import numpy as np
import os
import pandas as pd
import unittest
from reports import groupby_risk


def update_dataframe(df):
    """
    Assigns order to the NARA risk categories and adds NARA_Plan_Type.
    In production, this is done as part of the spreadsheet_risk() function.
    """
    # Assigns an order to the NARA risk categories, so results are in order of increasing risk.
    risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
    df['NARA_Risk Level'] = pd.Categorical(df['NARA_Risk Level'], risk_order, ordered=True)

    # Makes a new column to classify the type of NARA preservation action plan.
    conditions = [(df['NARA_Proposed Preservation Plan'].notnull()) &
                  (df['NARA_Proposed Preservation Plan'].str.startswith("Depends on version")),
                  (df['NARA_Proposed Preservation Plan'].notnull()) &
                  (df['NARA_Proposed Preservation Plan'].str.startswith("Further research is required")),
                  df['NARA_Proposed Preservation Plan'] == "Retain",
                  (df['NARA_Proposed Preservation Plan'].notnull()) &
                  (df['NARA_Proposed Preservation Plan'].str.startswith("Retain ")),
                  (df['NARA_Proposed Preservation Plan'].notnull()) &
                  (df['NARA_Proposed Preservation Plan'].str.startswith("Transform"))]
    plan_type = ["Depends on version", "Further research required", "Retain", "Retain but act", "Transform"]
    df["NARA_Plan_Type"] = np.select(conditions, plan_type)

    return df


class MyTestCase(unittest.TestCase):

    def test_archive_all_levels_dup_ids(self):
        """
        Test for when some format identifications are repeated.
        All four NARA risk levels are present.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2010-01.csv"))
        df_group = update_dataframe(df_group)

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
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2010-02.csv"))
        df_group = update_dataframe(df_group)

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
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2010-03.csv"))
        df_group = update_dataframe(df_group)

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
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2011-01.csv"))
        df_group = update_dataframe(df_group)

        # Runs the function being tested.
        dept_risk = groupby_risk(df_group, ['Group', 'NARA_Risk Level'])

        # Tests if dept_risk has the expected values.
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
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2011-02.csv"))
        df_group = update_dataframe(df_group)

        # Runs the function being tested.
        dept_risk = groupby_risk(df_group, ['Group', 'NARA_Risk Level'])

        # Tests if dept_risk has the expected values.
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
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2011-03.csv"))
        df_group = update_dataframe(df_group)

        # Runs the function being tested.
        dept_risk = groupby_risk(df_group, ['Group', 'NARA_Risk Level'])

        # Tests if dept_risk has the expected values.
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

    def test_match_multiple(self):
        """
        Test for when there are multiple NARA match types, each more than once.
        Some format identifications are repeated.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2012-01.csv"))
        df_group = update_dataframe(df_group)

        # Runs the function being tested.
        match = groupby_risk(df_group, ['NARA_Match_Type'])

        # Tests if match_risk has the expected values.
        result = [match.columns.tolist()] + match.values.tolist()
        expected = [["NARA_Match_Type", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["Format Name", 60, 0.01, 2],
                    ["No NARA Match", 399, 138.12, 6],
                    ["PRONOM", 1487, 138.14, 8],
                    ["PRONOM and Name", 229, 1.76, 4],
                    ["PRONOM and Version", 8296, 6.69, 14]]
        self.assertEqual(result, expected, "Problem with the test for multiple NARA match types")

    def test_match_multiple_once(self):
        """
        Test for when there are multiple NARA match types, each only once.
        All format identifications are unique.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2012-02.csv"))
        df_group = update_dataframe(df_group)

        # Runs the function being tested.
        match = groupby_risk(df_group, ['NARA_Match_Type'])

        # Tests if match_risk has the expected values.
        result = [match.columns.tolist()] + match.values.tolist()
        expected = [["NARA_Match_Type", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["Format Name", 48, 0.0, 1],
                    ["PRONOM", 565, 0, 1],
                    ["PRONOM and Name", 33, 0.47, 1]]
        self.assertEqual(result, expected, "Problem with the test multiple NARA match types, each match once")

    def test_match_one(self):
        """
        Test for when there is one NARA match type.
        All format identifications are unique.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2012-03.csv"))
        df_group = update_dataframe(df_group)

        # Runs the function being tested.
        match = groupby_risk(df_group, ['NARA_Match_Type'])

        # Tests if match_risk has the expected values.
        result = [match.columns.tolist()] + match.values.tolist()
        expected = [["NARA_Match_Type", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["PRONOM and Version", 5123, 4.62, 4]]
        self.assertEqual(result, expected, "Problem with the test for one match")

    def test_type_one(self):
        """
        Test for when there is one format type.
        Not all NARA risk levels are present and all format identifications are unique.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2013-01.csv"))

        # Runs the function being tested.
        type_risk = groupby_risk(df_group, ['Format Type', 'NARA_Risk Level'])

        # Tests if type_risk has the expected values.
        result = [type_risk.columns.tolist()] + type_risk.values.tolist()
        expected = [["Format Type", "NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["image", "Low Risk", 13375, 41414.64, 18],
                    ["image", "Moderate Risk", 2579, 4.02, 8]]
        self.assertEqual(result, expected, "Problem with the test for one type")

    def test_type_multiple_one_risk(self):
        """
        Test for when there are multiple types, and each type has one risk level.
        Not all NARA risk levels are present and all format identifications are unique.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2013-02.csv"))
        df_group = update_dataframe(df_group)

        # Runs the function being tested.
        type_risk = groupby_risk(df_group, ['Format Type', 'NARA_Risk Level'])

        # Tests if type_risk has the expected values.
        result = [type_risk.columns.tolist()] + type_risk.values.tolist()
        expected = [["Format Type", "NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["application", "Low Risk", 0, 0.0, 0],
                    ["application", "Moderate Risk", 0, 0.0, 0],
                    ["application", "High Risk", 141, 0.04, 5],
                    ["application", "No Match", 0, 0.0, 0],
                    ["archive", "Low Risk", 0, 0.0, 0],
                    ["archive", "Moderate Risk", 220, 138.1, 2],
                    ["archive", "High Risk", 0, 0.0, 0],
                    ["archive", "No Match", 0, 0.0, 0],
                    ["web_archive", "Low Risk", 0, 0.0, 0],
                    ["web_archive", "Moderate Risk", 0, 0.0, 0],
                    ["web_archive", "High Risk", 0, 0.0, 0],
                    ["web_archive", "No Match", 218, 138.1, 1]]
        self.assertEqual(result, expected, "Problem with the test for multiple types, one risk each")

    def test_type_multiple_many_risk(self):
        """
        Test for when there are multiple types, and types have more than one risk level.
        All NARA risk levels are present and some format identifications are repeated.
        """
        # Makes the dataframe used for the function input and sets the order of NARA_Risk Level.
        df_group = pd.read_csv(os.path.join("groupby_risk", "archive_formats_by_group_2013-03.csv"))
        df_group = update_dataframe(df_group)

        # Runs the function being tested.
        type_risk = groupby_risk(df_group, ['Format Type', 'NARA_Risk Level'])

        # Tests if type_risk has the expected values.
        result = [type_risk.columns.tolist()] + type_risk.values.tolist()
        expected = [["Format Type", "NARA_Risk Level", "File_IDs", "Size (GB)", "Format Identifications"],
                    ["audio", "Low Risk", 0, 0.0, 0],
                    ["audio", "Moderate Risk", 0, 0.0, 0],
                    ["audio", "High Risk", 1166, 1065.99, 1],
                    ["audio", "No Match", 0, 0.0, 0],
                    ["structured_text", "Low Risk", 590, 0.0, 2],
                    ["structured_text", "Moderate Risk", 0, 0.0, 0],
                    ["structured_text", "High Risk", 4, 0.0, 1],
                    ["structured_text", "No Match", 0, 0.0, 0],
                    ["text", "Low Risk", 629, 0.0, 2],
                    ["text", "Moderate Risk", 111, 0.01, 3],
                    ["text", "High Risk", 63, 0.0, 1],
                    ["text", "No Match", 57, 0.0, 2],
                    ["video", "Low Risk", 37, 0.47, 2],
                    ["video", "Moderate Risk", 35418, 604509.14, 7],
                    ["video", "High Risk", 252, 1.46, 7],
                    ["video", "No Match", 124, 0.02, 3]]
        self.assertEqual(result, expected, "Problem with the test for multiple types, multiple risks")


if __name__ == '__main__':
    unittest.main()
