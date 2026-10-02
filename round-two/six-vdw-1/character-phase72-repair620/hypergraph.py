"""Untrusted normalized producer for F31 character x phase20 bad supports."""
import argparse
import hashlib
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def build(mask):
    require(type(mask) is int and 0 <= mask < 1024, 'absolute ten-bit input')
    character = [None] + [int(pow(r, 15, 31) != 1) for r in range(1, 31)]
    phase = [((mask >> (s % 10)) & 1) ^ (s // 10) for s in range(20)]
    phase_bad = sum(len({phase[(s + j * h) % 20] for j in range(7)}) == 1
                    for s in range(20) for h in range(1, 20))
    require(phase_bad == 0, 'only a legal phase profile is this producer target')
    patterns = []
    for a in range(1, 25):
        for s in range(20):
            for h in range(20):
                colors = [character[a + j] ^ phase[(s + j * h) % 20] for j in range(7)]
                if len(set(colors)) == 1:
                    patterns.append([a, s, h, colors[0]])
    starts = sorted({p[0] for p in patterns})
    edges = sorted({tuple(sorted((mu * (a + j)) % 31 for j in range(7)))
                    for mu in range(1, 31) for a in starts})
    degrees = [sum(r in edge for edge in edges) for r in range(1, 31)]
    require(edges and all(len(e) == 7 and 0 not in e for e in edges), 'nonempty seven-regular edges')
    require(len(set(degrees)) == 1 and degrees[0] > 0, 'positive scalar-transitive degree')
    return {'schema': 'F31_CHARACTER_PHASE20_BAD_SUPPORTS_V1', 'author': 'six-vdw-1',
            'role': 'researcher', 'q': 31, 'period': 620, 'phase_period': 20,
            'mask': mask, 'character_word': character, 'phase_word': phase,
            'tested_normalized_patterns': 9600, 'tested_constant_field_patterns': 380,
            'constant_field_bad_patterns': phase_bad,
            'monochromatic_primitive_patterns': patterns, 'normalized_field_starts': starts,
            'edges': [list(e) for e in edges], 'edge_degrees': degrees,
            'edge_sha256': digest([list(e) for e in edges]),
            'primitive_sha256': digest(patterns),
            'scope': 'Complete bad-support proposal for one legal profile; no integer minimum or coloring.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mask', type=int, default=72)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), 'preserve existing mathematical proposal')
    record = build(args.mask)
    args.out.write_text(json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps({'author': 'six-vdw-1', 'role': 'researcher',
                      'status': 'UNTRUSTED_COMPLETE_NORMALIZED_HYPERGRAPH_PROPOSAL',
                      'mask': args.mask, 'normalized_field_starts': record['normalized_field_starts'],
                      'primitive_bad_patterns': len(record['monochromatic_primitive_patterns']),
                      'distinct_edges': len(record['edges']), 'degree': record['edge_degrees'][0],
                      'edge_sha256': record['edge_sha256'],
                      'primitive_sha256': record['primitive_sha256']}, sort_keys=True))
