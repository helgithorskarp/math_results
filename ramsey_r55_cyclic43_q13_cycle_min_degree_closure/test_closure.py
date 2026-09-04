#!/usr/bin/env python3
"""Focused tests for the minimum-degree cycle-only closure."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import generate_closure as fast
import verify_closure as independent


HERE = Path(__file__).resolve().parent
CERTIFICATE = json.loads((HERE / "closure_certificate.json").read_text())
GROWTH = json.loads((HERE / "growth_10000.json").read_text())


class ClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fast_tools, cls.fast_engine = fast.load_fast_engine()
        cls.slow_tools, cls.slow_engine = independent.load_independent_tools()
        cls.states = [cls.slow_engine.pack(item) for item in CERTIFICATE["q13_states"]]

    def test_exact_headline(self):
        claims = CERTIFICATE["claims"]
        self.assertEqual(claims["parent_cycle_seed_count"], 1381)
        self.assertEqual(claims["input_seed_count"], 4)
        self.assertEqual(claims["state_count"], 36)
        self.assertEqual(claims["component_count"], 4)
        self.assertEqual(claims["component_size_histogram"], {"2": 2, "16": 2})
        self.assertEqual(claims["simple_internal_edges"], 54)
        self.assertEqual(claims["simple_cycle_rank"], 22)
        self.assertEqual(claims["support_signature_histogram"], {"cycle_only": 36})

    def test_degree_selection_census(self):
        claims = CERTIFICATE["claims"]
        histogram = claims["parent_cycle_seed_q13_degree_histogram"]
        self.assertEqual(sum(histogram.values()), 1381)
        self.assertEqual(histogram["1"], 2)
        self.assertEqual(histogram["2"], 2)
        self.assertEqual(claims["selected_seed_q13_degree_histogram"], {"1": 2, "2": 2})
        self.assertEqual(claims["parent_cycle_seeds_in_closure"], 8)
        self.assertEqual(
            claims["closure_parent_seed_q13_degree_histogram"],
            {"1": 2, "2": 2, "3": 2, "4": 2},
        )

    def test_algorithms_agree_on_samples(self):
        for state in (self.states[0], self.states[17], self.states[-1]):
            self.assertEqual(
                self.fast_engine.canonical_state(state),
                self.slow_tools.canonical_state(self.slow_engine, state),
            )
            objective, moves = self.fast_tools.objective_and_moves(self.fast_engine, state)
            red, blue = self.slow_engine.color_rows(state)
            direct = self.slow_engine.count_cliques(red, 5) + self.slow_engine.count_cliques(blue, 5)
            self.assertEqual(objective, direct)
            for edge in (0, 451, 902):
                u, v = self.slow_engine.EDGES[edge]
                r = self.slow_tools.edge_common_triangle_count(red, red[u] & red[v])
                b = self.slow_tools.edge_common_triangle_count(blue, blue[u] & blue[v])
                after = direct - r + b if (red[u] >> v) & 1 else direct + r - b
                self.assertEqual(moves[edge][1], after)

    def test_sublevel_payload_and_reflection(self):
        low = CERTIFICATE["sublevel_endpoint_states_by_objective"]
        self.assertEqual({objective: len(entries) for objective, entries in low.items()}, {
            "10": 6,
            "11": 22,
            "12": 74,
        })
        self.assertEqual(CERTIFICATE["claims"]["reflection_component_pairs"], [[0, 1], [2, 3]])
        self.assertEqual(CERTIFICATE["claims"]["reflection_fixed_state_count"], 0)
        for objective, entries in low.items():
            states = [self.slow_engine.pack(item) for item in entries]
            self.assertEqual(states, sorted(set(states), key=self.slow_engine.words))
            for state in (states[0], states[-1]):
                red, blue = self.slow_engine.color_rows(state)
                self.assertEqual(
                    self.slow_engine.count_cliques(red, 5)
                    + self.slow_engine.count_cliques(blue, 5),
                    int(objective),
                )

    def test_growth_prefix_obstruction(self):
        self.assertEqual(GROWTH["processing_cap"], 10000)
        self.assertEqual(GROWTH["processed_state_count"], 10000)
        self.assertEqual(GROWTH["reached_state_count"], 26651)
        self.assertEqual(GROWTH["unprocessed_queue_count"], 16651)
        self.assertFalse(GROWTH["closed"])
        self.assertEqual(GROWTH["directed_q13_incidences_from_processed"], 72335)
        self.assertEqual(GROWTH["reached_support_signature_histogram"], {"cycle_only": 26651})
        self.assertEqual(GROWTH["checkpoints"][-1]["processed"], 10000)
        self.assertEqual(GROWTH["checkpoints"][-1]["reached"], 26651)
        self.assertEqual(GROWTH["checkpoints"][-1]["queue"], 16651)
        for key in (
            "processed_sequence_sha256_words_le",
            "reached_sorted_sha256_words_le",
            "queue_sequence_sha256_words_le",
        ):
            self.assertEqual(len(GROWTH[key]), 64)


if __name__ == "__main__":
    unittest.main()
