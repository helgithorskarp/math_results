import unittest

from verify import (
    complement,
    direct_sum,
    j_value,
    left_down,
    left_up,
    right_down,
    right_up,
    skew_sum,
    verify_pair,
)


class DirectSumTests(unittest.TestCase):
    def test_endpoint_anchors(self):
        self.assertTrue(left_down((3, 2, 1, 5, 4)))
        self.assertTrue(right_down((2, 1, 5, 4, 3)))
        self.assertFalse(left_down((2, 4, 1, 3)))
        self.assertFalse(right_down((2, 4, 1, 3)))

    def test_junction_present(self):
        left, right = (1, 3, 2), (2, 1, 3)
        self.assertEqual(verify_pair(left, right)[0], 1)
        self.assertEqual(j_value(direct_sum(left, right)), j_value(left) + j_value(right) + 1)

    def test_junction_absent(self):
        block = (2, 4, 1, 3)
        self.assertEqual(verify_pair(block, block)[0], 0)
        self.assertEqual(j_value(direct_sum(block, block)), 4)

    def test_skew_duality(self):
        left, right = (2, 1, 3), (1, 3, 2)
        self.assertEqual(
            skew_sum(left, right),
            complement(direct_sum(complement(left), complement(right))),
        )
        expected = j_value(left) + j_value(right) + int(right_up(left) and left_up(right))
        self.assertEqual(j_value(skew_sum(left, right)), expected)

    def test_layered_recovery(self):
        layers = ((2, 1), (3, 2, 1), (1,))
        w = layers[0]
        for layer in layers[1:]:
            w = direct_sum(w, layer)
        self.assertEqual(j_value(w), len(w) - 1)


if __name__ == "__main__":
    unittest.main()

