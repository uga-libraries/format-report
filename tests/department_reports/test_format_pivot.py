"""
Test for the function format_pivot(),
which makes a pivot table to indicate which formats are in each Collection and AIP.
Returns a dataframe.

NARA risk levels in the data were assigned to get the testing variation needed and are not necessarily accurate.
The Hargrett format identification information is accurate, other than a format may not be part of the specified AIP.
"""
import pandas as pd
import unittest
from department_reports import formats_pivot


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

    def test_aip_multiple(self):
        """
        Test for one AIP per collection when there are multiple formats per AIP and NARA risk level.
        All NARA risk levels are included.
        """
        # Makes a dataframe to use as test input.
        rows = [["hargrett", "har-ua20-002", "har-ua20-002_0002_metadata", "xml", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["hargrett", "har-ua20-002", "har-ua20-002_0002_metadata", "Plain text", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["hargrett", "harg-0000", "harg-0000-web-202007-0002", "GZIP Format", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["hargrett", "harg-0000", "harg-0000-web-202007-0002", "TIFF EXIF", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["hargrett", "harg-ms3770", "harg-ms3770er0002", "Plain text", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["hargrett", "harg-ms3770", "harg-ms3770er0002", "MPEG-PS", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["hargrett", "harg-ms3770", "harg-ms3770er0002", "MPEG video", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["hargrett", "harg-ms3786", "harg-ms3786er0020", "MPEG-PS", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["hargrett", "harg-ms3786", "harg-ms3786er0020", "MPEG video", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["hargrett", "harg-ms3786", "harg-ms3786er0020", "Quicktime video", "NO VALUE", "NO VALUE",
                 "No Match", "Retain", "No Match", "Unchanged"],
                ["hargrett", "harg-ms3786", "harg-ms3786er0020", "SWF", "NO VALUE", "NO VALUE",
                 "No Match", "Retain", "No Match", "Unchanged"]]
        df = make_df(rows)

        # Runs the function being tested.
        formats = formats_pivot(df)

        # Tests that formats contains the correct information.
        formats.reset_index(inplace=True)
        result = [formats.columns.tolist()] + formats.values.tolist()
        expected = [[("Collection", "", ""), ("AIP", "", ""),
                     ("Format_Name", "No Match", "Quicktime video (No Match)"),
                     ("Format_Name", "No Match", "SWF (No Match)"),
                     ("Format_Name", "High Risk", "GZIP Format (High Risk)"),
                     ("Format_Name", "Moderate Risk", "MPEG video (Moderate Risk)"),
                     ("Format_Name", "Moderate Risk", "MPEG-PS (Moderate Risk)"),
                     ("Format_Name", "Moderate Risk", "xml (Moderate Risk)"),
                     ("Format_Name", "Low Risk", "Plain text (Low Risk)"),
                     ("Format_Name", "Low Risk", "TIFF EXIF (Low Risk)")],
                    ["har-ua20-002", "har-ua20-002_0002_metadata", False, False, False, False, False, True, True, False],
                    ["harg-0000", "harg-0000-web-202007-0002", False, False, True, False, False, False, False, True],
                    ["harg-ms3770", "harg-ms3770er0002", False, False, False, True, True, False, True, False],
                    ["harg-ms3786", "harg-ms3786er0020", True, True, False, True, True, False, False, False]]
        self.assertEqual(result, expected, "Problem with test for one AIP, multiple formats")

    def test_aip_one(self):
        """
        Test for one AIP per collection when there is one format per AIP and NARA risk level.
        All NARA risk levels are included.
        """
        # Makes a dataframe to use as test input.
        rows = [["hargrett", "har-ua20-002", "har-ua20-002_0001_metadata", "xml", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["hargrett", "harg-0000", "harg-0000-web-202007-0001", "GZIP Format", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["hargrett", "harg-ms3770", "harg-ms3770er0002", "Plain text", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["hargrett", "harg-ms3786", "harg-ms3786er0007",  "NEF EXIF", "NO VALUE", "NO VALUE",
                 "No Match", "Retain", "No Match", "Unchanged"]]
        df = make_df(rows)

        # Runs the function being tested.
        formats = formats_pivot(df)

        # Tests that formats contains the correct information.
        formats.reset_index(inplace=True)
        result = [formats.columns.tolist()] + formats.values.tolist()
        expected = [[("Collection", "", ""), ("AIP", "", ""),
                     ("Format_Name", "No Match", "NEF EXIF (No Match)"),
                     ("Format_Name", "High Risk", "GZIP Format (High Risk)"),
                     ("Format_Name", "Moderate Risk", "xml (Moderate Risk)"),
                     ("Format_Name", "Low Risk", "Plain text (Low Risk)")],
                    ["har-ua20-002", "har-ua20-002_0001_metadata", False, False, True, False],
                    ["harg-0000", "harg-0000-web-202007-0001", False, True, False, False],
                    ["harg-ms3770", "harg-ms3770er0002", False, False, False, True],
                    ["harg-ms3786", "harg-ms3786er0007", True, False, False, False]]
        self.assertEqual(result, expected, "Problem with test for one AIP, one format")

    def test_aips_multiple(self):
        """
        Test for multiple AIPs per collection when there are multiple formats per AIP and NARA risk level.
        Two of the NARA risk levels are included.
        """
        # Makes a dataframe to use as test input.
        rows = [["hargrett", "harg-ms3770", "harg-ms3770er0002", "xml", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["hargrett", "harg-ms3770", "harg-ms3770er0002", "Plain text", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["hargrett", "harg-ms3770", "harg-ms3770er0001", "Plain text", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["hargrett", "harg-ms3770", "harg-ms3770er0001", "JPEG EXIF", "1.2", "NO VALUE",
                 "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["hargrett", "harg-ms3796", "harg-ms3796er0007", "xml", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["hargrett", "harg-ms3796", "harg-ms3796er0007", "MPEG video", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["hargrett", "harg-ms3796", "harg-ms3796er0025", "JPEG EXIF", "1.2", "NO VALUE",
                 "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["hargrett", "harg-ms3796", "harg-ms3796er0025", "TIFF EXIF", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["hargrett", "harg-ms3796", "harg-ms3796er0025", "Plain text", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "Low Risk", "Unchanged"]]
        df = make_df(rows)

        # Runs the function being tested.
        formats = formats_pivot(df)

        # Tests that formats contains the correct information.
        formats.reset_index(inplace=True)
        result = [formats.columns.tolist()] + formats.values.tolist()
        expected = [[("Collection", "", ""), ("AIP", "", ""),
                     ("Format_Name", "Moderate Risk", "MPEG video (Moderate Risk)"),
                     ("Format_Name", "Moderate Risk", "xml (Moderate Risk)"),
                     ("Format_Name", "Low Risk", "JPEG EXIF 1.2 (Low Risk)"),
                     ("Format_Name", "Low Risk", "Plain text (Low Risk)"),
                     ("Format_Name", "Low Risk", "TIFF EXIF (Low Risk)")],
                    ["harg-ms3770", "harg-ms3770er0001", False, False, True, True, False],
                    ["harg-ms3770", "harg-ms3770er0002", False, True, False, True, False],
                    ["harg-ms3796", "harg-ms3796er0007", True, True, False, False, False],
                    ["harg-ms3796", "harg-ms3796er0025", False, False, True, True, True]]
        self.assertEqual(result, expected, "Problem with test for multiple AIPs, multiple formats")

    def test_aips_one(self):
        """
        Test for multiple AIPs per collection when there is one format per AIP and NARA risk level.
        All NARA risk levels are included.
        """
        # Makes a dataframe to use as test input.
        rows = [["hargrett", "harg-ms3786", "harg-ms3786er0012", "xml", "NO VALUE", "NO VALUE",
                 "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"],
                ["hargrett", "harg-ms3770", "harg-ms3770er0001", "GZIP Format", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["hargrett", "harg-ms3770", "harg-ms3770er0002", "Plain text", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["hargrett", "harg-ms3786", "harg-ms3786er0007", "NEF EXIF", "NO VALUE", "NO VALUE",
                 "No Match", "Retain", "No Match", "Unchanged"]]
        df = make_df(rows)

        # Runs the function being tested.
        formats = formats_pivot(df)

        # Tests that formats contains the correct information.
        formats.reset_index(inplace=True)
        result = [formats.columns.tolist()] + formats.values.tolist()
        expected = [[("Collection", "", ""), ("AIP", "", ""),
                     ("Format_Name", "No Match", "NEF EXIF (No Match)"),
                     ("Format_Name", "High Risk", "GZIP Format (High Risk)"),
                     ("Format_Name", "Moderate Risk", "xml (Moderate Risk)"),
                     ("Format_Name", "Low Risk", "Plain text (Low Risk)")],
                    ["harg-ms3770", "harg-ms3770er0001", False, True, False, False],
                    ["harg-ms3770", "harg-ms3770er0002", False, False, False, True],
                    ["harg-ms3786", "harg-ms3786er0007", True, False, False, False],
                    ["harg-ms3786", "harg-ms3786er0012", False, False, True, False]]
        self.assertEqual(result, expected, "Problem with test for multiple AIPs, one format")

    def test_puid_duplicates(self):
        """
        Test for when the same format may be repeated in an AIP, once with and once without a PUID.
        There are collections with one and with multiple AIPs. Two of the NARA risk levels are included.
        """
        # Makes a dataframe to use as test input.
        rows = [["hargrett", "harg-0000", "harg-0000-web-202007-0001", "GZIP Format", "NO VALUE", "NO VALUE",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["hargrett", "harg-0000", "harg-0000-web-202007-0001", "GZIP Format", "NO VALUE",
                 "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/266",
                 "High Risk", "Retain", "High Risk", "Unchanged"],
                ["hargrett", "harg-ms3786", "harg-ms3786er0004", "Plain text", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["hargrett", "harg-ms3786", "harg-ms3786er0024", "Plain text", "NO VALUE"
                 "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/266",
                 "Low Risk", "Retain", "Low Risk", "Unchanged"],
                ["hargrett", "harg-ms3786", "harg-ms3786er0024", "Plain text", "NO VALUE", "NO VALUE",
                 "Low Risk", "Retain", "Low Risk", "Unchanged"]]
        df = make_df(rows)

        # Runs the function being tested.
        formats = formats_pivot(df)

        # Tests that formats contains the correct information.
        formats.reset_index(inplace=True)
        result = [formats.columns.tolist()] + formats.values.tolist()
        expected = [[("Collection", "", ""), ("AIP", "", ""),
                     ("Format_Name", "High Risk", "GZIP Format (High Risk)"),
                     ("Format_Name", "Low Risk", "Plain text (Low Risk)")],
                    ["harg-0000", "harg-0000-web-202007-0001", True, False],
                    ["harg-ms3786", "harg-ms3786er0004", False, True],
                    ["harg-ms3786", "harg-ms3786er0024", False, True]]
        self.assertEqual(result, expected, "Problem with test for PUID duplicates")


if __name__ == '__main__':
    unittest.main()
