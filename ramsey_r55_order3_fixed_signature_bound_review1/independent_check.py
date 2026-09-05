#!/usr/bin/env python3
"""Clean-room checks for the fixed-signature lemma, census, and fixture."""

from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import argparse
import hashlib
import json


ROOT = Path(__file__).resolve().parent
TARGET = ROOT.parent / "ramsey_r55_order3_fixed_signature_bound"
FIXTURE = TARGET / "sharp25.edges"
FIXTURE_SHA256 = "a1d95f21cc88ac8a1fc536d359e672c2d395193206e86f7759eb488772e8a5d4"
SIGNATURES = tuple(mask for mask in range(1, 16) if mask.bit_count() <= 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def red_in_core(a, b):
    """Literal definition of the submitted twelve-vertex core."""
    require(0 <= a < b < 12, "core pair out of range")
    i, s = divmod(a, 3)
    j, t = divmod(b, 3)
    if i == j:
        return True
    difference = (t - s) % 3
    return difference == 0 if (i, j) in ((0, 1), (2, 3)) else difference in (0, 1)


def core_audit():
    red = {pair for pair in combinations(range(12), 2) if red_in_core(*pair)}
    blue = set(combinations(range(12), 2)) - red
    require(len(red) == 42, "unexpected core edge count")
    require(not any(all(pair in blue for pair in combinations(vertices, 2))
                    for vertices in combinations(range(12), 3)),
            "the core contains a blue triangle")

    blue_cross_edges = {}
    for i, j in combinations(range(4), 2):
        edges = [(a, b) for a in range(3 * i, 3 * i + 3)
                 for b in range(3 * j, 3 * j + 3) if (a, b) in blue]
        require(edges, f"no blue edge between core triangles {i},{j}")
        blue_cross_edges[f"{i}{j}"] = edges[0]

    witnesses = {}
    for support in combinations(range(4), 3):
        vertices = [3 * i + s for i in support for s in range(3)]
        cliques = [choice for choice in combinations(vertices, 4)
                   if all(pair in red for pair in combinations(choice, 2))]
        require(cliques, f"no red K4 on triangle support {support}")
        witnesses["".join(map(str, support))] = cliques[0]
    return red, blue, blue_cross_edges, witnesses


def signature_index(mask):
    return SIGNATURES.index(mask)


def hand_inequality_audit(blue_cross_edges):
    # Three copies of any one nonempty signature are pairwise forced blue and
    # share a forced-blue core edge outside that signature.  Hence each
    # multiplicity is at most two before this finite audit begins.
    for signature in SIGNATURES:
        outside = [i for i in range(4) if not (signature >> i) & 1]
        require(len(outside) >= 2, "signature support unexpectedly too large")
        pair = tuple(outside[:2])
        require("".join(map(str, pair)) in blue_cross_edges,
                "missing core edge needed for multiplicity-two bound")

    maximum = -1
    equality_vectors = []
    admissible = 0
    for counts in product(range(3), repeat=10):
        def count(mask):
            return counts[signature_index(mask)]

        first = [sum(counts[k] for k, mask in enumerate(SIGNATURES)
                     if (mask >> i) & 1) <= 4 for i in range(4)]
        second = [count(1 << i) + count((1 << i) | (1 << j)) <= 2
                  for i in range(4) for j in range(4) if i != j]
        if not all(first + second):
            continue
        admissible += 1
        total = sum(counts)
        if total > maximum:
            maximum = total
            equality_vectors = [counts]
        elif total == maximum:
            equality_vectors.append(counts)
    require(maximum == 10, "incidence inequalities permit more than ten vertices")
    require(equality_vectors == [tuple([1] * 10)], "equality pattern is not unique")
    return {
        "multiplicity_vectors_checked": 3 ** 10,
        "vectors_satisfying_hand_inequalities": admissible,
        "maximum_nonempty_vertices": maximum,
        "maximizers": [list(vector) for vector in equality_vectors],
    }


def fixed_multiset_forces_blue_clique(signatures, core_vertices, blue_core):
    return (
        all(a & b for a, b in combinations(signatures, 2))
        and all(not ((signature >> (v // 3)) & 1)
                for signature in signatures for v in core_vertices)
        and all(pair in blue_core for pair in combinations(core_vertices, 2))
    )


def minimal_forbidden_requirements(blue_core):
    """Derive forced-blue K5 obstructions without signature-family bounds."""
    requirements = set()
    templates_checked = 0
    for fixed_count in (3, 4, 5):
        core_count = 5 - fixed_count
        for signatures in combinations_with_replacement(SIGNATURES, fixed_count):
            requirement = tuple(signatures.count(mask) for mask in SIGNATURES)
            # Census coordinates range from zero to two.  Larger requirements
            # cannot be dominated by any census vector and may be discarded.
            if max(requirement) > 2:
                continue
            for core_vertices in combinations(range(12), core_count):
                templates_checked += 1
                if fixed_multiset_forces_blue_clique(signatures, core_vertices, blue_core):
                    requirements.add(requirement)
                    break

    minimal = sorted(requirement for requirement in requirements
                     if not any(other != requirement and
                                all(a <= b for a, b in zip(other, requirement))
                                for other in requirements))
    require(minimal, "no forced-blue K5 requirements found")
    return minimal, templates_checked


def census(blue_core):
    forbidden, templates_checked = minimal_forbidden_requirements(blue_core)
    histogram = Counter()
    digest = hashlib.sha256()
    survivors = 0
    equality = []
    nonnegative = 0
    for counts in product(range(3), repeat=10):
        total = sum(counts)
        if total > 13:
            continue
        nonnegative += 1
        if any(all(need <= have for need, have in zip(requirement, counts))
               for requirement in forbidden):
            continue
        z = 13 - total
        survivors += 1
        histogram[z] += 1
        digest.update((str(z) + " " + ",".join(map(str, counts)) + "\n").encode())
        if z == 3:
            equality.append(counts)

    expected_histogram = {3: 1, 4: 10, 5: 50, 6: 178, 7: 424, 8: 548,
                          9: 405, 10: 186, 11: 55, 12: 10, 13: 1}
    require(nonnegative == 53856, "wrong number of nonnegative-z vectors")
    require(survivors == 1868, "independent census total differs")
    require(dict(sorted(histogram.items())) == expected_histogram,
            "independent census histogram differs")
    require(equality == [tuple([1] * 10)], "independent census equality case differs")
    require(digest.hexdigest() ==
            "e9814163f0c41a8c72c9fdcec60150b3b73de5b1beb8dbefd6d1d9ff01e27f03",
            "independent survivor stream differs")

    family_count = 0
    for family_bits in range(1, 1 << len(SIGNATURES)):
        family = [SIGNATURES[i] for i in range(10) if (family_bits >> i) & 1]
        if all(a & b for a, b in combinations(family, 2)):
            family_count += 1
    require(family_count == 58, "pairwise-intersecting family count differs")
    return {
        "count_vectors_checked": 3 ** 10,
        "nonnegative_empty_count_vectors": nonnegative,
        "blue_k5_templates_checked": templates_checked,
        "minimal_forbidden_multiplicity_patterns": len(forbidden),
        "pairwise_intersecting_families": family_count,
        "survivors": survivors,
        "histogram_by_empty_count": dict(sorted(histogram.items())),
        "survivor_stream_sha256": digest.hexdigest(),
    }


def read_fixture(path):
    require(hashlib.sha256(path.read_bytes()).hexdigest() == FIXTURE_SHA256,
            "literal fixture hash differs")
    lines = path.read_text().splitlines()
    n, claimed_edges = map(int, lines[0].split())
    edges = {tuple(map(int, line.split())) for line in lines[1:]}
    require(n == 25 and claimed_edges == 132 and len(edges) == 132,
            "literal fixture dimensions differ")
    require(all(0 <= a < b < n for a, b in edges), "malformed literal fixture edge")
    return n, edges


def fixture_audit(core_red):
    n, red = read_fixture(FIXTURE)
    require({pair for pair in red if pair[1] < 12} == core_red,
            "fixture does not induce the defined core")

    signatures = []
    for fixed_vertex in range(12, 25):
        signature = 0
        for i in range(4):
            colors = {(v, fixed_vertex) in red for v in range(3 * i, 3 * i + 3)}
            require(len(colors) == 1, "fixture incidence is not triangle-uniform")
            if colors.pop():
                signature |= 1 << i
        signatures.append(signature)
    require(signatures == [0, 0, 0] + list(SIGNATURES),
            "fixture signature pattern differs")

    permutation = [3 * (v // 3) + (v + 1) % 3 if v < 12 else v for v in range(n)]
    for a, b in combinations(range(n), 2):
        image = tuple(sorted((permutation[a], permutation[b])))
        require(((a, b) in red) == (image in red), "fixture is not order-three invariant")

    monochromatic = []
    five_sets = 0
    for vertices in combinations(range(n), 5):
        five_sets += 1
        red_pairs = sum(pair in red for pair in combinations(vertices, 2))
        if red_pairs in (0, 10):
            monochromatic.append(vertices)
    require(five_sets == 53130 and not monochromatic,
            "literal fixture has a monochromatic K5")
    return {
        "fixture_sha256": FIXTURE_SHA256,
        "vertices": n,
        "red_edges": len(red),
        "five_sets_checked": five_sets,
        "monochromatic_five_sets": len(monochromatic),
        "fixed_signatures": signatures,
        "order_three_invariant_pairs_checked": n * (n - 1) // 2,
    }


def lexicographic_prefix_audit():
    checks = 0
    for nonempty_prefix in product((0, 1), repeat=4):
        if not any(nonempty_prefix):
            continue
        for empty_suffix in product((0, 1), repeat=6):
            for nonempty_suffix in product((0, 1), repeat=6):
                require((0, 0, 0, 0) + empty_suffix < nonempty_prefix + nonempty_suffix,
                        "empty minority prefix is not lexicographically first")
                checks += 1
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    red, blue, blue_edges, red_k4s = core_audit()
    report = {
        "core": {
            "vertices": 12,
            "red_edges": len(red),
            "blue_edges": len(blue),
            "red_k4_witness_by_three_triangle_support": red_k4s,
            "blue_cross_edge_witnesses": blue_edges,
        },
        "hand_inequalities": hand_inequality_audit(blue_edges),
        "forced_blue_census": census(blue),
        "fixture": fixture_audit(red),
        "lexicographic_prefix_pairs_checked": lexicographic_prefix_audit(),
    }
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "maximum_nonempty_vertices": report["hand_inequalities"]["maximum_nonempty_vertices"],
        "equality_pattern_unique": len(report["hand_inequalities"]["maximizers"]) == 1,
        "surviving_vectors": report["forced_blue_census"]["survivors"],
        "fixture_monochromatic_k5s": report["fixture"]["monochromatic_five_sets"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
