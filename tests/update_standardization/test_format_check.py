"""
Tests for the function format_check(),
which gets all the format names from every format report in the report_folder,
matches the names to standardize_format.csv, and returns a dictionary
with the format name as the key and if found or missing as the value.

For input, tests use format reports that are in the update_standardization tests folder of this script repo.
"""

import os
import sys
import unittest
from update_standardization import format_check


class MyTestCase(unittest.TestCase):

    def test_blank_row(self):
        """
        Test for when the format reports include a blank row at the end of the CSV.
        The function will skip those rows.
        """
        # Runs the function being tested.
        formats_checked = format_check("reports_blank_row", os.path.join(sys.path[1], "standardize_formats.csv"))

        # Tests that the formats_checked dictionary contains the correct information.
        expected = {"DPX": "Found",
                    "JPEG File Interchange Format": "Found",
                    "Microsoft Word Binary File Format": "Found",
                    "New AV 1": "Missing",
                    "QuickTime": "Found",
                    "cue": "Found"}
        self.assertEqual(formats_checked, expected, "Problem with blank row test")

    def test_not_a_report(self):
        """
        Test for a format_reports folder that includes files which are not format reports.
        The function will skip those files and only read ones that are format reports.
        """
        # Runs the function being tested.
        formats_checked = format_check("reports_not_a_report", os.path.join(sys.path[1], "standardize_formats.csv"))

        # Tests that the formats_checked dictionary contains the correct information.
        expected = {"DPX": "Found",
                    "JPEG File Interchange Format": "Found",
                    "Microsoft Word Binary File Format": "Found",
                    "New AV 1": "Missing",
                    "QuickTime": "Found",
                    "cue": "Found"}
        self.assertEqual(formats_checked, expected, "Problem with not a report test")

    def test_one_report(self):
        """
        Test for a format_reports folder that only contains one format report.
        """
        # Runs the function being tested.
        formats_checked = format_check("reports_one", os.path.join(sys.path[1], "standardize_formats.csv"))

        # Tests that the formats_checked dictionary contains the correct information.
        expected = {"JPEG File Interchange Format": "Found",
                    "Microsoft Word Binary File Format": "Found",
                    "New AV 1": "Missing"}
        self.assertEqual(formats_checked, expected, "Problem with one report test")

    def test_three_reports(self):
        """
        Test for a format_reports folder that contains three format reports.
        """
        # Runs the function being tested.
        formats_checked = format_check("reports_three", os.path.join(sys.path[1], "standardize_formats.csv"))

        # Tests that the formats_checked dictionary contains the correct information.
        expected = {"DPX": "Found",
                    "JPEG File Interchange Format": "Found",
                    "Microsoft Word Binary File Format": "Found",
                    "New AV 1": "Missing",
                    "QuickTime": "Found",
                    "Tagged Image File Format": "Found",
                    "TIFF": "Found",
                    "cue": "Found"}
        self.assertEqual(formats_checked, expected, "Problem with three reports test")


if __name__ == '__main__':
    unittest.main()
