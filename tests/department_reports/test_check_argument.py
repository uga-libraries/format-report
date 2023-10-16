"""
Tests for the function check_arguments(),
which verifies that both required arguments are present, the paths are valid,
and they have the expected data based on the filenames.
Returns both arguments and a list of errors.

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
        current_formats_csv, previous_formats_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of current_formats_csv is correct.
        expected_format = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        self.assertEqual(current_formats_csv, expected_format, 
                         "Problem with test for both arguments correct, current_formats_csv")

        # Tests that the value of previous_formats_csv is correct.
        expected_previous = "archive_formats_by_aip_2021-08.csv"
        self.assertEqual(previous_formats_csv, expected_previous,
                         "Problem with test for both arguments correct, previous_formats_csv")

        # Tests that the value of errors_list is correct.
        expected_list = []
        self.assertEqual(errors_list, expected_list, "Problem with test for both arguments correct, errors_list")

    def test_both_error(self):
        """
        Test for when both required arguments have an error:
        current_formats_csv is not a valid path and previous_formats_csv is missing.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("error", "archive_formats_by_aip_2023-08.csv")
        current_formats_csv, previous_formats_csv, errors_list = check_arguments([script_path, first_arg])

        # Tests that the value of current_formats_csv is correct.
        expected_format = os.path.join("error", "archive_formats_by_aip_2023-08.csv")
        self.assertEqual(current_formats_csv, expected_format, 
                         "Problem with test for both arguments error, current_formats_csv")

        # Tests that the value of previous_formats_csv is correct.
        expected_previous = None
        self.assertEqual(previous_formats_csv, expected_previous,
                         "Problem with test for both arguments error, previous_formats_csv")

        # Tests that the value of errors_list is correct.
        expected_list = [f"current_formats_csv '{first_arg}' does not exist",
                         "Required argument previous_formats_csv is missing"]
        self.assertEqual(errors_list, expected_list, "Problem with test for both arguments error, errors_list")

    def test_current_missing(self):
        """
        Test for when the first required argument current_formats_csv is missing.
        The other required argument, previous_formats_csv, is present and correct.
        This causes the value of previous_formats_csv to be assigned to current_formats_csv.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        second_arg = "archive_formats_by_aip_2021-08.csv"
        current_formats_csv, previous_formats_csv, errors_list = check_arguments([script_path, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = ["Required argument previous_formats_csv is missing"]
        self.assertEqual(errors_list, expected_list, "Problem with test for current_formats_csv is missing")

    def test_current_name_error(self):
        """
        Test for when the first required argument current_formats_csv is present and a valid path
        but is not named correctly.
        The other required argument, previous_formats_csv, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_group_2023-08.csv")
        second_arg = "archive_formats_by_aip_2021-08.csv"
        current_formats_csv, previous_formats_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"'{first_arg}' is not the correct type (should be archive_formats_by_aip_date.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for current_formats_csv name error")

    def test_current_name_extension_error(self):
        """
        Test for when the first required argument current_formats_csv is present and a valid path
        but is not the correct file extension.
        The other required argument, previous_formats_csv, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.xlsx")
        second_arg = "archive_formats_by_aip_2021-08.csv"
        current_formats_csv, previous_formats_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"'{first_arg}' is not the correct type (should be archive_formats_by_aip_date.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for current_formats_csv name extension error")

    def test_current_name_and_path_error(self):
        """
        Test for when the first required argument current_formats_csv is present
        but is not named correctly and is not a valid path.
        The other required argument, previous_formats_csv, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("path_error", "name_error.csv")
        second_arg = "archive_formats_by_aip_2021-08.csv"
        current_formats_csv, previous_formats_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"current_formats_csv '{first_arg}' does not exist",
                         f"'{first_arg}' is not the correct type (should be archive_formats_by_aip_date.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for current_formats_csv name and path error")

    def test_current_path_error(self):
        """
        Test for when the first required argument current_formats_csv is present and named correctly
        but is not a valid path.
        The other required argument, previous_formats_csv, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("path_error", "archive_formats_by_aip_2023-08.csv")
        second_arg = "archive_formats_by_aip_2021-08.csv"
        current_formats_csv, previous_formats_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"current_formats_csv '{first_arg}' does not exist"]
        self.assertEqual(errors_list, expected_list, "Problem with test for current_formats_csv path error")

    def test_previous_missing(self):
        """
        Test for when the second required argument previous_formats_csv is missing.
        The first required argument, current_formats_csv, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        current_formats_csv, previous_formats_csv, errors_list = check_arguments([script_path, first_arg])

        # Tests that the value of errors_list is correct.
        expected_list = ["Required argument previous_formats_csv is missing"]
        self.assertEqual(errors_list, expected_list, "Problem with test for previous_formats_csv is missing")

    def test_previous_name_error(self):
        """
        Test for when the second required argument previous_formats_csv is present and a valid path
        but is not named correctly.
        The first required argument, current_formats_csv, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        second_arg = os.path.join("check_arguments", "archive_formats_by_group_2021-08.csv")
        current_formats_csv, previous_formats_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"'{second_arg}' is not the correct type (should be archive_formats_by_aip_date.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for previous_formats_csv name error")

    def test_previous_name_extension_error(self):
        """
        Test for when the second required argument previous_formats_csv is present and a valid path
        but is not the correct file extension.
        The first required argument, current_formats_csv, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        second_arg = os.path.join("check_arguments", "archive_formats_by_aip_2021-08.xlsx")
        current_formats_csv, previous_formats_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"'{second_arg}' is not the correct type (should be archive_formats_by_aip_date.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for previous_formats_csv name extension error")

    def test_previous_name_and_path_error(self):
        """
        Test for when the second required argument previous_formats_csv is present
        but is not named correctly and is not a valid path.
        The first required argument, current_formats_csv, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        second_arg = os.path.join("path_error", "name_error.csv")
        current_formats_csv, previous_formats_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"previous_formats_csv '{second_arg}' does not exist",
                         f"'{second_arg}' is not the correct type (should be archive_formats_by_aip_date.csv)"]
        self.assertEqual(errors_list, expected_list, "Problem with test for previous_formats_csv name and path error")

    def test_previous_path_error(self):
        """
        Test for when the second required argument previous_formats_csv is present and named correctly
        but is not a valid path.
        The first required argument, current_formats_csv, is present and correct.
        """
        # Makes the variables used for function input and runs the function being tested.
        script_path = os.path.join(sys.path[1], "department_reports.py")
        first_arg = os.path.join("check_arguments", "archive_formats_by_aip_2023-08.csv")
        second_arg = os.path.join("path error", "archive_formats_by_aip_2021-08.csv")
        current_formats_csv, previous_formats_csv, errors_list = check_arguments([script_path, first_arg, second_arg])

        # Tests that the value of errors_list is correct.
        expected_list = [f"previous_formats_csv '{second_arg}' does not exist"]
        self.assertEqual(errors_list, expected_list, "Problem with test for previous_formats_csv path error")


if __name__ == '__main__':
    unittest.main()
