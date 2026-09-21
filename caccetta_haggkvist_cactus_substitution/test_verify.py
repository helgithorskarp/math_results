import unittest

import verify


class DefinitionTests(unittest.TestCase):
    def test_triangle_is_cactus(self) -> None:
        self.assertTrue(verify.is_cactus(3, ((0, 1), (1, 2), (0, 2))))

    def test_diamond_is_not_cactus(self) -> None:
        self.assertFalse(
            verify.is_cactus(4, ((0, 1), (1, 2), (2, 0), (0, 3), (3, 2)))
        )

    def test_directed_cycle_is_out_packing(self) -> None:
        arcs = ((0, 1), (1, 2), (2, 3), (3, 0))
        self.assertTrue(verify.is_out_packing(4, arcs, (0, 1, 2, 3)))

    def test_collision_is_rejected(self) -> None:
        arcs = ((0, 1), (1, 2), (2, 0), (0, 3), (1, 3))
        self.assertFalse(verify.is_out_packing(4, arcs, (0, 1, 2)))

    def test_wheel_boundary_has_no_certificate(self) -> None:
        arcs = (
            (1, 0), (0, 3), (3, 2), (2, 1),
            (0, 4), (2, 4), (4, 1), (4, 3),
        )
        cycles = verify.directed_cycles(5, arcs)
        self.assertTrue(cycles)
        self.assertFalse(any(verify.is_out_packing(5, arcs, c) for c in cycles))


if __name__ == "__main__":
    unittest.main()
