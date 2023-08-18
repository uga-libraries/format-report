"""
Test for the function read_report(),
which reads the data from one report and returns lists of rows to add to the CSVs.

The function does not have variations to test.
It either works or doesn't, but there is enough testing ahead of time that error handling has not been needed yet.

For input, test uses a format report that is in the merge_format_reports folder of this script repo.
"""

import os
import unittest
from merge_format_reports import read_report


class MyTestCase(unittest.TestCase):

    def test_read_report(self):
        """
        Test for reading a a report correctly.
        """
        # Runs the function being tested.
        aip_report_list, group_report_list = read_report(os.path.join("read_report", "file_formats_hargrett.csv"))

        # Tests that the aip_report_list contains the correct information.
        expected_aip = [["hargrett", "harg-ms3786", "harg-ms3786er0001", "image", "JPEG",
                         "JPEG File Interchange Format|1.02|fmt/44", "JPEG File Interchange Format", "1.02",
                         "https://www.nationalarchives.gov.uk/PRONOM", "fmt/44", "NO VALUE"],
                        ["hargrett", "harg-ms3786", "harg-ms3786er0002", "image", "JPEG",
                         "JPEG File Interchange Format|1.02|fmt/44", "JPEG File Interchange Format", "1.02",
                         "https://www.nationalarchives.gov.uk/PRONOM", "fmt/44", "NO VALUE"],
                        ["hargrett", "harg-ms3770", "harg-ms3770er0002", "text", "Plain Text File",
                         "Plain text|NO VALUE|NO VALUE", "Plain text", "NO VALUE", "NO VALUE", "NO VALUE",
                         "For testing"]]
        self.assertEqual(aip_report_list, expected_aip, "Problem with aip_report_list")

        # Tests that the group_report_list contains the correct information.
        expected_group = [["hargrett", "1474", "2.001", "image", "JPEG", "JPEG File Interchange Format|1.02|fmt/44",
                           "JPEG File Interchange Format", "1.02", "https://www.nationalarchives.gov.uk/PRONOM",
                           "fmt/44", "NO VALUE"],
                          ["hargrett", "48", "0.001", "text", "Plain Text File", "Plain text|NO VALUE|NO VALUE",
                           "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "For testing"]]
        self.assertEqual(group_report_list, expected_group, "Problem with group_report_list")


if __name__ == '__main__':
    unittest.main()
