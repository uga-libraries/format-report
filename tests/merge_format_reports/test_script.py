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
        Gets the current date, formatted YYYYMM, to use in naming the script outputs.
        """
        self.today = datetime.datetime.now().strftime("%Y-%m")

    def tearDown(self):
        """
        Deletes the CSVs produced by the script, if it is made by the test.
        """
        file_paths = [os.path.join("reports_one", f"archive_formats_{self.today}.csv"),
                      os.path.join("reports_one", f"archive_formats_by_aip_{self.today}.csv"),
                      os.path.join("reports_three", f"archive_formats_{self.today}.csv"),
                      os.path.join("reports_three", f"archive_formats_by_aip_{self.today}.csv")]
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_one_report(self):
        """
        Test for a report_folder that only contains one ARCHive format report.
        Also contains a usage report.
        """
        # Runs the script.
        script_path = os.path.join("..", "..", "merge_format_reports.py")
        subprocess.run(f"python {script_path} reports_one", shell=True)

        # Tests if archive_formats.csv has the expected values.
        result = csv_to_list(os.path.join("reports_one", f"archive_formats_{self.today}.csv"))
        expected = [["Group", "File_IDs", "Size (GB)", "Format Type", "Format Standardized Name",
                     "Format Identification", "Format Name", "Format Version", "Registry Name", "Registry Key",
                     "Format Note"],
                    ["hargrett", "1474", "2.001", "image", "JPEG", "JPEG File Interchange Format|1.02|fmt/44",
                     "JPEG File Interchange Format", "1.02", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/44", "NO VALUE"],
                    ["hargrett", "1322", "0.687", "image", "JPEG", "JPEG File Interchange Format|1.01|fmt/43",
                     "JPEG File Interchange Format", "1.01", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/43", "NO VALUE"],
                    ["hargrett", "55", "0.005", "text", "Microsoft Word",
                     "Microsoft Word Binary File Format|97-2003|fmt/40", "Microsoft Word Binary File Format",
                     "97-2003", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/40", "For testing"],
                    ["hargrett", "48", "0.001", "text", "Plain Text File", "Plain text|NO VALUE|NO VALUE",
                     "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE"]]
        self.assertEqual(result, expected, "Problem with one report, archive_formats.csv")

        # Tests if archive_formats_by_aip.csv has the expected values.
        result = csv_to_list(os.path.join("reports_one", f"archive_formats_by_aip_{self.today}.csv"))
        expected = [["Group", "Collection", "AIP", "Format Type", "Format Standardized Name", "Format Identification",
                     "Format Name", "Format Version", "Registry Name", "Registry Key", "Format Note"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0001", "image", "JPEG",
                     "JPEG File Interchange Format|1.02|fmt/44", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/44", "NO VALUE"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0002", "image", "JPEG",
                     "JPEG File Interchange Format|1.02|fmt/44", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/44", "NO VALUE"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0001", "image", "JPEG",
                     "JPEG File Interchange Format|1.01|fmt/43", "JPEG File Interchange Format", "1.01",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/43", "NO VALUE"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0004", "image", "JPEG",
                     "JPEG File Interchange Format|1.01|fmt/43", "JPEG File Interchange Format", "1.01",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/43", "NO VALUE"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0005", "image", "JPEG",
                     "JPEG File Interchange Format|1.01|fmt/43", "JPEG File Interchange Format", "1.01",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/43", "NO VALUE"],
                    ["hargrett", "harg-ms3770", "harg-ms3770er0002", "text", "Microsoft Word",
                     "Microsoft Word Binary File Format|97-2003|fmt/40", "Microsoft Word Binary File Format",
                     "97-2003", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/40", "For testing"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0001", "text", "Microsoft Word",
                     "Microsoft Word Binary File Format|97-2003|fmt/40", "Microsoft Word Binary File Format",
                     "97-2003", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/40", "For testing"],
                    ["hargrett", "harg-ms3770", "harg-ms3770er0002", "text", "Plain Text File",
                     "Plain text|NO VALUE|NO VALUE", "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE"]]
        self.assertEqual(result, expected, "Problem with one report, archive_formats_by_aip.csv")


    def test_three_reports(self):
        """
        Test for a report_folder that contains three ARCHive format reports.
        Also contains a usage report.
        """
        # Runs the script.
        script_path = os.path.join("..", "..", "merge_format_reports.py")
        subprocess.run(f"python {script_path} reports_three", shell=True)

        # Tests if archive_formats.csv has the expected values.
        result = csv_to_list(os.path.join("reports_three", f"archive_formats_{self.today}.csv"))
        expected = [["Group", "File_IDs", "Size (GB)", "Format Type", "Format Standardized Name",
                     "Format Identification", "Format Name", "Format Version", "Registry Name", "Registry Key",
                     "Format Note"],
                    ["bmac", "836", "17005.995", "video", "Quicktime", "QuickTime|NO VALUE|NO VALUE", "QuickTime",
                     "NO VALUE", "NO VALUE", "NO VALUE", "File is encoded in the following wrapper:ProRes 422 HQ"],
                    ["bmac", "26", "0.005", "application", "Cue Sheet", "cue|NO VALUE|NO VALUE", "cue",
                     "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE"],
                    ["dlg", "1", "0.001", "image", "JPEG", "JPEG File Interchange Format|1.01|fmt/43",
                     "JPEG File Interchange Format", "1.01", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/43", "NO VALUE"],
                    ["dlg", "33", "0.025", "image", "JPEG", "JPEG File Interchange Format|1.02|fmt/44",
                     "JPEG File Interchange Format", "1.02", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/44", "NO VALUE"],
                    ["hargrett", "1474", "2.001", "image", "JPEG", "JPEG File Interchange Format|1.02|fmt/44",
                     "JPEG File Interchange Format", "1.02", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/44", "NO VALUE"],
                    ["hargrett", "48", "0.001", "text", "Plain Text File", "Plain text|NO VALUE|NO VALUE",
                     "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE"]]
        self.assertEqual(result, expected, "Problem with three reports, archive_formats.csv")

        # Tests if archive_formats_by_aip.csv has the expected values.
        result = csv_to_list(os.path.join("reports_three", f"archive_formats_by_aip_{self.today}.csv"))
        expected = [["Group", "Collection", "AIP", "Format Type", "Format Standardized Name", "Format Identification",
                     "Format Name", "Format Version", "Registry Name", "Registry Key", "Format Note"],
                    ["bmac", "wtoc", "bmac_wtoc_8984", "video", "Quicktime", "QuickTime|NO VALUE|NO VALUE", "QuickTime",
                     "NO VALUE", "NO VALUE", "NO VALUE", "File is encoded in the following wrapper:ProRes 422 HQ"],
                    ["bmac", "hm-lawton", "bmac_hm-lawton_0021", "application", "Cue Sheet",
                     "cue|NO VALUE|NO VALUE", "cue", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE"],
                    ["bmac", "hm-lawton", "bmac_hm-lawton_0022", "application", "Cue Sheet",
                     "cue|NO VALUE|NO VALUE", "cue", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE"],
                    ["dlg", "arl_awc", "arl_awc_awc171", "image", "JPEG", "JPEG File Interchange Format|1.01|fmt/43",
                     "JPEG File Interchange Format", "1.01", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/43", "NO VALUE"],
                    ["dlg", "arl_awc", "arl_awc_awc171", "image", "JPEG", "JPEG File Interchange Format|1.02|fmt/44",
                     "JPEG File Interchange Format", "1.02", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/44", "NO VALUE"],
                    ["dlg", "dlg_ww2", "dlg_ww2_cws20018", "image", "JPEG", "JPEG File Interchange Format|1.02|fmt/44",
                     "JPEG File Interchange Format", "1.02", "https://www.nationalarchives.gov.uk/PRONOM",
                     "fmt/44", "NO VALUE"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0001", "image", "JPEG",
                     "JPEG File Interchange Format|1.02|fmt/44", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/44", "NO VALUE"],
                    ["hargrett", "harg-ms3786", "harg-ms3786er0002", "image", "JPEG",
                     "JPEG File Interchange Format|1.02|fmt/44", "JPEG File Interchange Format", "1.02",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/44", "NO VALUE"],
                    ["hargrett", "harg-ms3770", "harg-ms3770er0002", "text", "Plain Text File",
                     "Plain text|NO VALUE|NO VALUE", "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE"]]
        self.assertEqual(result, expected, "Problem with three reports, archive_formats_by_aip.csv")


if __name__ == '__main__':
    unittest.main()
