#!/usr/bin/env python3
"""Optional bounded discovery; the separate verifier trusts no solver verdict."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time

from model import formula, dimacs

HERE = Path(__file__).resolve().parent


def read_clauses(path):
    answer = []
    for line in path.read_text().splitlines():
        if not line or line[0] in 'pc':
            continue
        row = list(map(int, line.split()))
        if row[-1] != 0:
            raise ValueError('unterminated clause')
        answer.append(tuple(sorted(row[:-1])))
    return answer


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--kissat', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.work.exists():
        raise ValueError('use a fresh work directory')
    args.work.mkdir(parents=True)
    args.output.mkdir(parents=True, exist_ok=True)
    template = json.loads((HERE/'TEMPLATE.json').read_text())
    start = time.monotonic()

    def solve(name, deleted=None, full=False):
        variables, clauses = formula(template, deleted, full)
        cnf, proof = args.work/f'{name}.cnf', args.work/f'{name}.drat'
        cnf.write_text(dimacs(variables, clauses))
        logpath = args.work/f'{name}.log'
        with logpath.open('w') as log:
            completed = subprocess.run([str(args.kissat), '--time=10', str(cnf), str(proof)],
                                       stdout=log, stderr=subprocess.STDOUT, timeout=30)
        if completed.returncode not in (10, 20):
            raise ValueError(f'{name}: no conclusion; keep checkpoint, no theorem')
        return completed.returncode, variables, clauses, logpath

    status, variables, clauses, _ = solve('obstruction')
    if status != 20:
        raise ValueError('expected an obstruction')
    with (args.work/'replay.log').open('w') as log:
        replay = subprocess.run([str(args.drat_trim), str(args.work/'obstruction.cnf'),
                                 str(args.work/'obstruction.drat'), '-c', str(args.work/'support.cnf'),
                                 '-l', str(args.work/'trimmed.drat')], stdout=log,
                                stderr=subprocess.STDOUT, timeout=30)
    if replay.returncode != 0 or 's VERIFIED' not in (args.work/'replay.log').read_text():
        raise ValueError('external proof replay failed')
    support = tuple(sorted(set(read_clauses(args.work/'support.cnf')), key=lambda c:(len(c),c)))
    if not set(support) <= set(clauses):
        raise ValueError('unsupported proof premise')
    (args.output/'SUPPORT.cnf').write_text(dimacs(variables, support))
    # Keep all additions and ignore deletions. This strengthens the available
    # clause set, so valid RUP additions remain valid. The independent checker
    # below rejects any non-RUP (including genuine RAT-only) addition.
    additions = [line for line in (args.work/'trimmed.drat').read_text().splitlines()
                 if line and not line.startswith('d ')]
    (args.output/'CERTIFICATE.rup').write_text('\n'.join(additions)+'\n')

    deletion_witnesses = []
    for deleted in range(18):
        status, variables, _, logfile = solve(f'delete_{deleted:02d}', deleted, full=True)
        if status != 10:
            raise ValueError('vertex minimality not established')
        assignment = {}
        for line in logfile.read_text().splitlines():
            if line.startswith('v '):
                for token in line[2:].split():
                    value = int(token)
                    if value:
                        assignment[abs(value)] = value > 0
        if set(assignment) != set(range(1, len(variables)+1)):
            raise ValueError('incomplete SAT witness')
        bits = sum(1 << i for i in range(len(variables)) if assignment[i+1])
        deletion_witnesses.append({'deleted': deleted, 'central_red_mask_hex': format(bits, 'x')})
    (args.output/'DELETIONS.json').write_text(json.dumps(deletion_witnesses, indent=2)+'\n')
    provenance = {
        'scope': 'one 18-vertex mixed obstruction and all 18 full-Ramsey vertex deletions',
        'solve_seconds_per_case': 10,
        'process_timeout_seconds': 30,
        'elapsed_seconds': round(time.monotonic()-start, 6),
        'largest_child_peak_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        'kissat_binary_sha256': hashlib.sha256(args.kissat.read_bytes()).hexdigest(),
        'drat_trim_binary_sha256': hashlib.sha256(args.drat_trim.read_bytes()).hexdigest(),
        'full_formula_sha256': hashlib.sha256((args.work/'obstruction.cnf').read_bytes()).hexdigest(),
        'full_proof_sha256': hashlib.sha256((args.work/'obstruction.drat').read_bytes()).hexdigest(),
        'full_proof_bytes': (args.work/'obstruction.drat').stat().st_size,
    }
    (args.output/'discovery_report.json').write_text(json.dumps(provenance, indent=2, sort_keys=True)+'\n')
    print(json.dumps(provenance, sort_keys=True))


if __name__ == '__main__':
    main()
