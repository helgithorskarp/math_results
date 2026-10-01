"""Optional exact phase-lock certificates, PySAT1.8.dev24 / Glucose4.

One solver at a time. UNKNOWN, guards and interrupted runs are incomplete.
"""
import hashlib
import json
from pathlib import Path
import resource
import time
from compact import compile_subset
from contact import Tile, require, check_patch
from local import compile_cnf, dimacs
from rup import RupChecker
from pysat.solvers import Glucose4

HERE = Path(__file__).resolve().parent


def encode(poses):
    return [[o, str(x), str(y)] for o, x, y in poses]


def checked_proof(cnf, nv):
    with Glucose4(bootstrap_with=cnf, with_proof=True) as solver:
        solver.conf_budget(200000)
        status = solver.solve_limited()
        require(status is False, 'SAT or UNKNOWN: no negative certificate')
        # Keeping all previously justified clauses makes deletions unnecessary
        # for forward RUP. Filter deletion-only logs before the compact limit.
        lines = [line for line in solver.get_proof() if not line.startswith('d ')]
    trace = '\n'.join(lines)+'\n' if lines else '0\n'
    require(len(trace.encode()) <= 250000, 'raw proof guard: incomplete certification')
    trimmed = RupChecker(cnf, nv).verify(trace, capture=True)['trimmed']
    RupChecker(cnf, nv).verify(trimmed)
    return trimmed


def main():
    start = time.monotonic()
    data = json.loads((HERE/'input.json').read_text())
    tile = Tile(data['cells'])
    pool, cnf, nv = compile_cnf(tile, [tile.root], 2)
    require(len(pool) <= 1000 and len(cnf) <= 160000,
            'first formula guard: incomplete certification')
    floating = {i for i, (p, pixels) in enumerate(pool, 1)
                if (p[1] % 1) or (p[2] % 1)}
    supported, witnesses = set(), []
    with Glucose4(bootstrap_with=cnf) as solver:
        for i in sorted(floating):
            if i in supported:
                continue
            solver.conf_budget(200000)
            status = solver.solve_limited(assumptions=[i])
            require(status is not None, 'UNKNOWN: first support incomplete')
            if status:
                selected = sorted(v for v in solver.get_model() if 0 < v <= len(pool))
                poses = [tile.root]+[pool[v-1][0] for v in selected]
                check_patch(tile, [tile.root], poses, scale=2)
                witnesses.append(encode(poses))
                supported.update(set(selected) & floating)
    checker = RupChecker(cnf, nv)
    dependencies, added, endings = {}, {}, []

    def add(clause):
        clause = list(dict.fromkeys(clause))
        ok, used = checker.rup(clause)
        require(ok, 'invalid conditional RUP clause')
        cid = checker.add(clause)
        dependencies[cid], added[cid] = used, clause
        return cid

    solver_calls = 0
    for count, i in enumerate(sorted(floating-supported), 1):
        if checker.rup([-i])[0]:
            endings.append(add([-i]))
        else:
            proof = checked_proof(checker.clauses+[[i]], nv)
            solver_calls += 1
            for line in proof.splitlines():
                clause = list(map(int, line.split()))[:-1]
                cid = add([-i]+clause)
            endings.append(cid)
        if count % 50 == 0:
            print('checked floating exclusions', count, 'solver calls', solver_calls,
                  'seconds', round(time.monotonic()-start, 2), flush=True)
    needed, pending = set(endings), list(endings)
    while pending:
        for dep in dependencies[pending.pop()]:
            if dep not in needed:
                needed.add(dep)
                pending.append(dep)
    trace = ''.join(' '.join(map(str, added[cid]))+' 0\n' for cid in sorted(needed))
    require(len(trace.encode()) <= 100000, 'trimmed support guard: incomplete certification')
    (HERE/'floating-support.rup').write_text(trace)
    support_types = sorted((pool[i-1][0][0], int(2*pool[i-1][0][1]),
                            int(2*pool[i-1][0][2])) for i in supported)
    reciprocal = [t for t in support_types
                  if tile.relative_type(tile.pose(t), tile.root) in support_types]
    require(reciprocal == [tuple(data['exceptional_floating_type'])],
            'exceptional pair list changed')
    fixed = [tile.root, tile.pose(reciprocal[0])]
    p, c, n = compile_subset(tile, fixed, 4, data['quarter_grid_core_target'])
    proof = checked_proof(c, n)
    (HERE/'exceptional-pair.rup').write_text(proof)
    result = {
        'first_formula_sha256': hashlib.sha256(dimacs(cnf, nv)).hexdigest(),
        'floating_support': support_types, 'first_witnesses': witnesses,
        'support_proof_sha256': hashlib.sha256(trace.encode()).hexdigest(),
        'support_proof_steps': len(needed),
        'exceptional_pair': {'type': reciprocal[0], 'pool': len(p), 'clauses': len(c),
                             'nv': n, 'cnf_sha256': hashlib.sha256(dimacs(c, n)).hexdigest(),
                             'proof_sha256': hashlib.sha256(proof.encode()).hexdigest()}}
    (HERE/'certificate.json').write_text(json.dumps(result, indent=2)+'\n')
    print({'floating': len(floating), 'floating_support': len(supported),
           'reciprocal_floating_support': len(reciprocal), 'core_pool': len(p),
           'core_clauses': len(c), 'support_proof_bytes': len(trace.encode()),
           'pair_proof_bytes': len(proof.encode()), 'seconds': time.monotonic()-start,
           'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, flush=True)


if __name__ == '__main__':
    main()
