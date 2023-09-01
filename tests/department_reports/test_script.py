"""
Tests the entire script department_reports.py,
which makes summaries of data from the archive_formats_by_aip.csv for each department.
"""

import os
import pandas as pd
import subprocess
import unittest


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """
        Deletes the Excel spreadsheets produced by the script, if they were made by the test.
        """
        filenames = []
        for filename in filenames:
            if os.path.exists(filename):
                os.remove(filename)

    def test_correct_input(self):
        """
        Test for running the script on a valid archive_formats_by_aip CSV.
        """
        # Runs the script.
        script_path = os.path.join("..", "..", "department_reports.py")
        format_csv = os.path.join("script", "archive_formats_by_aip_2023-09.csv")
        subprocess.run(f"python {script_path} {format_csv}")

        # Reads the BMAC Excel file into pandas, and then each sheet into a separate dataframe.
        bmac = pd.ExcelFile("bmac_risk_report.xlsx")
        df_b1 = pd.read_excel(bmac, "AIP Risk Data")
        bmac.close()

        # Reads the Hargrett Excel file into pandas, and then each sheet into a separate dataframe.
        hargrett = pd.ExcelFile("hargrett_risk_report.xlsx")
        df_h1 = pd.read_excel(hargrett, "AIP Risk Data")
        hargrett.close()

        # Tests if the BMAC AIP Risk Data sheet has the expected values.
        result_b1 = [df_b1.columns.tolist()] + df_b1.values.tolist()
        expected_b1 = [["Group", "Collection", "AIP", "Format Name", "Format Version", "PRONOM URL"],
                       ["bmac", "peabody", "bmac_51021enr-1a", "Wave", "NO VALUE", "NO VALUE"],
                       ["bmac", "peabody", "bmac_51021enr-1b", "Wave", "NO VALUE", "NO VALUE"]]
        self.assertEqual(result_b1, expected_b1, "Problem with BMAC AIP Risk Data")

        # Tests if teh Hargrett AIP Risk Data sheet has the expected values.
        result_h1 = [df_h1.columns.tolist()] + df_h1.values.tolist()
        expected_h1 = [["hargrett", "harg-ms3786", "harg-ms3786er0004", "JPEG EXIF", "2.1",
                        "https://www.nationalarchives.gov.uk/pronom/x-fmt/390"],
                       ["hargrett", "harg-ms3786", "harg-ms3786er0001", "JPEG File Interchange Format", "1.01",
                        "https://www.nationalarchives.gov.uk/pronom/fmt/43"],
                       ["hargrett", "harg-0000", "harg-0000-web-202007-0001", "WARC", "NO VALUE",
                        "https://www.nationalarchives.gov.uk/pronom/fmt/289"],
                       ["hargrett", "harg-0000", "harg-0000-web-202007-0002", "WARC", "NO VALUE",
                        "https://www.nationalarchives.gov.uk/pronom/fmt/289"]]
        self.assertEqual(result_h1, expected_h1, "Problem with Hargrett AIP Risk Data")


if __name__ == '__main__':
    unittest.main()
