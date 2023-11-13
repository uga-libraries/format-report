"""
Tests for the function add_nara_risk(),
which adds information from the NARA Preservation Action Plans CSV to ARCHive formats CSVs.
"""

import numpy as np
import os
import pandas as pd
import shutil
import unittest
from merge_format_reports import add_nara_risk


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """
        Delete the test version of CSVs, when produced.
        """
        if os.path.exists(os.path.join("add_nara_risk", "archive_formats_by_aip_test.csv")):
            os.remove(os.path.join("add_nara_risk", "archive_formats_by_aip_test.csv"))

        if os.path.exists(os.path.join("add_nara_risk", "archive_formats_by_group_test.csv")):
            os.remove(os.path.join("add_nara_risk", "archive_formats_by_group_test.csv"))

    def test_by_aip(self):
        """
        Test for using the function on the ARCHive formats CSV organized by AIP.
        """
        # Make a copy of the CSV to use for input, since the function changes it.
        test_original = os.path.join("add_nara_risk", "archive_formats_by_aip.csv")
        test_copy = os.path.join("add_nara_risk", "archive_formats_by_aip_test.csv")
        shutil.copy2(test_original, test_copy)

        # Run the function being tested and converts the resulting CSV into a list for easier comparison.
        add_nara_risk(test_copy, "NARA_PreservationActionPlan_FileFormats_test.csv")
        df = pd.read_csv(test_copy)
        result = [df.columns.tolist()] + df.values.tolist()

        # Tests that the CSV produced by the function has the correct values.
        expected = [['Group', 'Collection', 'AIP', 'Format_Type', 'Format_Standardized_Name', 'Format_Identification',
                     'Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key', 'Format_Note',
                     'NARA_Format_Name', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['hargrett', 'harg-ms3786', 'harg-ms3786er0006', 'structured_text', 'HTML', 'HTML|5.1|fmt/96',
                     'HTML', '5.1', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/96', 'NO VALUE',
                     'Hypertext Markup Language 5.1', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Low Risk', 'Retain', 'PRONOM and Version'],
                    ['hargrett', 'harg-ms3786', 'harg-ms3786er0006', 'structured_text', 'HTML', 'HTML|1.0|fmt/102',
                     'HTML', '1.0', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/102', 'NO VALUE',
                     'eXtensible Hypertext Markup Language 1.0', 'https://www.nationalarchives.gov.uk/pronom/fmt/102',
                     'Low Risk', 'Retain', 'PRONOM and Version'],
                    ['hargrett', 'harg-ms3786', 'harg-ms3786er0006', 'structured_text', 'HTML', 'HTML|1.0|fmt/102',
                     'HTML', '1.0', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/102', 'NO VALUE',
                     'Hypertext Markup Language 1.0', 'https://www.nationalarchives.gov.uk/pronom/fmt/102',
                     'Low Risk', 'Retain', 'PRONOM and Version'],
                    ['hargrett', 'harg-ms3786', 'harg-ms3786er0007', 'structured_text', 'HTML', 'HTML|1.0|fmt/102',
                     'HTML', '1.0', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/102', 'NO VALUE',
                     'eXtensible Hypertext Markup Language 1.0', 'https://www.nationalarchives.gov.uk/pronom/fmt/102',
                     'Low Risk', 'Retain', 'PRONOM and Version'],
                    ['hargrett', 'harg-ms3786', 'harg-ms3786er0007', 'structured_text', 'HTML', 'HTML|1.0|fmt/102',
                     'HTML', '1.0', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/102', 'NO VALUE',
                     'Hypertext Markup Language 1.0', 'https://www.nationalarchives.gov.uk/pronom/fmt/102',
                     'Low Risk', 'Retain', 'PRONOM and Version'],
                    ['hargrett', 'harg-ms3786', 'harg-ms3786er0007', 'structured_text', 'HTML', 'HTML|5.1|fmt/96',
                     'HTML', '5.1', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/96', 'NO VALUE',
                     'Hypertext Markup Language 5.1', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Low Risk', 'Retain', 'PRONOM and Version'],
                    ['dlg', 'arl_acl', 'arl_acl_acl328', 'design', 'CorelDraw Compressed Drawing',
                     'CorelDraw Compressed Drawing|NO VALUE|x-fmt/31', 'CorelDraw Compressed Drawing',
                     'NO VALUE', 'https://www.nationalarchives.gov.uk/PRONOM', 'x-fmt/31', 'NO VALUE',
                     'CorelDraw Compressed Drawing', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/31',
                     'High Risk', 'Transform to a TBD format, possibly PDF or TIFF', 'PRONOM and Name'],
                    ['dlg', 'arl_awc', 'arl_awc_awc171', 'design', 'CorelDraw Compressed Drawing',
                     'CorelDraw Compressed Drawing|NO VALUE|x-fmt/31', 'CorelDraw Compressed Drawing',
                     'NO VALUE', 'https://www.nationalarchives.gov.uk/PRONOM', 'x-fmt/31', 'NO VALUE',
                     'CorelDraw Compressed Drawing', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/31',
                     'High Risk', 'Transform to a TBD format, possibly PDF or TIFF', 'PRONOM and Name'],
                    ['dlg', 'dlg_vsbg', 'dlg_vsbg_jaj001', 'image', 'DNG', 'Digital Negative|NO VALUE|fmt/436',
                     'Digital Negative', 'NO VALUE', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/436',
                     'NO VALUE', 'Digital Negative Format 1.0', 'https://www.nationalarchives.gov.uk/pronom/fmt/436',
                     'Low Risk', 'Retain', 'PRONOM'],
                    ['dlg', 'dlg_vsbg', 'dlg_vsbg_jaj002', 'image', 'DNG', 'Digital Negative|NO VALUE|fmt/436',
                     'Digital Negative', 'NO VALUE', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/436',
                     'NO VALUE', 'Digital Negative Format 1.0', 'https://www.nationalarchives.gov.uk/pronom/fmt/436',
                     'Low Risk', 'Retain', 'PRONOM'],
                    ['hargrett', 'harg-ms3786', 'harg-ms3786er0005', 'image', 'DNG',
                     'Digital Negative|NO VALUE|fmt/436', 'Digital Negative', 'NO VALUE',
                     'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/436', 'NO VALUE',
                     'Digital Negative Format 1.0', 'https://www.nationalarchives.gov.uk/pronom/fmt/436',
                     'Low Risk', 'Retain', 'PRONOM'],
                    ['hargrett', 'harg-ms3786', 'harg-ms3786er0013', 'image', 'DNG',
                     'Digital Negative|NO VALUE|fmt/436', 'Digital Negative', 'NO VALUE',
                     'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/436', 'NO VALUE',
                     'Digital Negative Format 1.0', 'https://www.nationalarchives.gov.uk/pronom/fmt/436',
                     'Low Risk', 'Retain', 'PRONOM'],
                    ['hargrett', 'harg-ms3786', 'harg-ms3786er0004', 'executable', 'Batch script',
                     'batch script|NO VALUE|NO VALUE', 'batch script', 'NO VALUE', 'NO VALUE', 'NO VALUE',
                     'NO VALUE', 'Batch Script', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/413',
                     'Moderate Risk', 'Retain', 'Format Name'],
                    ['dlg', 'arl_acl', 'arl_acl_acl328', 'application', 'Unknown Binary',
                     'Unknown Binary|NO VALUE|NO VALUE', 'Unknown Binary', 'NO VALUE', 'NO VALUE', 'NO VALUE',
                     'NO VALUE', 'No Match', np.NaN, 'No Match', np.NaN, 'No NARA Match']]
        self.assertEqual(result, expected, "Problem with test for by_aip CSV")

    def test_by_group(self):
        """
        Test for using the function on the ARCHive formats CSV organized by group.
        """
        # Make a copy of the CSV to use for input, since the function changes it.
        test_original = os.path.join("add_nara_risk", "archive_formats_by_group.csv")
        test_copy = os.path.join("add_nara_risk", "archive_formats_by_group_test.csv")
        shutil.copy2(test_original, test_copy)

        # Run the function being tested and converts the resulting CSV into a list for easier comparison.
        add_nara_risk(test_copy, "NARA_PreservationActionPlan_FileFormats_test.csv")
        df = pd.read_csv(test_copy)
        result = [df.columns.tolist()] + df.values.tolist()

        # Tests that the CSV produced by the function has the correct values.
        expected = [['Group', 'File_IDs', 'Size_GB', 'Format_Type', 'Format_Standardized_Name',
                     'Format_Identification', 'Format_Name', 'Format_Version', 'Registry_Name', 'Registry_Key',
                     'Format_Note', 'NARA_Format_Name', 'NARA_PRONOM_URL', 'NARA_Risk_Level',
                     'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['hargrett', 57, 0.02, 'structured_text', 'HTML', 'HTML|5.1|fmt/96', 'HTML', '5.1',
                     'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/96', 'NO VALUE',
                     'Hypertext Markup Language 5.1', 'https://www.nationalarchives.gov.uk/pronom/fmt/96', 'Low Risk',
                     'Retain', 'PRONOM and Version'],
                    ['hargrett', 90, 0.04, 'structured_text', 'HTML', 'HTML|1.0|fmt/102', 'HTML', '1.0',
                     'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/102', 'NO VALUE',
                     'eXtensible Hypertext Markup Language 1.0', 'https://www.nationalarchives.gov.uk/pronom/fmt/102',
                     'Low Risk', 'Retain', 'PRONOM and Version'],
                    ['hargrett', 90, 0.04, 'structured_text', 'HTML', 'HTML|1.0|fmt/102', 'HTML', '1.0',
                     'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/102', 'NO VALUE',
                     'Hypertext Markup Language 1.0', 'https://www.nationalarchives.gov.uk/pronom/fmt/102', 'Low Risk',
                     'Retain', 'PRONOM and Version'],
                    ['dlg', 581, 69.2, 'design', 'CorelDraw Compressed Drawing',
                     'CorelDraw Compressed Drawing|NO VALUE|x-fmt/31', 'CorelDraw Compressed Drawing',
                     'NO VALUE', 'https://www.nationalarchives.gov.uk/PRONOM', 'x-fmt/31', 'NO VALUE',
                     'CorelDraw Compressed Drawing', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/31',
                     'High Risk', 'Transform to a TBD format, possibly PDF or TIFF', 'PRONOM and Name'],
                    ['dlg', 300, 20.0, 'image', 'DNG', 'Digital Negative|NO VALUE|fmt/436', 'Digital Negative',
                     'NO VALUE', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/436', 'NO VALUE',
                     'Digital Negative Format 1.0', 'https://www.nationalarchives.gov.uk/pronom/fmt/436', 'Low Risk',
                     'Retain', 'PRONOM'],
                    ['hargrett', 13, 1.5, 'image', 'DNG', 'Digital Negative|NO VALUE|fmt/436',
                     'Digital Negative', 'NO VALUE', 'https://www.nationalarchives.gov.uk/PRONOM', 'fmt/436',
                     'NO VALUE', 'Digital Negative Format 1.0', 'https://www.nationalarchives.gov.uk/pronom/fmt/436',
                     'Low Risk', 'Retain', 'PRONOM'],
                    ['hargrett', 132, 0.687, 'executable', 'Batch script', 'batch script|NO VALUE|NO VALUE',
                     'batch script', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'Batch Script',
                     'https://www.nationalarchives.gov.uk/pronom/x-fmt/413', 'Moderate Risk', 'Retain', 'Format Name'],
                    ['dlg', 1, 662.702, 'application', 'Unknown Binary', 'Unknown Binary|NO VALUE|NO VALUE',
                     'Unknown Binary', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'No Match', np.NaN, 'No Match',
                     np.NaN, 'No NARA Match']]
        self.assertEqual(result, expected, "Problem with test for by_group CSV")


if __name__ == '__main__':
    unittest.main()
