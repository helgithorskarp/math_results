#!/usr/bin/env python3
"""Independent row-subset enumeration and literal 22-point spine controls.

Does not import the producer or use its missing-word parametrization.
Fixed test matrices are completions for selected-spine validation only;
they are not asserted to be valid Ramsey colorings.
"""
from collections import Counter
from copy import deepcopy
from itertools import combinations, product
from pathlib import Path
import argparse
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def frame(rows, edge_bits):
    # Root coordinates u=0,v=1,a=2; X=3..10,Y=11..18,T=19..21.
    graph = [[False] * 22 for _ in range(22)]

    def add(i, j):
        graph[i][j] = graph[j][i] = True

    add(0, 1)
    add(0, 2)
    add(1, 2)
    for x in range(3, 11):
        add(0, x)
    for y in range(11, 19):
        add(1, y)
    special = (3, 4, 11, 12)
    for s in special:
        add(2, s)
    for t in range(19, 22):
        add(2, t)
    # Give each special exactly two neighbors inside its own block.
    # These specified edges make all the special red/blue spine bounds tight.
    for s, others in ((3, (5, 6)), (4, (7, 8)),
                      (11, (13, 14)), (12, (15, 16))):
        for z in others:
            add(s, z)
    for t, subset in enumerate(rows):
        for position in subset:
            add(19 + t, special[position])
    for bit, (i, j) in enumerate(((19, 20), (19, 21), (20, 21))):
        if edge_bits & (1 << bit):
            add(i, j)
    return graph


def pages(graph, i, j, red=True):
    return sum(graph[i][k] == red and graph[j][k] == red
               for k in range(22) if k not in (i, j))


def triangles(graph):
    return sum(graph[i][j] and graph[i][k] and graph[j][k]
               for i, j, k in combinations(range(len(graph)), 3))


def fresh_record():
    # All 16 subsets in each of three T rows: exactly 4096 row triples.
    subsets = tuple(frozenset(i for i in range(4) if mask & (1 << i))
                    for mask in range(16))
    counts = {str(e): {"candidates": 0, "survivors": 0} for e in range(4)}
    accepted = set()
    profiles = Counter()
    row_trials = 0
    orbit_sizes = Counter()
    specials = (3, 4, 11, 12)
    for rows in product(subsets, repeat=3):
        row_trials += 1
        if any(sum(position in r for r in rows) != 2 for position in range(4)):
            continue
        for edges in range(8):
            graph = frame(rows, edges)
            require([sum(graph[r]) for r in (0, 1, 2)] == [10, 10, 9],
                    "root/mark degrees")
            require([k for k in range(22) if graph[0][k] and graph[1][k]] == [2],
                    "single red page")
            require(pages(graph, 0, 2) == pages(graph, 1, 2) == 3,
                    "red root--mark pages")
            for position, s in enumerate(specials):
                root, other = (0, 1) if position < 2 else (1, 0)
                require(pages(graph, root, s) == 3, "special red-root pages")
                require(pages(graph, other, s, red=False) == 6,
                        "special blue-root pages")
                require(pages(graph, 2, s) == 3, "mark--special pages")
            e = sum(graph[i][j] for i, j in ((19, 20), (19, 21), (20, 21)))
            counts[str(e)]["candidates"] += 1
            if any(pages(graph, 2, t) > 3 for t in range(19, 22)):
                continue
            counts[str(e)]["survivors"] += 1
            # Encode from actual entries, rather than the producer's missing word.
            word = sum(int(graph[s][19 + t]) << (3 * position + t)
                       for position, s in enumerate(specials) for t in range(3))
            word += sum(int(graph[i][j]) << (12 + bit)
                        for bit, (i, j) in enumerate(((19, 20), (19, 21), (20, 21))))
            require(word not in accepted, "duplicate literal core")
            accepted.add(word)
            vertices = [i for i in range(22) if graph[2][i]]
            local = [[graph[i][j] for j in vertices] for i in vertices]
            degree = sorted(sum(r) for r in local)
            require(degree == [2] + [3] * 8, "degree-nine neighborhood degrees")
            require(triangles(local) == 0, "degree-nine neighborhood triangles")
            require(sum(degree) // 2 == 13, "degree-nine neighborhood edges")
            profiles[tuple(degree)] += 1
            unique = degree.count(2)
            require(unique == 1, "unique suppressible vertex")
            z = next(i for i, row in enumerate(local) if sum(row) == 2)
            endpoints = [i for i in range(9) if local[z][i]]
            require(not local[endpoints[0]][endpoints[1]], "simple suppression")
            keep = [i for i in range(9) if i != z]
            cubic = [[local[i][j] for j in keep] for i in keep]
            p, q = (keep.index(i) for i in endpoints)
            cubic[p][q] = cubic[q][p] = True
            require(all(sum(r) == 3 for r in cubic), "suppressed cubic degrees")
            number = triangles(cubic)
            same = (endpoints[0] in (vertices.index(3), vertices.index(4))
                    and endpoints[1] in (vertices.index(3), vertices.index(4)))
            same |= (endpoints[0] in (vertices.index(11), vertices.index(12))
                     and endpoints[1] in (vertices.index(11), vertices.index(12)))
            require(number == int(same), "suppressed triangle orbit")
            orbit_sizes["same_block" if same else "cross_block"] += 1
    require(row_trials == 4096, "complete row domain")
    require(len(accepted) == 36 and counts["0"]["candidates"] == 81,
            "unexpected necessary core cardinalities")
    return {
        "domain_size": sum(c["candidates"] for c in counts.values()),
        "by_T_edges": counts, "survivors": len(accepted),
        "core_words": sorted(accepted),
        "labeled_orbits": dict(sorted(orbit_sizes.items())),
        "neighborhood_edges": 13, "neighborhood_degrees": [2] + [3] * 8,
        "neighborhood_triangles": 0,
        "suppressed_cubic_triangles": {"same_block": 1, "cross_block": 0},
    }


def validate(candidate, actual):
    require(isinstance(candidate, dict), "record object required")
    require(isinstance(candidate.get("core_words"), list), "core list required")
    require(all(type(w) is int for w in candidate["core_words"]),
            "literal integer core words required")
    require(len(set(candidate["core_words"])) == len(candidate["core_words"]),
            "duplicate listed core")
    for key, value in actual.items():
        require(candidate.get(key) == value, "frozen record differs at " + key)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    stored = json.loads((Path(__file__).parent / "EXPECTED.json").read_text())
    actual = fresh_record()
    validate(stored, actual)
    if args.self_test:
        tests = []
        changed = deepcopy(stored); changed["core_words"].pop(); tests.append(changed)
        changed = deepcopy(stored); changed["core_words"].append(changed["core_words"][0]); tests.append(changed)
        changed = deepcopy(stored); changed["core_words"][0] ^= 1; tests.append(changed)
        changed = deepcopy(stored); changed["core_words"][0] = True; tests.append(changed)
        changed = deepcopy(stored); changed["by_T_edges"]["1"]["survivors"] = 1; tests.append(changed)
        changed = deepcopy(stored); changed["labeled_orbits"]["same_block"] = 24; tests.append(changed)
        for damage in tests:
            try:
                validate(damage, actual)
            except ValueError:
                continue
            raise ValueError("a concrete damaged record was accepted")
        print(json.dumps({"damages_rejected": len(tests)}, sort_keys=True))
    else:
        print(json.dumps(actual, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
