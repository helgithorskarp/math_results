"""Optional floating discovery; only exact integer checks prune branches.

Author: six-covering-3, researcher. Uses six-covering-2's published quotient
at ../distinct_covering_residual_weight_duals/orbits.py. The checker and
audit import no orbit code, NumPy, SciPy or solver.
"""
from functools import reduce
from math import gcd
from pathlib import Path
from time import monotonic
import argparse
import importlib.util
import json
import os
import warnings
import check

for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[variable] = '1'

spec = importlib.util.spec_from_file_location(
    'published_stabilizer_orbits',
    Path(__file__).resolve().parent.parent / 'distinct_covering_residual_weight_duals/orbits.py')
orbits = importlib.util.module_from_spec(spec)
spec.loader.exec_module(orbits)


def discover(residues, time_limit=2):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    Q = check.period(len(residues))
    anchors = list(zip(check.ANCHORS, residues))
    resource = check.coefficients(Q, check.ANCHORS[:len(residues)])
    groups, rows = orbits.quotient_rows(Q, anchors, sorted(resource))
    count = len(groups)
    offsets = {g: count + i for i, g in enumerate(sorted(resource))}
    rr, cc, vv = [], [], []
    for i, (g, key, terms) in enumerate(rows):
        for j, value in terms.items():
            rr.append(i)
            cc.append(j)
            vv.append(value)
        rr.append(i)
        cc.append(offsets[g])
        vv.append(-1)
    shape = len(rows), count + len(resource)
    matrix = coo_matrix((vv, (rr, cc)), shape=shape).tocsr()
    equality = coo_matrix(([len(o) for o in groups], ([0] * count, list(range(count)))),
                          shape=(1, shape[1])).tocsr()
    objective = np.zeros(shape[1])
    for g, index in offsets.items():
        objective[index] = resource[g] / 4
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', message='Unrecognized options detected')
        answer = linprog(objective, A_ub=matrix, b_ub=np.zeros(len(rows)),
                         A_eq=equality, b_eq=[1], bounds=(0, None), method='highs',
                         options={'threads': 1, 'time_limit': time_limit,
                                  'primal_feasibility_tolerance': 1e-9,
                                  'dual_feasibility_tolerance': 1e-9})
    # Solver status or objective never supplies a mathematical cut.
    if answer.x is None or (answer.fun is not None and answer.fun > 1.000000001):
        return None
    for scale in (1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000):
        values = [max(0, int(round(float(value) * scale))) for value in answer.x[:count]]
        common = reduce(gcd, values, 0)
        if common:
            values = [value // common for value in values]
        vector = [0] * Q
        for group, value in zip(groups, values):
            for x in group:
                vector[x] = value
        try:
            check.exact_certificate(Q, vector, residues)
        except ValueError:
            continue
        boxes = orbits.boxes_from_weights(Q, anchors,
                                          {x: w for x, w in enumerate(vector) if w})
        decoded = check.decode_boxes(Q, boxes)
        if decoded != vector:
            raise RuntimeError('discovery box encoding changes point weights')
        check.exact_certificate(Q, decoded, residues)
        return boxes
    return None


def generate(seconds=45, max_nodes=10000, max_solves=1000):
    certificates = []
    nodes, solves = 0, 0
    start = monotonic()
    def visit(depth, U, seen, residues):
        nonlocal nodes, solves
        if nodes >= max_nodes or monotonic() - start > seconds:
            raise check.IncompleteSearch('discovery node/time budget reached')
        nodes += 1
        Q = check.period(depth)
        if not U:
            raise RuntimeError('an anchor prefix covers')
        vector = [int(bool(U >> x & 1)) for x in range(Q)]
        total, maxima = check.capacity(Q, vector, check.coefficients(Q, check.ANCHORS[:depth]))
        if total <= 4 * sum(vector):
            return
        if depth >= 5:
            if solves >= max_solves:
                raise check.IncompleteSearch('discovery LP-count budget reached')
            solves += 1
            boxes = discover(residues)
            if boxes is not None:
                certificates.append([list(residues), Q, boxes])
                return
        if depth == len(check.ANCHORS):
            raise RuntimeError(f'discovery left an uncertified branch: {residues}')
        R = check.period(depth + 1)
        base = U if Q == R else check.lift(U, Q, R)
        m = check.ANCHORS[depth]
        for a, following in check.canonical_options(m, seen):
            visit(depth + 1, base & ~check.class_mask(R, m, a), following, residues + (a,))
    visit(0, (1 << check.period(0)) - 1, {}, ())
    certificates.sort(key=lambda row: tuple(row[0]))
    return certificates, nodes, solves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True,
                        help='write a complete candidate certificate file')
    args = parser.parse_args()
    start = monotonic()
    certificates, nodes, solves = generate()
    header = json.dumps({'format_version': 1,
                         'axes_by_period': {str(Q): list(a) for Q, a in check.AXES.items()}})[:-1]
    output = header + ',"certificates":[\n' + ',\n'.join(
        json.dumps(c, separators=(',', ':')) for c in certificates) + '\n]}\n'
    args.out.write_text(output)
    result = check.search(args.out)
    print(f'COMPLETE: {nodes} nodes, {solves} LP calls, {len(certificates)} exact certificates.')
    print('Solver-free replay passed; events SHA256:', result['proof_events_sha256'])
    print('Certificate SHA256:', result['weights_file_sha256'])
    print(f'Elapsed seconds: {monotonic() - start:.3f}')


if __name__ == '__main__':
    main()
