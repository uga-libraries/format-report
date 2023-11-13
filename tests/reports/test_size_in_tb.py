"""
Test for the function size_in_tb(),
which finds the group sizes in the usage report
and returns a dataframe with the sizes for each group, converted to TB.

For input, tests use files in the reports folder of this script repo.
The names of the input CSV does not follow the naming convention used in production
so that the variations can be saved to the same folder in the repo for easier organization.
"""

import os
import unittest
from reports import size_in_tb


class MyTestCase(unittest.TestCase):

    def test_usage_report_all(self):
        """
        Test for when the usage report contains all groups that are included in format analysis,
        and no other groups, with a mix of size units.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        size_by_group = size_in_tb(os.path.join("size_in_tb", "usage_report_20170101_20171231.csv"))
        result = [size_by_group.columns.tolist()] + size_by_group.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Size"], ["bmac", 868.0], ["dlg", 34.3], ["dlg-hargrett", 0.33], ["dlg-magil", 1.91],
                    ["hargrett", 0.82], ["magil", 0.43], ["russell", 42.4]]
        self.assertEqual(result, expected, "Problem with test for usage: all")

    def test_usage_report_byte(self):
        """
        Test for when the sizes in the usage report are all in bytes.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        size_by_group = size_in_tb(os.path.join("size_in_tb", "usage_report_20180101_20181231.csv"))
        result = [size_by_group.columns.tolist()] + size_by_group.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Size"], ["hargrett", 0.0], ["magil", 0.0]]
        self.assertEqual(result, expected, "Problem with test for usage: byte")

    def test_usage_report_kb(self):
        """
        Test for when the sizes in the usage report are all in KBs.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        size_by_group = size_in_tb(os.path.join("size_in_tb", "usage_report_20190101_20191231.csv"))
        result = [size_by_group.columns.tolist()] + size_by_group.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Size"], ["hargrett", 0.0], ["magil", 0.0]]
        self.assertEqual(result, expected, "Problem with test for usage: KB")

    def test_usage_report_mb(self):
        """
        Test for when the sizes in the usage report are all in MBs.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        size_by_group = size_in_tb(os.path.join("size_in_tb", "usage_report_20200101_20201231.csv"))
        result = [size_by_group.columns.tolist()] + size_by_group.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Size"], ["dlg-hargrett", 0]]
        self.assertEqual(result, expected, "Problem with test for usage: MB")

    def test_usage_report_gb(self):
        """
        Test for when the sizes in the usage report are all in GBs.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        size_by_group = size_in_tb(os.path.join("size_in_tb", "usage_report_20210101_20211231.csv"))
        result = [size_by_group.columns.tolist()] + size_by_group.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Size"], ["dlg-hargrett", 0.33], ["hargrett", 0.82]]
        self.assertEqual(result, expected, "Problem with test for usage: GB")

    def test_usage_report_tb(self):
        """
        Test for when the sizes in the usage report are all in TBs.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        size_by_group = size_in_tb(os.path.join("size_in_tb", "usage_report_20220101_20221231.csv"))
        result = [size_by_group.columns.tolist()] + size_by_group.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Size"], ["bmac", 868], ["dlg", 34.3], ["dlg-magil", 1.91]]
        self.assertEqual(result, expected, "Problem with test for usage: TB")

    def test_usage_unexpected_group(self):
        """
        Test for when the usage report contains all groups that are included in format analysis,
        as well as additional groups that are not included, with a mix of size units.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        size_by_group = size_in_tb(os.path.join("size_in_tb", "usage_report_20230101_20231231.csv"))
        result = [size_by_group.columns.tolist()] + size_by_group.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Size"], ["bmac", 868.0], ["dlg", 34.3], ["dlg-hargrett", 0.33], ["dlg-magil", 1.91],
                    ["hargrett", 0.82], ["magil", 0.43], ["russell", 42.4]]
        self.assertEqual(result, expected, "Problem with test for usage: unexpected group")

    def test_usage_report_unexpected_unit(self):
        """
        Test for when the sizes in the usage report are in PB (which isn't accounted for in the function) and TB.
        """
        # Runs the function being tested and converts the output into a list for easier comparison.
        size_by_group = size_in_tb(os.path.join("size_in_tb", "usage_report_20240101_20241231.csv"))
        result = [size_by_group.columns.tolist()] + size_by_group.reset_index().values.tolist()

        # Tests if the function output has the expected values.
        expected = [["Size"], ["bmac", 0], ["dlg", 34.3]]
        self.assertEqual(result, expected, "Problem with test for usage: unexpected unit")


if __name__ == '__main__':
    unittest.main()
