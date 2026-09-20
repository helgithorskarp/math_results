#!/usr/bin/env python3

import unittest

import verify


class StableTransitivityTests(unittest.TestCase):
    def test_order_profile(self) -> None:
        self.assertEqual(verify.order_profile((0, 1, 2)), (1, 1, 1))
        self.assertEqual(verify.order_profile((2, 1, 0)), (0, 0, 0))

    def test_small_stable_numbers(self) -> None:
        transitive = (1, 1, 1)
        directed_triangle = (1, 0, 1)  # 0->1->2->0
        self.assertEqual(verify.stable_number(3, 1, transitive), 0)
        self.assertEqual(verify.stable_number(3, 1, directed_triangle), 1)
        self.assertEqual(verify.stable_number(3, 2, (2, 0, 2)), 2)

    def test_substitution(self) -> None:
        quotient = (1, 0, 1)
        singleton = ()
        expanded = verify.substitute(quotient, (singleton,) * 3, (1, 1, 1), 1)
        self.assertEqual(expanded, quotient)

        # Ordinal sum of a directed triangle and one singleton.
        expanded = verify.substitute(
            (1,),
            (quotient, ()),
            (3, 1),
            1,
        )
        self.assertEqual(verify.stable_number(4, 1, expanded), 1)

    def test_support_components(self) -> None:
        triangle = (1, 0, 1)
        expanded = verify.substitute((1,), (triangle, triangle), (3, 3), 1)
        self.assertEqual(verify.support_sccs(expanded, 6, 1), ((0, 1, 2), (3, 4, 5)))


if __name__ == "__main__":
    unittest.main()
