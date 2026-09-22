#!/usr/bin/env python3
import unittest

import verify


class AuditTests(unittest.TestCase):
    def test_exception_catalogue(self):
        self.assertTrue(verify.is_exception((('P', 1), ('C', 3))))
        self.assertTrue(verify.is_exception((('P', 2), ('C', 5))))
        self.assertFalse(verify.is_exception((('P', 2), ('C', 7))))

    def test_forbidden_triangle_has_no_allowed_edge(self):
        vertices = [0, 1, 2]
        forbidden = {(0, 1), (0, 2), (1, 2)}
        self.assertEqual(verify.maximum_allowed_matching(vertices, forbidden), [])

    def test_complement_chromatic_boundary(self):
        self.assertEqual(verify.complement_chromatic_number((('C', 3),)), 1)
        self.assertEqual(verify.complement_chromatic_number((('C', 5),)), 3)
        self.assertEqual(
            verify.complement_chromatic_number((('P', 3), ('C', 5))), 5
        )

    def test_mutated_branch_fails_connectivity(self):
        h_adj, _ = verify.build_graph((('P', 4),))
        self.assertFalse(verify.verify_minor(h_adj, [{0}, {1, 2}]))

    def test_mutated_branch_fails_cross_adjacency(self):
        h_adj, _ = verify.build_graph((('C', 4),))
        self.assertFalse(verify.verify_minor(h_adj, [{0}, {1, 3}]))

    def test_exception_equality_is_rejected(self):
        for core in verify.EXCEPTION_CORES:
            with self.subTest(core=core):
                self.assertFalse(verify.equality_model_exists(core))

    def test_nonexception_certificates(self):
        for sig in [
            (('C', 5),),
            (('C', 6),),
            (('P', 2), ('C', 7)),
            (('P', 1), ('P', 4), ('C', 3)),
        ]:
            sig = verify.normalized(sig)
            h_adj, _ = verify.build_graph(sig)
            branches = verify.certificate(sig)
            expected = (len(h_adj) + verify.independence_number(sig)) // 2
            self.assertEqual(len(branches), expected)
            self.assertTrue(verify.verify_minor(h_adj, branches))


if __name__ == '__main__':
    unittest.main()
