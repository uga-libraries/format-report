"""
Tests for the function check_argument(),
which verifies that the required argument is present, valid, and named correctly,
and returns the path and the error (if any).

For input, tests use a list with argument values. In production, this would be the contents of sys.argv.
"""

import os
import unittest
from fix_versions import check_argument


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """
        Test for when the required argument is present and correct.
        """
        # Runs the function being tested.
        test_csv = os.path.join("check_argument", "archive_formats_by_group_2023-11.csv")
        csv_path, error_msg = check_argument(["fix_versions.py", test_csv])

        # Tests that the value of csv_path is correct.
        self.assertEqual(csv_path, test_csv, "Problem with test for correct, csv_path")

        # Tests that the value of error_msg is correct.
        self.assertEqual(error_msg, None, "Problem with test for correct, error_msg")

    def test_missing_arg(self):
        """
        Test for when the required argument is missing.
        """
        # Runs the function being tested.
        csv_path, error_msg = check_argument(["fix_versions.py"])

        # Tests that the value of csv_path is correct.
        self.assertEqual(csv_path, None, "Problem with test for missing argument, csv_path")

        # Tests that the value of error_msg is correct.
        expected_msg = "Required argument csv_path is missing"
        self.assertEqual(error_msg, expected_msg, "Problem with test for missing argument, error_msg")


if __name__ == '__main__':
    unittest.main()
