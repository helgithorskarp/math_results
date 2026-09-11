#!/usr/bin/env python3
"""Regenerate exact A3 certificates outside Git; CPython3.11.2/NumPy2.4.6/SciPy1.15.3.

Floating optimization proposes multipliers. The separate standard-library
verifier proves every resulting integer inequality. No bundle is downloaded.
"""
import argparse,json,time,pathlib
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix,csr_matrix,eye,hstack
from a3_models import cases
D=10**8

def sparse(rows,n):
 x=lil_matrix((len(rows),n))
 for j,row in enumerate(rows):
  for i,v in row.items():x[j,i]=v
 return csr_matrix(x)

def dual_cert(name,T,E,eq,eb,ub,bb,objective=None):
 n=len(T)+len(E);M=sparse(eq,n);U=sparse(ub,n);st=time.perf_counter()
 if objective is None:
  ne=len(eq);nu=len(ub)
  me=hstack([M,eye(ne),-eye(ne),csr_matrix((ne,nu))],format='csr')
  mu=hstack([U,csr_matrix((nu,2*ne)),-eye(nu)],format='csr')
  r=linprog(np.r_[np.zeros(n),np.ones(2*ne+nu)],A_eq=me,b_eq=eb,A_ub=mu,b_ub=bb,bounds=(0,None),method='highs')
  obj=[Fraction(0)]*n
 else:
  obj=objective
  r=linprog(np.array([float(v) for v in obj]),A_eq=M,b_eq=eb,A_ub=U,b_ub=bb,bounds=(0,None),method='highs')
 if not r.success:raise RuntimeError((name,r.status,r.message))
 lm=[round(float(v)*D) for v in r.eqlin.marginals];um=[min(0,round(float(v)*D)) for v in r.ineqlin.marginals]
 cs=[Fraction(0)]*n;rhs=Fraction(0)
 for rows,bs,multipliers in [(eq,eb,lm),(ub,bb,um)]:
  for row,b,mul in zip(rows,bs,multipliers):
   rhs+=Fraction(mul,D)*Fraction(b)
   if mul:
    for i,v in row.items():cs[i]+=Fraction(mul,D)*Fraction(v)
 err=max([Fraction(0)]+[cs[i]-obj[i] for i in range(n)]);bound=rhs-428*err
 rec={'name':name,'denominator':D,'dimensions':[len(T),len(E),len(eq),len(ub)],'equality_multipliers':[[i,v] for i,v in enumerate(lm) if v],'inequality_multipliers':[[i,v] for i,v in enumerate(um) if v],'uncorrected_bound':str(rhs),'coefficient_excess':str(err),'variable_budget':428,'corrected_bound':str(bound)}
 print(json.dumps({'name':name,'floating_phase_value':r.fun,'exact_bound':str(bound),'seconds':time.perf_counter()-st}),flush=True)
 if bound<=(1 if name=='m_at_A3' else 0):raise ValueError('no strict certificate')
 return rec


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=pathlib.Path,required=True)
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError(args.output)
    bundle=[]
    for name,(T,E,eq,eb,ub,bb),objective in cases():
        bundle.append(dual_cert(name,T,E,eq,eb,ub,bb,objective if name=='m_at_A3' else None))
    args.output.write_text(json.dumps(bundle,indent=2)+'\n')
    print('GENERATED: 14 cases; verify this bundle with verify_a3.py')


if __name__=='__main__':main()
