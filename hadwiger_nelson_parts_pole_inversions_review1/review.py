#!/usr/bin/env python3
"""Clean-room review of the Parts509 source-pole inversion gate.

This file deliberately does not import code from the target package.  It reads
only the hash-pinned coordinate JSON and reconstructs the finite-field images,
inverted points, residue graphs, degeneracy reductions, and positive
four-colourings.
"""

from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import isqrt
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "hadwiger_nelson_parts509_degree_pool_minimum" / "certificate_D7.json"
TARGET = ROOT / "hadwiger_nelson_parts_pole_inversions"
EXPECTED_SOURCE_SHA256 = "41a47be8d0568be7e1497f16a45c17d433e31e01fb62877856189fbf1ad53729"
TARGET_STREAM_SHA256 = "956fdb8478b527ac69c858e05a1a6430592684c9b6698c14fec9ab85645443a7"
TARGET_CERTIFICATE_SHA256 = "821d530500889925b044eaf0dedb937f827ff36c7b269a2f41791386a682a29a"
PRIME = 1_000_000_271
PAIR_COUNT = 508 * 507 // 2
RAD8 = (1, 3, 5, 15, 11, 33, 55, 165)
RAD4 = (1, 5, 33, 165)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256((data + "\n").encode()).hexdigest()


def source_rows() -> list[tuple[list[Fraction], list[Fraction]]]:
    require(sha256(SOURCE) == EXPECTED_SOURCE_SHA256, "source coordinate hash changed")
    raw = json.loads(SOURCE.read_text())["coordinates"]
    require({str(i) for i in range(509)} <= set(raw), "source labels do not contain 0..508")
    rows = []
    for i in range(509):
        pair = raw[str(i)]
        require(len(pair) == 2 and all(len(row) == 8 for row in pair), "malformed coordinate row")
        rows.append(tuple([Fraction(x) for x in row] for row in pair))
    require(len(set((tuple(x), tuple(y)) for x, y in rows)) == 509, "source coordinate collision")
    return rows


def prime_and_roots() -> tuple[int, int, int]:
    require(PRIME % 4 == 3, "review square-root shortcut unavailable")
    require(all(PRIME % d for d in range(2, isqrt(PRIME) + 1)), "review modulus is composite")
    roots = tuple(pow(a, (PRIME + 1) // 4, PRIME) for a in (3, 5, 11))
    require(all(r * r % PRIME == a for r, a in zip(roots, (3, 5, 11))), "missing radical image")
    return roots


def project_source(
    rows: list[tuple[list[Fraction], list[Fraction]]],
    signs: tuple[int, int],
) -> tuple[np.ndarray, dict[str, int]]:
    """Evaluate the original eight-radical Cartesian rows directly in F_p.

    sqrt(3) uses the deterministic root from Euler's criterion.  The two sign
    choices independently conjugate sqrt(5) and sqrt(11); these induce all four
    maps of the squared-distance field Q(sqrt(5),sqrt(33)).
    """
    p = PRIME
    r3, r5, r11 = prime_and_roots()
    r5 = r5 if signs[0] == 1 else (-r5) % p
    r11 = r11 if signs[1] == 1 else (-r11) % p
    basis = (1, r3, r5, r3 * r5 % p, r11, r3 * r11 % p, r5 * r11 % p, r3 * r5 % p * r11 % p)
    require(all(x * x % p == r for x, r in zip(basis, RAD8)), "bad Cartesian radical basis")

    def evaluate(row: list[Fraction]) -> int:
        total = 0
        for coefficient, image in zip(row, basis):
            require(coefficient.denominator % p != 0, "source denominator vanishes modulo p")
            residue = coefficient.numerator % p * pow(coefficient.denominator, -1, p) % p
            total = (total + residue * image) % p
        return total

    xy = np.array([(evaluate(x), evaluate(y)) for x, y in rows], dtype=np.int64)
    metadata = {
        "sqrt3": r3,
        "sqrt5": r5,
        "sqrt11": r11,
        "sqrt33": r3 * r11 % p,
    }
    return xy, metadata


def dsatur_core(adj: list[list[int]], core: list[int]) -> list[int] | None:
    """Find a positive four-colouring; failure is never used as an UNSAT proof."""
    colours = [-1] * len(adj)
    remaining = set(core)

    def search() -> bool:
        if not remaining:
            return True
        vertex = max(
            remaining,
            key=lambda v: (len({colours[u] for u in adj[v] if colours[u] >= 0}), len(adj[v]), -v),
        )
        forbidden = {colours[u] for u in adj[vertex] if colours[u] >= 0}
        remaining.remove(vertex)
        for colour in range(4):
            if colour not in forbidden:
                colours[vertex] = colour
                if search():
                    return True
        colours[vertex] = -1
        remaining.add(vertex)
        return False

    return colours if search() else None


def positive_word(edges: list[tuple[int, int]], order: int = 508) -> tuple[str, int]:
    """Peel degree-at-most-three vertices with a heap, then colour any 4-core."""
    adj = [[] for _ in range(order)]
    incident: set[int] = set()
    for u, v in edges:
        require(0 <= u < v < order, "edge outside canonical local labels")
        adj[u].append(v)
        adj[v].append(u)
        incident.add(u)
        incident.add(v)
    active = [False] * order
    degree = [0] * order
    heap: list[tuple[int, int]] = []
    for v in incident:
        active[v] = True
        degree[v] = len(adj[v])
        heapq.heappush(heap, (degree[v], v))
    removed: list[int] = []
    while heap:
        d, v = heapq.heappop(heap)
        if not active[v] or d != degree[v]:
            continue
        if d > 3:
            break
        active[v] = False
        removed.append(v)
        for u in adj[v]:
            if active[u]:
                degree[u] -= 1
                heapq.heappush(heap, (degree[u], u))
    core = [v for v in incident if active[v]]
    colours = dsatur_core(adj, core)
    require(colours is not None, "independent search did not find a four-colouring")
    for v in reversed(removed):
        forbidden = {colours[u] for u in adj[v] if colours[u] >= 0}
        colours[v] = next(c for c in range(4) if c not in forbidden)
    for v in range(order):
        if colours[v] < 0:
            colours[v] = 0
    require(all(colours[u] != colours[v] for u, v in edges), "constructed word is improper")
    return "".join(map(str, colours)), len(core)


def scan_projection(
    xy: np.ndarray,
    roots: dict[str, int],
    published_certificate: dict[tuple[int, int], dict[str, object]] | None = None,
) -> dict[str, object]:
    """Directly invert all points and enumerate residue graphs for one projection."""
    start_time = time.time()
    p = PRIME
    require(2 * (p - 1) ** 2 < 2**63, "int64 direct squared-norm bound fails")
    dx = xy[:, 0, None] - xy[None, :, 0]
    dy = xy[:, 1, None] - xy[None, :, 1]
    norms = (dx * dx + dy * dy) % p
    require(np.count_nonzero(norms) == 509 * 508, "projected off-diagonal source distance vanished")
    pair_u, pair_v = np.triu_indices(508, 1)
    stream_hash = hashlib.sha256()
    histogram: Counter[int] = Counter()
    residual_rows = []
    pole_rows = []
    largest: dict[str, int] | None = None
    published_word_checks = 0

    for pole in range(509):
        ids = np.array([i for i in range(509) if i != pole], dtype=np.int64)
        vx = (xy[ids, 0] - xy[pole, 0]) % p
        vy = (xy[ids, 1] - xy[pole, 1]) % p
        inv = np.array([pow(int(norms[pole, i]), -1, p) for i in ids], dtype=np.int64)
        qx = vx * inv % p
        qy = vy * inv % p
        ex = qx[pair_u] - qx[pair_v]
        ey = qy[pair_u] - qy[pair_v]
        values = (ex * ex + ey * ey) % p
        require(np.count_nonzero(values) == PAIR_COUNT, "inverted point collision in finite-field image")
        stream_hash.update(values.astype("<u4").tobytes())

        permutation = np.argsort(values, kind="stable")
        sorted_values = values[permutation]
        starts = np.r_[0, np.flatnonzero(sorted_values[1:] != sorted_values[:-1]) + 1]
        counts = np.diff(np.r_[starts, PAIR_COUNT])
        histogram.update(map(int, counts))
        rich = 0
        nondegenerate = 0
        local_max = int(counts.max())
        for lo, count in zip(starts[counts >= 10], counts[counts >= 10]):
            rich += 1
            chosen = permutation[lo : lo + count]
            edges = list(zip(map(int, pair_u[chosen]), map(int, pair_v[chosen])))
            word, core_order = positive_word(edges)
            if core_order:
                nondegenerate += 1
                residue = int(sorted_values[lo])
                if published_certificate is not None:
                    require((pole, residue) in published_certificate, "published certificate misses a residual bucket")
                    published = published_certificate[(pole, residue)]
                    published_word = published.get("word")
                    require(published.get("edges") == int(count), "published certificate edge count differs")
                    require(isinstance(published_word, str) and len(published_word) == 508,
                            "published certificate has a malformed word")
                    require(set(published_word) <= set("0123"), "published certificate uses a fifth colour")
                    require(all(published_word[u] != published_word[v] for u, v in edges),
                            "published certificate word is improper")
                    published_word_checks += 1
                residual_rows.append(
                    {
                        "pole": pole,
                        "residue": residue,
                        "edges": int(count),
                        "core_order": core_order,
                        "word_sha256": hashlib.sha256(word.encode()).hexdigest(),
                    }
                )
            candidate = {"pole": pole, "residue": int(sorted_values[lo]), "edges": int(count)}
            if largest is None or candidate["edges"] > largest["edges"]:
                largest = candidate
        pole_rows.append(
            {
                "pole": pole,
                "buckets": int(len(counts)),
                "rich": rich,
                "nondegenerate": nondegenerate,
                "max_edges": local_max,
            }
        )

    require(largest is not None, "no rich bucket encountered")
    if published_certificate is not None:
        require(published_word_checks == len(published_certificate), "published certificate has extra rows")
    residual_key_rows = [{k: row[k] for k in ("pole", "residue", "edges")} for row in residual_rows]
    result = {
        "roots": roots,
        "poles": 509,
        "points_per_drawing": 508,
        "scale_representatives": 509 * PAIR_COUNT,
        "residue_buckets": sum(row["buckets"] for row in pole_rows),
        "buckets_with_at_least_ten_edges": sum(row["rich"] for row in pole_rows),
        "three_degenerate_buckets": sum(row["buckets"] for row in pole_rows) - len(residual_rows),
        "residual_buckets": len(residual_rows),
        "largest_supergraph": largest,
        "stream_sha256": stream_hash.hexdigest(),
        "pole_inventory_sha256": canonical_hash(pole_rows),
        "edge_histogram_sha256": canonical_hash(dict(sorted(histogram.items()))),
        "residual_keys_sha256": canonical_hash(residual_key_rows),
        "independent_words_sha256": canonical_hash(residual_rows),
        "max_core_order": max((row["core_order"] for row in residual_rows), default=0),
        "published_word_checks": published_word_checks,
        "seconds": time.time() - start_time,
    }
    return result


def kadd(a: tuple[Fraction, ...], b: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(x + y for x, y in zip(a, b))


def ksub(a: tuple[Fraction, ...], b: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(x - y for x, y in zip(a, b))


def kscale(a: tuple[Fraction, ...], scalar: Fraction) -> tuple[Fraction, ...]:
    return tuple(scalar * x for x in a)


def kmul(a: tuple[Fraction, ...], b: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    out = [Fraction(0) for _ in range(4)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i ^ j] += x * y * RAD4[i & j]
    return tuple(out)


def exact_points(rows: list[tuple[list[Fraction], list[Fraction]]]):
    points = []
    for x, y in rows:
        require(all(x[i] == 0 for i in (1, 3, 4, 6)), "unexpected x parity")
        require(all(y[i] == 0 for i in (0, 2, 5, 7)), "unexpected y parity")
        xx = (x[0], x[2], x[5], x[7])
        yy = (y[1], y[3], y[4] / 3, y[6] / 3)
        points.append((xx, yy))
    require(len(set(points)) == 509, "four-basis source collision")
    return points


def exact_squared_distance(a, b) -> tuple[Fraction, ...]:
    dx = ksub(a[0], b[0])
    dy = ksub(a[1], b[1])
    return kadd(kmul(dx, dx), kscale(kmul(dy, dy), Fraction(3)))


def exact_record_fixture(rows) -> dict[str, object]:
    """Count the pole-0, scale-2/3 edges via 4*d_ij = 9*d_0i*d_0j."""
    points = exact_points(rows)
    zero = (Fraction(0),) * 4
    pole_distances = [None] + [exact_squared_distance(points[0], points[i]) for i in range(1, 509)]
    require(all(d != zero for d in pole_distances[1:]), "source point equals pole")
    edges = []
    for i, j in combinations(range(1, 509), 2):
        dij = exact_squared_distance(points[i], points[j])
        if kscale(dij, Fraction(4)) == kscale(kmul(pole_distances[i], pole_distances[j]), Fraction(9)):
            edges.append((i - 1, j - 1))
    word, core_order = positive_word(edges)
    edge_bytes = "".join(f"{u} {v}\n" for u, v in edges).encode()
    return {
        "pole": 0,
        "scale_numerator": 2,
        "scale_denominator": 3,
        "points": 508,
        "edges": len(edges),
        "pair_checks": PAIR_COUNT,
        "edges_sha256": hashlib.sha256(edge_bytes).hexdigest(),
        "core_order": core_order,
        "word_sha256": hashlib.sha256(word.encode()).hexdigest(),
    }


def controls() -> dict[str, int]:
    k4 = list(combinations(range(4), 2))
    k5 = list(combinations(range(5), 2))
    word, core = positive_word(k4, 5)
    require(core == 0 and all(word[u] != word[v] for u, v in k4), "K4 control failed")
    try:
        positive_word(k5, 5)
    except ValueError:
        rejected = 1
    else:
        raise ValueError("K5 accepted as four-colourable")

    # Direct rational inversion of a four-point source creates a unit triangle.
    # The y-coordinate is represented as a coefficient of sqrt(3): 1/6.
    inverted = []
    for x, ycoef in ((Fraction(1), Fraction(0)), (Fraction(1, 2), Fraction(0)), (Fraction(1, 2), Fraction(1, 6))):
        norm = x * x + 3 * ycoef * ycoef
        inverted.append((x / norm, ycoef / norm))
    require(all((inverted[i][0] - inverted[j][0]) ** 2 + 3 * (inverted[i][1] - inverted[j][1]) ** 2 == 1
                for i, j in combinations(range(3), 2)), "inversion triangle control failed")
    return {"positive_graph_controls": 1, "negative_graph_controls": rejected, "inversion_controls": 1}


def run(check_expected: bool) -> dict[str, object]:
    started = time.time()
    rows = source_rows()
    require(sha256(TARGET / "certificate.json") == TARGET_CERTIFICATE_SHA256, "target certificate hash changed")
    published_rows = json.loads((TARGET / "certificate.json").read_text())
    published_certificate = {(row["pole"], row["residue"]): row for row in published_rows}
    require(len(published_certificate) == len(published_rows) == 17, "published certificate keys repeat")
    projections = []
    for sign5, sign11 in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        xy, roots = project_source(rows, (sign5, sign11))
        projection = scan_projection(
            xy,
            roots,
            published_certificate if (sign5, sign11) == (1, 1) else None,
        )
        projection["sign5"] = sign5
        projection["sign11"] = sign11
        projections.append(projection)
        print(
            f"projection {sign5:+d},{sign11:+d}: buckets={projection['residue_buckets']} "
            f"residual={projection['residual_buckets']} max={projection['largest_supergraph']['edges']} "
            f"seconds={projection['seconds']:.3f}",
            flush=True,
        )
    require(any(p["stream_sha256"] == TARGET_STREAM_SHA256 for p in projections),
            "none of the four conjugate projections reproduces the target stream")
    fixture = exact_record_fixture(rows)
    result = {
        "source_sha256": sha256(SOURCE),
        "target_certificate_sha256": sha256(TARGET / "certificate.json"),
        "prime": PRIME,
        "projection_count": len(projections),
        "projections": projections,
        "exact_fixture": fixture,
        "controls": controls(),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "PASS": True,
        "seconds": time.time() - started,
    }
    if check_expected:
        expected = json.loads((HERE / "expected.json").read_text())
        stable = json.loads(json.dumps(result))
        stable.pop("seconds")
        stable.pop("python")
        stable.pop("numpy")
        for projection in stable["projections"]:
            projection.pop("seconds")
        require(stable == expected, "review output differs from expected.json")
    print(json.dumps(result, indent=2), flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    run(args.check_expected)
