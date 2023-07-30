"""
Tests for the function in_standard(),
which compares a format name to standardize_formats.csv
and returns "Found" or "Missing".
"""

import os
import sys
import unittest
from update_standardization import in_standard


class MyTestCase(unittest.TestCase):

    def test_found_case_match(self):
        """
        Test for a format that matches a format in the CSV, including having the same letter cases.
        """
        # Runs the function being tested.
        match_status = in_standard(os.path.join(sys.path[1], "standardize_formats.csv"), "TIFF")

        # Tests that the function returns the correct value.
        self.assertEqual(match_status, "Found", "Problem with found: case match")

    def test_found_case_not_match(self):
        """
        Test for a format that matched a format in the CSV, but has different letter cases.
        """
        # Runs the function being tested.
        match_status = in_standard(os.path.join(sys.path[1], "standardize_formats.csv"), "Quicktime")

        # Tests that the function returns the correct value.
        self.assertEqual(match_status, "Found", "Problem with found: case not match")

    def test_missing(self):
        """
        Test for a format that does not match a format in the CSV.
        """
        # Runs the function being tested.
        match_status = in_standard(os.path.join(sys.path[1], "standardize_formats.csv"), "New AV 1")

        # Tests that the function returns the correct value.
        self.assertEqual(match_status, "Missing", "Problem with missing")

    def test_missing_error(self):
        """
        Test for a format name that starts with ERROR: cannot read.
        This is from a format identification tool and is automatically assigned Missing without checking the CSV.
        """
        # Runs the function being tested.
        match_status = in_standard(os.path.join(sys.path[1], "standardize_formats.csv"), "ERROR: cannot read file")

        # Tests that the function returns the correct value.
        self.assertEqual(match_status, "Missing", "Problem with missing: error")


if __name__ == '__main__':
    unittest.main()
