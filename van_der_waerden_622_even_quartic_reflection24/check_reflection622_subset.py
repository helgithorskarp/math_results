"""Separate definition-level checker for an explicitly requested subset only.

No solver, hypergraph, proposer or shared numerical verifier is imported.
The requested index list is part of the quantified result, not all625 cases.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import sys
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--indexes', type=int, nargs='+', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists() and len(args.indexes) <= 12, 'Fresh bounded subset')
    require(args.indexes == sorted(set(args.indexes)) and all(0 <= x < 625 for x in args.indexes), 'Requested index domain')
    began = time.monotonic()
    raw = args.certificate.read_bytes()
    data = json.loads(raw)
    require(type(data) is dict and set(data) == {'modulus', 'pairs_per_case', 'cases'}, 'Certificate schema')
    require(type(data['modulus']) is int and data['modulus'] == 311 and
            type(data['pairs_per_case']) is int and data['pairs_per_case'] == 12, 'Exact modulus/target')
    require(type(data['cases']) is list and len(data['cases']) == len(args.indexes), 'Requested subset coverage')
    count = 0
    for index, case in zip(args.indexes, data['cases']):
        require(type(case) is dict and set(case) == {'index', 'coefficients', 'pairs'}, 'Case schema')
        require(type(case['index']) is int and case['index'] == index, 'Requested index')
        if index < 3:
            expected = [(0, 1, 11)[index], 0, 0, 0, 1]
        elif index < 314:
            expected = [index - 3, 0, 1, 0, 1]
        else:
            expected = [index - 314, 0, 11, 0, 1]
        coefficients = case['coefficients']
        require(type(coefficients) is list and len(coefficients) == 5 and all(type(x) is int for x in coefficients), 'Coefficients')
        require(coefficients == expected, 'Canonical coefficient identity')
        require(type(case['pairs']) is list and len(case['pairs']) == 12, 'Twelve pairs')
        used = set()
        for pair in case['pairs']:
            require(type(pair) is list and len(pair) == 2, 'Two actual AP members')
            supports, steps = [], []
            for ap in pair:
                require(type(ap) is list and len(ap) == 2 and all(type(x) is int for x in ap), 'Integer AP pair')
                a, d = ap
                require(1 <= a <= 311 and 1 <= d <= 310 and a + 6 * d <= 2171, 'Actual AP geometry')
                support, colors = set(), []
                for j in range(7):
                    t = a - 1 + j * d
                    x = t % 311
                    q = 0
                    for coefficient in reversed(coefficients):
                        q = (q * x + coefficient) % 311
                    require(q != 0, 'Root term')
                    chi = pow(q, 155, 311)
                    require(chi in [1, 310], 'Euler character')
                    colors.append((t % 2) ^ int(chi == 1))
                    support.add(x)
                    count += 1
                require(len(support) == 7 and len(set(colors)) == 1, 'Actual AP is bichromatic/degenerate')
                require(not support.intersection(used), 'Field support overlap')
                used.update(support)
                supports.append(support)
                steps.append(d)
            require(steps[0] == steps[1] and supports[1] == {(-x) % 311 for x in supports[0]}, 'Reflection relation')
        require(len(used) == 168, 'Field support coverage')
    result = {'agent': 'six-vdw-1', 'role': 'researcher',
              'checked_at': datetime.now(timezone.utc).isoformat(),
              'status': 'EXPLICIT_REQUESTED_SUBSET24_AP_PACKINGS_VERIFIED',
              'indexes': args.indexes, 'cases': len(args.indexes), 'APs_checked': 24 * len(args.indexes),
              'actual_term_colors_checked': count, 'field_residues_per_case': 168,
              'all625_claim': False, 'new_W_bound': None, 'mathematical_nonexistence_claim': False,
              'certificate_sha256': hashlib.sha256(raw).hexdigest(),
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'interpreter_optimization': sys.flags.optimize, 'seconds': time.monotonic() - began,
              'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'conservative_combined_cases': 20 * count + 500,
              'threads': 1, 'external_independent_review': False}
    require(result['conservative_combined_cases'] <= 200000 and result['seconds'] < 30, 'Unchanged child guards')
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
