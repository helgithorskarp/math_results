"""Produce a physical, arc-consistent but unjoinable prescribed star system.

The general proof is in MATHEMATICS.md. This generator contains no search.
Its output is a finite control, not an order-44 Ramsey certificate.
"""

import argparse
import itertools
import json
from pathlib import Path


def make_fixture(s):
    if s < 5:
        raise ValueError("The proved construction requires s >= 5")
    k = s - 2
    bags = [list(range(j * k, (j + 1) * k)) for j in range(4)]
    r0, r1, w0, w1 = bags
    edges = set()

    def add(u, v):
        edges.add(tuple(sorted((u, v))))

    for bag in (r0, r1):
        for u, v in itertools.combinations(bag, 2):
            add(u, v)
    for i in range(k):
        add(r0[i], r1[i])
    for u in w0:
        for v in w1:
            add(u, v)
    for r in (r0, r1):
        for w in (w0, w1):
            for i in range(k):
                add(r[i], w[i])
    a_stars = [sorted(r0 + w1), sorted(r1 + w0)]
    b_stars = [r0, r1]
    failures = []
    for a, b, c in itertools.product(range(2), repeat=3):
        if a == b:
            color, vertices = "red", bags[a] + [4 * k, 4 * k + 1]
        elif b == c:
            color, vertices = "red", bags[b] + [4 * k + 1, 4 * k + 2]
        else:
            color, vertices = "blue", bags[2 + a] + [4 * k, 4 * k + 2]
        failures.append({"bits": [a, b, c], "color": color,
                         "vertices": sorted(vertices)})
    return {
        "schema": "physical-star-arc-control-v1",
        "scope": "prescribed subdomains, not the full unary star domain",
        "s": s,
        "core_order": 4 * k,
        "bags": dict(zip(("R0", "R1", "W0", "W1"), bags)),
        "red_edges": [list(e) for e in sorted(edges)],
        "domains": [a_stars, b_stars, a_stars],
        "root_red_edges": [[0, 1], [1, 2]],
        "expected_pair_relations": [[[False, True], [True, False]]] * 3,
        "full_failure_witnesses": failures,
        "positive_stars_outside_prescribed_domains": [a_stars[0], [], a_stars[1]],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--s", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(make_fixture(args.s), indent=2,
                                     sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
