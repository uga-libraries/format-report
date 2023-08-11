"""
Tests for the function get_report_paths(),
which finds and returns the path for all three reports used for script input,
as well as a list of any reports that are missing.

# For input, tests use report folders in the repo for this script.
"""

import os
import unittest
from reports import get_report_paths


class MyTestCase(unittest.TestCase):

    def test_all_present(self):
        """
        Test for when all three expected reports are present in the reports folder.
        """
        formats_by_aip_report, formats_report, usage_report, missing = get_report_paths("correct_input")

        # Tests that the value of formats_by_aip_report is correct.
        expected = os.path.join("correct_input", "archive_formats_by_aip_2023-08.csv")
        self.assertEqual(formats_by_aip_report, expected, "Problem with test for all present, formats_by_aip")

        # Tests that the value of formats_report is correct.
        expected = os.path.join("correct_input", "archive_formats_2023-08.csv")
        self.assertEqual(formats_report, expected, "Problem with test for all present, formats")

        # Tests that the value of usage_report is correct.
        expected = os.path.join("correct_input", "usage_report_20171101_20211101.csv")
        self.assertEqual(usage_report, expected, "Problem with test for all present, usage")

        # Tests that the value of missing is correct.
        expected = []
        self.assertEqual(missing, expected, "Problem with test for all present, missing")

    def test_missing_all(self):
        """
        Test for when all three expected reports are missing from the reports folder.
        """
        formats_by_aip_report, formats_report, usage_report, missing = get_report_paths("missing_input_all")
        expected = ["archive_formats_by_aip.csv", "archive_formats.csv", "usage_report.csv"]
        self.assertEqual(missing, expected, "Problem with test for missing all reports")

    def test_missing_formats_by_aip(self):
        """
        Test for when the formats_by_aip report is missing from the reports folder.
        """
        formats_by_aip_report, formats_report, usage_report, missing = get_report_paths("missing_formats_by_aip")
        expected = ["archive_formats_by_aip.csv"]
        self.assertEqual(missing, expected, "Problem with test for missing formats by aip report")

    def test_missing_format(self):
        """
        Test for when the formats report is missing from the reports folder.
        """
        formats_by_aip_report, formats_report, usage_report, missing = get_report_paths("missing_formats")
        expected = ["archive_formats.csv"]
        self.assertEqual(missing, expected, "Problem with test for missing formats report")

    def test_missing_usage(self):
        """
        Test for when the usage report is missing from the reports folder.
        """
        formats_by_aip_report, formats_report, usage_report, missing = get_report_paths("missing_usage")
        expected = ["usage_report.csv"]
        self.assertEqual(missing, expected, "Problem with test for missing usage report")


if __name__ == '__main__':
    unittest.main()
