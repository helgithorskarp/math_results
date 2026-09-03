#!/usr/bin/env python3

from __future__ import annotations

import unittest

import verify


class ConstructionTests(unittest.TestCase):
    def test_formula_values(self) -> None:
        expected = {2: 2, 3: 4, 4: 5, 5: 8, 6: 9, 7: 12, 8: 12}
        self.assertEqual(
            {n: verify.parameters(n)[2] for n in expected},
            expected,
        )

    def test_all_parity_and_exceptional_cases(self) -> None:
        for n in range(2, 21):
            with self.subTest(n=n):
                verify.verify_construction(n)
                verify.verify_shell_bound(n)

    def test_rejects_degenerate_parameter(self) -> None:
        with self.assertRaises(ValueError):
            verify.parameters(1)


if __name__ == "__main__":
    unittest.main()
