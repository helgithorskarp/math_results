#!/usr/bin/env python3
"""Binary-core/leaf-choice audit, literal22-point pages, exact record comparison.

Actual author six-books-2, researcher; no imports from another generator.
The generated main records are untrusted comparison data, never a domain
input. Complete domain reconstruction precedes entry-level equality checks.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time

PAIRS = tuple(combinations(range(11), 2))
PAIR_INDEX = {e: i for i, e in enumerate(PAIRS)}
ALL_VERTICES = (1 << 22) - 1


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def core_inventory(m, caps):
    """Every binary word on the whole nonleaf core, grouped by degrees."""
    edges = tuple(combinations(range(m), 2))
    incident = [sum(1 << index for index, e in enumerate(edges) if i in e) for i in range(m)]
    groups = {}
    for word in range(1 << len(edges)):
        degrees = tuple((word & mask).bit_count() for mask in incident)
        if any(d > caps[i] for i, d in enumerate(degrees)):
            continue
        groups.setdefault(degrees, []).append(word)
    return edges, incident, groups


def red_graph(word, edges, target, incident):
    m = len(target)
    current = [(word & mask).bit_count() for mask in incident]
    if any(current[i] > target[i] for i in range(m)):
        return None
    red = {e for index, e in enumerate(edges) if (word >> index) & 1}
    leaf = m
    for i in range(m):
        for _ in range(target[i] - current[i]):
            red.add((i, leaf))
            leaf += 1
    require(leaf == 11 and len(red) == 9, "independent R reconstruction")
    nr = [set() for _ in range(11)]
    for i, j in red:
        nr[i].add(j)
        nr[j].add(i)
    red_mask = sum(1 << PAIR_INDEX[e] for e in red)
    return red, nr, red_mask


def leaf_and_core_blues(red, nr, inside, m, core_edges, rword, inventory):
    wanted = [len(nr[i]) + ((inside >> i) & 1) for i in range(11)]
    choices = []
    forced = set()
    for i in range(m):
        forced.update(combinations(sorted(nr[i] & set(range(m, 11))), 2))
    for leaf in range(m, 11):
        parent = next(iter(nr[leaf]))
        choices.append(tuple(combinations(sorted(nr[parent] - {leaf}), wanted[leaf])))
    for selected in product(*choices):
        blue = {tuple(sorted((leaf, v))) for leaf, row in zip(range(m, 11), selected) for v in row}
        if red & blue or not forced <= blue:
            continue
        if any(sum(leaf in e for e in blue) != wanted[leaf] for leaf in range(m, 11)):
            continue
        needed = tuple(wanted[i] - sum(i in e for e in blue) for i in range(m))
        if any(d < 0 for d in needed):
            continue
        for word in inventory.get(needed, []):
            if word & rword:
                continue
            whole = blue | {e for index, e in enumerate(core_edges) if (word >> index) & 1}
            require(len(whole) == 9 + inside.bit_count() // 2, "independent D edge count")
            require(all(sum(i in e for e in whole) == wanted[i] for i in range(11)), "independent D degrees")
            yield sum(1 << PAIR_INDEX[e] for e in whole)


def literal_obstruction(red_mask, blue_mask, inside):
    """Only bitset intersections of literal vertex neighborhoods; no W formulas."""
    rows = [0] * 22
    red_pairs, matching_pairs = [], []
    for index, (i, j) in enumerate(PAIRS):
        if (red_mask >> index) & 1:
            rows[2 * i] |= 3 << (2 * j)
            rows[2 * i + 1] |= 3 << (2 * j)
            rows[2 * j] |= 3 << (2 * i)
            rows[2 * j + 1] |= 3 << (2 * i)
            red_pairs.append((i, j))
        elif not (blue_mask >> index) & 1:
            rows[2 * i] |= 1 << (2 * j)
            rows[2 * i + 1] |= 1 << (2 * j + 1)
            rows[2 * j] |= 1 << (2 * i)
            rows[2 * j + 1] |= 1 << (2 * i + 1)
            matching_pairs.append((i, j))
    for i in range(11):
        if (inside >> i) & 1:
            rows[2 * i] |= 1 << (2 * i + 1)
            rows[2 * i + 1] |= 1 << (2 * i)
    require(all(row.bit_count() == 10 for row in rows), "decoded graph must be ten-regular")
    for i, j in red_pairs:
        pages = ((rows[2 * i] & rows[2 * j]).bit_count()
                 + (rows[2 * i] & rows[2 * j + 1]).bit_count())
        if pages > 6:
            return "red_uniform_upper", [i, j, pages]
    opposite = [ALL_VERTICES ^ (1 << v) ^ row for v, row in enumerate(rows)]
    for i, j in matching_pairs:
        pages = ((rows[2 * i] & rows[2 * j]).bit_count()
                 + (opposite[2 * i] & opposite[2 * j + 1]).bit_count())
        if pages > 9:
            return "matching_upper", [i, j, pages]
    return "survivor", None


def run(main_records, progress=False):
    # Type and duplicates are checked before any comparison. None of these
    # values drive domain generation or mathematical rejection.
    expected = {}
    for line in main_records.read_text().splitlines():
        row = json.loads(line)
        require(isinstance(row, list) and len(row) == 2 and type(row[0]) is int
                and isinstance(row[1], list), "malformed main record")
        require(0 <= row[0] < (1 << 55) and row[0] not in expected, "bad/duplicate R key")
        expected[row[0]] = row[1]
    started = time.monotonic()
    profiles, encoded_rows = [], {}
    literal_words = 0
    inventory_words = 0
    literal_lifts = 0
    for k3 in range(4):
        target = [3] * k3 + [2] * (7 - 2 * k3)
        m = len(target)
        edges, incident, inventory = core_inventory(m, target)
        inventory_words += 1 << len(edges)
        core_count, eligible, total, equal_total = 0, 0, 0, 0
        counts, equal_counts = Counter(), Counter()
        # All core words, including wrong edge count/degrees; no graph table.
        for rword in range(1 << len(edges)):
            if rword.bit_count() != 5 - k3:
                continue
            item = red_graph(rword, edges, target, incident)
            if item is None:
                continue
            red, nr, red_mask = item
            require(red_mask not in encoded_rows, "independent duplicate R graph")
            core_count += 1
            permitted = sum(1 << leaf for leaf in range(m, 11)
                            if len(nr[next(iter(nr[leaf]))]) == 3)
            records = []
            for inside in range(1 << 11):
                literal_words += 1
                if inside & ~permitted or inside.bit_count() % 2:
                    continue
                eligible += 1
                for blue_mask in leaf_and_core_blues(red, nr, inside, m, edges, rword, inventory):
                    kind, payload = literal_obstruction(red_mask, blue_mask, inside)
                    literal_lifts += 1
                    require(kind != "survivor", "independently generated necessary survivor")
                    records.append([inside, blue_mask, kind, payload])
                    counts[kind] += 1
                    total += 1
                    if inside == 0:
                        equal_counts[kind] += 1
                        equal_total += 1
            records.sort(key=lambda r: (r[0], r[1]))
            require(len({(r[0], r[1]) for r in records}) == len(records), "independent duplicate D/flag record")
            require(red_mask in expected, "main omitted an R graph")
            require(records == expected.pop(red_mask), "entry-level D/inside/literal obstruction mismatch")
            encoded_rows[red_mask] = (json.dumps([red_mask, records], separators=(",", ":")) + "\n").encode()
            if progress and core_count % 1000 == 0:
                print(json.dumps({"k3": k3, "R_words": core_count, "literal_lifts": literal_lifts,
                                  "seconds": time.monotonic() - started}), file=sys.stderr, flush=True)
        row = {"k3": k3, "nonleaf_vertices": 7 - k3, "nonleaf_R_edges": 5 - k3,
               "R_core_words": core_count, "eligible_inside_words": eligible,
               "D_completions": total, "first_failure_counts": dict(counts),
               "all_blue_inside_D_completions": equal_total,
               "all_blue_inside_first_failure_counts": dict(equal_counts)}
        profiles.append(row)
    require(not expected, "main included unmatched R graphs")
    checksum = sha256()
    for red_mask in sorted(encoded_rows):
        checksum.update(encoded_rows[red_mask])
    return {"agent": "six-books-2", "role": "researcher", "complete": True,
            "independent_domain": "all binary R/D nonleaf core words and every individual leaf-neighborhood choice",
            "independent_spines": "literal22-point bitset intersections, no signed matrix formula",
            "all_R_D_inside_obstruction_records_match_entrywise": True,
            "profiles": profiles, "binary_core_inventory_words": inventory_words,
            "literal_inside_words": literal_words, "literal_regular_lifts": literal_lifts,
            "canonical_domain_obstruction_sha256": checksum.hexdigest(),
            "threads": 1, "local_jobs": 1, "author_independence_not_peer_review": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--main-records", type=Path, required=True)
    parser.add_argument("--expected", type=Path, default=Path(__file__).with_name("twenty_expected.json"))
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    result = run(args.main_records, args.progress)
    if not args.emit:
        require(result == json.loads(args.expected.read_text())["independent"], "independent output differs from fixture")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
