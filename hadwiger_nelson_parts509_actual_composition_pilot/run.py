#!/usr/bin/env python3
"""One fixed-cost actual-composition pilot, with an explicit 32-query stop."""
import argparse
from collections import deque
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
from pysat.solvers import Solver
from engine import build, direct, decode, check_colouring, require


def save(path, value):
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    temporary.replace(path)


def file_cap():
    resource.setrlimit(resource.RLIMIT_FSIZE, (268435456, 268435456))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--kissat', type=Path, required=True)
    ap.add_argument('--drat-trim', type=Path, required=True)
    args = ap.parse_args()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    resource.setrlimit(resource.RLIMIT_AS, (4294967296, 4294967296))
    start = time.monotonic()
    data = build()
    save(work / 'preflight.json', data['facts'])
    (work / 'seed.cnf').write_bytes(direct(data, data['seed_U'])[0])
    result = dict(status='running', preflight=data['facts'], queries=[], selected_U=data['seed_U'])
    save(work / 'result.json', result)
    mandatory = set(data['interface'])
    inverse = {a: v for v, a in data['activation'].items()}
    selected = set(data['seed_U'])
    with Solver(name='cadical195', bootstrap_with=data['clauses']) as solver:
        def query(U, budget, removed):
            assumptions = [data['activation'][v] for v in sorted(U - mandatory)]
            solver.conf_budget(budget)
            begin = time.monotonic()
            answer = solver.solve_limited(assumptions=assumptions)
            row = dict(query=len(result['queries']), block_vertices=len(U), removed=sorted(removed),
                       conflict_budget=budget, wall_seconds=time.monotonic() - begin,
                       answer='UNSAT_UNCERTIFIED' if answer is False else 'SAT_CHECKED' if answer is True else 'UNKNOWN')
            if answer is True:
                row['witness'] = decode(data, U, solver.get_model())
            elif answer is False:
                core = solver.get_core() or []
                require(set(core) <= set(assumptions), 'assumption core')
                row['core_U'] = sorted(mandatory | {inverse[a] for a in core})
            result['queries'].append(row)
            save(work / 'result.json', result)
            print(json.dumps({k: v for k, v in row.items() if k not in ('core_U', 'witness')}), flush=True)
            return answer, row
        answer, row = query(selected, 100000, [])
        if answer is not False:
            result.update(status='SEED_FOUR_COLOURABLE' if answer else 'SEED_UNKNOWN', wall_seconds=time.monotonic() - start)
            save(work / 'result.json', result)
            return
        selected = set(row['core_U'])
        order = sorted(selected - mandatory, key=lambda v: (v < 509, len(data['full_adj'][v] & (selected | set(data['S']))), v))
        queue = deque(order[i:i + 24] for i in range(0, len(order), 24))
        while queue and len(result['queries']) < 33 and len(selected) > 373:
            chunk = [v for v in queue.popleft() if v in selected]
            if not chunk:
                continue
            answer, row = query(selected - set(chunk), 25000, chunk)
            if answer is False:
                selected = set(row['core_U'])
            elif len(chunk) > 1:
                midpoint = len(chunk) // 2
                queue.append(chunk[:midpoint])
                queue.append(chunk[midpoint:])
            result.update(selected_U=sorted(selected), pending_chunks=list(queue))
            save(work / 'result.json', result)
    result.update(selected_U=sorted(selected), final_block_vertices=len(selected), final_graph_vertices=len(selected) + 135,
                  status='FINAL_DIRECT_PROOF_PENDING')
    raw, vertices, edges = direct(data, selected)
    (work / 'final.cnf').write_bytes(raw)
    result.update(final_edges=len(edges), final_cnf_sha256=sha256(raw).hexdigest())
    save(work / 'result.json', result)
    begin = time.monotonic()
    with (work / 'final_solver.log').open('w') as stream:
        completed = subprocess.run([str(args.kissat.resolve()), '--time=180', str(work / 'final.cnf'), str(work / 'final.drat')],
                                   stdout=stream, stderr=subprocess.STDOUT, preexec_fn=file_cap)
    result['final_solver'] = dict(exit_code=completed.returncode, wall_seconds=time.monotonic() - begin)
    if completed.returncode == 20:
        begin = time.monotonic()
        with (work / 'final_checker.log').open('w') as stream:
            checked = subprocess.run([str(args.drat_trim.resolve()), str(work / 'final.cnf'), str(work / 'final.drat')],
                                     stdout=stream, stderr=subprocess.STDOUT)
        require(checked.returncode == 0 and 's VERIFIED' in (work / 'final_checker.log').read_text(), 'complete final proof rejected')
        result.update(status='NON_FOUR_COLOURABILITY_DRAT_VERIFIED',
                      final_checker=dict(exit_code=checked.returncode, wall_seconds=time.monotonic() - begin),
                      final_proof_bytes=(work / 'final.drat').stat().st_size,
                      final_proof_sha256=sha256((work / 'final.drat').read_bytes()).hexdigest())
        raw5, _, _ = direct(data, selected, 5)
        (work / 'five.cnf').write_bytes(raw5)
        five = subprocess.run([str(args.kissat.resolve()), '--time=20', str(work / 'five.cnf')], capture_output=True, text=True)
        (work / 'five_solver.log').write_text(five.stdout + five.stderr)
        result['five_solver_exit'] = five.returncode
        if five.returncode == 10:
            positive = {int(v) for line in five.stdout.splitlines() if line.startswith('v ') for v in line.split()[1:] if int(v) > 0}
            colouring = ''.join(str(next(c for c in range(5) if 5 * i + c + 1 in positive)) for i in range(len(vertices)))
            check_colouring(data, selected, colouring, 5)
            result.update(status='FIVE_CHROMATIC_GRAPH_VERIFIED', five_colouring=colouring)
    else:
        result['status'] = 'FINAL_NEGATIVE_CERTIFICATE_INCOMPLETE'
    result['wall_seconds'] = time.monotonic() - start
    result['search_peak_RSS_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    save(work / 'result.json', result)
    print(json.dumps({k: v for k, v in result.items() if k not in ('queries', 'selected_U', 'pending_chunks', 'five_colouring')}), flush=True)


if __name__ == '__main__':
    main()
