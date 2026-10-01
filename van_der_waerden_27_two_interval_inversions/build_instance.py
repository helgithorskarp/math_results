"""Portable deterministic proposal; verify_encoding.py independently audits it."""
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time

SOURCE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    began = time.monotonic()
    if args.output_dir.exists():
        raise RuntimeError('Existing model')
    expected = json.loads((SOURCE / 'expected.json').read_text())
    base_path, pool_path = SOURCE / 'base3704.bits', SOURCE / 'AP-pool.json'
    if any(sha(SOURCE / name) != digest for name, digest in expected['input_sha256'].items()):
        raise RuntimeError('Pinned compact inputs changed')
    base = base_path.read_text().strip()
    aps = json.loads(pool_path.read_text())['APs']
    n, top = 3704, 7408
    if len(base) != n or set(base) != {'0', '1'} or len(aps) != 1485:
        raise RuntimeError('Wrong construction domain')
    starts = [[-(n + 1), 1], [n + 1, -1]]
    for t in range(2, n + 1):
        starts.extend([[-(n + t), t], [-(n + t), -(t - 1)], [n + t, -t, t - 1]])

    def a(i):
        return top + i if i < 3 else top + 2 * i - 1

    def b(i):
        return top + 3 if i == 2 else top + 2 * i - 2

    counter = []
    for i in range(1, n - 1):
        counter.append([-(n + i), a(i)])
        if i < n - 2:
            counter.append([-a(i), a(i + 1)])
        counter.append([-(n + i + 1), -a(i), b(i + 1)])
        if i < n - 2:
            counter.append([-b(i + 1), b(i + 2)])
        counter.append([-(n + i + 2), -b(i + 1)])
    clauses = starts + counter
    for first, step in aps:
        positives = [p if base[p - 1] == '0' else -p for p in range(first, first + 7 * step, step)]
        clauses.extend([positives, [-lit for lit in positives]])
    variables = 4 * n - 4
    literal_count = sum(map(len, clauses))
    cases = len(clauses) + literal_count + 7 * len(aps) + n + 100
    if cases > 200000:
        raise RuntimeError('Existing200000-case generation cap')
    args.output_dir.mkdir(parents=True)
    cnf = args.output_dir / 'instance.cnf'
    with cnf.open('x') as stream:
        stream.write(f'p cnf {variables} {len(clauses)}\n')
        for row in clauses:
            stream.write(' '.join(map(str, row)) + ' 0\n')
    if sha(cnf) != expected['CNF_sha256']:
        raise RuntimeError('Canonical instance byte hash differs')
    result = {'agent': 'six-vdw-1', 'role': 'researcher', 'created_at': datetime.now(timezone.utc).isoformat(),
              'status': 'TWO_RUN_CNF_READY_PENDING_SOLVER_AND_DEFINITION_CHECK',
              'base_word': str(base_path), 'base_file_sha256': sha(base_path),
              'AP_pool': str(pool_path), 'AP_pool_sha256': sha(pool_path), 'APs': len(aps),
              'length': n, 'term_count': 7, 'max_disagreement_runs': 2,
              'edit_ids': [1, n], 'start_ids': [n + 1, 2 * n],
              'virtual_edit_at_zero': False, 'no_symmetry_breaking': True,
              'cardinality_encoding': 'Explicit sequential atmost2 counter; canonical original row order.',
              'variables': variables, 'clauses': len(clauses), 'literals': literal_count,
              'CNF': str(cnf.resolve()), 'CNF_sha256': sha(cnf), 'source_sha256': sha(__file__),
              'conservative_combined_cases': cases, 'seconds': time.monotonic() - began,
              'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'threads': 1, 'family_exclusion': False, 'new_W_bound': None}
    (args.output_dir / 'metadata.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'CNF_sha256', 'conservative_combined_cases', 'seconds']}), flush=True)


if __name__ == '__main__':
    main()
