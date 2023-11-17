"""
Tests the entire script fix_versions.py,
which fixes errors in the version caused by openening the CSV in Excel.
"""

import os
import subprocess
import unittest


class MyTestCase(unittest.TestCase):

    def test_argument_error(self):
        """
        Test for running the script with the required argument.
        It will print a message and exit the script.
        """
        script_path = os.path.join("..", "..", "fix_versions.py")

        # Tests that the script exits due to the error.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {script_path}", shell=True, check=True)

        # Tests that the expected error message was produced. In production, this is printed to the terminal.
        # Run the script a second time because cannot capture output within self.assertRaises.
        output = subprocess.run(f"python {script_path}", shell=True, stdout=subprocess.PIPE)
        error_msg = output.stdout.decode("utf-8")
        expected_msg = "Required argument csv_path is missing\r\n"
        self.assertEqual(error_msg, expected_msg, "Problem with test for argument error, error message")


if __name__ == '__main__':
    unittest.main()
