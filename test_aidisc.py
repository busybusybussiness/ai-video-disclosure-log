"""Fixture tests for aidisc. Run: python test_aidisc.py"""
import os
import tempfile
import unittest

import aidisc


class RecordTests(unittest.TestCase):
    def test_no_ai_known_bad_none(self):
        t = aidisc.build_record("v1", "T", [], False, False, False, False, "2026-01-01")
        self.assertIn("AI used: no", t)
        self.assertIn("no (no AI content recorded)", t)

    def test_realistic_unapplied_flags_action(self):
        t = aidisc.build_record("v2", "T", ["SDXL"], True, False, True, False, "2026-01-01")
        self.assertIn("YES - realistic AI content", t)
        self.assertIn("ACTION: required disclosure not yet marked", t)

    def test_realistic_applied_no_action(self):
        t = aidisc.build_record("v3", "T", ["SDXL"], True, True, True, True, "2026-01-01")
        self.assertNotIn("ACTION:", t)
        self.assertIn("Disclosure applied in upload form: yes", t)

    def test_non_realistic_ai_probably_no(self):
        t = aidisc.build_record("v4", "T", ["x"], True, False, False, False, "2026-01-01")
        self.assertIn("probably no", t)

    def test_disclaimer_always_present(self):
        t = aidisc.build_record("v5", "T", [], False, False, False, False, "2026-01-01")
        self.assertIn("not legal advice", t)
        self.assertIn("does not state that the video complies", t)

    def test_slugify_rejects_empty_and_sanitizes(self):
        self.assertEqual(aidisc.slugify("../../etc passwd"), "etc-passwd")
        with self.assertRaises(ValueError):
            aidisc.slugify("...")


class FileTests(unittest.TestCase):
    def test_writes_then_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            t = aidisc.build_record("ep-001", "T", [], False, False, False, False, "2026-01-01")
            path = aidisc.write_record(d, "ep-001", t)
            self.assertTrue(os.path.exists(path))
            with self.assertRaises(FileExistsError):
                aidisc.write_record(d, "ep-001", t)

    def test_cli_flag_validation(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(SystemExit):
                aidisc.main(["--out", d, "--video-id", "x", "--title", "t", "--altered"])

    def test_cli_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            rc = aidisc.main(["--out", d, "--video-id", "ep-9", "--title", "Rain",
                              "--tool", "SDXL", "--ai-used", "--realistic"])
            self.assertEqual(rc, 0)
            with open(os.path.join(d, "ep-9.md"), encoding="utf-8") as f:
                body = f.read()
            self.assertIn("ACTION: required disclosure not yet marked", body)
            self.assertEqual(aidisc.main(["--out", d, "--video-id", "ep-9", "--title", "Rain"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
