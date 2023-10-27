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
        msg_expected = "Required argument current_formats_csv is missing\r\n" \
                       "Required argument previous_formats_csv is missing\r\n" \
                       "Script usage: python path/department_reports.py current_formats_csv previous_formats_csv\r\n"
        self.assertEqual(msg_result, msg_expected, "Problem with test for error argument, message")

    def test_correct_input(self):
        """
        Test for running the script on a valid archive_formats_by_aip CSV.
        """
        # Runs the script.
        script_path = os.path.join("..", "..", "department_reports.py")
        formats_current = os.path.join("script", "archive_formats_by_aip_2023-09.csv")
        formats_previous = "archive_formats_by_aip_2021-08.csv"
        subprocess.run(f"python {script_path} {formats_current} {formats_previous}")

        # # Reads the BMAC Excel file into pandas, and then each sheet into a separate dataframe.
        date = datetime.date.today().strftime("%Y%m")
        bmac = pd.ExcelFile(os.path.join("script", f"bmac_risk_report_{date}.xlsx"))
        df_bmac_data = pd.read_excel(bmac, "AIP Risk Data")
        df_bmac_dept = pd.read_excel(bmac, "Department Risk Levels")
        df_bmac_coll = pd.read_excel(bmac, "Collection Risk Levels")
        df_bmac_aip = pd.read_excel(bmac, "AIP Risk Levels")
        df_bmac_format = pd.read_excel(bmac, "Formats")
        bmac.close()

        # Reads the Hargrett Excel file into pandas, and then each sheet into a separate dataframe.
        hargrett = pd.ExcelFile(os.path.join("script", f"hargrett_risk_report_{date}.xlsx"))
        df_harg_data = pd.read_excel(hargrett, "AIP Risk Data")
        df_harg_dept = pd.read_excel(hargrett, "Department Risk Levels")
        df_harg_coll = pd.read_excel(hargrett, "Collection Risk Levels")
        df_harg_aip = pd.read_excel(hargrett, "AIP Risk Levels")
        df_harg_format = pd.read_excel(hargrett, "Formats")
        hargrett.close()

        # Tests if the BMAC AIP Risk Data sheet has the expected values.
        result_bmac_data = [df_bmac_data.columns.tolist()] + df_bmac_data.values.tolist()
        expected_bmac_data = [["Group", "Collection", "AIP", "Format_Name", "Format_Version", "PRONOM_URL",
                               "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan",
                               "2021_NARA_Risk_Level", "Risk_Level_Change"],
                              ["bmac", "hm-lawton", "bmac_hm-lawton_0001", "Wave", "NO VALUE", "NO VALUE",
                               "Low Risk", "Retain", "Low Risk", "Unchanged"],
                              ["bmac", "hm-lawton", "bmac_hm-lawton_0002", "cue", "NO VALUE", "NO VALUE",
                               "No Match", "NO VALUE", "No Match", "Unchanged"]]
        self.assertEqual(result_bmac_data, expected_bmac_data, "Problem with BMAC AIP Risk Data")

        # Tests if the BMAC Department Risk Levels sheet has the expected values.
        result_bmac_dept = [df_bmac_dept.columns.tolist()] + df_bmac_dept.values.tolist()
        expected_bmac_dept = [["Group", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                              ["bmac", 2, 50, 0, 0, 50]]
        self.assertEqual(result_bmac_dept, expected_bmac_dept, "Problem with BMAC Department Risk Levels")

        # Tests if the BMAC Collection Risk Levels sheet has the expected values.
        result_bmac_coll = [df_bmac_coll.columns.tolist()] + df_bmac_coll.values.tolist()
        expected_bmac_coll = [["Collection", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                              ["hm-lawton", 2, 50, 0, 0, 50]]
        self.assertEqual(result_bmac_coll, expected_bmac_coll, "Problem with BMAC Collection Risk Levels")

        # Tests if the BMAC AIP Risk Levels sheet has the expected values.
        result_bmac_aip = [df_bmac_aip.columns.tolist()] + df_bmac_aip.values.tolist()
        expected_bmac_aip = [["AIP", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                             ["bmac_hm-lawton_0001", 1, 0, 0, 0, 100],
                             ["bmac_hm-lawton_0002", 1, 100, 0, 0, 0]]
        self.assertEqual(result_bmac_aip, expected_bmac_aip, "Problem with BMAC AIP Risk Levels")

        # Tests if the BMAC Formats sheet has the expected values.
        result_bmac_format = [df_bmac_format.columns.tolist()] + df_bmac_format.values.tolist()
        expected_bmac_format = [["Unnamed: 0", "Unnamed: 1", "Format_Name", "Unnamed: 3"],
                                [np.NaN, "2023_NARA_Risk_Level", "No Match", "Low Risk"],
                                [np.NaN, "Format", "cue (No Match)", "Wave (Low Risk)"],
                                ["Collection", "AIP", np.NaN, np.NaN],
                                ["hm-lawton", "bmac_hm-lawton_0001", False, True],
                                [np.NaN, "bmac_hm-lawton_0002", True, False]]
        self.assertEqual(result_bmac_format, expected_bmac_format, "Problem with BMAC Formats")

        # Tests if the Hargrett AIP Risk Data sheet has the expected values.
        result_harg_data = [df_harg_data.columns.tolist()] + df_harg_data.values.tolist()
        expected_harg_data = [["Group", "Collection", "AIP", "Format_Name", "Format_Version", "PRONOM_URL",
                               "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan",
                               "2021_NARA_Risk_Level", "Risk_Level_Change"],
                              ["hargrett", "harg-0000", "harg-0000-web-202007-0001", "WARC", "NO VALUE",
                               "https://www.nationalarchives.gov.uk/PRONOM/fmt/289", "Low Risk", "Retain",
                               "Low Risk", "Unchanged"],
                              ["hargrett", "harg-0000", "harg-0000-web-202007-0002", "WARC", "NO VALUE",
                               "https://www.nationalarchives.gov.uk/PRONOM/fmt/289", "Low Risk", "Retain",
                               "Low Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0001", "JPEG File Interchange Format",
                               "1.01", "https://www.nationalarchives.gov.uk/PRONOM/fmt/43", "Low Risk",
                               "Retain", "Low Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0002", "CorelDraw Drawing", "8.0",
                               "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/292", "High Risk",
                               "Transform to a TBD format, possibly PDF or TIFF", "High Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0002", "JPEG File Interchange Format",
                               "1.01", "https://www.nationalarchives.gov.uk/PRONOM/fmt/43", "Low Risk",
                               "Retain", "Low Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0003", "WARC", "NO VALUE",
                               "https://www.nationalarchives.gov.uk/PRONOM/fmt/289", "Low Risk", "Retain",
                               "Low Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0003", "WARC", "NO VALUE", "NO VALUE",
                               "Low Risk", "Retain", "Low Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0004", "CorelDraw Drawing", "8.0",
                               "NO VALUE", "High Risk", "Transform to a TBD format, possibly PDF or TIFF",
                               "High Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0004", "CorelDraw Drawing", "8.0",
                               "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/292", "High Risk",
                               "Transform to a TBD format, possibly PDF or TIFF", "High Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0005", "CorelDraw Drawing", "8.0",
                               "NO VALUE", "High Risk", "Transform to a TBD format, possibly PDF or TIFF",
                               "High Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0005", "CorelDraw Drawing", "8.0",
                               "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/292", "High Risk",
                               "Transform to a TBD format, possibly PDF or TIFF", "High Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0005", "JPEG File Interchange Format",
                               "1.01", "https://www.nationalarchives.gov.uk/PRONOM/fmt/43", "Low Risk",
                               "Retain", "Low Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0005", "JPEG File Interchange Format",
                               "1.01", "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0006", "CorelDraw Drawing", "8.0",
                               "NO VALUE", "High Risk", "Transform to a TBD format, possibly PDF or TIFF",
                               "High Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0006", "CorelDraw Drawing", "8.0",
                               "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/292", "High Risk",
                               "Transform to a TBD format, possibly PDF or TIFF", "High Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0006", "cue", "NO VALUE", "NO VALUE",
                               "No Match", "NO VALUE", "No Match", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0006", "JPEG File Interchange Format",
                               "1.01", "https://www.nationalarchives.gov.uk/PRONOM/fmt/43", "Low Risk", "Retain",
                               "Low Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0006", "JPEG File Interchange Format",
                               "1.01", "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"]]
        self.assertEqual(result_harg_data, expected_harg_data, "Problem with Hargrett AIP Risk Data")

        # Tests if the Hargrett Department Risk Levels sheet has the expected values.
        result_harg_dept = [df_harg_dept.columns.tolist()] + df_harg_dept.values.tolist()
        expected_harg_dept = [["Group", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                              ["hargrett", 4, 25, 25, 0, 50]]
        self.assertEqual(result_harg_dept, expected_harg_dept, "Problem with Hargrett Department Risk Levels")

        # Tests if the Hargrett Collection Risk Levels sheet has the expected values.
        result_harg_coll = [df_harg_coll.columns.tolist()] + df_harg_coll.values.tolist()
        expected_harg_coll = [["Collection", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                              ["harg-0000", 1, 0, 0, 0, 100],
                              ["harg-ms3786", 4, 25, 25, 0, 50]]
        self.assertEqual(result_harg_coll, expected_harg_coll, "Problem with Hargrett Collection Risk Levels")

        # Tests if the Hargrett AIP Risk Levels sheet has the expected values.
        result_harg_aip = [df_harg_aip.columns.tolist()] + df_harg_aip.values.tolist()
        expected_harg_aip = [["AIP", "Formats", "No Match %", "High Risk %", "Moderate Risk %", "Low Risk %"],
                             ["harg-0000-web-202007-0001", 1, 0.0, 0.0, 0, 100.0],
                             ["harg-0000-web-202007-0002", 1, 0.0, 0.0, 0, 100.0],
                             ["harg-ms3786er0001", 1, 0.0, 0.0, 0, 100.0],
                             ["harg-ms3786er0002", 2, 0.0, 50.0, 0, 50.0],
                             ["harg-ms3786er0003", 1, 0.0, 0.0, 0, 100.0],
                             ["harg-ms3786er0004", 1, 0.0, 100.0, 0, 0.0],
                             ["harg-ms3786er0005", 2, 0.0, 50.0, 0, 50.0],
                             ["harg-ms3786er0006", 3, 33.33, 33.33, 0, 33.33]]
        self.assertEqual(result_harg_aip, expected_harg_aip, "Problem with Hargrett AIP Risk Levels")

        # Tests if the Hargrett Formats sheet has the expected values.
        result_harg_format = [df_harg_format.columns.tolist()] + df_harg_format.values.tolist()
        expected_harg_format = [["Unnamed: 0", "Unnamed: 1", "Format_Name", "Unnamed: 3", "Unnamed: 4", "Unnamed: 5"],
                                [np.NaN, "2023_NARA_Risk_Level", "No Match", "High Risk", "Low Risk", np.NaN],
                                [np.NaN, "Format", "cue (No Match)", "CorelDraw Drawing 8.0 (High Risk)",
                                 "JPEG File Interchange Format 1.01 (Low Risk)", "WARC (Low Risk)"],
                                ["Collection", "AIP", np.NaN, np.NaN, np.NaN, np.NaN],
                                ["harg-0000", "harg-0000-web-202007-0001", False, False, False, True],
                                [np.NaN, "harg-0000-web-202007-0002", False, False, False, True],
                                ["harg-ms3786", "harg-ms3786er0001", False, False, True, False],
                                [np.NaN, "harg-ms3786er0002", False, True, True, False],
                                [np.NaN, "harg-ms3786er0003", False, False, False, True],
                                [np.NaN, "harg-ms3786er0004", False, True, False, False],
                                [np.NaN, "harg-ms3786er0005", False, True, True, False],
                                [np.NaN, "harg-ms3786er0006", True, True, True, False]]
        self.assertEqual(result_harg_format, expected_harg_format, "Problem with Hargrett Formats")


if __name__ == '__main__':
    unittest.main()
