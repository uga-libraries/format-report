"""
Tests for the function check_arguments(),
which verifies the required argument is present and argument paths are valid,
and returns report_folder, standard_csv, and a list with errors.

For input, tests use a list with argument values. In production, this would be the contents of sys.argv.
"""

import os
import sys
import unittest
from update_standardization import check_arguments


class MyTestCase(unittest.TestCase):

    def test_csv_argument_correct(self):
        """
        Test for when the optional argument standard_csv is present and a valid path.
        """
        # Runs the function being tested.
        sys_argv = [os.path.join(sys.path[1], "update_standardization.py"), "reports_new_formats",
                    os.path.join(os.getcwd(), "standardize_formats_custom.csv")]
        report_folder, standardize_formats_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of standardize_formats_csv is correct.
        expected = os.path.join(os.getcwd(), "standardize_formats_custom.csv")
        self.assertEqual(standardize_formats_csv, expected, "Problem with csv from argument: correct")

        # Tests that there were no errors (list is empty).
        self.assertEqual(len(errors_list), 0, "Problem with csv from argument: correct, errors list")

    def test_csv_argument_path_error(self):
        """
        Test for when the optional argument standard_csv is present but not a valid path.
        """
        # Runs the function being tested.
        sys_argv = [os.path.join(sys.path[1], "update_standardization.py"), "reports_new_formats",
                    "standardize_formats_error.csv"]
        report_folder, standardize_formats_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of errors_list is correct.
        expected = ["Standardize Formats CSV 'standardize_formats_error.csv' does not exist"]
        self.assertEqual(errors_list, expected, "Problem with csv from argument: path error")

    def test_csv_default_correct(self):
        """
        Test for when the optional argument standard_csv is not present
        and the default csv path is a valid path.
        """
        # Runs the function being tested.
        sys_argv = [os.path.join(sys.path[1], "update_standardization.py"), "reports_new_formats"]
        report_folder, standardize_formats_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of standardize_formats_csv is correct.
        expected = os.path.join(sys.path[1], "standardize_formats.csv")
        self.assertEqual(standardize_formats_csv, expected, "Problem with csv from default: correct")

        # Tests that there were no errors (list is empty).
        self.assertEqual(len(errors_list), 0, "Problem with csv from default: correct, errors list")

    def test_csv_default_path_error(self):
        """
        Test for when the optional argument standard_csv is not present
        but the default csv path is not a valid path.
        """
        # Changes the name of standardize_formats.csv to cause the error.
        original_name = os.path.join(sys.path[1], "standardize_formats.csv")
        temp_name = os.path.join(sys.path[1], "hide_standardize_formats.csv")
        os.rename(original_name, temp_name)

        # Runs the function being tested.
        sys_argv = [os.path.join(sys.path[1], "update_standardization.py"), "reports_new_formats"]
        report_folder, standardize_formats_csv, errors_list = check_arguments(sys_argv)

        # Changes standardize_formats.csv back to the correct name.
        os.rename(temp_name, original_name)

        # Tests that the value of errors_list is correct.
        expected = [f"Standardize Formats CSV '{original_name}' does not exist"]
        self.assertEqual(errors_list, expected, "Problem with csv from default: path error")

    def test_multiple_errors(self):
        """
        Test for when the required argument report_folder and optional argument standard_csv are both present
        but neither is a valid path.
        """
        # Runs the function being tested.
        sys_argv = [os.path.join(sys.path[1], "update_standardization.py"), "reports_error", "standardize_error.csv"]
        report_folder, standardize_formats_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of errors_list is correct.
        expected = ["Report folder 'reports_error' does not exist",
                    "Standardize Formats CSV 'standardize_error.csv' does not exist"]
        self.assertEqual(errors_list, expected, "Problem with multiple errors")

    def test_report_correct(self):
        """
        Test for when the required argument report_folder is present and a valid path.
        """
        # Runs the function being tested.
        sys_argv = [os.path.join(sys.path[1], "update_standardization.py"), "reports_new_formats"]
        report_folder, standardize_formats_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of report_folder is correct.
        expected = "reports_new_formats"
        self.assertEqual(report_folder, expected, "Problem with report: correct")

        # Tests that there were no errors (list is empty).
        self.assertEqual(len(errors_list), 0, "Problem with report: correct, errors list")

    def test_report_missing(self):
        """
        Test for when the required argument report_folder is not present.
        """
        # Runs the function being tested.
        sys_argv = [os.path.join(sys.path[1], "update_standardization.py")]
        report_folder, standardize_formats_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of errors_list is correct.
        expected = ["Required argument report_folder_folder_folder is missing"]
        self.assertEqual(errors_list, expected, "Problem with report: missing")

    def test_report_path_error(self):
        """
        Test for when the required argument report_folder is present but not a valid path.
        """
        # Runs the function being tested.
        sys_argv = [os.path.join(sys.path[1], "update_standardization.py"), "reports_error"]
        report_folder, standardize_formats_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of errors_list is correct.
        expected = ["Report folder 'reports_error' does not exist"]
        self.assertEqual(errors_list, expected, "Problem with report: path error")


if __name__ == '__main__':
    unittest.main()
