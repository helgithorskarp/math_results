#!/usr/bin/env python3
"""Independent checks for the dense-tail transversal census.

The optimized scanner uses recursive hitting-set branching.  This verifier
uses a separate graph6 decoder, checks every emitted positive witness entry by
entry, and establishes four representative minima by direct enumeration of
all candidate hitting subsets.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path


N = 24


def decode_g6(raw: bytes) -> list[int]:
    vals = [c - 63 for c in raw.strip()]
    if not vals or vals[0] != N or len(vals) != 47:
        raise ValueError("malformed order-24 graph6 record")
    adj = [0] * N
    pos = 0
    for j in range(1, N):
        for i in range(j):
            word, shift = divmod(pos, 6)
            if vals[1 + word] >> (5 - shift) & 1:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            pos += 1
    return adj


def edge_count(adj: list[int]) -> int:
    return sum(a.bit_count() for a in adj) // 2


def independent_fours(adj: list[int]) -> list[int]:
    out = []
    full = (1 << N) - 1
    non = [full & ~adj[v] & ~(1 << v) for v in range(N)]
    for a in range(N):
        after_a = non[a] & ~((1 << (a + 1)) - 1)
        while after_a:
            bbit = after_a & -after_a
            b = bbit.bit_length() - 1
            after_a ^= bbit
            after_b = non[a] & non[b] & ~((1 << (b + 1)) - 1)
            while after_b:
                cbit = after_b & -after_b
                c = cbit.bit_length() - 1
                after_b ^= cbit
                after_c = non[a] & non[b] & non[c] & ~((1 << (c + 1)) - 1)
                while after_c:
                    dbit = after_c & -after_c
                    after_c ^= dbit
                    out.append((1 << a) | bbit | cbit | dbit)
    return out


def verify_no_smaller_hitting_set(edges: list[int], claimed: int) -> None:
    """Meet-in-the-middle enumeration, deliberately unlike the C++ recursion."""
    incidence = [0] * N
    for q, edge in enumerate(edges):
        for v in range(N):
            if edge >> v & 1:
                incidence[v] |= 1 << q
    target = (1 << len(edges)) - 1
    halves = []
    for offset in (0, 12):
        covers = [0] * (1 << 12)
        by_weight = [[] for _ in range(13)]
        by_weight[0].append(0)
        for mask in range(1, 1 << 12):
            bit = mask & -mask
            v = offset + bit.bit_length() - 1
            covers[mask] = covers[mask ^ bit] | incidence[v]
            by_weight[mask.bit_count()].append(covers[mask])
        halves.append(by_weight)
    for total in range(claimed):
        for left_weight in range(max(0, total - 12), min(12, total) + 1):
            right_weight = total - left_weight
            for left in halves[0][left_weight]:
                for right in halves[1][right_weight]:
                    if left | right == target:
                        raise SystemExit(f"found hitting set smaller than claimed {claimed}")


def load_rows(path: Path) -> tuple[list[tuple[int, int, int, int, int]], str]:
    raw = path.read_bytes()
    rows = []
    for line_number, line in enumerate(raw.decode("ascii").splitlines(), 1):
        fields = line.split()
        if len(fields) != 5:
            raise ValueError(f"row {line_number}: expected five fields")
        i, e, q, tau = map(int, fields[:4])
        witness = int(fields[4], 16)
        rows.append((i, e, q, tau, witness))
    return rows, sha256(raw).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("catalogue", type=Path)
    ap.add_argument("rows", type=Path)
    ap.add_argument(
        "--expected",
        type=Path,
        default=Path(__file__).with_name("EXPECTED_RESULT.json"),
    )
    ns = ap.parse_args()
    expected = json.loads(ns.expected.read_text())
    catalogue_raw = ns.catalogue.read_bytes()
    if sha256(catalogue_raw).hexdigest() != expected["catalogue_sha256"]:
        raise SystemExit("catalogue SHA-256 mismatch")
    rows, rows_hash = load_rows(ns.rows)
    if rows_hash != expected["rows_sha256"]:
        raise SystemExit("result-row SHA-256 mismatch")
    if len(rows) != expected["dense_records"]:
        raise SystemExit("wrong dense-row count")

    edge_counts = Counter()
    tau_counts = Counter()
    edge_tau = defaultdict(Counter)
    i4_range: dict[int, list[int]] = {}
    fixtures = {int(k): v for k, v in expected["brute_force_fixture_tau"].items()}
    fixture_edges: dict[int, list[int]] = {}
    row_pos = 0
    catalogue_records = 0
    for raw in catalogue_raw.splitlines():
        if not raw:
            continue
        catalogue_records += 1
        adj = decode_g6(raw)
        e = edge_count(adj)
        if e < 126:
            continue
        if row_pos >= len(rows):
            raise SystemExit("catalogue has more dense records than rows")
        i, row_e, row_q, tau, witness = rows[row_pos]
        if i != row_pos or row_e != e:
            raise SystemExit(f"row {row_pos}: index/edge mismatch")
        fours = independent_fours(adj)
        if len(fours) != row_q:
            raise SystemExit(f"row {row_pos}: independent-four count mismatch")
        if witness.bit_count() != tau or any((witness & q) == 0 for q in fours):
            raise SystemExit(f"row {row_pos}: invalid minimum-size witness")
        if i in fixtures:
            fixture_edges[i] = fours
        edge_counts[e] += 1
        tau_counts[tau] += 1
        edge_tau[e][tau] += 1
        i4_range.setdefault(e, [row_q, row_q])
        i4_range[e][0] = min(i4_range[e][0], row_q)
        i4_range[e][1] = max(i4_range[e][1], row_q)
        row_pos += 1
    if catalogue_records != expected["catalogue_records"] or row_pos != len(rows):
        raise SystemExit("catalogue coverage mismatch")

    for i, want in sorted(fixtures.items()):
        verify_no_smaller_hitting_set(fixture_edges[i], want)

    got = {
        "catalogue_records": catalogue_records,
        "dense_records": len(rows),
        "catalogue_sha256": expected["catalogue_sha256"],
        "rows_sha256": rows_hash,
        "edge_counts": {str(k): edge_counts[k] for k in sorted(edge_counts)},
        "tau_counts": {str(k): tau_counts[k] for k in sorted(tau_counts)},
        "edge_tau_counts": {
            str(e): {str(t): edge_tau[e][t] for t in sorted(edge_tau[e])}
            for e in sorted(edge_tau)
        },
        "independent_four_ranges": {str(e): i4_range[e] for e in sorted(i4_range)},
        "brute_force_fixture_tau": {str(i): fixtures[i] for i in sorted(fixtures)},
    }
    if got != expected:
        print(json.dumps(got, indent=2, sort_keys=True))
        raise SystemExit("summary mismatch")
    print("VERIFIED_COMPLETE_DENSE24_TRANSVERSAL_CENSUS")
    print(json.dumps(got, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
