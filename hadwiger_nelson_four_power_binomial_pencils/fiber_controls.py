#!/usr/bin/env python3
"""Positive and negative controls for nonlinear and repeated algebraic fibers."""
import importlib.util,json
from pathlib import Path
from interface import A,HERE
import roots
spec=importlib.util.spec_from_file_location('binomial_fiber_verifier',HERE/'verify.py')
V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
def sparse(expr,x,y):return tuple((a,b,int(c)) for (a,b),c in A.sp.Poly(expr,x,y).terms())
def run():
    x,y,s=A.sp.symbols('x y s')
    left=sparse(y*y-x,x,y);right=sparse(x*x-2,x,y)
    cc=[dict(c,key=A.digest(c)) for c in roots.resultant(left,right,x,y,s)]
    plain=V.fiber_audit(([0,1],left,right,cc))
    repeated=V.fiber_audit(([0,1],sparse((y*y-x)**2,x,y),right,cc))
    A.need(len(cc)==1 and len(cc[0]['q'])-1==4,'four distinct algebraic points')
    A.need(plain['nonlinear_nonrational_fibers']==repeated['nonlinear_nonrational_fibers']==1,'nonlinear rational-extension fiber exercised')
    A.need(plain['fibers'][0][1:3]==[2,2] and repeated['fibers'][0][1:3]==[4,2],'multiplicity removed by derivative gcd')
    rejected=[]
    for name,data in [('omit_entire_algebraic_component',[]),('duplicate_component',cc+cc)]:
        try:V.fiber_audit(([0,1],left,right,data))
        except ValueError as error:
            A.need(any(w in str(error) for w in ('complete square-free fiber coverage','unique x projection factor')),'intended fiber rejection')
            rejected.append(name)
        else:raise ValueError('corruption accepted')
    return {'status':'PASS','distinct_complex_points':4,'distinct_real_points':sum(roots.nreal(c) for c in cc),'fiber_degrees':[2,4],'square_free_fiber_degrees':[2,2],'corruptions_rejected':rejected}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
