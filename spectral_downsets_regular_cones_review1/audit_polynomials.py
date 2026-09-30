#!/usr/bin/env python3
"""Independent cone determinant audit, SymPy QQ polynomial division.

Derive P from the cleared three-vector Gram determinant, not author P code.
Check complete coefficient tables and an independent exact determining grid.
All variables have characteristic zero; no numerical eigenvalues are used.
"""
import argparse
import hashlib
import itertools
import json
import resource
import time
from fractions import Fraction as Q
from pathlib import Path
import sympy as s

def check(ok, message):
    if not ok: raise ValueError(message)

def scalar(h,d,l):
    # Six determinant terms of the normalized symmetric block; sqrt factors
    # pair to g. This expression is defined also at the zero-image endpoint.
    g=d+l; w=Q(2*(d-1),d*(h-2)); z=Q(2*(2*d-h),d*(h-4)+2)
    a=h+1; b=-1+Q(2,d)*l; c=h-Q(h-d,d)*l
    e=h+2+z-(1+z)*g
    return a*c*e+2*b*(1+w)*g-a*g-c*(1+w)**2*g-e*b*b

def records(p,variables):
    return [list(k)+[int(v)] for k,v in sorted(s.Poly(p,*variables,domain=s.ZZ).terms())]

def run(compare=None):
    h,d,l=s.symbols('h d lambda')
    H=h-2; E=d*(h-4)+2; g=d+l
    w=2*(d-1)/(d*H); z=2*(2*d-h)/E
    a=h+1; b=-1+2*l/d; c=h-(h-d)*l/d; e=h+2+z-(1+z)*g
    # Coordinate vectors: spoke y, singleton y, B^T y (squared norm g).
    gram=s.Matrix([[a,b,-(1+w)*g],[b,c,-g],[-(1+w)*g,-g,g*e]])
    clear=d*H*E
    mat=gram.applyfunc(lambda v:s.cancel(clear*v))
    check(all(s.denom(v)==1 for v in mat),'uncleared Gram denominator')
    determinant=s.Poly(mat.det(method='domain-ge'),h,d,l,domain=s.ZZ)
    divisor=s.Poly(g*H*E**2,h,d,l,domain=s.ZZ)
    P=determinant.exquo(divisor).as_expr()
    check(s.expand(P*divisor.as_expr()-determinant.as_expr())==0,'exact quotient identity')
    # A separate rational determinant expansion checks interpretation.
    direct=a*c*e+2*b*(1+w)*g-a*g-c*(1+w)**2*g-e*b*b
    check(s.cancel(P-d**3*H**2*E*direct)==0,'normalized determinant identity')
    A,B,V=s.symbols('A B V');variables=(A,B,V)
    fixtures={};summary={};grids=0
    mappings={
        'dense':(2*A+B+4,A+B+2,A-V,2*A+B+2),
        'middle':(2*B+5,B+2,B+1-V,2*B+3),
        'sparse':(A+2*B+6,B+2,B+2-V,2*B+4)}
    for name,(hv,dv,lv,limit) in mappings.items():
        substituted=s.Poly(P.subs({h:hv,d:dv,l:lv},simultaneous=True),*variables,domain=s.ZZ)
        check(substituted.degree(V)==3 and substituted.total_degree()<=10,'degree bound')
        parts=[s.expand(substituted.as_expr()).coeff(V,i) for i in range(4)]
        positives=(parts[0],parts[1],parts[2]+limit*parts[3],-parts[3])
        tables=[records(p,variables) for p in positives]
        for p,t in zip(positives,tables):
            check(t and all(row[-1]>0 for row in t),'nonpositive coefficient')
            check(p.subs({A:0,B:0,V:0})>0,'nonpositive constant')
        fixtures[name]=dict(zip(('P0','P1','P2_plus_limit_P3','minus_P3'),tables))
        # A priori degree <=10 in each parameter, <=3 in V follows from the
        # cleared determinant expansion (given explicitly in the review).
        # This complete grid independently checks identity with Fraction,
        # rather than treating a few substitutions as universal evidence.
        coeffs=records(substituted.as_expr(),variables)
        points=itertools.product(range(11) if name!='middle' else range(1),range(11),range(4))
        for av,bv,vv in points:
            hv0,dv0,lv0=[int(x.subs({A:av,B:bv,V:vv})) for x in (hv,dv,lv)]
            value=sum(c*av**i*bv**j*vv**k for i,j,k,c in coeffs)
            want=dv0**3*(hv0-2)**2*(dv0*(hv0-4)+2)*scalar(hv0,dv0,Q(lv0))
            check(value==want,'determining rational grid mismatch')
            grids+=1
        summary[name]={'positive_terms':list(map(len,tables)),
                       'positive_constants':[int(p.subs({A:0,B:0,V:0})) for p in positives],
                       'P_total_degree':substituted.total_degree(),
                       'P_parameter_degrees':[substituted.degree(x) for x in variables]}
    if compare:
        check(fixtures==json.loads(compare.read_text()),'author coefficient table mismatch')
    canonical=json.dumps(fixtures,sort_keys=True,separators=(',',':')).encode()
    return {'status':'COMPLETE','agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'sympy_version':s.__version__,'domain':'Z[h,d,lambda], exact division; Z[A,B,V]',
            'canonical_coefficient_sha256':hashlib.sha256(canonical).hexdigest(),
            'regimes':summary,'exact_determining_grid_points':grids,
            'cleared_Gram_exact_quotient_and_normalized_identity':True}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--compare-author',type=Path)
    p.add_argument('--output',type=Path);p.add_argument('--check',type=Path);args=p.parse_args()
    start=time.monotonic();r=run(args.compare_author)
    payload=json.dumps(r,sort_keys=True,separators=(',',':'))+'\n'
    if args.check:check(r==json.loads(args.check.read_text()),'expected output mismatch')
    if args.output:args.output.write_text(payload)
    print(json.dumps({'result':r,'sha256':hashlib.sha256(payload.encode()).hexdigest(),
                     'seconds':time.monotonic()-start,'rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
