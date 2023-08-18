"""
Tests for the function read_row(),
which reads data from a row in a report and returns lists of rows to add to the CSVs.
"""

import unittest
from merge_format_reports import read_row


class MyTestCase(unittest.TestCase):

    def test_aip_attribute_error(self):
        """
        Test for a row that has an AIP which does match any patterns for its group.
        The error is raised by collection_from_aip().
        """
        # Makes test input and runs the function being tested.
        report_row = ["1", "48", "0.001", "Plain text", "", "", "", "", "har-error-001_001"]
        aip_row_list, group_row = read_row(report_row, "hargrett")

        # Tests that aip_row_list contains the correct information.
        expected_aip = [["hargrett", "UNABLE TO CALCULATE", "har-error-001_001", "text", "Plain Text File",
                         "Plain text|NO VALUE|NO VALUE", "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE"]]
        self.assertEqual(aip_row_list, expected_aip, "Problem with test for aip: value error, aip_row_list")

        # Tests that group_row contains the correct information.
        expected_group = ["hargrett", "48", "0.001", "text", "Plain Text File", "Plain text|NO VALUE|NO VALUE",
                          "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE"]
        self.assertEqual(group_row, expected_group, "Problem with test for aip: value error, group_row")

    def test_aip_value_error(self):
        """
        Test for a row that has an unexpected group. The error is raised by collection_from_aip().
        """
        # Makes test input and runs the function being tested.
        report_row = ["1", "48", "0.001", "Plain text", "", "", "", "", "error_new_0001"]
        aip_row_list, group_row = read_row(report_row, "error")

        # Tests that aip_row_list contains the correct information.
        expected_aip = [["error", "UNABLE TO CALCULATE", "error_new_0001", "text", "Plain Text File",
                         "Plain text|NO VALUE|NO VALUE", "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE"]]
        self.assertEqual(aip_row_list, expected_aip, "Problem with test for aip: value error, aip_row_list")

        # Tests that group_row contains the correct information.
        expected_group = ["error", "48", "0.001", "text", "Plain Text File", "Plain text|NO VALUE|NO VALUE",
                          "Plain text", "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE"]
        self.assertEqual(group_row, expected_group, "Problem with test for aip: value error, group_row")

    def test_aip_one(self):
        """
        Test for a row that includes only one AIP.
        """
        # Makes test input and runs the function being tested.
        report_row = ["1", "17", "0.161", "TIFF", "", "", "", "", "zjf_skp_skp001"]
        aip_row_list, group_row = read_row(report_row, "dlg")

        # Tests that aip_row_list contains the correct information.
        expected_aip = [["dlg", "zjf_skp", "zjf_skp_skp001", "image", "TIFF", "TIFF|NO VALUE|NO VALUE", "TIFF",
                         "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE"]]
        self.assertEqual(aip_row_list, expected_aip, "Problem with test for aip: one, aip_row_list")

        # Tests that group_row contains the correct information.
        expected_group = ["dlg", "17", "0.161", "image", "TIFF", "TIFF|NO VALUE|NO VALUE", "TIFF",
                          "NO VALUE", "NO VALUE", "NO VALUE", "NO VALUE"]
        self.assertEqual(group_row, expected_group, "Problem with test for aip: one, group_row")

    def test_aip_three(self):
        """
        Test for a row that includes three AIPs.
        """
        # Makes test input and runs the function being tested.
        report_row = ["3", "386", "16.934", "TIFF EXIF", "2.2", "https://www.nationalarchives.gov.uk/PRONOM",
                      "x-fmt/387", "", "arl_awc_awc343a|chat_scp_cvl205|satp_hrl_hrl039"]
        aip_row_list, group_row = read_row(report_row, "dlg")

        # Tests that aip_row_list contains the correct information.
        expected_aip = [["dlg", "arl_awc", "arl_awc_awc343a", "image", "TIFF", "TIFF EXIF|2.2|x-fmt/387",
                         "TIFF EXIF", "2.2", "https://www.nationalarchives.gov.uk/PRONOM", "x-fmt/387", "NO VALUE"],
                        ["dlg", "chat_scp", "chat_scp_cvl205", "image", "TIFF", "TIFF EXIF|2.2|x-fmt/387",
                         "TIFF EXIF", "2.2", "https://www.nationalarchives.gov.uk/PRONOM", "x-fmt/387", "NO VALUE"],
                        ["dlg", "satp_hrl", "satp_hrl_hrl039", "image", "TIFF", "TIFF EXIF|2.2|x-fmt/387",
                         "TIFF EXIF", "2.2", "https://www.nationalarchives.gov.uk/PRONOM", "x-fmt/387", "NO VALUE"]]
        self.assertEqual(aip_row_list, expected_aip, "Problem with test for aip: three, aip_row_list")

        # Tests that group_row contains the correct information.
        expected_group = ["dlg", "386", "16.934", "image", "TIFF", "TIFF EXIF|2.2|x-fmt/387", "TIFF EXIF", "2.2",
                          "https://www.nationalarchives.gov.uk/PRONOM", "x-fmt/387", "NO VALUE"]
        self.assertEqual(group_row, expected_group, "Problem with test for aip: three, group_row")

    def test_blank(self):
        """
        Test for a row that includes blank values.
        """
        # Makes test input and runs the function being tested.
        report_row = ["2", "28656", "256468.469", "MXF", "", "", "", "Video is encoded in the following codec: DV",
                      "bmac_wsb-video_ac01012003|bmac_wsb-video_ac01012004"]
        aip_row_list, group_row = read_row(report_row, "bmac")

        # Tests that aip_row_list contains the correct information.
        expected_aip = [["bmac", "wsb-video", "bmac_wsb-video_ac01012003", "video", "MXF", "MXF|NO VALUE|NO VALUE",
                         "MXF", "NO VALUE", "NO VALUE", "NO VALUE", "Video is encoded in the following codec: DV"],
                        ["bmac", "wsb-video", "bmac_wsb-video_ac01012004", "video", "MXF", "MXF|NO VALUE|NO VALUE",
                         "MXF", "NO VALUE", "NO VALUE", "NO VALUE", "Video is encoded in the following codec: DV"]]
        self.assertEqual(aip_row_list, expected_aip, "Problem with test for blank, aip_row_list")

        # Tests that group_row contains the correct information.
        expected_group = ["bmac", "28656", "256468.469", "video", "MXF", "MXF|NO VALUE|NO VALUE", "MXF",
                          "NO VALUE", "NO VALUE", "NO VALUE", "Video is encoded in the following codec: DV"]
        self.assertEqual(group_row, expected_group, "Problem with test for blank, group_row")

    def test_no_blank(self):
        """
        Test for a row that does not include blank values.
        """
        # Makes test input and runs the function being tested.
        report_row = ["2", "836", "17005.995", "QuickTime", "for_test_version",
                      "https://www.nationalarchives.gov.uk/PRONOM", "x-fmt/384",
                      "File is encoded in the following wrapper:ProRes 422 HQ",
                      "bmac_99144ent-2|bmac_athdept_0066"]
        aip_row_list, group_row = read_row(report_row, "bmac")

        # Tests that aip_row_list contains the correct information.
        expected_aip = [["bmac", "peabody", "bmac_99144ent-2", "video", "Quicktime",
                         "QuickTime|for_test_version|x-fmt/384", "QuickTime", "for_test_version",
                         "https://www.nationalarchives.gov.uk/PRONOM", "x-fmt/384",
                         "File is encoded in the following wrapper:ProRes 422 HQ"],
                        ["bmac", "athdept", "bmac_athdept_0066", "video", "Quicktime",
                         "QuickTime|for_test_version|x-fmt/384", "QuickTime", "for_test_version",
                         "https://www.nationalarchives.gov.uk/PRONOM", "x-fmt/384",
                         "File is encoded in the following wrapper:ProRes 422 HQ"]]
        self.assertEqual(aip_row_list, expected_aip, "Problem with test for no blank, aip_row_list")

        # Tests that group_row contains the correct information.
        expected_group = ["bmac", "836", "17005.995", "video", "Quicktime", "QuickTime|for_test_version|x-fmt/384",
                          "QuickTime", "for_test_version", "https://www.nationalarchives.gov.uk/PRONOM", "x-fmt/384",
                          "File is encoded in the following wrapper:ProRes 422 HQ"]
        self.assertEqual(group_row, expected_group, "Problem with test for no blank, group_row")


if __name__ == '__main__':
    unittest.main()
