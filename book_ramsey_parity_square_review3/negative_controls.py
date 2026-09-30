#!/usr/bin/env python3
"""Bounded corruption guards; imports only this reviewer's own checker."""
import json
from independent_check import CASES, forced_square, graph_data, validate_forced


def expect_rejection(name, operation):
    try:
        operation()
    except ValueError as error:
        return {'name': name, 'rejected': True, 'reason': str(error)}
    raise RuntimeError('corruption accepted: '+name)


def main():
    records = []
    for name, i, j, change in [('diagonal unit', 0, 0, 1),
                               ('symmetric offdiagonal unit', 0, 1, 1),
                               ('deleted defect pair', 7, 8, 4),
                               ('cross-class coefficient', 0, 19, 4)]:
        h = forced_square(CASES[0])
        h[i][j] += change
        if i != j:
            h[j][i] += change
        records.append(expect_rejection(name, lambda: validate_forced(CASES[0], h)))
    records.append(expect_rejection('wrong histogram', lambda:
                                    validate_forced(CASES[1], forced_square(CASES[0]))))
    a = [[0]*22 for _ in range(22)]
    a[0][0] = 1
    records.append(expect_rejection('loop', lambda: graph_data(a)))
    a = [[0]*22 for _ in range(22)]
    a[0][1] = 1
    records.append(expect_rejection('asymmetric adjacency', lambda: graph_data(a)))
    print(json.dumps({'agent': 'six-reviewer-3', 'complete': True,
                      'corruptions_rejected': len(records), 'records': records},
                     sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
