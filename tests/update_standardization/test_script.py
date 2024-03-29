"""
Tests the entire script update_standardization.py,
which compares all formats in the format archive_reports to the standardize_formats.csv
and creates a file new_formats.txt if any are not in standardize_formats.csv.

For input, tests use format archive_reports that are in the update_standardization tests folder of this script repo.
"""

import os
import subprocess
import unittest


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """
        Deletes the new_formats.txt file, if it is made by the test.
        """
        file_path = os.path.join("reports_new_formats", "new_formats.txt")
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_argument_error(self):
        """
        Test for running the script without the required argument.
        It will print a message and exit the script.
        """
        # Runs the script without the required argument
        # and tests that the script exits.
        script_path = os.path.join("..", "..", "update_standardization.py")

        # Tests that the script exits due to the error.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {script_path}", shell=True, check=True)

        # Tests if the expected message was produced. In production, this is printed to the terminal.
        # Must run the script a second time because cannot capture output within self.assertRaises.
        output = subprocess.run(f"python {script_path}", shell=True, stdout=subprocess.PIPE)
        msg_result = output.stdout.decode("utf-8")
        msg_expected = "Required argument report_folder is missing\r\n" \
                       "Script usage: python path/update_standardization.py report_folder\r\n"
        self.assertEqual(msg_result, msg_expected, "Problem with test for error argument, message")

    def test_new_formats(self):
        """
        Test for format archive_reports that include formats which are not in standardize_formats.csv.
        Two new formats (New AV 1 and New AV 2) are in both format archive_reports.
        Two new formats (New AV 3 and New Text 1) are each in one format report.
        There is a new format at the beginning, middle, and end of each format report.
        """
        # Runs the script.
        script_path = os.path.join("..", "..", "update_standardization.py")
        output = subprocess.run(f"python {script_path} reports_new_formats", shell=True, stdout=subprocess.PIPE)

        # Tests if the expected message was produced. In production, this is printed to the terminal.
        msg_result = output.stdout.decode("utf-8")
        msg_expected = "New formats were found: check new_formats.txt in report_folder\r\n"
        self.assertEqual(msg_result, msg_expected, "Problem with new formats, message")

        # Tests if the new_formats.txt file has the expected values.
        with open(os.path.join("reports_new_formats", "new_formats.txt"), "r") as file:
            result = file.read()
        expected = "New AV 1\nNew AV 2\nNew AV 3\nNew Text 1\n"
        self.assertEqual(result, expected, "Problem with new formats, new_formats.txt")

    def test_no_new_formats(self):
        """
        Test for format archive_reports where all formats are in standardize_formats.csv.
        """
        # Runs the script.
        script_path = os.path.join("..", "..", "update_standardization.py")
        output = subprocess.run(f"python {script_path} reports_no_new_formats", shell=True, stdout=subprocess.PIPE)

        # Tests that no message was produced. In production, only prints if there are new formats.
        msg_result = output.stdout.decode("utf-8")
        msg_expected = ""
        self.assertEqual(msg_result, msg_expected, "Problem with no new formats, message")

        # Tests that the new_formats.txt file was not created.
        result = os.path.exists(os.path.join("reports_no_new_formats", "new_formats.txt"))
        self.assertEqual(result, False, "Problem with no new formats, new_formats.txt")


if __name__ == '__main__':
    unittest.main()
