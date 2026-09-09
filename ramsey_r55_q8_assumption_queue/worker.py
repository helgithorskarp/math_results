"""Materialize, import and join complete physical43 worker certificates.

This module never launches a target solver. Positive-hint LRAT is accepted;
RAT additions require a separate verified conversion and are rejected here.
"""
import argparse
import hashlib
import json
from pathlib import Path

import basis
import certificate
import task_queue


def checked_job(job):
    if not isinstance(job, dict) or set(job) != {'r', 'core_assumptions', 'edge_cube'}:
        raise ValueError('Worker job schema')
    basis.checked_r(job['r'])
    task_queue.match_mask(job['core_assumptions'])
    cube = job['edge_cube']
    if not isinstance(cube, list) or any(type(x) is not int or not 2 <= abs(x) <= 801 for x in cube):
        raise ValueError('Branch only on the 800 physical cross edges')
    if len({abs(x) for x in cube}) != len(cube):
        raise ValueError('Duplicate or contradictory edge cube')
    return job['core_assumptions']+cube


def metadata(r):
    basis.checked_r(r)
    return json.loads((basis.HERE/'EXPECTED.json').read_text())['bases'][str(r)]


def base_bytes(directory, r):
    meta = metadata(r)
    raw = (Path(directory)/f'q8-r{r}.cnf').read_bytes()
    if hashlib.sha256(raw).hexdigest() != meta['sha256']:
        raise ValueError('Wrong complete physical base')
    return meta, raw


def materialize(directory, job, output):
    a = checked_job(job)
    meta, raw = base_bytes(directory, job['r'])
    header, body = raw.split(b'\n', 1)
    if header != f"p cnf {meta['variables']} {meta['clauses']}".encode():
        raise ValueError('Base header mismatch')
    digest = hashlib.sha256()
    with Path(output).open('xb') as f:
        for part in [f"p cnf {meta['variables']} {meta['clauses']+len(a)}\n".encode(), body,
                     ''.join(f'{x} 0\n' for x in a).encode()]:
            f.write(part); digest.update(part)
    return dict(job=job, base_sha256=meta['sha256'], worker_sha256=digest.hexdigest(),
                variables=meta['variables'], clauses=meta['clauses']+len(a),
                assumptions=a, target_solver_calls=0)


def lrat_steps(text, nc, assumption_count):
    initial = nc+assumption_count
    ids = {}
    def known(i): return 1 <= i <= initial or i in ids
    steps = []
    for line in text.splitlines():
        if not line.strip() or line.startswith('c '):
            continue
        s = line.split()
        if len(s) < 3:
            raise ValueError('LRAT line')
        old = int(s[0])
        if s[1] == 'd':
            if s[-1] != '0' or any(not known(int(x)) for x in s[2:-1]):
                raise ValueError('LRAT deletion syntax')
            continue  # Retaining proved clauses preserves every RUP inference.
        values = [int(x) for x in s[1:]]
        if old <= nc+assumption_count or old in ids or values.count(0) != 2 or values[-1] != 0:
            raise ValueError('LRAT addition framing/identity')
        cut = values.index(0)
        clause, hints = values[:cut], values[cut+1:-1]
        if any(h <= 0 or not known(h) for h in hints):
            raise ValueError('Only already-defined positive RUP hints are supported; RAT is rejected')
        steps.append(dict(clause=clause, hints=[h if h <= initial else ids[h] for h in hints]))
        ids[old] = nc+assumption_count+len(steps)
    if not steps or steps[-1]['clause']:
        raise ValueError('LRAT must finish with an empty clause')
    return steps


def wrap(job, proof):
    checked_job(job)
    return dict(format='q8-hinted-rup-worker-v1', **job,
                base_sha256=metadata(job['r'])['sha256'],
                catalog_sha256=task_queue.specs()['sha256'], proof=proof)


def verify(directory, worker):
    required = {'format', 'r', 'core_assumptions', 'edge_cube', 'base_sha256', 'catalog_sha256', 'proof'}
    if not isinstance(worker, dict) or set(worker) != required or worker['format'] != 'q8-hinted-rup-worker-v1':
        raise ValueError('Worker certificate schema')
    job = {k: worker[k] for k in ['r', 'core_assumptions', 'edge_cube']}
    a = checked_job(job)
    meta, raw = base_bytes(directory, job['r'])
    if worker['base_sha256'] != meta['sha256'] or worker['catalog_sha256'] != task_queue.specs()['sha256']:
        raise ValueError('Worker certificate provenance')
    del raw
    proof = worker['proof']
    if not isinstance(proof, list):
        raise ValueError('Worker proof')
    needed = set()
    for step in proof:
        if not isinstance(step, dict) or set(step) != {'clause', 'hints'} or not isinstance(step['hints'], list):
            raise ValueError('Worker proof step')
        for h in step['hints']:
            if type(h) is not int or h <= 0:
                raise ValueError('Worker hint')
            if h <= meta['clauses']:
                needed.add(h)
    base = {i: c for i, c in enumerate(basis.read_cnf(Path(directory)/f"q8-r{job['r']}.cnf"), 1) if i in needed}
    certificate.checked_transfer(base, meta['clauses'], meta['variables'], a, proof)
    return meta, base


def join(directory, positive, negative):
    if positive['r'] != negative['r'] or positive['core_assumptions'] != negative['core_assumptions']:
        raise ValueError('Branches belong to different core tasks')
    left, right = positive['edge_cube'], negative['edge_cube']
    if not left or not right or left[:-1] != right[:-1] or left[-1] <= 0 or right[-1] != -left[-1]:
        raise ValueError('Both complementary physical edge branches required')
    meta, base1 = verify(directory, positive)
    _, base2 = verify(directory, negative)
    base1.update(base2)
    job = dict(r=positive['r'], core_assumptions=positive['core_assumptions'], edge_cube=left[:-1])
    proof = certificate.merge_branches(base1, meta['clauses'], meta['variables'], checked_job(job), left[-1],
                                       positive['proof'], negative['proof'])
    return wrap(job, proof)


def as_cover(worker):
    if worker['edge_cube']:
        raise ValueError('A physical child refutation does not close its parent task')
    return dict(format='q8-hinted-rup-cover-v1', r=worker['r'], base_sha256=worker['base_sha256'],
                catalog_sha256=worker['catalog_sha256'], assumptions=worker['core_assumptions'], proof=worker['proof'])


def target(directory, job, model_path):
    a = checked_job(job)
    meta, raw = base_bytes(directory, job['r'])
    del raw
    values, statuses = {}, []
    for line in Path(model_path).read_text().splitlines():
        if line.startswith('s '):
            statuses.append(line)
        if line.startswith('v '):
            for item in line[2:].split():
                x = int(item)
                if x == 0:
                    continue
                if not 1 <= abs(x) <= meta['variables'] or (abs(x) in values and values[abs(x)] != (x > 0)):
                    raise ValueError('Conflicting or out-of-range model literal')
                values[abs(x)] = x > 0
    if statuses != ['s SATISFIABLE'] or set(values) != set(range(1, meta['variables']+1)):
        raise ValueError('Complete exact SAT model required')
    if not all(values[abs(x)] == (x > 0) for x in a):
        raise ValueError('Model violates worker assumptions')
    for c in basis.read_cnf(Path(directory)/f"q8-r{job['r']}.cnf"):
        if not any(values[abs(x)] == (x > 0) for x in c):
            raise ValueError('Model violates complete physical base')
    word = 0
    for k, e in enumerate(basis.EDGES):
        red = values[basis.VARIABLES[e]] if e in basis.VARIABLES else e[0]//4 < job['r']
        word |= int(red) << k
    bad = certificate.mono_witness(43, 5, word)
    if bad is not None:
        raise ValueError('Literal good43 check failed: '+json.dumps(bad))
    return dict(status='VERIFIED_GOOD43', n=43, red_hex=f'{word:0226x}', five_sets_checked=962598,
                worker_job=job, base_sha256=meta['sha256'],
                scope='Physical target; partial-core worker need not have a listed catalog core')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='command', required=True)
    a = sub.add_parser('materialize'); a.add_argument('directory'); a.add_argument('job'); a.add_argument('output')
    a = sub.add_parser('import-lrat'); a.add_argument('directory'); a.add_argument('job'); a.add_argument('lrat'); a.add_argument('output')
    a = sub.add_parser('join'); a.add_argument('directory'); a.add_argument('positive'); a.add_argument('negative'); a.add_argument('output')
    a = sub.add_parser('cover'); a.add_argument('directory'); a.add_argument('worker'); a.add_argument('output')
    a = sub.add_parser('target'); a.add_argument('directory'); a.add_argument('job'); a.add_argument('model'); a.add_argument('output')
    a = p.parse_args()
    def read(path): return json.loads(Path(path).read_text())
    if a.command == 'materialize':
        result = materialize(a.directory, read(a.job), a.output)
    elif a.command == 'import-lrat':
        job = read(a.job); assumptions = checked_job(job); meta = metadata(job['r'])
        result = wrap(job, lrat_steps(Path(a.lrat).read_text(), meta['clauses'], len(assumptions)))
        verify(a.directory, result)
    elif a.command == 'join':
        result = join(a.directory, read(a.positive), read(a.negative))
    elif a.command == 'target':
        result = target(a.directory, read(a.job), a.model)
    else:
        w = read(a.worker); verify(a.directory, w); result = as_cover(w)
        certificate.verify_cover(a.directory, result)
    if a.command != 'materialize':
        with Path(a.output).open('x') as f:
            f.write(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
