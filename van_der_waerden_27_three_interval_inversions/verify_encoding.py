"""Independent literal audit, partitioned by semantic clause families."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import sys
import time


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=Path, required=True)
    parser.add_argument('--part', choices=['starts_and_normalization', 'counter', 'APs'], required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    began = time.monotonic()
    require(not args.output.exists(), 'Existing literal audit')
    meta = json.loads((args.model_dir / 'metadata.json').read_text())
    base = Path(meta['base_word']).read_text().strip()
    n = len(base)
    require(n in [9, 3704] and set(base) <= {'0', '1'} and sha(meta['base_word']) == meta['base_file_sha256'], 'Base domain')
    if n == 3704:
        formula = ''.join('1' if t == 3703 else '0' if t == 3704 or (t - 1) % 617 == 0 else
                          '0' if pow((t - 1) % 617, 308, 617) == 1 else '1' for t in range(1, 3705))
        require(base == formula and sha(meta['base_word']) ==
                '42e6cbef0710d38089475954306b3bd2c0367d5a28aed5ccc74b2698f27fed87', 'Euler near-word including poles')
    else:
        require(base == '010110010', 'Literal nine-bit fixture')
    pool = json.loads(Path(meta['AP_pool']).read_text())
    require(type(pool) is dict and set(pool) == {'length', 'term_count', 'base_bits_sha256', 'APs'}
            and type(pool['length']) is int and pool['length'] == n and type(pool['term_count']) is int
            and pool['term_count'] == 7 and pool['base_bits_sha256'] == hashlib.sha256(base.encode()).hexdigest(), 'Pool scope')
    aps = pool['APs']
    require(type(aps) is list and 1 <= len(aps) <= 2893 and aps == sorted(aps)
            and all(type(ap) is list and len(ap) == 2 and all(type(x) is int for x in ap)
                    and ap[0] > 0 and ap[1] > 0 and ap[0] + 6 * ap[1] <= n for ap in aps)
            and len(set(map(tuple, aps))) == len(aps), 'Actual distinct positive APs')
    require(sha(meta['AP_pool']) == meta['AP_pool_sha256'] and sha(meta['CNF']) == meta['CNF_sha256'], 'Input pins')
    variables = 5 * n - 3
    starts_count, counter_count = 3 * n, 7 * (n - 2) + 4
    total = starts_count + counter_count + 2 * len(aps)
    sections = {'starts_and_normalization': [0, starts_count], 'counter': [starts_count, starts_count + counter_count],
                'APs': [starts_count + counter_count, total]}
    require(meta['variables'] == variables and meta['clauses'] == total and meta['sections'] == sections
            and meta['max_disagreement_runs'] == 3 and meta['first_edit_bit'] == 0, 'Independently counted instance domain')
    def s(i):
        return n + i
    def threshold(i, j):
        require(1 <= i < n and 1 <= j <= 3, 'Threshold domain')
        return 2 * n + 3 * i - 3 + j
    expected = []
    if args.part == 'starts_and_normalization':
        expected = [[-1], [-s(1), 1], [s(1), -1]]
        expected.extend([[-s(i), i] for i in range(2, n + 1)])
        expected.extend([[-s(i), -(i - 1)] for i in range(2, n + 1)])
        expected.extend([[s(i), -i, i - 1] for i in range(2, n + 1)])
    elif args.part == 'counter':
        # Group by semantic implication, independently of the generator's i-major loop.
        expected = [[-threshold(1, j)] for j in [2, 3]]
        expected.extend([[-s(i), threshold(i, 1)] for i in range(1, n)])
        for j in [1, 2, 3]:
            expected.extend([[-threshold(i - 1, j), threshold(i, j)] for i in range(2, n)])
        for j in [2, 3]:
            expected.extend([[-s(i), -threshold(i - 1, j - 1), threshold(i, j)] for i in range(2, n)])
        expected.extend([[-s(i), -threshold(i - 1, 3)] for i in range(2, n + 1)])
        aux = [threshold(i, j) for j in [1, 2, 3] for i in range(1, n)]
        require(len(aux) == len(set(aux)) == 3 * (n - 1) and set(aux) == set(range(2 * n + 1, variables + 1)), 'Exact fresh auxiliary domain')
    else:
        for a, d in aps:
            colors = [int(base[a + k * d - 1]) for k in range(7)]
            ones = [(a + k * d) * (1 if colors[k] == 0 else -1) for k in range(7)]
            expected.extend([ones, [-x for x in ones]])
    lo, hi = sections[args.part]
    lines = Path(meta['CNF']).read_text().splitlines()
    require(lines[0] == f'p cnf {variables} {total}' and len(lines) == total + 1, 'Complete CNF line/header domain')
    actual = []
    for line in lines[lo + 1:hi + 1]:
        row = list(map(int, line.split()))
        require(row and row[-1] == 0 and all(0 < abs(x) <= variables for x in row[:-1]), 'Clause literal domain')
        require(len(set(row[:-1])) == len(row) - 1 and not set(row[:-1]).intersection(-x for x in row[:-1]), 'No repeated/tautological literals')
        actual.append(tuple(sorted(row[:-1])))
    require(len(actual) == len(expected) and Counter(actual) == Counter(tuple(sorted(row)) for row in expected), 'Literal clause-family mismatch')
    cases = total + 2 * len(actual) + sum(map(len, actual)) + 3 * (n - 1) + 7 * len(aps) + 2 * n + 100
    require(cases <= 200000, 'Unchanged literal-audit case cap')
    result = {'agent': 'six-vdw-1', 'role': 'researcher', 'checked_at': datetime.now(timezone.utc).isoformat(),
              'status': 'INDEPENDENT_THREE_RUN_LITERAL_CLAUSE_PART_VERIFIED', 'part': args.part,
              'clause_start': lo, 'clause_stop_exclusive': hi, 'clause_rows_verified': len(actual),
              'CNF_sha256': meta['CNF_sha256'], 'AP_pool_sha256': meta['AP_pool_sha256'], 'length': n,
              'metadata_sha256': sha(args.model_dir / 'metadata.json'), 'checker_sha256': sha(__file__),
              'solver_or_encoder_imported': False, 'interpreter_optimization': sys.flags.optimize,
              'completeness_witness': 'Q(i,j)=1 iff actual starts in1..i number at leastj; at most3 starts makes all overflow clauses true.',
              'conservative_combined_cases': cases, 'seconds': time.monotonic() - began,
              'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'family_exclusion': False, 'new_W_bound': None}
    require(result['seconds'] < 30, 'Unchanged audit30-second cap')
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'part', 'clause_rows_verified', 'conservative_combined_cases', 'seconds']}), flush=True)


if __name__ == '__main__':
    main()
