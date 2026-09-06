#!/usr/bin/env python3
"""One bounded call on the audited 41-core formula; no repeated solver attempts."""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import resource
import subprocess
import time

from check_certificate import input_rows
from drat import require


def run(command, log, timeout):
    start = time.monotonic()
    with log.open('w') as out:
        process = subprocess.Popen(list(map(str, command)), stdout=out, stderr=subprocess.STDOUT)
        expired = False
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            expired = True
            process.terminate()
            try:
                code = process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                process.kill()
                code = process.wait()
    return {'command': list(map(str, command)), 'exit_code': code, 'wall_timeout': expired,
            'wall_seconds': time.monotonic()-start,
            'children_max_rss_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}


def sat_witness(log, destination):
    rows, _ = input_rows()
    assignment = {}
    for line in log.read_text().splitlines():
        if line.startswith('v '):
            for lit in map(int, line.split()[1:]):
                if lit == 0:
                    continue
                require(1 <= abs(lit) <= 40 and abs(lit) not in assignment, 'SAT variable')
                assignment[abs(lit)] = int(lit > 0)
    require(set(assignment) == set(range(1,41)), 'complete SAT assignment')
    assignment[0] = 0
    graph = {(u,v) for u,v in combinations(range(41),2)
             if int(bool(rows[u] & (1 << v))) ^ assignment[u] ^ assignment[v]}
    for q in combinations(range(41),5):
        require(len({e in graph for e in combinations(q,2)}) == 2, 'SAT graph contains monochromatic K5')
    destination.write_text('41\n'+''.join(f'{u} {v}\n' for u,v in sorted(graph)))
    return {'vertices': 41, 'red_edges': len(graph), 'spins': [assignment[v] for v in range(41)],
            'edge_sha256': sha256(destination.read_bytes()).hexdigest(), 'target_43_graph': False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--kissat', type=Path, required=True)
    p.add_argument('--drat-trim', type=Path, required=True)
    a = p.parse_args()
    w = a.work.resolve()
    require(not (w/'solver.log').exists(), 'existing solver attempt')
    cnf = w/'switch.cnf'
    verified = json.loads((w/'verification.json').read_text())
    require(verified['status'] == 'VERIFIED_EXACT_CORE_SWITCH_FORMULA', 'unaudited formula')
    require(verified['cnf_sha256'] == sha256(cnf.read_bytes()).hexdigest(), 'audited formula identity')
    result = {'status': 'NOT_STARTED', 'solver_invocations': 1, 'cnf_sha256': verified['cnf_sha256'],
              'kissat_sha256': sha256(a.kissat.read_bytes()).hexdigest(),
              'drat_trim_sha256': sha256(a.drat_trim.read_bytes()).hexdigest()}
    result['solver'] = run([a.kissat.resolve(), '--time=300', '--no-binary', cnf, w/'untrimmed.drat'], w/'solver.log', 330)
    status = result['solver']['exit_code']
    if result['solver']['wall_timeout'] or status not in (10,20):
        result['status'] = 'NO_CONCLUSION'
    elif status == 10:
        require('s SATISFIABLE' in (w/'solver.log').read_text(), 'missing SAT status')
        result['witness'] = sat_witness(w/'solver.log', w/'ramsey41.edges')
        result['status'] = 'DIRECTLY_VERIFIED_RAMSEY41_SWITCH'
    else:
        require('s UNSATISFIABLE' in (w/'solver.log').read_text(), 'missing UNSAT status')
        result['status'] = 'UNSAT_UNCHECKED'
        (w/'decision.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
        result['proof_check'] = run([a.drat_trim.resolve(), cnf, w/'untrimmed.drat',
                                    '-c', w/'obstruction.dimacs', '-l', w/'certificate.drat.txt'], w/'trim.log', 330)
        require(result['proof_check']['exit_code'] == 0 and 's VERIFIED' in (w/'trim.log').read_text(), 'proof not checked')
        result['status'] = 'DRAT_TRIM_CHECKED_PENDING_PHYSICAL_CERTIFICATE'
    result['files'] = {f.name: {'bytes': f.stat().st_size, 'sha256': sha256(f.read_bytes()).hexdigest()}
                       for f in sorted(w.iterdir()) if f.is_file() and f.name != 'decision.json'}
    (w/'decision.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
