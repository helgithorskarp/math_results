"""Bounded MARCO pilot through the exact right-block interface.

The native oracle permits arbitrary interior recolouring. Only witnesses and
checked refutations, never unchecked oracle answers, support final claims.
"""
import argparse
from collections import Counter
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


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def write(path, data):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
    tmp.replace(path)


def prepare():
    plan = json.loads((HERE / 'plan.json').read_text())
    for path, digest in plan['input_files'].items():
        need(sha((REPO / path).read_bytes()) == digest, ('input', path))
    points, edges, _ = B.geometry()
    boundary = json.loads((REPO / 'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    m = set(boundary['mandatory_vertices'])
    u = set(boundary['optional_vertices'])
    p = json.loads((REPO / 'hadwiger_nelson_heule560_separator/certificate.json').read_text())
    left = set(p['blocks']['full']['vertices'])
    q = p['separator']; right = sorted((m | u) - left | set(q))
    optional = sorted(u - (left - {310}))
    es = [(a, b) for a, b in edges if a in right and b in right]
    states = [r['state'] for r in p['blocks']['mandatory']['states']]
    full = {r['state'] for r in p['blocks']['full']['states']}
    need(len(right) == 196 and len(es) == 806 and len(optional) == 60, 'right geometry')
    return plan, m, optional, right, es, q, states, full


def formula(optional, right, edges, q, states, full):
    index = {v: i for i, v in enumerate(right)}
    colour = lambda v, c: 4 * index[v] + c + 1
    selectors = {v: 4 * len(right) + i + 1 for i, v in enumerate(optional)}
    top = 4 * len(right) + len(optional)
    gates = {s: top + i + 1 for i, s in enumerate(states)}
    clauses = []
    for v in right:
        clauses.append([colour(v, c) for c in range(4)])
        for a in range(4):
            for b in range(a + 1, 4):
                clauses.append([-colour(v, a), -colour(v, b)])
    for a, b in edges:
        guards = [-selectors[v] for v in (a, b) if v in selectors]
        for c in range(4):
            clauses.append(guards + [-colour(a, c), -colour(b, c)])
    clauses.append(list(gates.values()))
    for s, z in gates.items():
        clauses.extend([[-z, colour(v, int(c))] for v, c in zip(q, s)])
        if s not in full:
            clauses.append([-selectors[310], -z])
    return clauses, colour, selectors, top + len(states)


def dimacs(clauses, top):
    return (f'p cnf {top} {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)).encode('ascii')


def aggregate(base, selectors, top, negative):
    clauses = [list(c) for c in base]
    clauses.append([top + i + 1 for i in range(len(negative))])
    optional = list(selectors)
    for i, row in enumerate(negative):
        z = top + i + 1
        clauses.extend([[-z, selectors[v]] for j, v in enumerate(optional) if row['mask'] >> j & 1])
    return dimacs(clauses, top + len(negative)), top + len(negative), len(clauses)


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
    resource.setrlimit(resource.RLIMIT_FSIZE, (512 * 1024**2, 512 * 1024**2))


class BoundedStop(Exception):
    pass


def main():
    from pysat.solvers import Solver
    from pysat.card import CardEnc, EncType
    import pysat
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--kissat', default='/scratch/researcher3-kissat/build/kissat')
    ap.add_argument('--drat-trim', default='/scratch/drat-trim-package/usr/bin/drat-trim')
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=False)
    plan, m, optional, right, edges, q, states, full = prepare()
    base, colour, selectors, top = formula(optional, right, edges, q, states, full)
    (args.out / 'oracle.cnf').write_bytes(dimacs(base, top))
    limits()
    started = time.monotonic(); queries = 0
    positives = []; negatives = []; master_clauses = []
    query_log = (args.out / 'queries.jsonl').open('w')
    current = {}; status = 'SEARCHING'; fullmask = (1 << len(optional)) - 1

    def snapshot(status):
        write(args.out / 'checkpoint.json', {'status': status, 'positives': positives, 'negatives': negatives,
              'current': current, 'queries': queries, 'seconds': time.monotonic() - started,
              'negative_proof_verified': False, 'next_phase_started': False})

    with Solver(name='g4', bootstrap_with=base) as oracle, Solver(name='g4') as master:
        def query(mask, phase):
            nonlocal queries
            oracle.conf_budget(plan['query_conflicts'])
            timer = threading.Timer(plan['query_seconds'], oracle.interrupt)
            before = time.monotonic(); timer.start()
            assumptions = [selectors[v] if mask >> i & 1 else -selectors[v] for i, v in enumerate(optional)]
            try:
                answer = oracle.solve_limited(assumptions=assumptions, expect_interrupt=True)
            finally:
                timer.cancel(); timer.join()
            oracle.clear_interrupt(); queries += 1
            query_log.write(json.dumps({'mask': mask, 'answer': answer, 'phase': phase,
                                       'seconds': time.monotonic() - before}) + '\n'); query_log.flush()
            if answer is None:
                raise BoundedStop('ORACLE_LIMIT')
            if not answer:
                return None
            model = set(x for x in oracle.get_model() if x > 0)
            selected = {v for i, v in enumerate(optional) if mask >> i & 1}
            support = (m | selected) & set(right)
            cs = {}
            for v in support:
                choices = [c for c in range(4) if colour(v, c) in model]
                need(len(choices) == 1, 'decoded one-hot'); cs[v] = choices[0]
            need(all(cs[a] != cs[b] for a, b in edges if a in support and b in support), 'decoded edge')
            state = ''.join(str(cs[v]) for v in q)
            need(state in (full if 310 in selected else states), 'decoded interface')
            return {'mask': mask, 'state': state, 'colouring': ''.join(str(cs[v]) if v in cs else '.' for v in right)}

        # These are controls of the new right encoding, not a rerun of the left theorem.
        need(query(0, 'empty_control') is not None, 'empty positive control')
        need(query(fullmask, 'full_control') is None, 'full negative control')
        for i in range(len(optional)):
            master.add_clause([i + 1, -(i + 1)])
        master.set_phases(list(range(1, len(optional) + 1)))
        try:
            while True:
                if len(positives) + len(negatives) >= plan['boundary_cap']:
                    status = 'BOUNDARY_CAP'; break
                if queries >= plan['query_cap'] or time.monotonic() - started >= plan['search_seconds']:
                    status = 'SEARCH_LIMIT'; break
                master.conf_budget(plan['query_conflicts'])
                timer = threading.Timer(plan['query_seconds'], master.interrupt); timer.start()
                try:
                    ans = master.solve_limited(expect_interrupt=True)
                finally:
                    timer.cancel(); timer.join()
                master.clear_interrupt()
                if ans is None:
                    status = 'MASTER_LIMIT'; break
                if not ans:
                    status = 'LATTICE_COMPLETE'; break
                model = set(x for x in master.get_model() if x > 0)
                mask = sum(1 << i for i in range(len(optional)) if i + 1 in model)
                current = {'initial_mask': mask}; snapshot('SEARCHING')
                witness = query(mask, 'initial')
                if witness is not None:
                    for i in range(len(optional)):
                        if mask >> i & 1:
                            continue
                        trial = mask | (1 << i)
                        new = query(trial, 'grow')
                        if new is not None:
                            mask = trial; witness = new
                    positives.append(witness)
                    clause = [i + 1 for i in range(len(optional)) if not mask >> i & 1]
                else:
                    deletion = {}
                    for i in range(len(optional)):
                        if not mask >> i & 1:
                            continue
                        trial = mask & ~(1 << i)
                        new = query(trial, 'shrink')
                        if new is None:
                            mask = trial
                        else:
                            deletion[i] = new
                    # Restrict every positive deletion witness to the final core-minus-v.
                    ds = []
                    for i in range(len(optional)):
                        if not mask >> i & 1:
                            continue
                        w = deletion[i]; submask = mask & ~(1 << i)
                        keep = m | {v for j, v in enumerate(optional) if submask >> j & 1}
                        text = ''.join(c if v in keep else '.' for v, c in zip(right, w['colouring']))
                        ds.append({'removed': optional[i], 'mask': submask, 'state': w['state'], 'colouring': text})
                    negatives.append({'mask': mask, 'deletion_witnesses': ds})
                    clause = [-(i + 1) for i in range(len(optional)) if mask >> i & 1]
                master.add_clause(clause); master_clauses.append(clause)
                current = {}; snapshot('SEARCHING')
                print(json.dumps({'rows': len(positives) + len(negatives), 'positives': len(positives),
                      'negatives': len(negatives), 'last_size': mask.bit_count(), 'queries': queries,
                      'seconds': time.monotonic() - started}), flush=True)
                if witness is None and mask.bit_count() <= 16:
                    status = 'TARGET_CANDIDATE'; break
        except BoundedStop as stop:
            status = str(stop)
    query_log.close()
    search_seconds = time.monotonic() - started
    certificate = {'optional_order': optional, 'right_vertices': right, 'separator': q,
                   'positive_covers': positives, 'negative_cores': negatives,
                   'search_status': status, 'whole560_family_closed': False, 'record_improvement': False}
    write(args.out / 'certificate.json', certificate)
    # Terminal frontier count is capped, with no follow-on graph queries.
    cardinal = CardEnc.equals(list(range(1, len(optional) + 1)), 16, encoding=EncType.seqcounter)
    frontier = []; terminal_complete = False
    with Solver(name='g4', bootstrap_with=master_clauses + cardinal.clauses) as rem:
        while len(frontier) < 4097 and time.monotonic() - started < search_seconds + 60:
            rem.conf_budget(200000)
            timer = threading.Timer(5, rem.interrupt); timer.start()
            try:
                answer = rem.solve_limited(expect_interrupt=True)
            finally:
                timer.cancel(); timer.join()
            rem.clear_interrupt()
            if answer is None:
                break
            if not answer:
                terminal_complete = True; break
            model = set(x for x in rem.get_model() if x > 0)
            mask = sum(1 << i for i in range(len(optional)) if i + 1 in model)
            need(mask.bit_count() == 16, 'terminal size')
            frontier.append(mask)
            rem.add_clause([-(i + 1) for i in range(len(optional)) if mask >> i & 1])
    write(args.out / 'terminal_frontier.json', {'complete': terminal_complete, 'masks': frontier})
    raw, nvars, nclauses = aggregate(base, selectors, top, negatives)
    cnf = args.out / 'negative.cnf'; cnf.write_bytes(raw)
    proof = args.out / 'negative.drat'; snapshot('SEARCH_FINISHED_PROOF_PENDING')
    manifest = None
    if negatives:
        with (args.out / 'kissat.log').open('wb') as log:
            result = subprocess.run([args.kissat, '--seed=0', '--conflicts=4000000', '--time=180', str(cnf), str(proof)], stdout=log, stderr=subprocess.STDOUT, timeout=200, preexec_fn=limits)
        need(result.returncode == 20, 'combined negative proof')
        with (args.out / 'drat.log').open('wb') as log:
            result = subprocess.run([args.drat_trim, str(cnf), str(proof)], stdout=log, stderr=subprocess.STDOUT, timeout=200, preexec_fn=limits)
        need(result.returncode == 0 and b's VERIFIED' in (args.out / 'drat.log').read_bytes().splitlines(), 'combined DRAT')
        manifest = {'cnf_sha256': sha(raw), 'cnf_bytes': len(raw), 'variables': nvars, 'clauses': nclauses,
                    'proof_sha256': sha(proof.read_bytes()), 'proof_bytes': proof.stat().st_size, 'cases': len(negatives),
                    'solver_sha256': sha(Path(args.kissat).read_bytes()), 'checker_sha256': sha(Path(args.drat_trim).read_bytes()),
                    'verified': True}
        write(args.out / 'proof_manifest.json', manifest)
    result = {'search_status': status, 'queries': queries, 'positive_covers': len(positives), 'negative_cores': len(negatives),
              'negative_core_sizes': dict(sorted(Counter(r['mask'].bit_count() for r in negatives).items())),
              'positive_cover_sizes': dict(sorted(Counter(r['mask'].bit_count() for r in positives).items())),
              'terminal_frontier_complete': terminal_complete, 'terminal_frontier_count_or_lower_bound': len(frontier),
              'python_sat': pysat.__version__, 'search_seconds': search_seconds, 'total_seconds': time.monotonic() - started,
              'negative_proof_verified': bool(manifest), 'whole560_family_closed': False, 'record_improvement': False,
              'next_phase_started': False, 'oracle_variables': top, 'oracle_clauses': len(base),
              'oracle_sha256': sha(dimacs(base, top)), 'certificate_bytes': (args.out / 'certificate.json').stat().st_size}
    write(args.out / 'result.json', result); write(args.out / 'checkpoint.json', result)
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
