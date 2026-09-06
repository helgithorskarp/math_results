"""Independent physical edge-list and monochromatic-five-set checker."""
import argparse
import json
from itertools import combinations
from pathlib import Path


def verify(doc):
    def need(ok, message):
        if not ok:
            raise ValueError(message)
    need(isinstance(doc, dict) and set(doc) == {'n', 'edges', 'color', 'witness'}, 'physical schema')
    need(type(doc['n']) is int and doc['n'] == 43, 'physical order')
    raw = doc['edges']
    need(isinstance(raw, list) and all(isinstance(e, list) and len(e) == 2 and all(type(v) is int for v in e) for e in raw), 'edge format')
    edges = [tuple(e) for e in raw]
    need(edges == sorted(set(edges)) and all(0 <= u < v < 43 for u, v in edges), 'canonical edges')
    witness = doc['witness']
    need(isinstance(witness, list) and len(witness) == 5 and all(type(v) is int and 0 <= v < 43 for v in witness), 'witness range')
    need(witness == sorted(set(witness)), 'distinct witness')
    color = doc['color']
    need(type(color) is int and color in (0, 1), 'witness color')
    edges = set(edges)
    need(all(int(e in edges) == color for e in combinations(witness, 2)), 'physical five-set')
    return {'status': 'VERIFIED_PHYSICAL_MONOCHROMATIC_FIVE_SET', 'color': color,
            'witness': witness, 'red_edges': len(edges), 'target_graph': False}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('witness', type=Path)
    args = ap.parse_args()
    print(json.dumps(verify(json.loads(args.witness.read_text())), indent=2, sort_keys=True))
