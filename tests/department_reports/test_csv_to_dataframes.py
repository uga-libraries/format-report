"""
Tests for the function csv_to_dataframes(),
which reads the format CSV into a dataframe, handles encoding errors, does clean up,
and returns a list of dataframes, one dataframe for each group.
"""

import os
import unittest
from department_reports import csv_to_dataframes


class MyTestCase(unittest.TestCase):

    def test_encoding_error(self):
        """
        Test for reading an archive_formats_by_aip CSV with an encoding error.
        """
        # Runs the function being tested.
        # NOTE: the function prints an error message to the terminal if it is working correctly.
        format_csv = os.path.join("csv_to_dataframes", "archive_formats_by_aip_encoding-error.csv")
        department_dfs = csv_to_dataframes(format_csv)

        # Tests that the resulting list of dataframes contains the correct number of items.
        self.assertEqual(len(department_dfs), 1, "Problem with test for encoding error, list count")

        # Tests that the dataframe in the list contains the correct information.
        result = [department_dfs[0].columns.to_list()] + department_dfs[0].values.tolist()
        expected = [["Group", "Collection", "AIP", "Format Name", "Format Version", "PRONOM URL",
                     "NARA_Risk Level", "NARA_Proposed Preservation Plan"],
                    ["bmac", "peabody", "bmac_2000002pst-arch", "Matroska", "NO VALUE", "NO VALUE",
                     "No Match", "NO VALUE"],
                    ["bmac", "peabody", "bmac_2000023pst-arch", "Matroska", "NO VALUE", "NO VALUE",
                     "No Match", "NO VALUE"]]
        self.assertEqual(result, expected, "Problem with test for encoding error, df contents")

    def test_multi_groups(self):
        """
        Test for reading an archive_formats_by_aip CSV with multiple groups.
        Some groups have one format and others have multiple formats.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframes", "archive_formats_by_aip_multiple.csv")
        department_dfs = csv_to_dataframes(format_csv)

        # Tests that the resulting list of dataframes contains the correct number of items.
        self.assertEqual(len(department_dfs), 3, "Problem with test for multiple groups, list count")

        # Tests that the first dataframe in the list contains the correct information.
        result = [department_dfs[0].columns.to_list()] + department_dfs[0].values.tolist()
        expected = [["Group", "Collection", "AIP", "Format Name", "Format Version", "PRONOM URL",
                     "NARA_Risk Level", "NARA_Proposed Preservation Plan"],
                    ["bmac", "peabody", "bmac_51021enr-1a", "Wave", "NO VALUE", "NO VALUE",
                     "Low Risk", "Retain"]]
        self.assertEqual(result, expected, "Problem with test for multiple groups, first df contents")

        # Tests that the second dataframe in the list contains the correct information.
        result = [department_dfs[1].columns.to_list()] + department_dfs[1].values.tolist()
        expected = [["Group", "Collection", "AIP", "Format Name", "Format Version", "PRONOM URL",
                     "NARA_Risk Level", "NARA_Proposed Preservation Plan"],
                    ["dlg", "arl_acl", "arl_acl_acl332", "Tagged Image File Format", "6",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/353", "Low Risk", "Retain"],
                    ["dlg", "zhj_tecc", "zhj_tecc_rml-ohp-001", "Waveform Audio", "NO VALUE", "NO VALUE",
                     "Low Risk", "Retain"]]
        self.assertEqual(result, expected, "Problem with test for multiple groups, second df contents")

        # Tests that the third dataframe in the list contains the correct information.
        result = [department_dfs[2].columns.to_list()] + department_dfs[2].values.tolist()
        expected = [["Group", "Collection", "AIP", "Format Name", "Format Version", "PRONOM URL",
                     "NARA_Risk Level", "NARA_Proposed Preservation Plan"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0007", "Tagged Image File Format", "NO VALUE", "NO VALUE",
                     "Low Risk", "Depends on version, retain TIFF 1-6, otherwise see specific version plan"],
                    ["hargrett", "harg-0000", "harg-0000-web-202007-0001", "WARC", "NO VALUE",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/289", "Low Risk", "Retain"],
                    ["hargrett", "harg-0000", "harg-0000-web-202007-0002", "WARC", "NO VALUE",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/289", "Low Risk", "Retain"]]
        self.assertEqual(result, expected, "Problem with test for multiple groups, third df contents")

    def test_puid_all(self):
        """
        Test for reading an archive_formats_by_aip CSV with one group and all formats have a PRONOM URL.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframes", "archive_formats_by_aip_puid-all.csv")
        department_dfs = csv_to_dataframes(format_csv)

        # Tests that the resulting list of dataframes contains the correct number of items.
        self.assertEqual(len(department_dfs), 1, "Problem with test for PUID: all, list count")

        # Tests that the dataframe in the list contains the correct information.
        result = [department_dfs[0].columns.to_list()] + department_dfs[0].values.tolist()
        expected = [["Group", "Collection", "AIP", "Format Name", "Format Version", "PRONOM URL",
                     "NARA_Risk Level", "NARA_Proposed Preservation Plan"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0013", "JPEG EXIF", "2.1",
                     "https://www.nationalarchives.gov.uk/pronom/x-fmt/390", "Low Risk", "Retain"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0016", "JPEG EXIF", "2.1",
                     "https://www.nationalarchives.gov.uk/pronom/x-fmt/390", "Low Risk", "Retain"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0001", "JPEG File Interchange Format", "1.01",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/43", "Low Risk", "Retain"]]
        self.assertEqual(result, expected, "Problem with test for PUID: all, df contents")

    def test_puid_mix(self):
        """
        Test for reading an archive_formats_by_aip CSV with one group and some formats have a PRONOM URL.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframes", "archive_formats_by_aip_puid-mix.csv")
        department_dfs = csv_to_dataframes(format_csv)

        # Tests that the resulting list of dataframes contains the correct number of items.
        self.assertEqual(len(department_dfs), 1, "Problem with test for PUID: mix, list count")

        # Tests that the dataframe in the list contains the correct information.
        result = [department_dfs[0].columns.to_list()] + department_dfs[0].values.tolist()
        expected = [["Group", "Collection", "AIP", "Format Name", "Format Version", "PRONOM URL",
                     "NARA_Risk Level", "NARA_Proposed Preservation Plan"],
                    ["dlg", "arl_nnc", "arl_nnc_nnc004-001-003", "Tagged Image File Format", "5", "NO VALUE",
                     "Low Risk", "Retain"],
                    ["dlg", "arl_acl", "arl_acl_acl328", "Tagged Image File Format", "6",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/353", "Low Risk", "Retain"],
                    ["dlg", "arl_acl", "arl_acl_acl329", "Tagged Image File Format", "6",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/353", "Low Risk", "Retain"],
                    ["dlg", "guan_ms40", "dlg_turningpoint_harg0040-001-002", "Tagged Image File Format", "NO VALUE",
                     "NO VALUE", "Low Risk", "Depends on version, retain TIFF 1-6, otherwise see specific version plan"]]
        self.assertEqual(result, expected, "Problem with test for PUID: mix, df contents")

    def test_puid_none(self):
        """
        Test for reading an archive_formats_by_aip CSV with one group and no formats have a PRONOM URL.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframes", "archive_formats_by_aip_puid-none.csv")
        department_dfs = csv_to_dataframes(format_csv)

        # Tests that the resulting list of dataframes contains the correct number of items.
        self.assertEqual(len(department_dfs), 1, "Problem with test for PUID: none, list count")

        # Tests that the dataframe in the list contains the correct information.
        result = [department_dfs[0].columns.to_list()] + department_dfs[0].values.tolist()
        expected = [["Group", "Collection", "AIP", "Format Name", "Format Version", "PRONOM URL",
                     "NARA_Risk Level", "NARA_Proposed Preservation Plan"],
                    ["bmac", "peabody", "bmac_2000002pst-arch", "Matroska", "NO VALUE", "NO VALUE",
                     "No Match", "NO VALUE"],
                    ["bmac", "peabody", "bmac_2000023pst-arch", "Matroska", "NO VALUE", "NO VALUE",
                     "No Match", "NO VALUE"]]
        self.assertEqual(result, expected, "Problem with test for PUID: none, df contents")


if __name__ == "__main__":
    unittest.main()
