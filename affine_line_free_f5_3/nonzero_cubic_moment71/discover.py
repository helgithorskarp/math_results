#!/usr/bin/env python3
"""Optional LP discovery; every output certificate is immediately checked exactly."""
import argparse
from fractions import Fraction
from functools import reduce
from math import gcd, lcm
import json
from pathlib import Path
import tempfile

import numpy as np
from scipy.optimize import linprog

from field import require
from model import FORMS, check_certificate, geometry, instance
from verify import build, collect_cases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--cxx',default='g++')
    parser.add_argument('--cxxflags',default='-O2')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='cubic71-discovery-') as temp:
        binaries = build(temp,args.cxx,args.cxxflags)
        _, cases = collect_cases(binaries['quartics'])
    incidence = geometry()
    certificates = []
    for case in cases:
        C,d,D = instance(FORMS[case['form']],case['representative'],case['epsilon'],incidence)
        n = len(C[0])
        # A common nonnegative slack makes phase I feasible. Its dual yields
        # a Farkas separation when the optimum is strictly positive.
        answer = linprog(np.r_[np.zeros(n),1.0],
                         A_ub=np.column_stack((C,-np.ones(len(C)))),b_ub=d,
                         A_eq=np.column_stack((D,np.zeros(len(D)))),b_eq=np.ones(len(D)),
                         bounds=(0,None),method='highs')
        require(answer.success and answer.fun > 1e-7, 'no numerical separation found')
        lam = [Fraction(float(-x)).limit_denominator(1000000) for x in answer.ineqlin.marginals]
        y = [Fraction(float(-x)).limit_denominator(1000000) for x in answer.eqlin.marginals]
        denominator = lcm(*(x.denominator for x in lam+y))
        lam = [int(x*denominator) for x in lam]
        y = [int(x*denominator) for x in y]
        common = reduce(gcd,(abs(x) for x in lam+y))
        require(common > 0, 'zero candidate certificate')
        lam,y = [x//common for x in lam],[x//common for x in y]
        row = dict(case)
        row.update(inequality_multipliers=[[i,x] for i,x in enumerate(lam) if x],
                   equality_multipliers=[[i,x] for i,x in enumerate(y) if x],
                   contradiction=sum(x*b for x,b in zip(lam,d))+sum(y))
        check_certificate(row,FORMS[case['form']],incidence)
        certificates.append(row)
        # Preserve each checked result. A partial output is rejected by the
        # verifier's exact case-cover comparison.
        args.out.write_text(json.dumps({'format':'nonzero-cubic-farkas-v1',
                                        'cases':certificates},indent=2)+'\n')
        print(case['form'],case['orbit'],case['epsilon'],row['contradiction'],flush=True)


if __name__ == '__main__':
    main()
