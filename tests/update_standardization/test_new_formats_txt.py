"""
Tests for the function new_formats_txt(),
which makes a text file with any formats that are not in standardize_formats.csv so they can be added
and returns a Boolean value for if there are new formats for the script to print a message.

For input, each test generates a dictionary with format names as the key and Found/Missing as the value.
In production, this would be created by the previous script step.
"""

import os
import unittest
from update_standardization import new_formats_txt


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the new_formats.txt file, if it is made by the test."""
        file_path = os.path.join("reports_new_formats", "new_formats.txt")
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_all_match(self):
        """
        Test for when all formats match a row in standardize_formats.csv.
        """
        # Makes input dictionary and runs the function being tested.
        format_matches = {"CorelDraw Drawing": "Found", "DPX": "Found", "GZIP Format": "Found"}
        new_formats = new_formats_txt(format_matches, "reports_new_formats")

        # Tests that the function returned the correct Boolean value.
        self.assertEqual(new_formats, False, "Problem with all match, function return")

        # Tests that the function did not make a new_formats.txt file.
        file_made = os.path.exists(os.path.join("reports_new_formats", "new_formats.txt"))
        self.assertEqual(file_made, False, "Problem with all match, new_formats.txt")

    def test_one_no_match(self):
        """
        Test for when one format does not match anything in standardize_formats.csv and two do match.
        """
        # Makes input dictionary and runs the function being tested.
        format_matches = {"CorelDraw Drawing": "Found", "DPX": "Found", "New Zip Format": "Missing"}
        new_formats = new_formats_txt(format_matches, "reports_new_formats")

        # Tests that the function returned the correct Boolean value.
        self.assertEqual(new_formats, True, "Problem with one no match, function return")

        # Tests that the new_formats.txt file contains the correct information.
        with open(os.path.join("reports_new_formats", "new_formats.txt"), "r") as file:
            result = file.read()
        expected = "New Zip Format\n"
        self.assertEqual(result, expected, "Problem with one no match, new_formats.txt")

    def test_three_no_match(self):
        """
        Test for when three formats do not match anything in standardize_formats.csv and two do match.
        """
        # Makes input dictionary and runs the function being tested.
        format_matches = {"New Drawing Format": "Missing", "CorelDraw Drawing": "Found",
                          "New AV Format": "Missing", "DPX": "Found", "New Zip Format": "Missing"}
        new_formats = new_formats_txt(format_matches, "reports_new_formats")

        # Tests that the function returned the correct Boolean value.
        self.assertEqual(new_formats, True, "Problem with three no match, function return")

        # Tests that the new_formats.txt file contains the correct information.
        with open(os.path.join("reports_new_formats", "new_formats.txt"), "r") as file:
            result = file.read()
        expected = "New Drawing Format\nNew AV Format\nNew Zip Format\n"
        self.assertEqual(result, expected, "Problem with three no match, new_formats.txt")


if __name__ == '__main__':
    unittest.main()
