"""
Tests the entire script merge_format_reports.py,
which combines ARCHive group format reports and data in standardize_formats.csv
to make a spreadsheet organized by group/format and another organized by AIP/format.

For input, tests use format reports that are in the merge_format_reports folder of this script repo.
"""

import csv
import datetime
import os
import subprocess
import unittest


def csv_to_list(csv_path):
    """
    Converts the information in a CSV to a list, where item is a list with one row's contents.
    Used to compare the script output to expected results.
    """
    with open(csv_path, newline="") as open_csv:
        read_csv = csv.reader(open_csv)
        row_list = list(read_csv)
    return row_list


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """
        Variables with constant values used in all of the tests.
        Today's date is used for naming the script outputs.
        """
        self.script_path = os.path.join("..", "..", "merge_format_reports.py")
        self.nara_csv = "NARA_PreservationActionPlan_FileFormats_test.csv"
        self.today = datetime.datetime.now().strftime("%Y-%m")

    def tearDown(self):
        """
        Deletes the CSVs produced by the script, if it is made by the test.
        """
        file_paths = [os.path.join("reports_one", f"archive_formats_by_aip_{self.today}.csv"),
                      os.path.join("reports_one", f"archive_formats_by_group_{self.today}.csv"),
                      os.path.join("reports_three", f"archive_formats_by_aip_{self.today}.csv"),
                      os.path.join("reports_three", f"archive_formats_by_group_{self.today}.csv")]
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_argument_error(self):
        """
        Test for running the script without the second required argument.
        It will print a message and exit the script.
        """
        # Tests that the script exits due to the error.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {self.script_path} reports_one", shell=True, check=True)

        # Tests if the expected message was produced. In production, this is printed to the terminal.
        # Must run the script a second time because cannot capture output within self.assertRaises.
        output = subprocess.run(f"python {self.script_path} reports_one", shell=True, stdout=subprocess.PIPE)
        msg_result = output.stdout.decode("utf-8")
        msg_expected = "Required argument nara_csv is missing\r\n" \
                       "Script usage: python path/merge_format_reports.py report_folder nara_csv\r\n"
        self.assertEqual(msg_result, msg_expected, "Problem with test for error argument, message")

    def test_one_report(self):
        """
        Test for a report_folder that only contains one ARCHive format report.
        Also contains a usage report.
        """
        # Runs the script.
        subprocess.run(f"python {self.script_path} reports_one {self.nara_csv}", shell=True)

        # Tests if archive_formats_by_aip.csv has the expected values.
        result = csv_to_list(os.path.join("reports_one", f"archive_formats_by_aip_{self.today}.csv"))
        expected = [["Group", "Collection", "AIP", "Format_Type", "Format_Standardized_Name", "Format_Identification",
                     "Format_Name", "Format_Version", "Registry_Name", "Registry_Key", "Format_Note",
                     "NARA_Format_Name", "NARA_PRONOM_URL", "NARA_Risk_Level", "NARA_Proposed_Preservation_Plan",
                     "NARA_Match_Type"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0001", "image", "JPEG",
                     "JPEG File Interchange Format|1.02|fmt/44", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/44", "NO VALUE", 
                     "JPEG File Interchange Format 1.02", "https://www.nationalarchives.gov.uk/pronom/fmt/44",
                     "Low Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0002", "image", "JPEG",
                     "JPEG File Interchange Format|1.02|fmt/44", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/44", "NO VALUE", 
                     "JPEG File Interchange Format 1.02", "https://www.nationalarchives.gov.uk/pronom/fmt/44",
                     "Low Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0001", "image", "JPEG",
                     "JPEG File Interchange Format|1.01|fmt/43", "JPEG File Interchange Format", "1.01",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/43", "NO VALUE",
                     "JPEG File Interchange Format 1.01", "https://www.nationalarchives.gov.uk/pronom/fmt/43",
                     "Low Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0004", "image", "JPEG",
                     "JPEG File Interchange Format|1.01|fmt/43", "JPEG File Interchange Format", "1.01",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/43", "NO VALUE",
                     "JPEG File Interchange Format 1.01", "https://www.nationalarchives.gov.uk/pronom/fmt/43",
                     "Low Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0005", "image", "JPEG",
                     "JPEG File Interchange Format|1.01|fmt/43", "JPEG File Interchange Format", "1.01",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/43", "NO VALUE",
                     "JPEG File Interchange Format 1.01", "https://www.nationalarchives.gov.uk/pronom/fmt/43",
                     "Low Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "harg-ms3770", "harg-ms3770er0002", "text", "Microsoft Word",
                     "Microsoft Word Binary File Format|97-2003|fmt/40", "Microsoft Word Binary File Format",
                     "97-2003", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/40", "For testing",
                     "Microsoft Word for Windows 97-2003", "https://www.nationalarchives.gov.uk/pronom/fmt/40",
                     "Moderate Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0001", "text", "Microsoft Word",
                     "Microsoft Word Binary File Format|97-2003|fmt/40", "Microsoft Word Binary File Format",
                     "97-2003", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/40", "For testing",
                     "Microsoft Word for Windows 97-2003", "https://www.nationalarchives.gov.uk/pronom/fmt/40",
                     "Moderate Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "harg-ms3770", "harg-ms3770er0002", "text", "Plain Text File",
                     "Plain text|NO VALUE|NO VALUE", "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE",
                     "Plain Text", "https://www.nationalarchives.gov.uk/pronom/x-fmt/111", "Low Risk", "Retain",
                     "Format Name"]]
        self.assertEqual(result, expected, "Problem with one report, archive_formats_by_aip.csv")

        # Tests if archive_formats_by_group.csv has the expected values.
        result = csv_to_list(os.path.join("reports_one", f"archive_formats_by_group_{self.today}.csv"))
        expected = [["Group", "File_IDs", "Size_GB", "Format_Type", "Format_Standardized_Name",
                     "Format_Identification", "Format_Name", "Format_Version", "Registry_Name", "Registry_Key",
                     "Format_Note", "NARA_Format_Name", "NARA_PRONOM_URL", "NARA_Risk_Level",
                     "NARA_Proposed_Preservation_Plan", "NARA_Match_Type"],
                    ["hargrett", "1474", "2.001", "image", "JPEG", "JPEG File Interchange Format|1.02|fmt/44",
                     "JPEG File Interchange Format", "1.02", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/44", "NO VALUE", "JPEG File Interchange Format 1.02",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/44", "Low Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "1322", "0.687", "image", "JPEG", "JPEG File Interchange Format|1.01|fmt/43",
                     "JPEG File Interchange Format", "1.01", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/43", "NO VALUE", "JPEG File Interchange Format 1.01",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/43", "Low Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "55", "0.005", "text", "Microsoft Word",
                     "Microsoft Word Binary File Format|97-2003|fmt/40", "Microsoft Word Binary File Format",
                     "97-2003", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/40", "For testing",
                     "Microsoft Word for Windows 97-2003", "https://www.nationalarchives.gov.uk/pronom/fmt/40",
                     "Moderate Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "48", "0.001", "text", "Plain Text File", "Plain text|NO VALUE|NO VALUE",
                     "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE", "Plain Text",
                     "https://www.nationalarchives.gov.uk/pronom/x-fmt/111", "Low Risk", "Retain", "Format Name"]]
        self.assertEqual(result, expected, "Problem with one report, archive_formats_by_group.csv")

    def test_three_reports(self):
        """
        Test for a report_folder that contains three ARCHive format reports.
        Also contains a usage report.
        """
        # Runs the script.
        subprocess.run(f"python {self.script_path} reports_three {self.nara_csv}", shell=True)

        # Tests if archive_formats_by_aip.csv has the expected values.
        result = csv_to_list(os.path.join("reports_three", f"archive_formats_by_aip_{self.today}.csv"))
        expected = [["Group", "Collection", "AIP", "Format_Type", "Format_Standardized_Name", "Format_Identification",
                     "Format_Name", "Format_Version", "Registry_Name", "Registry_Key", "Format_Note",
                     "NARA_Format_Name", "NARA_PRONOM_URL", "NARA_Risk_Level", "NARA_Proposed_Preservation_Plan",
                     "NARA_Match_Type"],
                    ["dlg", "arl_awc", "arl_awc_awc171", "image", "JPEG", "JPEG File Interchange Format|1.01|fmt/43",
                     "JPEG File Interchange Format", "1.01", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/43", "NO VALUE",
                     "JPEG File Interchange Format 1.01", "https://www.nationalarchives.gov.uk/pronom/fmt/43",
                     "Low Risk", "Retain", "PRONOM and Version"],
                    ["dlg", "arl_awc", "arl_awc_awc171", "image", "JPEG", "JPEG File Interchange Format|1.02|fmt/44",
                     "JPEG File Interchange Format", "1.02", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/44", "NO VALUE", "JPEG File Interchange Format 1.02",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/44", "Low Risk", "Retain", "PRONOM and Version"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20018", "image", "JPEG", "JPEG File Interchange Format|1.02|fmt/44",
                     "JPEG File Interchange Format", "1.02", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/44", "NO VALUE", "JPEG File Interchange Format 1.02",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/44", "Low Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0001", "image", "JPEG",
                     "JPEG File Interchange Format|1.02|fmt/44", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/44", "NO VALUE",
                     "JPEG File Interchange Format 1.02", "https://www.nationalarchives.gov.uk/pronom/fmt/44",
                     "Low Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0002", "image", "JPEG",
                     "JPEG File Interchange Format|1.02|fmt/44", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/44", "NO VALUE",
                     "JPEG File Interchange Format 1.02", "https://www.nationalarchives.gov.uk/pronom/fmt/44",
                     "Low Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "harg-ms3770", "harg-ms3770er0002", "text", "Plain Text File",
                     "Plain text|NO VALUE|NO VALUE", "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE",
                     "Plain Text", "https://www.nationalarchives.gov.uk/pronom/x-fmt/111", "Low Risk", "Retain",
                     "Format Name"],
                    ["bmac", "wtoc", "bmac_wtoc_8984", "video", "Quicktime", "QuickTime|NO VALUE|NO VALUE", "QuickTime",
                     "NO VALUE", "NO VALUE", "NO VALUE", "File is encoded in the following wrapper:ProRes 422 HQ",
                     "No Match", "", "No Match", "", "No NARA Match"],
                    ["bmac", "hm-lawton", "bmac_hm-lawton_0021", "application", "Cue Sheet",
                     "cue|NO VALUE|NO VALUE", "cue", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE", "No Match", "",
                     "No Match", "", "No NARA Match"],
                    ["bmac", "hm-lawton", "bmac_hm-lawton_0022", "application", "Cue Sheet",
                     "cue|NO VALUE|NO VALUE", "cue", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE", "No Match", "",
                     "No Match", "", "No NARA Match"]]
        self.assertEqual(result, expected, "Problem with three reports, archive_formats_by_aip.csv")

        # Tests if archive_formats_by_group.csv has the expected values.
        result = csv_to_list(os.path.join("reports_three", f"archive_formats_by_group_{self.today}.csv"))
        expected = [["Group", "File_IDs", "Size_GB", "Format_Type", "Format_Standardized_Name",
                     "Format_Identification", "Format_Name", "Format_Version", "Registry_Name", "Registry_Key",
                     "Format_Note", "NARA_Format_Name", "NARA_PRONOM_URL", "NARA_Risk_Level",
                     "NARA_Proposed_Preservation_Plan", "NARA_Match_Type"],
                    ["dlg", "1", "0.001", "image", "JPEG", "JPEG File Interchange Format|1.01|fmt/43",
                     "JPEG File Interchange Format", "1.01", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/43", "NO VALUE",
                     "JPEG File Interchange Format 1.01", "https://www.nationalarchives.gov.uk/pronom/fmt/43",
                     "Low Risk", "Retain", "PRONOM and Version"],
                    ["dlg", "33", "0.025", "image", "JPEG", "JPEG File Interchange Format|1.02|fmt/44",
                     "JPEG File Interchange Format", "1.02", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/44", "NO VALUE", "JPEG File Interchange Format 1.02",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/44", "Low Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "1474", "2.001", "image", "JPEG", "JPEG File Interchange Format|1.02|fmt/44",
                     "JPEG File Interchange Format", "1.02", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/44", "NO VALUE", "JPEG File Interchange Format 1.02",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/44", "Low Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", "48", "0.001", "text", "Plain Text File", "Plain text|NO VALUE|NO VALUE",
                     "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE", "Plain Text",
                     "https://www.nationalarchives.gov.uk/pronom/x-fmt/111", "Low Risk", "Retain", "Format Name"],
                    ["bmac", "836", "17005.995", "video", "Quicktime", "QuickTime|NO VALUE|NO VALUE", "QuickTime",
                     "NO VALUE", "NO VALUE", "NO VALUE", "File is encoded in the following wrapper:ProRes 422 HQ",
                     "No Match", "", "No Match", "", "No NARA Match"],
                    ["bmac", "26", "0.005", "application", "Cue Sheet", "cue|NO VALUE|NO VALUE", "cue",
                     "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE", "No Match", "", "No Match", "",
                     "No NARA Match"]]
        self.assertEqual(result, expected, "Problem with three reports, archive_formats_by_group.csv")


if __name__ == '__main__':
    unittest.main()
