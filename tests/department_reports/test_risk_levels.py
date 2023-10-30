"""
Tests for the function risk_levels(),
which calculates the percentage of formats at each risk level.
Returns a dataframe.

Collections, AIP IDs, and NARA risk levels in the data were assigned to get the testing variation needed
and are not necessarily accurate. The format identifications are all present in Russell holdings.
"""
import pandas as pd
import unittest
from department_reports import risk_levels


def make_df(rows_list):
    """
    Makes a dataframe from the provided rows to use as input for tests. The columns are the same each time.
    Returns the dataframe.
    """

    columns_list = ["Group", "Collection", "AIP", "Format", "Format_Name", "Format_Version",
                    "PRONOM_URL", "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan",
                    "2021_NARA_Risk_Level", "Risk_Level_Change"]
    df = pd.DataFrame(rows_list, columns=columns_list)

    # Makes the NARA Risk Level columns ordered categorical, so risk levels can be sorted.
    # In production, this is done as part of csv_to_dataframe().
    risk_order = ["Low Risk", "Moderate Risk", "High Risk", "No Match"]
    df['2023_NARA_Risk_Level'] = pd.Categorical(df['2023_NARA_Risk_Level'], risk_order, ordered=True)
    df['2021_NARA_Risk_Level'] = pd.Categorical(df['2021_NARA_Risk_Level'], risk_order, ordered=True)

    return df


class MyTestCase(unittest.TestCase):

    def test_aip_all_levels(self):
        """
        Test for AIP risk levels when all four NARA risk levels are present.
        Some occur once and others occur multiple times.
        """
        # Makes a dataframe to use as test input.
        rows = [["russell", "rbrl-025", "rbrl-025-er-000001", "ACR (High Risk)", "ACR", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "FPX (No Match)", "FPX", "NO VALUE", "NO VALUE",
                 "No Match", "", "No Match", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "DOT (Moderate Risk)", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Low Risk", "Increase"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "JPEG (Low Risk)", "JPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "Midi (High Risk)", "Midi", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "MPEG (Low Risk)", "MPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000003", "DOT (Moderate Risk)", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000003", "JPEG (Low Risk)", "JPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"]]
        df = make_df(rows)

        # Runs the function being tested.
        aip_risk = risk_levels(df, 'AIP')

        # Tests that aip_risk contains the correct information.
        aip_risk.reset_index(inplace=True)
        result = [aip_risk.columns.tolist()] + aip_risk.values.tolist()
        expected = [["AIP", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                    ["rbrl-025-er-000001", 1, 0, 100, 0, 0],
                    ["rbrl-025-er-000002", 5, 20, 20, 20, 40],
                    ["rbrl-025-er-000003", 2, 0, 0, 50, 50]]
        self.assertEqual(result, expected, "Problem with test for AIP, all levels")

    def test_aip_two_levels(self):
        """
        Test for AIP risk levels when two of the four NARA risk levels are present.
        One occurs once and the other occurs multiple times.
        """
        # Makes a dataframe to use as test input.
        rows = [["russell", "rbrl-025", "rbrl-025-er-000001", "ACR (High Risk)", "ACR", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "ASF (Moderate Risk)", "ASF", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Low Risk", "Increase"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "DOT (Moderate Risk)", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000003", "DOT (Moderate Risk)", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"]]
        df = make_df(rows)

        # Runs the function being tested.
        aip_risk = risk_levels(df, 'AIP')

        # Tests that aip_risk contains the correct information.
        aip_risk.reset_index(inplace=True)
        result = [aip_risk.columns.tolist()] + aip_risk.values.tolist()
        expected = [["AIP", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                    ["rbrl-025-er-000001", 1, 0, 100, 0, 0],
                    ["rbrl-025-er-000002", 2, 0, 0, 100, 0],
                    ["rbrl-025-er-000003", 1, 0, 0, 100, 0]]
        self.assertEqual(result, expected, "Problem with test for AIP, two levels")

    def test_collection_all_levels(self):
        """
        Test for collection risk levels when all four NARA risk levels are present.
        Some occur once and others occur multiple times.
        """
        # Makes a dataframe to use as test input.
        rows = [["russell", "rbrl-025", "rbrl-025-er-000001", "ACR (High Risk)", "ACR", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000001", "FPX (No Match)", "FPX", "NO VALUE", "NO VALUE",
                 "No Match", "", "No Match", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "DOT (Moderate Risk)", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Low Risk", "Increase"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "JPEG (Low Risk)", "JPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "MOV (Low Risk)", "MOV", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000003", "MPEG (Low Risk)", "MPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-026", "rbrl-026-er-000001", "DOT (Moderate Risk)", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-027", "rbrl-026-er-000001", "DOT (Moderate Risk)", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-027", "rbrl-027-er-000002", "JPEG (Low Risk)", "JPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"]]
        df = make_df(rows)

        # Runs the function being tested.
        collection_risk = risk_levels(df, 'Collection')

        # Tests that collection_risk contains the correct information.
        collection_risk.reset_index(inplace=True)
        result = [collection_risk.columns.tolist()] + collection_risk.values.tolist()
        expected = [["Collection", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                    ["rbrl-025", 6, 16.67, 16.67, 16.67, 50],
                    ["rbrl-026", 1, 0, 0, 100, 0],
                    ["rbrl-027", 2, 0, 0, 50, 50]]
        self.assertEqual(result, expected, "Problem with test for collection, all levels")

    def test_collection_two_levels(self):
        """
        Test for collection risk levels when two of the four NARA risk levels are present.
        One occurs once and the other occurs multiple times.
        """
        # Makes a dataframe to use as test input.
        rows = [["russell", "rbrl-025", "rbrl-025-er-000001", "ACR (High Risk)", "ACR", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "JPEG (Low Risk)", "JPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "MOV (Low Risk)", "MOV", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000003", "MPEG (Low Risk)", "MPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-027", "rbrl-027-er-000002", "JPEG (Low Risk)", "JPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"]]
        df = make_df(rows)

        # Runs the function being tested.
        collection_risk = risk_levels(df, 'Collection')

        # Tests that dept_risk contains the correct information.
        collection_risk.reset_index(inplace=True)
        result = [collection_risk.columns.tolist()] + collection_risk.values.tolist()
        expected = [["Collection", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                    ["rbrl-025", 4, 0, 25, 0, 75],
                    ["rbrl-027", 1, 0, 0, 0, 100]]
        self.assertEqual(result, expected, "Problem with test for collection, two levels")

    def test_dept_all_levels(self):
        """
        Test for department risk levels when all four NARA risk levels are present.
        Some occur once and others occur multiple times.
        """
        # Makes a dataframe to use as test input.
        rows = [["russell", "rbrl-025", "rbrl-025-er-000001", "ACR (High Risk)", "ACR", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000001", "FPX (No Match)", "FPX", "NO VALUE", "NO VALUE",
                 "No Match", "", "No Match", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "ASF (Moderate Risk)", "ASF", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Low Risk", "Increase"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "dat (Low Risk)", "dat", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-026", "rbrl-026-er-000001", "DOT (Moderate Risk)", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-026", "rbrl-026-er-000001", "FLA (Moderate Risk)", 'FLA', "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-027", "rbrl-027-er-000001", "JPEG (Low Risk)", "JPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"]]
        df = make_df(rows)

        # Runs the function being tested.
        dept_risk = risk_levels(df, 'Group')

        # Tests that dept_risk contains the correct information.
        dept_risk.reset_index(inplace=True)
        result = [dept_risk.columns.tolist()] + dept_risk.values.tolist()
        expected = [["Group", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                    ["russell", 7, 14.29, 14.29, 42.86, 28.57]]
        self.assertEqual(result, expected, "Problem with test for department, all levels")

    def test_dept_two_levels(self):
        """
        Test for department risk levels when two of the four NARA risk levels are present.
        One occurs once and the other occurs multiple times.
        """
        # Makes a dataframe to use as test input.
        rows = [["russell", "rbrl-025", "rbrl-025-er-000002", "ASF (Moderate Risk)", "ASF", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Low Risk", "Increase"],
                ["russell", "rbrl-026", "rbrl-026-er-000001", "DOT (Moderate Risk)", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-026", "rbrl-026-er-000001", "FLA (Moderate Risk)", 'FLA', "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-027", "rbrl-027-er-000001", "JPEG (Low Risk)", "JPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"]]
        df = make_df(rows)

        # Runs the function being tested.
        dept_risk = risk_levels(df, 'Group')

        # Tests that dept_risk contains the correct information.
        dept_risk.reset_index(inplace=True)
        result = [dept_risk.columns.tolist()] + dept_risk.values.tolist()
        expected = [["Group", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                    ["russell", 4, 0, 0, 75, 25]]
        self.assertEqual(result, expected, "Problem with test for department, two levels")


if __name__ == '__main__':
    unittest.main()
