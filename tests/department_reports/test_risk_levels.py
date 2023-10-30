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

    columns_list = ["Group", "Collection", "AIP", "Format_Name", "Format_Version", "PRONOM_URL",
                    "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan",
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
        rows = [["russell", "rbrl-025", "rbrl-025-er-000001", "ACR", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "FPX", "NO VALUE", "NO VALUE",
                 "No Match", "", "No Match", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Low Risk", "Increase"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "JPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "Midi", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "MPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000003", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000003", "JPEG", "NO VALUE", "NO VALUE",
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

    def test_aip_multiple_levels(self):
        """
        Test for AIP risk levels when two of the four NARA risk levels are present.
        One occurs once and the other occurs multiple times.
        """
        # Makes a dataframe to use as test input.
        rows = [["russell", "rbrl-025", "rbrl-025-er-000001", "ACR", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "ASF", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Low Risk", "Increase"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000003", "DOT", "NO VALUE", "NO VALUE",
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
        self.assertEqual(result, expected, "Problem with test for AIP, multiple levels")

    def test_aip_remove_duplicates(self):
        """
        Test for AIP risk levels where some formats are duplicated in an AIP, once with the PUID and once without.
        These should only be counted as one format per AIP.
        """
        # Makes a dataframe to use as test input.
        rows = [["russell", "rbrl-025", "rbrl-025-er-000001", "JPEG EXIF", "7.1",
                 "https://www.nationalarchives.gov.uk/PRONOM/fmt/645", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000001", "JPEG EXIF", "7.1",
                 "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "JPEG EXIF", "7.1",
                 "https://www.nationalarchives.gov.uk/PRONOM/fmt/645", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "JPEG EXIF", "7.1",
                 "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "JPEG EXIF", "7.2",
                 "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000003", "JPEG EXIF", "7.1",
                 "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000003", "JPEG EXIF", "7.2",
                 "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"]]
        df = make_df(rows)

        # Runs the function being tested.
        aip_risk = risk_levels(df, 'AIP')

        # Tests that aip_risk contains the correct information.
        aip_risk.reset_index(inplace=True)
        result = [aip_risk.columns.tolist()] + aip_risk.values.tolist()
        expected = [["AIP", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                    ["rbrl-025-er-000001", 1, 0, 0, 0, 100],
                    ["rbrl-025-er-000002", 2, 0, 0, 0, 100],
                    ["rbrl-025-er-000003", 2, 0, 0, 0, 100]]
        self.assertEqual(result, expected, "Problem with test for AIP, remove duplicates")

    def test_collection_all_levels(self):
        """
        Test for collection risk levels when all four NARA risk levels are present.
        Some occur once and others occur multiple times.
        """
        # Makes a dataframe to use as test input.
        rows = [["russell", "rbrl-025", "rbrl-025-er-000001", "ACR", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000001", "FPX", "NO VALUE", "NO VALUE",
                 "No Match", "", "No Match", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Low Risk", "Increase"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "JPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "MOV", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000003", "MPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-026", "rbrl-026-er-000001", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-027", "rbrl-026-er-000001", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-027", "rbrl-027-er-000002", "JPEG", "NO VALUE", "NO VALUE",
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

    def test_collection_multiple_levels(self):
        """
        Test for collection risk levels when two of the four NARA risk levels are present.
        One occurs once and the other occurs multiple times.
        """
        # Makes a dataframe to use as test input.
        rows = [["russell", "rbrl-025", "rbrl-025-er-000001", "ACR", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "JPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "MOV", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-025", "rbrl-025-er-000003", "MPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-027", "rbrl-027-er-000002", "JPEG", "NO VALUE", "NO VALUE",
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
        self.assertEqual(result, expected, "Problem with test for collection, multiple levels")

    def test_collection_remove_duplicates(self):
        """
        Test for collection risk levels where some formats are duplicated in multiple AIPs.
        These should only be counted as one format per collection.
        """
        # Makes a dataframe to use as test input.
        rows = [["russell", "rbrl-025", "rbrl-025-er-000001", "JPEG EXIF", "7.1",
                 "https://www.nationalarchives.gov.uk/PRONOM/fmt/645", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000001", "JPEG EXIF", "7.1",
                 "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "FPX", "NO VALUE",
                 "NO VALUE", "No Match", "", "No Match", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000003", "FPX", "NO VALUE",
                 "NO VALUE", "No Match", "", "No Match", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000003", "JPEG EXIF", "7.1",
                 "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000004", "JPEG EXIF", "7.2",
                 "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["russell", "rbrl-026", "rbrl-026-er-000001", "FPX", "NO VALUE",
                 "NO VALUE", "No Match", "", "No Match", "Unchanged"],
                ["russell", "rbrl-026", "rbrl-026-er-000001", "JPEG EXIF", "7.2",
                 "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"]]
        df = make_df(rows)

        # Runs the function being tested.
        collection_risk = risk_levels(df, 'Collection')

        # Tests that dept_risk contains the correct information.
        collection_risk.reset_index(inplace=True)
        result = [collection_risk.columns.tolist()] + collection_risk.values.tolist()
        expected = [["Collection", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                    ["rbrl-025", 3, 33.33, 0.0, 0.0, 66.67],
                    ["rbrl-026", 2, 50, 0, 0, 50]]
        self.assertEqual(result, expected, "Problem with test for collection, remove duplicates")

    def test_dept_all_levels(self):
        """
        Test for department risk levels when all four NARA risk levels are present.
        Some occur once and others occur multiple times.
        """
        # Makes a dataframe to use as test input.
        rows = [["russell", "rbrl-025", "rbrl-025-er-000001", "ACR", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000001", "FPX", "NO VALUE", "NO VALUE",
                 "No Match", "", "No Match", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "ASF", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Low Risk", "Increase"],
                ["russell", "rbrl-025", "rbrl-025-er-000002", "dat", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"],
                ["russell", "rbrl-026", "rbrl-026-er-000001", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-026", "rbrl-026-er-000001", "FLA", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-027", "rbrl-027-er-000001", "JPEG", "NO VALUE", "NO VALUE",
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

    def test_dept_multiple_levels(self):
        """
        Test for department risk levels when two of the four NARA risk levels are present.
        One occurs once and the other occurs multiple times.
        """
        # Makes a dataframe to use as test input.
        rows = [["russell", "rbrl-025", "rbrl-025-er-000002", "ASF", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Low Risk", "Increase"],
                ["russell", "rbrl-026", "rbrl-026-er-000001", "DOT", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-026", "rbrl-026-er-000001", "FLA", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-027", "rbrl-027-er-000001", "JPEG", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "No Match", "New Match"]]
        df = make_df(rows)

        # Runs the function being tested.
        dept_risk = risk_levels(df, 'Group')

        # Tests that dept_risk contains the correct information.
        dept_risk.reset_index(inplace=True)
        result = [dept_risk.columns.tolist()] + dept_risk.values.tolist()
        expected = [["Group", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                    ["russell", 4, 0, 0, 75, 25]]
        self.assertEqual(result, expected, "Problem with test for department, multiple levels")

    def test_department_remove_duplicates(self):
        """
        Test for department risk levels where some formats are duplicated in multiple AIPs.
        These should only be counted once.
        """
        # Makes a dataframe to use as test input.
        rows = [["russell", "rbrl-025", "rbrl-025-er-000001", "JPEG EXIF", "7.1",
                 "https://www.nationalarchives.gov.uk/PRONOM/fmt/645", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["russell", "rbrl-025", "rbrl-025-er-000001", "JPEG EXIF", "7.1",
                 "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["russell", "rbrl-026", "rbrl-026-er-000001", "DOT", "NO VALUE",
                 "NO VALUE", "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-027", "rbrl-027-er-000001", "JPEG EXIF", "7.1",
                 "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["russell", "rbrl-028", "rbrl-028-er-000001", "DOT", "NO VALUE",
                 "NO VALUE", "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-028", "rbrl-028-er-000002", "ASF", "NO VALUE",
                 "NO VALUE", "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["russell", "rbrl-028", "rbrl-028-er-000002", "JPEG EXIF", "7.2",
                 "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["russell", "rbrl-028", "rbrl-028-er-000002", "JPEG EXIF", "7.2",
                 "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"]]
        df = make_df(rows)

        # Runs the function being tested.
        dept_risk = risk_levels(df, 'Group')

        # Tests that dept_risk contains the correct information.
        dept_risk.reset_index(inplace=True)
        result = [dept_risk.columns.tolist()] + dept_risk.values.tolist()
        expected = [["Group", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                    ["russell", 4, 0, 0, 50, 50]]
        self.assertEqual(result, expected, "Problem with test for department, remove duplicates")


if __name__ == '__main__':
    unittest.main()
