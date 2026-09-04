#!/usr/bin/env python3
"""Exact Python geometry checks, separate from the C++ implementation.

Sample the first and last placement per orientation and a largest overlap.
This sample audit supplements, rather than replaces, the full C++ check.
"""

import argparse
import json
from pathlib import Path

import enumerate_lowden as field

HERE = Path(__file__).resolve().parent


def edges(points, scale):
    out = []
    for i, (x, y) in enumerate(points):
        for j in range(i):
            dx = field.add(x, field.neg(points[j][0]))
            dy = field.add(y, field.neg(points[j][1]))
            if field.add(field.mul(dx, dx), field.mul(dy, dy)) == (scale*scale,)+(0,)*7:
                out.append((j, i))
    return out


def rows(path, prefix):
    return [dict(x.split('=', 1) for x in line.split(';'))
            for line in path.read_text().splitlines() if line.startswith(prefix)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('transforms', type=Path)
    parser.add_argument('colorings', type=Path)
    args = parser.parse_args()
    left = field.points(HERE / 'points159.tsv')
    right = field.points(HERE / 'points214.tsv')
    assert len(edges(left, 12)) == 646
    assert len(edges(right, 12)) == 977
    transforms = rows(args.transforms, 'placement=')
    colors = rows(args.colorings, 'graph=')
    assert len(transforms) == len(colors) == 39004
    by_orientation = {}
    for i, row in enumerate(transforms):
        key = tuple(row[x] for x in ('reflected', 'denominator', 'c', 's'))
        by_orientation.setdefault(key, []).append(i)
    selected = {i for ids in by_orientation.values() for i in (ids[0], ids[-1])}
    selected.add(max(range(len(transforms)), key=lambda i: int(transforms[i]['placement'])))
    checked = 0
    for i in sorted(selected):
        row, witness = transforms[i], colors[i]
        assert int(witness['graph']) == i
        c, s, tx, ty = (tuple(map(int, row[k].split(','))) for k in ('c', 's', 'tx', 'ty'))
        d = int(row['denominator'])
        labelled = [(field.scale(x, d), field.scale(y, d)) for x, y in left]
        labelled += [(field.add(x, tx), field.add(y, ty))
                     for x, y in (field.image(p, int(row['reflected']), c, s) for p in right)]
        points = list(dict.fromkeys(labelled))
        ee = edges(points, 12*d)
        assert len(points) == int(witness['order']) == len(witness['colors'])
        assert len(ee) == int(witness['edges'])
        assert all(color in '0123' for color in witness['colors'])
        assert all(witness['colors'][u] != witness['colors'][v] for u, v in ee)
        checked += len(ee)
    print(json.dumps({'left_internal_edges': 646, 'right_internal_edges': 977,
                      'orientations_sampled': len(by_orientation), 'graphs_sampled': len(selected),
                      'sample_indices': sorted(selected), 'checked_edges': checked,
                      'exact_python_geometry': True}, indent=2))


if __name__ == '__main__':
    main()
