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
        file_paths = [os.path.join("script", f"dlg-magil_risk_report_{date}.xlsx"),
                      os.path.join("script", f"bmac_risk_report_{date}.xlsx"),
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

    def test_one_department(self):
        """
        Test for running the script on valid archive_formats_by_aip CSVs with one department.
        """
        # Runs the script.
        script_path = os.path.join("..", "..", "department_reports.py")
        formats_current = os.path.join("script", "archive_formats_by_aip_2023-11.csv")
        formats_previous = os.path.join("script", "archive_formats_by_aip_2021-11.csv")
        subprocess.run(f"python {script_path} {formats_current} {formats_previous}")

        # # Reads the DLG-MAGIL Excel file into pandas, and then each sheet into a separate dataframe.
        date = datetime.date.today().strftime("%Y%m")
        df = pd.ExcelFile(os.path.join("script", f"dlg-magil_risk_report_{date}.xlsx"))
        df_data = pd.read_excel(df, "AIP Risk Data")
        df_dept = pd.read_excel(df, "Department Risk Levels")
        df_coll = pd.read_excel(df, "Collection Risk Levels")
        df_aip = pd.read_excel(df, "AIP Risk Levels")
        df_format = pd.read_excel(df, "Formats")
        df.close()

        # Tests if the DLG-MAGIL AIP Risk Data sheet has the expected values.
        result_data = [df_data.columns.tolist()] + df_data.values.tolist()
        expected_data = [["Group", "Collection", "AIP", "Format_Name", "Format_Version", "PRONOM_URL",
                          "2023_NARA_Risk_Level", "2023_NARA_Proposed_Preservation_Plan",
                          "2021_NARA_Risk_Level", "Risk_Level_Change"],
                          ["dlg-magil", "dlg_sanb", "dlg_sanb_savannah-1884", "Tagged Image File Format", "6",
                           "NO VALUE", "Low Risk", "Retain", np.NaN, "New Format"],
                          ["dlg-magil", "dlg_sanb", "dlg_sanb_savannah-1888", "Tagged Image File Format", "6",
                           "NO VALUE", "Low Risk", "Retain", np.NaN, "New Format"],
                          ["dlg-magil", "gyca_gaphind", "gyca_gaphind_appling-1952", "Plain text", "NO VALUE",
                           "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/111", "Low Risk", "Retain",
                           "Low Risk", "Unchanged"],
                          ["dlg-magil", "gyca_gaphind", "gyca_gaphind_appling-1952",
                           "TIFF DLF Benchmark for Faithful Digital Reproductions of Monographs and Serials: color",
                           "5", "NO VALUE", "No Match", np.NaN, "No Match", "Unchanged"],
                          ["dlg-magil", "gyca_gaphind", "gyca_gaphind_appling-1962", "Plain text", "NO VALUE",
                           "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/111", "Low Risk", "Retain",
                           "Low Risk", "Unchanged"],
                          ["dlg-magil", "gyca_gaphind", "gyca_gaphind_appling-1962",
                           "TIFF DLF Benchmark for Faithful Digital Reproductions of Monographs and Serials: color",
                           "5", "NO VALUE", "No Match", np.NaN, "No Match", "Unchanged"],
                          ["dlg-magil", "gyca_gaphind", "gyca_gaphind_appling-1968", "Plain text", "NO VALUE",
                           "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/111", "Low Risk", "Retain",
                           "Low Risk", "Unchanged"],
                          ["dlg-magil", "gyca_gaphind", "gyca_gaphind_appling-1968",
                           "TIFF DLF Benchmark for Faithful Digital Reproductions of Monographs and Serials: color",
                           "5", "NO VALUE", "No Match", np.NaN, "No Match", "Unchanged"],
                          ["dlg-magil", "gyca_gaphind", "gyca_gaphind_atkinson-1939",
                           "TIFF DLF Benchmark for Faithful Digital Reproductions of Monographs and Serials: color",
                           "5", "NO VALUE", "No Match", np.NaN, "No Match", "Unchanged"],
                          ["dlg-magil", "gyca_gaphind", "gyca_gaphind_atkinson-1947",
                           "TIFF DLF Benchmark for Faithful Digital Reproductions of Monographs and Serials: color",
                           "5", "NO VALUE", "No Match", np.NaN, "No Match", "Unchanged"],
                          ["dlg-magil", "gyca_gaphind", "gyca_gaphind_bacon-1956-57",
                           "TIFF DLF Benchmark for Faithful Digital Reproductions of Monographs and Serials: color",
                           "5", "NO VALUE", "No Match", np.NaN, "No Match", "Unchanged"],
                          ["dlg-magil", "gyca_gaphind", "gyca_gaphind_bacon-1962-63", "Plain text", "NO VALUE",
                           "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/111", "Low Risk", "Retain",
                           "Low Risk", "Unchanged"],
                          ["dlg-magil", "gyca_gaphind", "gyca_gaphind_bacon-1962-63",
                           "TIFF DLF Benchmark for Faithful Digital Reproductions of Monographs and Serials: color",
                           "5", "NO VALUE", "No Match", np.NaN, "No Match", "Unchanged"],
                          ["dlg-magil", "gyca_gaphind", "gyca_gaphind_bacon-1968", "Plain text", "NO VALUE",
                           "https://www.nationalarchives.gov.uk/PRONOM/x-fmt/111", "Low Risk", "Retain",
                           "Low Risk", "Unchanged"],
                          ["dlg-magil", "gyca_gaphind", "gyca_gaphind_bacon-1968",
                           "TIFF DLF Benchmark for Faithful Digital Reproductions of Monographs and Serials: color",
                           "5", "NO VALUE", "No Match", np.NaN, "No Match", "Unchanged"]]
        self.assertEqual(result_data, expected_data, "Problem with DLG-MAGIL AIP Risk Data")

        # Tests if the DLG-MAGIL Department Risk Levels sheet has the expected values.
        result_dept = [df_dept.columns.tolist()] + df_dept.values.tolist()
        expected_dept = [["Group", "Formats", "No_Match_%", "High_Risk_%", "Moderate_Risk_%", "Low_Risk_%"],
                         ["dlg-magil", 3, 33.33, 0, 0, 66.67]]
        self.assertEqual(result_dept, expected_dept, "Problem with DLG-MAGIL Department Risk Levels")

        # Tests if the DLG-MAGIL Collection Risk Levels sheet has the expected values.
        result_coll = [df_coll.columns.tolist()] + df_coll.values.tolist()
        expected_coll = [["Collection", "Formats", "No_Match_%", "High_Risk_%", "Moderate_Risk_%", "Low_Risk_%"],
                         ["dlg_sanb", 1, 0, 0, 0, 100],
                         ["gyca_gaphind", 2, 50, 0, 0, 50]]
        self.assertEqual(result_coll, expected_coll, "Problem with DLG-MAGIL Collection Risk Levels")

        # Tests if the DLG-MAGIL AIP Risk Levels sheet has the expected values.
        result_aip = [df_aip.columns.tolist()] + df_aip.values.tolist()
        expected_aip = [["AIP", "Formats", "No_Match_%", "High_Risk_%", "Moderate_Risk_%", "Low_Risk_%"],
                        ["dlg_sanb_savannah-1884", 1, 0, 0, 0, 100],
                        ["dlg_sanb_savannah-1888", 1, 0, 0, 0, 100],
                        ["gyca_gaphind_appling-1952", 2, 50, 0, 0, 50],
                        ["gyca_gaphind_appling-1962", 2, 50, 0, 0, 50],
                        ["gyca_gaphind_appling-1968", 2, 50, 0, 0, 50],
                        ["gyca_gaphind_atkinson-1939", 1, 100, 0, 0, 0],
                        ["gyca_gaphind_atkinson-1947", 1, 100, 0, 0, 0],
                        ["gyca_gaphind_bacon-1956-57", 1, 100, 0, 0, 0],
                        ["gyca_gaphind_bacon-1962-63", 2, 50, 0, 0, 50],
                        ["gyca_gaphind_bacon-1968", 2, 50, 0, 0, 50]]
        self.assertEqual(result_aip, expected_aip, "Problem with DLG-MAGIL AIP Risk Levels")

        # Tests if the DLG-MAGIL Formats sheet has the expected values.
        result_format = [df_format.columns.tolist()] + df_format.values.tolist()
        expected_format = [["Unnamed: 0", "Unnamed: 1", "Format_Name", "Unnamed: 3", "Unnamed: 4"],
                           [np.NaN, "2023_NARA_Risk_Level", "No Match", "Low Risk", np.NaN],
                           [np.NaN, "Format", "TIFF DLF Benchmark for Faithful Digital Reproductions of Monographs and Serials: color 5 (No Match)",
                            "Plain text (Low Risk)", "Tagged Image File Format 6 (Low Risk)"],
                           ["Collection", "AIP", np.NaN, np.NaN, np.NaN],
                           ["dlg_sanb", "dlg_sanb_savannah-1884", False, False, True],
                           [np.NaN, "dlg_sanb_savannah-1888", False, False, True],
                           ["gyca_gaphind", "gyca_gaphind_appling-1952", True, True, False],
                           [np.NaN, "gyca_gaphind_appling-1962", True, True, False],
                           [np.NaN, "gyca_gaphind_appling-1968", True, True, False],
                           [np.NaN, "gyca_gaphind_atkinson-1939", True, False, False],
                           [np.NaN, "gyca_gaphind_atkinson-1947", True, False, False],
                           [np.NaN, "gyca_gaphind_bacon-1956-57", True, False, False],
                           [np.NaN, "gyca_gaphind_bacon-1962-63", True, True, False],
                           [np.NaN, "gyca_gaphind_bacon-1968", True, True, False]]
        self.assertEqual(result_format, expected_format, "Problem with DLG-MAGIL Formats")

    def test_two_departments(self):
        """
        Test for running the script on valid archive_formats_by_aip CSVs with two departments.
        """
        # Runs the script.
        script_path = os.path.join("..", "..", "department_reports.py")
        formats_current = os.path.join("script", "archive_formats_by_aip_2023-09.csv")
        formats_previous = os.path.join("script", "archive_formats_by_aip_2021-08.csv")
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
                               "Moderate Risk", "Retain", "No Match", "New Match"]]
        self.assertEqual(result_bmac_data, expected_bmac_data, "Problem with BMAC AIP Risk Data")

        # Tests if the BMAC Department Risk Levels sheet has the expected values.
        result_bmac_dept = [df_bmac_dept.columns.tolist()] + df_bmac_dept.values.tolist()
        expected_bmac_dept = [["Group", "Formats", "No_Match_%", "High_Risk_%", "Moderate_Risk_%", "Low_Risk_%"],
                              ["bmac", 2, 0, 0, 50, 50]]
        self.assertEqual(result_bmac_dept, expected_bmac_dept, "Problem with BMAC Department Risk Levels")

        # Tests if the BMAC Collection Risk Levels sheet has the expected values.
        result_bmac_coll = [df_bmac_coll.columns.tolist()] + df_bmac_coll.values.tolist()
        expected_bmac_coll = [["Collection", "Formats", "No_Match_%", "High_Risk_%", "Moderate_Risk_%", "Low_Risk_%"],
                              ["hm-lawton", 2, 0, 0, 50, 50]]
        self.assertEqual(result_bmac_coll, expected_bmac_coll, "Problem with BMAC Collection Risk Levels")

        # Tests if the BMAC AIP Risk Levels sheet has the expected values.
        result_bmac_aip = [df_bmac_aip.columns.tolist()] + df_bmac_aip.values.tolist()
        expected_bmac_aip = [["AIP", "Formats", "No_Match_%", "High_Risk_%", "Moderate_Risk_%", "Low_Risk_%"],
                             ["bmac_hm-lawton_0001", 1, 0, 0, 0, 100],
                             ["bmac_hm-lawton_0002", 1, 0, 0, 100, 0]]
        self.assertEqual(result_bmac_aip, expected_bmac_aip, "Problem with BMAC AIP Risk Levels")

        # Tests if the BMAC Formats sheet has the expected values.
        result_bmac_format = [df_bmac_format.columns.tolist()] + df_bmac_format.values.tolist()
        expected_bmac_format = [["Unnamed: 0", "Unnamed: 1", "Format_Name", "Unnamed: 3"],
                                [np.NaN, "2023_NARA_Risk_Level", "Moderate Risk", "Low Risk"],
                                [np.NaN, "Format", "cue (Moderate Risk)", "Wave (Low Risk)"],
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
                               "https://www.nationalarchives.gov.uk/PRONOM/fmt/289", "Moderate Risk", "Retain",
                               "Low Risk", "Increase"],
                              ["hargrett", "harg-0000", "harg-0000-web-202007-0002", "WARC", "NO VALUE",
                               "https://www.nationalarchives.gov.uk/PRONOM/fmt/289", "Moderate Risk", "Retain",
                               "Low Risk", "Increase"],
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
                               "https://www.nationalarchives.gov.uk/PRONOM/fmt/289", "Moderate Risk", "Retain",
                               "Low Risk", "Increase"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0003", "WARC", "NO VALUE", "NO VALUE",
                               "Moderate Risk", "Retain", "Low Risk", "Increase"],
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
                               "No Match", np.NaN, "No Match", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0006", "JPEG File Interchange Format",
                               "1.01", "https://www.nationalarchives.gov.uk/PRONOM/fmt/43", "Low Risk", "Retain",
                               "Low Risk", "Unchanged"],
                              ["hargrett", "harg-ms3786", "harg-ms3786er0006", "JPEG File Interchange Format",
                               "1.01", "NO VALUE", "Low Risk", "Retain", "Low Risk", "Unchanged"]]
        self.assertEqual(result_harg_data, expected_harg_data, "Problem with Hargrett AIP Risk Data")

        # Tests if the Hargrett Department Risk Levels sheet has the expected values.
        result_harg_dept = [df_harg_dept.columns.tolist()] + df_harg_dept.values.tolist()
        expected_harg_dept = [["Group", "Formats", "No_Match_%", "High_Risk_%", "Moderate_Risk_%", "Low_Risk_%"],
                              ["hargrett", 4, 25, 25, 25, 25]]
        self.assertEqual(result_harg_dept, expected_harg_dept, "Problem with Hargrett Department Risk Levels")

        # Tests if the Hargrett Collection Risk Levels sheet has the expected values.
        result_harg_coll = [df_harg_coll.columns.tolist()] + df_harg_coll.values.tolist()
        expected_harg_coll = [["Collection", "Formats", "No_Match_%", "High_Risk_%", "Moderate_Risk_%", "Low_Risk_%"],
                              ["harg-0000", 1, 0, 0, 100, 0],
                              ["harg-ms3786", 4, 25, 25, 25, 25]]
        self.assertEqual(result_harg_coll, expected_harg_coll, "Problem with Hargrett Collection Risk Levels")

        # Tests if the Hargrett AIP Risk Levels sheet has the expected values.
        result_harg_aip = [df_harg_aip.columns.tolist()] + df_harg_aip.values.tolist()
        expected_harg_aip = [["AIP", "Formats", "No_Match_%", "High_Risk_%", "Moderate_Risk_%", "Low_Risk_%"],
                             ["harg-0000-web-202007-0001", 1, 0.0, 0.0, 100.0, 0.0],
                             ["harg-0000-web-202007-0002", 1, 0.0, 0.0, 100.0, 0.0],
                             ["harg-ms3786er0001", 1, 0.0, 0.0, 0, 100.0],
                             ["harg-ms3786er0002", 2, 0.0, 50.0, 0, 50.0],
                             ["harg-ms3786er0003", 1, 0.0, 0.0, 100.0, 0.0],
                             ["harg-ms3786er0004", 1, 0.0, 100.0, 0, 0.0],
                             ["harg-ms3786er0005", 2, 0.0, 50.0, 0, 50.0],
                             ["harg-ms3786er0006", 3, 33.33, 33.33, 0, 33.33]]
        self.assertEqual(result_harg_aip, expected_harg_aip, "Problem with Hargrett AIP Risk Levels")

        # Tests if the Hargrett Formats sheet has the expected values.
        result_harg_format = [df_harg_format.columns.tolist()] + df_harg_format.values.tolist()
        expected_harg_format = [["Unnamed: 0", "Unnamed: 1", "Format_Name", "Unnamed: 3", "Unnamed: 4", "Unnamed: 5"],
                                [np.NaN, "2023_NARA_Risk_Level", "No Match", "High Risk", "Moderate Risk", "Low Risk"],
                                [np.NaN, "Format", "cue (No Match)", "CorelDraw Drawing 8.0 (High Risk)",
                                 "WARC (Moderate Risk)", "JPEG File Interchange Format 1.01 (Low Risk)"],
                                ["Collection", "AIP", np.NaN, np.NaN, np.NaN, np.NaN],
                                ["harg-0000", "harg-0000-web-202007-0001", False, False, True, False],
                                [np.NaN, "harg-0000-web-202007-0002", False, False, True, False],
                                ["harg-ms3786", "harg-ms3786er0001", False, False, False, True],
                                [np.NaN, "harg-ms3786er0002", False, True, False, True],
                                [np.NaN, "harg-ms3786er0003", False, False, True, False],
                                [np.NaN, "harg-ms3786er0004", False, True, False, False],
                                [np.NaN, "harg-ms3786er0005", False, True, False, True],
                                [np.NaN, "harg-ms3786er0006", True, True, False, True]]
        self.assertEqual(result_harg_format, expected_harg_format, "Problem with Hargrett Formats")


if __name__ == '__main__':
    unittest.main()
