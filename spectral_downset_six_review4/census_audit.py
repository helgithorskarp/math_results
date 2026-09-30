#!/usr/bin/env python3
"""Complete independent cardinality-growth and full-permutation downset audit.

The candidate JSONL is untrusted. No target program is imported here.
At each size, only that size's labeled permutation orbits are stored.
"""
import argparse
from array import array
from collections import Counter
import hashlib
from itertools import permutations
import json
from pathlib import Path
import sys
import time

from exception_audit import family as exception_family, run as exceptional_audit


def need(condition, message):
    if not condition:
        raise ValueError(message)


class PermutationImages:
    def __init__(self, n):
        self.n = n
        self.width = 1 << n
        self.tables = []
        self.permutations = list(permutations(range(n)))
        need(array("Q").itemsize == 8 and n <= 6, "unsigned64 storage bound")
        for p in self.permutations:
            positions = [0] * self.width
            for a in range(1, self.width):
                low = a & -a
                positions[a] = positions[a ^ low] | (1 << p[low.bit_length() - 1])
            tables = []
            for first in range(0, self.width, 8):
                count = min(8, self.width - first)
                entries = array("Q", [0]) * (1 << count)
                for b in range(1, 1 << count):
                    low = b & -b
                    entries[b] = entries[b ^ low] | (1 << positions[first + low.bit_length() - 1])
                tables.append(entries)
            self.tables.append(tables)

    def orbit(self, f):
        chunks = [(f >> k) & 255 for k in range(0, self.width, 8)]
        if self.n == 6:
            b0, b1, b2, b3, b4, b5, b6, b7 = chunks
            return {t[0][b0] | t[1][b1] | t[2][b2] | t[3][b3]
                    | t[4][b4] | t[5][b5] | t[6][b6] | t[7][b7]
                    for t in self.tables}
        result = set()
        for t in self.tables:
            value = 0
            for table, b in zip(t, chunks):
                value |= table[b]
            result.add(value)
        return result

    def basis_controls(self):
        checks = 0
        for p, tables in zip(self.permutations, self.tables):
            for a in range(self.width):
                image = 0
                for i in range(self.n):
                    if a & (1 << i):
                        image |= 1 << p[i]
                got = tables[a // 8][1 << (a % 8)]
                need(got == 1 << image, "optimized permutation basis differs")
                checks += 1
        return checks


def members(f, n):
    return [a for a in range(1 << n) if f & (1 << a)]


def positive_certificate(f, bins, n):
    sets = members(f, n)
    for a in sets:
        for i in range(n):
            if a & (1 << i):
                need(f & (1 << (a ^ (1 << i))), "candidate not a downset")
    nonempty = set(sets) - {0}
    if not nonempty:
        need(bins == [], "trivial certificate")
        return False
    need(isinstance(bins, list) and all(isinstance(b, list) for b in bins), "partition type")
    s = max(sum(a & (1 << i) != 0 for a in sets) for i in range(n))
    need(len(bins) == s, "largest-star partition size")
    flattened = [a for block in bins for a in block]
    need(all(type(a) is int for a in flattened), "partition integer labels")
    need(len(flattened) == len(nonempty) and set(flattened) == nonempty,
         "exact positive partition coverage")
    for block in bins:
        occupied = 0
        need(bool(block), "empty bin in a largest-star certificate")
        for a in block:
            need(not occupied & a, "intersecting words share a bin")
            occupied |= a
    # Exact integer formulas for the proposed Gram matrix's row sums.
    N = len(sets)
    sizes = [len(block) for block in bins]
    cross = [N - s * m for m in sizes]
    diagonal = s * sum(m * m for m in sizes) - N * (N - 2)
    need(N - s > 0, "Hoffman denominator")
    need(all(s * m + c == N for m, c in zip(sizes, cross)), "nonempty Gram row")
    need(diagonal + sum(m * c for m, c in zip(sizes, cross)) == N, "empty Gram row")
    return True


def read_candidates(path):
    records = [dict() for _ in range(65)]
    for line in path.read_text().splitlines():
        r = json.loads(line)
        f, o = r["family"], r["orbit"]
        need(type(f) is int and 0 <= f < (1 << 64), "candidate family range")
        need(type(o) is int and 1 <= o <= 720 and 720 % o == 0, "candidate orbit type")
        size = f.bit_count()
        need(f not in records[size], "duplicate candidate representative")
        records[size][f] = r
    return records


def run(n, records=None, progress=False):
    start = time.monotonic()
    action = PermutationImages(n)
    basis = action.basis_controls()
    width = 1 << n
    predecessors = []
    for a in range(width):
        predecessors.append(sum(1 << (a ^ (1 << i))
                                for i in range(n) if a & (1 << i)))
    exceptional_orbit = set()
    if n == 6:
        exceptional_orbit = action.orbit(sum(1 << a for a in exception_family()[0]))
    partition_count = trivial_count = exception_count = candidate_count = 0
    labeled_sum = 0
    all_classes = []
    orbit_histogram = Counter()
    size_histogram = {}

    def consume(orbit):
        nonlocal partition_count, trivial_count, exception_count, candidate_count, labeled_sum
        canonical = min(orbit)
        size = canonical.bit_count()
        all_classes.append((canonical, len(orbit)))
        orbit_histogram[len(orbit)] += 1
        labeled_sum += sum(orbit)
        if records is not None:
            matched = [(f, records[size][f]) for f in orbit if f in records[size]]
            need(len(matched) == 1, "exactly one candidate for each independent orbit")
            f, r = matched[0]
            del records[size][f]
            need(r["orbit"] == len(orbit), "direct orbit multiplicity")
            candidate_count += 1
            if r["bins"] is None:
                need(f in exceptional_orbit, "unsupported missing partition")
                exception_count += 1
            elif positive_certificate(f, r["bins"], n):
                partition_count += 1
            else:
                trivial_count += 1
        return canonical, len(orbit)

    current = [consume({0})]
    labeled_count = 0
    for size in range(width + 1):
        need(bool(current), "cardinality growth terminated early")
        level_labels = sum(o for _, o in current)
        size_histogram[str(size)] = level_labels
        labeled_count += level_labels
        if records is not None:
            need(not records[size], "unmatched candidate orbit")
        if progress and (size % 8 == 0 or size == width):
            print(f"cardinality={size} classes_checked={len(all_classes)} elapsed={time.monotonic()-start:.2f}s",
                  file=sys.stderr, flush=True)
        if size == width:
            need(current == [((1 << width) - 1, 1)], "full-family endpoint")
            break
        next_seen = set()
        following = []
        for f, _ in current:
            for a, required in enumerate(predecessors):
                if f & (1 << a) or required & ~f:
                    continue
                child = f | (1 << a)
                if child in next_seen:
                    continue
                orbit = action.orbit(child)
                need(not orbit & next_seen, "overlapping full permutation orbits")
                next_seen.update(orbit)
                following.append(consume(orbit))
        current = following
    if records is not None:
        need(all(not d for d in records), "unconsumed candidate records")
        need((candidate_count, partition_count, exception_count, trivial_count)
             == (16353, 16350, 1, 2), "certificate cohort totals")
    digest = hashlib.sha256()
    for f, o in sorted(all_classes):
        digest.update(f"{f}:{o}\n".encode())
    return {"ground_set_size": n, "classes": len(all_classes),
            "labeled_downsets": labeled_count, "labeled_family_mask_sum": labeled_sum,
            "labeled_size_histogram": size_histogram,
            "orbit_size_histogram": {str(k): v for k, v in sorted(orbit_histogram.items())},
            "full_group_minimum_census_sha256": digest.hexdigest(),
            "permutation_basis_controls": basis,
            "candidate_orbits_checked": candidate_count,
            "partition_certificates_checked": partition_count,
            "exceptional_orbits_checked": exception_count,
            "trivial_orbits_checked": trivial_count}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path)
    parser.add_argument("--n", type=int, default=6, choices=range(7))
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    need(args.candidates is None or args.n == 6, "six-element candidate format")
    records = read_candidates(args.candidates) if args.candidates else None
    result = run(args.n, records, progress=True)
    if args.n == 6 and args.candidates:
        result["exception"] = exceptional_audit()
    if args.expect:
        need(result == json.loads(args.expect.read_text()), "expected result differs")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
