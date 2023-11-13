"""
Tests for the function match_nara_risk,
which combines format identifications with NARA risk information to produce df_results.

To simplify the testing, the format identifications only have columns used by match_nara_risk()."""

import numpy as np
import os
import unittest
from merge_format_reports import csv_to_dataframe, match_nara_risk


class MyTestCase(unittest.TestCase):

    def test_name_case(self):
        """
        Test for format ids that match one name (no version) in the NARA spreadsheet, with the same case.
        Format ids do not have PUIDs. Some NARA matches have a PUID and some do not.
        """
        # Creates test input. In production, this is done by add_nara_risk().
        df_format = csv_to_dataframe(os.path.join('match_nara_risk', 'archive_formats_name_case.csv'))
        df_nara = csv_to_dataframe("NARA_PreservationActionPlan_FileFormats_test.csv")

        # Runs the function being tested and converts the resulting dataframe to a list, including the column headers.
        df_results = match_nara_risk(df_format, df_nara)
        result = [df_results.columns.tolist()] + df_results.values.tolist()

        # Creates a list with the expected result.
        expected = [['Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'NARA_Format_Name',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Electronic Mail Format', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'Electronic Mail Format',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/278', 'Low Risk', 'Retain', 'Format Name'],
                    ['ROM Image', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'ROM Image', np.NaN, 'Moderate Risk',
                     'Retain', 'Format Name']]

        # Compares the results. assertEqual prints "OK" or the differences between the two lists.
        self.assertEqual(result, expected, 'Problem with name, case match')

    def test_name_not_case(self):
        """
        Test for format ids that match one name (no version) in the NARA spreadsheet, case doesn't match.
        Format ids do not have PUIDs. Some NARA matches have a PUID and some do not.
        """
        # Creates test input. In production, this is done by add_nara_risk().
        df_format = csv_to_dataframe(os.path.join('match_nara_risk', 'archive_formats_name_not_case.csv'))
        df_nara = csv_to_dataframe("NARA_PreservationActionPlan_FileFormats_test.csv")

        # Runs the function being tested and converts the resulting dataframe to a list, including the column headers.
        df_results = match_nara_risk(df_format, df_nara)
        result = [df_results.columns.tolist()] + df_results.values.tolist()

        # Creates a list with the expected result.
        expected = [['Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'NARA_Format_Name',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['batch script', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'Batch Script',
                     'https://www.nationalarchives.gov.uk/pronom/x-fmt/413', 'Moderate Risk', 'Retain', 'Format Name'],
                    ['Rom image', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'ROM Image', np.NaN, 'Moderate Risk',
                     'Retain', 'Format Name']]

        # Compares the results. assertEqual prints "OK" or the differences between the two lists.
        self.assertEqual(result, expected, 'Problem with name, case does not match')

    def test_name_version_case(self):
        """
        Test for format ids that match one name/version combination in the NARA spreadsheet, with the same case.
        Format ids do not have PUIDs. Some NARA matches have a PUID and some do not.
        """
        # Creates test input. In production, this is done by add_nara_risk().
        df_format = csv_to_dataframe(os.path.join('match_nara_risk', 'archive_formats_name_version_case.csv'))
        df_nara = csv_to_dataframe("NARA_PreservationActionPlan_FileFormats_test.csv")

        # Runs the function being tested and converts the resulting dataframe to a list, including the column headers.
        df_results = match_nara_risk(df_format, df_nara)
        result = [df_results.columns.tolist()] + df_results.values.tolist()

        # Creates a list with the expected result.
        expected = [['Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'NARA_Format_Name',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Lotus 1-2-3 Worksheet', '3.0', 'NO VALUE', 'NO VALUE', 'Lotus 1-2-3 Worksheet 3.0',
                     'https://www.nationalarchives.gov.uk/pronom/x-fmt/115', 'Moderate Risk',
                     'Transform to CSV or XLSX', 'Format Name'],
                    ['Avid Pro Tools Session', '5.1-6.9', 'NO VALUE', 'NO VALUE',
                     'Avid Pro Tools Session 5.1-6.9', np.NaN, 'High Risk', 'Transform to WAV if possible',
                     'Format Name']]

        # Compares the results. assertEqual prints "OK" or the differences between the two lists.
        self.assertEqual(result, expected, 'Problem with name and version, case match')

    def test_name_version_not_case(self):
        """
        Test for format ids that match one name/version combination in the NARA spreadsheet, case doesn't match.
        Format ids do not have PUIDs. Some NARA matches have a PUID and some do not.
        """
        # Creates test input. In production, this is done by add_nara_risk().
        df_format = csv_to_dataframe(os.path.join('match_nara_risk', 'archive_formats_name_version_not_case.csv'))
        df_nara = csv_to_dataframe("NARA_PreservationActionPlan_FileFormats_test.csv")

        # Runs the function being tested and converts the resulting dataframe to a list, including the column headers.
        df_results = match_nara_risk(df_format, df_nara)
        result = [df_results.columns.tolist()] + df_results.values.tolist()

        # Creates a list with the expected result.
        expected = [['Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'NARA_Format_Name',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['lotus 1-2-3 worksheet', '3.0', 'NO VALUE', 'NO VALUE', 'Lotus 1-2-3 Worksheet 3.0',
                     'https://www.nationalarchives.gov.uk/pronom/x-fmt/115', 'Moderate Risk',
                     'Transform to CSV or XLSX', 'Format Name'],
                    ['microsoft ACCESS', '2016', 'NO VALUE', 'NO VALUE', 'Microsoft Access 2016',
                     np.NaN, 'Moderate Risk', 'Transform to CSV', 'Format Name']]

        # Compares the results. assertEqual prints "OK" or the differences between the two lists.
        self.assertEqual(result, expected, 'Problem with name and version, case does not match')

    def test_no_match(self):
        """
        Test for format ids with no PUIDs that do not match any formats in the NARA spreadsheet.
        Format ids do not have PUIDs. Some NARA matches have a PUID and some do not.
        """
        # Creates test input. In production, this is done by add_nara_risk().
        df_format = csv_to_dataframe(os.path.join('match_nara_risk', 'archive_formats_no_match.csv'))
        df_nara = csv_to_dataframe("NARA_PreservationActionPlan_FileFormats_test.csv")

        # Runs the function being tested and converts the resulting dataframe to a list, including the column headers.
        df_results = match_nara_risk(df_format, df_nara)
        result = [df_results.columns.tolist()] + df_results.values.tolist()

        # Creates a list with the expected result.
        expected = [['Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'NARA_Format_Name',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['New Format', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'No Match', np.NaN, 'No Match', np.NaN,
                     'No NARA Match'],
                    ['Unknown Binary', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'No Match', np.NaN,
                     'No Match', np.NaN, 'No NARA Match']]

        # Compares the results. assertEqual prints "OK" or the differences between the two lists.
        self.assertEqual(result, expected, 'Problem with no matches')

    def test_puid_multiple(self):
        """
        Test for format ids that match multiple PUIDs in the NARA spreadsheet.
        """
        # Creates test input. In production, this is done by add_nara_risk().
        df_format = csv_to_dataframe(os.path.join('match_nara_risk', 'archive_formats_puid_multiple.csv'))
        df_nara = csv_to_dataframe("NARA_PreservationActionPlan_FileFormats_test.csv")

        # Runs the function being tested and converts the resulting dataframe to a list, including the column headers.
        df_results = match_nara_risk(df_format, df_nara)
        result = [df_results.columns.tolist()] + df_results.values.tolist()

        # Creates a list with the expected result.
        expected = [['Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'NARA_Format_Name',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['XHTML', '1.1', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/103',
                     'eXtensible Hypertext Markup Language 1.1', 'https://www.nationalarchives.gov.uk/pronom/fmt/103',
                     'Low Risk', 'Retain', 'PRONOM and Version'],
                    ['XHTML', '1.1', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/103',
                     'Hypertext Markup Language 1.1', 'https://www.nationalarchives.gov.uk/pronom/fmt/103',
                     'Low Risk', 'Retain', 'PRONOM and Version'],
                    ['Open XML Paper', 'NO VALUE', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/657',
                     'Microsoft XML Paper Specification 1.0', 'https://www.nationalarchives.gov.uk/pronom/fmt/657',
                     'Moderate Risk', 'Transform to PDF or possibly OXPS', 'PRONOM'],
                    ['Open XML Paper', 'NO VALUE', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/657',
                     'Open XML Paper Specification', 'https://www.nationalarchives.gov.uk/pronom/fmt/657', 'Low Risk',
                     'Further research is required, possibly transform to PDF, or retain as OXPS', 'PRONOM']]

        # Compares the results. assertEqual prints "OK" or the differences between the two lists.
        self.assertEqual(result, expected, 'Problem with PUID, multiple matches')

    def test_puid_name(self):
        """
        Test for format ids that match a single PUID and format name (not version) combination in the NARA spreadsheet.
        """
        # Creates test input. In production, this is done by add_nara_risk().
        df_format = csv_to_dataframe(os.path.join('match_nara_risk', 'archive_formats_puid_name.csv'))
        df_nara = csv_to_dataframe("NARA_PreservationActionPlan_FileFormats_test.csv")

        # Runs the function being tested and converts the resulting dataframe to a list, including the column headers.
        df_results = match_nara_risk(df_format, df_nara)
        result = [df_results.columns.tolist()] + df_results.values.tolist()

        # Creates a list with the expected result.
        expected = [['Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'NARA_Format_Name',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['ESRI ArcInfo Interchange File Format', 'NO VALUE', 'https://www.nationalarchives.gov.uk/PRONOM',
                     'x-fmt/235', 'ESRI ArcInfo Interchange File Format',
                     'https://www.nationalarchives.gov.uk/pronom/x-fmt/235', 'Moderate Risk',
                     'Transform to KML, ESRI Shapefile, and/or GML as appropriate', 'PRONOM and Name'],
                    ['MPEG-2 Video', 'NO VALUE', 'https://www.nationalarchives.gov.uk/PRONOM', 'x-fmt/386',
                     'MPEG-2 Video', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/386',
                     'Low Risk', 'Retain', 'PRONOM and Name']]

        # Compares the results. assertEqual prints "OK" or the differences between the two lists.
        self.assertEqual(result, expected, 'Problem with PUID and Name')

    def test_puid_no_match(self):
        """
        Test for format ids with a PUID that do not match any formats in the NARA spreadsheet.
        """
        # Creates test input. In production, this is done by add_nara_risk().
        df_format = csv_to_dataframe(os.path.join('match_nara_risk', 'archive_formats_puid_no_match.csv'))
        df_nara = csv_to_dataframe("NARA_PreservationActionPlan_FileFormats_test.csv")

        # Runs the function being tested.
        # Converts the resulting dataframe to a list, including the column headers, for easier comparison.
        df_results = match_nara_risk(df_format, df_nara)
        result = [df_results.columns.tolist()] + df_results.values.tolist()

        # Tests that the value of the result is correct.
        expected = [['Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'NARA_Format_Name',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Cascading Style Sheets', '2', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/000',
                     'No Match', np.NaN, 'No Match', np.NaN, 'No NARA Match'],
                    ['Comma Separated Values', 'NO VALUE', 'https://www.nationalarchives.gov.uk/PRONOM', 'x-fmt/000',
                     'No Match', np.NaN, 'No Match', np.NaN, 'No NARA Match']]
        self.assertEqual(result, expected, 'Problem with PUID, no matches')

    def test_puid_single(self):
        """
        Test for format ids that match a single PUID, but not format name or version, in the NARA spreadsheet.
        """
        # Creates test input. In production, this is done by add_nara_risk().
        df_format = csv_to_dataframe(os.path.join('match_nara_risk', 'archive_formats_puid_single.csv'))
        df_nara = csv_to_dataframe("NARA_PreservationActionPlan_FileFormats_test.csv")

        # Runs the function being tested and converts the resulting dataframe to a list, including the column headers.
        df_results = match_nara_risk(df_format, df_nara)
        result = [df_results.columns.tolist()] + df_results.values.tolist()

        # Creates a list with the expected result.
        expected = [['Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'NARA_Format_Name',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['CorelDraw', 'NO VALUE', 'https://www.nationalarchives.gov.uk/PRONOM', 'x-fmt/31',
                     'CorelDraw Compressed Drawing', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/31',
                     'High Risk', 'Transform to a TBD format, possibly PDF or TIFF', 'PRONOM'],
                    ['Digital Negative 1.0', 'NO VALUE', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/436',
                     'Digital Negative Format 1.0', 'https://www.nationalarchives.gov.uk/pronom/fmt/436',
                     'Low Risk', 'Retain', 'PRONOM']]

        # Compares the results. assertEqual prints "OK" or the differences between the two lists.
        self.assertEqual(result, expected, 'Problem with PUID, single match')

    def test_puid_version(self):
        """
        Test for format ids that match a single PUID and format version combination in the NARA spreadsheet.
        """
        # Creates test input. In production, this is done by add_nara_risk().
        df_format = csv_to_dataframe(os.path.join('match_nara_risk', 'archive_formats_puid_version.csv'))
        df_nara = csv_to_dataframe("NARA_PreservationActionPlan_FileFormats_test.csv")

        # Runs the function being tested and converts the resulting dataframe to a list, including the column headers.
        df_results = match_nara_risk(df_format, df_nara)
        result = [df_results.columns.tolist()] + df_results.values.tolist()

        # Creates a list with the expected result.
        expected = [['Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'NARA_Format_Name',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['CSS', '2.0', 'https://www.nationalarchives.gov.uk/PRONOM', 'x-fmt/224',
                     'Cascading Style Sheets 2.0', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/224',
                     'Low Risk', 'Retain', 'PRONOM and Version'],
                    ['HTML', '5.1', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/96',
                     'Hypertext Markup Language 5.1', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Low Risk', 'Retain', 'PRONOM and Version']]

        # Compares the results. assertEqual prints "OK" or the differences between the two lists.
        self.assertEqual(result, expected, 'Problem with PUID and Version')


if __name__ == '__main__':
    unittest.main()
