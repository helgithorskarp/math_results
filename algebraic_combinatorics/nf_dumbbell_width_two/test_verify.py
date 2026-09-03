import unittest

import verify


class NFWidthTwoTests(unittest.TestCase):
    def test_exceptional_isomorphism(self) -> None:
        verify.verify_exceptional_isomorphism()

    def test_all_symbolic_transitions_through_100(self) -> None:
        states, transitions = verify.verify_type_formula(100)
        self.assertEqual(states, transitions)
        self.assertGreater(states, 5000)

    def test_definition_level_through_7(self) -> None:
        states, facets = verify.verify_definition_level(7)
        self.assertGreater(states, 40)
        self.assertGreater(facets, 100)

    def test_wave_endpoints(self) -> None:
        for m in range(3, 30):
            b = m - 1
            self.assertEqual(
                verify.delta_types(verify.wave_types(b - 1, m), m),
                verify.wave_types(b - 2, m),
            )
            self.assertEqual(
                verify.delta_types(verify.wave_types(0, m), m),
                verify.initial_types(m),
            )


if __name__ == "__main__":
    unittest.main()
