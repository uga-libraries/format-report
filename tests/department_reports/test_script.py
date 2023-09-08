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
        file_paths = [os.path.join("script", "bmac_risk_report.xlsx"),
                      os.path.join("script", "hargrett_risk_report.xlsx")]
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_argument_error(self):
        """
        Test for running the script without the required argument.
        It will print a message and exit the script.
        """
        # Tests that the script exits due to the error.
        script_path = os.path.join("..", "..", "department_reports.py")
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {script_path}", shell=True, check=True)

        # Tests if the expected message was produced. In production, this is printed to the terminal.
        # Must run the script a second time because cannot capture output within self.assertRaises.
        output = subprocess.run(f"python {script_path}", shell=True, stdout=subprocess.PIPE)
        msg_result = output.stdout.decode("utf-8")
        msg_expected = "Required argument format_csv is missing\r\n" \
                       "Script usage: python path/department_reports.py archive_formats_by_aip\r\n"
        self.assertEqual(msg_result, msg_expected, "Problem with test for error argument, message")

    def test_correct_input(self):
        """
        Test for running the script on a valid archive_formats_by_aip CSV.
        """
        # Runs the script.
        script_path = os.path.join("..", "..", "department_reports.py")
        format_csv = os.path.join("script", "archive_formats_by_aip_2023-09.csv")
        subprocess.run(f"python {script_path} {format_csv}")
        self.assertEqual(True, True)

        # Reads the BMAC Excel file into pandas, and then each sheet into a separate dataframe.
        bmac = pd.ExcelFile(os.path.join("script", "bmac_risk_report.xlsx"))
        df_b1 = pd.read_excel(bmac, "AIP Risk Data")
        df_b2 = pd.read_excel(bmac, "Collection Risk Levels")
        bmac.close()

        # Reads the Hargrett Excel file into pandas, and then each sheet into a separate dataframe.
        hargrett = pd.ExcelFile(os.path.join("script", "hargrett_risk_report.xlsx"))
        df_h1 = pd.read_excel(hargrett, "AIP Risk Data")
        df_h2 = pd.read_excel(hargrett, "Collection Risk Levels")
        hargrett.close()

        # Tests if the BMAC AIP Risk Data sheet has the expected values.
        result_b1 = [df_b1.columns.tolist()] + df_b1.values.tolist()
        expected_b1 = [["Group", "Collection", "AIP", "Format Name", "Format Version", "PRONOM URL",
                        "NARA_Risk Level", "NARA_Proposed Preservation Plan"],
                       ["bmac", "peabody", "bmac_51021enr-1a", "Wave", "NO VALUE", "NO VALUE", "Low Risk", "Retain"],
                       ["bmac", "hm-lawton", "bmac_hm-lawton_0021", "cue", "NO VALUE", "NO VALUE", "No Match",
                        "NO VALUE"]]
        self.assertEqual(result_b1, expected_b1, "Problem with BMAC AIP Risk Data")

        # Tests if the BMAC Collection Risk Levels sheet has the expected values.
        result_b2 = [df_b2.columns.tolist()] + df_b2.values.tolist()
        expected_b2 = [["Collection", "Low Risk", "No Match", "AIPs"],
                       ["hm-lawton", 0, 1, 1], ["peabody", 1, 0, 1], ["All", 1, 1, 2]]
        self.assertEqual(result_b2, expected_b2, "Problem with BMAC Collection Risk Levels")

        # Tests if the Hargrett AIP Risk Data sheet has the expected values.
        result_h1 = [df_h1.columns.tolist()] + df_h1.values.tolist()
        expected_h1 = [["Group", "Collection", "AIP", "Format Name", "Format Version", "PRONOM URL",
                        "NARA_Risk Level", "NARA_Proposed Preservation Plan"],
                       ["hargrett", "harg-ms3786", "harg-ms3786er0004", "CorelDraw Drawing", "8.0",
                        "https://www.nationalarchives.gov.uk/pronom/x-fmt/292", "High Risk",
                        "Transform to a TBD format, possibly PDF or TIFF"],
                       ["hargrett", "harg-ms3786", "harg-ms3786er0001", "JPEG File Interchange Format", "1.01",
                        "https://www.nationalarchives.gov.uk/pronom/fmt/43", "Low Risk", "Retain"],
                       ["hargrett", "harg-0000", "harg-0000-web-202007-0001", "WARC", "NO VALUE",
                        "https://www.nationalarchives.gov.uk/pronom/fmt/289", "Low Risk", "Retain"],
                       ["hargrett", "harg-0000", "harg-0000-web-202007-0002", "WARC", "NO VALUE",
                        "https://www.nationalarchives.gov.uk/pronom/fmt/289", "Low Risk", "Retain"]]
        self.assertEqual(result_h1, expected_h1, "Problem with Hargrett AIP Risk Data")

        # Tests if the Hargrett Collection Risk Levels sheet has the expected values.
        result_h2 = [df_h2.columns.tolist()] + df_h2.values.tolist()
        expected_h2 = [["Collection", "High Risk", "Low Risk", "AIPs"],
                       ["harg-0000", 0, 2, 2], ["harg-ms3786", 1, 1, 2], ["All", 1, 3, 4]]
        self.assertEqual(result_h2, expected_h2, "Problem with Hargrett Collection Risk Levels")


if __name__ == '__main__':
    unittest.main()
