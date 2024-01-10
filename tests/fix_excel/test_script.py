"""
Tests the entire script fix_excel.py,
which fixes errors caused by opening the CSV in Excel.
"""

import numpy as np
import os
import pandas as pd
import shutil
import subprocess
import unittest


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """
        Deletes the updated CSVs produced by the test, if made.
        """
        paths = [os.path.join("script", "archive_formats_by_aip_2023-11.csv"),
                 os.path.join("script", "archive_formats_by_group_2023-11.csv")]
        for path in paths:
            if os.path.exists(path):
                os.remove(path)

    def test_argument_error(self):
        """
        Test for running the script with the required argument.
        It will print a message and exit the script.
        """
        script_path = os.path.join("..", "..", "fix_excel.py")

        # Tests that the script exits due to the error.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f"python {script_path}", shell=True, check=True)

        # Tests that the expected error message was produced. In production, this is printed to the terminal.
        # Run the script a second time because cannot capture output within self.assertRaises.
        output = subprocess.run(f"python {script_path}", shell=True, stdout=subprocess.PIPE)
        error_msg = output.stdout.decode("utf-8")
        expected_msg = "Required argument csv_path is missing\r\n"
        self.assertEqual(error_msg, expected_msg, "Problem with test for argument error, error message")

    def test_by_aip(self):
        """
        Test for running the script with correct input for a "by_aip" CSV.
        """
        # Makes a copy of the CSV for this test, since the test will edit the CSV.
        csv_original = os.path.join("script", "archive_formats_by_aip.csv")
        csv_test = os.path.join("script", "archive_formats_by_aip_2023-11.csv")
        shutil.copy(csv_original, csv_test)

        # Runs the script
        script_path = os.path.join("..", "..", "fix_excel.py")
        subprocess.run(f"python {script_path} {csv_test}", shell=True)

        # Tests that the updated test CSV has the expected values.
        df = pd.read_csv(csv_test)
        result = [df.columns.tolist()] + df.values.tolist()
        expected = [["Group", "Collection", "AIP", "Format_Type", "Format_Standardized_Name", "Format_Identification",
                     "Format_Name", "Format_Version", "Registry_Name", "Registry_Key", "Format_Note",
                     "NARA_Format_Name", "NARA_PRONOM_URL", "NARA_Risk_Level", "NARA_Proposed_Preservation_Plan",
                     "NARA_Match_Type"],
                    ["dlg", "aarl_afpc", "aarl_afpc_brownjuanita19850217", "text", "PDF",
                     "Portable Document Format|1.6|fmt/20", "Portable Document Format", "1.6",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/20", "NO VALUE",
                     "Portable Document Format (PDF) version 1.6", "https://www.nationalarchives.gov.uk/pronom/fmt/20",
                     "Moderate Risk", "Retain", "PRONOM and Version"],
                    ["dlg", "aarl_afpc", "aarl_afpc_culbreathbernice20010227", "structured_text", "XML",
                     "Extensible Markup Language|1.0|fmt/101", "Extensible Markup Language", "1.0",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/101", "NO VALUE",
                     "eXtensible Markup Language 1.0", "https://www.nationalarchives.gov.uk/pronom/fmt/101",
                     "Low Risk", "Retain", "PRONOM and Version"],
                    ["dlg", "arl_acl", "arl_acl_acl001", "image", "TIFF", "Tagged Image File Format|5.0|fmt/353",
                     "Tagged Image File Format", "5.0", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/353",
                     "NO VALUE", "Tagged Image File Format (TIFF) 1-6",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/353", "Low Risk", "Retain", "PRONOM"],
                    ["dlg", "arl_acl", "arl_acl_acl328", "image", "TIFF", "Tagged Image File Format|6.0|fmt/353",
                     "Tagged Image File Format", "6.0", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/353",
                     "NO VALUE", "Tagged Image File Format (TIFF) 1-6",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/353", "Low Risk", "Retain", "PRONOM"],
                    ["dlg", "arl_acl", "arl_acl_acl389", "image", "TIFF", "Tagged Image File Format|NO VALUE|fmt/353",
                     "Tagged Image File Format", "NO VALUE", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/353",
                     "NO VALUE", "Tagged Image File Format (TIFF) 1-6",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/353", "Low Risk", "Retain", "PRONOM"],
                    ["dlg", "arl_awc", "arl_awc_awc171", "image", "JPEG", "JPEG File Interchange Format|1.01|fmt/43",
                     "JPEG File Interchange Format", "1.01", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/43",
                     "NO VALUE", "JPEG File Interchange Format 1.01",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/43", "Low Risk", "Retain", "PRONOM and Version"],
                    ["dlg", "gbru_bcd", "gbru_bcd_gbru-bcd-1890", "text", "PDF", "PDF/A|1b|fmt/354", "PDF/A", "1b",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/354", "NO VALUE",
                     "Portable Document Format/Archiving (PDF/A-1b) basic",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/354", "Low Risk", "Retain", "PRONOM"],
                    ["dlg", "gcfa_gtaa", "gcfa_gtaa_gtaa00-11-taa-a-cass-01", "audio", "Waveform Audio",
                     "Waveform Audio|1 PCM Encoding|fmt/704", "Waveform Audio", "1 PCM Encoding",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/704", "NO VALUE",
                     "Waveform Audio File Format (WAVE) with LPCM Audio", np.nan, "Low Risk", "Retain",
                     "Manual (Approximate)"],
                    ["dlg", "gcfa_gtaa", "gcfa_gtaa_gtaa15-04-1-01", "audio", "MPEG",
                     "MPEG 1/2 Audio Layer 3|1|fmt/134", "MPEG 1/2 Audio Layer 3", "1",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/134", "NO VALUE", "MPEG-1 Audio Layer 3",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/134", "Low Risk", "Transform to BWF", "PRONOM"]]
        self.assertEqual(result, expected, "Problem with test for by_aip CSV")

    def test_by_group(self):
        """
        Test for running the script with correct input for a "by_group" CSV.
        """
        # Makes a copy of the CSV for this test, since the test will edit the CSV.
        csv_original = os.path.join("script", "archive_formats_by_group.csv")
        csv_test = os.path.join("script", "archive_formats_by_group_2023-11.csv")
        shutil.copy(csv_original, csv_test)

        # Runs the script
        script_path = os.path.join("..", "..", "fix_excel.py")
        subprocess.run(f"python {script_path} {csv_test}", shell=True)

        # Tests that the updated test CSV has the expected values.
        df = pd.read_csv(csv_test)
        result = [df.columns.tolist()] + df.values.tolist()
        expected = [["Group", "File_IDs", "Size_GB", "Format_Type", "Format_Standardized_Name", "Format_Identification",
                     "Format_Name", "Format_Version", "Registry_Name", "Registry_Key", "Format_Note",
                     "NARA_Format_Name", "NARA_PRONOM_URL", "NARA_Risk_Level", "NARA_Proposed_Preservation_Plan",
                     "NARA_Match_Type"],
                    ["hargrett", 63, 0.005, "text", "Microsoft Word",
                     "Microsoft Word Binary File Format|97-2003|fmt/40", "Microsoft Word Binary File Format",
                     "97-2003", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/40", "NO VALUE",
                     "Microsoft Word for Windows 97-2003", "https://www.nationalarchives.gov.uk/pronom/fmt/40",
                     "Moderate Risk", "Retain", "PRONOM and Version"],
                    ["hargrett", 55, 0.001, "text", "Microsoft Word", "Microsoft Word Binary File Format|5.0|x-fmt/65",
                     "Microsoft Word Binary File Format", "5.0", "https://www.nationalarchives.gov.uk/PRONOM",
                     "x-fmt/65", "NO VALUE", "Microsoft Word for Macintosh 5.0",
                     "https://www.nationalarchives.gov.uk/pronom/x-fmt/65", "Moderate Risk", "Transform to ODT",
                     "PRONOM and Version"],
                    ["hargrett", 931, 0.06, "image", "BMP", "Windows Bitmap|3.0|fmt/116", "Windows Bitmap", "3.0",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/116", "NO VALUE", "Windows Bitmap 3.0",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/116", "Moderate Risk", "Transform to TIFF",
                     "PRONOM and Version"],
                    ["hargrett", 330, 0.347, "image", "JPEG", "JPEG EXIF|2.0|x-fmt/398", "JPEG EXIF", "2.0",
                     "https://www.nationalarchives.gov.uk/PRONOM", "x-fmt/398", "NO VALUE",
                     "Exchangeable Image File Format Compressed 2.0",
                     "https://www.nationalarchives.gov.uk/pronom/x-fmt/398", "Low Risk", "Retain",
                     "PRONOM and Version"],
                    ["russell", 188, 0.003, "text", "WordPerfect", "Wordperfect Secondary File|5.1/5.2|x-fmt/43",
                     "Wordperfect Secondary File", "5.1/5.2", "https://www.nationalarchives.gov.uk/PRONOM",
                     "x-fmt/43", "NO VALUE", "WordPerfect Secondary File 5.1/5.2",
                     "https://www.nationalarchives.gov.uk/pronom/x-fmt/43", "Moderate Risk", "Transform to ODT",
                     "PRONOM and Version"],
                    ["hargrett", 38, 0.14, "image", "JPEG", "JPEG EXIF|10.0|fmt/645", "JPEG EXIF", "10.0",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/645", "NO VALUE",
                     "Exchangeable Image File Format Compressed 2.21",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/645", "Low Risk", "Retain", "PRONOM"],
                    ["hargrett", 12, 0.033, "image", "JPEG", "JPEG EXIF|9.10|fmt/645", "JPEG EXIF", "9.10",
                     "https://www.nationalarchives.gov.uk/PRONOM", "fmt/645", "NO VALUE",
                     "Exchangeable Image File Format Compressed 2.21",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/645", "Low Risk", "Retain", "PRONOM"],
                    ["russell", 99, 0.015, "text", "Microsoft Word",
                     "Microsoft Word Binary File Format|99022200|fmt/40", "Microsoft Word Binary File Format",
                     "99022200", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/40", "NO VALUE",
                     "Microsoft Word Backup File, version 97-onwards",
                     "https://www.nationalarchives.gov.uk/pronom/fmt/40", "Moderate Risk",
                     "Depends on version, transform to Word or PDF", "PRONOM"],
                    ["russell", 115, 0.159, "design", "Adobe Illustrator", "Adobe Illustrator|1.2 0|fmt/423",
                     "Adobe Illustrator", "1.2 0", "https://www.nationalarchives.gov.uk/PRONOM", "fmt/423", "NO VALUE",
                     "Adobe Illustrator 7.0", "https://www.nationalarchives.gov.uk/pronom/fmt/423", "Moderate Risk",
                     "Transform to PDF", "PRONOM"],
                    ["hargrett", 2, 0.0, "image", "JPEG", "JPEG EXIF|1.00|NO VALUE", "JPEG EXIF", "1.00", "NO VALUE",
                     "NO VALUE", "NO VALUE", "No Match", np.nan, "No Match", np.nan, "No NARA Match"],
                    ["magil", 1, 0.908, "web_archive", "WARC",
                     "WARC Archive version 1.0\\015grams\@\\177B|NO VALUE|NO VALUE",
                     "WARC Archive version 1.0\\015grams\@\\177B", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE",
                     "No Match", np.nan, "No Match", np.nan, "No NARA Match"],
                    ["russell", 796, 0.01, "structured_text", "HTML", "HTML Transitional|HTML 4.0|NO VALUE",
                     "HTML Transitional", "HTML 4.0", "NO VALUE", "NO VALUE", "NO VALUE", "No Match", np.nan,
                     "No Match", np.nan, "No NARA Match"]]
        self.assertEqual(result, expected, "Problem with test for by_group CSV")


if __name__ == '__main__':
    unittest.main()
