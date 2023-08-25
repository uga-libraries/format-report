"""
Tests for the function add_nara_risk(),
which adds information from the NARA Preservation Action Plans CSV to ARCHive formats CSVs.
"""

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
        if os.path.exists(os.path.join("add_nara_risk", "archive_formats_by_group_test.csv")):
            os.remove(os.path.join("add_nara_risk", "archive_formats_by_group_test.csv"))

    def test_status(self):
        """
        Using this to test the function as I develop it.
        """
        # Make a copy of the CSV to use for input, since the function changes it.
        test_copy = os.path.join("add_nara_risk", "archive_formats_by_group_test.csv")
        shutil.copy2(os.path.join("add_nara_risk", "archive_formats_by_group_simpler.csv"), test_copy)

        # Run the function being tested.
        add_nara_risk(test_copy, "NARA_PreservationActionPlan_FileFormats_test.csv")

        # Tests that the CSV produced by the function has the correct values.
        csv_df = pd.read_csv(test_copy)
        result = [csv_df.columns.tolist()] + csv_df.values.tolist()
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
