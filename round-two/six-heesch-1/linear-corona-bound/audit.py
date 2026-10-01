"""Definition-level checks of the sweep geometry and bound arithmetic.

No native solver or earlier campaign module is imported. Polygon areas are
also obtained by independent exact vertical-section integration.
"""

from fractions import Fraction
import argparse
import json
from pathlib import Path

import sweep


def check_hull_certificate(points, poly):
    points = set(points)
    sweep.require(len(poly) >= 3 and len(set(poly)) == len(poly), "bad polygon")
    sweep.require(all(p in points for p in poly), "hull vertex absent from input")
    for i, a in enumerate(poly):
        b = poly[(i + 1) % len(poly)]
        c = poly[(i + 2) % len(poly)]
        sweep.require(sweep.cross(a, b, c) > 0, "hull not strictly convex CCW")
        sweep.require(all(sweep.cross(a, b, p) >= 0 for p in points),
                      "input point outside proposed hull")


def section_area(poly):
    """Integrate exact affine top/bottom sections, rather than shoelace area."""
    edges = list(zip(poly, poly[1:] + poly[:1]))
    xs = sorted({p[0] for p in poly})
    total = Fraction(0)
    for left, right in zip(xs, xs[1:]):
        middle = Fraction(left + right, 2)
        heights = []
        for a, b in edges:
            if min(a[0], b[0]) < middle < max(a[0], b[0]):
                heights.append(a[1] + (middle - a[0]) * Fraction(b[1] - a[1], b[0] - a[0]))
        sweep.require(len(heights) == 2, "convex section should have exactly two endpoints")
        total += (right - left) * (max(heights) - min(heights))
    return total


def direct_differences(cells):
    corners = {(x + dx, y + dy) for x, y in cells
               for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1))}
    differences = {(x - u, y - v) for x, y in corners for u, v in corners}
    return {(sx * (y if swap else x), sy * (x if swap else y))
            for x, y in differences for sx in (-1, 1) for sy in (-1, 1)
            for swap in (False, True)}


def small_free_shapes(max_area):
    layer = {((0, 0),)}
    shapes = []
    counts = []
    for area in range(1, max_area + 1):
        counts.append(len(layer))
        shapes.extend(sorted(layer))
        enlarged = set()
        for tile in layer:
            cells = set(tile)
            boundary = {(x + dx, y + dy) for x, y in cells for dx, dy in sweep.FOUR} - cells
            for p in boundary:
                enlarged.add(min(sweep.variants(cells | {p})))
        layer = enlarged
    return shapes, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path)
    args = parser.parse_args()
    shapes, counts = small_free_shapes(6)
    sweep.require(counts == [1, 1, 2, 5, 12, 35], "small free-polyomino count mismatch")
    seed = sweep.read_cells(json.loads(Path(__file__).with_name("input.json").read_text())["cells"])
    shapes += [seed]
    vectors = [(x, y) for x in range(-3, 4) for y in range(-3, 4)]
    sweep_checks = 0
    radial_checks = 0
    phase_checks = 0
    for tile in shapes:
        body = sweep.difference_body(tile)
        raw = direct_differences(tile)
        check_hull_certificate(raw, body)
        sweep.require(section_area(body) * 2 == sweep.twice_area(body), "body area disagreement")
        for dx, dy in vectors:
            points = set(body) | {(x + dx, y + dy) for x, y in body}
            expanded = sweep.hull(points)
            check_hull_certificate(points, expanded)
            direct_area = section_area(expanded)
            formula_area = Fraction(sweep.twice_area(body), 2) + 2 * sweep.support(body, (-dy, dx))
            sweep.require(direct_area == formula_area, "sweep area disagreement")
            sweep_checks += 1
        for radius in range(1, 4):
            rho = sweep.target_rho(tile, sweep.radial_target(tile, radius), body)
            sweep.require(rho == radius * sweep.support(body, (1, 1)), "radial support identity failed")
            radial_checks += 1
        for tx, ty in ((-2, -1), (-1, 2), (0, 1), (1, 0), (1, 1), (2, -2)):
            integer_support = sweep.support(body, (-ty, tx))
            for fx in (Fraction(1, 7), Fraction(1, 2), Fraction(6, 7)):
                for fy in (Fraction(1, 7), Fraction(1, 2), Fraction(6, 7)):
                    qx, qy = tx + fx, ty + fy
                    px, py = max(0, min(1, qx)), max(0, min(1, qy))
                    real_support = sweep.support(body, (-(qy - py), qx - px))
                    sweep.require(real_support < integer_support, "open-cell strict inequality failed")
                    phase_checks += 1
    for radius in range(1, 5):
        monomino = sweep.bound(((0, 0),), radius, exact_target=True)
        sweep.require(monomino["body_twice_area"] == 8 and
                      monomino["diagonal_support"] == 2 and
                      monomino["uniform_upper"] == 4 * radius + 2,
                      "integral threshold should use a strict inequality")
    controls = [[], [[0, 0], [0, 0]], [[0.5, 0]], [[0, 0], [2, 0]],
                [[0, 0], [1, 1]],
                [[0, 0], [1, 0], [2, 0], [0, 1], [2, 1], [0, 2], [1, 2], [2, 2]]]
    rejected = 0
    for raw in controls:
        try:
            sweep.read_cells(raw)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("malformed or nondisc tile was accepted")
    for radius in (0, -1, True, 1.5):
        try:
            sweep.bound(((0, 0),), radius)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("invalid radius was accepted")
    # The hull checker must reject even an inward displacement of one vertex.
    body = sweep.difference_body(seed)
    wrong = list(body)
    wrong[0] = (wrong[0][0] + 1, wrong[0][1])
    try:
        check_hull_certificate(direct_differences(seed), tuple(wrong))
    except ValueError:
        rejected += 1
    else:
        raise ValueError("damaged hull was accepted")
    result = {"small_free_counts": counts, "body_certificates": len(shapes),
              "sweep_area_checks": sweep_checks, "radial_checks": radial_checks,
              "strict_open_cell_checks": phase_checks, "controls_rejected": rejected,
              "seed_body_twice_area": sweep.twice_area(body),
              "seed_diagonal_support": sweep.support(body, (1, 1))}
    if args.expected:
        sweep.require(result == json.loads(args.expected.read_text()), "audit output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
