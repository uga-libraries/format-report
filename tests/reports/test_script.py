"""
Tests the entire script reports.py,
which makes summaries of data from combined ARCHive format reports and the usage report.

For input, tests use files in the reports folder of this script repo.
"""

import datetime
import os
import subprocess
import sys
import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """
        Calculates variables that are used in all or most tests:
        the path to reports.py (used to run the script) and the date (used in naming script output).
        """
        self.script_path = os.path.join("..", "..", "reports.py")
        self.today = datetime.datetime.now().strftime("%Y-%m")

    def tearDown(self):
        """
        Deletes the Excel spreadsheet produced by the script, if it is made by the test.
        """
        file_paths = []
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_missing_argument(self):
        """
        Test for running the script without the required argument.
        It will print a message and exit the script.
        """
        # Runs the script without the required argument and tests that the script exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {self.script_path}", shell=True, check=True)

        # Tests if the expected message was produced. In production, this is printed to the terminal.
        # Must run the script a second time because cannot capture output with self.assertRaises.
        output = subprocess.run(f"python {self.script_path}", shell=True, stdout=subprocess.PIPE)
        msg_result = output.stdout.decode("utf-8")
        msg_expected = "The report folder path was either not given or is not a valid directory. " \
                       "Please try the script again.\r\n" \
                       "Script usage: python path/reports.py report_folder\r\n"
        self.assertEqual(msg_result, msg_expected, "Problem with test for missing argument, message")

    def test_missing_input(self):
        """
        Test for running the script on a report_folder without the expected reports.
        It will print a message and exit the script.
        """
        # Runs the script without the required argument and tests that the script exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {self.script_path} missing_input_all", shell=True, check=True)

        # Tests if the expected message was produced. In production, this is printed to the terminal.
        # Must run the script a second time because cannot capture output with self.assertRaises.
        output = subprocess.run(f"python {self.script_path} missing_input_all", shell=True, stdout=subprocess.PIPE)
        msg_result = output.stdout.decode("utf-8")
        msg_expected = "Could not find the archive_formats_by_aip report in the report folder.\r\n" \
                       "Could not find the archive_formats report in the report folder.\r\n" \
                       "Could not find the usage report in the report folder.\r\n" \
                       "Please add the missing report(s) to the report folder and run this script again.\r\n"
        self.assertEqual(msg_result, msg_expected, "Problem with test for missing input, message")

    def test_no_blank_tabs(self):
        """
        Test for ARCHive format reports with data for every possible analysis type,
        which results in data in all 15 of the Excel tabs.
        """
        # Runs the script.
        subprocess.run(f"python {self.script_path} no_blank_tabs", shell=True)

        # Tests if the output has the expected values.
        self.assertEqual(True, True, "No Blank Tabs is TBD")

    def test_some_blank_tabs(self):
        """
        Test for ARCHive format reports that does not have data for every possible analysis type,
        which results in data in x/15 of the Excel tabs.
        """
        # Runs the script.
        subprocess.run(f"python {self.script_path} some_blank_tabs", shell=True)

        # Tests if the output has the expected values.
        self.assertEqual(True, True, "Some Blank Tabs is TBD")


if __name__ == '__main__':
    unittest.main()
