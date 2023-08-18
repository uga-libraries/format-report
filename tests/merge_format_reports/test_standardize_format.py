"""
Tests for the function standardize_format(),
which looks up a format in standardize_formats.csv
and returns its standardized name and format type.
"""

import os
import unittest
from merge_format_reports import standardize_format


class MyTestCase(unittest.TestCase):

    def test_identification_error(self):
        """
        Test for when the format is an identification error.
        """
        # Makes test input and runs the function being tested.
        format_name = "ERROR: cannot read file path\\file.ext."
        standard_csv_path = os.path.join("..", "..", "standardize_formats.csv")
        format_standard, format_type = standardize_format(format_name, standard_csv_path)

        # Tests that the value of format_standard is correct.
        self.assertEqual(format_standard, "IDENTIFICATION ERROR", "Problem with identification error, format_standard")

        # Tests that the value of format_type is correct.
        self.assertEqual(format_type, "IDENTIFICATION ERROR", "Problem with identification error, format_type")

    def test_match_case(self):
        """
        Test for when the format in the CSV and matches the case exactly.
        """
        # Makes test input and runs the function being tested.
        format_name = "DV"
        standard_csv_path = os.path.join("..", "..", "standardize_formats.csv")
        format_standard, format_type = standardize_format(format_name, standard_csv_path)

        # Tests that the value of format_standard is correct.
        self.assertEqual(format_standard, "Digital Video", "Problem with identification error, format_standard")

        # Tests that the value of format_type is correct.
        self.assertEqual(format_type, "video", "Problem with identification error, format_type")

    def test_match_case_insensitive(self):
        """
        Test for when the format is in the CSV but does not match the case (still a match).
        """
        # Makes test input and runs the function being tested.
        format_name = "jpeg Exif"
        standard_csv_path = os.path.join("..", "..", "standardize_formats.csv")
        format_standard, format_type = standardize_format(format_name, standard_csv_path)

        # Tests that the value of format_standard is correct.
        self.assertEqual(format_standard, "JPEG", "Problem with identification error, format_standard")

        # Tests that the value of format_type is correct.
        self.assertEqual(format_type, "image", "Problem with identification error, format_type")

    def test_no_match(self):
        """
        Test for when the format is not in the CSV.
        This causes the function to exit the script instead of returning values.
        """
        format_name = "new format"
        standard_csv_path = os.path.join("..", "..", "standardize_formats.csv")
        with self.assertRaises(SystemExit):
            standardize_format(format_name, standard_csv_path)


if __name__ == '__main__':
    unittest.main()
