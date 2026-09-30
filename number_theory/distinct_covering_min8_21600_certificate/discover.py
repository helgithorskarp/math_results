"""Optional one-prefix floating discovery, followed by exact integer checking.

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
        objective[index] = resource[g] / check.DENOMINATOR
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



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prefix', default='[0,0,0,1,0]',
                        help='JSON phases of a canonical anchor prefix')
    args = parser.parse_args()
    residues = tuple(json.loads(args.prefix))
    if not 1 <= len(residues) <= len(check.ANCHORS):
        raise ValueError('invalid prefix length')
    seen = {}
    for m, a in zip(check.ANCHORS, residues):
        choices = dict(check.canonical_options(m, seen))
        if a not in choices:
            raise ValueError('prefix must be canonical')
        seen = choices[a]
    start = monotonic()
    boxes = discover(residues)
    if boxes is None:
        print('INCONCLUSIVE: this numerical attempt found no exact certificate.')
        return
    Q = check.period(len(residues))
    demand, total, maxima = check.exact_certificate(Q, check.decode_boxes(Q, boxes), residues)
    print(json.dumps({'agent':'six-covering-3','role':'researcher',
                      'prefix':residues,'Q':Q,'boxes':boxes,'demand':demand,
                      'scaled_capacity':total,'scaled_gap':check.DENOMINATOR*demand-total},separators=(',',':')))
    print('EXACT local weighted cut checked; this one-prefix run is not a universal exclusion.')
    print(f'Elapsed seconds: {monotonic() - start:.3f}')


if __name__ == '__main__':
    main()
