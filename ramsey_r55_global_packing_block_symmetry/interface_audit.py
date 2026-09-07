#!/usr/bin/env python3
"""Audit identical-atom block normalization across all 60 h3835 branches."""
from collections import OrderedDict
from math import factorial, prod
from pathlib import Path
import argparse
import hashlib
import json
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from block_symmetry import added_clauses

LAST = ('B3', 'E3', 'P3', 'R3')
SIZES = {'R4': 4, 'B4': 4, 'R3': 3, 'B3': 3, 'E3': 3, 'P3': 3}


def expected_types(branch):
    r, s, t = branch
    return ['R4'] * r + ['B4'] * (7 - r) + ['R3'] * s + ['B3'] * (4 - s) + [LAST[t]]


def run(target):
    target = Path(target); sys.path.insert(0, str(target))
    import model
    records = []
    for r in (5, 6, 7):
        for s in range(5):
            for t in range(4):
                branch = [r, s, t]; packing = model.Packing(branch)
                types = expected_types(branch)
                if packing.types != types or packing.types[0] != 'R4':
                    raise ValueError('branch type reconstruction')
                groups = OrderedDict()
                for index, kind in enumerate(types[1:], 1):
                    groups.setdefault(kind, []).append(index)
                group_rows = []
                expected_aux = expected_clauses = expected_comparisons = 0
                action_factors = []
                for kind, indices in groups.items():
                    if len(indices) < 2:
                        continue
                    length = 4 * SIZES[kind]; comparisons = len(indices) - 1
                    expected_comparisons += comparisons
                    expected_aux += comparisons * (length - 1)
                    expected_clauses += comparisons * (6 * length - 5)
                    action_factors.append(factorial(len(indices)))
                    group_rows.append({'kind': kind, 'blocks': indices,
                                       'key_bits': length,
                                       'action_factor': factorial(len(indices))})
                clauses, maximum, comparison_rows = added_clauses(packing)
                if maximum != 847 + expected_aux or len(clauses) != expected_clauses:
                    raise ValueError('added formula dimensions')
                if len(comparison_rows) != expected_comparisons:
                    raise ValueError('comparison census')
                if any(abs(x) > maximum or x == 0 for clause in clauses for x in clause):
                    raise ValueError('literal range')
                records.append({'branch': branch, 'groups': group_rows,
                                'block_action_order': prod(action_factors),
                                'block_comparisons': expected_comparisons,
                                'auxiliary_prefix_variables': expected_aux,
                                'symmetry_clauses': expected_clauses,
                                'normalized_variables': maximum})
    payload = json.dumps(records, sort_keys=True, separators=(',', ':')).encode()
    return {'status': 'VERIFIED_ALL_60_IDENTICAL_BLOCK_NORMALIZATIONS',
            'branches': len(records),
            'r7_s4_t3': next(row for row in records if row['branch'] == [7, 4, 3]),
            'records_sha256': hashlib.sha256(payload).hexdigest(),
            'records': records}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--target', required=True); parser.add_argument('--output')
    args = parser.parse_args(); result = run(args.target)
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output: Path(args.output).write_text(text)
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, sort_keys=True))
