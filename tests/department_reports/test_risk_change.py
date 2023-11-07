"""
Tests for the function risk_change(),
which updates the current analysis dataframe with risk data from the previous analysis and
the type of change between the previous analysis and current analysis.
Returns the updated current dataframe.

Reading CSV into dataframe with csv_to_dataframe() rather than making a dataframe within the test
so that the input matches production exactly.
"""

import numpy as np
import os
import unittest
from department_reports import csv_to_dataframe, risk_change


class MyTestCase(unittest.TestCase):

    def test_all(self):
        """
        Test for when all six types of format risk change are present.
        """
        # Reads test input into dataframes.
        current_format_csv = os.path.join("risk_change", "archive_formats_by_aip_2023-01.csv")
        current_format_df = csv_to_dataframe(current_format_csv)
        previous_format_csv = os.path.join("risk_change", "archive_formats_by_aip_2021-01.csv")
        previous_format_df = csv_to_dataframe(previous_format_csv)

        # Runs the function being tested.
        current_format_df = risk_change(current_format_df, previous_format_df)

        # Tests that the updated current df contains the correction information.
        result = [current_format_df.columns.to_list()] + current_format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Name", "Format_Version", "PRONOM_URL",
                     "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan", "2021_NARA_Risk_Level",
                     "Risk_Level_Change"],
                    ["dlg", "arl_acl", "arl_acl_acl286", "Tagged Image File Format", "5.0",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/353", "Low Risk", "Retain",
                     "High Risk", "Decrease"],
                    ["dlg", "dlg_ghn", "batch_gua_augweeklychronsent02_archival",
                     "Extensible Markup Language", "1.0", "https://www.nationalarchives.gov.uk/PRONOM/fmt/101",
                     "No Match", np.NaN, np.NaN, "New Format"],
                    ["dlg", "dlg_ghn", "batch_gua_palladium_archival", "JPEG 2000 JP2", "NO VALUE",
                     "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/392", "No Match", np.NaN,
                     "Low Risk", "Unmatched"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20017", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/44", "Moderate Risk", "Retain",
                     "Low Risk", "Increase"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20018", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/44", "Moderate Risk", "Retain",
                     "Low Risk", "Increase"],
                    ["dlg", "gawcl-sylv_wccent", "gawcl-sylv_wccent_film001", "Matroska", "NO VALUE", "NO VALUE",
                     "Moderate Risk", "Retain", "No Match", "New Match"],
                    ["dlg", "zhj_tecc", "zhj_tecc_rml-ohp-037", "Waveform Audio", "NO VALUE", "NO VALUE",
                     "Moderate Risk", "Retain", "Moderate Risk", "Unchanged"]]
        self.assertEqual(result, expected, "Problem with test for risk, all types")

    def test_decrease(self):
        """
        Test for when format risk is lower in current than it is in previous.
        Includes all possible combinations of risk levels that decrease.
        Does not include previous No Match with current match, because those are classified as New Format.
        """
        # Reads test input into dataframes.
        current_format_csv = os.path.join("risk_change", "archive_formats_by_aip_2023-02.csv")
        current_format_df = csv_to_dataframe(current_format_csv)
        previous_format_csv = os.path.join("risk_change", "archive_formats_by_aip_2021-02.csv")
        previous_format_df = csv_to_dataframe(previous_format_csv)

        # Runs the function being tested.
        current_format_df = risk_change(current_format_df, previous_format_df)

        # Tests that the updated current df contains the correction information.
        result = [current_format_df.columns.to_list()] + current_format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Name", "Format_Version", "PRONOM_URL",
                     "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan", "2021_NARA_Risk_Level",
                     "Risk_Level_Change"],
                    ["dlg", "arl_acl", "arl_acl_acl286", "Tagged Image File Format", "5.0",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/353",
                     "Moderate Risk", "Retain", "High Risk", "Decrease"],
                    ["dlg", "dlg_ghn", "batch_gua_augweeklychronsent02_archival",
                     "Extensible Markup Language", "1.0", "https://www.nationalarchives.gov.uk/PRONOM/fmt/101",
                     "Low Risk", "Retain", "High Risk", "Decrease"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20017", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/44",
                     "Low Risk", "Retain", "Moderate Risk", "Decrease"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20018", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/44",
                     "Low Risk", "Retain", "Moderate Risk", "Decrease"]]
        self.assertEqual(result, expected, "Problem with test for risk decrease")

    def test_increase(self):
        """
        Test for when format risk is higher in current than it is in previous.
        Includes all possible combinations of risk levels that increase.
        It does not include any with current of No Match, which is the category Unmatched instead.
        """
        # Reads test input into dataframes.
        current_format_csv = os.path.join("risk_change", "archive_formats_by_aip_2023-03.csv")
        current_format_df = csv_to_dataframe(current_format_csv)
        previous_format_csv = os.path.join("risk_change", "archive_formats_by_aip_2021-03.csv")
        previous_format_df = csv_to_dataframe(previous_format_csv)

        # Runs the function being tested.
        current_format_df = risk_change(current_format_df, previous_format_df)

        # Tests that the updated current df contains the correction information.
        result = [current_format_df.columns.to_list()] + current_format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Name", "Format_Version", "PRONOM_URL",
                     "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan", "2021_NARA_Risk_Level",
                     "Risk_Level_Change"],
                    ["dlg", "arl_acl", "arl_acl_acl286", "Tagged Image File Format", "5.0",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/353",
                     "Moderate Risk", "Retain", "Low Risk", "Increase"],
                    ["dlg", "dlg_ghn", "batch_gua_augweeklychronsent02_archival",
                     "Extensible Markup Language", "1.0", "https://www.nationalarchives.gov.uk/PRONOM/fmt/101",
                     "High Risk", "Retain", "Low Risk", "Increase"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20017", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/44",
                     "High Risk", "Retain", "Moderate Risk", "Increase"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20018", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/44",
                     "High Risk", "Retain", "Moderate Risk", "Increase"]]
        self.assertEqual(result, expected, "Problem with test for risk increase")

    def test_new_format(self):
        """
        Test for when a format is not present in previous and is in current.
        Includes matching all four risk levels in current.
        """
        # Reads test input into dataframes.
        current_format_csv = os.path.join("risk_change", "archive_formats_by_aip_2023-04.csv")
        current_format_df = csv_to_dataframe(current_format_csv)
        previous_format_csv = os.path.join("risk_change", "archive_formats_by_aip_2021-04.csv")
        previous_format_df = csv_to_dataframe(previous_format_csv)

        # Runs the function being tested.
        current_format_df = risk_change(current_format_df, previous_format_df)

        # Tests that the updated current df contains the correction information.
        result = [current_format_df.columns.to_list()] + current_format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Name", "Format_Version", "PRONOM_URL",
                     "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan", "2021_NARA_Risk_Level",
                     "Risk_Level_Change"],
                    ["dlg", "arl_acl", "arl_acl_acl286", "Tagged Image File Format", "5.0",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/353",
                     "Low Risk", "Retain", np.NaN, "New Format"],
                    ["dlg", "dlg_ghn", "batch_gua_palladium_archival", "JPEG 2000 JP2", "NO VALUE",
                     "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/392", "Moderate Risk", "Retain",
                     np.NaN, "New Format"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20017", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/44", "High Risk", "Retain", np.NaN, "New Format"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20018", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/44", "High Risk", "Retain", np.NaN, "New Format"],
                    ["dlg", "gawcl-sylv_wccent", "gawcl-sylv_wccent_film001", "Matroska", "NO VALUE", "NO VALUE",
                     "No Match", np.NaN, np.NaN, "New Format"]]
        self.assertEqual(result, expected, "Problem with test for risk new match")

    def test_new_match(self):
        """
        Test for when a format did not match a NARa risk in previous and does match in current.
        Includes matching all three risk levels for match in current.
        """
        # Reads test input into dataframes.
        current_format_csv = os.path.join("risk_change", "archive_formats_by_aip_2023-05.csv")
        current_format_df = csv_to_dataframe(current_format_csv)
        previous_format_csv = os.path.join("risk_change", "archive_formats_by_aip_2021-05.csv")
        previous_format_df = csv_to_dataframe(previous_format_csv)

        # Runs the function being tested.
        current_format_df = risk_change(current_format_df, previous_format_df)

        # Tests that the updated current df contains the correction information.
        result = [current_format_df.columns.to_list()] + current_format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Name", "Format_Version", "PRONOM_URL",
                     "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan", "2021_NARA_Risk_Level",
                     "Risk_Level_Change"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20017", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/44", "Low Risk", "Retain",
                     "No Match", "New Match"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20018", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/44", "Low Risk", "Retain",
                     "No Match", "New Match"],
                    ["dlg", "gawcl-sylv_wccent", "gawcl-sylv_wccent_film001", "Matroska", "NO VALUE", "NO VALUE",
                     "Moderate Risk", "Retain", "No Match", "New Match"],
                    ["dlg", "zhj_tecc", "zhj_tecc_rml-ohp-037", "Waveform Audio", "NO VALUE", "NO VALUE",
                     "High Risk", "Retain", "No Match", "New Match"]]
        self.assertEqual(result, expected, "Problem with test for risk new match")

    def test_unmatched(self):
        """
        Test for when a format matched a NARA risk in previous and does not match in current.
        Includes matching all three risk levels for match in previous.
        """
        # Reads test input into dataframes.
        current_format_csv = os.path.join("risk_change", "archive_formats_by_aip_2023-07.csv")
        current_format_df = csv_to_dataframe(current_format_csv)
        previous_format_csv = os.path.join("risk_change", "archive_formats_by_aip_2021-07.csv")
        previous_format_df = csv_to_dataframe(previous_format_csv)

        # Runs the function being tested.
        current_format_df = risk_change(current_format_df, previous_format_df)

        # Tests that the updated current df contains the correction information.
        result = [current_format_df.columns.to_list()] + current_format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Name", "Format_Version", "PRONOM_URL",
                     "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan", "2021_NARA_Risk_Level",
                     "Risk_Level_Change"],
                    ["dlg", "dlg_ghn", "batch_gua_augweeklychronsent02_archival", "Extensible Markup Language", "1.0",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/101", "No Match", np.NaN,
                     "Moderate Risk", "Unmatched"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20017", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/44", "No Match", np.NaN,
                     "Low Risk", 'Unmatched'],
                    ["dlg", "zhj_tecc", "zhj_tecc_rml-ohp-037", "Waveform Audio", "NO VALUE", "NO VALUE",
                     "No Match", np.NaN, "High Risk", "Unmatched"]]
        self.assertEqual(result, expected, "Problem with test for risk unmatched")

    def test_unchanged(self):
        """
        Test for when format risk is the same in previous and current.
        Includes all four risk levels.
        """
        # Reads test input into dataframes.
        current_format_csv = os.path.join("risk_change", "archive_formats_by_aip_2023-06.csv")
        current_format_df = csv_to_dataframe(current_format_csv)
        previous_format_csv = os.path.join("risk_change", "archive_formats_by_aip_2021-06.csv")
        previous_format_df = csv_to_dataframe(previous_format_csv)

        # Runs the function being tested.
        current_format_df = risk_change(current_format_df, previous_format_df)

        # Tests that the updated current df contains the correction information.
        result = [current_format_df.columns.to_list()] + current_format_df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Name", "Format_Version", "PRONOM_URL",
                     "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan", "2021_NARA_Risk_Level",
                     "Risk_Level_Change"],
                    ["dlg", "arl_acl", "arl_acl_acl286", "Tagged Image File Format", "5.0",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/353", "Low Risk", "Retain",
                     "Low Risk", "Unchanged"],
                    ["dlg", "dlg_ghn", "batch_gua_palladium_archival", "JPEG 2000 JP2", "NO VALUE",
                     "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/392", "Moderate Risk", "Retain",
                     "Moderate Risk", "Unchanged"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20017", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/44", "High Risk", "Retain",
                     "High Risk", "Unchanged"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20018", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM/fmt/44", "High Risk", "Retain",
                     "High Risk", "Unchanged"],
                    ["dlg", "gawcl-sylv_wccent", "gawcl-sylv_wccent_film001", "Matroska", "NO VALUE", "NO VALUE",
                     "No Match", np.NaN, "No Match", "Unchanged"]]
        self.assertEqual(result, expected, "Problem with test for risk unchanged")


if __name__ == '__main__':
    unittest.main()
