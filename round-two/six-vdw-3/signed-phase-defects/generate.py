#!/usr/bin/env python3
"""Exact cut-and-puncture model for one exceptional period-6q phase column.

The base cut generator is the previously published pair-parity ladder source.
Its bytes are checked before importing it. Solver output is not a proof.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASE_HASH = '21bba5e30eae728ded9cc45a6a75c5522c644fd411980bc5c9310e96b19e637f'


def model(q=103, base_source=None):
    source = Path(base_source) if base_source else ROOT.parent / 'parity-ladders' / 'generate.py'
    if hashlib.sha256(source.read_bytes()).hexdigest() != BASE_HASH:
        raise ValueError('Published cut-generator dependency differs')
    spec = importlib.util.spec_from_file_location('published_cut_generator', source)
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)
    text, metadata = base.model(q)
    if q < 11:
        raise ValueError('This model interface requires a prime q>=11')
    clauses = {tuple(map(int, line.split()[:-1])) for line in text.splitlines()[1:]}
    old_count = len(clauses)
    forbidden = {sum(((b + j*s) % 6 >= 3) << j for j in range(7))
                 for b in range(6) for s in range(6)}
    exceptional_supports = 0
    for r in range(1, (q+1)//2):
        for a in range(q):
            points = [(a + j*r) % q for j in range(7)]
            if 0 not in points:
                continue
            exceptional_supports += 1
            k = points.index(0)
            patterns = {sum(((b + j*s - int(j == k)) % 6 >= 3) << j
                            for j in range(7))
                        for b in range(6) for s in range(6)}
            if not forbidden <= patterns:
                raise ValueError('Single-defect dominance failed')
            punctures = {word & ~(1 << k) for word in forbidden
                         if word ^ (1 << k) in patterns}
            if len(patterns) != 28 or len(punctures) != 12:
                raise ValueError('Single-defect local count failed')
            # With u(0)=0, edge {0,x} has label x and equals u(x).
            # Each such puncture forbids both values at the deleted site.
            for word in punctures:
                clause = tuple(sorted(((-x if (word >> j) & 1 else x)
                                       for j, x in enumerate(points) if x), key=abs))
                clauses.add(clause)
    ordered = sorted(clauses)
    raw = 'p cnf {} {}\n'.format(metadata['variables'], len(ordered))
    raw += ''.join(' '.join(map(str, row)) + ' 0\n' for row in ordered)
    metadata.update({
        'exceptional_column': 0,
        'exceptional_phase_offset': 1,
        'exceptional_supports': exceptional_supports,
        'puncture_cnf_clauses': len(ordered) - old_count,
        'clauses': len(ordered),
        'sha256': hashlib.sha256(raw.encode('ascii')).hexdigest(),
    })
    return raw, metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--q', type=int, default=103)
    parser.add_argument('--base-source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    text, metadata = model(args.q, args.base_source)
    args.output.write_text(text, encoding='ascii')
    print(json.dumps(metadata, sort_keys=True))


if __name__ == '__main__':
    main()
