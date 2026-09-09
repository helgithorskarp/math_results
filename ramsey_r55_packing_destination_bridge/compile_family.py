"""Physical and task-variable h4035 suffixes for every full bo1 task."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
from support import INDEX, need, parents

def selected_matching(core, wanted):
    unused = set(range(len(core))); result = []
    for u, v in combinations(range(len(core)), 2):
        if u in unused and v in unused and (core[u] >> v) & 1:
            result.append((u,v)); unused.remove(u); unused.remove(v)
    need(len(result) >= wanted, 'selected matching')
    return result[:wanted]

def physical_suffix(q, r, core):
    """903-variable positive-RED vocabulary; no auxiliary variables."""
    if q not in (8, 9): return
    m = selected_matching(core, 4 if q == 8 else 2)
    for b in range(r):
        block = list(range(4*b, 4*b+4))
        for e, f in combinations(m, 2):
            for s in combinations(block, 2):
                t = [x for x in block if x not in s]
                yield tuple(-INDEX[tuple(sorted((u, 4*q+v)))]
                            for part, edge in ((s,e), (t,f)) for u in part for v in edge)

def local_suffix(task):
    from support import PAIRS
    for clause in physical_suffix(task.q, task.r, task.core):
        yield tuple(-task.variables[PAIRS[-v-1]] for v in clause)

def compile_task(name, cache, path=None):
    ordered, _, _ = parents()
    task, plan, old = ordered.build(name, cache, False)
    suffix = list(local_suffix(task))
    h = hashlib.sha256(); old_hash = hashlib.sha256(); count = 0; size = 0
    handle = None if path is None else Path(path).open('xb')
    def emit(raw):
        nonlocal size
        size += len(raw); h.update(raw)
        if handle is not None: handle.write(raw)
    old_header = f"p cnf {old['variables']} {old['clauses']}\n".encode()
    old_hash.update(old_header)
    emit(f"p cnf {old['variables']} {old['clauses']+len(suffix)}\n".encode())
    try:
        for clause in ordered.clauses(task, plan, old):
            raw = (' '.join(map(str,clause)) + ' 0\n').encode()
            emit(raw); old_hash.update(raw); count += 1
        need(count == old['clauses'], 'base clause count')
        for clause in suffix:
            emit((' '.join(map(str,clause)) + ' 0\n').encode()); count += 1
    finally:
        if handle is not None: handle.close()
    return {'task': name, 'variables': old['variables'], 'clauses': count,
            'added_clauses': len(suffix), 'added_variables': 0, 'bytes': size,
            'sha256': h.hexdigest(), 'upstream_cnf_sha256': old_hash.hexdigest(),
            'scope': 'NEW_GLOBAL_COVER_NOT_A_FIXED_TASK_RAMSEY_IMPLICATE'}

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('cache'); p.add_argument('--task', required=True)
    p.add_argument('--cnf'); p.add_argument('--physical-suffix', action='store_true'); args = p.parse_args()
    if args.physical_suffix:
        ordered, _, _ = parents(); task, _, _ = ordered.build(args.task, args.cache, False)
        answer = {'task': args.task, 'clauses': list(physical_suffix(task.q, task.r, task.core)),
                  'scope': 'NEW_GLOBAL_COVER_NOT_A_FIXED_TASK_RAMSEY_IMPLICATE'}
    else: answer = compile_task(args.task, args.cache, args.cnf)
    print(json.dumps(answer, indent=2, sort_keys=True))
