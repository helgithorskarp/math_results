#!/usr/bin/env python3
"""Focused regression tests for the medium-support q=13 closure."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

import generate_closure as fast
import verify_closure as independent


HERE = Path(__file__).resolve().parent
CERTIFICATE = json.loads((HERE / "closure_certificate.json").read_text())
MEMBERSHIP = json.loads((HERE / "primary_membership.json").read_text())


def load_engine(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fast_engine = fast.load_boundary_engine()
        cls.slow_engine = independent.load_independent_engine()
        cls.states = [cls.slow_engine.pack(item) for item in CERTIFICATE["q13_states"]]

    def test_exact_headline(self):
        claims = CERTIFICATE["claims"]
        self.assertEqual(claims["input_seed_count"], 386)
        self.assertEqual(claims["state_count"], 6279)
        self.assertEqual(claims["component_count"], 33)
        self.assertEqual(claims["simple_internal_edges"], 12720)
        self.assertEqual(claims["simple_cycle_rank"], 6474)
        self.assertEqual(claims["support_signature_histogram"], {
            "16,16": 4454,
            "5,16": 574,
            "5,16,16": 1251,
        })

    def test_parent_seed_set(self):
        parent_path = HERE.parent / "ramsey_r55_cyclic43_q13_boundary_certificate" / "boundary_certificate.json"
        self.assertEqual(independent.digest(parent_path), independent.EXPECTED_BOUNDARY_SHA256)
        parent = json.loads(parent_path.read_text())
        expected = {
            self.slow_engine.pack(item)
            for item in parent["target_states"]
            if self.slow_engine.support(self.slow_engine.pack(item)) in independent.SEED_SIGNATURES
        }
        actual = {self.slow_engine.pack(item) for item in CERTIFICATE["seed_states"]}
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 386)

    def test_algorithms_agree_on_samples(self):
        for state in (self.states[0], self.states[1234], self.states[-1]):
            self.assertEqual(
                self.fast_engine.canonical_state(state),
                independent.canonical_state(self.slow_engine, state),
            )
            self.assertEqual(
                fast.reflected_state(self.fast_engine, state),
                independent.reflected_state(self.slow_engine, state),
            )
            objective, moves = fast.objective_and_moves(self.fast_engine, state)
            red, blue = self.slow_engine.color_rows(state)
            direct = self.slow_engine.count_cliques(red, 5) + self.slow_engine.count_cliques(blue, 5)
            self.assertEqual(objective, direct)
            self.assertEqual(objective, 13)
            for edge in (0, 137, 451, 902):
                u, v = self.slow_engine.EDGES[edge]
                r = independent.edge_common_triangle_count(red, red[u] & red[v])
                b = independent.edge_common_triangle_count(blue, blue[u] & blue[v])
                after = direct - r + b if (red[u] >> v) & 1 else direct + r - b
                self.assertEqual(moves[edge][1], after)

    def test_sublevel_payload(self):
        low = CERTIFICATE["sublevel_endpoint_states_by_objective"]
        self.assertEqual({objective: len(entries) for objective, entries in low.items()}, {
            "7": 229,
            "8": 6,
            "9": 245,
            "10": 8218,
            "11": 1084,
            "12": 1431,
        })
        for objective, entries in low.items():
            states = [self.slow_engine.pack(item) for item in entries]
            self.assertEqual(states, sorted(set(states), key=self.slow_engine.words))
            for state in (states[0], states[len(states) // 2], states[-1]):
                red, blue = self.slow_engine.color_rows(state)
                self.assertEqual(
                    self.slow_engine.count_cliques(red, 5)
                    + self.slow_engine.count_cliques(blue, 5),
                    int(objective),
                )

    def test_reflection_and_primary_membership_summaries(self):
        claims = CERTIFICATE["claims"]
        self.assertEqual(claims["reflection_fixed_component_count"], 1)
        self.assertEqual(claims["reflection_fixed_state_count"], 11)
        self.assertEqual(claims["dihedral_state_orbit_count"], 3145)
        self.assertEqual(MEMBERSHIP["closure_certificate_sha256"], independent.digest(HERE / "closure_certificate.json"))
        self.assertEqual(
            {objective: layer["endpoint_count"] for objective, layer in MEMBERSHIP["layers"].items()},
            {"7": 229, "8": 6, "9": 245, "10": 8218},
        )
        self.assertTrue(all(layer["all_endpoints_present"] for layer in MEMBERSHIP["layers"].values()))


if __name__ == "__main__":
    unittest.main()
