#!/usr/bin/env python3
"""Independent exact audit of all pair-anchored Parts/Moser overlays."""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import math
import time
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path


RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
ZERO = (0,) * 8
ONE = (1,) + (0,) * 7


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(a, k):
    return tuple(k * x for x in a)


def mul(a, b):
    out = [0] * 8
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i ^ j] += x * y * RADICANDS[i & j]
    return tuple(out)


def inverse(a):
    """Inverse in the real degree-eight field by rational row reduction."""
    columns = [mul(a, tuple(int(i == j) for i in range(8))) for j in range(8)]
    matrix = [[F(columns[j][i]) for j in range(8)] + [F(i == 0)] for i in range(8)]
    for j in range(8):
        pivot = next(i for i in range(j, 8) if matrix[i][j])
        matrix[j], matrix[pivot] = matrix[pivot], matrix[j]
        q = matrix[j][j]
        matrix[j] = [x / q for x in matrix[j]]
        for i in range(8):
            if i != j and matrix[i][j]:
                q = matrix[i][j]
                matrix[i] = [x - q * y for x, y in zip(matrix[i], matrix[j])]
    answer = tuple(matrix[i][8] for i in range(8))
    need(mul(a, answer) == ONE, "real inverse")
    return answer


def cadd(a, b):
    return add(a[:8], b[:8]) + add(a[8:], b[8:])


def csub(a, b):
    return sub(a[:8], b[:8]) + sub(a[8:], b[8:])


def cscale(a, k):
    return scale(a[:8], k) + scale(a[8:], k)


def cmul(a, b):
    return sub(mul(a[:8], b[:8]), mul(a[8:], b[8:])) + add(
        mul(a[:8], b[8:]), mul(a[8:], b[:8])
    )


def conjugate(a):
    return a[:8] + scale(a[8:], -1)


def norm(a):
    return add(mul(a[:8], a[:8]), mul(a[8:], a[8:]))


def cdiv(a, b):
    numerator = cmul(a, conjugate(b))
    denominator_inverse = inverse(norm(b))
    return mul(numerator[:8], denominator_inverse) + mul(numerator[8:], denominator_inverse)


def spindle():
    z = ZERO + ZERO
    one = ONE + ZERO
    omega = (F(1, 2),) + (0,) * 7 + (0, F(1, 2)) + (0,) * 6
    rho = (F(5, 6),) + (0,) * 7 + (0, 0, 0, 0, F(1, 6), 0, 0, 0)
    return (z, one, omega, cadd(one, omega), rho, cmul(rho, omega), cmul(rho, cadd(one, omega)))


def unpack(raw, count):
    need(len(raw) == (count + 3) // 4, "packed colour length")
    need(count % 4 == 0 or raw[-1] >> (2 * (count % 4)) == 0, "unused colour bits")
    return [(raw[i // 4] >> (2 * (i % 4))) & 3 for i in range(count)]


def load_colour_libraries(root, base_edges):
    critical = root / "hadwiger_nelson_parts509_criticality/certificate.json"
    quad = root / "hadwiger_nelson_parts509_quad_closure/certificate.json.gz"
    need(hashlib.sha256(critical.read_bytes()).hexdigest() == "d354f9629c41639168b80fc1aa6feb6e4187dd37dee7efcb83b4ef6ebe68d16c", "critical certificate hash")
    need(hashlib.sha256(quad.read_bytes()).hexdigest() == "33e22b281bf05e550b31f644e62ad10acad781bb258a3f92f0aa043fe97642c5", "quad certificate hash")
    data = json.loads(critical.read_text())
    packed = base64.b64decode(data["deletion_colorings_base64"], validate=True)
    need(len(packed) == 509 * 127, "critical row framing")
    libraries = []
    for deleted in range(509):
        word = unpack(packed[deleted * 127 : (deleted + 1) * 127], 508)
        word.insert(deleted, -1)
        libraries.append([word])
    data = json.loads(gzip.decompress(quad.read_bytes()))
    packed = base64.b64decode(data["family_rows_base64"], validate=True)
    offset = 0
    for deleted, count in enumerate(data["family_sizes"]):
        need(type(count) is int and count >= 0, "quad family size")
        for _ in range(count):
            word = unpack(packed[offset : offset + 127], 508)
            offset += 127
            word.insert(deleted, -1)
            libraries[deleted].append(word)
    need(offset == len(packed), "quad row framing")
    checks = 0
    for deleted, words in enumerate(libraries):
        for word in words:
            need(word[deleted] == -1 and len(word) == 509, "deletion word shape")
            need(
                all(word[a] != word[b] for a, b in base_edges if deleted not in (a, b)),
                "improper imported deletion word",
            )
            checks += 1
    return libraries, checks


def modular_values(point, prime, roots):
    basis = [math.prod(roots[j] for j in range(3) if i >> j & 1) % prime for i in range(8)]
    return (
        sum(a * b for a, b in zip(point[:8], basis)) % prime,
        sum(a * b for a, b in zip(point[8:], basis)) % prime,
    )


def build_geometry(root, progress=False):
    points_path = root / "hadwiger_nelson_parts509_completion_census_degree9/points.tsv"
    raw = points_path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50", "point source hash")
    parts = [tuple(map(int, line.split())) for line in raw.decode().splitlines() if not line.startswith("#")]
    need(len(parts) == 509 and all(len(p) == 16 for p in parts), "Parts point table")
    need(len(set(parts)) == 509, "Parts points distinct")

    motif = spindle()
    unit = ONE
    motif_edges = [(i, j) for i, j in combinations(range(7), 2) if norm(csub(motif[i], motif[j])) == unit]
    need(len(motif_edges) == 11, "Moser spindle edges")
    colour_counts = {
        colours: sum(
            all(word[a] != word[b] for a, b in motif_edges)
            for word in product(range(colours), repeat=7)
        )
        for colours in (3, 4)
    }
    need(colour_counts == {3: 0, 4: 384}, "Moser spindle chromatic control")

    # For every unordered source pair, enumerate both endpoint orders and both
    # chiralities.  Canonical normalized images remove duplicate routes.
    templates = defaultdict(set)
    for i, j in combinations(range(7), 2):
        length = norm(csub(motif[j], motif[i]))
        for left, right in ((i, j), (j, i)):
            shape = tuple(cdiv(csub(m, motif[left]), csub(motif[right], motif[left])) for m in motif)
            templates[length].add(tuple(sorted(shape)))
            templates[length].add(tuple(sorted(conjugate(p) for p in shape)))
    denominator = math.lcm(
        *(F(c).denominator for shapes in templates.values() for shape in shapes for p in shape for c in p)
    )
    need(denominator == 72, "template denominator")
    integer_templates = {}
    for length, shapes in templates.items():
        key = tuple(int(F(c) * 96**2) for c in length)
        need(all(F(c * 96**2).denominator == 1 for c in length), "scaled source length")
        integer_templates[key] = [
            tuple(tuple(int(F(c) * denominator) for c in p) for p in shape)
            for shape in sorted(shapes)
        ]

    base_edges = []
    matching = defaultdict(list)
    for a, b in combinations(range(509), 2):
        length = norm(csub(parts[b], parts[a]))
        if length == scale(ONE, 96**2):
            base_edges.append((a, b))
        if length in integer_templates:
            matching[length].append((a, b))
    need(len(base_edges) == 2442, "Parts strict edge count")

    parts_scaled = {cscale(p, denominator): i for i, p in enumerate(parts)}
    placements = set()
    routes = 0
    for length, shapes in integer_templates.items():
        for a, b in matching[length]:
            delta = csub(parts[b], parts[a])
            origin = cscale(parts[a], denominator)
            for shape in shapes:
                image = tuple(sorted(cadd(origin, cmul(delta, p)) for p in shape))
                need(len(set(image)) == 7, "degenerate spindle image")
                placements.add(image)
                routes += 1
    coordinate_scale = 96 * denominator
    scaled_parts = set(parts_scaled)
    external = sorted({p for image in placements for p in image if p not in scaled_parts})
    external_index = {p: i for i, p in enumerate(external)}
    need(len(external) == 24751, "external point count")
    if progress:
        print("placements", len(placements), "external", len(external), flush=True)

    # A different checked finite-field embedding supplies rejection only;
    # every modular survivor is decided again by the exact norm.
    prime = 1000199
    roots = (299728, 494204, 217245)
    need(all(pow(root, 2, prime) == radicand for root, radicand in zip(roots, (3, 5, 11))), "modular roots")
    inv96 = pow(96, -1, prime)
    inv_den = pow(coordinate_scale, -1, prime)
    parts_mod = [tuple(value * inv96 % prime for value in modular_values(p, prime, roots)) for p in parts]
    neighbours = []
    modular_survivors = 0
    exact_unit = scale(ONE, coordinate_scale**2)
    for q_index, q in enumerate(external):
        qx, qy = (value * inv_den % prime for value in modular_values(q, prime, roots))
        row = []
        for vertex, (px, py) in enumerate(parts_mod):
            if ((qx - px) ** 2 + (qy - py) ** 2 - 1) % prime == 0:
                modular_survivors += 1
                if norm(csub(q, cscale(parts[vertex], denominator))) == exact_unit:
                    row.append(vertex)
        neighbours.append(row)
        if progress and q_index % 5000 == 0:
            print("external incidence", q_index, flush=True)

    assemblies = []
    overlap_histogram = Counter()
    five_degree_gate = 0
    for image in placements:
        overlap = sorted(parts_scaled[p] for p in image if p in parts_scaled)
        fresh_points = sorted(p for p in image if p not in parts_scaled)
        fresh = tuple(external_index[p] for p in fresh_points)
        edges = tuple(
            (i, j)
            for i, j in combinations(range(len(fresh)), 2)
            if norm(csub(fresh_points[i], fresh_points[j])) == exact_unit
        )
        degrees = [len(neighbours[q]) for q in fresh]
        for i, j in edges:
            degrees[i] += 1
            degrees[j] += 1
        overlap_histogram[len(overlap)] += 1
        if fresh:
            assemblies.append({"fresh": fresh, "edges": edges, "overlap": tuple(overlap)})
            five_degree_gate += len(fresh) == 5 and min(degrees) >= 4

    assemblies.sort(key=lambda row: (row["fresh"], row["overlap"]))
    return {
        "parts": parts,
        "external": external,
        "neighbours": neighbours,
        "assemblies": assemblies,
        "base_edges": base_edges,
        "scale": coordinate_scale,
        "summary": {
            "template_counts": [len(integer_templates[k]) for k in integer_templates],
            "matching_pair_counts": [len(matching[k]) for k in integer_templates],
            "routes": routes,
            "placements": len(placements),
            "overlap_histogram": dict(overlap_histogram),
            "fresh_points": len(external),
            "modular_unit_survivors": modular_survivors,
            "noncontained_placements": len(assemblies),
            "five_fresh_minimum_degree_at_least_four": five_degree_gate,
            "placements_sha256": digest(sorted(placements)),
            "external_points_sha256": digest(external),
            "neighbours_sha256": digest(neighbours),
            "assemblies_sha256": digest(assemblies),
            "moser_colouring_counts": {
                str(key): value for key, value in colour_counts.items()
            },
        },
    }


@lru_cache(maxsize=None)
def extendable(edges, masks):
    n = len(masks)
    adjacency = [0] * n
    for a, b in edges:
        adjacency[a] |= 1 << b
        adjacency[b] |= 1 << a

    def visit(remaining, chosen):
        if not remaining:
            return True
        candidates = [i for i in range(n) if remaining >> i & 1]
        vertex = min(
            candidates,
            key=lambda i: sum(
                not any(chosen[j] == colour for j in range(n) if adjacency[i] >> j & 1)
                for colour in range(4)
                if masks[i] >> colour & 1
            ),
        )
        forbidden = {chosen[j] for j in range(n) if adjacency[vertex] >> j & 1 and chosen[j] >= 0}
        for colour in range(4):
            if masks[vertex] >> colour & 1 and colour not in forbidden:
                chosen[vertex] = colour
                if visit(remaining & ~(1 << vertex), chosen):
                    return True
        chosen[vertex] = -1
        return False

    return visit((1 << n) - 1, [-1] * n)


def masks(word, fresh, neighbours):
    answer = []
    for q in fresh:
        allowed = 15
        for vertex in neighbours[q]:
            colour = word[vertex]
            if colour >= 0:
                allowed &= ~(1 << colour)
        answer.append(allowed)
    return answer


def obstruction_sets(geometry, libraries, progress=False):
    assemblies = geometry["assemblies"]
    unknown = [[] for _ in assemblies]
    used = set()
    for deleted, words in enumerate(libraries):
        pending = list(range(len(assemblies)))
        for row_index, word in enumerate(words):
            next_pending = []
            cache = {}
            for index in pending:
                assembly = assemblies[index]
                local_masks = []
                for q in assembly["fresh"]:
                    if q not in cache:
                        cache[q] = masks(word, (q,), geometry["neighbours"])[0]
                    local_masks.append(cache[q])
                if extendable(assembly["edges"], tuple(local_masks)):
                    used.add((deleted, row_index))
                else:
                    next_pending.append(index)
            pending = next_pending
            if not pending:
                break
        for index in pending:
            unknown[index].append(deleted)
        if progress and deleted % 50 == 0:
            print("deletion family", deleted, "pending", len(pending), flush=True)
    return unknown, used


def partial_frontier(geometry, libraries, unknown):
    candidates = {}
    routes = 0
    for assembly, blocked in zip(geometry["assemblies"], unknown):
        n = len(assembly["fresh"])
        for size in range(1, min(n, len(blocked) - 1) + 1):
            for positions in combinations(range(n), size):
                key = tuple(assembly["fresh"][i] for i in positions)
                routes += 1
                pos = {old: new for new, old in enumerate(positions)}
                edges = tuple(
                    (pos[a], pos[b])
                    for a, b in assembly["edges"]
                    if a in pos and b in pos
                )
                if key not in candidates:
                    candidates[key] = [set(blocked), edges]
                else:
                    need(candidates[key][1] == edges, "inconsistent induced fresh-edge set")
                    candidates[key][0].intersection_update(blocked)
    frontier = []
    tested = 0
    for fresh, (bound, edges) in sorted(candidates.items()):
        if len(bound) <= len(fresh):
            continue
        tested += 1
        blocked = []
        for deleted in sorted(bound):
            if not any(
                extendable(edges, tuple(masks(word, fresh, geometry["neighbours"])))
                for word in libraries[deleted]
            ):
                blocked.append(deleted)
        if len(blocked) > len(fresh):
            frontier.append({"fresh": fresh, "edges": edges, "unknown": tuple(blocked)})
    return frontier, {
        "subset_routes": routes,
        "distinct_subsets": len(candidates),
        "requiring_new_tests": tested,
        "residual_subsets": len(frontier),
        "target_instances": sum(math.comb(len(row["unknown"]), len(row["fresh"]) + 1) for row in frontier),
        "subset_size_histogram": dict(Counter(len(row["fresh"]) for row in frontier)),
    }


def check_certificate(root, geometry, frontier, path=None):
    if path is None:
        path = root / "hadwiger_nelson_parts_moser_isometry_closure/certificate.json"
    need(hashlib.sha256(path.read_bytes()).hexdigest() == "9315dda9981850529ecb7e816f2c055e3e376796327b878691d7b081b109bacc", "target certificate hash")
    certificate = json.loads(path.read_text())
    need(certificate["format"] == "parts-moser-isometry-colours-v1", "target certificate format")
    rows = {}
    for row in certificate["rows"]:
        key = (tuple(row["fresh"]), tuple(row["deleted"]))
        need(key not in rows, "duplicate target certificate row")
        rows[key] = row
    required = {
        (row["fresh"], deleted)
        for row in frontier
        for deleted in combinations(row["unknown"], len(row["fresh"]) + 1)
    }
    need(set(rows) == required, "target key coverage")
    edge_checks = 0
    exact_unit = scale(ONE, geometry["scale"] ** 2)
    for (fresh, deleted), row in rows.items():
        word = unpack(base64.b64decode(row["colours"], validate=True), 508)
        retained = [vertex for vertex in range(509) if vertex not in deleted]
        need(len(retained) + len(fresh) == 508, "target order")
        colours = {vertex: word[i] for i, vertex in enumerate(retained)}
        colours.update({509 + i: word[len(retained) + i] for i in range(len(fresh))})
        edges = [(a, b) for a, b in geometry["base_edges"] if a not in deleted and b not in deleted]
        edges.extend(
            (vertex, 509 + i)
            for i, q in enumerate(fresh)
            for vertex in geometry["neighbours"][q]
            if vertex not in deleted
        )
        edges.extend(
            (509 + i, 509 + j)
            for i, j in combinations(range(len(fresh)), 2)
            if norm(csub(geometry["external"][fresh[i]], geometry["external"][fresh[j]])) == exact_unit
        )
        need(all(colours[a] != colours[b] for a, b in edges), "improper target certificate row")
        edge_checks += len(edges)
    return {
        "target_rows": len(rows),
        "target_edge_checks": edge_checks,
        "certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def run(root, progress=False, certificate=None):
    started = time.monotonic()
    geometry = build_geometry(root, progress)
    libraries, library_rows = load_colour_libraries(root, geometry["base_edges"])
    unknown, used = obstruction_sets(geometry, libraries, progress)
    frontier, partial = partial_frontier(geometry, libraries, unknown)
    target = check_certificate(root, geometry, frontier, certificate)
    result = {
        "geometry": geometry["summary"],
        "base_colour_rows_checked": library_rows,
        "used_base_rows": len(used),
        "uncovered_histogram": dict(Counter(len(row) for row in unknown)),
        "maximum_uncovered": max(map(len, unknown)),
        "coverage_sha256": digest(unknown),
        "partial": partial,
        "frontier_sha256": digest(frontier),
        **target,
        "all_sub509_subgraphs_four_colourable": True,
    }
    result["wall_seconds_observed"] = round(time.monotonic() - started, 3)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run(args.repo, args.progress, args.certificate)
    stable = {key: value for key, value in result.items() if key != "wall_seconds_observed"}
    if args.check_expected:
        expected_path = Path(__file__).resolve().with_name("EXPECTED.json")
        need(
            json.loads(json.dumps(stable)) == json.loads(expected_path.read_text()),
            "EXPECTED.json mismatch",
        )
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
