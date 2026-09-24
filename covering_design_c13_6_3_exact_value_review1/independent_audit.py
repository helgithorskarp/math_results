#!/usr/bin/env python3
"""Independent structural audit for the C(13,6,3)=21 computation.

This script imports no module from either reviewed package. It validates the
catalogue projection, reconstructs every catalogue automorphism group by a
pair-colour backtrack followed by a block-family check, recomputes all three
decoration-orbit counts, and checks the published upper cover directly.
"""

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def blocks_from_masks(masks, points, size):
    require(len(masks) == len(set(masks)), "duplicate block")
    require(
        all(
            type(b) is int
            and 0 < b < (1 << points)
            and b.bit_count() == size
            for b in masks
        ),
        "malformed block",
    )
    return tuple(masks)


def point_degrees(blocks, points):
    return tuple(sum((b >> p) & 1 for b in blocks) for p in range(points))


def pair_colours(blocks, points):
    return tuple(
        tuple(
            0
            if p == q
            else sum(
                ((b >> p) & 1) and ((b >> q) & 1) for b in blocks
            )
            for q in range(points)
        )
        for p in range(points)
    )


def automorphisms(blocks, points):
    """All point automorphisms, without published signatures or code."""
    degrees = point_degrees(blocks, points)
    colours = pair_colours(blocks, points)
    invariants = []
    for p in range(points):
        by_degree = {}
        for q in range(points):
            if q != p:
                by_degree.setdefault(degrees[q], []).append(colours[p][q])
        invariants.append(
            (
                degrees[p],
                tuple(
                    (degree, tuple(sorted(values)))
                    for degree, values in sorted(by_degree.items())
                ),
            )
        )
    options = {
        p: tuple(q for q in range(points) if invariants[q] == invariants[p])
        for p in range(points)
    }
    block_set = set(blocks)
    action = [-1] * points
    answers = []

    def visit(used):
        if len(used) == points:
            moved = {
                sum(
                    1 << action[p]
                    for p in range(points)
                    if (b >> p) & 1
                )
                for b in blocks
            }
            if moved == block_set:
                answers.append(tuple(action))
            return
        unassigned = [p for p in range(points) if action[p] < 0]
        p = min(
            unassigned,
            key=lambda x: sum(q not in used for q in options[x]),
        )
        for q in options[p]:
            if q in used:
                continue
            if any(
                action[x] >= 0
                and colours[p][x] != colours[q][action[x]]
                for x in range(points)
            ):
                continue
            action[p] = q
            used.add(q)
            visit(used)
            used.remove(q)
            action[p] = -1

    visit(set())
    require(answers, "missing identity automorphism")
    return tuple(sorted(answers))


def set_orbits(objects, actions, move):
    left = set(objects)
    count = 0
    while left:
        item = min(left)
        orbit = {move(item, action) for action in actions}
        require(item in orbit, "identity missing from action group")
        left.difference_update(orbit)
        count += 1
    return count


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: independent_audit.py TARGET_DIR CATALOGUE_DIR")
    target = Path(sys.argv[1]).resolve()
    upstream = Path(sys.argv[2]).resolve()
    links = json.loads((target / "LINKS.json").read_text())
    catalogue = json.loads((upstream / "CATALOGUE.json").read_text())[
        "designs"
    ]
    require(len(links) == len(catalogue) == 107, "wrong catalogue size")

    fields = (
        "id",
        "blocks",
        "point_signatures",
        "point_orbits",
        "automorphism_order",
    )
    projected = [
        {field: design[field] for field in fields} for design in catalogue
    ]
    require(
        links == projected,
        "LINKS.json is not the exact upstream projection",
    )

    orbit_totals = Counter()
    aut_orders = Counter()
    all_actions = []
    for index, design in enumerate(links):
        require(design["id"] == index, "nonconsecutive catalogue id")
        blocks = blocks_from_masks(tuple(design["blocks"]), 12, 5)
        require(len(blocks) == 9, "wrong link block count")
        require(
            all(
                any(
                    (b >> p) & 1 and (b >> q) & 1 for b in blocks
                )
                for p, q in combinations(range(12), 2)
            ),
            "uncovered catalogue pair",
        )
        degrees = point_degrees(blocks, 12)
        require(
            min(degrees) >= 3 and max(degrees) <= 5,
            "catalogue degree outside 3..5",
        )
        signatures = [
            sum(
                1 << j
                for j, b in enumerate(blocks)
                if (b >> p) & 1
            )
            for p in range(12)
        ]
        require(
            signatures == design["point_signatures"],
            "signature mismatch",
        )
        actions = automorphisms(blocks, 12)
        require(
            len(actions) == design["automorphism_order"],
            "automorphism order mismatch",
        )
        computed_orbits = sorted(
            {
                tuple(sorted({action[p] for action in actions}))
                for p in range(12)
            }
        )
        require(
            computed_orbits == sorted(map(tuple, design["point_orbits"])),
            "point orbit mismatch",
        )
        aut_orders[len(actions)] += 1
        all_actions.append(actions)

        points = tuple(range(12))
        orbit_totals["twelve"] += set_orbits(
            points, actions, lambda p, action: action[p]
        )
        ordered = tuple(
            (h, q) for h in points for q in points if h != q
        )
        orbit_totals["eleven"] += set_orbits(
            ordered,
            actions,
            lambda pair, action: (action[pair[0]], action[pair[1]]),
        )
        triples = tuple(combinations(points, 3))
        orbit_totals["balanced"] += set_orbits(
            triples,
            actions,
            lambda triple, action: tuple(
                sorted(action[p] for p in triple)
            ),
        )

        for high_size in (1, 2, 3):
            for high in combinations(points, high_size):
                k = max(degrees[p] for p in points if p not in high)
                require(
                    k in (4, 5),
                    "second low point lacks link degree four or five",
                )

    require(
        dict(orbit_totals)
        == {"twelve": 954, "eleven": 8451, "balanced": 12819},
        "primary decoration orbit count mismatch",
    )
    labelled_roots = {
        "twelve": 107 * 12,
        "eleven": 107 * 12 * 11,
        "balanced": 107 * len(tuple(combinations(range(12), 3))),
    }
    require(
        labelled_roots
        == {"twelve": 1284, "eleven": 14124, "balanced": 23540},
        "audit root count mismatch",
    )

    upper_rows = json.loads((target / "UPPER21.json").read_text())[
        "blocks"
    ]
    upper = tuple(sum(1 << (p - 1) for p in row) for row in upper_rows)
    blocks_from_masks(upper, 13, 6)
    require(len(upper) == 21, "wrong upper-cover size")
    triples = tuple(
        sum(1 << p for p in triple)
        for triple in combinations(range(13), 3)
    )
    require(
        all(any((block & triple) == triple for block in upper) for triple in triples),
        "upper witness misses a triple",
    )

    result = {
        "status": "independent structural audit passed",
        "catalogue_classes": len(links),
        "catalogue_automorphisms": sum(
            len(actions) for actions in all_actions
        ),
        "automorphism_order_histogram": {
            str(order): aut_orders[order] for order in sorted(aut_orders)
        },
        "primary_decoration_orbits": dict(orbit_totals),
        "audit_labelled_roots": labelled_roots,
        "upper_blocks": len(upper),
        "upper_covered_triples": len(triples),
        "upper_point_degrees": point_degrees(upper, 13),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
