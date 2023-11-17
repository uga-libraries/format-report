"""
Tests the entire script fix_versions.py,
which fixes errors in the version caused by openening the CSV in Excel.
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
        paths = [os.path.join("script", "archive_formats_by_aip_2023-11.csv")]
        for path in paths:
            if os.path.exists(path):
                os.remove(path)

    def test_argument_error(self):
        """
        Test for running the script with the required argument.
        It will print a message and exit the script.
        """
        script_path = os.path.join("..", "..", "fix_versions.py")

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
        script_path = os.path.join("..", "..", "fix_versions.py")
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


if __name__ == '__main__':
    unittest.main()
