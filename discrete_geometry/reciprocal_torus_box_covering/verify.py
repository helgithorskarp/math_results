#!/usr/bin/env python3
"""Exact finite corroboration of PROOF.md; CPython 3.11+, standard library.

Independent routes: a complete endpoint/cell arrangement audit of concrete
covering boxes, and the constructive cyclic-gap selection with all invariants.
All inputs are deterministic. No floating point, solver, network, or data file
is needed except EXPECTED.json when --check is used.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
import json
from math import gcd, prod
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def parameters(ms):
    ms = tuple(ms)
    if not ms or any(type(m) is not int or m < 1 for m in ms):
        raise ValueError("a nonempty tuple of positive integers is required")
    order = sorted(range(len(ms)), key=lambda i: (-ms[i], i))
    sorted_ms = tuple(ms[i] for i in order)
    prefixes = [1]
    for m in sorted_ms:
        prefixes.append(prefixes[-1] * m)
    tails = [1] * (len(ms) + 1)
    for i in reversed(range(len(ms))):
        tails[i] = sorted_ms[i] * tails[i + 1] + 1
    require(tails[0] == sum(prefixes), "prefix/tail count agreement")
    return sorted_ms, order, prefixes, tails


def centers(ms):
    """Explicit grid, mapped back to the supplied coordinate order."""
    _, order, prefixes, tails = parameters(ms)
    total = tails[0]
    out = []
    for j in range(total):
        point = [F(0)] * len(ms)
        for i, original in enumerate(order):
            point[original] = F((prefixes[i] * j) % total, total)
        out.append(tuple(point))
    require(len(set(out)) == total, "centers are not distinct")
    return out


def contains(point, center, sides, closed=False):
    distances = [(x - v) % 1 for x, v in zip(point, center)]
    if closed:
        return all(0 <= d <= a for d, a in zip(distances, sides))
    return all(0 < d < a for d, a in zip(distances, sides))


def circle_patterns(values, side, closed):
    """All endpoint and open-cell coverage masks on one circle."""
    cuts = sorted({v % 1 for v in values} | {(v + side) % 1 for v in values})
    patterns = {}
    for i, x in enumerate(cuts):
        next_x = cuts[(i + 1) % len(cuts)] + int(i + 1 == len(cuts))
        for representative in (x, ((x + next_x) / 2) % 1):
            mask = 0
            for j, v in enumerate(values):
                distance = (representative - v) % 1
                inside = 0 <= distance <= side if closed else 0 < distance < side
                if inside:
                    mask |= 1 << j
            patterns.setdefault(mask, representative)
    return patterns, len(cuts)


def arrangement_cover(points, sides, closed=False):
    """Complete continuum check; no use of prefix/tail counts or gap proof.

    Membership is constant on each open cell and checked separately at
    every endpoint. Coordinate products reduce to intersections of masks.
    Equal prefix masks may be merged: all later intersections depend only
    on that mask. A zero mask yields an exact rational uncovered point.
    """
    if not points or not sides or any(len(p) != len(sides) for p in points):
        raise ValueError("nonempty, dimension-compatible center data required")
    if any(not 0 < a <= 1 for a in sides):
        raise ValueError("side lengths must lie in (0,1]")
    states = {(1 << len(points)) - 1: ()}
    statistics = []
    transitions = 0
    for i, side in enumerate(sides):
        masks, cuts = circle_patterns([p[i] for p in points], side, closed)
        following = {}
        for previous, prefix in states.items():
            for mask, x in masks.items():
                transitions += 1
                meet = previous & mask
                witness = prefix + (x,)
                if not meet:
                    hole = witness + (F(0),) * (len(sides) - len(witness))
                    require(not any(contains(hole, p, sides, closed) for p in points),
                            "reported hole is covered")
                    return {"covered": False, "hole": [str(x) for x in hole],
                            "transitions": transitions, "stages": statistics}
                following.setdefault(meet, witness)
        statistics.append({"cuts": cuts, "coordinate_masks": len(masks),
                           "surviving_masks": len(following)})
        states = following
    return {"covered": True, "transitions": transitions, "stages": statistics}


def cyclic_min_gap(values):
    values = sorted(values)
    if len(values) == 1:
        return F(1)
    return min([b - a for a, b in zip(values, values[1:])]
               + [1 + values[0] - values[-1]])


def constructive_find(ms, target):
    """Return a covering center while checking every proof invariant."""
    sorted_ms, order, prefixes, tails = parameters(ms)
    if len(target) != len(ms):
        raise ValueError("target dimension mismatch")
    if any(not isinstance(x, (int, F)) for x in target):
        raise ValueError("exact rational targets required")
    x = [F(target[i]) % 1 for i in order]
    total = tails[0]
    indices = list(range(total))
    for k, m in enumerate(sorted_ms):
        projected = {j: F((prefixes[k] * j) % total, total) for j in indices}
        require(len(indices) == tails[k], "stage cardinality")
        require(len(set(projected.values())) == len(indices), "selected projection collision")
        delta = F(prefixes[k], total)
        require(cyclic_min_gap(projected.values()) >= delta, "old minimum gap")
        earlier = sum(prefixes[:k])
        defect = prefixes[k] - (m - 1) * earlier
        other = 1 + sum((sorted_ms[j] - m) * prefixes[j] for j in range(k))
        require(defect == other and defect >= 1, "ordering identity")
        q = F(1, m) - F(defect, m * total)
        require(0 < q < F(1, m), "strict reciprocal margin")
        cyclic = sorted(indices, key=lambda j: (projected[j] - x[k]) % 1)
        indices = cyclic[-tails[k + 1]:]
        for j in indices:
            require(0 < (x[k] - projected[j]) % 1 <= q, "coordinate coverage bound")
            for i in range(k):
                require(0 < (x[i] - F(prefixes[i] * j, total)) % 1 < F(1, sorted_ms[i]),
                        "earlier coordinate lost")
        scaled = [F((prefixes[k + 1] * j) % total, total) for j in indices]
        require(len(set(scaled)) == len(indices), "new projection collision")
        require(cyclic_min_gap(scaled) >= F(prefixes[k + 1], total), "new minimum gap")
    require(len(indices) == 1, "final singleton")
    j = indices[0]
    point = [F(0)] * len(ms)
    for i, original in enumerate(order):
        point[original] = F((prefixes[i] * j) % total, total)
    require(contains(target, point, [F(1, m) for m in ms]), "decoder returned wrong center")
    return j


def targets(ms, points):
    total, dim = len(points), len(ms)
    out = [tuple(F(0) for _ in ms)]
    # Exact endpoints, shifted endpoints and nonuniform rational cell points.
    for j in (0, total // 2, total - 1):
        out.append(points[j])
        out.append(tuple((points[j][i] + F(1, ms[i])) % 1 for i in range(dim)))
    for j in range(25):
        out.append(tuple(F((17 * j + 13 * i + 7 * i * j) % (total * ms[i] + j + 1),
                           total * ms[i] + j + 1) for i in range(dim)))
    return out


def run():
    cases = {tuple(reversed(ms)) for n in range(1, 4)
             for ms in combinations_with_replacement(range(1, 5), n)}
    cases |= {tuple(reversed(ms)) for ms in combinations_with_replacement(range(1, 4), 4)}
    cases |= {(5, 3, 2), (7, 4), (5, 4, 3), (2, 2, 1, 1, 1),
              (3, 2, 1, 1, 1), (2, 2, 2, 1, 1), (1,) * 7}
    records = []
    target_count = stage_count = transition_count = 0
    for ms in sorted(cases, key=lambda a: (len(a), a)):
        ps = centers(ms)
        sides = [F(1, m) for m in ms]
        audit = arrangement_cover(ps, sides)
        require(audit['covered'], (ms, audit))
        transition_count += audit['transitions']
        decoder_outputs = []
        for x in targets(ms, ps):
            decoder_outputs.append(constructive_find(ms, x))
            target_count += 1
            stage_count += len(ms)
        _, _, prefixes, tails = parameters(ms)
        # Maximality of the sorted slicing bound, checked without sorting in the recurrence.
        if len(ms) <= 5:
            for order in set(permutations(ms)):
                lower = 1
                for m in reversed(order):
                    lower = m * lower + 1
                require(lower <= len(ps), "another slicing order gives a larger bound")
        if len(set(ms)) == 1:
            require(len(ps) == sum(ms[0] ** i for i in range(len(ms) + 1)),
                    "RSS equal-side control")
        records.append({"denominators": list(ms), "cover_size": len(ps),
                        "projection_gcds": [gcd(p, len(ps)) for p in prefixes[:-1]],
                        "arrangement": audit, "decoder_cases": len(decoder_outputs)})

    # Coordinate relabeling is the only sorting operation in the theorem.
    permutation_cases = 0
    for ms in sorted(set(permutations((3, 2, 1)))):
        ps = centers(ms)
        require(len(ps) == 16, "permutation changed optimal count")
        require(arrangement_cover(ps, [F(1, m) for m in ms])['covered'], "permuted cover")
        for x in targets(ms, ps)[:7]:
            constructive_find(ms, x)
        permutation_cases += 1

    # Removing a center must create a hole; independently exhibit one.
    holes = []
    for ms in [(2,), (3, 2), (3, 2, 1), (2, 2, 2), (1,) * 4]:
        audit = arrangement_cover(centers(ms)[1:], [F(1, m) for m in ms])
        require(not audit['covered'], "N-1 centers unexpectedly cover")
        holes.append({"denominators": list(ms), "hole_after_deleting_zero": audit['hole']})

    # Exact published negative control: RSS Remark 2.8.
    old = [(F(j, 3) % 1, F(j, 7)) for j in range(7)]
    old_hole = (F(5, 6), F(3, 14))
    require(not any(contains(old_hole, v, [F(1, 2)] * 2) for v in old),
            "published bad-cover boundary point was not rejected")

    # Open and closed reciprocal boxes have different counts.
    closed_controls = 0
    for ms in ((2,), (3, 2), (3, 2, 1), (1, 1, 1)):
        tiled = [tuple(F(j, m) for j, m in zip(index, ms))
                 for index in product(*(range(m) for m in ms))]
        require(len(tiled) == prod(ms), "tiling count")
        sides = [F(1, m) for m in ms]
        require(arrangement_cover(tiled, sides, closed=True)['covered'], "closed tiling failed")
        require(not arrangement_cover(tiled, sides)['covered'], "open tiling boundary missed")
        closed_controls += 1

    # An unsorted raw-prefix construction can have fewer than the lower bound.
    bad_ms = (1, 3, 2)
    bad_prefix = [1, 1, 3, 6]
    bad_n = sum(bad_prefix)
    bad = [tuple(F((j * p) % bad_n, bad_n) for p in bad_prefix[:-1]) for j in range(bad_n)]
    bad_audit = arrangement_cover(bad, [F(1, m) for m in bad_ms])
    require(not bad_audit['covered'], "unsorted negative control did not fail")

    rejected = 0
    for ms in ((), (0,), (-1, 2), (F(3, 2), 1), (True, 2)):
        try:
            centers(ms)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("invalid denominator accepted")
    return {"status": "PASS", "arithmetic": "exact Python integers and Fraction",
            "parameter_cases": len(cases), "arrangement_transitions": transition_count,
            "decoder_targets": target_count, "decoder_stages": stage_count,
            "permutation_cases": permutation_cases, "closed_open_controls": closed_controls,
            "deletion_holes": holes, "invalid_inputs_rejected": rejected,
            "old_seven_center_hole": [str(x) for x in old_hole],
            "unsorted_raw_grid_hole": bad_audit['hole'], "cases": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare adjacent EXPECTED.json')
    args = parser.parse_args()
    result = run()
    if args.check:
        expected = json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
        require(result == expected, 'EXPECTED.json mismatch')
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
