"""Bounded complete monotone selector relation; raw work stays in --out."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / 'hadwiger_nelson_heule632_pair_pilot'))
import build as B


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def write(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    temp.replace(path)


def prepare():
    plan = json.loads((HERE / 'plan.json').read_text())
    for path, digest in plan['input_files'].items():
        need(sha((REPO / path).read_bytes()) == digest, ('input identity', path))
    points, edges, _ = B.geometry()
    parent = json.loads((REPO / 'hadwiger_nelson_heule560_separator/certificate.json').read_text())
    vertices = parent['blocks']['full']['vertices']
    mandatory = set(parent['blocks']['mandatory']['vertices'])
    optional = sorted(set(vertices) - mandatory)
    need(optional == plan['optional_order'], 'selector order')
    edges = [(u, v) for u, v in edges if u in vertices and v in vertices]
    need(len(vertices) == 383 and len(edges) == 1952, 'full large block')
    return plan, parent, vertices, mandatory, optional, edges


def gated(vertices, optional, edges):
    index = {v: i for i, v in enumerate(vertices)}
    var = lambda v, c: 4 * index[v] + c + 1
    selector = {v: 4 * len(vertices) + i + 1 for i, v in enumerate(optional)}
    clauses = []
    for v in vertices:
        clauses.append([var(v, c) for c in range(4)])
        for a in range(4):
            for b in range(a + 1, 4):
                clauses.append([-var(v, a), -var(v, b)])
    for u, v in edges:
        guards = [-selector[w] for w in (u, v) if w in selector]
        for c in range(4):
            clauses.append(guards + [-var(u, c), -var(v, c)])
    return clauses, var, selector


def aggregate(vertices, optional, edges, q, rows):
    clauses, var, selector = gated(vertices, optional, edges)
    cases = [(r['state'], mask) for r in rows for mask in r.get('negative_masks', [])]
    top = 4 * len(vertices) + len(optional)
    clauses.append(list(range(top + 1, top + len(cases) + 1)))
    for i, (state, mask) in enumerate(cases):
        gate = top + i + 1
        clauses.extend([[-gate, var(v, int(c))] for v, c in zip(q, state)])
        clauses.extend([[-gate, selector[v]] for j, v in enumerate(optional) if mask >> j & 1])
    raw = (f'p cnf {top + len(cases)} {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)).encode('ascii')
    return raw, cases, top + len(cases), len(clauses)


class BoundedStop(Exception):
    pass


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
    resource.setrlimit(resource.RLIMIT_FSIZE, (512 * 1024**2, 512 * 1024**2))


def main():
    from pysat.solvers import Solver
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--kissat', default='/scratch/researcher3-kissat/build/kissat')
    ap.add_argument('--drat-trim', default='/scratch/drat-trim-package/usr/bin/drat-trim')
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=False)
    plan, parent, vertices, mandatory, optional, edges = prepare()
    limits()
    base, var, selector = gated(vertices, optional, edges)
    q = parent['separator']; full = {r['state'] for r in parent['blocks']['full']['states']}
    fullmask = (1 << len(optional)) - 1
    started = time.monotonic(); queries = 0; rows = []; current = {}
    order = sorted(range(fullmask + 1), key=lambda x: (-x.bit_count(), x))
    query_log = (args.out / 'queries.jsonl').open('w')

    def checkpoint(status):
        write(args.out / 'checkpoint.json', {'status': status, 'rows': rows, 'current': current,
              'queries': queries, 'seconds': time.monotonic() - started,
              'negative_certified': False, 'next_phase_started': False})

    try:
        for parent_row in parent['blocks']['mandatory']['states']:
            state = parent_row['state']
            if state in full:
                rows.append({'state': state, 'inherited_full': True}); continue
            colour = dict(zip(parent['blocks']['mandatory']['vertices'], parent_row['colouring']))
            positives = {0: ''.join(colour.get(v, '.') for v in vertices)}
            negatives = {fullmask}
            current = {'state': state}

            def add_positive(mask, text):
                need(not any(n & mask == n for n in negatives), 'positive/negative overlap')
                if any(mask & p == mask for p in positives):
                    return
                for p in list(positives):
                    if p & mask == p:
                        del positives[p]
                positives[mask] = text

            def save_current():
                current.update({'positive_masks': sorted(positives), 'negative_masks': sorted(negatives),
                                'positive_colourings': {str(m): c for m, c in positives.items()}})
                checkpoint('SEARCHING')

            with Solver(name='g4', bootstrap_with=base + [[var(v, int(c))] for v, c in zip(q, state)]) as solver:
                def query(mask):
                    nonlocal queries
                    remaining = plan['total_search_seconds'] - (time.monotonic() - started)
                    if remaining <= 0 or queries >= plan['query_cap']:
                        raise BoundedStop('TOTAL_LIMIT')
                    assumptions = [selector[v] if mask >> i & 1 else -selector[v] for i, v in enumerate(optional)]
                    solver.conf_budget(plan['query_conflicts'])
                    timer = threading.Timer(min(remaining, plan['query_seconds']), solver.interrupt)
                    before = time.monotonic(); timer.start()
                    try:
                        answer = solver.solve_limited(assumptions=assumptions, expect_interrupt=True)
                    finally:
                        timer.cancel(); timer.join()
                    solver.clear_interrupt(); queries += 1
                    query_log.write(json.dumps({'state': state, 'mask': mask, 'answer': answer, 'seconds': time.monotonic() - before}) + '\n'); query_log.flush()
                    if answer is None:
                        raise BoundedStop('QUERY_LIMIT')
                    if not answer:
                        return False, None
                    model = set(x for x in solver.get_model() if x > 0)
                    keep = mandatory | {v for i, v in enumerate(optional) if mask >> i & 1}
                    colours = {}
                    for v in keep:
                        choices = [c for c in range(4) if var(v, c) in model]
                        need(len(choices) == 1, 'one-hot model'); colours[v] = choices[0]
                    need(all(colours[a] != colours[b] for a, b in edges if a in keep and b in keep), 'proper model')
                    need(''.join(str(colours[v]) for v in q) == state, 'boundary pins')
                    return True, ''.join(str(colours[v]) if v in keep else '.' for v in vertices)

                while True:
                    unknown = next((mask for mask in order if not any(mask & p == mask for p in positives) and not any(mask & n == n for n in negatives)), None)
                    if unknown is None:
                        break
                    answer, text = query(unknown)
                    if answer:
                        add_positive(unknown, text)
                    else:
                        minimal = unknown
                        for bit in range(len(optional)):
                            if not (minimal >> bit & 1):
                                continue
                            trial = minimal & ~(1 << bit)
                            if any(trial & p == trial for p in positives):
                                continue
                            answer, text = query(trial)
                            if answer:
                                add_positive(trial, text)
                            else:
                                minimal = trial
                        need(not any(minimal & p == minimal for p in positives), 'negative/positive overlap')
                        negatives = {n for n in negatives if n & minimal != minimal}
                        negatives.add(minimal)
                    save_current()
            rows.append({'state': state, 'inherited_full': False,
                         'positive_covers': [{'mask': p, 'colouring': positives[p]} for p in sorted(positives)],
                         'negative_masks': sorted(negatives)})
            current = {}; checkpoint('SEARCHING')
            print(json.dumps({'states_complete': len(rows), 'queries': queries, 'positive_covers': len(positives), 'negative_masks': len(negatives), 'seconds': time.monotonic() - started}), flush=True)
    except BoundedStop as stop:
        checkpoint(str(stop)); print(str(stop), flush=True); return
    finally:
        query_log.close()
    certificate = {'optional_order': optional, 'separator': q, 'rows': rows,
                   'whole560_family_closed': False, 'record_improvement': False}
    write(args.out / 'certificate.json', certificate)
    raw, cases, nvars, nclauses = aggregate(vertices, optional, edges, q, rows)
    cnf = args.out / 'negative.cnf'; cnf.write_bytes(raw)
    proof = args.out / 'negative.drat'
    checkpoint('SEARCH_COMPLETE_PROOF_PENDING')
    t = time.monotonic()
    with (args.out / 'kissat.log').open('wb') as log:
        result = subprocess.run([args.kissat, '--seed=0', '--conflicts=2000000', '--time=120', str(cnf), str(proof)], stdout=log, stderr=subprocess.STDOUT, timeout=135, preexec_fn=limits)
    need(result.returncode == 20, 'combined proof UNSAT')
    logpath = args.out / 'drat.log'
    with logpath.open('wb') as log:
        result = subprocess.run([args.drat_trim, str(cnf), str(proof)], stdout=log, stderr=subprocess.STDOUT, timeout=135, preexec_fn=limits)
    need(result.returncode == 0 and b's VERIFIED' in logpath.read_bytes().splitlines(), 'combined DRAT verified')
    manifest = {'cases': len(cases), 'variables': nvars, 'clauses': nclauses, 'cnf_sha256': sha(raw), 'cnf_bytes': len(raw),
                'proof_sha256': sha(proof.read_bytes()), 'proof_bytes': proof.stat().st_size,
                'solver_sha256': sha(Path(args.kissat).read_bytes()), 'checker_sha256': sha(Path(args.drat_trim).read_bytes()), 'verified': True}
    write(args.out / 'proof_manifest.json', manifest)
    report = {'status': 'COMPLETE_DRAT_VERIFIED', 'states': len(rows), 'masks': fullmask + 1, 'queries': queries,
              'inherited_full_states': len(full), 'negative_cases': len(cases),
              'positive_covers': sum(len(r.get('positive_covers', [])) for r in rows),
              'seconds': time.monotonic() - started, 'proof_seconds': time.monotonic() - t,
              'certificate_bytes': (args.out / 'certificate.json').stat().st_size,
              'next_phase_started': False, 'whole560_family_closed': False, 'record_improvement': False}
    write(args.out / 'result.json', report)
    write(args.out / 'checkpoint.json', report)
    print(json.dumps(report, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
