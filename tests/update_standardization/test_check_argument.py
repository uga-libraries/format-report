"""
Tests for the function check_argument(),
which verifies the required argument is present and is a valid path,
and returns the path for report_folder and the error message (if any).

For input, tests use a list with argument values. In production, this would be the contents of sys.argv.
"""

import os
import sys
import unittest
from update_standardization import check_argument


class MyTestCase(unittest.TestCase):

    def test_report_correct(self):
        """
        Test for when the required argument report_folder is present and a valid path.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = [os.path.join(sys.path[1], "update_standardization.py"), "reports_new_formats"]
        report_folder, error_message = check_argument(sys_argv)

        # Tests that the value of report_folder is correct.
        expected = "reports_new_formats"
        self.assertEqual(report_folder, expected, "Problem with report: correct, report path")

        # Tests that the value of error_message is correct.
        self.assertEqual(error_message, None, "Problem with report: correct, error message")

    def test_report_missing(self):
        """
        Test for when the required argument report_folder is not present.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = [os.path.join(sys.path[1], "update_standardization.py")]
        report_folder, error_message = check_argument(sys_argv)

        # Tests that the value of error_message is correct.
        expected = "Required argument report_folder is missing"
        self.assertEqual(error_message, expected, "Problem with report: missing")

    def test_report_path_error(self):
        """
        Test for when the required argument report_folder is present but not a valid path.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = [os.path.join(sys.path[1], "update_standardization.py"), "reports_error"]
        report_folder, error_message = check_argument(sys_argv)

        # Tests that the value of error_message is correct.
        expected = "Report folder 'reports_error' does not exist"
        self.assertEqual(error_message, expected, "Problem with report: path error")


if __name__ == '__main__':
    unittest.main()
