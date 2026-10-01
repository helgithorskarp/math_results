"""Exact difference-body bounds for unmarked disc polyomino coronas.

The bound is conditional on an independently established rooted grid-cover
obstruction. This program does not decide coverability or Heesch numbers.
Python 3.11+, standard library; all geometric arithmetic is integral.
"""

from collections import Counter, deque
import argparse
import hashlib
import json
from pathlib import Path

FOUR = ((1, 0), (-1, 0), (0, 1), (0, -1))
MANIFEST_SHA256 = "8f96c536c15f739130b6ca7e5a67fcba1ff1e51fa4bbc18b16d652182c24ff85"
FAMILY_SHA256 = "935192a6bead7d979d7ed60f3907e52278962940d9b3c008d18af94a85fc36ef"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_cells(raw):
    require(isinstance(raw, list) and raw, "cells must be a nonempty list")
    require(all(isinstance(p, list) and len(p) == 2 and
                all(type(x) is int for x in p) for p in raw),
            "each cell must be a pair of integers")
    cells = tuple(map(tuple, raw))
    require(len(set(cells)) == len(cells), "duplicate cells")
    require(is_disc(cells), "tile must be an edge-connected closed disc")
    return normalize(cells)


def normalize(cells):
    cells = tuple(cells)
    require(bool(cells), "cannot normalize an empty cell set")
    xmin = min(x for x, y in cells)
    ymin = min(y for x, y in cells)
    return tuple(sorted((x - xmin, y - ymin) for x, y in cells))


def variants(cells):
    return sorted({normalize((sx * (y if swap else x),
                              sy * (x if swap else y))
                             for x, y in cells)
                   for sx in (-1, 1) for sy in (-1, 1)
                   for swap in (False, True)})


def is_disc(cells):
    cells = set(cells)
    if not cells:
        return False
    seen = {next(iter(cells))}
    queue = deque(seen)
    while queue:
        x, y = queue.popleft()
        for dx, dy in FOUR:
            p = x + dx, y + dy
            if p in cells and p not in seen:
                seen.add(p)
                queue.append(p)
    if seen != cells:
        return False
    vertices = {(x + dx, y + dy) for x, y in cells
                for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1))}
    for x, y in vertices:
        q = [(x - 1, y - 1) in cells, (x, y - 1) in cells,
             (x, y) in cells, (x - 1, y) in cells]
        if q == [True, False, True, False] or q == [False, True, False, True]:
            return False
    xmin, xmax = min(x for x, y in cells) - 1, max(x for x, y in cells) + 1
    ymin, ymax = min(y for x, y in cells) - 1, max(y for x, y in cells) + 1
    exterior = {(xmin, ymin)}
    queue = deque(exterior)
    while queue:
        x, y = queue.popleft()
        for dx, dy in FOUR:
            p = x + dx, y + dy
            if (xmin <= p[0] <= xmax and ymin <= p[1] <= ymax and
                    p not in cells and p not in exterior):
                exterior.add(p)
                queue.append(p)
    return len(exterior) + len(cells) == (xmax - xmin + 1) * (ymax - ymin + 1)


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull(points):
    points = sorted(set(points))
    require(len(points) >= 3, "degenerate hull")
    lower, upper = [], []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return tuple(lower[:-1] + upper[:-1])


def twice_area(poly):
    return sum(a[0] * b[1] - a[1] * b[0]
               for a, b in zip(poly, poly[1:] + poly[:1]))


def support(poly, vector):
    a, b = vector
    return max(a * x + b * y for x, y in poly)


def difference_body(cells):
    vertices = hull((x + dx, y + dy) for x, y in cells
                    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)))
    differences = {(a[0] - b[0], a[1] - b[1]) for a in vertices for b in vertices}
    return hull((sx * (y if swap else x), sy * (x if swap else y))
                for x, y in differences for sx in (-1, 1) for sy in (-1, 1)
                for swap in (False, True))


def ceil_div(a, b):
    require(type(a) is int and type(b) is int and a >= 0 and b > 0,
            "ceil division needs nonnegative numerator and positive denominator")
    return (a + b - 1) // b


def target_rho(cells, target, body):
    """rho=max over target cells t of min over root cells a of h_K(J(t-a))."""
    target = set(target)
    require(target and all(len(p) == 2 and all(type(x) is int for x in p)
                           for p in target), "invalid target")
    return max(min(support(body, (a[1] - t[1], t[0] - a[0]))
                   for a in cells) for t in target)


def radial_target(cells, radius):
    require(type(radius) is int and radius >= 1, "radius must be a positive integer")
    return {(x + dx, y + dy) for x, y in cells
            for dx in range(-radius, radius + 1)
            for dy in range(-radius, radius + 1)}


def upper_from_rho(cells, body, rho):
    # Strict inequality: (H+1)*m < area(K)+2*rho.
    return ceil_div(twice_area(body) + 4 * rho, 2 * len(cells)) - 2


def bound(cells, radius, exact_target=False):
    require(type(radius) is int and radius >= 1, "radius must be a positive integer")
    require(is_disc(cells), "tile must be a closed-disc polyomino")
    cells = normalize(cells)
    body = difference_body(cells)
    diagonal = support(body, (1, 1))
    result = {"area": len(cells), "body": [list(p) for p in body],
              "body_twice_area": twice_area(body), "diagonal_support": diagonal,
              "grid_blocking_radius": radius,
              "uniform_upper": upper_from_rho(cells, body, radius * diagonal)}
    if exact_target:
        rho = target_rho(cells, radial_target(cells, radius), body)
        require(rho <= radius * diagonal, "radial rho exceeds uniform bound")
        result.update(target_rho=rho, target_upper=upper_from_rho(cells, body, rho))
    return result


def growth_family(seed, added=3):
    """Independent local implementation, matched by full ordered-family hash."""
    require(type(added) is int and added >= 0, "invalid number of additions")
    layer = {normalize(seed)}
    counts = []
    for unused in range(added):
        enlarged = set()
        for tile in layer:
            cells = set(tile)
            halo = {(x + dx, y + dy) for x, y in cells for dx, dy in FOUR} - cells
            for p in halo:
                enlarged.add(normalize(cells | {p}))
        layer = enlarged
        counts.append(len(layer))
    return sorted({min(variants(tile)) for tile in layer if is_disc(tile)}), counts


def family_application(seed, manifest_path):
    raw = Path(manifest_path).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA256,
            "prior obstruction manifest bytes do not match")
    manifest = json.loads(raw)
    require(manifest["added_cells"] == 3, "wrong family")
    family, layers = growth_family(seed, 3)
    family_raw = (json.dumps(family, separators=(",", ":")) + "\n").encode()
    digest = hashlib.sha256(family_raw).hexdigest()
    require(digest == FAMILY_SHA256 == manifest["family_sha256"], "family mismatch")
    require(len(family) == len(manifest["cases"]) == 1233, "incomplete family")
    require([row["i"] for row in manifest["cases"]] == list(range(1233)),
            "manifest row indexing mismatch")
    uniform, targeted, old, improvement = Counter(), Counter(), Counter(), Counter()
    by_radius = {}
    rows = []
    periodic = 0
    for row, tile in zip(manifest["cases"], family):
        require(len(tile) == 20, "unexpected area")
        if "radius" not in row:
            require("periodic" in row, "unclassified prior row")
            periodic += 1
            continue
        radius = row["radius"]
        data = bound(tile, radius, exact_target=True)
        w = max(x for x, y in tile) + 1
        h = max(y for x, y in tile) + 1
        L = max(w, h)
        prior = ((w + 2 * radius + 2 * L) * (h + 2 * radius + 2 * L)) // 20 - 1
        u, t = data["uniform_upper"], data["target_upper"]
        require(t <= u < prior, "expected strict improvement failed")
        uniform[u] += 1
        targeted[t] += 1
        old[prior] += 1
        improvement[prior - t] += 1
        by_radius.setdefault(radius, []).append((prior, u, t))
        rows.append([row["i"], radius, data["body_twice_area"],
                     data["diagonal_support"], data["target_rho"], prior, u, t])
    require(len(rows) == 825 and periodic == 408, "prior cohort mismatch")
    encode_counter = lambda c: {str(k): c[k] for k in sorted(c)}
    return {"family_sha256": digest, "prior_manifest_sha256": MANIFEST_SHA256,
            "growth_layer_counts": layers, "family_size": len(family),
            "finite_cases": len(rows), "prior_periodic_cases": periodic,
            "old_upper_histogram": encode_counter(old),
            "uniform_upper_histogram": encode_counter(uniform),
            "target_upper_histogram": encode_counter(targeted),
            "improvement_histogram": encode_counter(improvement),
            "rows_sha256": hashlib.sha256((json.dumps(rows, separators=(",", ":")) + "\n").encode()).hexdigest(),
            "by_grid_blocking_radius": {str(r): {"cases": len(v),
                "old_range": [min(x[0] for x in v), max(x[0] for x in v)],
                "uniform_range": [min(x[1] for x in v), max(x[1] for x in v)],
                "target_range": [min(x[2] for x in v), max(x[2] for x in v)]}
                for r, v in sorted(by_radius.items())}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("input.json"))
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--expected", type=Path)
    args = parser.parse_args()
    inputs = json.loads(args.input.read_text())
    cells = read_cells(inputs["cells"])
    result = {"agent": "six-heesch-1", "role": "researcher",
              "seed": bound(cells, inputs["grid_blocking_radius"], exact_target=True),
              "scope": "conditional arithmetic transfer; no fresh coverability decisions"}
    if args.manifest:
        result["family"] = family_application(cells, args.manifest)
    if args.expected:
        require(result == json.loads(args.expected.read_text()), "expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
