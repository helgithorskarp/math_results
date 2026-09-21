#!/usr/bin/env python3
"""Exact rational inner/outer strip covers; Python 3.11+, standard library."""
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def interval_union_length(intervals):
    if not intervals:
        return 0
    intervals = sorted(intervals)
    left, right = intervals[0]
    total = 0
    for lo, hi in intervals[1:]:
        require(lo <= hi, "reversed interval")
        if lo > right:
            total += right - left
            left, right = lo, hi
        else:
            right = max(right, hi)
    return total + right - left


def ceil_sqrt(n):
    r = isqrt(n)
    return r + (r*r != n)


def area_bounds(centers, radius, step, scale):
    """Every inner interval is present at EVERY x in the strip, and
    every section is within its outer interval. Return exact areas."""
    require(centers and radius > 0 and step > 0 and scale > 0, "bad input")
    xmin = min(x-radius for x, _ in centers)
    xmax = max(x+radius for x, _ in centers)
    total_inner = total_outer = count = 0
    r2 = radius*radius
    for left in range(xmin, xmax, step):
        right = min(left+step, xmax)
        inner, outer = [], []
        for cx, cy in centers:
            dmin = max(left-cx, cx-right, 0)
            dmax = max(abs(left-cx), abs(right-cx))
            if dmin <= radius:
                hi = ceil_sqrt(r2-dmin*dmin)
                outer.append((cy-hi, cy+hi))
            if dmax <= radius:
                lo = isqrt(r2-dmax*dmax)
                inner.append((cy-lo, cy+lo))
        lo, hi = interval_union_length(inner), interval_union_length(outer)
        require(0 <= lo <= hi, "invalid strip enclosure")
        total_inner += (right-left)*lo
        total_outer += (right-left)*hi
        count += 1
    return (F(total_inner, scale*scale), F(total_outer, scale*scale)), count


def subtract(a, b):
    return a[0]-b[1], a[1]-b[0]


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def strictly_exceeds(bounds, threshold):
    require(bounds[0] > threshold, "positive margin is not certified")


def encode(bounds):
    return [str(x) for x in bounds]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="print summary without expected comparison")
    args = parser.parse_args()
    data = json.loads((ROOT/"fixtures.json").read_text())
    scale, radius, step = (data[k] for k in ("coordinate_scale", "radius", "strip_width"))
    require(scale == radius == 1000000 and step == 125, "unexpected fixture units")
    areas, strips, distances = {}, 0, {}
    for side in ("p", "q"):
        centers = data[side]
        require(len(centers) == 4 and len(set(map(tuple, centers))) == 4, "centers not distinct")
        graph = []
        distances[side] = {}
        for i, j in combinations(range(4), 2):
            squared = sum((centers[i][k]-centers[j][k])**2 for k in range(2))
            pair = data["labels"][i]+data["labels"][j]
            distances[side][pair] = str(F(squared, scale*scale))
            require(squared != 4*radius*radius, "tangent pair")
            if squared < 4*radius*radius:
                graph.append(pair)
        require(graph == ["AB", "AC", "AD", "BC", "BD"], "wrong overlap graph")
        for name, indices in data["bags"].items():
            bounds, count = area_bounds([centers[i] for i in indices], radius, step, scale)
            areas[side+"_"+name] = bounds
            strips += count
        require(areas[side+"_ABC"] == areas[side+"_ABD"], "reflection mismatch")
        identity = subtract(add(areas[side+"_ABC"], areas[side+"_ABD"]),
                            add(areas[side+"_ABCD"], areas[side+"_AB"]))
        require(identity[0] <= 0 <= identity[1], "gluing identity excluded")

    differences = {
        "ABC_local_loss": subtract(areas["p_ABC"], areas["q_ABC"]),
        "ABD_local_loss": subtract(areas["p_ABD"], areas["q_ABD"]),
        "ABCD_global_gain": subtract(areas["q_ABCD"], areas["p_ABCD"]),
        "AB_separator_loss": subtract(areas["p_AB"], areas["q_AB"]),
    }
    for name in ("ABC_local_loss", "ABD_local_loss"):
        strictly_exceeds(differences[name], F(data["local_margin"]))
    strictly_exceeds(differences["ABCD_global_gain"], F(data["global_margin"]))
    require(F(distances["p"]["AC"]) < F(distances["q"]["AC"]),
            "must expose failed contraction hypothesis")

    # Definition-level controls for section unions and enclosures.
    require(interval_union_length([(0, 2), (1, 3), (5, 7)]) == 5, "interval control")
    require(interval_union_length([(0, 1), (1, 2), (0, 2)]) == 2, "touch control")
    single, count = area_bounds([(0, 0)], radius, step, scale)
    strips += count
    require(F(314, 100) < single[0] < single[1] < F(22, 7), "single disk control")
    duplicate, count = area_bounds([(0, 0), (0, 0)], radius, step, scale)
    strips += count
    require(single == duplicate, "duplicate disk control")
    translated, count = area_bounds([(321125, -456250)], radius, step, scale)
    strips += count
    require(single == translated, "translation control")
    # Transpose coordinates, changing the strip decomposition entirely.
    rotated = {}
    for side in ("p", "q"):
        rotated[side], count = area_bounds([(y, -x) for x, y in data[side]], radius, step, scale)
        strips += count
        original = areas[side+"_ABCD"]
        require(max(original[0], rotated[side][0]) <= min(original[1], rotated[side][1]),
                "rotation enclosures incompatible")
    strictly_exceeds(subtract(rotated["q"], rotated["p"]), F(data["global_margin"]))

    rejected = 0
    for bad in (subtract(areas["p_ABC"], areas["p_ABC"]),
                subtract(areas["q_ABC"], areas["p_ABC"])):
        try:
            strictly_exceeds(bad, F(data["local_margin"]))
        except ValueError:
            rejected += 1
    require(rejected == 2, "failed to reject identity/reversed transitions")
    summary = {
        "method": "exact integer inner/outer vertical-strip rectangle covers",
        "strips_total": strips,
        "area_bounds": {k: encode(v) for k, v in sorted(areas.items())},
        "difference_bounds": {k: encode(v) for k, v in sorted(differences.items())},
        "squared_center_distances": distances,
        "rotated_global_bounds": {k: encode(v) for k, v in sorted(rotated.items())},
        "single_disk_bounds": encode(single),
        "negative_controls_rejected": rejected,
        "status": "all analytic margins corroborated; not a pairwise contraction",
    }
    if not args.emit:
        expected = json.loads((ROOT/"expected.json").read_text())
        require(summary == expected, "summary differs from expected.json")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
