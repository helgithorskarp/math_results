"""Literal audit of the actual CNF against an independently specified prefix counter."""
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


def expected_formula(base, aps):
    n, top = len(base), 2 * len(base)

    def s(i):
        return n + i

    def A(i):
        require(1 <= i <= n - 2, 'One-start prefix range')
        return top + i if i <= 2 else top + 2 * i - 1

    def B(i):
        require(2 <= i <= n - 1, 'Two-start prefix range')
        return top + 3 if i == 2 else top + 2 * i - 2

    # Different derivation: clauses grouped by their semantic implication,
    # rather than by the construction's sequential-counter loop.
    expected = [[-s(1), 1], [s(1), -1]]
    for i in range(2, n + 1):
        expected.extend([[-s(i), i], [-s(i), -(i - 1)], [s(i), -i, i - 1]])
    expected.extend([[-s(i), A(i)] for i in range(1, n - 1)])
    expected.extend([[-A(i), A(i + 1)] for i in range(1, n - 2)])
    expected.extend([[-s(i), -A(i - 1), B(i)] for i in range(2, n)])
    expected.extend([[-B(i), B(i + 1)] for i in range(2, n - 1)])
    expected.extend([[-s(i), -B(i - 1)] for i in range(3, n + 1)])
    # Derive the two forbidden color clauses directly, term by term.
    for a, d in aps:
        not_all_zero, not_all_one = [], []
        for k in range(7):
            p = a + k * d
            not_all_zero.append(p if base[p - 1] == '0' else -p)
            not_all_one.append(-p if base[p - 1] == '0' else p)
        expected.extend([not_all_zero, not_all_one])
    aux = [A(i) for i in range(1, n - 1)] + [B(i) for i in range(2, n)]
    require(set(aux) == set(range(2 * n + 1, 4 * n - 3)) and len(aux) == 2 * n - 4, 'Fresh exact auxiliary identifiers')
    return 4 * n - 4, expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    began = time.monotonic()
    require(not args.output.exists(), 'Existing encoding audit')
    meta = json.loads((args.model_dir / 'metadata.json').read_text())
    base = Path(meta['base_word']).read_text().strip()
    require(len(base) == 3704 and set(base) <= {'0', '1'}
            and sha(meta['base_word']) == '42e6cbef0710d38089475954306b3bd2c0367d5a28aed5ccc74b2698f27fed87', 'Literal near-word')
    # A separate Euler criterion checks the explained base formula, including poles.
    formula = ''.join('1' if t == 3703 else '0' if t == 3704 or (t - 1) % 617 == 0 else
                      '0' if pow((t - 1) % 617, 308, 617) == 1 else '1' for t in range(1, 3705))
    require(base == formula, 'Near-word formula differs')
    pool = json.loads(Path(meta['AP_pool']).read_text())
    require(type(pool) is dict and set(pool) == {'length', 'term_count', 'base_bits_sha256', 'APs'}
            and type(pool['length']) is int and pool['length'] == 3704
            and type(pool['term_count']) is int and pool['term_count'] == 7
            and pool['base_bits_sha256'] == hashlib.sha256(base.encode()).hexdigest(), 'Pool scope')
    aps = pool['APs']
    require(type(aps) is list and 1 <= len(aps) <= 1955, 'AP pool bound')
    require(all(type(ap) is list and len(ap) == 2 and all(type(x) is int for x in ap)
                and ap[0] > 0 and ap[1] > 0 and ap[0] + 6 * ap[1] <= 3704 for ap in aps), 'Positive actual APs')
    require(aps == sorted(aps) and len(set(map(tuple, aps))) == len(aps), 'Canonical unique actual APs')
    require(sha(meta['AP_pool']) == meta['AP_pool_sha256'] and sha(meta['CNF']) == meta['CNF_sha256'], 'Fixed encoding inputs')
    variables, expected = expected_formula(base, aps)
    lines = Path(meta['CNF']).read_text().splitlines()
    require(lines[0] == f'p cnf {variables} {len(expected)}', 'Exact independently derived header')
    actual = []
    for line in lines[1:]:
        row = list(map(int, line.split()))
        require(row[-1] == 0 and all(0 < abs(x) <= variables for x in row[:-1]), 'Integer CNF clause')
        require(len(set(row[:-1])) == len(row) - 1 and not set(row[:-1]).intersection(-x for x in row[:-1]), 'No repeated/tautological clause literals')
        actual.append(tuple(sorted(row[:-1])))
    require(len(actual) == len(expected) and Counter(actual) == Counter(tuple(sorted(row)) for row in expected),
            'Literal clause multiset differs from actual starts, prefix counter or actual APs')
    cases = 2 * len(actual) + sum(len(row) for row in actual) + 2 * variables + 7 * len(aps) + len(base) + 100
    require(cases <= 200000, 'Unchanged200000-case literal-audit cap')
    result = {'agent': 'six-vdw-1', 'role': 'researcher', 'checked_at': datetime.now(timezone.utc).isoformat(),
              'status': 'LITERAL_CNF_MATCHES_ACTUAL_RUN_STARTS_PREFIX_ATMOST_TWO_AND_POSITIVE_AP_CONSTRAINTS',
              'length': 3704, 'APs': len(aps), 'variables': variables, 'clauses': len(actual),
              'clause_multiset_match': True, 'exact_fresh_auxiliary_ids': True, 'base_formula_verified': True,
              'written_completeness_witness': 'A_i=1 iff prefix starts1..i has >=1; B_i=1 iff it has >=2.',
              'no_symmetry_balance_or_pole_constraint': True,
              'base_file_sha256': sha(meta['base_word']), 'AP_pool_sha256': sha(meta['AP_pool']),
              'CNF_sha256': sha(meta['CNF']), 'checker_sha256': sha(__file__),
              'solver_or_encoder_imported': False, 'interpreter_optimization': sys.flags.optimize,
              'conservative_combined_cases': cases, 'seconds': time.monotonic() - began,
              'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, 'threads': 1,
              'proof_still_requires_unsatisfiability_certificate': True, 'new_W_bound': None}
    require(result['seconds'] < 30, 'Unchanged30-second audit limit')
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'APs', 'conservative_combined_cases', 'seconds']}), flush=True)


if __name__ == '__main__':
    main()
