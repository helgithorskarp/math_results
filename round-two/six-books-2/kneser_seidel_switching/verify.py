#!/usr/bin/env python3
"""Set-based controls of the written proof and its independently swept cuts."""

import argparse
import collections
import hashlib
import itertools
import json
import re
from pathlib import Path

ROOTS = frozenset(range(7))
PAIRS = tuple(itertools.combinations(range(7), 2))
POINTS = tuple(map(frozenset, PAIRS))


def edge(a, b):
    return tuple(sorted((a, b)))


def clique(vertices):
    return frozenset(itertools.combinations(sorted(vertices), 2))


def join(universal, leaves):
    return clique(universal) | frozenset(edge(a, b)
                                        for a in universal for b in leaves)


def graph(switch):
    if not switch <= frozenset(PAIRS):
        raise ValueError("Not a root edge set")
    neighbors = [set() for _ in PAIRS]
    for i, j in itertools.combinations(range(21), 2):
        red = POINTS[i].isdisjoint(POINTS[j])
        if (PAIRS[i] in switch) != (PAIRS[j] in switch):
            red = not red
        if red:
            neighbors[i].add(j)
            neighbors[j].add(i)
    return neighbors


def pages(neighbors, i, j):
    red = j in neighbors[i]
    return red, {k for k in range(21) if k != i and k != j
                 and ((k in neighbors[i]) == red)
                 and ((k in neighbors[j]) == red)}


def record(switch):
    neighbors = graph(switch)
    maxima = [0, 0]
    hist = [collections.Counter(), collections.Counter()]
    for i, j in itertools.combinations(range(21), 2):
        red, common = pages(neighbors, i, j)
        maxima[red] = max(maxima[red], len(common))
        hist[red][len(common)] += 1
    cut = sum(1 << i for i, pair in enumerate(PAIRS) if pair in switch)
    if cut & 1:
        cut ^= (1 << 21) - 1
    return [cut, maxima[1], maxima[0]], hist


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def controls():
    table = [
        (clique(range(3)), (0, 3), (1, 4), True, 4),
        (clique(range(4)), (4, 5), (4, 6), False, 11),
        (clique(range(5)), (0, 1), (5, 6), False, 12),
        (clique(range(6)), (0, 6), (1, 6), False, 10),
        (join({3, 4}, {0, 1, 2}), (0, 1), (3, 5), True, 4),
        (join({4, 5}, {0, 1, 2, 3}), (0, 6), (4, 5), False, 12),
        (join({3, 4, 5}, {0, 1, 2}), (0, 6), (3, 4), False, 11),
    ]
    page_words = [
        "01 25 26 56",
        "01 02 03 12 13 23 04 14 24 34 56",
        "02 03 04 12 13 14 25 26 35 36 45 46",
        "23 24 25 26 34 35 36 45 46 56",
        "03 13 26 46",
        "01 02 03 16 26 36 14 15 24 25 34 35",
        "01 02 16 26 56 23 24 13 14 35 45",
    ]
    written = re.findall(r"\{[0-6][0-6](?:,[0-6][0-6])*\}",
                         Path(__file__).with_name("PROOF.md").read_text())
    proof_sets = [set(group[1:-1].split(",")) for group in written]
    require(proof_sets == [set(page_words[i].split())
                           for i in (0, 4, 1, 2, 3, 5, 6)],
            "Published proof page lists differ from the checked books")
    for (switch, e, f, color, count), words in zip(table, page_words):
        neighbors = graph(switch)
        actual_color, common = pages(neighbors, PAIRS.index(e), PAIRS.index(f))
        require(actual_color == color and len(common) == count,
                "Written book table mismatch")
        written_pages = {PAIRS.index(tuple(map(int, word))) for word in words.split()}
        require(common == written_pages, "Written literal page set mismatch")
        require(neighbors == graph(frozenset(PAIRS) - switch),
                "Switch complement changed the graph")

    # The red-spine identity uses only the eight edges aT,bT. Check all
    # their assignments with irrelevant edges all absent and all present.
    # Its universal validity is established by the written page bijection.
    v, a, b = 0, 1, 2
    local = tuple(edge(x, t) for x in (a, b) for t in (3, 4, 5, 6))
    irrelevant = frozenset(PAIRS) - frozenset(local) - {edge(v, a), edge(v, b)}
    identity_checks = 0
    for word in range(1 << 8):
        chosen = {local[i] for i in range(8) if word >> i & 1}
        for outside in (frozenset(), irrelevant):
            switch = frozenset(chosen | outside | {edge(v, a)})
            degrees = {x: sum(x in e for e in switch) for x in ROOTS}
            red, common = pages(graph(switch), PAIRS.index(edge(v, a)),
                                PAIRS.index(edge(v, b)))
            require(red and len(common) == 5 + degrees[b] - degrees[a],
                    "Local red-page identity mismatch")
            identity_checks += 1

    baseline, baseline_hist = record(frozenset())
    require(baseline == [0, 3, 5], "Kneser baseline mismatch")
    require(baseline_hist[1] == {3: 105} and baseline_hist[0] == {5: 105},
            "Kneser spine census mismatch")
    sharp, sharp_hist = record(clique(range(6)))
    require(sharp[1:] == [1, 10] and sharp_hist[1] == {0: 30, 1: 45}
            and sharp_hist[0] == {7: 60, 9: 60, 10: 15},
            "Sharpness page census mismatch")
    return {"literal_book_rows": len(table),
            "local_identity_checks": identity_checks,
            "sharp_red_histogram": dict(sorted(sharp_hist[1].items())),
            "sharp_blue_histogram": dict(sorted(sharp_hist[0].items()))}


def predicted_records():
    switches = {frozenset()}
    for size in (4, 5, 6):
        switches.update(clique(support)
                        for support in itertools.combinations(sorted(ROOTS), size))
    for isolated in ROOTS:
        support = ROOTS - {isolated}
        for size in (2, 3):
            switches.update(join(frozenset(u), support - frozenset(u))
                            for u in itertools.combinations(sorted(support), size))
    records = sorted(record(switch)[0] for switch in switches)
    require(len(records) == 309 and len({r[0] for r in records}) == 309,
            "The explicit root-shape orbit domain has changed")
    require(all(r[1] <= 3 for r in records), "Predicted cut has red B4")
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census", type=Path,
                        help="Compare every record from enumerate.py")
    args = parser.parse_args()
    result = controls()
    records = predicted_records()
    digest = hashlib.sha256(json.dumps(records, separators=(",", ":"))
                            .encode("ascii")).hexdigest()
    expected = json.loads(Path(__file__).with_name("expected.json").read_text())
    summary = {"cuts_scanned": 1 << 20, "red_B4_free_cuts": len(records),
               "maximum_blue_pages_histogram": dict(sorted(collections.Counter(
                   str(r[2]) for r in records).items(), key=lambda x: int(x[0]))),
               "record_sha256": digest}
    require(summary == expected, "Expected compact fixture mismatch")
    if args.census:
        observed = json.loads(args.census.read_text())
        require(observed.pop("records") == records, "Entrywise cut census mismatch")
        require(observed == summary, "Full census coverage or summary mismatch")
    result.update({"explicit_root_shape_cuts": len(records),
                   "record_sha256": digest,
                   "full_census_compared": args.census is not None})
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
