#!/usr/bin/env python3
"""Independent orbit and formula audit for the full-support exclusion."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from math import comb
from pathlib import Path
import sys


def dot(x, y):
    return (x & y).bit_count() & 1


def rank(values):
    basis = {}
    for value in values:
        x = value
        while x:
            p = x.bit_length() - 1
            if p in basis:
                x ^= basis[p]
            else:
                basis[p] = x
                break
    return len(basis)


def map_value(images, x):
    result = 0
    for i, image in enumerate(images):
        if (x >> i) & 1:
            result ^= image
    return result


def maps():
    result = []
    for images in permutations(range(1, 16), 4):
        if rank(images) != 4:
            continue
        row = tuple(map_value(images, x) for x in range(16))
        column = [None] * 16
        for z in range(16):
            y = sum(dot(images[i], z) << i for i in range(4))
            column[y] = z
        if any(dot(row[x], column[y]) != dot(x, y)
               for x in range(16) for y in range(16)):
            raise RuntimeError("dual action failure")
        result.append((row, tuple(column)))
    return result


def mask(values):
    return sum(1 << (x - 1) for x in values)


def act(value, permutation):
    return mask(permutation[x] for x in range(1, 16)
                if (value >> (x - 1)) & 1)


def affine(value):
    return any(value == mask(y for y in range(1, 16) if dot(w, y))
               for w in range(1, 16))


def clause_count(row_doubles, column_doubles):
    rows = list(range(1, 16)) + list(row_doubles)
    columns = list(range(1, 16)) + list(column_doubles)
    total = 2 * (comb(20, 5) + comb(23, 5))
    for x in rows:
        red = sum(dot(x, y) for y in columns)
        total += comb(red, 4) + comb(23 - red, 4)
    for left in combinations(rows, 2):
        red = sum(all(dot(x, y) for x in left) for y in columns)
        blue = sum(all(not dot(x, y) for x in left) for y in columns)
        total += comb(red, 3) + comb(blue, 3)
    for left in combinations(rows, 3):
        red = sum(all(dot(x, y) for x in left) for y in columns)
        blue = sum(all(not dot(x, y) for x in left) for y in columns)
        total += comb(red, 2) + comb(blue, 2)
    for y in columns:
        red = sum(dot(x, y) for x in rows)
        total += comb(red, 4) + comb(20 - red, 4)
    return total


def load_rows(directory):
    rows = []
    for shard in range(4):
        raw = (directory / f"proof_manifest_shard{shard}.jsonl").read_bytes()
        rows.extend(json.loads(line) for line in raw.splitlines())
    rows.sort(key=lambda row: row["orbit_index"])
    return rows


def main():
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    proof_rows = load_rows(directory)
    if [row["orbit_index"] for row in proof_rows] != list(range(1348)):
        raise RuntimeError("incomplete proof index partition")
    if any(row["status"] != "UNSAT_PROOF_VERIFIED" for row in proof_rows):
        raise RuntimeError("unverified proof status")
    if len({row["cnf_sha256"] for row in proof_rows}) != 1348:
        raise RuntimeError("CNF identity collision")
    if any(clause_count(tuple(row["row_doubles"]), tuple(row["column_doubles"])) !=
           row["clauses"] for row in proof_rows):
        raise RuntimeError("independent clause-count mismatch")

    group = maps()
    if len(group) != 20160:
        raise RuntimeError("incorrect GL(4,2) order")
    row_reps = sorted({mask(row["row_doubles"]) for row in proof_rows})
    if len(row_reps) != 4:
        raise RuntimeError("unexpected row-orbit representative count")
    row_orbits = []
    stabilizers = {}
    for representative in row_reps:
        orbit = {act(representative, row) for row, _ in group}
        row_orbits.append(orbit)
        stabilizers[representative] = [(row, column) for row, column in group
                                        if act(representative, row) == representative]
    if len(set().union(*row_orbits)) != 3003 or any(row_orbits[i] & row_orbits[j]
            for i in range(4) for j in range(i)):
        raise RuntimeError("row orbits do not partition all five-subsets")

    columns = [mask(values) for values in combinations(range(1, 16), 8)
               if not affine(mask(values))]
    column_orbit_counts = {}
    observed_counts = Counter(mask(row["row_doubles"]) for row in proof_rows)
    for representative in row_reps:
        stabilizer = stabilizers[representative]
        canonical = {min(act(value, column) for _, column in stabilizer)
                     for value in columns}
        observed = {min(act(mask(row["column_doubles"]), column)
                        for _, column in stabilizer)
                    for row in proof_rows
                    if mask(row["row_doubles"]) == representative}
        if observed != canonical:
            raise RuntimeError("pair-orbit representatives are incomplete")
        column_orbit_counts[str(tuple(x for x in range(1, 16)
                                      if (representative >> (x - 1)) & 1))] = len(canonical)
        if observed_counts[representative] != len(canonical):
            raise RuntimeError("row-block orbit count mismatch")

    result = json.loads((directory / "RESULT.json").read_text())
    proof = result["proofs"]
    if proof["verified_cases"] != 1348 or proof["clauses_total"] != sum(
            row["clauses"] for row in proof_rows):
        raise RuntimeError("result aggregate mismatch")
    evidence = {
        "status": "INDEPENDENT_AUDIT_FULL_SUPPORT_RANK4_EXCLUSION",
        "gl4_size": len(group),
        "row_orbit_sizes": sorted(map(len, row_orbits)),
        "row_orbits": len(row_reps),
        "column_orbits_by_row_representative": column_orbit_counts,
        "pair_orbits": sum(column_orbit_counts.values()),
        "pair_sets": 3003 * 6420,
        "proof_cases": len(proof_rows),
        "independent_clause_counts": len(proof_rows),
        "clauses_total": sum(row["clauses"] for row in proof_rows),
        "proof_bytes_total": sum(row["proof_bytes"] for row in proof_rows),
        "cnf_hashes_distinct": len({row["cnf_sha256"] for row in proof_rows}),
        "proof_hashes_distinct": len({row["proof_sha256"] for row in proof_rows}),
    }
    print(json.dumps(evidence, sort_keys=True))


if __name__ == "__main__":
    main()
