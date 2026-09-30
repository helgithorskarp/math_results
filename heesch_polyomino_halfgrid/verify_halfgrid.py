"""Finite exact diagnostics and independent doubled-candidate reconstruction."""
import argparse
from dataclasses import replace
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import time

from halfgrid import (collapse, decode_cover, double_cells, half_phase,
                      load_dependencies, vertex_quadrant)


def verify(prior, motion_directory):
    cover, motion = load_dependencies(prior, motion_directory)
    phases = [Fraction(0), Fraction(1, 7), Fraction(1, 4), Fraction(1, 2),
              Fraction(2, 3), Fraction(6, 7)]
    values = [n+f for n in range(-2, 3) for f in phases]
    thresholds = 0
    for x, y, n in product(values, values, range(-2, 3)):
        if x-y >= n:
            assert half_phase(x)-half_phase(y) >= n
        if x-y <= n:
            assert half_phase(x)-half_phase(y) <= n
        assert half_phase(x+n) == half_phase(x)+n
        thresholds += 1

    axes = []
    for a, f, n in product(phases, phases, range(-2, 3)):
        b = n+f
        d, e = abs(a-b), abs(half_phase(a)-half_phase(b))
        axes.append((d>=1, d<=1, e>=1, e<=1))
    pairs = separated = contacts = 0
    for x, y in product(axes, axes):
        pairs += 1
        if x[0] or y[0]:
            separated += 1
            assert x[2] or y[2]
            if x[1] and y[1]:
                contacts += 1
                assert x[3] and y[3]

    quadrant_tests = half_quadrants = 0
    for a, b, v, signs in product(values, values, (-1, 0, 1), product((-1, 1), repeat=2)):
        square, vertex = (a, b), (v, v)
        rounded = (half_phase(a), half_phase(b))
        before = vertex_quadrant(square, vertex, signs)
        assert before == vertex_quadrant(rounded, vertex, signs)
        quadrant_tests += 1
        if before:
            half_quadrants += 1
            for start, center, sign in zip(rounded, vertex, signs):
                low, high = sorted((Fraction(center), center+Fraction(sign, 2)))
                assert start <= low <= high <= start+1

    tile = ((0, 0),)
    star_examples = 0
    for top, bottom in product(phases[1:], repeat=2):
        poses = [motion.Pose(0, tile, Fraction(0), Fraction(0)),
                 motion.Pose(1, tile, Fraction(-1), Fraction(0)),
                 motion.Pose(1, tile, Fraction(1), Fraction(0))]
        for f, y in ((top, 1), (bottom, -1)):
            poses.extend(motion.Pose(1, tile, f+dx, Fraction(y)) for dx in (-1, 0))
        original = motion.check_corona(tile, 1, poses, holes_last=True)
        rounded = collapse(poses)
        after = motion.check_corona(tile, 1, rounded, holes_last=True)
        assert original[-1]['disc'] and after[-1]['disc']
        graph, new_graph = motion.contact_graph(poses), motion.contact_graph(rounded)
        assert all(a <= b for a, b in zip(graph, new_graph))
        pixels, _ = motion.rasterize(tile, rounded)
        assert len(pixels) == 4
        # Independently decode the raw doubled-cell certificate.
        _, pixel_records = motion.rasterize(tile, rounded)
        decoded, stats = decode_cover(tile, [r['cells'] for r in pixel_records], motion)
        assert len(decoded) == 7 and stats[-1]['disc']
        star_examples += 1

    # Outside the theorem's integer-root hypothesis, tying phases can fail.
    f = Fraction(1, 2)
    poses = [motion.Pose(0, tile, Fraction(0), Fraction(0)),
             motion.Pose(1, tile, Fraction(-1), Fraction(0)),
             motion.Pose(1, tile, Fraction(1), Fraction(0))]
    for y in (-1, 1):
        poses.extend(motion.Pose(1, tile, dx+f, Fraction(y)) for dx in (-1, 0))
    shifted = [replace(p, tx=p.tx+Fraction(1, 4)) for p in poses]
    snapped = collapse(shifted)
    recentered = [replace(p, tx=p.tx-snapped[0].tx, ty=p.ty-snapped[0].ty) for p in snapped]
    motion.check_corona(tile, 1, poses, holes_last=True)
    try:
        motion.check_corona(tile, 1, recentered, holes_last=True)
    except ValueError as error:
        assert str(error) == 'incomplete surround'
    else:
        raise AssertionError('noninteger-root scope counterexample missed')

    small_tiles = [((0, 0),), ((0, 0), (1, 0)), ((0, 0), (1, 0), (2, 0)),
        ((0, 0), (1, 0), (0, 1)), tuple((x, 0) for x in range(4)),
        ((0, 0), (1, 0), (0, 1), (1, 1)), ((0, 0), (1, 0), (2, 0), (1, 1)),
        ((0, 0), (0, 1), (0, 2), (1, 0)), ((0, 0), (1, 0), (1, 1), (2, 1))]
    inventory = []
    for tile in small_tiles:
        enlarged = double_cells(tile)
        circuit, candidates, stats = cover.build_cover(enlarged, 1)
        root = set(enlarged)
        # Metric target and translation joins, unlike rectangular generator loops.
        target = {(x, y) for x in range(-1, max(x for x, y in root)+2)
                  for y in range(-1, max(y for x, y in root)+2)
                  if min(max(abs(x-a), abs(y-b)) for a, b in root) <= 1}
        expected = set()
        for shape in motion.variants(tile):
            shape = double_cells(shape)
            translations = {(u-x, v-y) for u, v in target for x, y in shape}
            for x, y in translations:
                cells = tuple(sorted((a+x, b+y) for a, b in shape))
                if not root.intersection(cells):
                    expected.add(cells)
        actual = {tuple(sorted(q['cells'])) for q in candidates}
        assert actual == expected
        assert len(actual) == len(candidates)
        inventory.append({'cells': len(tile), 'candidates': len(candidates),
                          'target_cells': len(target)})

    rejected = 0
    for bad in ([], [(0, 0), (0, 0)], [(0.0, 0)], [(0,)], [(True, 0)]):
        try:
            double_cells(bad)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError('malformed tile accepted')
    return {'agent': 'six-heesch-1', 'role': 'researcher',
            'scope': 'finite diagnostics; universal geometry is the written proof',
            'integer_threshold_cases': thresholds, 'rectangle_pairs': pairs,
            'disjoint_pairs_preserved': separated, 'contacts_preserved': contacts,
            'integer_vertex_quadrant_tests': quadrant_tests,
            'closed_half_quadrants_checked': half_quadrants,
            'rational_first_coronas_checked_before_and_after': star_examples,
            'doubled_certificates_independently_decoded': star_examples,
            'noninteger_root_counterexample': 'collapse loses complete surround',
            'independent_candidate_inventories': inventory,
            'invalid_inputs_rejected': rejected}


def main():
    p = argparse.ArgumentParser()
    base = Path(__file__).resolve().parent.parent
    p.add_argument('--prior-dir', type=Path, default=base/'heesch_polyomino_euler_cnf')
    p.add_argument('--motion-dir', type=Path, default=base/'heesch_polyomino_motion_bridge')
    p.add_argument('--expected', type=Path, default=Path(__file__).parent/'expected.json')
    p.add_argument('--write-expected', action='store_true')
    args = p.parse_args()
    start = time.monotonic()
    result = verify(args.prior_dir, args.motion_dir)
    encoded = json.dumps(result, sort_keys=True, indent=2)+'\n'
    if args.write_expected:
        args.expected.write_text(encoded)
    else:
        assert result == json.loads(args.expected.read_text()), 'expected output mismatch'
    print(encoded, end='')
    print(json.dumps({'seconds': round(time.monotonic()-start, 3)}))


if __name__ == '__main__':
    main()
