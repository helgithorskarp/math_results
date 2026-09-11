#!/usr/bin/env python3
"""Exact finite controls for the human exclusion of all z12,A2 graphs.

Python 3.11+, standard library. No solver or 54-vertex graph enumeration.
"""
import hashlib
import json
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from math import comb


def require(condition, message):
    if not condition:
        raise ValueError(message)


def stream_hash(rows):
    h = hashlib.sha256()
    for row in rows:
        h.update((",".join(map(str, row)) + "\n").encode())
    return h.hexdigest()


def colored_edge_packing():
    edges = list(combinations(range(5), 2))
    sets = list(map(frozenset, edges))
    matchings = [()] + [(i,) for i in range(10)] + [
        (i, j) for i, j in combinations(range(10), 2)
        if sets[i].isdisjoint(sets[j])
    ]
    require(len(matchings) == 26, "matching list on five labeled points")
    matching_words = []
    for classes in product(matchings, repeat=3):
        if any(set(a) & set(b) for a, b in combinations(classes, 2)):
            continue
        word = [0]*10
        for color, matching in enumerate(classes, 1):
            for i in matching:
                word[i] = color
        matching_words.append(tuple(word))
    matching_words.sort()

    # Independent search: every edge is absent or has one of three colors.
    # Check the definition at each endpoint; no matching list is used.
    direct_words = []
    for word in product(range(4), repeat=10):
        used = [set() for _ in range(3)]
        good = True
        for i, color in enumerate(word):
            if not color:
                continue
            if used[color-1] & sets[i]:
                good = False
                break
            used[color-1].update(sets[i])
        if good:
            direct_words.append(word)
    require(direct_words == matching_words, "entrywise colored-graph comparison")

    hist = Counter()
    for word in direct_words:
        selected = [(i, c) for i, c in enumerate(word) if c]
        score = sum(c != d and sets[i].isdisjoint(sets[j])
                    for (i, c), (j, d) in combinations(selected, 2))
        # Recover the actual high triples on B={0,1,2}, O={3,...,7}.
        triples = [frozenset([c-1] + [x+3 for x in edges[i]])
                   for i, c in selected]
        require(all(len(a & b) <= 1 for a, b in combinations(triples, 2)),
                "triple linearity")
        partitions = []
        for i, j in combinations(range(len(triples)), 2):
            a, b = triples[i], triples[j]
            remaining = frozenset(range(8)) - a - b
            if a.isdisjoint(b):
                require(len(remaining) == 2 and len(remaining & {0, 1, 2}) == 1,
                        "complementary bad two-set")
                partitions.append((i, j, remaining))
        require(len(partitions) == score, "graph pairs versus actual partitions")
        # Each remaining high two-set must be unique in a graph. This test
        # allows duplicates; the proof only needs the weaker pair bound.
        r = len(selected)
        deg = [sum(v in edges[i] for i, _ in selected) for v in range(5)]
        sizes = [word.count(c) for c in (1, 2, 3)]
        identity = comb(r, 2) - sum(comb(d, 2) for d in deg) - sum(comb(a, 2) for a in sizes)
        require(identity == score and score <= 3, "colored disjoint-pair formula")
        hist[(r, score)] += 1
    counts = [sum(n for (r, p), n in hist.items() if r == k) for k in range(7)]
    maxima = [max(p for (r, p), n in hist.items() if r == k) for k in range(7)]
    require(counts == [1, 30, 315, 1440, 2970, 2700, 870], "all colored graphs")
    require(maxima == [0, 0, 1, 2, 2, 3, 3], "colored packing maxima")
    return {
        "matching_triples_examined": 26**3,
        "edge_words_examined": 4**10,
        "valid_colored_graphs": len(direct_words),
        "counts_by_size": counts,
        "maxima_by_size": maxima,
        "histogram": [[r, p, n] for (r, p), n in sorted(hist.items())],
        "entry_stream_sha256": stream_hash(direct_words)
    }


def arithmetic_table():
    rows = []
    for r in range(7):
        vertex_min = min(sum(comb(d, 2) for d in ds)
                         for ds in product(range(4), repeat=5) if sum(ds) == 2*r)
        color_min = min(sum(comb(a, 2) for a in sizes)
                        for sizes in product(range(3), repeat=3) if sum(sizes) == r)
        bound = comb(r, 2) - vertex_min - color_min
        require(bound <= 3, "integer minimum upper bound")
        rows.append([r, vertex_min, color_min, bound])
    require(rows == [[0, 0, 0, 0], [1, 0, 0, 0], [2, 0, 0, 1],
                     [3, 1, 0, 2], [4, 3, 1, 2], [5, 5, 2, 3],
                     [6, 9, 3, 3]], "convexity table")
    return rows


def incidence_cover():
    universe = set(range(12))
    q1, q2 = {0, 1, 2, 3}, {0, 4, 5, 6}
    outside = set(range(7, 12))
    triples = [
        frozenset(t) for t in combinations(range(12), 3)
        if len(set(t) & q1) <= 1 and len(set(t) & q2) <= 1
    ]
    require(len(triples) == 125, "complete triple inventory")
    singles = []
    doubles = []
    two_far_formats = 0
    singleton_formats = 0
    for y_tuple in combinations(range(12), 2):
        y = set(y_tuple)
        if len(y & q1) > 1 or len(y & q2) > 1:
            continue
        for qi, qj in ((q1, q2), (q2, q1)):
            for u, v in combinations(triples, 2):
                if len(u & v) > 1 or not all(y.isdisjoint(z) for z in (qi, u, v)):
                    continue
                blocks = [y, qi, u, v]
                multiplicities = [sum(t in z for z in blocks) for t in range(12)]
                if min(multiplicities) < 1:
                    continue
                require(multiplicities == [1]*12, "single-quad correction vanishes")
                require(len(u & (qj-qi)) == len(v & (qj-qi)) == 1,
                        "one of three colors per triple")
                require(len(u & outside) == len(v & outside) == 2,
                        "two outside points per triple")
                singles.append((tuple(sorted(qi)), y_tuple, tuple(sorted(u)), tuple(sorted(v))))
        for u in triples:
            if not all(y.isdisjoint(z) for z in (q1, q2, u)):
                continue
            blocks = [y, q1, q2, u]
            mult = [sum(t in z for z in blocks) for t in range(12)]
            if min(mult) < 1:
                continue
            require(mult == [2] + [1]*11 and u <= outside,
                    "both-quad unique repeated point and outside triple")
            require(y == outside-set(u), "both-quad complementary two-set")
            doubles.append((y_tuple, tuple(sorted(u))))
        for u in map(set, combinations(range(12), 2)):
            if universe <= y | q1 | q2 | u:
                two_far_formats += 1
    require(two_far_formats == 0, "4+4+2 cannot cover with own two-set")
    for y in range(12):
        for u in triples:
            if universe <= {y} | q1 | q2 | set(u):
                singleton_formats += 1
    require(singleton_formats == 0, "negative singleton type cannot cover")

    # Linear triples entirely in the five-point outside set: direct all
    # subfamilies, including the empty family, without size truncation.
    outside_triples = list(map(frozenset, combinations(range(5), 3)))
    families = []
    for mask in range(1 << len(outside_triples)):
        selected = [outside_triples[i] for i in range(10) if mask >> i & 1]
        if all(len(a & b) <= 1 for a, b in combinations(selected, 2)):
            families.append(mask)
            require(len(selected) <= 2, "at most two both-quad helper triples")
    require(len(singles) == 180 and len(doubles) == 10, "complete far-cover templates")
    return {
        "admissible_triples": len(triples),
        "single_quad_templates_per_quad": len(singles)//2,
        "both_quad_templates": len(doubles),
        "both_quad_size2_helper_templates": two_far_formats,
        "singleton_negative_templates": singleton_formats,
        "outside_linear_triple_families": len(families),
        "outside_maximum_family_size": max(mask.bit_count() for mask in families),
        "both_quad_extra_multiplicity": {"point": 0, "extra": 1}
    }


def sign_and_far_sizes():
    negative = set()
    for d, cs in ((6, (2, 3, 4)), (7, (1, 2))):
        for c in cs:
            for a in range(d-c+1):
                b = d-a-c
                eps = b + 2*c - (8 if d == 6 else 7)
                if (c-3)*eps < 0:
                    negative.add((d, c, eps))
    require(sorted(negative) == [(7, 1, 1), (7, 2, 1), (7, 2, 2)],
            "negative sign types")
    formats = {}
    for c, eps in ((1, 1), (2, 1), (2, 2)):
        formats[f"c{c}_epsilon{eps}"] = [
            sizes for sizes in combinations_with_replacement(range(1, 5), 4-eps)
            if sizes.count(4) <= 2 and sum(sizes) >= 12-c
        ]
    require(formats == {"c1_epsilon1": [(3, 4, 4)],
                        "c2_epsilon1": [(2, 4, 4), (3, 3, 4), (3, 4, 4)],
                        "c2_epsilon2": []}, "exhaustive far-size possibilities")
    require(3*6-8 == 10 and 3+3+2 == 8 and 8 < 10, "closing contradiction")
    return {"negative_types": sorted(negative), "far_size_formats_before_cover": formats,
            "bad_lower_bound": 10, "bad_upper_bound": 8}


def main():
    result = {
        "claim": "All z12,A2 graphs are impossible, so total high distant incidences A<=1",
        "proof_role": "finite controls for a human incidence proof; imports preceding classification and matching exclusion",
        "colored_edge_packing": colored_edge_packing(),
        "convexity_table_r_vertex_min_color_min_bound": arithmetic_table(),
        "incidence_cover": incidence_cover(),
        "local": sign_and_far_sizes()
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
