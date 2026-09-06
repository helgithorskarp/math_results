#!/usr/bin/env python3
"""Independent audit of the score-123 C3 phase-family obstruction.

This checker uses only Python's standard library and imports no code from the
reviewed package.  Red edges are listed; every omitted edge is blue.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import csv
import json
from pathlib import Path
import sys


N = 43
ROOT = 42
ALL = (1 << N) - 1
EXPECTED_SHA256 = {
    "baseline.edges": "36c4a4ff6359e56ece7c9a6b41e35fae02cb04d72e56d832dc1a4dc056c6e88e",
    "traded.edges": "6a971024aacc5f1311665b9fd0934388e200af4811fb7eeb1d04ff79d7c1250b",
    "best.edges": "ff1c0922aa3aee7252a46635dec5980263ea70a084a258e9ab8c090542282979",
}
EXPECTED_PARENT_HISTOGRAM = {0: 10, 1: 33, 2: 40, 3: 8}
EXPECTED_PARENT_FIXED_BLUE = [
    (6, 30, 31, 32, 42),
    (7, 30, 31, 32, 42),
    (8, 30, 31, 32, 42),
]
EXPECTED_TRADE = {
    (2, 10): 1,
    (0, 5): 1,
    (0, 2): -1,
    (5, 10): -1,
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def canonical(u, v):
    return (u, v) if u < v else (v, u)


def rotate(v):
    return v if v == ROOT else 3 * (v // 3) + (v + 1) % 3


def read_graph(path):
    raw = path.read_bytes()
    lines = raw.decode("ascii").splitlines()
    require(lines and lines[0] == str(N), f"bad order in {path.name}")
    parsed = [tuple(map(int, line.split())) for line in lines[1:]]
    require(all(0 <= u < v < N for u, v in parsed), f"bad edge in {path.name}")
    require(parsed == sorted(set(parsed)), f"noncanonical edge list in {path.name}")
    require(len(parsed) == 453, f"wrong red-edge count in {path.name}")
    edges = set(parsed)
    rows = [0] * N
    for u, v in edges:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return raw, edges, rows


def red(edges, u, v):
    return canonical(u, v) in edges


def degree_histogram(rows):
    return dict(sorted(Counter(row.bit_count() for row in rows).items()))


def analyze_structure(edges):
    rotated = {canonical(rotate(u), rotate(v)) for u, v in edges}
    require(rotated == edges, "graph is not invariant under the stated C3 action")

    for i in range(14):
        colors = {red(edges, u, v) for u, v in combinations(range(3 * i, 3 * i + 3), 2)}
        require(colors == {i < 7}, f"unexpected internal color for triangle {i}")

    hub = []
    for i in range(14):
        contacts = {red(edges, 3 * i + s, ROOT) for s in range(3)}
        require(len(contacts) == 1, f"nonconstant root contact at triangle {i}")
        hub.append(int(contacts.pop()))

    offsets = {}
    counts = {}
    for i, j in combinations(range(14), 2):
        bits = []
        covered = set()
        for d in range(3):
            matching = {canonical(3 * i + s, 3 * j + (s + d) % 3) for s in range(3)}
            require(len(matching) == 3 and not (covered & matching), "matching partition failure")
            covered |= matching
            colors = {edge in edges for edge in matching}
            require(len(colors) == 1, f"non-invariant matching on pair {(i, j)}")
            bits.append(int(colors.pop()))
        require(len(covered) == 9, f"incomplete K3,3 partition on pair {(i, j)}")
        offsets[(i, j)] = tuple(bits)
        counts[(i, j)] = sum(bits)
    return hub, offsets, counts


def fixed_rows(counts, hub, color):
    rows = [0] * N
    for u, v in combinations(range(N), 2):
        if v == ROOT:
            value = hub[u // 3]
        elif u // 3 == v // 3:
            value = int(u // 3 < 7)
        else:
            multiplicity = counts[tuple(sorted((u // 3, v // 3)))]
            value = 0 if multiplicity == 0 else 1 if multiplicity == 3 else None
        if value == color:
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return rows


def cliques(rows, size, candidates=ALL, prefix=()):
    if size == 0:
        yield prefix
        return
    while candidates.bit_count() >= size:
        bit = candidates & -candidates
        candidates ^= bit
        vertex = bit.bit_length() - 1
        yield from cliques(rows, size - 1, candidates & rows[vertex], prefix + (vertex,))


def fixed_fives(counts, hub):
    return [list(cliques(fixed_rows(counts, hub, color), 5)) for color in (0, 1)]


def physical_defects(rows, include_lists=False):
    blue = [ALL ^ rows[u] ^ (1 << u) for u in range(N)]
    if include_lists:
        return [list(cliques(blue, 5)), list(cliques(rows, 5))]
    return [sum(1 for _ in cliques(blue, 5)), sum(1 for _ in cliques(rows, 5))]


def rows_to_edges(rows):
    return {(u, v) for u, v in combinations(range(N), 2) if rows[u] & (1 << v)}


def flip_matching(edges, pair, offset):
    i, j = pair
    result = set(edges)
    for s in range(3):
        edge = canonical(3 * i + s, 3 * j + (s + offset) % 3)
        if edge in result:
            result.remove(edge)
        else:
            result.add(edge)
    return result


def make_rows(edges):
    rows = [0] * N
    for u, v in edges:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return rows


def decode_phases(base_edges, counts, word):
    mixed = [pair for pair in combinations(range(14), 2) if counts[pair] in (1, 2)]
    require(len(word) == len(mixed) and set(word) <= {"0", "1", "2"}, "bad phase word")
    edges = set(base_edges)
    for pair, digit in zip(mixed, word):
        i, j = pair
        for u in range(3 * i, 3 * i + 3):
            for v in range(3 * j, 3 * j + 3):
                edges.discard((u, v))
        excluded_or_selected = int(digit)
        for d in range(3):
            is_red = d == excluded_or_selected if counts[pair] == 1 else d != excluded_or_selected
            if is_red:
                for s in range(3):
                    edges.add((3 * i + s, 3 * j + (s + d) % 3))
    return edges, make_rows(edges)


def splitmix_phases(seed, size):
    mask = (1 << 64) - 1
    digits = []
    for _ in range(size):
        seed = (seed + 0x9E3779B97F4A7C15) & mask
        value = seed
        value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & mask
        value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & mask
        value ^= value >> 31
        digits.append(str(value % 3))
    return "".join(digits)


def find_first_trade(parent_counts, hub):
    attempts = []
    for k in range(14):
        for ell in range(14):
            if len({2, 10, k, ell}) < 4:
                continue
            signed = [((2, 10), 1), (tuple(sorted((k, ell))), 1),
                      (tuple(sorted((2, k))), -1), (tuple(sorted((10, ell))), -1)]
            counts = dict(parent_counts)
            for pair, delta in signed:
                counts[pair] += delta
            if any(value < 0 or value > 3 for value in counts.values()):
                continue
            fixed = fixed_fives(counts, hub)
            attempts.append((k, ell, len(fixed[0]), len(fixed[1])))
            if not fixed[0] and not fixed[1]:
                return k, ell, signed, counts, attempts
    raise AssertionError("no admissible trade")


def verify_phase_endpoints(package, base_edges, traded_edges, traded_counts, best_edges):
    records = list(csv.DictReader((package / "restarts.tsv").open(), delimiter="\t"))
    require(len(records) == 16, "restart count")
    summaries = []
    decoded = []
    for index, record in enumerate(records):
        require(int(record["restart"]) == index, "restart index")
        require(int(record["seed"]) == 2026090621 + index, "restart seed")
        require(int(record["steps_done"]) == 25000, "incomplete restart")
        require(0 <= int(record["best_step"]) <= 25000, "best-step range")
        edges, rows = decode_phases(traded_edges, traded_counts, record["phases"])
        counts = physical_defects(rows)
        require(sum(counts) == int(record["best"]), f"bad saved score at restart {index}")
        initial_word = record["phases"] if index == 0 else splitmix_phases(int(record["seed"]), 76)
        if index == 0:
            initial_edges, initial_rows = traded_edges, make_rows(traded_edges)
        else:
            initial_edges, initial_rows = decode_phases(traded_edges, traded_counts, initial_word)
        require(len(initial_edges) == 453, "initial edge count")
        require(sum(physical_defects(initial_rows)) == int(record["initial"]), "bad initial score")
        summaries.append({"restart": index, "score": sum(counts), "blue_red": counts})
        decoded.append(edges)
    first = min(range(len(records)), key=lambda i: int(records[i]["best"]))
    require(decoded[first] == best_edges, "best.edges is not the first saved winner")
    status = json.loads((package / "status.json").read_text())
    require(status.get("complete") is True and status.get("candidate_target") is False,
            "search status does not describe a completed non-target batch")
    require(sum(int(record["steps_done"]) for record in records) == 400000, "move total")
    return summaries


def main():
    require(len(sys.argv) == 2, "usage: independent_check.py REVIEWED_PACKAGE")
    package = Path(sys.argv[1]).resolve()
    graphs = {}
    for name, digest in EXPECTED_SHA256.items():
        raw, edges, rows = read_graph(package / name)
        require(sha256(raw).hexdigest() == digest, f"SHA-256 mismatch for {name}")
        graphs[name] = (edges, rows)

    base_edges, base_rows = graphs["baseline.edges"]
    traded_edges, traded_rows = graphs["traded.edges"]
    best_edges, best_rows = graphs["best.edges"]
    base_hub, base_offsets, base_counts = analyze_structure(base_edges)
    traded_hub, traded_offsets, traded_counts = analyze_structure(traded_edges)
    analyze_structure(best_edges)

    require(degree_histogram(base_rows) == {20: 6, 21: 28, 22: 9}, "parent degrees")
    require([row.bit_count() for row in base_rows] == [row.bit_count() for row in traded_rows],
            "trade does not preserve every labeled degree")
    require([row.bit_count() for row in traded_rows] == [row.bit_count() for row in best_rows],
            "phase endpoint changed a labeled degree")
    require(base_hub == traded_hub, "root contacts changed")
    require(Counter(base_counts.values()) == Counter(EXPECTED_PARENT_HISTOGRAM), "parent counts")
    require(sum(value in (1, 2) for value in base_counts.values()) == 73, "parent variable count")
    require(3 ** 73 == 67585198634817523235520443624317923, "parent family size")

    # Each mixed pair exposes three different labeled matching patterns.  Pair
    # edge sets are disjoint, so the direct product map to labeled graphs is injective.
    phase_patterns = 0
    used_pair_edges = set()
    for pair, bits in base_offsets.items():
        if sum(bits) not in (1, 2):
            continue
        patterns = []
        i, j = pair
        pair_edges = {canonical(3 * i + s, 3 * j + t) for s in range(3) for t in range(3)}
        require(not (used_pair_edges & pair_edges), "different pair coordinates overlap")
        used_pair_edges |= pair_edges
        for phase in range(3):
            pattern = frozenset(
                canonical(3 * i + s, 3 * j + (s + d) % 3)
                for d in range(3) for s in range(3)
                if (d == phase if sum(bits) == 1 else d != phase)
            )
            patterns.append(pattern)
        require(len(set(patterns)) == 3, f"non-injective phase at {pair}")
        phase_patterns += len(patterns)
    require(phase_patterns == 219, "phase-pattern count")

    parent_fixed = fixed_fives(base_counts, base_hub)
    require(parent_fixed[0] == EXPECTED_PARENT_FIXED_BLUE and parent_fixed[1] == [],
            "unexpected parent fixed-color five-sets")
    for witness in EXPECTED_PARENT_FIXED_BLUE:
        require(all(not red(base_edges, u, v) for u, v in combinations(witness, 2)),
                f"displayed witness is not blue: {witness}")

    delta = {pair: traded_counts[pair] - base_counts[pair] for pair in base_counts}
    require({pair: value for pair, value in delta.items() if value} == EXPECTED_TRADE, "count trade")
    require(sum(value in (1, 2) for value in traded_counts.values()) == 76, "traded variable count")
    require(3 ** 76 == 1824800363140073127359051977856583921, "traded family size")
    require(fixed_fives(traded_counts, traded_hub) == [[], []], "traded fixed-color K5")

    k, ell, signed, selected_counts, attempts = find_first_trade(base_counts, base_hub)
    require((k, ell) == (0, 5), "wrong first lexicographic trade")
    require(attempts == [(0, 1, 0, 6), (0, 3, 0, 21), (0, 4, 3, 0), (0, 5, 0, 0)],
            "unexpected lexicographic trade prefix")
    require(selected_counts == traded_counts, "selected quotient does not match traded graph")
    require(dict(signed) == EXPECTED_TRADE, "selected signed trade")

    # Exhaust the 3*3*2*3 = 54 single-matching realizations of the four
    # multiplicity changes and independently score each physical graph.
    choices = []
    for pair, change in signed:
        old = base_offsets[pair]
        choices.append([d for d, bit in enumerate(old) if bit == (0 if change == 1 else 1)])
    require([len(choice) for choice in choices] == [3, 3, 2, 3], "realization counts")
    realization_scores = []
    realization_edges = []
    for offsets in product(*choices):
        edges = set(base_edges)
        for (pair, _), offset in zip(signed, offsets):
            edges = flip_matching(edges, pair, offset)
        rows = make_rows(edges)
        realization_scores.append(sum(physical_defects(rows)))
        realization_edges.append(edges)
    require(len(realization_scores) == 54 and min(realization_scores) == 186, "54-way trade score")
    first_minimum = realization_scores.index(min(realization_scores))
    require(realization_edges[first_minimum] == traded_edges, "traded graph is not first minimum")
    require(sum(physical_defects(traded_rows)) == 186, "traded score")

    restart_summaries = verify_phase_endpoints(
        package, base_edges, traded_edges, traded_counts, best_edges
    )
    best_defects = physical_defects(best_rows, include_lists=True)
    require([len(part) for part in best_defects] == [123, 54], "best endpoint score split")
    require(all(item["score"] == 177 for item in restart_summaries), "saved restart best scores")

    report = {
        "status": "INDEPENDENTLY_VERIFIED_SCOPED_PHASE_FAMILY_OBSTRUCTION",
        "reviewed_package": package.name,
        "parent": {
            "red_edges": len(base_edges),
            "degree_histogram": degree_histogram(base_rows),
            "multiplicity_histogram": dict(sorted(Counter(base_counts.values()).items())),
            "phase_variables": 73,
            "labeled_family_size": 3 ** 73,
            "distinct_phase_patterns_checked": phase_patterns,
            "fixed_blue_K5": [list(q) for q in parent_fixed[0]],
            "fixed_red_K5": [],
            "universal_defect_lower_bound": 3,
        },
        "trade": {
            "first_lexicographic_k_l": [k, ell],
            "attempts_blue_red": [list(item) for item in attempts],
            "degree_preserved_per_label": True,
            "changed_multiplicities": {f"{i},{j}": value for (i, j), value in delta.items() if value},
            "phase_variables": 76,
            "labeled_family_size": 3 ** 76,
            "fixed_blue_red": [0, 0],
            "realizations_scored": 54,
            "first_minimum_score": 186,
        },
        "bounded_experiment_fixture": {
            "restarts": len(restart_summaries),
            "recorded_moves": 400000,
            "all_saved_best_scores": sorted({item["score"] for item in restart_summaries}),
            "first_winner_blue_red": [len(part) for part in best_defects],
            "exhaustive": False,
            "traded_family_excluded": False,
        },
        "scope": {
            "ramsey_43_coloring_constructed": False,
            "R_5_5_lower_bound_improved": False,
            "score_123_optimality_proved": False,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
