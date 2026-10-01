#!/usr/bin/env python3
"""Complete necessary regular r=9 domain; no signing or host search.

Actual author six-books-2, researcher. Whole remaining degree-star helper
adapted from own sourcec388377/eighteen_controls.py. Other imports are
standard library only. TWENTY.md supplies normalization and coverage.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys
import time

PAIRS = tuple(combinations(range(11), 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def neighbors(edges):
    return tuple(frozenset(j if i == v else i for i, j in edges if v in (i, j))
                 for v in range(11))


def pair_mask(edges):
    return sum(1 << i for i, e in enumerate(PAIRS) if e in edges)


def red_cores(k3):
    degrees = [3] * k3 + [2] * (7 - 2 * k3)
    m = len(degrees)
    for core in combinations(tuple(combinations(range(m), 2)), 5 - k3):
        current = [sum(i in e for e in core) for i in range(m)]
        if any(current[i] > degrees[i] for i in range(m)):
            continue
        red, leaf = set(core), m
        for i in range(m):
            for _ in range(degrees[i] - current[i]):
                red.add((i, leaf))
                leaf += 1
        require(leaf == 11 and len(red) == 9, "R core/leaf reconstruction")
        yield frozenset(red), m


def blue_completions(red, nr, inside):
    degree = [len(nr[i]) + ((inside >> i) & 1) for i in range(11)]
    leaf_allowed, forced = {}, set()
    for i in range(11):
        siblings = sorted(j for j in nr[i] if len(nr[j]) == 1)
        forced.update(combinations(siblings, 2))
        if len(nr[i]) == 1:
            parent = next(iter(nr[i]))
            leaf_allowed[i] = nr[parent] - {i}
    allowed = set()
    for i, j in PAIRS:
        if (i, j) in red:
            continue
        if i in leaf_allowed and j not in leaf_allowed[i]:
            continue
        if j in leaf_allowed and i not in leaf_allowed[j]:
            continue
        allowed.add((i, j))
    if not forced <= allowed:
        return
    residual = [degree[i] - sum(i in e for e in forced) for i in range(11)]
    if any(d < 0 for d in residual):
        return
    free = allowed - forced

    def visit(i, remaining, edges):
        while i < 11 and remaining[i] == 0:
            i += 1
        if i == 11:
            yield frozenset(forced | edges)
            return
        choices = [j for j in range(i + 1, 11)
                   if remaining[j] > 0 and (i, j) in free]
        for selected in combinations(choices, remaining[i]):
            after = remaining[:]
            after[i] = 0
            for j in selected:
                after[j] -= 1
            # All labels<=i are now saturated. For each remaining j,
            # count every active neighbor, including both sides of j.
            if all(after[j] <= sum(after[k] > 0 and
                   (min(j, k), max(j, k)) in free
                   for k in range(i + 1, 11) if k != j)
                   for j in range(i + 1, 11)):
                yield from visit(i + 1, after, edges | {(i, j) for j in selected})

    yield from visit(0, residual, set())


def obstruction(nr, nd, red, blue, inside):
    def square(i, j):
        return ((nr[i] & nr[j]).bit_count() + (nd[i] & nd[j]).bit_count()
                - (nr[i] & nd[j]).bit_count() - (nd[i] & nr[j]).bit_count())
    for i, j in sorted(red):
        pages = 7 + square(i, j) + ((inside >> i) & 1) + ((inside >> j) & 1)
        if pages > 6:
            return "red_uniform_upper", [i, j, pages]
    for i, j in PAIRS:
        if (i, j) in red or (i, j) in blue:
            continue
        pages = 9 + square(i, j)
        if pages > 9:
            return "matching_upper", [i, j, pages]
    return "survivor", None


def run(record_path=None, progress=False):
    started = time.monotonic()
    profiles, encoded_rows = [], {}
    handle = record_path.open("w") if record_path else None
    try:
        for k3 in range(4):
            core_count, inside_count, total, equal_total = 0, 0, 0, 0
            counts, equal_counts = Counter(), Counter()
            for red, m in red_cores(k3):
                core_count += 1
                nrs = neighbors(red)
                nr = [sum(1 << v for v in row) for row in nrs]
                permitted = [i for i in range(m, 11)
                             if len(nrs[next(iter(nrs[i]))]) == 3]
                records = []
                for flag_word in range(1 << len(permitted)):
                    if flag_word.bit_count() % 2:
                        continue
                    inside_count += 1
                    inside = sum(1 << v for k, v in enumerate(permitted) if (flag_word >> k) & 1)
                    for blue in blue_completions(red, nrs, inside):
                        nds = neighbors(blue)
                        require(not (red & blue), "R/D disjointness")
                        require(len(blue) == 9 + inside.bit_count() // 2, "D edge count")
                        require([len(nds[i]) for i in range(11)] ==
                                [len(nrs[i]) + ((inside >> i) & 1) for i in range(11)], "regular D degrees")
                        nd = [sum(1 << v for v in row) for row in nds]
                        kind, payload = obstruction(nr, nd, red, blue, inside)
                        require(kind != "survivor", "necessary quotient survived; theorem not established")
                        counts[kind] += 1
                        total += 1
                        if inside == 0:
                            equal_counts[kind] += 1
                            equal_total += 1
                        records.append([inside, pair_mask(blue), kind, payload])
                records.sort(key=lambda r: (r[0], r[1]))
                require(len({(r[0], r[1]) for r in records}) == len(records), "duplicate D/inside record")
                red_mask = pair_mask(red)
                require(red_mask not in encoded_rows, "duplicate normalized R graph")
                encoded = json.dumps([red_mask, records], separators=(",", ":")) + "\n"
                encoded_rows[red_mask] = encoded.encode()
                if handle:
                    handle.write(encoded)
            row = {"k3": k3, "nonleaf_vertices": 7 - k3, "nonleaf_R_edges": 5 - k3,
                   "R_core_words": core_count, "eligible_inside_words": inside_count,
                   "D_completions": total, "first_failure_counts": dict(counts),
                   "all_blue_inside_D_completions": equal_total,
                   "all_blue_inside_first_failure_counts": dict(equal_counts)}
            profiles.append(row)
            if progress:
                print(json.dumps({"finished_profile": row, "seconds": time.monotonic() - started}),
                      file=sys.stderr, flush=True)
    finally:
        if handle:
            handle.close()
    checksum = sha256()
    for red_mask in sorted(encoded_rows):
        checksum.update(encoded_rows[red_mask])
    return {"agent": "six-books-2", "role": "researcher", "complete": True,
            "scope": "r9/all admissible inside flags and every b, all R core words with canonical leaf attachments, all regular D degrees subject to proved transfer and sibling conditions",
            "profiles": profiles, "total_R_core_words": sum(r["R_core_words"] for r in profiles),
            "total_eligible_inside_words": sum(r["eligible_inside_words"] for r in profiles),
            "total_D_completions": sum(r["D_completions"] for r in profiles),
            "survivors": 0, "canonical_domain_obstruction_sha256": checksum.hexdigest(),
            "threads": 1, "local_jobs": 1, "signing_or_host_search": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, help="generated entry-level records in scratch, never publication input")
    parser.add_argument("--expected", type=Path, default=Path(__file__).with_name("twenty_expected.json"))
    parser.add_argument("--emit", action="store_true", help="print author output without fixture comparison")
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    result = run(args.records, args.progress)
    if not args.emit:
        require(result == json.loads(args.expected.read_text())["census"], "census differs from fixture")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
