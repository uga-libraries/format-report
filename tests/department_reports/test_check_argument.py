"""
Tests for the function check_arguments(),
which verifies both required arguments are present, valid paths, and named correctly,
and returns the paths and a list of errors (if any).

For input, tests use a list of argument values. In production, this would be the contents of sys.argv.
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
        second_arg = "archive_formats_by_aip_2021-08.csv"
        current_format_csv, previous_format_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of current_format_csv is correct.
        expected_format = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        self.assertEqual(current_format_csv, expected_format, 
                         "Problem with test for both arguments correct, current_format_csv")

        # Tests that the value of previous_format_csv is correct.
        expected_previous = "archive_formats_by_aip_2021-08.csv"
        self.assertEqual(previous_format_csv, expected_previous,
                         "Problem with test for both arguments correct, previous_format_csv")

        # Tests that the value of errors_list is correct.
        expected_list = []
        self.assertEqual(errors_list, expected_list, "Problem with test for both arguments correct, errors_list")

    def test_both_error(self):
        """
        Test for when both required arguments have an error:
        current_format_csv is not a valid path and previous_format_csv is missing.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("error", "archive_formats_by_aip_2023-08.csv")
        current_format_csv, previous_format_csv, errors_list = check_arguments([script_path, first_arg])

        # Tests that the value of current_format_csv is correct.
        expected_format = os.path.join("error", "archive_formats_by_aip_2023-08.csv")
        self.assertEqual(current_format_csv, expected_format, 
                         "Problem with test for both arguments error, current_format_csv")

        # Tests that the value of previous_format_csv is correct.
        expected_previous = None
        self.assertEqual(previous_format_csv, expected_previous,
                         "Problem with test for both arguments error, previous_format_csv")

        # Tests that the value of errors_list is correct.
        expected_list = [f"formats_current '{first_arg}' does not exist",
                         "Required argument formats_previous is missing"]
        self.assertEqual(errors_list, expected_list, "Problem with test for both arguments error, errors_list")

    def test_current_missing(self):
        """
        Test for when the first required argument formats_current is missing.
        The other required argument, formats_previous, is present and correct.
        This causes the value of formats_previous to be assigned to formats_current.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        second_arg = "archive_formats_by_aip_2021-08.csv"
        current_format_csv, previous_format_csv, errors_list = check_arguments([script_path, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = ["Required argument formats_previous is missing"]
        self.assertEqual(errors_list, expected_list, "Problem with test for formats_current is missing")

    def test_current_name_error(self):
        """
        Test for when the first required argument formats_current is present and a valid path
        but is not named correctly.
        The other required argument, formats_previous, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_group_2023-08.csv")
        second_arg = "archive_formats_by_aip_2021-08.csv"
        current_format_csv, previous_format_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"'{first_arg}' is not the correct type (should be archive_formats_by_aip_date.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for formats_current name error")

    def test_current_name_extension_error(self):
        """
        Test for when the first required argument formats_current is present and a valid path
        but is not the correct file extension.
        The other required argument, formats_previous, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.xlsx")
        second_arg = "archive_formats_by_aip_2021-08.csv"
        current_format_csv, previous_format_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"'{first_arg}' is not the correct type (should be archive_formats_by_aip_date.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for formats_current name extension error")

    def test_current_name_and_path_error(self):
        """
        Test for when the first required argument formats_current is present
        but is not named correctly and is not a valid path.
        The other required argument, formats_previous, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("path_error", "name_error.csv")
        second_arg = "archive_formats_by_aip_2021-08.csv"
        current_format_csv, previous_format_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"formats_current '{first_arg}' does not exist",
                         f"'{first_arg}' is not the correct type (should be archive_formats_by_aip_date.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for formats_current name and path error")

    def test_current_path_error(self):
        """
        Test for when the first required argument formats_current is present and named correctly
        but is not a valid path.
        The other required argument, formats_previous, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("path_error", "archive_formats_by_aip_2023-08.csv")
        second_arg = "archive_formats_by_aip_2021-08.csv"
        current_format_csv, previous_format_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"formats_current '{first_arg}' does not exist"]
        self.assertEqual(errors_list, expected_list, "Problem with test for formats_current path error")

    def test_previous_missing(self):
        """
        Test for when the second required argument formats_previous is missing.
        The first required argument, formats_current, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        current_format_csv, previous_format_csv, errors_list = check_arguments([script_path, first_arg])

        # Tests that the value of errors_list is correct.
        expected_list = ["Required argument formats_previous is missing"]
        self.assertEqual(errors_list, expected_list, "Problem with test for formats_previous is missing")

    def test_previous_name_error(self):
        """
        Test for when the second required argument formats_previous is present and a valid path
        but is not named correctly.
        The first required argument, formats_current, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        second_arg = os.path.join("check_arguments", "archive_formats_by_group_2021-08.csv")
        current_format_csv, previous_format_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"'{second_arg}' is not the correct type (should be archive_formats_by_aip_date.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for formats_previous name error")

    def test_previous_name_extension_error(self):
        """
        Test for when the second required argument formats_previous is present and a valid path
        but is not the correct file extension.
        The first required argument, formats_current, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        second_arg = os.path.join("check_arguments", "archive_formats_by_aip_2021-08.xlsx")
        current_format_csv, previous_format_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"'{second_arg}' is not the correct type (should be archive_formats_by_aip_date.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for formats_previous name extension error")

    def test_previous_name_and_path_error(self):
        """
        Test for when the second required argument formats_previous is present
        but is not named correctly and is not a valid path.
        The first required argument, formats_current, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        second_arg = os.path.join("path_error", "name_error.csv")
        current_format_csv, previous_format_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"formats_previous '{second_arg}' does not exist",
                         f"'{second_arg}' is not the correct type (should be archive_formats_by_aip_date.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for formats_previous name and path error")

    def test_previous_path_error(self):
        """
        Test for when the second required argument formats_previous is present and named correctly
        but is not a valid path.
        The first required argument, formats_current, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        second_arg = os.path.join("path error", "archive_formats_by_aip_2021-08.csv")
        current_format_csv, previous_format_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"formats_previous '{second_arg}' does not exist"]
        self.assertEqual(errors_list, expected_list, "Problem with test for formats_previous path error")


if __name__ == '__main__':
    unittest.main()
