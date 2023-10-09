"""
Tests for the function check_argument(),
which verifies the required argument is present, a valid path, and named correctly,
and returns the path and a list of errors (if any).

For input, tests use a list of argument values. In production, this would be the contents of sys_argv.
"""

import os
import sys
import unittest
from department_reports import check_arguments


class MyTestCase(unittest.TestCase):

    def test_both_correct(self):
        """
        Test for when the required arguments are present, valid paths, and named correctly.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        second_arg = "hargrett_risk_report_202110.xlsx"
        format_csv, previous_risk_xlsx, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of format_csv is correct.
        expected_format = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        self.assertEqual(format_csv, expected_format, "Problem with test for both arguments correct, format_csv")

        # Tests that the value of previous_risk_xlsx is correct.
        expected_previous = "hargrett_risk_report_202110.xlsx"
        self.assertEqual(previous_risk_xlsx, expected_previous,
                         "Problem with test for both arguments correct, previous_risk_xlsx")

        # Tests that the value of errors_list is correct.
        expected_list = []
        self.assertEqual(errors_list, expected_list, "Problem with test for both arguments correct, errors_list")

    def test_both_error(self):
        """
        Test for when both required arguments have an error:
        format_csv is not a valid path and previous_risk_xlsx is missing.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("error", "archive_formats_by_aip_2023-08.csv")
        format_csv, previous_risk_xlsx, errors_list = check_arguments([script_path, first_arg])

        # Tests that the value of format_csv is correct.
        expected_format = os.path.join("error", "archive_formats_by_aip_2023-08.csv")
        self.assertEqual(format_csv, expected_format, "Problem with test for both arguments error, format_csv")

        # Tests that the value of previous_risk_xlsx is correct.
        expected_previous = None
        self.assertEqual(previous_risk_xlsx, expected_previous,
                         "Problem with test for both arguments error, previous_risk_xlsx")

        # Tests that the value of errors_list is correct.
        expected_list = [f"archive_formats_by_aip_csv '{first_arg}' does not exist",
                         "Required argument dept_risk_report is missing"]
        self.assertEqual(errors_list, expected_list, "Problem with test for both arguments error, errors_list")

    def test_format_missing(self):
        """
        Test for when the first required argument format_csv is missing.
        The other required argument, previous_risk_xlsx, is present and correct.
        This causes the value of previous_risk_xlsx to be assigned to format_csv.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        second_arg = "hargrett_risk_report_202110.xlsx"
        format_csv, previous_risk_xlsx, errors_list = check_arguments([script_path, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = ["archive_formats_by_aip_csv 'hargrett_risk_report_202110.xlsx' is not the correct type (should be by_aip.csv)",
                         "Required argument dept_risk_report is missing"]
        self.assertEqual(errors_list, expected_list, "Problem with test for format_csv is missing")

    def test_format_name_error(self):
        """
        Test for when the first required argument format_csv is present and a valid path but is not named correctly.
        The other required argument, previous_risk_xlsx, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_group_2023-08.csv")
        second_arg = "hargrett_risk_report_202110.xlsx"
        format_csv, previous_risk_xlsx, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"archive_formats_by_aip_csv '{first_arg}' is not the correct type (should be by_aip.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for format_csv name error")

    def test_format_name_extension_error(self):
        """
        Test for when the first required argument format_csv is present and a valid path
        but is not the correct file extension.
        The other required argument, previous_risk_xlsx, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.xlsx")
        second_arg = "hargrett_risk_report_202110.xlsx"
        format_csv, previous_risk_xlsx, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"archive_formats_by_aip_csv '{first_arg}' is not the correct type (should be by_aip.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for format_csv name extension error")

    def test_format_name_and_path_error(self):
        """
        Test for when the first required argument format_csv is present
        but is not named correctly and is not a valid path.
        The other required argument, previous_risk_xlsx, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("path_error", "name_error.csv")
        second_arg = "hargrett_risk_report_202110.xlsx"
        format_csv, previous_risk_xlsx, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"archive_formats_by_aip_csv '{first_arg}' does not exist",
                         f"archive_formats_by_aip_csv '{first_arg}' is not the correct type (should be by_aip.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for format_csv name and path error")

    def test_format_path_error(self):
        """
        Test for when the first required argument format_csv is present and named correctly but is not a valid path.
        The other required argument, previous_risk_xlsx, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("path_error", "archive_formats_by_aip_2023-08.csv")
        second_arg = "hargrett_risk_report_202110.xlsx"
        format_csv, previous_risk_xlsx, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"archive_formats_by_aip_csv '{first_arg}' does not exist"]
        self.assertEqual(errors_list, expected_list, "Problem with test for format_csv path error")

    def test_previous_missing(self):
        """
        Test for when the second required argument previous_risk_xlsx is missing.
        The first required argument, format_csv, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        format_csv, previous_risk_xlsx, errors_list = check_arguments([script_path, first_arg])

        # Tests that the value of errors_list is correct.
        expected_list = ["Required argument dept_risk_report is missing"]
        self.assertEqual(errors_list, expected_list, "Problem with test for previous_risk_xlsx is missing")

    def test_previous_name_error(self):
        """
        Test for when the second required argument previous_risk_xlsx is present and a valid path
        but is not named correctly.
        The first required argument, format_csv, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        second_arg = os.path.join("check_arguments", "hargrett.xlsx")
        format_csv, previous_risk_xlsx, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"dept_risk_report '{second_arg}' is not the correct type (should be dept_risk_report.xlsx)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for previous_risk_xlsx name error")

    def test_previous_name_extension_error(self):
        """
        Test for when the second required argument previous_risk_xlsx is present and a valid path
        but is not the correct file extension.
        The first required argument, format_csv, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        second_arg = os.path.join("check_arguments", "hargrett_risk_report_202110.ods")
        format_csv, previous_risk_xlsx, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"dept_risk_report '{second_arg}' is not the correct type (should be dept_risk_report.xlsx)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for previous_risk_xlsx name extension error")

    def test_previous_name_and_path_error(self):
        """
        Test for when the second required argument previous_risk_xlsx is present
        but is not named correctly and is not a valid path.
        The first required argument, format_csv, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        second_arg = os.path.join("path_error", "name_error.xlsx")
        format_csv, previous_risk_xlsx, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"dept_risk_report '{second_arg}' does not exist",
                         f"dept_risk_report '{second_arg}' is not the correct type (should be dept_risk_report.xlsx)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for previous_risk_xlsx name and path error")

    def test_previous_path_error(self):
        """
        Test for when the second required argument previous_risk_xlsx is present and named correctly
        but is not a valid path.
        The first required argument, format_csv, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        second_arg = os.path.join("path error", "hargrett_risk_report_202110.xlsx")
        format_csv, previous_risk_xlsx, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"dept_risk_report '{second_arg}' does not exist"]
        self.assertEqual(errors_list, expected_list, "Problem with test for previous_risk_xlsx path error")


if __name__ == '__main__':
    unittest.main()
