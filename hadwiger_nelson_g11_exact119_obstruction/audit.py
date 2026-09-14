#!/usr/bin/env python3
"""Alternate-basis audit of the exact-119-image G_11 obstruction.

This imports neither producer nor verifier.  Unlike the main certificate path,
it enumerates every one-collision four-cycle in reverse canonical order and
constructs a fresh rank basis before testing all second contractions.
"""
import argparse
from itertools import combinations
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ONE = HERE.parent / "hadwiger_nelson_g11_one_collision"
CERTIFICATE = HERE / "certificate.json"
EXPECTED = HERE / "AUDIT_EXPECTED.json"
Q = 11


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def graph():
    points = [(x, y) for x in range(Q) for y in range(Q)]
    edges = []
    for u in range(121):
        x, y = points[u]
        for v in range(u + 1, 121):
            a, b = points[v]
            if ((x - a) * (x - a) + (y - b) * (y - b)) % Q == 1:
                edges.append((u, v))
    return points, edges


def fold_first(edges, identified):
    raw = [0 if v == identified else v for v in range(121)]
    labels = {value: i for i, value in enumerate(dict.fromkeys(raw))}
    mapping = [labels[value] for value in raw]
    answer = set()
    for u, v in edges:
        a, b = mapping[u], mapping[v]
        need(a != b, "first fold loop")
        answer.add(tuple(sorted((a, b))))
    return sorted(answer)


def neighborhoods(order, edges):
    adj = [set() for _ in range(order)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def add_to_basis(basis, row):
    while row:
        pivot = row.bit_length() - 1
        if pivot not in basis:
            basis[pivot] = row
            return True
        row ^= basis[pivot]
    return False


def fresh_cycle_basis(order, edges):
    adj = neighborhoods(order, edges)
    witnesses = {}
    for a, c in combinations(range(order), 2):
        for b, d in combinations(sorted(adj[a] & adj[c]), 2):
            key = tuple(sorted(((a, c), (b, d))))
            witnesses.setdefault(key, (a, b, c, d))
    basis = {}
    selected = []
    for key in sorted(witnesses, reverse=True):
        cycle = witnesses[key]
        row = sum(1 << v for v in cycle)
        if add_to_basis(basis, row):
            selected.append(cycle)
    return adj, selected, len(witnesses)


def collapse_vertex(v, lo, hi):
    if v == hi:
        v = lo
    return v - (v > hi)


def collapsed_basis_rank(cycles, u, v):
    lo, hi = sorted((u, v))
    basis = {}
    for cycle in cycles:
        image = [collapse_vertex(x, lo, hi) for x in cycle]
        if len(set(image)) == 4:
            add_to_basis(basis, sum(1 << x for x in image))
    return len(basis)


def collapsed_edges(edges, u, v):
    lo, hi = sorted((u, v))
    answer = set()
    for a, b in edges:
        x = collapse_vertex(a, lo, hi)
        y = collapse_vertex(b, lo, hi)
        need(x != y, "second fold loop")
        answer.add(tuple(sorted((x, y))))
    return sorted(answer)


def digest_line(shell, shape, u, v, compatible):
    return (json.dumps([shell, shape, u, v, 118, compatible],
                       separators=(",", ":")) + "\n").encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(CERTIFICATE.read_text())
    predecessor = json.loads((ONE / "certificate.json").read_text())
    cases = {case["norm"]: case for case in predecessor["cases"]}
    points, source_edges = graph()
    need(len(points) == 121 and len(source_edges) == 726, "source census")
    stream = hashlib.sha256()
    counts = {"triple": 0, "two_pairs": 0, "fallback": 0,
              "compatible": 0, "one_collision_cycles": 0}
    for shell in range(2, 11):
        case = cases[shell]
        x, y = case["representative"]
        first_edges = fold_first(source_edges, x * Q + y)
        adj, basis_cycles, cycle_count = fresh_cycle_basis(120, first_edges)
        need(len(basis_cycles) == 119, "alternate one-collision rank")
        counts["one_collision_cycles"] += cycle_count
        colours = case["five_colouring"]

        def event(shape, u, v):
            rank = collapsed_basis_rank(basis_cycles, u, v)
            if rank < 118:
                counts["fallback"] += 1
                final_edges = collapsed_edges(first_edges, u, v)
                _, final_basis, _ = fresh_cycle_basis(119, final_edges)
                rank = len(final_basis)
            need(rank == 118, "alternate basis found surviving event")
            compatible = colours[u] == colours[v]
            counts["compatible"] += int(compatible)
            counts[shape] += 1
            stream.update(digest_line(shell, shape, u, v, compatible))

        for third in range(1, 120):
            if third not in adj[0]:
                event("triple", 0, third)
        for u, v in combinations(range(1, 120), 2):
            if v not in adj[u]:
                event("two_pairs", u, v)
    need(counts["triple"] == certificate["events_by_fibre_shape"]["triple"],
         "triple count")
    need(counts["two_pairs"] == certificate["events_by_fibre_shape"]["two_pairs"],
         "two-pair count")
    need(counts["compatible"] == certificate["five_colour_compatible_normalizations"],
         "compatible count")
    need(stream.hexdigest() == certificate["event_stream_sha256"], "event stream")
    result = {
        "verified": True,
        "alternate_one_collision_basis": True,
        "one_collision_cycles_enumerated": counts["one_collision_cycles"],
        "normalized_events_checked": counts["triple"] + counts["two_pairs"],
        "alternate_basis_fallbacks": counts["fallback"],
        "five_colour_compatible_normalizations": counts["compatible"],
        "all_final_ranks_mod_2": [118],
        "exactly_119_images_excluded": True,
        "event_stream_sha256": stream.hexdigest(),
    }
    if args.check_expected:
        need(result == json.loads(EXPECTED.read_text()), "audit expected result")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
