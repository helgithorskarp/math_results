#!/usr/bin/env python3
"""Optional floating-point discovery; the exact verifier supplies proof evidence.

Original environment: CPython 3.11.2, NumPy 2.4.6, SciPy 1.15.3.
Run with --output /tmp/z12-four-defects.json; never overwrites a certificate.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix, csr_matrix
from forest_constraints import model


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError(args.output)
    types,edges,eq,eb,ub,bb=model((16,26,12),edge_bounds=False)
    n=len(types)+len(edges)
    eq.append({i:5-ns[1]-2*ns[2] for i,(d,ns) in enumerate(types) if d==8})
    eb.append(4)
    def matrix(rows):
        x=lil_matrix((len(rows),n))
        for j,row in enumerate(rows):
            for i,v in row.items():x[j,i]=float(v)
        return csr_matrix(x)
    objective=np.zeros(n)
    for i,(d,ns) in enumerate(types):
        if d==8:objective[i]=ns[2]/2
    result=linprog(objective,A_ub=matrix(ub),b_ub=bb,A_eq=matrix(eq),b_eq=eb,
                   bounds=(0,None),method='highs')
    if not result.success:raise RuntimeError(result.message)
    denominator=1000000
    lm=[round(float(v)*denominator) for v in result.eqlin.marginals]
    mu=[min(0,round(float(v)*denominator)) for v in result.ineqlin.marginals]
    coefficients=[Fraction(0)]*n;rhs=Fraction(0)
    for rows,bs,multipliers in [(eq,eb,lm),(ub,bb,mu)]:
        for row,b,mul in zip(rows,bs,multipliers):
            rhs+=Fraction(mul*b,denominator)
            for i,v in row.items():coefficients[i]+=Fraction(mul,denominator)*v
    exact_objective=[Fraction(0)]*n
    for i,(d,ns) in enumerate(types):
        if d==8:exact_objective[i]=Fraction(ns[2],2)
    delta=max([Fraction(0)]+[coefficients[i]-exact_objective[i] for i in range(n)])
    bound=rhs-428*delta
    if bound<=1:raise ValueError('rounded certificate does not establish m>1')
    data={'description':'m>1 for z=12, total high far count A=4; every locally allowed type retained',
          'denominator':denominator,
          'equality_multipliers':[[i,x] for i,x in enumerate(lm) if x],
          'inequality_multipliers':[[i,x] for i,x in enumerate(mu) if x],
          'uncorrected_bound':str(rhs),'max_coefficient_error':str(delta),
          'variable_budget':428,'corrected_bound':str(bound),'sizes':[16,26,12],
          'total_high_far_count':4,'dimensions':[len(types),len(edges),len(eq),len(ub)]}
    args.output.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'floating_objective':result.fun,'exact_rounded_bound':str(bound),
                      'output':str(args.output)},sort_keys=True))


if __name__=='__main__':main()
