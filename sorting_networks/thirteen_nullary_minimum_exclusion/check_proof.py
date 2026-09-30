"""Replay regenerated native proofs without importing encoder or SAT library."""
import argparse
import hashlib
import json
from pathlib import Path
import time
from watched_rup import replay, self_check

HERE = Path(__file__).resolve().parent


def clauses(path):
    with path.open() as src:
        header = src.readline().split(); assert header[:2] == ['p', 'cnf']; n, expected = map(int, header[2:])
        rows = []
        for line in src:
            r = list(map(int, line.split())); assert r[-1] == 0
            assert all(0 < abs(v) <= n for v in r[:-1]); rows.append(r[:-1])
    assert len(rows) == expected
    return n, rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--index', type=int)
    parser.add_argument('--manifest-only', action='store_true', help='Checks hashes only; does not establish UNSAT')
    args = parser.parse_args()
    c = json.loads((HERE / 'certificate.json').read_text()); start = time.monotonic()
    print(json.dumps({'small_truth_table_checks': self_check()}), flush=True)
    records = [r for r in c['proofs'] if args.index is None or r['index'] == args.index]; assert records
    additions = 0
    for r in records:
        stem = args.scratch / f"F{r['index']}-size10"; cnf, proof = stem.with_suffix('.cnf'), stem.with_suffix('.drat')
        assert hashlib.sha256(cnf.read_bytes()).hexdigest() == r['full_cnf_sha256']
        assert hashlib.sha256(proof.read_bytes()).hexdigest() == r['native_proof_sha256']
        n, initial = clauses(cnf); assert n == r['variables'] and len(initial) == r['clauses']
        if args.manifest_only:
            print(json.dumps({'index': r['index'], 'status': 'Hashes agree; no new proof replay'}), flush=True)
            continue
        a, d = replay(n, initial, proof)
        assert a == r['RUP_additions'] and d == r['ignored_deletions']; additions += a
        print(json.dumps({'index': r['index'], 'RUP_additions': a, 'status': 'Verified empty clause'}), flush=True)
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher', 'sources_checked': len(records),
                      'RUP_additions': additions, 'elapsed_seconds': time.monotonic() - start,
                      'status': 'Hashes only' if args.manifest_only else 'Complete forward RUP replay passed'}))


if __name__ == '__main__':
    main()
