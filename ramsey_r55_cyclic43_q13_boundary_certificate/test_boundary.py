#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

import generate_boundary as generator
import verify_certificate as verifier


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "objective-twelve-component-fast.json"
CERTIFICATE = HERE / "boundary_certificate.json"


class BoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        document = json.loads(SOURCE.read_text())
        cls.states = [
            generator.state_from_edges(edges)
            for edges in document["complete_additional_objective_12_rotation_representatives"]
        ]

    def test_fixed_input(self) -> None:
        self.assertEqual(
            generator.sha256(SOURCE),
            "4803b2e40dba06c0f82c3d23cbd5ae0a9127da0db24e5655971fff179fb68ec3",
        )
        self.assertEqual(len(self.states), 238)
        self.assertEqual(len(set(self.states)), 238)

    def test_seed_is_regular_and_colours_partition_edges(self) -> None:
        red, blue = generator.adjacency(generator.SEED_RED_MASK)
        self.assertEqual({row.bit_count() for row in red}, {22})
        self.assertEqual({row.bit_count() for row in blue}, {20})
        for vertex in range(generator.ORDER):
            self.assertEqual(red[vertex] & blue[vertex], 0)
            self.assertEqual(
                red[vertex] | blue[vertex],
                generator.ALL_VERTICES ^ (1 << vertex),
            )

    def test_two_canonicalizers_agree_and_are_rotation_invariant(self) -> None:
        for state in self.states[::47]:
            expected = generator.canonical_state(state)
            self.assertEqual(verifier.canonical(state), expected)
            for shift in (0, 1, 7, 21, 42):
                self.assertEqual(
                    generator.canonical_state(generator.rotate_state(state, shift)),
                    expected,
                )

    def test_triangle_algorithms_agree(self) -> None:
        for state in self.states[::79]:
            red, blue = generator.adjacency(generator.SEED_RED_MASK ^ state)
            for edge in range(0, generator.EDGE_COUNT, 97):
                u, v = generator.EDGES[edge]
                for rows in (red, blue):
                    vertices = rows[u] & rows[v]
                    self.assertEqual(
                        generator.triangle_count(rows, vertices),
                        verifier.explicit_triangle_count(list(rows), vertices),
                    )

    def test_flip_delta_against_direct_objective(self) -> None:
        for state in self.states[::119]:
            red, blue = generator.adjacency(generator.SEED_RED_MASK ^ state)
            objective = generator.clique_count(red, 5) + generator.clique_count(blue, 5)
            self.assertEqual(objective, 12)
            for edge in (0, 42, 251, 509, 902):
                u, v = generator.EDGES[edge]
                r = generator.triangle_count(red, red[u] & red[v])
                b = generator.triangle_count(blue, blue[u] & blue[v])
                predicted = objective - r + b if ((red[u] >> v) & 1) else objective + r - b
                flipped_red, flipped_blue = generator.adjacency(
                    generator.SEED_RED_MASK ^ state ^ (1 << edge)
                )
                direct = generator.clique_count(flipped_red, 5) + generator.clique_count(
                    flipped_blue, 5
                )
                self.assertEqual(predicted, direct)

    def test_certificate_headline_claims(self) -> None:
        certificate = json.loads(CERTIFICATE.read_text())
        claims = certificate["claims"]
        self.assertEqual(claims["source_count"], 238)
        self.assertEqual(claims["raw_incidences"], 1924)
        self.assertEqual(claims["distinct_source_target_pairs"], 1923)
        self.assertEqual(claims["distinct_targets"], 1785)
        self.assertEqual(claims["pair_multiplicity_histogram"], {"1": 1922, "2": 1})
        self.assertEqual(claims["bipartite_component_count"], 164)
        self.assertEqual(claims["simple_cycle_rank"], 64)
        self.assertEqual(claims["multigraph_cycle_rank"], 65)
        self.assertEqual(Counter(row[2] for row in certificate["incidences"]), {1: 1922, 2: 1})


if __name__ == "__main__":
    unittest.main()
