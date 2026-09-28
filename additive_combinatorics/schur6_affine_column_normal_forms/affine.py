"""Affine column parameter orbits and exact compact search encodings.

For odd a coprime to 5, Q2(q)=Q1(lam*q+delta), with lam a unit modulo a.
The unit-dilation parameter orbits are indexed by
  ({lam,-1/lam}, gcd(5*delta+1-2*lam,a)).
This is a classification of specified parameters, not disjoint word sets.
"""
import argparse
import collections
import hashlib
import itertools
import json
import math
import time
from pathlib import Path


def key(a, lam, delta):
    return tuple(sorted({lam % a, -pow(lam, -1, a) % a})), math.gcd(5*delta+1-2*lam, a)


def action(a, lam, delta, u):
    assert math.gcd(a, 10) == 1 and math.gcd(lam, a) == math.gcd(u, 5*a) == 1
    v = u if u % 5 in (1, 2) else -u
    if v % 5 == 1:
        return lam, (v*delta+(1-2*lam)*((v-1)//5)) % a
    inv = pow(lam, -1, a)
    return -inv % a, (inv*v*delta+inv*((v-2)//5)-(2*v+1)//5) % a


def literal_pointer(a, lam, delta, x):
    x %= 5*a
    q, b = divmod(x, 5)
    assert b
    if b > 2:
        q, b = divmod(5*a-x, 5)
    return (q if b == 1 else lam*q+delta) % a, b-1


def orbit_audit(a):
    assert a > 1 and math.gcd(a, 10) == 1
    units_a = [u for u in range(1, a) if math.gcd(u, a) == 1]
    units = [u for u in range(1, 5*a) if math.gcd(u, 5*a) == 1]
    classes = collections.defaultdict(set)
    for lam in units_a:
        for delta in range(a):
            classes[key(a, lam, delta)].add((lam, delta))
    checked = 0
    for invariant, parameters in classes.items():
        lam, delta = min(parameters)
        orbit = set()
        for u in units:
            new_lam, new_delta = action(a, lam, delta, u)
            orbit.add((new_lam, new_delta))
            assert key(a, new_lam, new_delta) == invariant
            inv = pow(u, -1, 5*a)
            swap = u % 5 in (2, 3)
            for q in range(a):
                left = literal_pointer(a, lam, delta, inv*(5*q+2))
                right = literal_pointer(a, lam, delta, inv*(5*((new_lam*q+new_delta) % a)+1))
                assert left[0] == right[0]
                assert (1-left[1] if swap else left[1]) == 1
                assert (1-right[1] if swap else right[1]) == 0
                checked += 1
        assert orbit == parameters
    roots = [u for u in units_a if (u*u+1) % a == 0]
    divisors = [d for d in range(1, a+1) if a % d == 0]
    expected_count = (len(units_a)+len(roots))*len(divisors)//2
    assert len(classes) == expected_count
    assert sum(map(len, classes.values())) == a*len(units_a)
    # The degenerate orbit forces every long-coordinate state residual.
    lam = pow(2, -1, a)
    assert key(a, lam, 0) == key(a, a-2, a-1)
    assert all((lam*(2*q)) % a == q for q in range(a))
    return dict(axis_factor=a, affine_parameters=a*len(units_a), orbits=len(classes),
                orbit_size_histogram={str(size): count for size, count in sorted(collections.Counter(map(len, classes.values())).items())},
                minus_one_square_roots=roots, divisors=divisors,
                symbolic_point_checks=checked, doubling_obstructed_representative=[lam, 0],
                status='AFFINE_PARAMETER_ORBITS_VERIFIED')


def encoding(a, lam, delta, symmetry=True):
    from model import encoding as split_encoding
    assert math.gcd(lam, a) == 1
    m, clauses = split_encoding(a, symmetry=False)
    nvar = m['h']*6+a*5
    projection = {v: v for v in range(1, nvar+1)}
    for q in range(a):
        for c in m['labels']:
            projection[m['Q'][2, q, c]] = m['Q'][1, (lam*q+delta) % a, c]
    cnf = set()
    for clause in clauses:
        image = {(1 if v > 0 else -1)*projection[abs(v)] for v in clause}
        if any(-v in image for v in image):
            continue
        cnf.add(tuple(sorted(image)))
    if symmetry:
        seen = {c: [] for c in m['common']}
        rows = [{c: m['Q'][1, q, c] for c in m['common']} for q in range(a)]
        rows += [{c: m['E'][u, c] for c in m['common']} for u in range(1, m['h']+1)]
        for row in rows:
            for c in m['common'][1:]:
                cnf.add(tuple([-row[c], *seen[c-1]]))
            for c in m['common']:
                seen[c].append(row[c])
    cnf = sorted(cnf, key=lambda cl: (len(cl), cl))
    m.update(affine_variables=nvar, projection=projection, lam=lam, delta=delta)
    return m, cnf


def clause_audit(a, lam, delta):
    # The literal audit builds an independent point table before substituting
    # the affine relation. It does not use the mixed-column criterion.
    from audit import literal_clauses
    from model import criterion_clauses
    m, _ = encoding(a, lam, delta, symmetry=False)
    literal, pairs, _ = literal_clauses(a)
    def project(clauses):
        return {tuple(sorted({-m['projection'][-v] for v in cl})) for cl in clauses}
    actual, expected = project(criterion_clauses(m)), project(literal)
    assert actual == expected
    return dict(axis_factor=a, lam=lam, delta=delta, variables=m['affine_variables'],
                schur_clauses=len(actual), modular_pairs=pairs, status='AFFINE_CLAUSES_MATCH')


def run(a, lam, delta, budget, output):
    from pysat.solvers import Solver
    from model import decode
    from verify import verify_word
    start = time.monotonic()
    m, cnf = encoding(a, lam, delta)
    payload = ('p cnf %d %d\n' % (m['affine_variables'], len(cnf))+
               ''.join(' '.join(map(str, row))+' 0\n' for row in cnf)).encode()
    report = dict(axis_factor=a, short_factor=5, colours=6, lam=lam, delta=delta,
                  variables=m['affine_variables'], clauses=len(cnf), budget=budget,
                  solver='cadical195', cnf_bytes=len(payload),
                  cnf_sha256=hashlib.sha256(payload).hexdigest())
    with Solver(name='cadical195', bootstrap_with=cnf) as solver:
        solver.conf_budget(budget)
        result = solver.solve_limited()
        report.update(status={True: 'SAT', False: 'UNSAT_UNCERTIFIED', None: 'UNKNOWN'}[result],
                      stats=solver.accum_stats())
        if result:
            truth = set(solver.get_model())
            expanded = {v for v, target in m['projection'].items() if target in truth}
            report['word'] = decode(m, expanded)
            report['check'] = verify_word(report)
            from symmetry import columns
            q1, q2 = columns(report['word'])
            assert all(q2[q] == q1[(lam*q+delta) % a] for q in range(a))
    report['seconds'] = time.monotonic()-start
    Path(output).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'word'}), flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output')
    parser.add_argument('--axis-factor', type=int, default=109)
    parser.add_argument('--lam', type=int)
    parser.add_argument('--delta', type=int, default=0)
    parser.add_argument('--budget', type=int, default=100000)
    parser.add_argument('--export-cnf')
    args = parser.parse_args()
    if args.export_cnf:
        if args.lam is None:
            parser.error('--export-cnf needs --lam')
        m, cnf = encoding(args.axis_factor, args.lam, args.delta)
        payload = ('p cnf %d %d\n' % (m['affine_variables'], len(cnf))+
                   ''.join(' '.join(map(str, cl))+' 0\n' for cl in cnf)).encode()
        Path(args.export_cnf).write_bytes(payload)
        print(json.dumps(dict(variables=m['affine_variables'], clauses=len(cnf), bytes=len(payload),
                              sha256=hashlib.sha256(payload).hexdigest())))
    elif args.output and args.lam is not None:
        run(args.axis_factor, args.lam, args.delta, args.budget, args.output)
    elif args.output:
        results = []
        for a in (7, 13, 47, 61, 77, 109):
            record = orbit_audit(a)
            results.append(record)
            print(json.dumps(record), flush=True)
        Path(args.output).write_text(json.dumps(results, indent=2)+'\n')
    else:
        parser.error('provide --output or --export-cnf')
