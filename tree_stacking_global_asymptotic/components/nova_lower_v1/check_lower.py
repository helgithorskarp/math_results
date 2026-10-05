#!/usr/bin/env python3
"""Bounded exact author controls for the eventual all-order lower component.

Run with CPython >=3.11, standard library only. No predecessor code/data import.
The infinite statement is proved in PROOF.md at its explicit primary inputs.
"""

from collections import deque
from fractions import Fraction
from hashlib import sha256
import json
from math import comb
import platform
import resource
import sys
import time


def literal_tree(d, e, t):
    assert min(d, e, t) >= 1
    adjacency = [[] for _ in range(t + 1)]

    def edge(a, b):
        adjacency[a].append(b)
        adjacency[b].append(a)

    def vertex(parent):
        v = len(adjacency)
        adjacency.append([])
        edge(parent, v)
        return v

    for v in range(t):
        edge(v, v + 1)
    siblings = [vertex(0) for _ in range(d)]
    arms, tips = [], []
    for _ in range(e):
        a = vertex(t)
        arms.append(a)
        tips.append(vertex(a))
    assert len(adjacency) == d + 2 * e + t + 1
    assert sum(map(len, adjacency)) == 2 * (len(adjacency) - 1)
    return adjacency, siblings, arms, tips


def all_potentials(adjacency):
    """Direct BFS ambient degree-distance definition, not closed potentials."""
    values = []
    n = len(adjacency)
    core = [v for v in range(n) if len(adjacency[v]) > 1]
    for root in range(n):
        distances = [-1] * n
        distances[root] = 0
        todo = deque([root])
        while todo:
            v = todo.popleft()
            for u in adjacency[v]:
                if distances[u] < 0:
                    distances[u] = distances[v] + 1
                    todo.append(u)
        assert all(x >= 0 for x in distances)
        values.append(sum(len(adjacency[u]) << distances[u] for u in core))
    return values


def rooted_order(adjacency):
    parents = [-2] * len(adjacency)
    parents[0] = -1
    order = [0]
    for v in order:
        for u in adjacency[v]:
            if u == parents[v]:
                continue
            assert parents[u] == -2
            parents[u] = v
            order.append(u)
    assert len(order) == len(adjacency)
    return parents, order


def structural_sums(adjacency):
    """Two iterative tree passes for every directed structural deficit."""
    parents, order = rooted_order(adjacency)
    upwards = [0] * len(adjacency)
    downwards = [0] * len(adjacency)
    totals = [0] * len(adjacency)
    for v in reversed(order[1:]):
        childsum = sum(upwards[u] for u in adjacency[v] if u != parents[v])
        upwards[v] = 1 if len(adjacency[v]) == 1 else 3 + 2 * childsum
    for v in order:
        total = downwards[v] + sum(
            upwards[u] for u in adjacency[v] if u != parents[v]
        )
        totals[v] = total
        for u in adjacency[v]:
            if u != parents[v]:
                downwards[u] = (
                    1 if len(adjacency[v]) == 1 else 3 + 2 * (total - upwards[u])
                )
    return totals


def transfer(value):
    if value <= 1:
        return 2 * value - 3
    if value % 2 == 0:
        return value // 2
    return (value - 3) // 2


def all_scores(adjacency, piles):
    """Iterative occupied/EMPTY-aware messages. None is distinct from zero."""
    assert len(piles) == len(adjacency) and all(c >= 0 for c in piles)
    parents, order = rooted_order(adjacency)
    upwards = [None] * len(adjacency)
    downwards = [None] * len(adjacency)
    scores = [0] * len(adjacency)
    for v in reversed(order[1:]):
        messages = [upwards[u] for u in adjacency[v] if u != parents[v]]
        occupied = piles[v] > 0 or any(x is not None for x in messages)
        if occupied:
            upwards[v] = transfer(piles[v] + sum(x for x in messages if x is not None))
    for v in order:
        children = [u for u in adjacency[v] if u != parents[v]]
        messages = [upwards[u] for u in children]
        total = piles[v] + sum(x for x in messages if x is not None)
        occupied_children = sum(x is not None for x in messages)
        if downwards[v] is not None:
            total += downwards[v]
        scores[v] = total
        for u in children:
            own = upwards[u]
            rest_occupied = (
                piles[v] > 0
                or downwards[v] is not None
                or occupied_children > int(own is not None)
            )
            if rest_occupied:
                downwards[u] = transfer(total - (own if own is not None else 0))
    return scores


def composition_controls(total, parts):
    assert total >= 0 and parts >= 1
    candidates = [[total] + [0] * (parts - 1)]
    candidates.append([0] * (parts - 1) + [total])
    q, r = divmod(total, parts)
    candidates.append([q + int(i < r) for i in range(parts)])
    if parts >= 2:
        candidates.append([total // 2, total - total // 2] + [0] * (parts - 2))
    seen = set()
    result = []
    for xs in candidates:
        assert len(xs) == parts and sum(xs) == total and min(xs) >= 0
        if tuple(xs) not in seen:
            result.append(xs)
            seen.add(tuple(xs))
    return result


def exact_integer_digest(value):
    assert value >= 0
    b = value.to_bytes(max(1, (value.bit_length() + 7) // 8), "big")
    return sha256(b).hexdigest()


def tree_control(d, e, t, expected_max_parent=None):
    adjacency, siblings, arms, tips = literal_tree(d, e, t)
    values = all_potentials(adjacency)
    degrees = [len(x) for x in adjacency]
    leaves = [v for v, degree in enumerate(degrees) if degree == 1]
    assert set(leaves) == set(siblings + tips)
    deficits = structural_sums(adjacency)
    assert deficits == [values[v] + int(degrees[v] == 1) for v in range(len(adjacency))]
    xp = values[0]
    xa = values[arms[0]]
    assert xp == d - 3 + (5 * e + 3) * (1 << t)
    assert all(values[a] == xa for a in arms)
    assert xa == (d + 3) * (1 << (t + 1)) + 10 * e - 12
    assert xp - xa == (5 * e - 2 * d - 3) * (1 << t) + d - 10 * e + 9
    maximum = max(values)
    maximum_vertices = [v for v, value in enumerate(values) if value == maximum]
    assert all(v in leaves for v in maximum_vertices)
    max_parents = sorted({adjacency[v][0] for v in maximum_vertices})
    if expected_max_parent == "p":
        assert max_parents == [0] and xp > xa
    elif expected_max_parent == "arms":
        assert max_parents == sorted(arms) and xp < xa
    elif expected_max_parent == "tie":
        assert max_parents == sorted([0] + arms) and xp == xa
    threshold = len(leaves) + maximum + 1
    zero_score_count = 0
    for xs in composition_controls(xp, d):
        piles = [0] * len(adjacency)
        for leaf in leaves:
            piles[leaf] = 1
        for leaf, x in zip(siblings, xs):
            piles[leaf] = 1 + 2 * x
        assert sum(piles) == len(leaves) + 2 * xp
        assert all(s == 0 for s in all_scores(adjacency, piles))
        assert (sum(piles) == threshold - 1) == (xp >= xa)
        zero_score_count += 1
    # EMPTY and occupied-zero branches differ: on K2, piles(0,0) give
    # both scores0, while piles(3,0) give scores(3,0) and are stackable.
    assert all_scores([[1], [0]], [0, 0]) == [0, 0]
    assert all_scores([[1], [0]], [3, 0]) == [3, 0]
    return {
        "n": len(adjacency), "d": d, "e": e, "t": t,
        "potential_p": str(xp), "potential_arm": str(xa),
        "max_parent_count": len(max_parents),
        "p_is_max_parent": 0 in max_parents,
        "core_height_p": t + 1, "graph_leaf_height_p": t + 2,
        "zero_score_configurations_checked": zero_score_count,
        "threshold_bits": threshold.bit_length(),
    }


def add_polynomial(left, right):
    result = dict(left)
    for term, coefficient in right.items():
        result[term] = result.get(term, 0) + coefficient
        if result[term] == 0:
            del result[term]
    return result


def scale_polynomial(poly, scalar):
    return {term: coefficient * scalar for term, coefficient in poly.items() if coefficient * scalar}


def multiply_polynomials(left, right):
    result = {}
    for (am, ass), a in left.items():
        for (bm, bs), b in right.items():
            term = am + bm, ass + bs
            result[term] = result.get(term, 0) + a * b
    return {term: coefficient for term, coefficient in result.items() if coefficient}


def audit_polynomial_identity():
    # Exact coefficient comparison in Z[m,s], not finite evaluation.
    n = {(1, 0): 18, (0, 1): 1, (0, 0): 1}
    r = {(1, 0): 5, (0, 0): 2}
    t_plus_one = {(1, 0): 9, (0, 1): 1, (0, 0): -6}
    exponent = multiply_polynomials(r, t_plus_one)
    lhs = scale_polynomial(exponent, 36)
    lhs = add_polynomial(lhs, scale_polynomial(multiply_polynomials(n, n), -5))
    lhs = add_polynomial(lhs, scale_polynomial(n, 45))
    rhs = {(1, 0): 198, (0, 0): -392, (0, 1): 107, (0, 2): -5}
    assert lhs == rhs
    return [[list(term), coefficient] for term, coefficient in sorted(lhs.items())]


def main():
    start = time.process_time()
    coefficient_record = audit_polynomial_identity()
    records = []
    # All eighteen residues for five separated m values. This is a bounded
    # control set, not all n>=37 or an exhaustive search of trees.
    sampled_m = [2, 3, 4, 10, 32]
    for m in sampled_m:
        for s in range(18):
            n = 18 * m + 1 + s
            assert divmod(n - 1, 18) == (m, s)
            d, e, t = 5 * m + 3, 2 * m + 2, 9 * m - 7 + s
            row = tree_control(d, e, t, "p")
            assert row["n"] == n
            xp, xa = int(row["potential_p"]), int(row["potential_arm"])
            assert xp - xa == (1 << t) - (15 * m + 8) > 0
            r = d - 1
            y = xp + r
            assert y == (10 * m + 13) * (1 << t) + 10 * m + 2
            assert y > r * (1 << (t + 1))
            count = comb(y, r)
            exponent = r * (t + 1)
            assert count > (1 << exponent)
            assert exponent - Fraction(5, 36) * n * n + Fraction(5, 4) * n > 0
            assert 36 * exponent - 5 * n * n + 45 * n == 198 * m - 392 + s * (107 - 5 * s)
            row.update({
                "m": m, "s": s, "lower_integer_exponent": exponent,
                "exact_count_bits": count.bit_length(),
                "exact_count_sha256_unsigned_big_endian": exact_integer_digest(count),
            })
            records.append(row)
    controls = [
        tree_control(1, 1, 1, "tie"),
        tree_control(1, 1, 2, "tie"),
        tree_control(2, 2, 1, "arms"),
        tree_control(8, 4, 4, "arms"),
        tree_control(8, 4, 5, "p"),
        tree_control(8, 4, 6, "p"),
    ]
    canonical = json.dumps({"records": records, "controls": controls, "polynomial_coefficients": coefficient_record}, sort_keys=True, separators=(",", ":")).encode()
    output = {
        "status": "AUTHOR_BOUNDED_EXACT_CONTROLS_PASS",
        "claim_status": "ordinary conditional proof in PROOF.md; awaits Rowan internal check",
        "domain": {"all_n_lower_start": 37, "C_minus": "5/4"},
        "sampled_m": sampled_m,
        "all_residues_s": [0, 17],
        "witness_trees_checked": len(records),
        "boundary_or_losing_parent_trees_checked": len(controls),
        "all_target_score_vectors_checked": sum(x["zero_score_configurations_checked"] for x in records + controls),
        "symbolic_polynomial_coefficients": coefficient_record,
        "deterministic_record_sha256": sha256(canonical).hexdigest(),
        "records": records,
        "controls": controls,
        "runtime": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "cpu_seconds": time.process_time() - start,
            "peak_rss_KiB_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "processes": 1,
            "native_threads": 1,
            "arithmetic": "integer/Fraction, no numerical logarithms",
            "command": "PYTHONDONTWRITEBYTECODE=1 python3 check_lower.py",
        },
        "trust": "BFS/score controls use the stated primary mathematical inputs; no raw legal-move oracle or infinite enumeration",
    }
    json.dump(output, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
