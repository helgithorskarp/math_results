import unittest

from verify import (
    Witness,
    configuration,
    exception_family,
    theorem_witness,
    verify_witness,
)


class ThreeSingletonTests(unittest.TestCase):
    def test_small_boundary(self):
        for positions in ((1, 2, 3), (1, 2, 4), (2, 4, 6)):
            self.assertTrue(verify_witness(3, positions, theorem_witness(3, positions)))

    def test_all_three_exception_families(self):
        k = 12
        for positions in ((7, 11, 13), (7, 12, 13), (7, 12, 14)):
            self.assertIsNotNone(exception_family(k, positions))
            self.assertTrue(verify_witness(k, positions, theorem_witness(k, positions)))

    def test_reflection(self):
        k = 11
        order = 2 * k + 1
        positions = (4, 10, 12)
        reflected = tuple(sorted(order - x for x in positions))
        self.assertTrue(verify_witness(k, reflected, theorem_witness(k, reflected)))

    def test_malformed_inputs(self):
        with self.assertRaises(ValueError):
            configuration(2, (1, 2, 3))
        with self.assertRaises(ValueError):
            configuration(5, (1, 1, 2))
        self.assertFalse(verify_witness(5, (1, 2, 3), object()))

    def test_corrupted_witness(self):
        witness = theorem_witness(10, (3, 9, 11))
        bad = Witness(witness.cut, witness.left, witness.target, witness.score + 1)
        self.assertFalse(verify_witness(10, (3, 9, 11), bad))


if __name__ == "__main__":
    unittest.main()
