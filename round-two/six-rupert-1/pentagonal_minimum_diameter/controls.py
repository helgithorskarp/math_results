#!/usr/bin/env python3
"""Arithmetic controls and rejection of damaged finite proof evidence."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import json
from verify import Q, PHI, H, I, require, qi, lf, Z, ONE, group, vertices, orbit_rows
from verify import dual_check, cover_check


def rejects(fun):
    try:
        fun()
    except (ValueError, KeyError, TypeError):
        return
    raise ValueError('damaged certificate was accepted')


def main():
    require(PHI*PHI == PHI+1 and PHI/PHI == ONE, 'field normalization')
    for q, sign in [(Q(0), 0), (PHI-1, 1), (PHI-2, -1),
                    (Q(123)-76*PHI, 1), (Q(199)-123*PHI, -1)]:
        require(q.sign() == sign, 'exact irrational sign control')
    for box in [I(0, 0), I(2, 2), I(F(1, 3), F(5, 7)), I(4, 9)]:
        root = box.sqrt()
        require(root.lo*root.lo <= box.lo and root.hi*root.hi >= box.hi,
                'outward square-root enclosure')
    rejects(lambda: I(1, -1))
    rejects(lambda: I(-1, 1).inv())
    rejects(lambda: I(-1, 1).sqrt())
    row = (lf(0, Z), lf(0, Z), lf(0))
    require(dual_check([row], [lf(0, Q(2))], {'rows': [0], 'weights': [1]}) > 0,
            'known impossible sphere halfspace')
    bad = [({'rows': [1], 'weights': [1]}, 2),
           ({'rows': [0], 'weights': [-1]}, 2),
           ({'rows': [0], 'weights': [0]}, 2),
           ({'rows': [0], 'weights': [1], 'extra': 0}, 2),
           ({'rows': [0, 0], 'weights': [1, 1]}, 2),
           ({'rows': [0], 'weights': [1]}, 1)]
    for c, b in bad:
        rejects(lambda c=c, b=b: dual_check([row], [lf(0, Q(b))], c))
    mats = group()
    D, E = orbit_rows(vertices(mats))
    original = json.loads(Path(__file__).with_name('duals.json').read_text())
    defects = []
    c = deepcopy(original)
    c['ico'].pop()
    defects.append(c)
    c = deepcopy(original)
    c['ico'][1] = c['ico'][0]
    defects.append(c)
    c = deepcopy(original)
    c['stage1'].pop()
    defects.append(c)
    c = deepcopy(original)
    c['stage2'].pop()
    defects.append(c)
    c = deepcopy(original)
    c['stage2'][0]['certificate']['weights'] = [0]*len(c['stage2'][0]['certificate']['weights'])
    defects.append(c)
    for c in defects:
        rejects(lambda c=c: cover_check(mats, D, E, c))
    print(json.dumps({'arithmetic_controls': 'PASS',
                      'malformed_evidence_rejections': 14}, sort_keys=True))


if __name__ == '__main__':
    main()
