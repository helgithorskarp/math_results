#!/usr/bin/env python3
"""Deterministically extract a small exact transversal certificate; no solver."""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / 'hadwiger_nelson_heule517_family_pilot/certificate.json'


def build():
    raw = INPUT.read_bytes()
    cuts = [set(row['D']) for row in json.loads(raw)['rows']]
    forced = set().union(*(d for d in cuts if len(d) == 1))
    added = set(range(510, 517))
    residual = [i for i, d in enumerate(cuts) if not d & (forced | added)]
    universe = sorted(set().union(*(cuts[i] for i in residual)))
    extras = [list(t) for t in combinations(universe, 3)
              if all(set(t) & cuts[i] for i in residual)]
    # Three disjoint residual edges and one disjoint pair for each new point.
    packing = [cuts.index(set(d)) for d in ([360, 393], [417, 445], [438, 457])]
    used = forced | set().union(*(cuts[i] for i in packing))
    for v in sorted(added):
        i = next(i for i, d in enumerate(cuts)
                 if len(d) == 2 and v in d and not d & used)
        packing.append(i)
        used |= cuts[i]
    steps = []
    for v, count in [(510, 11), (511, 11), (512, 11), (515, 11),
                     (516, 11), (513, 6), (514, 6)]:
        rows = [i for i, d in enumerate(cuts) if len(d) == 2 and v in d]
        steps.append({'vertex': v, 'pair_rows': rows[:count]})
    return {'input_sha256': sha256(raw).hexdigest(), 'optimum': 339,
            'added_vertices': sorted(added), 'packing_extra_rows': packing,
            'hub_forcing_steps': steps, 'residual_rows': residual,
            'optimal_extras': extras}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = build()
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'certificate': str(args.out), 'optimum': result['optimum'],
                      'optimal_sets': len(result['optimal_extras'])}))
