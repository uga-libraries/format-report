"""
Tests for the function check_argument(),
which verifies the required argument is present and is a valid path,
and returns report_folder and the error message (if any).

For input, tests use a list of argument values. In production, this would be the contents of sys.argv.
"""

import os
import sys
import unittest
from reports import check_argument


class MyTestCase(unittest.TestCase):

    def test_report_correct(self):
        """
        Test for when the required argument report_folder is present and a valid path.
        """
        # Runs the function being tested.
        sys_argv = [os.path.join(sys.path[1], "reports.py"), "correct_input"]
        report_folder, errors_message = check_argument(sys_argv)

        # Tests that the value of report_folder is correct.
        expected = "correct_input"
        self.assertEqual(report_folder, expected, "Problem with report: correct")

        # Tests that there were no errors (variable value is None).
        self.assertEqual(errors_message, None, "Problem with report: correct, errors list")

    def test_report_missing(self):
        """
        Test for when the required argument report_folder is not present.
        """
        # Runs the function being tested.
        sys_argv = [os.path.join(sys.path[1], "reports.py")]
        report_folder, error_message = check_argument(sys_argv)

        # Tests that the value of error_message is correct.
        expected = "Required argument report_folder is missing"
        self.assertEqual(error_message, expected, "Problem with report: missing")

    def test_report_path_error(self):
        """
        Test for when the required argument report_folder is present but not a valid path.
        """
        # Runs the function being tested.
        sys_argv = [os.path.join(sys.path[1], "reports.py"), "reports_error"]
        report_folder, error_message = check_argument(sys_argv)

        # Tests that the value of errors_list is correct.
        expected = "Report folder 'reports_error' does not exist"
        self.assertEqual(error_message, expected, "Problem with report: path error")


if __name__ == '__main__':
    unittest.main()
