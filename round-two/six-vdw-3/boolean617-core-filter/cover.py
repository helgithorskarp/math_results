#!/usr/bin/env python3
"""Affine field geometry cover; this is not a full-interval quotient."""
import argparse
import itertools
import json
from pathlib import Path


def cover():
    p = 617
    rows = []
    representatives = set()
    for t in range(2, p):
        roots = (0, 1, t)
        maps = []
        for order in itertools.permutations(range(3)):
            delta = (roots[order[1]] - roots[order[0]]) % p
            inverse = pow(delta, -1, p)
            u = (roots[order[2]] - roots[order[0]]) * inverse % p
            maps.append((u, list(order), roots[order[0]], delta))
        u, order, shift, scale = min(maps)
        representatives.add(u)
        rows.append({'t': t, 'representative': u, 'root_order': order,
                     'inverse_map_shift': shift, 'inverse_map_scale': scale})
    return {'schema': 'boolean617-field-geometry-cover-v1', 'prime': p,
            'roots': '0,1,t', 'geometries': sorted(representatives), 'maps': rows,
            'meaning': 'Necessary regular field-core reduction only; not a quotient of [1,3704].'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = cover()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'raw_geometries': len(result['maps']), 'representatives': len(result['geometries'])}))


if __name__ == '__main__':
    main()
