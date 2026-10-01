"""Propose root-free, field-disjoint APs for affine-even quartic seeds.

Greedy discovery only. A failed packing is not a nonexistence assertion.
Each child covers at most two specified cases and at most193722 cases.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import time


def case_at(index):
    if index < 3:
        return 'pure_quartic', 0, (0, 1, 11)[index]
    index -= 3
    return 'biquartic', (1, 11)[index // 311], index % 311


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, required=True)
    parser.add_argument('--count', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert 0 <= args.start < 625 and 1 <= args.count <= 2
    assert args.start + args.count <= 625 and not args.output.exists()
    began = time.monotonic()
    squares = {x * x % 311 for x in range(1, 311)}
    cases, total_choices = [], 0
    for index in range(args.start, args.start + args.count):
        kind, quadratic, constant = case_at(index)
        values = []
        for x in range(311):
            square = x * x % 311
            value = (square * square + quadratic * square + constant) % 311
            values.append(None if value == 0 else int(value in squares))
        used, packing, choices = set(), [], 0
        for a in range(311):
            for d in range(1, 311):
                choices += 1
                residues = [(a + j * d) % 311 for j in range(7)]
                if any(x in used or values[x] is None for x in residues):
                    continue
                colors = [((a + j * d) % 2) ^ values[x] for j, x in enumerate(residues)]
                if len(set(colors)) != 1:
                    continue
                packing.append([a + 1, d])
                used.update(residues)
                if len(packing) == 20:
                    break
            if len(packing) == 20:
                break
        total_choices += choices
        cases.append({'index': index, 'kind': kind, 'quadratic': quadratic, 'constant': constant,
                      'coefficients': [constant, 0, quadratic, 0, 1], 'APs': packing,
                      'packing_size': len(packing), 'AP_choices': choices})
    conservative_cases = total_choices + 311 * args.count + 140 * args.count
    assert conservative_cases <= 193722 < 200000
    result = {'agent': 'six-vdw-1', 'role': 'researcher',
              'checked_at': datetime.now(timezone.utc).isoformat(),
              'status': 'GREEDY_ROOT_FREE_PACKINGS_PENDING_INDEPENDENT_CHECK',
              'start': args.start, 'count': args.count, 'cases': cases,
              'AP_choices': total_choices, 'conservative_combined_cases': conservative_cases,
              'seconds': time.monotonic() - began,
              'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'threads': 1, 'mathematical_exclusion': False, 'packing_optimality_claim': False}
    assert result['seconds'] < 30
    args.output.write_text(json.dumps(result, separators=(',', ':')) + '\n')
    print(json.dumps({'start': args.start, 'count': args.count,
                      'sizes': [c['packing_size'] for c in cases], 'AP_choices': total_choices,
                      'seconds': result['seconds']}), flush=True)


if __name__ == '__main__':
    main()
