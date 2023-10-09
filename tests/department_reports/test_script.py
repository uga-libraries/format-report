"""
Tests the entire script department_reports.py,
which makes summaries of data from the archive_formats_by_aip.csv for each department.
"""
import datetime
import numpy as np
import os
import pandas as pd
import subprocess
import unittest


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """
        Deletes the Excel spreadsheets produced by the script, if they were made by the test.
        """
        date = datetime.date.today().strftime("%Y%m")
        file_paths = [os.path.join("script", f"bmac_risk_report_{date}.xlsx"),
                      os.path.join("script", f"hargrett_risk_report_{date}.xlsx")]
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_argument_error(self):
        """
        Test for running the script without both required arguments.
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
        msg_expected = "Required argument archive_formats_by_aip_csv is missing\r\n" \
                       "Required argument dept_risk_report is missing\r\n" \
                       "Script usage: python path/department_reports.py archive_formats_by_aip_csv dept_risk_report\r\n"
        self.assertEqual(msg_result, msg_expected, "Problem with test for error argument, message")

    def test_correct_input(self):
        """
        Test for running the script on a valid archive_formats_by_aip CSV.
        """
        # Runs the script.
        script_path = os.path.join("..", "..", "department_reports.py")
        format_csv = os.path.join("script", "archive_formats_by_aip_2023-09.csv")
        previous_risk_xlsx = "hargrett_risk_report_202110.xlsx"
        subprocess.run(f"python {script_path} {format_csv} {previous_risk_xlsx}")
        self.assertEqual(True, True)

        # Reads the BMAC Excel file into pandas, and then each sheet into a separate dataframe.
        date = datetime.date.today().strftime("%Y%m")
        bmac = pd.ExcelFile(os.path.join("script", f"bmac_risk_report_{date}.xlsx"))
        df_b1 = pd.read_excel(bmac, "AIP Risk Data")
        df_b2 = pd.read_excel(bmac, "Collection Risk Levels")
        df_b3 = pd.read_excel(bmac, "AIP Risk Levels")
        df_b4 = pd.read_excel(bmac, "Formats")
        bmac.close()

        # Reads the Hargrett Excel file into pandas, and then each sheet into a separate dataframe.
        hargrett = pd.ExcelFile(os.path.join("script", f"hargrett_risk_report_{date}.xlsx"))
        df_h1 = pd.read_excel(hargrett, "AIP Risk Data")
        df_h2 = pd.read_excel(hargrett, "Collection Risk Levels")
        df_h3 = pd.read_excel(hargrett, "AIP Risk Levels")
        df_h4 = pd.read_excel(hargrett, "Formats")
        hargrett.close()

        # Tests if the BMAC AIP Risk Data sheet has the expected values.
        result_b1 = [df_b1.columns.tolist()] + df_b1.values.tolist()
        expected_b1 = [["Group", "Collection", "AIP", "Format Name", "Format Version", "PRONOM URL",
                        "NARA_Risk Level", "NARA_Proposed Preservation Plan"],
                       ["bmac", "hm-lawton", "bmac_hm-lawton_0001", "Wave", "NO VALUE", "NO VALUE", "Low Risk",
                        "Retain"],
                       ["bmac", "hm-lawton", "bmac_hm-lawton_0002", "cue", "NO VALUE", "NO VALUE", "No Match",
                        "NO VALUE"]]
        self.assertEqual(result_b1, expected_b1, "Problem with BMAC AIP Risk Data")

        # Tests if the BMAC Collection Risk Levels sheet has the expected values.
        result_b2 = [df_b2.columns.tolist()] + df_b2.values.tolist()
        expected_b2 = [["Collection", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                       ["hm-lawton", 2, 50, 0, 0, 50]]
        self.assertEqual(result_b2, expected_b2, "Problem with BMAC Collection Risk Levels")

        # Tests if the BMAC AIP Risk Levels sheet has the expected values.
        result_b3 = [df_b3.columns.tolist()] + df_b3.values.tolist()
        expected_b3 = [["AIP", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                       ["bmac_hm-lawton_0001", 1, 0, 0, 0, 100],
                       ["bmac_hm-lawton_0002", 1, 100, 0, 0, 0]]
        self.assertEqual(result_b3, expected_b3, "Problem with BMAC AIP Risk Levels")

        # Tests if the BMAC Formats sheet has the expected values.
        result_b4 = [df_b4.columns.tolist()] + df_b4.values.tolist()
        expected_b4 = [["Unnamed: 0", "Unnamed: 1", "Format Name", "Unnamed: 3"],
                       [np.NaN, "NARA_Risk Level", "No Match", "Low Risk"],
                       [np.NaN, "Format", "cue (No Match)", "Wave (Low Risk)"],
                       ["Collection", "AIP", np.NaN, np.NaN],
                       ["hm-lawton", "bmac_hm-lawton_0001", False, True],
                       [np.NaN, "bmac_hm-lawton_0002", True, False]]

        self.assertEqual(result_b4, expected_b4, "Problem with BMAC Formats")

        # Tests if the Hargrett AIP Risk Data sheet has the expected values.
        result_h1 = [df_h1.columns.tolist()] + df_h1.values.tolist()
        expected_h1 = [["Group", "Collection", "AIP", "Format Name", "Format Version", "PRONOM URL",
                        "NARA_Risk Level", "NARA_Proposed Preservation Plan"],
                       ["hargrett", "harg-0000", "harg-0000-web-202007-0001", "WARC", "NO VALUE",
                        "https://www.nationalarchives.gov.uk/PRONOM/fmt/289", "Low Risk", "Retain"],
                       ["hargrett", "harg-0000", "harg-0000-web-202007-0002", "WARC", "NO VALUE",
                        "https://www.nationalarchives.gov.uk/PRONOM/fmt/289", "Low Risk", "Retain"],
                       ["hargrett", "harg-ms3786", "harg-ms3786er0001", "JPEG File Interchange Format", "1.01",
                        "https://www.nationalarchives.gov.uk/PRONOM/fmt/43", "Low Risk", "Retain"],
                       ["hargrett", "harg-ms3786", "harg-ms3786er0002", "CorelDraw Drawing", "8.0",
                        "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/292", "High Risk",
                        "Transform to a TBD format, possibly PDF or TIFF"],
                       ["hargrett", "harg-ms3786", "harg-ms3786er0002", "JPEG File Interchange Format", "1.01",
                        "https://www.nationalarchives.gov.uk/PRONOM/fmt/43", "Low Risk", "Retain"],
                       ["hargrett", "harg-ms3786", "harg-ms3786er0003", "WARC", "NO VALUE",
                        "https://www.nationalarchives.gov.uk/PRONOM/fmt/289", "Low Risk", "Retain"],
                       ["hargrett", "harg-ms3786", "harg-ms3786er0003", "WARC", "NO VALUE", "NO VALUE",
                        "Low Risk", "Retain"]]
        self.assertEqual(result_h1, expected_h1, "Problem with Hargrett AIP Risk Data")

        # Tests if the Hargrett Collection Risk Levels sheet has the expected values.
        result_h2 = [df_h2.columns.tolist()] + df_h2.values.tolist()
        expected_h2 = [["Collection", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                       ["harg-0000", 1, 0, 0, 0, 100], ["harg-ms3786", 3, 0, 33.33, 0, 66.67]]
        self.assertEqual(result_h2, expected_h2, "Problem with Hargrett Collection Risk Levels")

        # Tests if the Hargrett AIP Risk Levels sheet has the expected values.
        result_h3 = [df_h3.columns.tolist()] + df_h3.values.tolist()
        expected_h3 = [["AIP", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                       ["harg-0000-web-202007-0001", 1, 0, 0, 0, 100],
                       ["harg-0000-web-202007-0002", 1, 0, 0, 0, 100],
                       ["harg-ms3786er0001", 1, 0, 0, 0, 100],
                       ["harg-ms3786er0002", 2, 0, 50, 0, 50],
                       ["harg-ms3786er0003", 2, 0, 0, 0, 100]]
        self.assertEqual(result_h3, expected_h3, "Problem with Hargrett AIP Risk Levels")

        # Tests if the Hargrett Formats sheet has the expected values.
        result_h4 = [df_h4.columns.tolist()] + df_h4.values.tolist()
        expected_h4 = [["Unnamed: 0", "Unnamed: 1", "Format Name", "Unnamed: 3", "Unnamed: 4"],
                       [np.NaN, "NARA_Risk Level", "High Risk", "Low Risk", np.NaN],
                       [np.NaN, "Format", "CorelDraw Drawing 8.0 (High Risk)",
                        "JPEG File Interchange Format 1.01 (Low Risk)", "WARC (Low Risk)"],
                       ["Collection", "AIP", np.NaN, np.NaN, np.NaN],
                       ["harg-0000", "harg-0000-web-202007-0001", False, False, True],
                       [np.NaN, "harg-0000-web-202007-0002", False, False, True],
                       ["harg-ms3786", "harg-ms3786er0001", False, True, False],
                       [np.NaN, "harg-ms3786er0002", True, True, False],
                       [np.NaN, "harg-ms3786er0003", False, False, True]]
        self.assertEqual(result_h4, expected_h4, "Problem with Hargrett Formats")


if __name__ == '__main__':
    unittest.main()
