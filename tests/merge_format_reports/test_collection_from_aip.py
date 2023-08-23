"""
Tests for the function collection_from_aip(),
which calculates the collection ID based on the AIP ID and group.
"""

import unittest
from merge_format_reports import collection_from_aip


class MyTestCase(unittest.TestCase):

    def test_bmac_peabody(self):
        """
        Test for an AIP ID that matches the pattern: 6th character (after bmac_) is a number
        """
        collection_id = collection_from_aip("bmac_2000032edt-1-arch", "bmac")
        self.assertEqual(collection_id, "peabody", "Problem with bmac: peabody")

    def test_bmac_har_ms(self):
        """
        Test for an AIP ID that matches the pattern: starts with har-ms
        """
        collection_id = collection_from_aip("har-ms4063_0011", "bmac")
        self.assertEqual(collection_id, "har-ms4063", "Problem with bmac: har-ms")

    def test_bmac_bmac_wsbn(self):
        """
        Test for an AIP ID that matches the pattern: starts with bmac_bmac_wsbn
        """
        collection_id = collection_from_aip("bmac_bmac_wsbn_0877", "bmac")
        self.assertEqual(collection_id, "wsbn", "Problem with bmac: bmac_wsbn")

    def test_bmac_wrdw(self):
        """
        Test for an AIP ID that matches the pattern: starts with bmac_wrdw_
        """
        collection_id = collection_from_aip("bmac_wrdw_0007", "bmac")
        self.assertEqual(collection_id, "wrdw-video", "Problem with bmac: wrdw")

    def test_bmac_walb(self):
        """
        Test for an AIP ID that matches the pattern: starts with bmac_walb
        """
        collection_id = collection_from_aip("bmac_walb_0421", "bmac")
        self.assertEqual(collection_id, "walb", "Problem with bmac: walb")

    def test_bmac_walb_video(self):
        """
        Test for an AIP ID that matches the pattern: starts with bmac_walb-video
        """
        collection_id = collection_from_aip("bmac_walb-video_0134", "bmac")
        self.assertEqual(collection_id, "walb", "Problem with bmac: walb-video")

    def test_bmac_general1(self):
        """
        Test for an AIP ID that matches the pattern: letters, numbers, and dashes between 'bmac_' and '_'
        This collection ID is letters only.
        """
        collection_id = collection_from_aip("bmac_artrosen_0138_01", "bmac")
        self.assertEqual(collection_id, "artrosen", "Problem with bmac: general1 ")

    def test_bmac_general2(self):
        """
        Test for an AIP ID that matches the pattern: letters, numbers, and dashes between 'bmac_' and '_'
        This collection ID is letters and a dash.
        """
        collection_id = collection_from_aip("bmac_hm-bennettk_0001", "bmac")
        self.assertEqual(collection_id, "hm-bennettk", "Problem with bmac: general 2")

    def test_bmac_general3(self):
        """
        Test for an AIP ID that matches the pattern: letters, numbers, and dashes between 'bmac_' and '_'
        This collection ID is letters, numbers, and dashes
        """
        collection_id = collection_from_aip("bmac_har-ua12-002_005", "bmac")
        self.assertEqual(collection_id, "har-ua12-002", "Problem with bmac: general 3")

    def test_bmac_error(self):
        """
        Test for an AIP ID that does not match any patterns and raises an AttributeError.
        """
        with self.assertRaises(AttributeError):
            collection_from_aip("error_123", "bmac")

    def test_dlg_turningpoint_ahc0062f_001(self):
        """
        Test for an AIP ID that is equal to dlg_turningpoint_ahc0062f-001
        """
        collection_id = collection_from_aip("dlg_turningpoint_ahc0062f-001", "dlg")
        self.assertEqual(collection_id, "geh_ahc-mss820f", "Problem with dlg: turningpoint_ahc0062f_001")

    def test_dlg_turningpoint_ahc_v(self):
        """
        Test for an AIP ID that matches the pattern: starts with turningpoint_ahc and has v
        """
        collection_id = collection_from_aip("dlg_turningpoint_ahc0198v-001", "dlg")
        self.assertEqual(collection_id, "geh_ahc-vis198", "Problem with dlg: turningpoint_ahc_v")

    def test_dlg_turningpoint_ahc_letter(self):
        """
        Test for an AIP ID that matches the pattern: starts with turningpoint_ahc and has a letter but not v
        """
        collection_id = collection_from_aip("dlg_turningpoint_ahc0101f-001", "dlg")
        self.assertEqual(collection_id, "geh_ahc-mss101f", "Problem with dlg: turningpoint_ahc")

    def test_dlg_turningpoint_ahc(self):
        """
        Test for an AIP ID that matches the pattern: starts with turningpoint_ahc and has no additional letter
        """
        collection_id = collection_from_aip("dlg_turningpoint_ahc0011-001-008", "dlg")
        self.assertEqual(collection_id, "geh_ahc-mss11", "Problem with dlg: turningpoint_ahc")

    def test_dlg_turningpoint_ghs_bs(self):
        """
        Test for an AIP ID that matches the pattern: starts with turningpoint_ghs and bs
        """
        collection_id = collection_from_aip("dlg_turningpoint_ghs1361bs-001", "dlg")
        self.assertEqual(collection_id, "g-hi_ms1361-bs", "Problem with dlg: turningpoint_ghs_bs")

    def test_dlg_turningpoint_ghs(self):
        """
        Test for an AIP ID that matches the pattern: starts with turningpoint_ghs and no bs
        """
        collection_id = collection_from_aip("dlg_turningpoint_ghs0002-001", "dlg")
        self.assertEqual(collection_id, "g-hi_ms0002", "Problem with dlg: turningpoint_ghs")

    def test_dlg_turningpoint_harg(self):
        """
        Test for an AIP ID that matches the pattern: starts with turningpoint_harg
        """
        collection_id = collection_from_aip("dlg_turningpoint_harg0015-001-002", "dlg")
        self.assertEqual(collection_id, "guan_ms15", "Problem with dlg: turningpoint_harg")

    def test_dlg_batch_gu(self):
        """
        Test for an AIP ID that matches the pattern: starts with batch_gu
        """
        collection_id = collection_from_aip("batch_gua_athensgazette_archival", "dlg")
        self.assertEqual(collection_id, "dlg_ghn", "Problem with dlg: batch_gu")

    def test_dlg_general1(self):
        """
        Test for an AIP ID that matches the pattern:
        letters, numbers, dashes, and one underscore before the second underscore
        This collection ID is just letters and the underscore.
        """
        collection_id = collection_from_aip("aarl_afpc_adamscarlton20171104", "dlg")
        self.assertEqual(collection_id, "aarl_afpc", "Problem with dlg: general 1")

    def test_dlg_general2(self):
        """
        Test for an AIP ID that matches the pattern:
        letters, numbers, dashes, and one underscore before the second underscore
        This collection ID is letters, a number and the underscore.
        """
        collection_id = collection_from_aip("c8y_gac_gac006", "dlg")
        self.assertEqual(collection_id, "c8y_gac", "Problem with dlg: general 2")

    def test_dlg_general3(self):
        """
        Test for an AIP ID that matches the pattern:
        letters, numbers, dashes, and one underscore before the second underscore
        This collection ID is letters, a dash and the underscore.
        """
        collection_id = collection_from_aip("eccca_aafp-ec_ecaaam-006", "dlg")
        self.assertEqual(collection_id, "eccca_aafp-ec", "Problem with dlg: general 3")

    def test_dlg_error(self):
        """
        Test for AIP IDs that does not match any patterns and raises an AttributeError.
        One is turningpoint and one is general to test both places where the error is raised.
        """
        with self.assertRaises(AttributeError):
            collection_from_aip("dlg_turningpoint_error_0001", "dlg")

        with self.assertRaises(AttributeError):
            collection_from_aip("error_123", "dlg")

    def test_dlg_hargrett_general(self):
        """
        Test for an AIP ID that matches the pattern:
        3-4 letters, and underscore, and 4 letters, numbers and/or dashes before a second underscore
        """
        collection_id = collection_from_aip("guan_1170_harg1170-070-026", "dlg-hargrett")
        self.assertEqual(collection_id, "guan_1170", "Problem with dlg-hargrett: general")

    def test_dlg_hargrett_error(self):
        """
        Test for an AIP ID that does not match the pattern and raises an AttributeError.
        """
        with self.assertRaises(AttributeError):
            collection_from_aip("error_123", "dlg-hargrett")

    def test_dlg_magil_general(self):
        """
        Test for an AIP ID that matches the pattern: letters and one underscore before the second underscore
        """
        collection_id = collection_from_aip("dlg_sanb_abbeville-1913", "dlg-magil")
        self.assertEqual(collection_id, "dlg_sanb", "Problem with dlg-magil: general")

    def test_dlg_magil_error(self):
        """
        Test for an AIP ID that does not match the pattern and raises an AttributeError.
        """
        with self.assertRaises(AttributeError):
            collection_from_aip("error_123", "dlg-magil")

    def test_hargrett_har(self):
        """
        Test for an AIP ID that matches the pattern: starts with har-
        """
        collection_id = collection_from_aip("har-ua20-002_0003_media", "hargrett")
        self.assertEqual(collection_id, "har-ua20-002", "Problem with hargrett: har-")

    def test_hargrett_general_er(self):
        """
        Test for an AIP ID that matches the pattern: anything before er (this test) or -web
        """
        collection_id = collection_from_aip("harg-ms3770er0003", "hargrett")
        self.assertEqual(collection_id, "harg-ms3770", "Problem with hargrett: general_er")

    def test_hargrett_general_web(self):
        """
        Test for an AIP ID that matches the pattern: anything before er or -web (this test)
        """
        collection_id = collection_from_aip("harg-0000-web-202007-0003", "hargrett")
        self.assertEqual(collection_id, "harg-0000", "Problem with hargrett: general")

    def test_hargrett_error(self):
        """
        Test for an AIP ID that does not match any patterns and raises an AttributeError.
        """
        with self.assertRaises(AttributeError):
            collection_from_aip("wrong_123", "hargrett")

    def test_magil_ggp(self):
        """
        Test for an AIP ID that matches the pattern: magil-ggp-7 numbers-4 numbers-2 numbers
        """
        collection_id = collection_from_aip("magil-ggp-2508399-2022-05", "magil")
        self.assertEqual(collection_id, "no-coll", "Problem with magil: ggp")

    def test_magil_error(self):
        """
        Test for an AIP ID that does not match any patterns and raises an AttributeError.
        """
        with self.assertRaises(AttributeError):
            collection_from_aip("wrong_123", "magil")

    def test_russell_general1(self):
        """
        Test for an AIP ID that matches the pattern: rbrl, dash (optional), 3 numbers
        This AIP ID is used for digital archives.
        """
        collection_id = collection_from_aip("rbrl-153-er-000015", "russell")
        self.assertEqual(collection_id, "rbrl153", "Problem with russell: general 1")

    def test_russell_general2(self):
        """
        Test for an AIP ID that matches the pattern: rbrl, dash (optional), 3 numbers
        This AIP ID is used for oral histories
        """
        collection_id = collection_from_aip("rbrl361aohp-002_media", "russell")
        self.assertEqual(collection_id, "rbrl361", "Problem with russell: general 2")

    def test_russell_general3(self):
        """
        Test for an AIP ID that matches the pattern: rbrl, dash (optional), 3 numbers
        This AIP ID is used for web AIPs.
        """
        collection_id = collection_from_aip("rbrl-057-web-202302-0001", "russell")
        self.assertEqual(collection_id, "rbrl057", "Problem with russell: general 3")

    def test_russell_error(self):
        """
        Test for an AIP ID that does not match the pattern and raises an AttributeError.
        """
        with self.assertRaises(AttributeError):
            collection_from_aip("error_123", "russell")

    def test_value_error(self):
        """
        Test for a group that does match any of the groups and raises a ValueError.
        """
        with self.assertRaises(ValueError):
            collection_from_aip("error_123", "error")


if __name__ == '__main__':
    unittest.main()
