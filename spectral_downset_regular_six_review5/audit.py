#!/usr/bin/env python3
"""Independent regular-six audit: meet-in-middle, full matrices, maximal cliques.

Author: six-reviewer-5, independent mathematical reviewer. Standard library only.
The small orbit-value fixture is attributed to six-downset-3; no author code
or precomputed enumeration enters the checks. All proof guards survive -O.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, permutations
from math import gcd, lcm
from pathlib import Path
import argparse
import copy
import hashlib
import json


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def six_census():
    triples = tuple(sum(1 << x for x in c) for c in combinations(range(6), 3))
    triples = tuple(sorted(triples))
    halves = []
    for part in (triples[:10], triples[10:]):
        table = defaultdict(list)
        for word in range(1024):
            selected = [part[j] for j in range(10) if word >> j & 1]
            degrees = tuple(sum(a >> i & 1 for a in selected) for i in range(6))
            table[degrees].append(word)
        halves.append(table)
    labelled = {}
    for d in range(1, 11):
        for left_degree, words in halves[0].items():
            need = tuple(d - x for x in left_degree)
            for right in halves[1].get(need, []):
                for left in words:
                    w = left | right << 10
                    require(w not in labelled, "duplicate meet-in-middle word")
                    selected = [a for j, a in enumerate(triples) if w >> j & 1]
                    require(len(selected) == 2*d, "regular incidence identity")
                    require(all(sum(a >> i & 1 for a in selected) == d
                                for i in range(6)), "direct point degrees")
                    labelled[w] = d
    maps = []
    positions = {a: j for j, a in enumerate(triples)}
    for p in permutations(range(6)):
        images = tuple(sum(1 << p[i] for i in range(6) if a >> i & 1)
                       for a in range(64))
        powers = tuple(1 << positions[images[a]] for a in triples)
        maps.append((p, images, powers))
    def image_word(w, powers):
        return sum(powers[j] for j in range(20) if w >> j & 1)
    covered = set()
    cases = []
    base = sum(1 << a for a in range(64) if a.bit_count() <= 2)
    for word, d in sorted(labelled.items()):
        if word in covered:
            continue
        orbit = {image_word(word, powers) for _, _, powers in maps}
        require(word == min(orbit), "noncanonical orbit start")
        require(not covered & orbit, "overlapping full orbits")
        require(orbit <= labelled.keys(), "orbit outside enumerated domain")
        require(all(labelled[w] == d for w in orbit), "orbit degree changed")
        covered.update(orbit)
        selected = [a for j, a in enumerate(triples) if word >> j & 1]
        autos = [(p, images) for p, images, powers in maps
                 if image_word(word, powers) == word]
        require(len(orbit)*len(autos) == 720, "orbit stabilizer identity")
        cases.append({"family": base + sum(1 << a for a in selected),
                      "triples": selected, "d": d, "N": 22+2*d, "s": 6+d,
                      "orbit_size": len(orbit), "automorphisms": len(autos),
                      "transitive": len({p[0] for p, _ in autos}) == 6,
                      "autos": [images for _, images in autos]})
    require(covered == labelled.keys(), "full orbit coverage incomplete")
    # Hypergraph complementation must be a bijection between degrees d and 10-d.
    for w, d in labelled.items():
        if d < 10:
            require(labelled.get(w ^ ((1 << 20)-1)) == 10-d,
                    "complement involution failed")
    return sorted(cases, key=lambda c: c["family"]), labelled


def fraction_free_psd_rank(matrix):
    """Symmetric Bareiss elimination with checked division and zero-row removal.

    After k positive pivots the active matrix is det(A[I,I]) times its
    Schur complement. The previous determinant is the Bareiss denominator.
    Positive diagonal pivots preserve inertia; a zero diagonal with any
    nonzero off-diagonal entry cannot occur in a PSD matrix.
    """
    require(all(isinstance(x, int) for row in matrix for x in row), "noninteger PSD input")
    n = len(matrix)
    require(all(len(row) == n for row in matrix), "nonsquare PSD input")
    require(all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n)),
            "nonsymmetric PSD input")
    b = [row[:] for row in matrix]
    active, previous, rank = list(range(n)), 1, 0
    while active:
        zeros = [i for i in active if b[i][i] == 0]
        for i in zeros:
            require(all(b[i][j] == 0 for j in active), "zero diagonal nonzero row")
        active = [i for i in active if b[i][i] != 0]
        if not active:
            break
        q = active[0]
        pivot = b[q][q]
        require(pivot > 0, "negative PSD pivot")
        rest = active[1:]
        for i in rest:
            for j in rest:
                numerator = pivot*b[i][j] - b[i][q]*b[q][j]
                quotient, remainder = divmod(numerator, previous)
                require(remainder == 0, "inexact Bareiss division")
                b[i][j] = quotient
        previous, active, rank = pivot, rest, rank+1
    return rank


def maximal_intersecting(sets):
    """Every maximal clique by pivoted Bron--Kerbosch; no size-bound pruning."""
    n = len(sets)
    adjacency = [sum(1 << j for j, b in enumerate(sets) if i != j and a & b)
                 for i, a in enumerate(sets)]
    largest, witnesses, nodes, leaves = 0, [], 0, 0
    def visit(chosen, possible, excluded):
        nonlocal largest, witnesses, nodes, leaves
        nodes += 1
        require(nodes <= 500000, "maximal-clique operational bound reached; incomplete")
        if not possible and not excluded:
            leaves += 1
            size = chosen.bit_count()
            if size > largest:
                largest, witnesses = size, [chosen]
            elif size == largest:
                witnesses.append(chosen)
            return
        union = possible | excluded
        vertices = [i for i in range(n) if union >> i & 1]
        pivot = max(vertices, key=lambda i: (possible & adjacency[i]).bit_count())
        branches = possible & ~adjacency[pivot]
        while branches:
            bit = branches & -branches
            i = bit.bit_length()-1
            visit(chosen | bit, possible & adjacency[i], excluded & adjacency[i])
            possible ^= bit
            excluded |= bit
            branches ^= bit
    visit(0, (1 << n)-1, 0)
    return largest, sorted(witnesses), nodes, leaves


def decode_matrix(case, certificate):
    sets = [a for a in range(64) if case["family"] >> a & 1]
    require(len(sets) == case["N"] and sets[0] == 0, "family dimension/empty")
    for a in sets:
        require(all((case["family"] >> (a ^ (1 << i))) & 1
                    for i in range(6) if a >> i & 1), "not a downset")
    reps, vals = certificate["orbit_representatives"], certificate["orbit_values"]
    require(len(reps) == len(vals), "orbit/value lengths")
    entries = {}
    included = set(sets[1:])
    for pair, text in zip(reps, vals):
        require(len(pair) == 2, "orbit representative length")
        a, b = pair
        require(a in included and b in included and a != b and not a & b,
                "invalid orbit representative")
        orbit = {tuple(sorted((mapping[a], mapping[b]))) for mapping in case["autos"]}
        require(not entries.keys() & orbit, "orbit overlap")
        value = F(text)
        for key in orbit:
            entries[key] = value
    allowed = {(a, b) for a, b in combinations(sets[1:], 2) if not a & b}
    require(entries.keys() == allowed, "missing/extra allowed orbit")
    n, s = case["N"], case["s"]
    # Reconstruct M directly from its nonempty block and normalized row sums.
    # No source core/lift/upper-congruence implementation is imported.
    m = [[F(0) for _ in range(n)] for _ in range(n)]
    for i, a in enumerate(sets[1:], 1):
        for j, b in enumerate(sets[1:], 1):
            if i != j and not a & b:
                m[i][j] = entries[tuple(sorted((a, b)))]/(n-s)
        m[0][i] = m[i][0] = 1-sum(m[i])
    m[0][0] = 1-sum(m[0][1:])
    denominator = lcm(*(x.denominator for row in m for x in row))
    numerator = [[int(x*denominator) for x in row] for row in m]
    g = gcd(denominator, gcd(*(x for row in numerator for x in row)))
    denominator //= g
    numerator = [[x//g for x in row] for row in numerator]
    require(all(sum(row) == denominator for row in numerator), "M row sums")
    require(all(numerator[i][j] == numerator[j][i] and
                (not a & b or numerator[i][j] == 0)
                for i, a in enumerate(sets) for j, b in enumerate(sets)), "M symmetry/support")
    low = [[(n-s)*numerator[i][j] + s*denominator*(i == j)
            for j in range(n)] for i in range(n)]
    upper = [[denominator*(i == j)-numerator[i][j]
              for j in range(n)] for i in range(n)]
    low_rank = fraction_free_psd_rank(low)
    upper_rank = fraction_free_psd_rank(upper)
    require(low_rank == n-6 and upper_rank == n-1, "full matrix ranks")
    stars = []
    for k in range(6):
        x = [int(a >> k & 1) for a in sets]
        require(sum(x) == s, "actual star sizes")
        z = [n*v-s for v in x]
        require(all(sum(row[j]*z[j] for j in range(n)) == 0 for row in low),
                "centered star kernel")
        stars.append(sum(1 << j for j, a in enumerate(sets[1:]) if a >> k & 1))
    alpha, maxima, nodes, leaves = maximal_intersecting(sets[1:])
    require(alpha == s and maxima == sorted(stars), "direct maximum-family classification")
    return {k: case[k] for k in ("family", "triples", "d", "N", "s", "orbit_size",
                                 "automorphisms", "transitive")} | {
        "M_denominator": denominator, "M_numerator_sha256": digest(numerator),
        "M_empty_diagonal": str(m[0][0]), "H_PSD_rank": low_rank,
        "I_minus_M_rank": upper_rank, "maximum_families": len(maxima),
        "maximal_cliques": leaves, "clique_nodes": nodes}


def boundary_nine():
    outputs = []
    k, b = (0, 1, 2), (3, 4, 5, 6, 7, 8)
    mask = lambda points: sum(1 << i for i in points)
    cross = {mask(pair + (j,)) for pair in combinations(k, 2) for j in b}
    btriples = {mask(t) for t in combinations(b, 3)}
    for epsilon in (0, 1):
        triples = cross | btriples
        if epsilon:
            triples.add(mask(k))
        else:
            triples -= {mask(b[:3]), mask(b[3:])}
        family = {mask(t) for size in (0, 1, 2) for t in combinations(range(9), size)} | triples
        nonstar = {mask(t) for t in combinations(k, 2)} | cross
        if epsilon:
            nonstar.add(mask(k))
        d = 12+epsilon
        require(all(sum(a >> i & 1 for a in triples) == d for i in range(9)),
                "nine-point regularity")
        s = 9+d
        require(all(sum(a >> i & 1 for a in family) == s for i in range(9)),
                "nine-point largest stars")
        require(nonstar <= family and len(nonstar) == s,
                "nine-point witness size")
        require(all(a & c for a in nonstar for c in nonstar), "nonintersecting witness")
        common = (1 << 9)-1
        for a in nonstar:
            common &= a
        require(common == 0, "witness is a star")
        require(not any(a.bit_count() == 1 for a in nonstar), "witness singleton")
        outputs.append({"epsilon": epsilon, "triples": len(triples), "N": len(family),
                        "degree": d, "s": s, "nonstar_size": len(nonstar),
                        "H_rank_upper_if_feasible": len(family)-10,
                        "triples_sha256": digest(sorted(triples)),
                        "witness_sha256": digest(sorted(nonstar))})
    return outputs


def controls():
    examples = [([[1, 1], [1, 1]], 1), ([[1, 0], [0, 0]], 1),
                ([[2, -1], [-1, 2]], 2), ([[0, 0], [0, 0]], 0),
                ([[0, 0, 0], [0, 2, 1], [0, 1, 2]], 2)]
    for a, rank in examples:
        require(fraction_free_psd_rank(a) == rank, "PSD control rank")
    bad = [[[0, 1], [1, 0]], [[1, 2], [2, 1]], [[-1]], [[1, 0], [1, 1]]]
    for a in bad:
        try:
            fraction_free_psd_rank(a)
        except ValueError:
            continue
        raise ValueError("indefinite/nonsymmetric control accepted")
    # Every graph on five vertices has an intersection-set representation:
    # one private element per vertex and one shared element per edge.
    # Compare all 1,024 graphs against all 32 vertex subsets directly.
    edges = list(combinations(range(5), 2))
    for graph in range(1 << len(edges)):
        sets = [1 << i for i in range(5)]
        for j, (u, v) in enumerate(edges):
            if graph >> j & 1:
                sets[u] |= 1 << (5+j)
                sets[v] |= 1 << (5+j)
        cliques = [w for w in range(32)
                   if all(sets[u] & sets[v] for u, v in edges
                          if w >> u & 1 and w >> v & 1)]
        size = max(w.bit_count() for w in cliques)
        witnesses = sorted(w for w in cliques if w.bit_count() == size)
        got_size, got_witnesses, _, _ = maximal_intersecting(sets)
        require((got_size, got_witnesses) == (size, witnesses), "five-vertex clique control")
    return len(examples), len(bad), 1024


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificates", type=Path,
                        default=Path(__file__).with_name("certificates.json"))
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    controls_ok = controls()
    cases, labelled = six_census()
    fixture = json.loads(args.certificates.read_text())
    require(fixture["agent"] == "six-downset-3", "fixture attribution")
    data = fixture["certificates"]
    lookup = {x["family"]: x for x in data}
    require(len(lookup) == len(data), "duplicate fixture family")
    require(lookup.keys() == {c["family"] for c in cases}, "certificate domain differs")
    first = cases[0]
    rejected = []
    for name in ("changed-value", "missing-orbit", "duplicate-orbit", "intersecting-orbit"):
        altered = copy.deepcopy(lookup[first["family"]])
        if name == "changed-value":
            altered["orbit_values"][0] = str(F(altered["orbit_values"][0])+1)
        elif name == "missing-orbit":
            altered["orbit_representatives"].pop()
            altered["orbit_values"].pop()
        elif name == "duplicate-orbit":
            altered["orbit_representatives"].append(altered["orbit_representatives"][0])
            altered["orbit_values"].append(altered["orbit_values"][0])
        else:
            altered["orbit_representatives"][0] = [1, 3]
        try:
            decode_matrix(first, altered)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("corrupt orbit fixture accepted: "+name)
    rows = [decode_matrix(case, lookup[case["family"]]) for case in cases]
    # The special family's dual needs no imported primal or code.
    special = next(c for c in cases if c["family"] == 1991589575991295)
    sets = [a for a in range(64) if special["family"] >> a & 1]
    require(not any((a ^ 63) in sets for a in special["triples"]),
            "exception complementary triples")
    dual = sum(F(max(a.bit_count()-1, 0), 3) for a in sets)
    require(dual == F(35, 3), "fractional dual sum")
    separation = []
    for d in range(1, 11):
        n, s = 22+2*d, 6+d
        _, remainder = divmod(n-1, s)
        bound = F(1+remainder*(s-remainder)-s, n-s)
        if bound > 1:
            separation.append({"d": d, "bound": str(bound),
                               "classes": sum(c["d"] == d for c in cases)})
    result = {"agent": "six-reviewer-5", "role": "independent mathematical reviewer",
              "enumeration": "10+10 meet-in-middle degree matching, full720 permutations",
              "classes": len(cases), "labelled": len(labelled),
              "labelled_words_sha256": digest(sorted(labelled)),
              "degree_counts": {str(k): v for k, v in Counter(labelled.values()).items()},
              "class_degree_counts": {str(k): v for k, v in Counter(c["d"] for c in cases).items()},
              "transitive_classes": sum(c["transitive"] for c in cases),
              "PSD_positive_controls": controls_ok[0], "PSD_negative_controls": controls_ok[1],
              "clique_control_graphs": controls_ok[2], "rejected_orbit_controls": rejected,
              "fractional_base_dual": str(dual), "partition_cap_separation": separation,
              "nine_point_boundaries": boundary_nine(), "cases": rows}
    if args.check:
        expected = json.loads(args.check.read_text())
        require(result == expected, "independent output differs from expected")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
