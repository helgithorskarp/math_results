"""Exhaustive semantic controls and full-base certificate plumbing checks."""
import argparse
import copy
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

import basis
import certificate as cert
import task_queue
import cohorts
import worker


def truth(clause, word):
    return any(bool(word >> (abs(x)-1) & 1) == (x > 0) for x in clause)


def conflict_trace(database, decisions):
    values = {abs(x): x > 0 for x in decisions}
    hints = []
    while True:
        changed = False
        for i, clause in database.items():
            if any(abs(x) in values and values[abs(x)] == (x > 0) for x in clause):
                continue
            free = [x for x in clause if abs(x) not in values]
            if not free:
                return hints+[i], values
            if len(free) == 1:
                values[abs(free[0])] = free[0] > 0
                hints.append(i)
                changed = True
        if not changed:
            return None, values


def derive(base, nv, assumptions):
    """Tiny exhaustive DPLL producer, used only on two-variable controls."""
    nc = len(base)
    db = dict(base)
    for i, a in enumerate(assumptions, nc+1):
        db[i] = [a]
    steps = []
    def visit(decisions):
        hints, values = conflict_trace(db, decisions)
        if hints is None:
            unassigned = [v for v in range(1, nv+1) if v not in values]
            if not unassigned:
                return False
            v = unassigned[0]
            if not visit(decisions+[v]) or not visit(decisions+[-v]):
                return False
            hints, _ = conflict_trace(db, decisions)
            if hints is None:
                raise ValueError('Resolution of child conflicts failed')
        step = dict(clause=[-x for x in decisions], hints=hints)
        steps.append(step)
        db[nc+len(assumptions)+len(steps)] = step['clause']
        return True
    return steps if visit([]) else None


def exhaustive():
    clauses = [[(v+1)*s for v, s in enumerate(signs) if s] for signs in product((-1, 0, 1), repeat=2)]
    assumption_sets = clauses
    checked = unsat = guarded = 0
    for mask in range(1 << len(clauses)):
        formula = [c for i, c in enumerate(clauses) if mask >> i & 1]
        base = {i+1: c for i, c in enumerate(formula)}
        for a in assumption_sets:
            models = [w for w in range(4) if all(truth(c, w) for c in formula) and all(truth([x], w) for x in a)]
            proof = derive(base, 2, a)
            if (proof is None) != bool(models):
                raise ValueError('DPLL disagrees with full truth table')
            checked += 1
            if proof is not None:
                lifted = cert.checked_transfer(base, len(base), 2, a, proof)
                unsat += 1; guarded += len(lifted)
                for w in range(4):
                    if all(truth(c, w) for c in formula) and not truth(lifted[-1]['clause'], w):
                        raise ValueError('Transferred clause is not entailed')
    good = 0
    for word in range(1024):
        a = [[False]*5 for _ in range(5)]
        for k, (i, j) in enumerate(combinations(range(5), 2)):
            a[i][j] = a[j][i] = bool(word >> k & 1)
        direct_bad = any(a[i][j] == a[i][k] == a[j][k] for i, j, k in combinations(range(5), 3))
        if (cert.mono_witness(5, 3, word) is not None) != direct_bad:
            raise ValueError('Literal graph checker control')
        good += not direct_bad
    if good != 12:
        raise ValueError('R(3,3) five-vertex control count')
    return dict(two_variable_formula_assumption_cases=checked, complete_refutations=unsat,
                guarded_lemmas_checked=guarded, literal_graph_controls=1024, good_R33_order5=good)


def rejection(function):
    try:
        function()
    except (ValueError, KeyError, TypeError):
        return True
    raise ValueError('Corruption was accepted')


def proof_controls():
    # Under a=b=1 the four clauses form an unsatisfiable two-variable square.
    base = {1: [-3, -4, 1, 2], 2: [-3, -4, 1, -2],
            3: [-3, -4, -1, 2], 4: [-3, -4, -1, -2]}
    proof = [dict(clause=[1], hints=[5, 6, 1, 2]),
             dict(clause=[], hints=[5, 6, 7, 3, 4])]
    lifted = cert.checked_transfer(base, 4, 4, [3, 4], proof)
    if lifted[-1]['clause'] != [-4, -3]:
        raise ValueError('Nontrivial guard conclusion')
    tests = []
    bad = copy.deepcopy(proof); bad[-1]['hints'] = [5, 6, 7, 3]
    tests.append(rejection(lambda: cert.checked_transfer(base, 4, 4, [3, 4], bad)))
    tests.append(rejection(lambda: cert.checked_transfer(base, 4, 4, [3, -3], proof)))
    tests.append(rejection(lambda: cert.checked_transfer(base, 4, 4, [3], proof)))
    tests.append(rejection(lambda: cert.checked_transfer(base, 4, 4, [3, 4], proof[:-1])))
    forward = copy.deepcopy(proof); forward[0]['hints'] = [7]
    tests.append(rejection(lambda: cert.checked_transfer(base, 4, 4, [3, 4], forward)))
    wrong = copy.deepcopy(proof); wrong[0]['clause'] = [-1]
    tests.append(rejection(lambda: cert.checked_transfer(base, 4, 4, [3, 4], wrong)))
    tests.append(rejection(lambda: cert.verify_steps(base, 4, 4, [], proof, [])))
    tests.append(rejection(lambda: cert.verify_steps({}, 0, 1, [], [dict(clause=[1], hints=[])], [1])))
    positive = [dict(clause=[], hints=[5, 6, 7, 3, 4])]
    negative = [dict(clause=[], hints=[5, 6, 7, 1, 2])]
    merged = cert.merge_branches(base, 4, 4, [3, 4], 1, positive, negative)
    tests.append(rejection(lambda: cert.merge_branches(base, 4, 4, [3, 4], 1, negative, positive)))
    # This last test detects the unsound operation of deleting assumptions
    # while exporting the original unguarded proof to a different task.
    return dict(nontrivial_projection=lifted, proof_corruptions_rejected=len(tests),
                complete_binary_branch_join=merged)


def cohort_controls():
    words = list(range(16))
    tree = cohorts.partition(words, 3)
    result = cohorts.audit(words, tree)
    bad = copy.deepcopy(tree); bad['nodes'][0]['one'] = bad['nodes'][0]['zero']
    rejection(lambda: cohorts.audit(words, bad))
    bad = copy.deepcopy(tree); bad['nodes'][-1]['count'] += 1
    rejection(lambda: cohorts.audit(words, bad))
    bad = copy.deepcopy(tree); bad['nodes'][0]['mask'] = '00000000000001'
    rejection(lambda: cohorts.audit(words, bad))
    bad = copy.deepcopy(tree); bad['leaves'] = bad['leaves'][1:]
    rejection(lambda: cohorts.audit(words, bad))
    return dict(small_partition=result, corruptions_rejected=4)


def worker_controls():
    text = '20 1 0 5 6 1 2 0\n21 d 1 2 0\n30 0 5 6 20 3 4 0\n'
    steps = worker.lrat_steps(text, 4, 2)
    base = {1: [-3, -4, 1, 2], 2: [-3, -4, 1, -2], 3: [-3, -4, -1, 2], 4: [-3, -4, -1, -2]}
    cert.checked_transfer(base, 4, 4, [3, 4], steps)
    bad = ['20 1 0 -1 0\n30 0 20 0\n', '20 1 0 30 0\n30 0 20 0\n',
           '20 1 0 5 6 1 2 0\n', '20 1 0 5 6 1 2 0\n20 0 20 0\n']
    for text in bad:
        rejection(lambda text=text: worker.lrat_steps(text, 4, 2))
    rejection(lambda: worker.checked_job(dict(r=5, core_assumptions=[802], edge_cube=[2, -2])))
    rejection(lambda: worker.checked_job(dict(r=10, core_assumptions=[802], edge_cube=[])))
    rejection(lambda: worker.as_cover(dict(edge_cube=[2])))
    return dict(positive_hint_lrat_import=True, deletion_ignored_soundly=True, corruptions_rejected=7)


def model_controls(directory):
    d = Path(directory)
    # Use the actual first cohort, without assuming the integration fixture exists.
    row = cohorts.job(json.loads((d/'cohorts.json').read_text()), 5, 0)
    job = dict(r=5, core_assumptions=row['assumptions'], edge_cube=[])
    nv = worker.metadata(5)['variables']
    cases = [('unknown', 's UNKNOWN\n'), ('partial', 's SATISFIABLE\nv 1 0\n'),
             ('conflicting', 's SATISFIABLE\nv 1 -1 0\n'),
             ('bad_complete', 's SATISFIABLE\nv '+' '.join(str(i if i == 1 else -i) for i in range(1, nv+1))+' 0\n')]
    results = []
    for name, text in cases:
        path = d/('model-control-'+name+'.out')
        path.write_text(text)
        try:
            worker.target(d, job, path)
        except ValueError as e:
            results.append(dict(control=name, rejected=True, reason=str(e)))
        else:
            raise ValueError('Invalid complete-worker model accepted')
    return results


def full_controls(directory):
    d = Path(directory)
    expected = json.loads((basis.HERE/'EXPECTED.json').read_text())
    a = [basis.VARIABLES[e] for e in combinations(range(32, 36), 2)]
    target = tuple(-v for v in a)
    receipts = []
    cert_paths = []
    for r in range(5, 9):
        meta = expected['bases'][str(r)]
        clause_id = None
        for i, clause in enumerate(basis.read_cnf(d/f'q8-r{r}.cnf'), 1):
            if tuple(clause) == target:
                clause_id = i
                break
        if clause_id is None:
            raise ValueError('Physical red4 clause missing')
        c = dict(format='q8-hinted-rup-cover-v1', r=r, base_sha256=meta['sha256'],
                 catalog_sha256=task_queue.specs()['sha256'], assumptions=a,
                 proof=[dict(clause=[], hints=list(range(meta['clauses']+1, meta['clauses']+7))+[clause_id])])
        receipt = cert.verify_cover(d, c)
        if receipt['status'] != 'VERIFIED_EMPTY_COVER' or receipt['matching_tasks'] != 0:
            raise ValueError('No catalog core may contain a red K4')
        receipts.append(receipt)
        path = d/f'empty-cover-control-r{r}.json'
        path.write_text(json.dumps(c, indent=2)+'\n'); cert_paths.append(path)
    # Exercise actual task admission with a valid but empty cover.
    request = task_queue.request('bo1-q8-r5-c000000', d, cert_paths[0])
    if request['status'] != 'UNKNOWN' or len(request['assumptions']) != 55:
        raise ValueError('An empty cover changed a real task')
    wrong = json.loads(cert_paths[0].read_text()); wrong['base_sha256'] = '0'*64
    rejection(lambda: cert.verify_cover(d, wrong))
    wrong = json.loads(cert_paths[0].read_text()); wrong['assumptions'] = [2]
    rejection(lambda: cert.verify_cover(d, wrong))
    wrong = json.loads(cert_paths[0].read_text()); wrong['r'] = 10
    rejection(lambda: cert.verify_cover(d, wrong))
    wrong = json.loads(cert_paths[0].read_text()); wrong['r'] = 6
    rejection(lambda: cert.verify_cover(d, wrong))
    rejected = 4
    for name in ['bo1-q10-r10-c000000', 'bo1-q7-r7-c000000', 'bo1-q9-r5-c000000',
                 'bo1-q8-r4-c000000', 'bo1-q8-r5-c546356', 'bo1-q8-r5-c0']:
        rejection(lambda name=name: task_queue.parameters(name)); rejected += 1
    words = task_queue.read_words(d/'cores.u64le')
    edges = dict.fromkeys(combinations(range(43), 2), 0)
    for b in range(8):
        for e in combinations(range(4*b, 4*b+4), 2):
            edges[e] = 1
    for k, (i, j) in enumerate(combinations(range(32, 43), 2)):
        edges[i, j] = words[0] >> k & 1
    word = sum(edges[e] << k for k, e in enumerate(combinations(range(43), 2)))
    # Fresh carrier assignment: passes core/block/order/maximality, fails I5.
    try:
        cert.accept_target(d, 'bo1-q8-r8-c000000', f'{word:0226x}')
    except ValueError as e:
        if 'Physical monochromatic five' not in str(e):
            raise
    else:
        raise ValueError('Non-target physical carrier accepted')
    for bad in ['0', 'f'*226, 'G'*226]:
        rejection(lambda bad=bad: cert.accept_target(d, 'bo1-q8-r8-c000000', bad)); rejected += 1
    return dict(full_base_checked_empty_covers=receipts, task_admission_status='UNKNOWN',
                actual_task_exclusions=0, actual_candidates=0, admission_corruptions_rejected=rejected,
                full_physical_false_candidate_rejected=True, worker_model_controls=model_controls(d))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--directory'); p.add_argument('--models-only', action='store_true'); a = p.parse_args()
    if a.models_only:
        if not a.directory:
            raise ValueError('Model controls require a complete prepared queue')
        print(json.dumps(model_controls(a.directory), indent=2))
        raise SystemExit(0)
    out = dict(exhaustive=exhaustive(), proof=proof_controls(), cohorts=cohort_controls(), worker=worker_controls())
    if a.directory:
        out['full'] = full_controls(a.directory)
    print(json.dumps(out, indent=2))
