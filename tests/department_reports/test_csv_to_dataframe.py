"""
Tests for the function csv_to_dataframe(),
which reads the previous or current archive_formats_by_aip_date.csv into a dataframe, 
including error handling for encoding errors, and cleans up the data.
Returns the dataframe.
"""

import os
import unittest
from department_reports import csv_to_dataframe


class MyTestCase(unittest.TestCase):

    def test_encoding_error(self):
        """
        Test for a CSV with an encoding error.
        """
        # Runs the function being tested.
        # NOTE: the function prints an error message to the terminal if it is working correctly.
        format_csv = os.path.join("csv_to_dataframe", "archive_formats_by_aip_encoding-error_2023-08.csv")
        format_df = csv_to_dataframe(format_csv)

        # Tests that the dataframe contains the correct information.
        result = [format_df.columns.to_list()] + format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Identification", "Format", "Format_Name", "Format_Version",
                     "PRONOM_URL", "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan"],
                    ["bmac", "peabody", "bmac_2000002pst-arch", "Matroska|NO VALUE|NO VALUE", "Matroska (No Match)",
                     "Matroska", "NO VALUE", "NO VALUE", "No Match", "NO VALUE"],
                    ["bmac", "peabody", "bmac_2000023pst-arch", "Matroska|NO VALUE|NO VALUE", "Matroska (No Match)",
                     "Matroska", "NO VALUE", "NO VALUE", "No Match", "NO VALUE"]]
        self.assertEqual(result, expected, "Problem with test for encoding error")

    def test_multi_groups(self):
        """
        Test for a CSV with multiple groups.
        Some groups have one format and others have multiple formats.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframe", "archive_formats_by_aip_multiple_2023-08.csv")
        format_df = csv_to_dataframe(format_csv)

        # Tests that the dataframe contains the correct information.
        result = [format_df.columns.to_list()] + format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Identification", "Format", "Format_Name", "Format_Version",
                     "PRONOM_URL", "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan"],
                    ["dlg", "arl_acl", "arl_acl_acl332", "Tagged Image File Format|6|fmt/353",
                     "Tagged Image File Format 6 (Low Risk)", "Tagged Image File Format", "6",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/353", "Low Risk", "Retain"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0007", "Tagged Image File Format|NO VALUE|NO VALUE",
                     "Tagged Image File Format (Low Risk)", "Tagged Image File Format", "NO VALUE", "NO VALUE",
                     "Low Risk", "Depends on version, retain TIFF 1-6, otherwise see specific version plan"],
                    ["hargrett", "harg-0000", "harg-0000-web-202007-0001", "WARC|NO VALUE|fmt/289", "WARC (Low Risk)",
                     "WARC", "NO VALUE", "https://www.nationalarchives.gov.uk/PRONOM/fmt/289", "Low Risk", "Retain"],
                    ["hargrett", "harg-0000", "harg-0000-web-202007-0002", "WARC|NO VALUE|fmt/289", "WARC (Low Risk)",
                     "WARC", "NO VALUE", "https://www.nationalarchives.gov.uk/PRONOM/fmt/289", "Low Risk", "Retain"],
                    ["bmac", "peabody", "bmac_51021enr-1a", "Wave|NO VALUE|NO VALUE", "Wave (Low Risk)", "Wave",
                     "NO VALUE", "NO VALUE", "Low Risk", "Retain"],
                    ["dlg", "zhj_tecc", "zhj_tecc_rml-ohp-001", "Waveform Audio|NO VALUE|NO VALUE",
                     "Waveform Audio (Low Risk)", "Waveform Audio", "NO VALUE", "NO VALUE", "Low Risk", "Retain"]]
        self.assertEqual(result, expected, "Problem with test for multiple groups")

    def test_puid_all(self):
        """
        Test for a CSV with one group and all formats have a PRONOM_URL.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframe", "archive_formats_by_aip_puid-all_2023-08.csv")
        format_df = csv_to_dataframe(format_csv)

        # Tests that the dataframe contains the correct information.
        result = [format_df.columns.to_list()] + format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Identification", "Format", "Format_Name", "Format_Version",
                     "PRONOM_URL", "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0013", "JPEG EXIF|2.1|x-fmt/390",
                     "JPEG EXIF 2.1 (Low Risk)", "JPEG EXIF", "2.1",
                     "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/390", "Low Risk", "Retain"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0016", "JPEG EXIF|2.1|x-fmt/390",
                     "JPEG EXIF 2.1 (Low Risk)", "JPEG EXIF", "2.1",
                     "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/390", "Low Risk", "Retain"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0001", "JPEG File Interchange Format|1.01|fmt/43",
                     "JPEG File Interchange Format 1.01 (Low Risk)",  "JPEG File Interchange Format", "1.01",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/43", "Low Risk", "Retain"]]
        self.assertEqual(result, expected, "Problem with test for PUID: all")

    def test_puid_mix(self):
        """
        Test for a CSV with one group and some formats have a PRONOM_URL.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframe", "archive_formats_by_aip_puid-mix_2023-08.csv")
        format_df = csv_to_dataframe(format_csv)

        # Tests that the dataframe contains the correct information.
        result = [format_df.columns.to_list()] + format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Identification", "Format", "Format_Name", "Format_Version",
                     "PRONOM_URL", "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan"],
                    ["dlg", "arl_nnc", "arl_nnc_nnc004-001-003", "Tagged Image File Format|5|NO VALUE",
                     "Tagged Image File Format 5 (Low Risk)", "Tagged Image File Format", "5", "NO VALUE",
                     "Low Risk", "Retain"],
                    ["dlg", "arl_acl", "arl_acl_acl328", "Tagged Image File Format|6|fmt/353",
                     "Tagged Image File Format 6 (Low Risk)", "Tagged Image File Format", "6",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/353", "Low Risk", "Retain"],
                    ["dlg", "arl_acl", "arl_acl_acl329", "Tagged Image File Format|6|fmt/353",
                     "Tagged Image File Format 6 (Low Risk)", "Tagged Image File Format", "6",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/353", "Low Risk", "Retain"],
                    ["dlg", "guan_ms40", "dlg_turningpoint_harg0040-001-002",
                     "Tagged Image File Format|NO VALUE|NO VALUE", "Tagged Image File Format (Low Risk)",
                     "Tagged Image File Format", "NO VALUE", "NO VALUE", "Low Risk",
                     "Depends on version, retain TIFF 1-6, otherwise see specific version plan"]]
        self.assertEqual(result, expected, "Problem with test for PUID: mix")

    def test_puid_none(self):
        """
        Test for a CSV with one group and no formats have a PRONOM_URL.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframe", "archive_formats_by_aip_puid-none_2023-08.csv")
        format_df = csv_to_dataframe(format_csv)

        # Tests that the dataframe contains the correct information.
        result = [format_df.columns.to_list()] + format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Identification", "Format", "Format_Name", "Format_Version",
                     "PRONOM_URL", "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan"],
                    ["bmac", "peabody", "bmac_2000002pst-arch", "Matroska|NO VALUE|NO VALUE", "Matroska (No Match)",
                     "Matroska", "NO VALUE", "NO VALUE", "No Match", "NO VALUE"],
                    ["bmac", "peabody", "bmac_2000023pst-arch", "Matroska|NO VALUE|NO VALUE", "Matroska (No Match)",
                     "Matroska", "NO VALUE", "NO VALUE", "No Match", "NO VALUE"]]
        self.assertEqual(result, expected, "Problem with test for PUID: none")

    def test_version_all(self):
        """
        Test for a CSV with one group and all formats have a version number.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframe", "archive_formats_by_aip_version-all_2023-08.csv")
        format_df = csv_to_dataframe(format_csv)

        # Tests that the dataframe contains the correct information.
        result = [format_df.columns.to_list()] + format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Identification", "Format", "Format_Name", "Format_Version",
                     "PRONOM_URL", "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan"],
                    ["russell", "rbrl213", "rbrl-213-er-000102", "Microsoft Excel|8X|fmt/61 fmt/62",
                     "Microsoft Excel 8X (Moderate Risk)", "Microsoft Excel", "8X",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/61 fmt/62", "Moderate Risk", "Transform to XLSX"],
                    ["russell", "rbrl459", "rbrl-459-er-000030", "Microsoft Works Database for DOS|1.05|fmt/169",
                     "Microsoft Works Database for DOS 1.05 (Moderate Risk)", "Microsoft Works Database for DOS",
                     "1.05", "https://www.nationalarchives.gov.uk/PRONOM/fmt/169", "Moderate Risk", "Transform to CSV"],
                    ["russell", "rbrl213", "rbrl-213-er-000101", "Rich Text Format (RTF)|1.5-1.6|fmt/50",
                     "Rich Text Format (RTF) 1.5-1.6 (Moderate Risk)", "Rich Text Format (RTF)", "1.5-1.6",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/50", "Moderate Risk", "Transform to PDF"]]
        self.assertEqual(result, expected, "Problem with test for version: all")

    def test_version_mix(self):
        """
        Test for a CSV with one group and some formats have a version number.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframe", "archive_formats_by_aip_version-mix_2023-08.csv")
        format_df = csv_to_dataframe(format_csv)

        # Tests that the dataframe contains the correct information.
        result = [format_df.columns.to_list()] + format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Identification", "Format", "Format_Name", "Format_Version",
                     "PRONOM_URL", "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan"],
                    ["dlg-magil", "gyca_gaphind", "gyca_gaphind_banks-1980", "Plain text|NO VALUE|x-fmt/111",
                     "Plain text (Low Risk)", "Plain text", "NO VALUE",
                     "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/111", "Low Risk", "Retain"],
                    ["dlg-magil", "gyca_gaphind", "gyca_gaphind_lee-1993", "Tagged Image File Format|4.0|NO VALUE",
                     "Tagged Image File Format 4.0 (Low Risk)", "Tagged Image File Format", "4.0", "NO VALUE",
                     "Low Risk", "Retain"],
                    ["dlg-magil", "dlg_sanb", "dlg_sanb_savannah-1888", "Tagged Image File Format|6.0|NO VALUE",
                     "Tagged Image File Format 6.0 (Low Risk)", "Tagged Image File Format", "6.0", "NO VALUE",
                     "Low Risk", "Retain"]]
        self.assertEqual(result, expected, "Problem with test for version: mix")

    def test_version_none(self):
        """
        Test for a CSV with one group and no formats have a version number.
        """
        # Runs the function being tested.
        format_csv = os.path.join("csv_to_dataframe", "archive_formats_by_aip_version-none_2023-08.csv")
        format_df = csv_to_dataframe(format_csv)

        # Tests that the dataframe contains the correct information.
        result = [format_df.columns.to_list()] + format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Identification", "Format", "Format_Name", "Format_Version",
                     "PRONOM_URL", "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan"],
                    ["russell", "rbrl459", "rbrl-459-er-000072", "Lotus 1-2-3 wk4 document data|NO VALUE|NO VALUE",
                     "Lotus 1-2-3 wk4 document data (Moderate Risk)", "Lotus 1-2-3 wk4 document data", "NO VALUE",
                     "NO VALUE", "Moderate Risk",
                     "Transform to CSV or XLSX"],
                    ["russell", "rbrl377", "rbrl-377-er-000001", "SWF|NO VALUE|NO VALUE", "SWF (Moderate Risk)",
                     "SWF", "NO VALUE", "NO VALUE", "Moderate Risk", "Retain"],
                    ["russell", "rbrl455", "rbrl-455-er-000069", "Quicken Data File|NO VALUE|x-fmt/213",
                     "Quicken Data File (No Match)", "Quicken Data File", "NO VALUE",
                     "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/213", "No Match", "NO VALUE"]]
        self.assertEqual(result, expected, "Problem with test for version: none")


if __name__ == "__main__":
    unittest.main()
