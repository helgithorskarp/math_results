"""Enumerate prefix ternary paths; publication retains compact witnesses."""
import argparse
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
SOURCE_COMMIT = 'e6f17bb707fbe6c5116221552578acedb6fada01'


def generate(binary):
    cert = json.loads((HERE / 'certificate.json').read_text())
    result = {'schema': 1, 'agent': 'six-sorting-1', 'role': 'researcher',
              'proof_status': 'Witness-certified necessary bounds; no exclusion or 44-gate construction',
              'dependency_source_commit': SOURCE_COMMIT, 'cases': []}
    for case_number in (1, 2):
        case = cert['cases'][case_number]
        gates = cert['prefix'] + case['tournament']
        fixture = '13 24\n' + '\n'.join(f'{a} {b}' for a, b in gates) + '\n'
        done = subprocess.run([str(binary)], input=fixture, text=True,
                              capture_output=True, check=True, timeout=45)
        header, *lines = done.stdout.splitlines()
        assert header.split()[:3] == ['#', 'inputs', '1532883']
        indices = {x: i for i, x in enumerate(case['states'])}
        rows = []
        for line in lines:
            x, y, deleted, witness = map(int, line.split())
            k = y.bit_count() - x.bit_count()
            assert x & ~y == 0 and x in indices and y in indices
            if y == 2047:
                assert deleted == case['maximum_prefix_deletions'][indices[x]]
            cap = 44 - cert['known_lower_bounds'][k] - deleted
            separate = (case['maximum_suffix_touch_limits'][indices[x]] +
                        case['minimum_suffix_touch_limits'][indices[y]])
            rows.append({'high_mask': x, 'nonlow_mask': y, 'middle_wires': k,
                         'prefix_deleted': deleted, 'suffix_union_cap': cap,
                         'separate_sum_cap': separate, 'witness_base3': witness})
        strict = [r for r in rows if r['high_mask'] and r['nonlow_mask'] < 2047
                  and r['middle_wires'] >= 7
                  and r['suffix_union_cap'] < r['separate_sum_cap']]
        strict.sort(key=lambda r: (-(r['separate_sum_cap'] - r['suffix_union_cap']),
                                  -r['middle_wires'], r['suffix_union_cap'],
                                  r['high_mask'], r['nonlow_mask']))
        one_one = [r for r in rows if r['high_mask'].bit_count() == 1
                   and r['nonlow_mask'].bit_count() == 10]
        one_one.sort(key=lambda r: (r['high_mask'], 2047 ^ r['nonlow_mask']))
        assert len(one_one) == 9
        result['cases'].append({'case': case_number,
                                'enumerated_inputs': 1532883,
                                'nested_residual_pairs': len(rows),
                                'strict_middle7_rows': strict,
                                'one_high_one_low_rows': one_one})
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--binary', type=Path, required=True)
    p.add_argument('--check', action='store_true')
    p.add_argument('--out', type=Path, default=HERE / 'mixed_certificate.json')
    args = p.parse_args()
    result = generate(args.binary.resolve())
    if args.check:
        assert json.loads(args.out.read_text()) == result
        print('Mixed prefix generator matches the compact certificate.')
    else:
        args.out.write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
