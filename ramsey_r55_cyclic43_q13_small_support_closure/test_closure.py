#!/usr/bin/env python3
"""Focused regression tests for the q=13 small-support closure."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

import generate_closure as fast
import verify_closure as independent


HERE = Path(__file__).resolve().parent
CERTIFICATE = json.loads((HERE / "closure_certificate.json").read_text())


def load_engine():
    source = HERE.parent / "ramsey_r55_cyclic43_q13_boundary_certificate" / "generate_boundary.py"
    spec = importlib.util.spec_from_file_location("test_boundary_engine", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = load_engine()
        cls.states = [independent.pack(item) for item in CERTIFICATE["q13_states"]]

    def test_exact_headline(self):
        claims = CERTIFICATE["claims"]
        self.assertEqual(claims["state_count"], 150)
        self.assertEqual(claims["component_size_histogram"], {"6": 2, "10": 2, "59": 2})
        self.assertEqual(claims["simple_internal_edges"], 228)
        self.assertEqual(claims["simple_cycle_rank"], 84)
        self.assertEqual(claims["reflection_component_pairs"], [[0, 3], [1, 4], [2, 5]])

    def test_two_canonicalizers_agree(self):
        for state in self.states:
            self.assertEqual(self.engine.canonical_state(state), independent.canonical(state))

    def test_two_reflections_agree(self):
        state_set = set(self.states)
        for state in self.states:
            left = fast.reflected_state(self.engine, state)
            right = independent.reflected(state)
            self.assertEqual(left, right)
            self.assertIn(left, state_set)

    def test_objective_and_selected_deltas(self):
        for state in (self.states[0], self.states[29], self.states[-1]):
            fast_objective, fast_moves = fast.objective_and_moves(self.engine, state)
            red, blue = independent.color_rows(state)
            slow_objective = independent.count_cliques(red, 5) + independent.count_cliques(blue, 5)
            self.assertEqual(fast_objective, slow_objective)
            self.assertEqual(fast_objective, 13)
            for edge in (0, 137, 451, 902):
                u, v = independent.EDGES[edge]
                red_extensions = independent.explicit_triangles(red, red[u] & red[v])
                blue_extensions = independent.explicit_triangles(blue, blue[u] & blue[v])
                expected = (
                    slow_objective - red_extensions + blue_extensions
                    if (red[u] >> v) & 1
                    else slow_objective + red_extensions - blue_extensions
                )
                self.assertEqual(fast_moves[edge][1], expected)

    def test_sublevel_endpoint_payload(self):
        low = CERTIFICATE["sublevel_endpoint_states_by_objective"]
        self.assertEqual({key: len(value) for key, value in low.items()}, {
            "6": 8,
            "8": 16,
            "10": 20,
            "11": 52,
            "12": 178,
        })
        for objective, entries in low.items():
            states = [independent.pack(item) for item in entries]
            self.assertEqual(states, sorted(set(states), key=independent.words))
            for state in states:
                red, blue = independent.color_rows(state)
                self.assertEqual(
                    independent.count_cliques(red, 5) + independent.count_cliques(blue, 5),
                    int(objective),
                )


if __name__ == "__main__":
    unittest.main()
