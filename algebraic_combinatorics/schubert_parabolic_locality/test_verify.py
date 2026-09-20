from __future__ import annotations

import unittest

import verify


class ParabolicLocalityTests(unittest.TestCase):
    def test_two_component_example(self) -> None:
        w = (0, 2, 1, 4, 3)  # 13254
        self.assertEqual(verify.coxeter_support(w), (2, 4))
        components = verify.parabolic_components(w)
        self.assertEqual(len(components), 2)
        self.assertEqual(
            [verify.transition_upsilon(c) for c in components], [2, 4]
        )
        self.assertEqual(verify.transition_upsilon(w), 8)
        self.assertEqual(verify.transition_upsilon(verify.inflate_identity(w, 2)), 6720)

    def test_absolute_labels_are_essential(self) -> None:
        # Standardizing both transposition factors would incorrectly give 1*1.
        local_transposition = (1, 0)
        self.assertEqual(verify.transition_upsilon(local_transposition), 1)
        w = (0, 2, 1, 4, 3)
        embedded_values = [
            verify.transition_upsilon(c) for c in verify.parabolic_components(w)
        ]
        self.assertEqual(embedded_values, [2, 4])

    def test_inflation_is_multiplicative_on_components(self) -> None:
        w = (0, 2, 1, 4, 3, 6, 5)
        verify.verify_component_factorization(w, 3)

    def test_grassmannian_shape_scaling(self) -> None:
        w = (0, 1, 3, 2)
        self.assertEqual(verify.grassmannian_partition(w), (1, 0, 0))
        image = verify.inflate_identity(w, 3)
        self.assertEqual(
            verify.grassmannian_partition(image),
            (3, 3, 3, 0, 0, 0, 0, 0, 0),
        )
        verify.verify_grassmannian(w, 3)

    def test_macdonald_and_transition_differently(self) -> None:
        w = (2, 0, 4, 1, 3)
        self.assertEqual(verify.transition_upsilon(w), verify.macdonald_upsilon(w))


if __name__ == "__main__":
    unittest.main()
