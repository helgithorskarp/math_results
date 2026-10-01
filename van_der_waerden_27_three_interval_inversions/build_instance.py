"""Three-run constructive CNF with explicit prefix thresholds and e1=0."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import time


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def encode(base, aps):
    n = len(base)
    def q(i, j):
        return 2 * n + 3 * (i - 1) + j
    starts = [[-(n + 1), 1], [n + 1, -1]]
    for t in range(2, n + 1):
        starts.extend([[-(n + t), t], [-(n + t), -(t - 1)], [n + t, -t, t - 1]])
    starts.append([-1])
    counter = [[-(n + 1), q(1, 1)], [-q(1, 2)], [-q(1, 3)]]
    for i in range(2, n):
        counter.extend([[-(n + i), q(i, 1)], [-q(i - 1, 1), q(i, 1)]])
        for j in [2, 3]:
            counter.extend([[-(n + i), -q(i - 1, j - 1), q(i, j)], [-q(i - 1, j), q(i, j)]])
        counter.append([-(n + i), -q(i - 1, 3)])
    counter.append([-2 * n, -q(n - 1, 3)])
    ap_rows = []
    for a, d in aps:
        literals = [p if base[p - 1] == '0' else -p for p in range(a, a + 7 * d, d)]
        ap_rows.extend([literals, [-x for x in literals]])
    return 5 * n - 3, starts, counter, ap_rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--word', type=Path, default=Path(__file__).with_name('base3704.bits'))
    parser.add_argument('--AP-pool', type=Path, default=Path(__file__).with_name('AP-pool.json'))
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--pilot-small', action='store_true')
    args = parser.parse_args()
    began = time.monotonic()
    require(not args.output_dir.exists(), 'Existing instance cannot be replaced')
    base = args.word.read_text().strip()
    n = 9 if args.pilot_small else 3704
    require(len(base) == n and set(base) <= {'0', '1'}, 'Binary base domain')
    require((args.pilot_small and base == '010110010') or sha(args.word) ==
            '42e6cbef0710d38089475954306b3bd2c0367d5a28aed5ccc74b2698f27fed87', 'Pinned base')
    pool = json.loads(args.AP_pool.read_text())
    require(type(pool) is dict and set(pool) == {'length', 'term_count', 'base_bits_sha256', 'APs'}, 'AP pool schema')
    require(type(pool['length']) is int and pool['length'] == n and type(pool['term_count']) is int
            and pool['term_count'] == 7 and pool['base_bits_sha256'] == hashlib.sha256(base.encode()).hexdigest(), 'Pool scope')
    aps = pool['APs']
    require(type(aps) is list and 1 <= len(aps) <= 2893, 'Fixed construction AP cap')
    require(all(type(ap) is list and len(ap) == 2 and all(type(x) is int for x in ap)
                and ap[0] > 0 and ap[1] > 0 and ap[0] + 6 * ap[1] <= n for ap in aps), 'Actual positive APs')
    require(aps == sorted(aps) and len(set(map(tuple, aps))) == len(aps), 'Canonical APs')
    variables, starts, counter, ap_rows = encode(base, aps)
    clauses = starts + counter + ap_rows
    literals = sum(map(len, clauses))
    cases = len(clauses) + literals + 7 * len(aps) + n + 100
    require(cases <= 200000, 'Unchanged generation case cap')
    args.output_dir.mkdir(parents=True)
    target = args.output_dir / 'instance.cnf'
    with target.open('x') as stream:
        stream.write(f'p cnf {variables} {len(clauses)}\n')
        for row in clauses:
            stream.write(' '.join(map(str, row)) + ' 0\n')
    expected = json.loads(Path(__file__).with_name('expected.json').read_text())
    require(not args.pilot_small and sha(target) == expected['CNF_sha256']
            and sha(args.AP_pool) == expected['input_sha256']['AP-pool.json'], 'Canonical production inputs/instance')
    result = {'agent': 'six-vdw-1', 'role': 'researcher', 'created_at': datetime.now(timezone.utc).isoformat(),
              'status': 'THREE_RUN_CANONICAL_CNF_READY_PENDING_SOLVER_AND_DEFINITION_CHECK',
              'base_word': str(args.word.resolve()), 'base_file_sha256': sha(args.word),
              'AP_pool': str(args.AP_pool.resolve()), 'AP_pool_sha256': sha(args.AP_pool), 'APs': len(aps),
              'length': n, 'term_count': 7, 'max_disagreement_runs': 3, 'first_edit_bit': 0,
              'normalization_dependency': 'Verified pass24 at-most-two edit/agreement-run barrier and global color complement.',
              'variables': variables, 'clauses': len(clauses), 'literals': literals,
              'sections': {'starts_and_normalization': [0, len(starts)],
                           'counter': [len(starts), len(starts) + len(counter)],
                           'APs': [len(starts) + len(counter), len(clauses)]},
              'CNF': str(target.resolve()), 'CNF_sha256': sha(target), 'source_sha256': sha(__file__),
              'cardinality_encoding': 'Explicit Q(i,j) prefix thresholds, 1<=i<N and 1<=j<=3; one-way implications.',
              'conservative_combined_cases': cases, 'seconds': time.monotonic() - began,
              'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'threads': 1, 'family_exclusion': False, 'new_W_bound': None}
    require(result['seconds'] < 30, 'Unchanged30-second generation cap')
    (args.output_dir / 'metadata.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'variables', 'clauses', 'literals', 'APs', 'conservative_combined_cases', 'seconds']}), flush=True)


if __name__ == '__main__':
    main()
