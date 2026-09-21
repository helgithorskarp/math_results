#!/usr/bin/env python3
"""Exact, dependency-free verification. See PROOF.md for the universal proof."""

from collections import Counter
from fractions import Fraction as F
from functools import reduce
from hashlib import sha256
from itertools import combinations, product
from math import gcd
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(obj):
    return sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"))
                  .encode("utf-8")).hexdigest()


def validate_k(k):
    require(type(k) is int and k >= 2, "k must be an integer >= 2")


def halfspaces(k):
    """Return integer (normal, offset) rows a.p <= b, in a fixed order."""
    validate_k(k)
    d = k + 2
    rows = []
    for j in range(d):
        a = [0] * d
        a[j] = -1
        rows.append((tuple(a), 0))
    for i in range(k):
        a = [2*i+1, 1] + [0] * k
        a[i+2] = 1
        rows.append((tuple(a), k*k+i*(i+1)))
    return rows


def dot(a, p):
    require(len(a) == len(p), "dimension mismatch")
    return sum(x*y for x, y in zip(a, p))


def integer_rank(rows):
    """Exact fraction-free row elimination; no geometric special cases."""
    if not rows:
        return 0
    m = [list(r) for r in rows]
    width = len(m[0])
    require(all(len(r) == width and all(type(v) is int for v in r)
                for r in m), "integer matrix required")
    rank = 0
    for col in range(width):
        p = next((j for j in range(rank, len(m)) if m[j][col]), None)
        if p is None:
            continue
        m[rank], m[p] = m[p], m[rank]
        pivot = m[rank][col]
        for j in range(rank+1, len(m)):
            q = m[j][col]
            if q:
                row = [pivot*x-q*y for x, y in zip(m[j], m[rank])]
                g = reduce(gcd, (abs(x) for x in row), 0)
                m[j] = [x//g for x in row] if g else row
        rank += 1
        if rank == len(m):
            break
    return rank


def solve(rows, offsets):
    """Generic rational Gaussian elimination, separate from integer_rank."""
    n = len(rows)
    require(all(len(row) == n for row in rows), "square system required")
    m = [[F(x) for x in row] + [F(b)] for row, b in zip(rows, offsets)]
    for c in range(n):
        j = next((j for j in range(c, n) if m[j][c]), None)
        if j is None:
            return None
        m[c], m[j] = m[j], m[c]
        p = m[c][c]
        m[c] = [v/p for v in m[c]]
        for j in range(n):
            if j != c and m[j][c]:
                q = m[j][c]
                m[j] = [x-q*y for x, y in zip(m[j], m[c])]
    return tuple(m[i][-1] for i in range(n))


def candidates(k):
    """Construct endpoint witnesses; zero intervals create no duplicates."""
    validate_k(k)
    for y, z in [(0, 0)] + [(j, k*k-j*j) for j in range(k+1)]:
        options = []
        for i in range(k):
            c = k*k+i*(i+1)-(2*i+1)*y-z
            require(c >= 0, "negative interval")
            options.append((0,) if c == 0 else (0, c))
        for x in product(*options):
            yield (y, z) + x


def check_vertex(rows, p):
    slacks = [b-dot(a, p) for a, b in rows]
    require(all(s >= 0 for s in slacks), "infeasible vertex witness")
    active = [j for j, s in enumerate(slacks) if s == 0]
    require(integer_rank([rows[j][0] for j in active]) == len(p),
            "active normals do not certify a vertex")
    return active


def check_ray(rows, removed, direction):
    vals = [dot(a, direction) for a, b in rows]
    require(vals[removed] > 0, "ray does not exit removed facet")
    require(all(v <= 0 for j, v in enumerate(vals) if j != removed),
            "ray violates a retained halfspace")


def geometric_certificates(k):
    rows = halfspaces(k)
    d = k+2
    interior = [F(1, 4)] * d
    require(all(dot(a, interior) < b for a, b in rows),
            "strict interior certificate failed")
    facet_points = []
    rays = []
    for r in range(len(rows)):
        p = interior[:]
        direction = [0] * d
        if r < d:
            p[r] = 0
            direction[r] = -1
        else:
            i = r-d
            p[i+2] = F(k*k+i*(i+1))-F(i+1, 2)
            direction[i+2] = 1
        slacks = [b-dot(a, p) for a, b in rows]
        require(slacks[r] == 0 and
                all(s > 0 for j, s in enumerate(slacks) if j != r),
                "facet does not have a relative interior witness")
        check_ray(rows, r, direction)
        facet_points.append([str(x) for x in p])
        rays.append(direction)
    # Nonnegative combinations of the supplied rows certify a finite
    # upper bound for each coordinate. No optimization software is used.
    upper_certificates = []
    for c in range(d):
        i = k-1 if c == 0 else (0 if c == 1 else c-2)
        a, b = rows[d+i]
        combined = list(a)
        for j in range(d):
            if j != c:
                require(a[j] >= 0, "negative combination multiplier")
                combined = [u+a[j]*v for u, v in zip(combined, rows[j][0])]
        require(combined[c] > 0 and
                all(v == 0 for j, v in enumerate(combined) if j != c),
                "coordinate boundedness certificate failed")
        upper_certificates.append(str(F(b, combined[c])))
    return {
        "facets": len(rows),
        "deletion_rays": len(rays),
        "coordinate_upper_bounds": upper_certificates,
        "facet_and_ray_sha256": digest([facet_points, rays]),
    }


def enumerate_all_bases(rows, d):
    """Independent finite completeness check from the H-representation."""
    vertices = set()
    tested = 0
    nonsingular = 0
    for ids in combinations(range(len(rows)), d):
        tested += 1
        p = solve([rows[i][0] for i in ids], [rows[i][1] for i in ids])
        if p is None:
            continue
        nonsingular += 1
        if all(dot(a, p) <= b for a, b in rows):
            vertices.add(p)
    return vertices, tested, nonsingular


def rejected(action):
    try:
        action()
    except ValueError:
        return True
    return False


def audit():
    evidence = []
    total_vertices = total_inequalities = total_bases = 0
    # Small cases are correctness controls; 9 and 10 are the two
    # conjecture-refuting witnesses, not a parameter census.
    for k in (2, 3, 4, 5, 9, 10):
        rows = halfspaces(k)
        points = list(candidates(k))
        require(len(points) == len(set(points)), "duplicate witnesses")
        active_records = []
        histogram = Counter()
        for p in points:
            active = check_vertex(rows, p)
            require(len(active) == k+2, "non-simple candidate")
            active_records.append([p, active])
            histogram[len(active)] += 1
        # The number here is a checked assertion after every distinct
        # witness has already passed direct halfspace/rank verification.
        require(len(points) == 2**(k-2)*(k+7), "count mismatch")
        record = {"k": k, "dimension": k+2, "vertices": len(points),
                  "cube_vertices": 2**(k+2),
                  "active_count_histogram": dict(sorted(histogram.items())),
                  "witness_sha256": digest(active_records),
                  **geometric_certificates(k)}
        if k <= 5:
            all_vertices, tested, nonsingular = enumerate_all_bases(rows, k+2)
            require(all_vertices == set(points),
                    "complete basis enumeration disagrees entry by entry")
            record["all_bases"] = tested
            record["nonsingular_bases"] = nonsingular
            total_bases += tested
        evidence.append(record)
        total_vertices += len(points)
        total_inequalities += len(points)*len(rows)
    require(evidence[-1]["vertices"] > evidence[-1]["cube_vertices"],
            "strict counterexample not established")
    require(evidence[-2]["vertices"] == evidence[-2]["cube_vertices"]
            and evidence[-2]["facets"] != 2*evidence[-2]["dimension"],
            "equality-clause counterexample not established")

    negative = 0
    for bad in (0, 1, -2, True, F(2), "10"):
        require(rejected(lambda bad=bad: halfspaces(bad)), "bad input accepted")
        negative += 1
    rows = halfspaces(2)
    # Feasible midpoint of an edge is not a vertex.
    midpoint = (0, 0, 2, 0)
    require(all(dot(a, midpoint) <= b for a, b in rows), "bad test fixture")
    require(rejected(lambda: check_vertex(rows, midpoint)),
            "non-vertex was accepted")
    negative += 1
    require(rejected(lambda: check_vertex(rows, (0, 0, 5, 0))),
            "infeasible point was accepted")
    negative += 1
    require(rejected(lambda: check_ray(rows, 0, (1, 0, 0, 0))),
            "wrong-sign deletion ray was accepted")
    negative += 1
    require(rejected(lambda: check_ray(rows, 4, (0, 0, 0, 1))),
            "wrong-private-coordinate deletion ray was accepted")
    negative += 1
    payload = {
        "instances": evidence,
        "totals": {"vertices": total_vertices,
                   "vertex_inequality_tests": total_inequalities,
                   "complete_small_bases": total_bases,
                   "facets_and_deletion_rays": sum(r["facets"] for r in evidence),
                   "negative_controls": negative},
    }
    return {"status": "VERIFIED", "evidence_sha256": digest(payload), **payload}


if __name__ == "__main__":
    result = audit()
    expected = json.loads(Path(__file__).with_name("expected.json").read_text())
    # JSON object keys are strings, so compare the canonical serialization.
    require(json.dumps(result, sort_keys=True) == json.dumps(expected, sort_keys=True),
            "results differ from expected.json")
    print(json.dumps(result, indent=2, sort_keys=True))
