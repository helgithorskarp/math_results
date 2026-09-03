#!/usr/bin/env python3

import itertools
import unittest

from verify_certificates import (
    ClassCertificate,
    check_equation,
    is_transitive,
    order_matrix,
    relabel_mask,
    tournament_matrix,
)


class VerifierTests(unittest.TestCase):
    def test_transitive_and_cyclic_three_tournaments(self) -> None:
        self.assertTrue(is_transitive(tournament_matrix(0, 3)))
        self.assertFalse(is_transitive(tournament_matrix(2, 3)))

    def test_direct_cyclic_three_certificate(self) -> None:
        certificate = ClassCertificate(
            mask=2,
            orbit_size=2,
            m=1,
            x=(0, 2, 1),
            y=(0, 1, 2),
            z=(2, 0, 1),
        )
        check_equation(certificate, 3)

    def test_bad_order_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            order_matrix((0, 1, 1), 3)

    def test_three_vertex_orbits_partition_all_tournaments(self) -> None:
        permutations = list(itertools.permutations(range(3)))
        transitive_orbit = {relabel_mask(0, p, 3) for p in permutations}
        cyclic_orbit = {relabel_mask(2, p, 3) for p in permutations}
        self.assertEqual(len(transitive_orbit), 6)
        self.assertEqual(len(cyclic_orbit), 2)
        self.assertEqual(transitive_orbit | cyclic_orbit, set(range(8)))
        self.assertFalse(transitive_orbit & cyclic_orbit)


if __name__ == "__main__":
    unittest.main()
