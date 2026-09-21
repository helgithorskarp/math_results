#!/usr/bin/env python3

import unittest

import verify


class RemoteResolverExtremalTests(unittest.TestCase):
    def test_extremal_family(self) -> None:
        self.assertEqual(verify.audit_extremal_family(6), (141, 120))

    def test_general_graphs(self) -> None:
        self.assertEqual(verify.audit_general_graphs(4), (43, 166, 88))

    def test_rooted_spiders(self) -> None:
        self.assertEqual(verify.audit_spider_family(5), (62, 449))

    def test_labelled_trees(self) -> None:
        self.assertEqual(verify.audit_all_labelled_trees(6), (1441, 8476, 644))

    def test_nonexample_path_endpoint(self) -> None:
        path = verify.graph_from_edges(3, [(0, 1), (1, 2)])
        self.assertFalse(verify.remote_resolver(path, 0))
        self.assertTrue(verify.remote_resolver(path, 1))


if __name__ == "__main__":
    unittest.main()
