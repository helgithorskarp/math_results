#!/usr/bin/env python3
"""Regenerate eleven exact dual proposals outside Git; verify with verify_a0.py.

CPython3.11.2, NumPy2.4.6, SciPy1.15.3. Floating optimization is discovery.
"""
import argparse,json,time
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,eye,hstack
from generate_a3_certificates import sparse
from a0_far_models import cases

DEN=10**8
BUDGET=470


def certificate(name,data):
 T,E,eq,eb,ub,bb,meta=data;n=len(T)+len(E)+len(meta)
 M=sparse(eq,n);U=sparse(ub,n);ne=len(eq);nu=len(ub)
 me=hstack([M,eye(ne),-eye(ne),csr_matrix((ne,nu))],format='csr')
 mu=hstack([U,csr_matrix((nu,2*ne)),-eye(nu)],format='csr')
 t=time.monotonic()
 r=linprog(np.r_[np.zeros(n),np.ones(2*ne+nu)],A_eq=me,b_eq=eb,A_ub=mu,b_ub=bb,bounds=(0,None),method='highs')
 if not r.success:raise ValueError((name,r.status,r.message))
 lm=[round(float(v)*DEN) for v in r.eqlin.marginals]
 um=[min(0,round(float(v)*DEN)) for v in r.ineqlin.marginals]
 cs=[Fraction(0)]*n;rhs=Fraction(0)
 for rows,bs,ms in ((eq,eb,lm),(ub,bb,um)):
  for row,b,mul in zip(rows,bs,ms):
   rhs+=Fraction(mul,DEN)*b
   if mul:
    for i,v in row.items():cs[i]+=Fraction(mul,DEN)*v
 delta=max([Fraction(0)]+cs);bound=rhs-BUDGET*delta
 if bound<=0:raise ValueError(('no positive exact corrected bound',name,str(bound)))
 rec={'name':name,'denominator':DEN,'dimensions':[len(T),len(E),len(meta),len(eq),len(ub)],
      'equality_multipliers':[[i,v] for i,v in enumerate(lm) if v],
      'inequality_multipliers':[[i,v] for i,v in enumerate(um) if v],
      'uncorrected_bound':str(rhs),'coefficient_excess':str(delta),'variable_budget':BUDGET,'corrected_bound':str(bound)}
 print(json.dumps({'name':name,'exact_bound':str(bound),'seconds':time.monotonic()-t}),flush=True)
 return rec


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.output.exists():raise FileExistsError(a.output)
 records=[certificate(name,data) for name,row,epsq,data in cases()]
 a.output.write_text(json.dumps(records,indent=2)+'\n')
 print('Generated eleven dual proposals. Exact independent verification is required.')

if __name__=='__main__':main()
