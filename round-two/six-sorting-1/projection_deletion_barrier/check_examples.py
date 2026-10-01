#!/usr/bin/env python3
"""Replay invalid construction examples and the published prefix-filter interface."""
import argparse
import collections
import importlib.util
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', type=Path, default=ROOT.parents[2] / 'round-two' / 'six-sorting-2' / 'semantic-pruning' / 'profile.py')
    args = parser.parse_args()
    doc = json.loads((ROOT / 'construction-examples.json').read_text())
    if hashlib.sha256(args.profile.read_bytes()).hexdigest() != doc['filter_source_sha256']:
        raise RuntimeError('published filter source hash mismatch')
    spec = importlib.util.spec_from_file_location('published_prefix_profile', args.profile)
    if spec is None or spec.loader is None:
        raise RuntimeError('published profile.py is unavailable')
    profile = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(profile)
    for example in doc['examples']:
        n, gates = example['n'], example['gates']
        if n != 13 or len(gates) != 44 or any(not 0 <= a < b < n for a, b in gates):
            raise RuntimeError('invalid candidate')
        failures, wrong = [], 0
        weights = collections.Counter()
        for mask in range(1 << n):
            v = [(mask >> i) & 1 for i in range(n)]
            target = sorted(v)
            for a, b in gates:
                if v[a] > v[b]:
                    v[a], v[b] = v[b], v[a]
            if any(v[i] > v[i + 1] for i in range(n - 1)):
                failures.append(mask)
                weights[str(sum(v))] += 1
            wrong += sum(x != y for x, y in zip(v, target))
        actual = dict(failed_inputs=len(failures), wrong_output_bits=wrong,
                      failures=failures, failed_weights=dict(weights))
        if actual != example['expected_boolean']:
            raise RuntimeError('Boolean replay mismatch')
        data = profile.analyze(n, gates)
        rejected = None
        for cut in range(len(gates) + 1):
            for name, l, h in profile.FAMILIES:
                mass = data[name]['trace'][cut]['semantic_mass']
                lower = profile.SIZES[n - l - h] + (mass - 1).bit_length()
                if lower > 44 and rejected is None:
                    rejected = dict(cut=cut, family=name, mass=mass, lower_bound=lower)
        if rejected != example['expected_first_rejection']:
            raise RuntimeError('prefix-filter replay mismatch')
        print(example['name'], 'NOT_A_SORTER', 'failed_inputs', len(failures),
              'first_rejection', json.dumps(rejected, sort_keys=True))
    print('CONSTRUCTION_HANDOFF_EXAMPLES_REPLAYED')


if __name__ == '__main__':
    main()
