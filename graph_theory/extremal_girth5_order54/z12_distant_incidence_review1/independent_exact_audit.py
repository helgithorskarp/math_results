#!/usr/bin/env python3
"""Clean-room exact audit of the z=12, A<=3 order-54 reduction."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path


SIZES = (16, 26, 12)
DEGREES = (6, 7, 8)
CLASS_PAIRS = ((0, 1), (0, 2), (1, 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def local_types():
    result = []
    for degree in DEGREES:
        cls = degree - 6
        for n6 in range(degree + 1):
            for n7 in range(degree - n6 + 1):
                ns = (n6, n7, degree - n6 - n7)
                if sum(d * count for d, count in zip(DEGREES, ns)) > 53:
                    continue
                if any(ns[j] > SIZES[j] - int(j == cls) for j in range(3)):
                    continue
                result.append((degree, ns))
    require(len(result) == 72, "wrong local-type count")
    return tuple(result)


def type_edges(types):
    result = []
    for i, (di, ni) in enumerate(types):
        for j in range(i, len(types)):
            dj, nj = types[j]
            if ni[dj - 6] and nj[di - 6]:
                result.append((i, j))
    require(len(result) == 1638, "wrong type-edge count")
    return tuple(result)


def multipliers(entries, length, denominator, nonpositive=False):
    result = [Fraction(0)] * length
    seen = set()
    for entry in entries:
        require(isinstance(entry, list) and len(entry) == 2, "malformed multiplier")
        index, numerator = entry
        require(type(index) is type(numerator) is int, "noninteger multiplier data")
        require(0 <= index < length and index not in seen, "bad multiplier index")
        require(not nonpositive or numerator <= 0, "upper-row multiplier has wrong sign")
        seen.add(index)
        result[index] = Fraction(numerator, denominator)
    return result


def x_coefficient(index, item, equality, upper):
    degree, ns = item
    cls = degree - 6
    value = equality[cls]
    for row, (a, b) in enumerate(CLASS_PAIRS, 3):
        value += equality[row] * (int(cls == a) * ns[b] - int(cls == b) * ns[a])
    for a in range(3):
        value -= equality[6 + 3 * index + a] * ns[a]
    if degree == 8:
        value += equality[-1] * (5 - ns[1] - 2 * ns[2])
    for a in range(3):
        value += upper[a] * (ns[a] * (ns[a] - 1) + int(cls == a) * ns[a])
    for row, (a, b) in enumerate(CLASS_PAIRS, 3):
        value += upper[row] * (ns[a] * ns[b] + int(cls == a) * ns[b])
    for a in range(3):
        value += upper[6 + 3 * index + a] * (
            ns[a] - SIZES[a] - (degree - 1) * int(cls == a)
        )
    return value


def y_coefficient(i, j, types, equality, upper):
    value = Fraction(0)
    directions = ((i, j),) if i == j else ((i, j), (j, i))
    for root, neighbor in directions:
        degree, ns = types[neighbor]
        value += equality[6 + 3 * root + degree - 6]
        value += sum(upper[6 + 3 * root + a] * ns[a] for a in range(3))
    return value


def check_certificate(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    require(data["sizes"] == list(SIZES), "wrong class sizes")
    require(data["total_high_far_count"] == 4, "wrong A value")
    require(data["dimensions"] == [72, 1638, 223, 222], "wrong dimensions")
    denominator = data["denominator"]
    require(type(denominator) is int and denominator > 0, "bad denominator")
    types = local_types()
    edges = type_edges(types)
    equality = multipliers(data["equality_multipliers"], 223, denominator)
    upper = multipliers(data["inequality_multipliers"], 222, denominator, True)

    rhs = sum(equality[a] * SIZES[a] for a in range(3)) + equality[-1] * 4
    rhs += sum(upper[a] * SIZES[a] * (SIZES[a] - 1) for a in range(3))
    rhs += sum(upper[3 + row] * SIZES[a] * SIZES[b]
               for row, (a, b) in enumerate(CLASS_PAIRS))

    coefficients = [x_coefficient(i, item, equality, upper)
                    for i, item in enumerate(types)]
    coefficients.extend(y_coefficient(i, j, types, equality, upper) for i, j in edges)
    objective = [Fraction(ns[2], 2) if degree == 8 else Fraction(0)
                 for degree, ns in types] + [Fraction(0)] * len(edges)
    excess = max(Fraction(0), *(c - o for c, o in zip(coefficients, objective)))
    budget = 54 + 2 * 187
    bound = rhs - budget * excess
    require(budget == data["variable_budget"] == 428, "wrong graph-derived budget")
    require(rhs == Fraction(data["uncorrected_bound"]) == Fraction(981743, 500000),
            "wrong dual right side")
    require(excess == Fraction(data["max_coefficient_error"]) == Fraction(11, 500000),
            "wrong coefficient excess")
    require(bound == Fraction(data["corrected_bound"]) == Fraction(195407, 100000),
            "wrong corrected bound")
    require(bound > 1, "certificate does not prove integral m >= 2")
    return {
        "types": len(types),
        "edge_variables": len(edges),
        "columns": len(coefficients),
        "rhs": rhs,
        "excess": excess,
        "bound": bound,
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def partitions(total, minimum=1):
    if total == 0:
        yield ()
        return
    for first in range(minimum, total + 1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


def arithmetic_reduction():
    allowed = {
        A: tuple(part for part in partitions(A)
                 if sum(a * (a + 4) for a in part) <= 28)
        for A in (4, 5, 6)
    }
    require(allowed[4] == ((1, 1, 1, 1), (1, 1, 2), (1, 3), (2, 2)),
            "wrong A=4 deficit list")
    require(allowed[5] == ((1, 1, 1, 1, 1), (1, 1, 1, 2)),
            "wrong A=5 deficit list")
    require(not allowed[6], "A >= 6 not excluded")

    a5_positive = []
    for m in range(1, 4):
        for k in range(4 - m):
            inventory = 3 - m - k
            lower = 22 - 2 * m - k
            upper = 9 * inventory
            require(lower > upper, "unexcluded positive-m A=5 case")
            a5_positive.append((m, k))
    require(2 * (9 + 3) < 27, "unexcluded m=0 A=5 case")

    survivor = []
    for m in range(2, 5):
        for k in range(5 - m):
            for q in range(5 - m - k):
                inventory = 4 - m - k - q
                lower = 20 - 2 * m - k + 4 * q
                if (m, k, q) == (2, 0, 0):
                    survivor.append((m, k, q))
                else:
                    require(inventory <= 2 and lower > 9 * inventory,
                            "unexcluded A=4 aggregate case")
    require(survivor == [(2, 0, 0)] and 16 > 9,
            "wrong A=4 inventory survivor")
    v6_profiles = [(n2, n3, 2) for n2 in range(15) for n3 in range(15)
                   if n2 + n3 == 14 and 2 * n2 + 3 * n3 + 2 * 4 == 44]
    v7_profiles = [(n1, n2) for n1 in range(27) for n2 in range(27)
                   if n1 + n2 == 26 and n1 + 2 * n2 == 48]
    require(v6_profiles == [(6, 8, 2)] and v7_profiles == [(4, 22)],
            "wrong surviving low profile")

    equality_states = []
    for deficit in allowed[4]:
        high_gap = sum(a * (a + 4) for a in deficit)
        for p7 in range(43):
            qmax = 28 - high_gap - 4 * p7
            if qmax < 0:
                continue
            for Q in range(qmax + 1):
                for N in range(Q + 1):
                    P = 8 + N
                    for b2 in range(16 + p7, P + 1):
                        equality_states.append((deficit, p7, Q, N, P, b2))
    require(equality_states == [((1, 1, 1, 1), 0, 8, 8, 16, 16)],
            "wrong terminal equality state")
    require([(R, E) for R in range(5) for E in range(25) if E - 16 == R - 20]
            == [(4, 0)], "wrong R/E equality")
    return len(a5_positive), len(equality_states), v6_profiles[0], v7_profiles[0]


def low_type_signs():
    negatives = set()
    checked = 0
    for degree in (6, 7):
        for c in range(degree + 1):
            for n7 in range(degree - c + 1):
                epsilon = n7 + 2 * c - (8 if degree == 6 else 7)
                inventory = ((c - 3) * (c - 2) // 2 if degree == 6
                             else (c - 1) * (c - 2) // 2)
                require(inventory >= 0, "negative inventory contribution")
                require((epsilon * epsilon if degree == 6 else epsilon * (epsilon - 1))
                        >= max(-epsilon, 0), "bad negative-part bound")
                product = (c - 3) * epsilon
                if degree == 6:
                    require(product >= 0, "bad degree-six sign")
                elif product < 0:
                    negatives.add((c, epsilon))
                checked += 1
    require(negatives == {(1, 1), (2, 1), (2, 2)}, "wrong negative types")
    require(checked == 64, "wrong low-type count")
    return checked


def subset_reduction():
    T = frozenset(range(12))
    U = frozenset(range(4))
    V = frozenset(range(4, 8))
    K = T - U - V
    p = 8
    Z = K - {p}
    require(max(min(2 + a, 5 - a) for a in range(4)) == 3,
            "wrong type-(1,1) capacity")

    one_four_candidates = 0
    for Y in map(frozenset, combinations(T - U, 2)):
        if len(Y & V) > 1:
            continue
        small = [frozenset(S) for size in range(4)
                 for S in combinations(T - Y, size)]
        for L in small:
            if len(L & V) > 1:
                continue
            for M in small:
                if len(M & V) > 1:
                    continue
                if U | Y | L | M == T:
                    one_four_candidates += 1
    require(one_four_candidates == 0, "type-(2,1) survives one-four case")

    two_four_candidates = 0
    for Y in map(frozenset, combinations(K, 2)):
        if len(Y & Z) > 1:
            continue
        for size in range(4):
            for R in map(frozenset, combinations(T - Y, size)):
                if U | V | Y | R != T:
                    continue
                if R == Z:
                    valid = not (Y & Z)
                else:
                    valid = len(R & Z) <= 1
                two_four_candidates += int(valid)
    require(two_four_candidates == 0, "type-(2,1) survives two-four case")

    matching = ({0, 1}, {2, 3})
    terminal_candidates = 0
    for t in range(4):
        mate = next(iter(next(edge for edge in matching if t in edge) - {t}))
        available = set(range(4)) - {t, mate}
        for size in range(2, len(available) + 1):
            for C in map(set, combinations(available, size)):
                terminal_candidates += 1
                require(any(edge <= C for edge in matching),
                        "terminal high-neighbor set remains independent")
    require(terminal_candidates == 4, "wrong terminal candidate count")
    return one_four_candidates, two_four_candidates, terminal_candidates


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    cert = check_certificate(args.certificate)
    positive_a5, equality_states, v6_profile, v7_profile = arithmetic_reduction()
    low_types = low_type_signs()
    one_four, two_four, terminal = subset_reduction()
    print("cleanroom_z12_distant_incidence_audit=PASS")
    print(f"local_types={cert['types']} type_edge_variables={cert['edge_variables']} columns={cert['columns']}")
    print(f"certificate_rhs={cert['rhs']} max_excess={cert['excess']} corrected_m_bound={cert['bound']} integer_m_min=2")
    print(f"certificate_sha256={cert['sha256']}")
    print(f"low_neighbor_types={low_types} negative_types=(1,1),(2,1),(2,2)")
    print(f"A5_positive_m_cases={positive_a5} A4_aggregate_survivors=1 equality_states={equality_states}")
    print(f"survivor_low_profile=V6_c2,c3,c4:{v6_profile} V7_c1,c2:{v7_profile}")
    print(f"type21_candidates_one_four={one_four} type21_candidates_two_four={two_four}")
    print(f"terminal_matching_candidates={terminal} all_force_triangle=true")
    print("conclusion=z12_implies_A_at_most_3")


if __name__ == "__main__":
    main()
