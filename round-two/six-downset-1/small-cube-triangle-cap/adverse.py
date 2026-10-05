"""Exact new-domain and original-data rejections, with named guard outcomes."""
from source_binding import verify_source as _verify_source
_verify_source()
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
import argparse
import copy
import json
from pathlib import Path
import signal

import geometry
import reader


def main():
    def expire(signum, frame):
        raise TimeoutError('fixed60s adverse child; unfinished is not a rejection')
    signal.signal(signal.SIGALRM, expire)
    signal.alarm(60)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    geometry.barrier()
    reader.require(not args.out.exists(), 'unique new adverse output')
    cases = []

    def rejected(name, action, exact):
        try:
            action()
        except ValueError as error:
            reader.require(str(error) == exact, 'wrong rejection gate for ' + name)
            cases.append({'name': name, 'rejected': True, 'exact_gate': str(error)})
        else:
            raise RuntimeError('accepted designated defect: ' + name)

    for name, n, counts, exact in (
        ('n1 outside proved domain', 1, [5, 4], 'proved small-cube domain and unchanged n<=6'),
        ('boolean old size', True, [5, 4], 'proved small-cube domain and unchanged n<=6'),
        ('one mark outside proof', 2, [9], 'literal distinct count/mark types'),
        ('more marks than old points', 2, [4, 3, 2], 'literal distinct count/mark types'),
        ('boolean count', 2, [5, True], 'literal distinct count/mark types'),
        ('nonunique maximum', 2, [5, 5], 'unique heavy literal h<=10'),
        ('light count1', 2, [8, 1], 'unique heavy literal h<=10'),
        ('F8 outside proved scalar domain', 2, [6, 2], 'qualified total F>=9'),
        ('h11 beyond resource guard', 2, [11, 2], 'unique heavy literal h<=10'),
        ('N82 beyond unchanged original guard', 2, [9, 4], 'unchanged original N80 parent guard BEFORE construction'),
    ):
        rejected(name, lambda n=n, counts=counts: geometry.preflight(n, counts), exact)

    raw = reader.load(args.input)
    reader.require(raw['n'] == 2 and raw['counts'] == [5, 4], 'exact new q=r adverse input')
    changes = []
    damaged = copy.deepcopy(raw)
    damaged['family'][0] = 1
    changes.append(('delete actual empty label', damaged, 'ENTIRE literal original family'))
    damaged = copy.deepcopy(raw)
    damaged['rows'][0] = damaged['rows'][1][:]
    changes.append(('replace actual empty row', damaged, 'ACTUAL empty negative proper-row sum'))
    damaged = copy.deepcopy(raw)
    damaged['group_scalars'][0]['mu'] = '0'
    changes.append(('stale heavy mean scalar', damaged, 'ALL variable-count original scalar fields'))
    damaged = copy.deepcopy(raw)
    damaged['b'][-1] = '0'
    changes.append(('drop light-full repair weight', damaged, 'ALL ORIGINAL COUNT-WEIGHTED repair coefficients'))
    damaged = copy.deepcopy(raw)
    damaged['dual_vector'][0] = str(reader.rational(damaged['dual_vector'][0]) + 1)
    changes.append(('alter original dual old score', damaged, 'EVERY original dual score INCLUDING ACTUAL empty'))
    damaged = copy.deepcopy(raw)
    damaged['kappa'] = '0'
    changes.append(('false lower endpoint energy', damaged, 'WHOLE original weighted dual inverse energy and uniform bound'))
    damaged = copy.deepcopy(raw)
    damaged['dimension'] += 1
    changes.append(('pad physical dimension', damaged, 'whole original dimensions/counts'))
    for name, damaged, exact in changes:
        rejected(name, lambda damaged=damaged: reader.check(damaged), exact)
    reader.require(len(cases) == 17 and all(x['rejected'] for x in cases), 'complete new rejection census')
    result = {'agent': 'six-downset-1', 'role': 'researcher', 'complete': True,
              'count': len(cases), 'cases': cases, 'source_commit': None, 'graph_ref': None}
    args.out.write_text(json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n')
    signal.alarm(0)
    print(json.dumps({'complete': True, 'exact_rejections': len(cases)}))


if __name__ == '__main__':
    main()
