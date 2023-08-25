"""
Tests for the function check_arguments(),
which verifies the two required arguments are present and are valid paths,
and returns the paths and a list of errors (if any).

For input, tests use a list with argument values. In production, this would be the contents of sys.argv.
"""

import os
import sys
import unittest
from merge_format_reports import check_arguments


class MyTestCase(unittest.TestCase):

    def test_both_correct(self):
        """
        Test for when both required arguments are present and valid paths.
        """
        # Makes the variable used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "merge_format_reports.py") 
        sys_argv = [script_path, "reports_one", "NARA_PreservationActionPlan_FileFormats_test.csv"]
        report_folder, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of report_folder is correct.
        expected = "reports_one"
        self.assertEqual(report_folder, expected, "Problem with both: correct, report path")

        # Tests that the value of nara_csv is correct.
        expected = "NARA_PreservationActionPlan_FileFormats_test.csv"
        self.assertEqual(nara_csv, expected, "Problem with both: correct, nara path")
        
        # Tests that the value of errors_list is correct.
        self.assertEqual(errors_list, [], "Problem with both: correct, errors list")

    def test_both_missing(self):
        """
        Test for when neither required argument is present.
        """
        # Makes the variable used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "merge_format_reports.py")
        sys_argv = [script_path]
        report_folder, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of report_folder is correct.
        self.assertEqual(report_folder, None, "Problem with both: missing, report path")

        # Tests that the value of nara_csv is correct.
        self.assertEqual(nara_csv, None, "Problem with both: missing, nara path")

        # Tests that the value of errors_list is correct.
        expected = ["Required argument report_folder is missing",
                    "Required argument nara_csv is missing"]
        self.assertEqual(errors_list, expected, "Problem with both: missing, errors list")

    def test_both_path_error(self):
        """
        Test for when both required arguments are present but are not valid paths.
        """
        # Makes the variable used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "merge_format_reports.py")
        sys_argv = [script_path, "reports_error", "nara_error.csv"]
        report_folder, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of report_folder is correct.
        expected = "reports_error"
        self.assertEqual(report_folder, expected, "Problem with both: path error, report path")

        # Tests that the value of nara_csv is correct.
        expected = "nara_error.csv"
        self.assertEqual(nara_csv, expected, "Problem with both: path error, nara path")

        # Tests that the value of errors_list is correct.
        expected = ["Report folder 'reports_error' does not exist",
                    "NARA CSV 'nara_error.csv' does not exist"]
        self.assertEqual(errors_list, expected, "Problem with both: path error, errors list")

    def test_report_missing(self):
        """
        Test for when the first required argument report_folder is not present.
        The second required argument, nara_csv, is present and valid,
        so the function treats it as report_path.
        """
        # Makes the variable used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "merge_format_reports.py")
        sys_argv = [script_path, "NARA_PreservationActionPlan_FileFormats_test.csv"]
        report_folder, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of report_folder is correct.
        expected = "NARA_PreservationActionPlan_FileFormats_test.csv"
        self.assertEqual(report_folder, expected, "Problem with report: missing, report path")

        # Tests that the value of nara_csv is correct.
        expected = None
        self.assertEqual(nara_csv, expected, "Problem with report: missing, nara path")

        # Tests that the value of errors_list is correct.
        expected = ["Required argument nara_csv is missing"]
        self.assertEqual(errors_list, expected, "Problem with report: missing, errors list")

    def test_report_path_error(self):
        """
        Test for when the first required argument report_folder is present but not a valid path.
        The second required argument, nara_csv, is present and valid.
        """
        # Makes the variable used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "merge_format_reports.py")
        sys_argv = [script_path, "reports_error", "NARA_PreservationActionPlan_FileFormats_test.csv"]
        report_folder, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of report_folder is correct.
        expected = "reports_error"
        self.assertEqual(report_folder, expected, "Problem with report: path error, report path")

        # Tests that the value of nara_csv is correct.
        expected = "NARA_PreservationActionPlan_FileFormats_test.csv"
        self.assertEqual(nara_csv, expected, "Problem with report: path error, nara path")

        # Tests that the value of errors_list is correct.
        expected = ["Report folder 'reports_error' does not exist"]
        self.assertEqual(errors_list, expected, "Problem with report: path error, errors list")

    def test_nara_missing(self):
        """
        Test for when the second required argument nara_csv is not present.
        The first required argument, report_folder, is present and valid.
        """
        # Makes the variable used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "merge_format_reports.py")
        sys_argv = [script_path, "reports_one"]
        report_folder, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of report_folder is correct.
        expected = "reports_one"
        self.assertEqual(report_folder, expected, "Problem with NARA: missing, report path")

        # Tests that the value of nara_csv is correct.
        self.assertEqual(nara_csv, None, "Problem with NARA: missing, nara path")

        # Tests that the value of errors_list is correct.
        expected = ["Required argument nara_csv is missing"]
        self.assertEqual(errors_list, expected, "Problem with NARA: missing, errors list")

    def test_nara_path_error(self):
        """
        Test for when the second required argument nara_csv is present but not a valid path.
        The first required argument, report_folder, is present and valid.
        """
        # Makes the variable used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "merge_format_reports.py")
        sys_argv = [script_path, "reports_one", "nara_error.csv"]
        report_folder, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of report_folder is correct.
        expected = "reports_one"
        self.assertEqual(report_folder, expected, "Problem with NARA: path error, report path")

        # Tests that the value of nara_csv is correct.
        expected = "nara_error.csv"
        self.assertEqual(nara_csv, expected, "Problem with NARA: path error, nara path")

        # Tests that the value of errors_list is correct.
        expected = ["NARA CSV 'nara_error.csv' does not exist"]
        self.assertEqual(errors_list, expected, "Problem with NARA: path error, errors list")


if __name__ == '__main__':
    unittest.main()
