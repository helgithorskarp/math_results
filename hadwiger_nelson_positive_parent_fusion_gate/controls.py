#!/usr/bin/env python3
"""Reject malformed witnesses and exercise all basis multiplication squares."""
from itertools import combinations
import json
import verify

def reject(call):
    try:
        call()
    except ValueError:
        return
    raise ValueError('invalid input accepted')

def main():
    zero = ((0,)*8, (0,)*8)
    tests = 0
    for i in range(8):
        x = [0]*8
        x[i] = 1
        verify.require(verify.norm((tuple(x), (0,)*8), zero) == (verify.RAD[i],)+(0,)*7, 'basis square')
        tests += 1
    for i, j in combinations(range(8), 2):
        x = [0]*8
        x[i] = x[j] = 1
        expected = [0]*8
        expected[0] = verify.RAD[i]+verify.RAD[j]
        expected[i ^ j] = 2*verify.RAD[i & j]
        verify.require(verify.norm((tuple(x), (0,)*8), zero) == tuple(expected), 'cross term')
        tests += 1
    reject(lambda: verify.proper([0, 1], [(0, 1)], '00'))
    reject(lambda: verify.proper([0, 1], [(0, 1)], '04'))
    reject(lambda: verify.proper([0, 1], [(0, 1)], '0'))
    reject(lambda: verify.point([['1/5']+['0']*7, ['0']*8]))
    print(json.dumps({'all_checks': True, 'field_controls': tests, 'rejected_faults': 4}))

if __name__ == '__main__':
    main()
