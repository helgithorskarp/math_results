"""Tests for the immutable-history dependency audit."""

from copy import deepcopy
import unittest

import verify_git_history as history


class GitHistoryTests(unittest.TestCase):
    def test_complete_history(self) -> None:
        records, review_links = history.audit_history(history.load_manifest())
        self.assertEqual(len(records), 9)
        self.assertEqual(sum(len(record["files"]) for record in records), 18)
        self.assertEqual(review_links, 5)

    def test_hash_rejection(self) -> None:
        manifest = deepcopy(history.load_manifest())
        manifest["artifacts"][0]["files"]["README.md"] = "0" * 64
        with self.assertRaises(AssertionError):
            history.audit_history(manifest)

    def test_noncanonical_commit_rejection(self) -> None:
        manifest = deepcopy(history.load_manifest())
        manifest["artifacts"][0]["source_commit"] = "HEAD"
        with self.assertRaises(ValueError):
            history.audit_history(manifest)

    def test_parent_path_rejection(self) -> None:
        manifest = deepcopy(history.load_manifest())
        manifest["artifacts"][0]["path"] = "../outside"
        with self.assertRaises(ValueError):
            history.audit_history(manifest)


if __name__ == "__main__":
    unittest.main()
