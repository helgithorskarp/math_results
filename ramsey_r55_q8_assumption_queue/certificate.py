"""Hinted RUP deduction and fail-closed q8 task admission. No solver invocation."""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re

import basis
import task_queue


def literals(a, nv):
    if not isinstance(a, list) or any(type(x) is not int or x == 0 or abs(x) > nv for x in a):
        raise ValueError('Literal list')
    if len(set(a)) != len(a):
        raise ValueError('Duplicate literal')
    return a


def rup(clause, hints, database, nv):
    literals(clause, nv)
    if not isinstance(hints, list) or any(type(i) is not int or i <= 0 or i not in database for i in hints):
        raise ValueError('Unknown, forward or noninteger hint ID')
    values = {}
    for lit in clause:
        v, value = abs(lit), lit < 0
        if v in values and values[v] != value:
            return True  # Tautology: negated conclusion is inconsistent.
        values[v] = value
    for h in hints:
        c = database[h]
        if any(abs(x) in values and values[abs(x)] == (x > 0) for x in c):
            continue
        free = [x for x in c if abs(x) not in values]
        if not free:
            return True
        if len(free) != 1:
            raise ValueError('Hint is not unit or conflicting')
        values[abs(free[0])] = free[0] > 0
    return False


def verify_steps(base, nc, nv, assumptions, steps, final):
    literals(assumptions, nv)
    if len({abs(x) for x in assumptions}) != len(assumptions):
        raise ValueError('Inconsistent or duplicate assumption')
    if not isinstance(steps, list) or not steps:
        raise ValueError('Nonempty proof required')
    db = dict(base)
    for i, a in enumerate(assumptions, nc+1):
        db[i] = [a]
    for i, step in enumerate(steps, nc+len(assumptions)+1):
        if not isinstance(step, dict) or set(step) != {'clause', 'hints'}:
            raise ValueError('Proof step schema')
        if not rup(step['clause'], step['hints'], db, nv):
            raise ValueError('No RUP conflict')
        db[i] = step['clause']
    if steps[-1]['clause'] != final:
        raise ValueError('Wrong terminal conclusion')
    return True


def lift(nc, assumptions, steps):
    """Discharge assumptions; each output lemma is a consequence of the base."""
    guard = [-x for x in assumptions]
    n = len(assumptions)
    result = []
    for step in steps:
        hints = [i if i <= nc else i-n for i in step['hints'] if not nc < i <= nc+n]
        result.append(dict(clause=sorted(set(step['clause']+guard)), hints=hints))
    return result


def checked_transfer(base, nc, nv, a, proof):
    verify_steps(base, nc, nv, a, proof, [])
    lifted = lift(nc, a, proof)
    conclusion = sorted(-x for x in a)
    verify_steps(base, nc, nv, [], lifted, conclusion)
    return lifted


def merge_branches(base, nc, nv, a, variable, positive, negative):
    """Join two complete physical edge branches into one parent refutation."""
    if type(variable) is not int or not 1 <= variable <= nv or variable in {abs(x) for x in a}:
        raise ValueError('Fresh branch variable')
    left = checked_transfer(base, nc, nv, a+[variable], positive)
    right = checked_transfer(base, nc, nv, a+[-variable], negative)
    result = []
    for offset, proof in [(len(a), left), (len(a)+len(left), right)]:
        for step in proof:
            result.append(dict(clause=step['clause'], hints=[i if i <= nc else i+offset for i in step['hints']]))
    first_last = nc+len(a)+len(left)
    second_last = nc+len(a)+len(left)+len(right)
    result.append(dict(clause=[], hints=list(range(nc+1, nc+len(a)+1))+[first_last, second_last]))
    checked_transfer(base, nc, nv, a, result)
    return result


def verify_cover(directory, cert):
    """Verify against the published, audited base identity, then determine IDs."""
    required = {'format', 'r', 'base_sha256', 'catalog_sha256', 'assumptions', 'proof'}
    if not isinstance(cert, dict) or set(cert) != required or cert['format'] != 'q8-hinted-rup-cover-v1':
        raise ValueError('Cover certificate schema')
    r = basis.checked_r(cert['r'])
    task_queue.match_mask(cert['assumptions'])
    expected = json.loads((basis.HERE/'EXPECTED.json').read_text())
    meta = expected['bases'][str(r)]
    if cert['base_sha256'] != meta['sha256'] or cert['catalog_sha256'] != task_queue.specs()['sha256']:
        raise ValueError('Wrong physical formula or catalog identity')
    d = Path(directory)
    path = d/f'q8-r{r}.cnf'
    digest = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            digest.update(chunk)
    if digest.hexdigest() != meta['sha256']:
        raise ValueError('Actual base bytes differ from audited input')
    needed = set()
    if not isinstance(cert['proof'], list):
        raise ValueError('Proof list')
    for step in cert['proof']:
        if not isinstance(step, dict) or set(step) != {'clause', 'hints'} or not isinstance(step['hints'], list):
            raise ValueError('Proof step schema')
        for h in step['hints']:
            if type(h) is not int or h <= 0:
                raise ValueError('Hint ID')
            if h <= meta['clauses']:
                needed.add(h)
    base = {i: c for i, c in enumerate(basis.read_cnf(path), 1) if i in needed}
    lifted = checked_transfer(base, meta['clauses'], meta['variables'], cert['assumptions'], cert['proof'])
    core_path = d/'cores.u64le'
    if hashlib.sha256(core_path.read_bytes()).hexdigest() != expected['queue']['files']['cores.u64le']['sha256']:
        raise ValueError('Actual queue core stream differs from audited input')
    words = task_queue.read_words(core_path)
    indices = task_queue.matching(words, cert['assumptions'])
    digest = hashlib.sha256()
    for c in indices:
        digest.update(f'bo1-q8-r{r}-c{c:06d}\n'.encode())
    mask, value = task_queue.match_mask(cert['assumptions'])
    return dict(status='CERTIFIED_TASK_COVER' if indices else 'VERIFIED_EMPTY_COVER',
                r=r, matching_tasks=len(indices), task_ids_sha256=digest.hexdigest(),
                core_mask=f'{mask:014x}', core_value=f'{value:014x}',
                conclusion=lifted[-1]['clause'], original_steps=len(cert['proof']),
                lifted_steps=len(lifted), base_sha256=meta['sha256'], good43=False)


def mono_witness(n, k, word):
    pairs = list(combinations(range(n), 2))
    a = {e: bool(word >> j & 1) for j, e in enumerate(pairs)}
    for vertices in combinations(range(n), k):
        colors = {a[e] for e in combinations(vertices, 2)}
        if len(colors) == 1:
            return dict(vertices=list(vertices), red=next(iter(colors)))
    return None


def accept_target(directory, name, red_hex):
    r, c = task_queue.parameters(name)
    if not isinstance(red_hex, str) or not re.fullmatch('[0-9a-f]{226}', red_hex):
        raise ValueError('Exact lowercase 226-hex physical43 word required')
    word = int(red_hex, 16)
    if word >= 1 << 903:
        raise ValueError('Nonzero physical word padding')
    edges = {e: (word >> k) & 1 for k, e in enumerate(combinations(range(43), 2))}
    core_word = sum(edges[i+32, j+32] << k for k, (i, j) in enumerate(combinations(range(11), 2)))
    d = Path(directory)
    expected = json.loads((basis.HERE/'EXPECTED.json').read_text())
    path = d/'cores.u64le'
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected['queue']['files']['cores.u64le']['sha256']:
        raise ValueError('Audited queue identity')
    if task_queue.read_words(path)[c] != core_word:
        raise ValueError('Wrong task core')
    matrices = []
    for b in range(8):
        if any(edges[e] != int(b < r) for e in combinations(range(4*b, 4*b+4), 2)):
            raise ValueError('Wrong fixed block')
        if b:
            columns = [sum(edges[u, 4*b+v] << u for u in range(4)) for v in range(4)]
            if columns != sorted(columns, reverse=True):
                raise ValueError('Root column order')
            matrices.append(sum(edges[u, 4*b+v] << (4*u+v) for u in range(4) for v in range(4)))
    for a, b in basis.comparisons(r):
        if matrices[a-1] < matrices[b-1]:
            raise ValueError('Whole-block order')
    for vertices in combinations(range(4*r, 43), 4):
        if all(edges[e] for e in combinations(vertices, 2)):
            raise ValueError('Red maximality')
    bad = mono_witness(43, 5, word)
    if bad is not None:
        raise ValueError('Physical monochromatic five: '+json.dumps(bad))
    return dict(status='VERIFIED_GOOD43', task=name, n=43, red_hex=red_hex, five_sets_checked=962598)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='command', required=True)
    a = sub.add_parser('cover'); a.add_argument('directory'); a.add_argument('certificate')
    a = sub.add_parser('target'); a.add_argument('directory'); a.add_argument('task'); a.add_argument('red_hex')
    a = p.parse_args()
    result = verify_cover(a.directory, json.loads(Path(a.certificate).read_text())) if a.command == 'cover' else accept_target(a.directory, a.task, a.red_hex)
    print(json.dumps(result, indent=2))
