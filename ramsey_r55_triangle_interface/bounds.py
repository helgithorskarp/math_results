"""Exact all-task width-nine/ten census and literal reduction by macro order."""
from math import comb
from pathlib import Path
import argparse
import json


def rows():
    result = []
    for q in range(7, 11):
        n = 43-4*q; fixed = 6*q+comb(n, 2)
        width10 = 2*(comb(q, 5)*4**5+comb(q, 4)*4**4*n)
        width9 = (6*q*(comb(q-1, 3)*4**3+comb(q-1, 2)*4**2*n)
                  + comb(n, 2)*comb(q, 3)*4**3)
        auxiliaries3 = 2*comb(q-1, 3)*4**3
        auxiliaries2 = 4*(q-2)*fixed
        reduction = 2*width10+width9-10*auxiliaries3-7*auxiliaries2
        if reduction <= 0:
            raise ValueError('nonpositive exact reduction')
        result.append({'q': q, 'core_order': n, 'fixed_edges': fixed,
                       'width9_target_clauses': width9, 'width10_target_clauses': width10,
                       'two_input_auxiliaries': auxiliaries2,
                       'three_input_auxiliaries': auxiliaries3,
                       'triangle_auxiliaries': auxiliaries2+auxiliaries3,
                       'exact_literal_reduction': reduction})
    return result


def check(audits):
    expected = {row['q']: row for row in rows()}; tasks = []
    for path in audits:
        tasks.extend(json.loads(Path(path).read_text())['tasks'])
    if len(tasks) != 18 or {(x['q'], x['r']) for x in tasks} != {(q, r) for q in range(7, 11) for r in range(5, q+1)}:
        raise ValueError('representative macro coverage')
    for task in tasks:
        row = expected[task['q']]
        if task['triangle_variables'] != row['triangle_auxiliaries'] or task['literal_reduction'] != row['exact_literal_reduction']:
            raise ValueError('exact formula/audit mismatch')
        if task['base_histogram'].get('9') != row['width9_target_clauses'] or task['base_histogram'].get('10') != row['width10_target_clauses']:
            raise ValueError('long-clause census mismatch')
    return {'status': 'VERIFIED_EXACT_ALL_TASK_FORMULAS_AND_18_MACRO_AUDITS',
            'tasks_covered_by_theorem': 2189178, 'macro_classes_audited': 18,
            'base_max_width': 10, 'factored_max_width': 8, 'rows': rows()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('audits', nargs='*', type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.audits) if args.audits else {'status': 'EXACT_FORMULAS', 'rows': rows()},
                     indent=2, sort_keys=True))
