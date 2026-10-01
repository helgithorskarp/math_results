"""Optional Glucose4 calibration regeneration; python-sat==1.8.dev24.
All negative decisions receive forward-RUP checks before being written.
A proof-size guard is incomplete certification, never an exclusion.
"""
import sys, json, time, hashlib
from pathlib import Path
from contact import Tile, check_patch, require
from local import compile_cnf, dimacs
from rup import RupChecker
from pysat.solvers import Glucose4
here = Path(__file__).resolve().parent
raw = json.loads((here / 'cases.json').read_text())
tile = Tile(raw['published_heptominoes'][2])

def encode(ps):
    return [[o, str(x), str(y)] for o, x, y in ps]

def verified_trace(cnf, nv):
    with Glucose4(bootstrap_with=cnf, with_proof=True) as s:
        sat = s.solve()
        if sat:
            return (True, s.get_model(), None)
        trace = '\n'.join(s.get_proof()) + '\n' if s.get_proof() else '0\n'
    require(len(trace.encode()) < 1000000, 'proof size guard; incomplete certification')
    check = RupChecker(cnf, nv)
    small = check.verify(trace, capture=True)['trimmed']
    RupChecker(cnf, nv).verify(small)
    return (False, None, small)
pool, cnf, nv = compile_cnf(tile, [tile.root], 2)
allowed = set()
positive = []
with Glucose4(bootstrap_with=cnf) as solver:
    for i in range(1, len(pool) + 1):
        if i in allowed:
            continue
        if solver.solve(assumptions=[i]):
            selected = {x for x in solver.get_model() if 0 < x <= len(pool)}
            poses = [tile.root] + [pool[j - 1][0] for j in sorted(selected)]
            check_patch(tile, [tile.root], poses, scale=2)
            positive.append(encode(poses))
            allowed |= selected
negative = sorted(set(range(1, len(pool) + 1)) - allowed)
checker = RupChecker(cnf, nv)
deps = {}
added = {}
ends = []

def add_conditional(clause):
    clause = list(dict.fromkeys(clause))
    ok, used = checker.rup(clause)
    require(ok, 'non-RUP conditional step')
    cid = checker.add(clause)
    deps[cid] = used
    added[cid] = clause
    return cid
for i in negative:
    if checker.rup([-i])[0]:
        ends.append(add_conditional([-i]))
        continue
    sat, model, proof = verified_trace(checker.clauses + [[i]], nv)
    require(not sat, 'support exclusion unexpectedly SAT')
    for line in proof.splitlines():
        clause = list(map(int, line.split()))[:-1]
        cid = add_conditional([-i] + clause)
    ends.append(cid)
needed = set(ends)
pending = list(ends)
while pending:
    for d in deps[pending.pop()]:
        if d not in needed:
            needed.add(d)
            pending.append(d)
trace = ''.join((' '.join(map(str, added[c])) + ' 0\n' for c in sorted(needed)))
(here / 'support.rup').write_text(trace)
F = sorted({(pool[i - 1][0][0], int(2 * pool[i - 1][0][1]), int(2 * pool[i - 1][0][2])) for i in allowed})
reciprocal = [t for t in F if tile.relative_type(tile.pose(t), tile.root) in F]
result = {'shape_index': 2, 'F': F, 'first_witnesses': positive, 'root_cnf_sha256': hashlib.sha256(dimacs(cnf, nv)).hexdigest(), 'support_proof_sha256': hashlib.sha256(trace.encode()).hexdigest(), 'support_proof_steps': len(needed), 'pairs': []}
print('certified first support', len(F), len(reciprocal), 'proof', len(trace.encode()), flush=True)
for k, ty in enumerate(reciprocal):
    start = time.monotonic()
    fixed = [tile.root, tile.pose(ty)]
    p, c, n = compile_cnf(tile, fixed, 4)
    sat, model, proof = verified_trace(c, n)
    record = {'type': ty, 'sat': sat, 'cnf_sha256': hashlib.sha256(dimacs(c, n)).hexdigest()}
    if sat:
        poses = fixed + [p[j - 1][0] for j in model if 0 < j <= len(p)]
        check_patch(tile, fixed, poses, scale=4)
        record['poses'] = encode(poses)
    else:
        fname = 'pair-%02d.rup' % k
        (here / fname).write_text(proof)
        record['proof'] = fname
        record['proof_sha256'] = hashlib.sha256(proof.encode()).hexdigest()
    result['pairs'].append(record)
    print('pair', k, sat, 'bytes', 0 if proof is None else len(proof.encode()), 'secs', time.monotonic() - start, flush=True)
E1 = {tuple(r['type']) for r in result['pairs'] if r['sat']}
require(all((x % 2 == y % 2 == 0 for o, x, y in E1)), 'not integer-only domain')
p, c, n = compile_cnf(tile, [tile.root], 1, E1)
sat, model, proof = verified_trace(c, n)
require(not sat, 'root survives E1; no upper-one certificate')
(here / 'root-E1.rup').write_text(proof)
result['final_root'] = {'scale': 1, 'pool': len(p), 'clauses': len(c), 'variables': n, 'cnf_sha256': hashlib.sha256(dimacs(c, n)).hexdigest(), 'proof_sha256': hashlib.sha256(proof.encode()).hexdigest()}
(here / 'calibration.json').write_text(json.dumps(result, indent=2) + '\n')
print('complete', len(E1), 'root', len(p), len(c), 'proof', len(proof.encode()), flush=True)
