#!/usr/bin/env python3
"""Optional stronger complex-affine audit of the24 selected h4195 pencils.

This CAS check is separate from the general physical theorem's portable proof.
It reuses the C0 package's exact polynomial interface and field-Euclid helpers.
"""
import argparse
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys
import exact as E

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'hadwiger_nelson_radix_c0_physical_star'
sys.path.insert(0,str(OLD))
import algebra as A
spec=importlib.util.spec_from_file_location('hn_h3_resultant_helpers',OLD/'verify.py')
V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)


def components(left,right,x,y,s):
    f,g=[A.expression(p,x,y) for p in (left,right)]
    R=A.sp.Poly(A.sp.resultant(f,g,y),x,domain=A.sp.QQ)
    E.need(not R.is_zero,'nonzero resultant')
    out=[]
    for q0,_ in A.sp.factor_list(R)[1]:
        qx=A.primitive(q0,x)
        q=V.fmpq_poly([V.fmpq(v) for v in A.coefficients(qx)])
        h=V.outer_gcd(V.fiber(left,q),V.fiber(right,q),q)
        E.need(h,'whole vertical component')
        if len(h)==1:continue
        if qx.degree()==1:
            x0=-qx.nth(0)/qx.nth(1)
            hy=A.sp.Poly(sum(A.sp.Rational(str(a[0]))*y**j for j,a in enumerate(h)),y)
            for h0,_ in A.sp.factor_list(hy)[1]:
                qy=A.primitive(h0.as_expr().subs(y,s),s)
                out.append(A.encode(qy,A.sp.Poly(x0,s,domain=A.sp.QQ),A.sp.Poly(s,s,domain=A.sp.QQ),s))
        else:
            E.need(len(h)==2 and h[1]==V.fmpq_poly([1]),'nonlinear nonrational fiber')
            qq=A.sp.Poly(qx.as_expr().subs(x,s),s,domain=A.sp.QQ)
            yy=A.sp.Poly(sum(-A.sp.Rational(str(v))*s**i for i,v in enumerate(h[0].coeffs())),s,domain=A.sp.QQ)
            out.append(A.encode(qq,A.sp.Poly(s,s,domain=A.sp.QQ),yy,s))
    return out


def run(method):
    interface=json.loads((HERE/'A5_INTERFACE.json').read_text())
    rows,events,factors,*_=A.architecture.build();lookup={f:i for i,f in enumerate(factors)}
    buckets={}
    for row,event in zip(rows,events):
        if not event or sum(c!=(0,0) for c in row)==1:continue
        normal=E.canonical_normal(tuple(E.residue(c) for c in row[1:]))
        pivot=next(E.residue(c) for c in row[1:] if c!=(0,0))
        inv=next(a for a in (1,2,3) if E.gf_mul(a,pivot)==1)
        sig=(normal,E.gf_mul(E.residue(row[0]),inv))
        buckets.setdefault(sig,[]).append(lookup[event])
    for sig in buckets:buckets[sig]=sorted(buckets[sig])
    x,y,s=A.sp.symbols('x y s');transcript=[];pair_count=0
    for index,p in interface['remaining_h4195_index_pencil']:
        domains=sorted([buckets[tuple(n),c] for n,c in p],key=lambda d:(len(d),d))
        E.need([len(d) for d in domains]==[2,2,2,4,4],'complete pencil domains')
        for a,b in product(*domains[:2]):
            pair_count+=1
            if method=='resultant':cc=components(factors[a],factors[b],x,y,s)
            else:cc=[A.encode(q,xx,yy,s) for q,xx,yy in A.groebner_components(A.expression(factors[a],x,y),A.expression(factors[b],x,y),x,y,s)]
            for field in sorted(cc,key=A.digest):
                ev=A.evaluator(field)
                E.need(ev(factors[a]) and ev(factors[b]),'anchor substitution')
                sections=[[j for j in d if ev(factors[j])] for d in domains]
                E.need(not all(sections),'complex-affine five-curve concurrence')
                transcript.append([index,[a,b],field,sections])
    return {'status':'PASS','pencils':24,'quintets':3072,'anchor_pairs':pair_count,
            'algebraic_components_with_pair_incidence':len(transcript),'complex_affine_concurrences':0,
            'transcript_sha256':A.digest(transcript)}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--method',choices=('resultant','groebner'),default='resultant');p.add_argument('--check-expected',action='store_true');args=p.parse_args()
    out=run(args.method)
    if args.check_expected:E.need(out==json.loads((HERE/'FINITE_A5_EXPECTED.json').read_text()),'finite result')
    print(json.dumps(out,sort_keys=True,indent=2))
