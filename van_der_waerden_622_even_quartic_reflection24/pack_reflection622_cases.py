"""Greedy reflection-paired quartic packing proposals; no exclusions.

At most two specified cases per child. Each scans at most311*310 AP
choices. Used supports are unions with their field negatives. A failed
greedy packing is not a bound on the maximum packing size.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import time


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def coefficients_at(index):
    require(type(index) is int and 0 <= index < 625, 'case index')
    if index < 3:
        return [(0, 1, 11)[index], 0, 0, 0, 1]
    if index < 314:
        return [index - 3, 0, 1, 0, 1]
    return [index - 314, 0, 11, 0, 1]


def propose(index, squares):
    coefficients = coefficients_at(index)
    B, A = coefficients[0], coefficients[2]
    values = []
    for x in range(311):
        square = x * x % 311
        q = (square * square + A * square + B) % 311
        values.append(None if q == 0 else int(q in squares))
    require(all(values[x] == values[-x % 311] for x in range(311)), 'even polynomial character')
    used, pairs, choices = set(), [], 0
    for a in range(311):
        for d in range(1, 311):
            choices += 1
            residues = [(a + j * d) % 311 for j in range(7)]
            if any(x == 0 or x in used or values[x] is None for x in residues):
                continue
            support = set(residues)
            negative = {-x % 311 for x in residues}
            if support.intersection(negative) or negative.intersection(used):
                continue
            colors = [((a + j * d) % 2) ^ values[x] for j, x in enumerate(residues)]
            if len(set(colors)) != 1:
                continue
            reflected_start = (-(a + 6 * d) % 622) % 311
            pairs.append([[a + 1, d], [reflected_start + 1, d]])
            used.update(support)
            used.update(negative)
            if len(pairs) == 12:
                break
        if len(pairs) == 12:
            break
    return {'index': index, 'coefficients': coefficients, 'pairs': pairs,
            'pairs_found': len(pairs), 'AP_choices': choices}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--indexes', type=int, nargs='+', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(1 <= len(args.indexes) <= 2 and len(set(args.indexes)) == len(args.indexes), 'at most two distinct cases')
    require(all(0 <= x < 625 for x in args.indexes), 'case range')
    require(not args.output.exists(), 'output already exists')
    began = time.monotonic()
    squares = {x * x % 311 for x in range(1, 311)}
    cases = [propose(index, squares) for index in args.indexes]
    choices = sum(case['AP_choices'] for case in cases)
    # Units are complete AP-choice evaluations, field evaluations/identities,
    # and all168 actual term slots in the accepted paired packing per case.
    conservative_cases = choices + 311 + len(cases) * (2 * 311 + 168)
    require(conservative_cases <= 194711 < 200000, 'unchanged case cap')
    result = {'agent': 'six-vdw-1', 'role': 'researcher',
              'checked_at': datetime.now(timezone.utc).isoformat(),
              'status': 'REFLECTION_PAIR_PROPOSALS_PENDING_INDEPENDENT_CHECK',
              'indexes': args.indexes, 'cases': cases, 'AP_choices': choices,
              'conservative_combined_cases': conservative_cases,
              'seconds': time.monotonic() - began,
              'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'threads': 1, 'mathematical_exclusion': False, 'packing_optimality_claim': False}
    require(result['seconds'] < 30, 'unchanged30s child time cap')
    args.output.write_text(json.dumps(result, separators=(',', ':')) + '\n')
    print(json.dumps({'indexes': args.indexes, 'pairs_found': [c['pairs_found'] for c in cases],
                      'AP_choices': choices, 'seconds': result['seconds']}), flush=True)


if __name__ == '__main__':
    main()
