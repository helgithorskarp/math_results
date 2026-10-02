#!/usr/bin/env python3
"""Standalone integer reader for a five-corona construction, not an upper."""
from collections import Counter
import json
from pathlib import Path
import geometry as g

HERE = Path(__file__).resolve().parent


def direction_step(dx, dy):
    """Angle of physical (dx,sqrt(3)*dy), in multiples of thirty degrees."""
    g.require(dx or dy, 'zero boundary edge')
    if dy == 0:
        return 0 if dx > 0 else 6
    if dx == 0:
        return 3 if dy > 0 else 9
    if dx == 3 * dy:
        return 1 if dx > 0 else 7
    if dx == dy:
        return 2 if dx > 0 else 8
    if dx == -dy:
        return 4 if dy > 0 else 10
    if dx == -3 * dy:
        return 5 if dy > 0 else 11
    raise ValueError('prototype edge is outside thirty-degree directions')


def angle_hypothesis(m):
    cycle, unused = g.boundary(g.atoms(m))
    steps = [direction_step(cycle[(i+1) % len(cycle)][0] - p[0],
                            cycle[(i+1) % len(cycle)][1] - p[1])
             for i, p in enumerate(cycle)]
    interiors = []
    for i, outgoing in enumerate(steps):
        exterior = (outgoing - steps[i-1] + 6) % 12 - 6
        g.require(exterior != -6, 'folded boundary')
        interiors.append(6 - exterior)
    return {'directed_edge_steps': dict(sorted(Counter(steps).items())),
            'interior_angle_steps': dict(sorted(Counter(interiors).items())),
            'q6_hypothesis_verified': True}


def main():
    data = json.loads((HERE / 'certificate.json').read_text())
    checked = g.check(data)
    fields = ('tile_hexagons', 'verified_coronas', 'copies', 'level_counts',
              'prefixes', 'closed_contact_pairs', 'atom_pair_tests')
    actual = {name: checked[name] for name in fields}
    actual['angle_hypothesis'] = angle_hypothesis(data['tile_hexagons'])
    actual = json.loads(json.dumps(actual))
    expected = json.loads((HERE / 'expected.json').read_text())
    g.require(actual == expected, 'exact evidence differs from expected certificate')
    print(json.dumps({'verified_coronas': checked['verified_coronas'],
                      'copies': checked['copies'], 'level_counts': checked['level_counts'],
                      'q6_hypothesis_verified': True, 'finite_upper_claimed': False,
                      'elapsed_seconds': checked['elapsed_seconds'],
                      'peak_rss_kib': checked['peak_rss_kib']}, indent=2))


if __name__ == '__main__':
    main()
