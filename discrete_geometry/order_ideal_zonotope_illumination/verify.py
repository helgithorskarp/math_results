#!/usr/bin/env python3
"""Exact finite corroboration; universal claims are proved in PROOF.md.

CPython 3.11+, standard library. Integers/Fraction only, no assert, solver,
random sample, external data, or runtime dependencies. Vertices are 0..n-1;
bit i represents vertex i; edge orientations use sorted endpoint pairs.
"""

from fractions import Fraction
from itertools import combinations, permutations
from math import lcm
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_poset(n, relations):
    require(type(n) is int and n >= 1, "invalid poset size")
    R = set(relations)
    require(len(R) == len(relations), "duplicate relation")
    require(all(type(a) is int and type(b) is int and 0 <= a < b < n
                for a, b in R), "natural labeling required")
    require(all((a, c) in R for a, b in R for x, c in R if b == x),
            "relation is not transitively closed")


def naturally_labeled_posets(n):
    possible = tuple(combinations(range(n), 2))
    for code in range(1 << len(possible)):
        R = tuple(e for j, e in enumerate(possible) if code >> j & 1)
        try:
            validate_poset(n, R)
        except ValueError:
            continue
        yield R


def ideals(n, relations):
    return [A for A in range(1 << n)
            if all(not (A >> b & 1) or (A >> a & 1) for a, b in relations)]


def independent_sets(n, edges):
    return [S for S in range(1 << n)
            if all(not ((S >> a & 1) and (S >> b & 1)) for a, b in edges)]


def subset_sums(vector):
    sums = [0] * (1 << len(vector))
    for mask in range(1, len(sums)):
        bit = mask & -mask
        sums[mask] = sums[mask ^ bit] + vector[bit.bit_length() - 1]
    return sums


def connected(n, edges):
    seen = {0}
    while True:
        more = seen | {b for a, b in edges if a in seen} | {
            a for a, b in edges if b in seen}
        if more == seen:
            return len(seen) == n
        seen = more


def arcs_of(edges, bits):
    return tuple((a, b) if bits >> j & 1 else (b, a)
                 for j, (a, b) in enumerate(edges))


def is_acyclic(n, arcs):
    remaining = set(range(n))
    while remaining:
        ready = {v for v in remaining
                 if all(b != v or a not in remaining for a, b in arcs)}
        if not ready:
            return False
        remaining -= ready
    return True


def order_orientation(edges, order):
    rank = {v: i for i, v in enumerate(order)}
    return sum(1 << j for j, (a, b) in enumerate(edges) if rank[a] < rank[b])


def orientations(n, edges):
    return sorted({order_orientation(edges, p) for p in permutations(range(n))})


def ideal_orientation(n, relations, A):
    require(0 <= A < (1 << n), "invalid ideal mask")
    require(all(not (A >> b & 1) or (A >> a & 1) for a, b in relations),
            "not an order ideal")
    return sum(1 << j for j, (a, b) in enumerate(relations)
               if not ((A >> a & 1) and not (A >> b & 1)))


def vertex(n, edges, bits, weights):
    require(len(weights) == len(edges) and all(w > 0 for w in weights),
            "strictly positive weights required")
    v = [0] * n
    for (a, b), w in zip(arcs_of(edges, bits), weights):
        v[a] -= w
        v[b] += w
    return tuple(v)


def weights_for(edges):
    rational = tuple(Fraction(1 + (7*j) % 13, 1 + (5*j) % 7)
                     for j in range(len(edges)))
    den = lcm(*(w.denominator for w in rational))
    # Global scaling clears rational denominators without changing signs.
    return [(1,) * len(edges), tuple(1 + (3*j) % 11 for j in range(len(edges))),
            tuple(int(w * den) for w in rational)]


def support(f, edges, weights):
    return sum(w * abs(f[b] - f[a]) for (a, b), w in zip(edges, weights))


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def check_lower(n, relations):
    validate_poset(n, relations)
    require(n >= 2 and connected(n, relations), "connected graph required")
    all_ideals = ideals(n, relations)
    antichains = independent_sets(n, relations)
    maximal_sets = []
    for A in all_ideals:
        M = sum(1 << a for a in range(n) if A >> a & 1
                and not any(x == a and (A >> b & 1) for x, b in relations))
        closure = M
        for a, b in relations:
            if M >> b & 1:
                closure |= 1 << a
        require(closure == A, "ideal/antichain inverse failed")
        maximal_sets.append(M)
    require(sorted(maximal_sets) == antichains, "ideal/antichain bijection failed")
    proper = all_ideals[:-1]
    codes = [ideal_orientation(n, relations, A) for A in proper]
    require(ideal_orientation(n, relations, 0) ==
            ideal_orientation(n, relations, (1 << n)-1), "endpoint identification failed")
    require(len(set(codes)) == len(codes), "repeated certificate orientation")
    require(all(is_acyclic(n, arcs_of(relations, c)) for c in codes),
            "cyclic certificate orientation")
    pair_checks = 0
    for weights in weights_for(relations):
        vv = [vertex(n, relations, code, weights) for code in codes]
        require(len(set(vv)) == len(codes), "repeated weighted vertex")
        for a, b in combinations(range(len(proper)), 2):
            f = tuple((proper[a] >> j & 1) - (proper[b] >> j & 1) for j in range(n))
            h = support(f, relations, weights)
            require(h > 0 and dot(f, vv[a]) == h and dot(f, vv[b]) == -h,
                    "opposite weighted supports failed")
            pair_checks += 1
    return {"proper_ideals": len(proper), "weighted_antipodal_pairs": pair_checks}


def source_set(n, arcs):
    heads = {b for a, b in arcs}
    return sum(1 << j for j in range(n) if j not in heads)


def common_neighbor(n, edges, S):
    require(0 < S < (1 << n), "invalid nonempty source mask")
    E = set(edges)
    require(all(not ((S >> a & 1) and (S >> b & 1)) for a, b in edges),
            "source set is not independent")
    for r in range(n):
        if not (S >> r & 1) and all(tuple(sorted((r, s))) in E
                                    for s in range(n) if S >> s & 1):
            return r
    raise ValueError("no common neighbor")


def direction(n, edges, S):
    r = common_neighbor(n, edges, S)
    s = S.bit_count()
    u = tuple(n if S >> v & 1 else -n*s+n-s-1 if v == r else -1
              for v in range(n))
    require(sum(u) == 0 and all((u[v] > 0) == bool(S >> v & 1) for v in range(n)),
            "wrong sum or signs of direction")
    return u


def cut_supports(n, edges, weights):
    return [sum(w for (a, b), w in zip(edges, weights) if ((M >> a) ^ (M >> b)) & 1)
            for M in range(1 << n)]


def illuminates_cut_data(u_sums, v_sums, heights):
    return all(u_sums[M] < 0 for M in range(1, len(heights)-1)
               if v_sums[M] == heights[M])


def check_upper(n, edges, compare_lower=False):
    require(connected(n, edges), "disconnected upper-bound input")
    indep = independent_sets(n, edges)[1:]
    sums = {S: subset_sums(direction(n, edges, S)) for S in indep}
    codes = orientations(n, edges)
    brute = 0
    if len(edges) <= 10:
        brute = 1 << len(edges)
        independently_enumerated = [c for c in range(brute)
                                   if is_acyclic(n, arcs_of(edges, c))]
        require(independently_enumerated == codes, "orientation enumerations disagree")
    active_count = step_count = 0
    baseline = {}
    for wi, weights in enumerate(weights_for(edges)):
        heights = cut_supports(n, edges, weights)
        seen = set()
        for code in codes:
            S = source_set(n, arcs_of(edges, code))
            u = sums[S]
            v = vertex(n, edges, code, weights)
            seen.add(v)
            x = subset_sums(v)
            require(all(x[M] <= heights[M] for M in range(1, len(x)-1)),
                    "vertex violates a supporting cut")
            active = tuple(M for M in range(1, len(x)-1) if x[M] == heights[M])
            require(active and illuminates_cut_data(u, x, heights),
                    "source direction violates strict illumination")
            if wi == 0:
                baseline[code] = active
            else:
                require(active == baseline[code], "positive weights changed normal fan")
            active_count += len(active)
            caps = [Fraction(heights[M]-x[M], u[M]) for M in range(1, len(x)-1) if u[M] > 0]
            step = min([Fraction(1)] + caps) / 2
            require(step > 0, "zero interior step")
            a, b = step.numerator, step.denominator
            require(all(b*x[M]+a*u[M] < b*heights[M] for M in range(1, len(x)-1)),
                    "actual rational step is not interior")
            step_count += 1
        require(len(seen) == len(codes), "weighted vertex reconstruction not injective")
        if compare_lower:
            proper = ideals(n, edges)[:-1]
            require(len(proper) == len(indep), "lower and upper cardinalities differ")
            used = []
            for A in proper:
                code = ideal_orientation(n, edges, A)
                x = subset_sums(vertex(n, edges, code, weights))
                lighting = [S for S in indep if illuminates_cut_data(sums[S], x, heights)]
                require(len(lighting) == 1, "certificate not uniquely illuminated")
                used += lighting
            require(sorted(used) == indep, "certificate/cover matching not bijective")
    result = {"vertices": len(codes), "edge_orientations_tested": brute,
              "strict_active_cuts": active_count, "exact_interior_steps": step_count}
    if compare_lower:
        result.update(check_lower(n, edges))
    return result


def ordinal_sum(a, P, b, Q):
    return tuple(sorted(P + tuple((x+a, y+a) for x, y in Q)
                        + tuple((x, y) for x in range(a) for y in range(a, a+b))))


def add_totals(totals, row):
    for k, v in row.items():
        totals[k] = totals.get(k, 0) + v


def expect_rejection(name, fn, labels):
    try:
        fn()
    except ValueError:
        labels.append(name)
    else:
        raise ValueError("negative control accepted: " + name)


def negative_controls():
    labels = []
    expect_rejection("nontransitive_relation", lambda: validate_poset(3, ((0, 1), (1, 2))), labels)
    expect_rejection("nonideal_subset", lambda: ideal_orientation(2, ((0, 1),), 2), labels)
    expect_rejection("disconnected_lower_input", lambda: check_lower(2, ()), labels)
    for w in (0, -1):
        expect_rejection("weight_" + str(w), lambda: vertex(2, ((0, 1),), 1, (w,)), labels)
    edges = ((0, 1),)
    h = cut_supports(2, edges, (1,))
    x = subset_sums(vertex(2, edges, 1, (1,)))
    require(not illuminates_cut_data([0]*4, x, h), "tangent direction accepted")
    u = direction(2, edges, 1)
    require(not illuminates_cut_data(subset_sums(tuple(-a for a in u)), x, h),
            "reversed direction accepted")
    labels += ["tangent_direction", "reversed_direction"]
    # Cone over K2 plus an isolated vertex: uniform source direction is tangent.
    paw = ((0, 1), (0, 3), (1, 3), (2, 3))
    c = order_orientation(paw, (0, 2, 1, 3))
    S = source_set(4, arcs_of(paw, c))
    x = subset_sums(vertex(4, paw, c, (1,)*4))
    h = cut_supports(4, paw, (1,)*4)
    uniform = tuple(4-S.bit_count() if S >> v & 1 else -S.bit_count() for v in range(4))
    require(not illuminates_cut_data(subset_sums(uniform), x, h), "uniform tangency lost")
    require(illuminates_cut_data(subset_sums(direction(4, paw, S)), x, h), "new direction fails")
    labels.append("uniform_source_tangency_new_direction_succeeds")
    C6 = ((0, 3), (0, 5), (1, 3), (1, 4), (2, 4), (2, 5))
    expect_rejection("C6_alternating_sources_no_common_neighbor",
                     lambda: common_neighbor(6, C6, 7), labels)
    require(len(independent_sets(6, C6)) == 18, "C6 independent-set count")
    row = check_lower(6, C6)
    require(row["proper_ideals"] == 17, "C6 lower bound count")
    return {"rejected_or_detected": labels, "C6_lower_certificate": row}


def main():
    posets = {n: list(naturally_labeled_posets(n)) for n in range(1, 6)}
    lower = {"connected_posets": 0}
    for n, pp in posets.items():
        if n == 1:
            continue
        for P in pp:
            if connected(n, P):
                lower["connected_posets"] += 1
                add_totals(lower, check_lower(n, P))

    join_cases = set()
    presentations = 0
    for n in range(2, 6):
        for a in range(1, n):
            b = n-a
            for P in posets[a]:
                for Q in posets[b]:
                    G = ordinal_sum(a, P, b, Q)
                    expected = len(ideals(a, P)) + len(ideals(b, Q)) - 2
                    require(len(independent_sets(n, G))-1 == expected, "join count formula")
                    presentations += 1
                    join_cases.add((n, G))

    # Complete labeled bipartite family with fixed parts 2+3, not a generic graph census.
    bipartite = {"graphs": 0, "independent_sets": 0}
    possible = tuple((a, b) for a in range(2) for b in range(2, 5))
    cone_cases = set()
    for code in range(1 << len(possible)):
        H = tuple(e for j, e in enumerate(possible) if code >> j & 1)
        count = len(independent_sets(5, H))
        require(count == len(ideals(5, H)), "height-two poset count failed")
        G = ordinal_sum(5, H, 1, ())
        require(len(ideals(6, G))-1 == count, "cone reduction count failed")
        # Delete the last coordinate in the segment generators, independently.
        projected = []
        for a, b in G:
            v = tuple(int(j == b)-int(j == a) for j in range(5))
            first = next(x for x in v if x)
            projected.append(tuple(x if first > 0 else -x for x in v))
        expected = [tuple(int(j == a) for j in range(5)) for a in range(5)]
        expected += [tuple(int(j == a)-int(j == b) for j in range(5)) for a, b in H]
        require(sorted(projected) == sorted(expected), "cube-plus-differences map failed")
        bipartite["graphs"] += 1
        bipartite["independent_sets"] += count
        cone_cases.add((6, G))

    # Two larger, non-height-two factors exercise transitivity beyond bipartite cones.
    extras = [(6, ordinal_sum(5, tuple(combinations(range(5), 2)), 1, ())),
              (7, ordinal_sum(3, ((0, 1), (0, 2)), 4,
                              ((0, 1), (0, 2), (0, 3), (1, 3), (2, 3))))]
    matched = {"graphs": 0}
    for n, G in sorted(join_cases | cone_cases | set(extras)):
        matched["graphs"] += 1
        add_totals(matched, check_upper(n, G, compare_lower=True))

    C5 = ((0, 1), (0, 4), (1, 2), (2, 3), (3, 4))
    cone_C5 = tuple(sorted(C5 + tuple((i, 5) for i in range(5))))
    noncomparability_upper = {
        "C5": check_upper(5, C5), "cone_C5": check_upper(6, cone_C5)}
    print(json.dumps({"status": "VERIFIED", "arithmetic": "integers and Fraction",
                      "weight_assignments_per_graph": 3,
                      "naturally_labeled_posets_by_size": {n: len(pp) for n, pp in posets.items()},
                      "order_ideal_lower_checks": lower,
                      "ordinal_sum_presentations": presentations,
                      "distinct_ordinal_sums_through_five_vertices": len(join_cases),
                      "bipartite_count_reduction": bipartite,
                      "matched_join_certificates": matched,
                      "upper_lemma_outside_comparability": noncomparability_upper,
                      "negative_controls": negative_controls()}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
