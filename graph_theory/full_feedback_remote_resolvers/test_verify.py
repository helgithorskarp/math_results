import unittest

import verify


class RemoteResolverTests(unittest.TestCase):
    def test_cycle_classification_prefix(self):
        observed = [n for n in range(3, 21) if verify.remote_resolvers(verify.cycle(n))]
        self.assertEqual(observed, [3, 5])

    def test_c5_signatures(self):
        signatures = verify.remote_signatures(verify.cycle(5), 0)
        self.assertEqual(
            signatures,
            {0: frozenset({1, 4}), 2: frozenset({1}), 3: frozenset({4})},
        )

    def test_even_cycle_antipodal_collision(self):
        signatures = verify.remote_signatures(verify.cycle(8), 0)
        self.assertEqual(signatures[0], signatures[4])

    def test_nonuniform_c5_strategy(self):
        graph = verify.cycle(5)
        for p in range(5):
            verify.audit_remote_resolver_strategy(graph, (2, 3, 4, 2, 3), p)

    def test_first_probe_criterion_both_directions(self):
        self.assertTrue(
            verify.first_probe_identifies_modules(verify.cycle(5), (2,) * 5, 0)
        )
        self.assertFalse(
            verify.first_probe_identifies_modules(verify.cycle(6), (2,) * 6, 0)
        )

    def test_malformed_blowup(self):
        with self.assertRaises(ValueError):
            verify.independent_blowup(verify.cycle(5), (2, 2, 2, 2, 1))

    def test_c5_base_audit(self):
        verify.audit_c5_base()


if __name__ == "__main__":
    unittest.main()
