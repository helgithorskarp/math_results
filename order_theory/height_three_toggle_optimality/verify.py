#!/usr/bin/env python3
"""Definition-level audits, independent of the component construction.

All prescribed incidence matrices with at most seven interior elements are
checked against exact BFS. Small weighted cases use Dijkstra. No floating
point, random input, solver, external catalogue, or third-party package.
"""

import argparse
from collections import Counter, deque
import hashlib
import heapq
import itertools
import json
from pathlib import Path

from compiler import compile_incidence, compile_poset


class AuditError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def incidence_order(m, rows):
    """Explicit set relation, including reflexivity and the two bounds."""
    a, n = len(rows), len(rows) + m + 2
    relation = {(v, v) for v in range(n)}
    relation.update((0, v) for v in range(n))
    relation.update((v, n - 1) for v in range(n))
    relation.update((i + 1, a + 1 + c) for i, row in enumerate(rows) for c in row)
    return [[(v, w) in relation for w in range(n)] for v in range(n)]


def game_data(order):
    """Generic Mobius recurrence and principal ideals; no incidence formulas."""
    n = len(order)
    tops = [v for v in range(n) if all(order[u][v] for u in range(n))]
    require(len(tops) == 1, "one top required")
    top = tops[0]
    mu = {top: 1}
    while len(mu) < n:
        ready = [v for v in range(n) if v not in mu
                 and all(w in mu for w in range(n) if w != v and order[v][w])]
        require(bool(ready), "not a poset")
        for v in ready:
            mu[v] = -sum(mu[w] for w in range(n) if w != v and order[v][w])
    ideals = {v: frozenset(u for u in range(n) if order[u][v]) for v in range(n)}
    return top, mu, ideals


def replay(order, word):
    top, mu, ideals = game_data(order)
    state, counts, signed = set(), Counter(), Counter()
    for step, v in enumerate(word):
        require(type(v) is int and v in ideals and v != top, f"bad move {step}")
        require(mu[v] != 0, f"zero-Mobius move {step}")
        ideal = ideals[v]
        require(not (state & ideal) or ideal <= state, f"mixed ideal at {step}")
        signed[v] += -1 if ideal <= state else 1
        state.symmetric_difference_update(ideal)
        counts[v] += 1
    require(state == set(range(len(order))) - {top}, "wrong final state")
    for v in range(len(order)):
        if v != top:
            require(signed[v] == -mu[v], "signed multiplicity mismatch")
            require(counts[v] == abs(mu[v]), "nonoptimal multiplicity")
    return mu


def shortest_cost(order, weights=None):
    """BFS / Dijkstra on all definitionally legal states, with bit masks.

    Unlike the compiler this can add or remove any permitted ideal at any
    time; it imposes neither sign coherence nor a component ordering.
    """
    top, mu, ideals = game_data(order)
    moves = [(v, sum(1 << u for u in ideals[v])) for v in ideals if v != top and mu[v]]
    goal = ((1 << len(order)) - 1) ^ (1 << top)
    distances = {0: 0}
    if weights is None:
        queue = deque([0])
        while queue:
            state = queue.popleft()
            if state == goal:
                return distances[state]
            for _, mask in moves:
                if state & mask in (0, mask):
                    next_state = state ^ mask
                    if next_state not in distances:
                        distances[next_state] = distances[state] + 1
                        queue.append(next_state)
    else:
        require(len(weights) == len(order) and all(type(w) is int and w >= 0 for w in weights),
                "nonnegative integer weights required by this audit")
        queue = [(0, 0)]
        while queue:
            cost, state = heapq.heappop(queue)
            if distances[state] != cost:
                continue
            if state == goal:
                return cost
            for v, mask in moves:
                if state & mask in (0, mask):
                    next_state, new_cost = state ^ mask, cost + weights[v]
                    if next_state not in distances or new_cost < distances[next_state]:
                        distances[next_state] = new_cost
                        heapq.heappush(queue, (new_cost, next_state))
    raise AuditError("unreachable goal")


def is_lattice(order):
    n = len(order)
    for v in range(n):
        for w in range(n):
            lower = [u for u in range(n) if order[u][v] and order[u][w]]
            upper = [u for u in range(n) if order[v][u] and order[w][u]]
            if sum(all(order[u][g] for u in lower) for g in lower) != 1:
                return False
            if sum(all(order[g][u] for u in upper) for g in upper) != 1:
                return False
    return True


def expect_rejection(function, *args):
    try:
        function(*args)
    except (ValueError, AuditError):
        return
    raise AuditError("invalid input/certificate was accepted")


def audit():
    digest = hashlib.sha256()
    cases, bfs_cases, weighted_cases, total_moves = 0, 0, 0, 0
    bottom_signs = Counter()
    for interior in range(1, 8):
        for m in range(1, interior + 1):
            a = interior - m
            subsets = [tuple(c for c in range(m) if mask & (1 << c))
                       for mask in range(1, 1 << m)]
            for rows in itertools.product(subsets, repeat=a):
                order = incidence_order(m, rows)
                word = compile_incidence(m, rows)
                mu = replay(order, word)
                optimum = shortest_cost(order)
                require(optimum == len(word), "BFS optimum mismatch")
                r = sum(len(row) - 1 for row in rows)
                require(len(word) == 2 * max(m - 1, r) + 1, "length formula mismatch")
                require(mu[0] == m - 1 - r, "bottom formula mismatch")
                if interior <= 5:
                    n = len(order)
                    for weights in ([((2 * v + 1) % 5) for v in range(n)],
                                    [17] + [(v % 3) for v in range(1, n)]):
                        observed = shortest_cost(order, weights)
                        require(observed == sum(weights[v] for v in word), "weighted optimum mismatch")
                        weighted_cases += 1
                bottom_signs[str((mu[0] > 0) - (mu[0] < 0))] += 1
                cases += 1
                bfs_cases += 1
                total_moves += len(word)
                digest.update((json.dumps([m, rows, word, optimum], separators=(",", ":")) + "\n").encode())

    # Named fixtures exercise arbitrary labels, high degrees, all bottom signs,
    # zero-Mobius atoms, and general posets that are not lattices.
    fano_rows = [tuple(c for c in range(7) if (v - c) % 7 in (0, 1, 3)) for v in range(7)]
    affine_lines = [{(x, (s * x + b) % 3) for x in range(3)}
                    for s in range(3) for b in range(3)]
    affine_lines += [{(b, y) for y in range(3)} for b in range(3)]
    affine_rows = [tuple(i for i, line in enumerate(affine_lines) if (x, y) in line)
                   for x in range(3) for y in range(3)]
    specifications = [
        ("crown_plus_isolated_zero_bottom", 4, [(0, 1), (1, 2), (2, 0)], True),
        ("two_crowns_plus_isolated", 7, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)], True),
        ("degree_one_atoms", 5, [(0,), (0, 1), (1, 2), (2, 0), (3,), (3,)], True),
        ("complete_incidence_3_by_3", 3, [(0, 1, 2)] * 3, False),
        ("fano_plane", 7, fano_rows, True),
        ("affine_plane_order_3", 12, affine_rows, True),
        ("fano_plus_eight_isolated", 15, fano_rows, True),
        ("fano_plus_twelve_isolated", 19, fano_rows, True),
    ]
    fixtures = []
    for name, m, rows, lattice in specifications:
        order = incidence_order(m, rows)
        word = compile_poset(order)
        mu = replay(order, word)
        require(is_lattice(order) == lattice, "fixture lattice status mismatch")
        # Reverse all labels, including top and bottom, before the generic API.
        n = len(order)
        reversed_order = [[order[n - 1 - v][n - 1 - w] for w in range(n)] for v in range(n)]
        renamed_word = compile_poset(reversed_order)
        replay(reversed_order, renamed_word)
        require(len(renamed_word) == len(word), "relabeling mismatch")
        fixtures.append({"name": name, "order": n, "lattice": lattice,
                         "bottom_mu": mu[0], "moves": len(word)})
    for n in range(1, 5):
        order = [[v <= w for w in range(n)] for v in range(n)]
        word = compile_poset(order)
        replay(order, word)
        require(len(word) == shortest_cost(order), "chain boundary optimum mismatch")
        fixtures.append({"name": f"chain_{n}", "order": n, "moves": len(word), "lattice": True})

    bad_orders = [[], [[1]], [[False]], [[True, True], [True, True]],
                  [[True, False], [False, True]],
                  [[True, True, False], [False, True, True], [False, False, True]],
                  [[v <= w for w in range(5)] for v in range(5)]]
    for order in bad_orders:
        expect_rejection(compile_poset, order)
    for m, rows in [(0, []), (1, [()]), (1, [(0, 0)]), (1, [(1,)])]:
        expect_rejection(compile_incidence, m, rows)
    order = incidence_order(4, [(0, 1), (1, 2), (2, 0)])
    word = compile_poset(order)
    expect_rejection(replay, order, [0] + word)  # forbidden zero-Mobius bottom
    expect_rejection(replay, order, word[:-1])  # incomplete certificate
    expect_rejection(replay, order, [4, 5])     # second ideal is mixed
    expect_rejection(replay, order, [len(order) - 1])  # forbidden top
    return {
        "status": "PASS", "incidence_matrices": cases,
        "max_interior_elements": 7, "bfs_optimum_checks": bfs_cases,
        "weighted_dijkstra_checks": weighted_cases,
        "compiled_moves_replayed": total_moves, "bottom_mu_sign_counts": dict(sorted(bottom_signs.items())),
        "entrywise_audit_sha256": digest.hexdigest(), "fixtures": fixtures,
        "relabeled_fixture_checks": len(specifications),
        "invalid_input_or_word_rejections": len(bad_orders) + 4 + 4,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-expected", action="store_true", help="regenerate the compact expected record")
    args = parser.parse_args()
    result = audit()
    path = Path(__file__).with_name("expected.json")
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_expected:
        path.write_text(rendered)
    else:
        require(json.loads(path.read_text()) == result, "expected record mismatch")
    print(rendered, end="")


if __name__ == "__main__":
    main()
