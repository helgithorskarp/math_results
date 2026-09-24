#!/usr/bin/env python3
"""Independently check Liu's small lexicographic FC decision tree.

The flow oracle supplies candidate arc flows; Python integers check every
capacity and conservation equation. Its status/optimal objective is not a
mathematical certificate. See PROOF.md for the cut bound and tree semantics.
"""
import argparse
import hashlib
import itertools
import json
import operator
from pathlib import Path

from ortools.graph.python import max_flow

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify_flow(arcs, values, vertices, source, sink, threshold):
    require(len(values) == len(arcs), "Flow has wrong length")
    balance = [0] * vertices
    for (a, b, capacity), raw in zip(arcs, values):
        value = operator.index(raw)  # Reject floats; use exact Python integers.
        require(0 <= value <= capacity, "Flow violates an arc capacity")
        balance[a] -= value
        balance[b] += value
    require(all(balance[i] == 0 for i in range(vertices) if i not in (source, sink)),
            "Flow violates conservation")
    require(balance[sink] == -balance[source] >= threshold, "Insufficient certified flow")
    return balance[sink]


def extend(present, seed, generators):
    """Generic queue closure, different from the upstream closed-form update."""
    result = set(present)
    todo = [seed]
    while todo:
        a = todo.pop()
        if a in result:
            continue
        todo.extend(a | b for b in result if (a | b) not in result)
        todo.extend(a | b for b in generators if (a | b) not in result)
        result.add(a)
    return frozenset(result)


class TreeChecker:
    def __init__(self, n, weights, generators):
        require(1 <= n <= 9 and len(weights) == n, "Bad dimension")
        require(all(type(w) is int and w >= 0 for w in weights) and sum(weights) > 0,
                "Bad weights")
        self.n, self.N = n, 1 << n
        self.weights = weights
        self.A = frozenset(generators)
        require(len(self.A) == len(generators) and all(0 <= a < self.N for a in self.A),
                "Bad generators")
        self.q = [2 * sum(weights[i] for i in range(n) if s >> i & 1) - sum(weights)
                  for s in range(self.N)]
        self.threshold = sum(-q for q in self.q if q < 0)
        self.capacity = 1 + sum(abs(q) for q in self.q)
        self.maps = []
        for p in itertools.permutations(range(n)):
            if any(weights[i] != weights[p[i]] for i in range(n)):
                continue
            mapping = [sum(1 << p[i] for i in range(n) if s >> i & 1)
                       for s in range(self.N)]
            if {mapping[a] for a in self.A} == self.A:
                self.maps.append(mapping)
        self.nodes = self.leaves = self.conflicts = self.arcs_checked = 0
        self.max_depth = 0
        self.min_flow = None

    def leaf(self, present, absent):
        N, M = self.N, self.capacity
        arcs = []
        for s, q in enumerate(self.q):
            if q < 0:
                arcs.append((N, s, -q))
            if q > 0:
                arcs.append((s, N + 1, q))
        arcs.extend((N, s, M) for s in sorted(present))
        arcs.extend((s, N + 1, M) for s in sorted(absent))
        # All currently forced sets give necessary union implications. Use the
        # full forced family, rather than upstream's list of selected seeds.
        implications = {(s, s | a) for a in self.A | present for s in range(N)
                        if s | a != s}
        arcs.extend((a, b, M) for a, b in sorted(implications))
        solver = max_flow.SimpleMaxFlow()
        for a, b, capacity in arcs:
            solver.add_arc_with_capacity(a, b, capacity)
        require(solver.solve(N, N + 1) == solver.OPTIMAL, "Flow oracle did not finish")
        values = [solver.flow(i) for i in range(len(arcs))]
        value = verify_flow(arcs, values, N + 2, N, N + 1, self.threshold)
        self.arcs_checked += len(arcs)
        self.min_flow = value if self.min_flow is None else min(self.min_flow, value)

    def visit(self, tokens, present, absent, depth):
        try:
            tag = next(tokens)
        except StopIteration as exc:
            raise ValueError("Truncated tree") from exc
        self.nodes += 1
        self.max_depth = max(self.max_depth, depth)
        if tag == "C":
            require(bool(present & absent), "False conflict leaf")
            self.conflicts += 1
        elif tag == "L":
            self.leaf(present, absent)
            self.leaves += 1
        elif tag in ("B", "O"):
            try:
                s = int(next(tokens))
            except (ValueError, StopIteration) as exc:
                raise ValueError("Malformed branch") from exc
            require(0 <= s < self.N and s not in present | absent, "Invalid split")
            orbit = {s}
            if tag == "O":
                for p in self.maps:
                    if {p[x] for x in present} == present and {p[x] for x in absent} == absent:
                        orbit.add(p[s])
            self.visit(tokens, extend(present, s, self.A), absent, depth + 1)
            self.visit(tokens, present, absent | orbit, depth + 1)
        else:
            raise ValueError("Unknown tree token")

    def check(self, text):
        tokens = iter(text.split())
        self.visit(tokens, frozenset(), frozenset(), 0)
        require(next(tokens, None) is None, "Trailing tree tokens")
        return {"verified": True, "nodes": self.nodes, "leaves": self.leaves,
                "conflicts": self.conflicts, "max_depth": self.max_depth,
                "weighted_automorphisms": len(self.maps), "arc_values_checked": self.arcs_checked,
                "required_flow": self.threshold, "minimum_certified_flow": self.min_flow}


def controls():
    arcs = [(0, 1, 2), (1, 2, 2)]
    require(verify_flow(arcs, [2, 2], 3, 0, 2, 2) == 2, "Valid flow rejected")
    for values in ([0, 0], [3, 3], [2, 1], [2.0, 2.0]):
        try:
            verify_flow(arcs, values, 3, 0, 2, 2)
        except (ValueError, TypeError):
            continue
        raise ValueError("Invalid flow accepted")
    # For generator {0,1,2} and unit weights, {empty,0,1,01,012} has share -1.
    # A claim that the root is already certified nonnegative must be rejected.
    for bad in ("L", "C", "O 0", "unknown"):
        try:
            TreeChecker(3, [1, 1, 1], [7]).check(bad)
        except ValueError:
            continue
        raise ValueError("Invalid tree accepted")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", type=Path, default=ROOT / "lex_positive.tree")
    args = ap.parse_args()
    controls()
    n = 8
    w = [6, 6, 4, 3, 3, 3, 4, 4]
    A = [15, 23, 39, 71, 135, 75, 139, 83, 147, 99, 163, 195]
    p = [0, 1, 4, 5, 6, 7, 2, 3]
    lex = [sum(1 << i for i in t) for t in itertools.islice(itertools.combinations(range(9), 4), 14)]
    require(len(set(p)) == 8 and all(0 <= i < 9 for i in p), "Invalid embedding")
    require({sum(1 << p[i] for i in range(n) if a >> i & 1) for a in A} <= set(lex),
            "Positive configuration does not embed in the lex segment")
    tree = args.tree.read_bytes()
    result = TreeChecker(n, w, A).check(tree.decode())
    result.update(tree_sha256=hashlib.sha256(tree).hexdigest(),
                  lex14=lex, flow_negative_controls=4, tree_negative_controls=4)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
