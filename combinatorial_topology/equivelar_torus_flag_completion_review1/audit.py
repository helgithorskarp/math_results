#!/usr/bin/env python3
"""Independent finite audit of the equivelar-torus flag-completion trichotomy.

This implementation intentionally does not import the submitted verifier.  It
represents lattice cosets by a breadth-first transversal and tests equality via
literal subgroup membership, rather than using the submitter's reduction map.
Only Python's standard library is required.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, deque


STEPS = ((1, 0), (0, 1), (1, -1), (-1, 0), (0, -1), (-1, 1))
AXES = STEPS[:3]


def add(p: tuple[int, int], q: tuple[int, int], k: int = 1) -> tuple[int, int]:
    return p[0] + k * q[0], p[1] + k * q[1]


def in_lattice(p: tuple[int, int], a: int, b: int, c: int) -> bool:
    """Test p in <(a,0),(b,c)> without choosing a quotient normal form."""
    x, y = p
    if y % c:
        return False
    return (x - b * (y // c)) % a == 0


def same_coset(
    p: tuple[int, int], q: tuple[int, int], a: int, b: int, c: int
) -> bool:
    return in_lattice((p[0] - q[0], p[1] - q[1]), a, b, c)


def quotient_transversal(a: int, b: int, c: int) -> list[tuple[int, int]]:
    """Find all cosets by Cayley-graph BFS, using subgroup tests for equality."""
    reps = [(0, 0)]
    todo = deque([(0, 0)])
    while todo:
        p = todo.popleft()
        for s in STEPS:
            q = add(p, s)
            if not any(same_coset(q, r, a, b, c) for r in reps):
                reps.append(q)
                todo.append(q)
    assert len(reps) == a * c
    return reps


def class_of(
    p: tuple[int, int], reps: list[tuple[int, int]], a: int, b: int, c: int
) -> int:
    hits = [i for i, q in enumerate(reps) if same_coset(p, q, a, b, c)]
    assert len(hits) == 1
    return hits[0]


def is_connected(vertices: set[int], edges: set[tuple[int, int]]) -> bool:
    if not vertices:
        return True
    adj = {v: set() for v in vertices}
    for x, y in edges:
        adj[x].add(y)
        adj[y].add(x)
    root = next(iter(vertices))
    seen = {root}
    todo = [root]
    while todo:
        v = todo.pop()
        for w in adj[v] - seen:
            seen.add(w)
            todo.append(w)
    return seen == vertices


def rank_mod(columns: list[dict[int, int]], prime: int) -> int:
    """Sparse column rank over F_prime."""
    pivots: dict[int, dict[int, int]] = {}
    for original in columns:
        v = {i: x % prime for i, x in original.items() if x % prime}
        while v:
            pivot = min(v)
            if pivot not in pivots:
                inv = pow(v[pivot], -1, prime)
                pivots[pivot] = {
                    i: (x * inv) % prime for i, x in v.items() if (x * inv) % prime
                }
                break
            factor = v[pivot]
            base = pivots[pivot]
            for i, x in base.items():
                value = (v.get(i, 0) - factor * x) % prime
                if value:
                    v[i] = value
                else:
                    v.pop(i, None)
    return len(pivots)


def betti_numbers(
    n: int, edges: set[tuple[int, int]], triangles: set[tuple[int, int, int]], prime: int
) -> tuple[int, int, int]:
    edge_list = sorted(edges)
    edge_id = {e: i for i, e in enumerate(edge_list)}
    d1 = [{x: -1, y: 1} for x, y in edge_list]
    d2 = []
    for x, y, z in sorted(triangles):
        d2.append(
            {
                edge_id[(y, z)]: 1,
                edge_id[(x, z)]: -1,
                edge_id[(x, y)]: 1,
            }
        )
    r1 = rank_mod(d1, prime)
    r2 = rank_mod(d2, prime)
    return n - r1, len(edge_list) - r1 - r2, len(triangles) - r2


def abelian_h1_two_generators(relations: list[tuple[int, int]]) -> str:
    """Smith invariants of Z^2 modulo the supplied abelianized relators."""
    entries = [abs(x) for row in relations for x in row if x]
    d1 = math.gcd(*entries) if entries else 0
    minors = [
        abs(x1 * y2 - y1 * x2)
        for (x1, y1), (x2, y2) in itertools.combinations(relations, 2)
        if x1 * y2 - y1 * x2
    ]
    if minors:
        determinant_gcd = math.gcd(*minors)
        d2 = determinant_gcd // d1
        torsion = [d for d in (d1, d2) if d > 1]
        return "0" if not torsion else " + ".join(f"Z/{d}" for d in torsion)
    if d1:
        return "Z" if d1 == 1 else f"Z + Z/{d1}"
    return "Z^2"


def graph_triangles(adj: list[set[int]]) -> set[tuple[int, int, int]]:
    out = set()
    for x in range(len(adj)):
        for y in (v for v in adj[x] if v > x):
            for z in (adj[x] & adj[y]):
                if z > y:
                    out.add((x, y, z))
    return out


def has_k4(adj: list[set[int]], triangles: set[tuple[int, int, int]]) -> bool:
    return any(adj[x] & adj[y] & adj[z] for x, y, z in triangles)


def link_distance(
    v: int, x: int, y: int, faces: set[tuple[int, int, int]]
) -> int | None:
    link_edges = set()
    for f in faces:
        if v in f:
            q = sorted(set(f) - {v})
            link_edges.add((q[0], q[1]))
    link_adj: dict[int, set[int]] = {}
    for p, q in link_edges:
        link_adj.setdefault(p, set()).add(q)
        link_adj.setdefault(q, set()).add(p)
    seen = {x}
    todo = deque([(x, 0)])
    while todo:
        p, d = todo.popleft()
        if p == y:
            return d
        for q in link_adj.get(p, ()) - seen:
            seen.add(q)
            todo.append((q, d + 1))
    return None


def analyze(a: int, b: int, c: int) -> dict[str, object]:
    n = a * c
    reps = quotient_transversal(a, b, c)
    neighbors = [
        [class_of(add(p, s), reps, a, b, c) for s in STEPS] for p in reps
    ]
    adj = [set(row) - {i} for i, row in enumerate(neighbors)]

    faces: set[tuple[int, int, int]] = set()
    face_degenerate = False
    for p in reps:
        x = class_of(p, reps, a, b, c)
        u = class_of(add(p, (1, 0)), reps, a, b, c)
        v = class_of(add(p, (0, 1)), reps, a, b, c)
        uv = class_of(add(p, (1, 1)), reps, a, b, c)
        for f in ((x, u, v), (uv, u, v)):
            if len(set(f)) != 3:
                face_degenerate = True
            faces.add(tuple(sorted(f)))

    edges = {
        tuple(sorted((x, y)))
        for x in range(n)
        for y in adj[x]
        if x != y
    }
    incidence = Counter()
    for f in faces:
        for e in itertools.combinations(f, 2):
            incidence[tuple(sorted(e))] += 1

    links_ok = True
    for x in range(n):
        link_edges = set()
        for f in faces:
            if x in f:
                remainder = sorted(set(f) - {x})
                if len(remainder) != 2:
                    links_ok = False
                    break
                p, q = remainder
                link_edges.add((p, q))
        if not links_ok:
            break
        link_vertices = set(itertools.chain.from_iterable(link_edges))
        degree = Counter(itertools.chain.from_iterable(link_edges))
        if not (
            len(link_vertices) == 6
            and len(link_edges) == 6
            and set(degree.values()) == {2}
            and is_connected(link_vertices, link_edges)
        ):
            links_ok = False
            break

    valid = (
        not face_degenerate
        and all(len(row) == 6 for row in adj)
        and all(i not in row for i, row in enumerate(adj))
        and all(i in adj[j] for i, row in enumerate(adj) for j in row)
        and len(edges) == 3 * n
        and len(faces) == 2 * n
        and set(incidence) == edges
        and set(incidence.values()) == {2}
        and links_ok
        and is_connected(set(range(n)), edges)
    )
    if not valid:
        return {"hnf": [a, b, c], "n": n, "status": "invalid"}

    triangles = graph_triangles(adj)
    if has_k4(adj, triangles):
        return {
            "hnf": [a, b, c],
            "n": n,
            "status": "K4_excluded",
            "graph_triangles": len(triangles),
        }

    missing = triangles - faces
    assert faces <= triangles
    short_axes = [s for s in AXES if in_lattice(add((0, 0), s, 3), a, b, c)]
    predicted: set[tuple[int, int, int]] = set()
    axis_orbits = []
    for s in short_axes:
        orbit_set = set()
        for p in reps:
            orbit = tuple(
                sorted(class_of(add(p, s, k), reps, a, b, c) for k in range(3))
            )
            assert len(set(orbit)) == 3
            orbit_set.add(orbit)
        assert len(orbit_set) == n // 3
        axis_orbits.append(orbit_set)
        predicted |= orbit_set
    assert missing == predicted
    assert len(short_axes) in (0, 1, 3)

    # Local proof premise: every corner of every missing triangle is opposite
    # in the surface six-cycle, not merely nonfacial.
    for f in missing:
        for v in f:
            x, y = sorted(set(f) - {v})
            assert link_distance(v, x, y, faces) == 3

    if len(short_axes) == 0:
        status = "torus"
        expected = (1, 2, 1)
        assert not missing
    elif len(short_axes) == 1:
        status = "one_axis"
        expected = (1, 1, n // 3)
        assert n % 3 == 0 and len(missing) == n // 3
        assert set().union(*axis_orbits) == missing
        vertex_use = Counter(itertools.chain.from_iterable(missing))
        assert set(vertex_use) == set(range(n)) and set(vertex_use.values()) == {1}
    else:
        status = "three_axes"
        expected = (1, 0, 8)
        assert n == 9 and len(missing) == 9
        # K_3,3,3 check: complement components are three independent triples.
        comp_edges = {
            (x, y)
            for x in range(n)
            for y in range(x + 1, n)
            if y not in adj[x]
        }
        comp_adj = [set() for _ in range(n)]
        for x, y in comp_edges:
            comp_adj[x].add(y)
            comp_adj[y].add(x)
        components = []
        unseen = set(range(n))
        while unseen:
            root = min(unseen)
            seen = {root}
            todo = [root]
            while todo:
                x = todo.pop()
                for y in comp_adj[x] - seen:
                    seen.add(y)
                    todo.append(y)
            components.append(seen)
            unseen -= seen
        assert sorted(map(len, components)) == [3, 3, 3]
        assert all(
            sum(1 for e in comp_edges if set(e) <= part) == 3 for part in components
        )

    betti = {str(p): betti_numbers(n, edges, triangles, p) for p in (2, 3, 5)}
    assert set(betti.values()) == {expected}
    return {
        "hnf": [a, b, c],
        "n": n,
        "status": status,
        "axes": len(short_axes),
        "missing": len(missing),
        "betti": list(expected),
    }


def enumerate_rows(bound: int) -> list[dict[str, object]]:
    rows = []
    for n in range(1, bound + 1):
        for a in range(1, n + 1):
            if n % a:
                continue
            c = n // a
            for b in range(a):
                rows.append(analyze(a, b, c))
    return rows


def summarize(rows: list[dict[str, object]], bound: int) -> dict[str, object]:
    prefix = [r for r in rows if int(r["n"]) <= bound]
    counts = Counter(str(r["status"]) for r in prefix)
    compact = [
        [r["hnf"], r["status"], r.get("axes"), r.get("missing"), r.get("betti")]
        for r in prefix
    ]
    digest = hashlib.sha256(
        json.dumps(compact, separators=(",", ":"), sort_keys=True).encode()
    ).hexdigest()
    first = {}
    for status in ("invalid", "K4_excluded", "three_axes", "one_axis", "torus"):
        candidates = [r for r in prefix if r["status"] == status]
        if candidates:
            first[status] = min(candidates, key=lambda r: (int(r["n"]), r["hnf"]))
    return {
        "bound": bound,
        "parameter_tuples": len(prefix),
        "counts": dict(sorted(counts.items())),
        "row_sha256": digest,
        "first_examples": first,
    }


def fixture_checks(rows: list[dict[str, object]]) -> dict[str, object]:
    by_hnf = {tuple(r["hnf"]): r for r in rows}
    expected = {
        (7, 2, 1): "K4_excluded",  # the seven-vertex K7 torus
        (4, 1, 2): "K4_excluded",  # smallest eight-vertex K4 control
        (3, 0, 3): "three_axes",    # K_3,3,3
        (3, 0, 4): "one_axis",
        (3, 1, 4): "one_axis",
        (4, 0, 4): "torus",
    }
    for hnf, status in expected.items():
        assert by_hnf[hnf]["status"] == status
    # Algebraic adversaries to the disk-attachment reduction.
    # A nonprimitive x^2 attachment has H_1 = Z + Z/2, unlike the theorem's
    # torsion-free wedge; independent transverse x,y attachments kill H_1.
    nonprimitive = abelian_h1_two_generators([(2, 0)])
    transverse = abelian_h1_two_generators([(1, 0), (0, 1)])
    parallel = abelian_h1_two_generators([(1, 0), (1, 0), (-1, 0)])
    assert nonprimitive == "Z + Z/2"
    assert transverse == "0"
    assert parallel == "Z"
    return {
        "lattice_fixtures": {str(k): by_hnf[k] for k in expected},
        "nonprimitive_loop_control_H1": nonprimitive,
        "transverse_primitive_controls_H1": transverse,
        "parallel_primitive_m_disks_H1": parallel,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, default=60)
    args = parser.parse_args()
    if args.bound < 60:
        parser.error("bound must be at least 60")
    rows = enumerate_rows(args.bound)
    summary60 = summarize(rows, 60)
    assert summary60["parameter_tuples"] == 3014
    assert summary60["counts"] == {
        "K4_excluded": 317,
        "invalid": 519,
        "one_axis": 153,
        "three_axes": 1,
        "torus": 2024,
    }
    summaries = [summary60]
    if args.bound != 60:
        summaries.append(summarize(rows, args.bound))
    out = {
        "method": "BFS coset transversal; subgroup-membership equality; direct F_2,F_3,F_5 chains",
        "summaries": summaries,
        "fixture_checks": fixture_checks(rows),
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
