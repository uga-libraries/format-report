"""
Tests for the function check_argument(),
which verifies the required argument is present, a valid path, and named correctly,
and returns the path and a list of errors (if any).

For input, tests use a list of argument values. In production, this would be the contents of sys.argv.
"""

import os
import sys
import unittest
from department_reports import check_argument


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """
        Test for when the required argument is present, a valid path, and named correctly.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        sys_argv = [script_path, os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")]
        format_csv, errors_list = check_argument(sys_argv)

        # Tests that the value of format_csv is correct.
        expected_path = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        self.assertEqual(format_csv, expected_path, "Problem with test for argument is correct, format_csv")

        # Tests that the value of errors_list is correct.
        expected_list = []
        self.assertEqual(errors_list, expected_list, "Problem with test for argument is correct, errors_list")

    def test_missing(self):
        """
        Test for when the required argument is missing.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        sys_argv = [script_path]
        format_csv, errors_list = check_argument(sys_argv)

        # Tests that the value of format_csv is correct.
        expected_path = None
        self.assertEqual(format_csv, expected_path, "Problem with test for argument is missing, format_csv")

        # Tests that the value of errors_list is correct.
        expected_list = ["Required argument archive_formats_by_aip_csv is missing"]
        self.assertEqual(errors_list, expected_list, "Problem with test for argument is missing, errors_list")

    def test_name_error(self):
        """
        Test for when the required argument is present and a valid path but is not named correctly.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        sys_argv = [script_path, os.path.join("check_arguments", "archive_formats_by_group_2023-08.csv")]
        format_csv, errors_list = check_argument(sys_argv)

        # Tests that the value of format_csv is correct.
        expected_path = os.path.join("check_arguments", "archive_formats_by_group_2023-08.csv")
        self.assertEqual(format_csv, expected_path, "Problem with test for argument name error, format_csv")

        # Tests that the value of errors_list is correct.
        expected_list = [f"archive_formats_by_aip_csv '{expected_path}' is not the correct type (should be by_aip)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for argument name error, errors_list")

    def test_name_and_path_error(self):
        """
        Test for when the required argument is present but is not named correctly and is not a valid path.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        sys_argv = [script_path, os.path.join("path_error", "name_error.csv")]
        format_csv, errors_list = check_argument(sys_argv)

        # Tests that the value of format_csv is correct.
        expected_path = os.path.join("path_error", "name_error.csv")
        self.assertEqual(format_csv, expected_path, "Problem with test for argument name and path error, format_csv")

        # Tests that the value of errors_list is correct.
        expected_list = [f"archive_formats_by_aip_csv '{expected_path}' does not exist",
                         f"archive_formats_by_aip_csv '{expected_path}' is not the correct type (should be by_aip)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for argument name and path error, errors_list")

    def test_path_error(self):
        """
        Test for when the required argument is present and named correctly but is not a valid path.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        sys_argv = [script_path, os.path.join("path_error", "archive_formats_by_aip_2023-08.csv")]
        format_csv, errors_list = check_argument(sys_argv)

        # Tests that the value of format_csv is correct.
        expected_path = os.path.join("path_error", "archive_formats_by_aip_2023-08.csv")
        self.assertEqual(format_csv, expected_path, "Problem with test for argument name error, format_csv")

        # Tests that the value of errors_list is correct.
        expected_list = [f"archive_formats_by_aip_csv '{expected_path}' does not exist"]
        self.assertEqual(errors_list, expected_list, "Problem with test for argument name error, errors_list")


if __name__ == '__main__':
    unittest.main()
