"""
Tests for the function csv_to_dataframe(),
which reads the previous or current format CSV into a dataframe, handles encoding errors, does clean up,
and returns the dataframe.
"""

import os
import unittest
from department_reports import csv_to_dataframe


class MyTestCase(unittest.TestCase):

    def test_encoding_error(self):
        """
        Test for an archive_formats_by_aip CSV with an encoding error.
        """
        # Runs the function being tested.
        # NOTE: the function prints an error message to the terminal if it is working correctly.
        format_csv = os.path.join("csv_to_dataframe", "archive_formats_by_aip_encoding-error_2023-08.csv")
        format_df = csv_to_dataframe(format_csv)

        # Tests that the dataframe contains the correct information.
        result = [format_df.columns.to_list()] + format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format", "Format_Name", "Format_Version", "PRONOM_URL",
                     "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan"],
                    ["bmac", "peabody", "bmac_2000002pst-arch", "Matroska (No Match)", "Matroska", "NO VALUE",
                     "NO VALUE", "No Match", "NO VALUE"],
                    ["bmac", "peabody", "bmac_2000023pst-arch", "Matroska (No Match)", "Matroska", "NO VALUE",
                     "NO VALUE", "No Match", "NO VALUE"]]
        self.assertEqual(result, expected, "Problem with test for encoding error")

    def test_multi_groups(self):
        """
        Test for an archive_formats_by_aip CSV with multiple groups.
        Some groups have one format and others have multiple formats.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframe", "archive_formats_by_aip_multiple_2023-08.csv")
        format_df = csv_to_dataframe(format_csv)

        # Tests that the dataframe contains the correct information.
        result = [format_df.columns.to_list()] + format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format", "Format_Name", "Format_Version", "PRONOM_URL",
                     "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan"],
                    ["dlg", "arl_acl", "arl_acl_acl332", "Tagged Image File Format 6 (Low Risk)",
                     "Tagged Image File Format", "6", "https://www.nationalarchives.gov.uk/PRONOM/fmt/353",
                     "Low Risk", "Retain"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0007", "Tagged Image File Format (Low Risk)",
                     "Tagged Image File Format", "NO VALUE", "NO VALUE", "Low Risk",
                     "Depends on version, retain TIFF 1-6, otherwise see specific version plan"],
                    ["hargrett", "harg-0000", "harg-0000-web-202007-0001", "WARC (Low Risk)", "WARC", "NO VALUE",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/289", "Low Risk", "Retain"],
                    ["hargrett", "harg-0000", "harg-0000-web-202007-0002", "WARC (Low Risk)", "WARC", "NO VALUE",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/289", "Low Risk", "Retain"],
                    ["bmac", "peabody", "bmac_51021enr-1a", "Wave (Low Risk)", "Wave", "NO VALUE", "NO VALUE",
                     "Low Risk", "Retain"],
                    ["dlg", "zhj_tecc", "zhj_tecc_rml-ohp-001", "Waveform Audio (Low Risk)", "Waveform Audio",
                     "NO VALUE", "NO VALUE", "Low Risk", "Retain"]]
        self.assertEqual(result, expected, "Problem with test for multiple groups")

    def test_puid_all(self):
        """
        Test for an archive_formats_by_aip CSV with one group and all formats have a PRONOM_URL.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframe", "archive_formats_by_aip_puid-all_2023-08.csv")
        format_df = csv_to_dataframe(format_csv)

        # Tests that the dataframe contains the correct information.
        result = [format_df.columns.to_list()] + format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format", "Format_Name", "Format_Version", "PRONOM_URL",
                     "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0013", "JPEG EXIF 2.1 (Low Risk)", "JPEG EXIF", "2.1",
                     "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/390", "Low Risk", "Retain"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0016", "JPEG EXIF 2.1 (Low Risk)", "JPEG EXIF", "2.1",
                     "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/390", "Low Risk", "Retain"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0001", "JPEG File Interchange Format 1.01 (Low Risk)", 
                     "JPEG File Interchange Format", "1.01", "https://www.nationalarchives.gov.uk/PRONOM/fmt/43", 
                     "Low Risk", "Retain"]]
        self.assertEqual(result, expected, "Problem with test for PUID: all")

    def test_puid_mix(self):
        """
        Test for an archive_formats_by_aip CSV with one group and some formats have a PRONOM_URL.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframe", "archive_formats_by_aip_puid-mix_2023-08.csv")
        format_df = csv_to_dataframe(format_csv)

        # Tests that the dataframe contains the correct information.
        result = [format_df.columns.to_list()] + format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format", "Format_Name", "Format_Version", "PRONOM_URL",
                     "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan"],
                    ["dlg", "arl_nnc", "arl_nnc_nnc004-001-003", "Tagged Image File Format 5 (Low Risk)", 
                     "Tagged Image File Format", "5", "NO VALUE", "Low Risk", "Retain"],
                    ["dlg", "arl_acl", "arl_acl_acl328", "Tagged Image File Format 6 (Low Risk)", 
                     "Tagged Image File Format", "6", "https://www.nationalarchives.gov.uk/PRONOM/fmt/353", 
                     "Low Risk", "Retain"],
                    ["dlg", "arl_acl", "arl_acl_acl329", "Tagged Image File Format 6 (Low Risk)", 
                     "Tagged Image File Format", "6", "https://www.nationalarchives.gov.uk/PRONOM/fmt/353", 
                     "Low Risk", "Retain"],
                    ["dlg", "guan_ms40", "dlg_turningpoint_harg0040-001-002", "Tagged Image File Format (Low Risk)", 
                     "Tagged Image File Format", "NO VALUE", "NO VALUE", "Low Risk", 
                     "Depends on version, retain TIFF 1-6, otherwise see specific version plan"]]
        self.assertEqual(result, expected, "Problem with test for PUID: mix")

    def test_puid_none(self):
        """
        Test for an archive_formats_by_aip CSV with one group and no formats have a PRONOM_URL.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframe", "archive_formats_by_aip_puid-none_2023-08.csv")
        format_df = csv_to_dataframe(format_csv)

        # Tests that the dataframe contains the correct information.
        result = [format_df.columns.to_list()] + format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format", "Format_Name", "Format_Version", "PRONOM_URL",
                     "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan"],
                    ["bmac", "peabody", "bmac_2000002pst-arch", "Matroska (No Match)", "Matroska", "NO VALUE",
                     "NO VALUE", "No Match", "NO VALUE"],
                    ["bmac", "peabody", "bmac_2000023pst-arch", "Matroska (No Match)", "Matroska", "NO VALUE",
                     "NO VALUE", "No Match", "NO VALUE"]]
        self.assertEqual(result, expected, "Problem with test for PUID: none")


if __name__ == "__main__":
    unittest.main()
