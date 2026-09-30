#!/usr/bin/env python3
"""Exact determinant certificates for all regular-cone degree regimes.

Middle: D=d-2>=0,Z=d-1-lambda in[0,2d-1],h=2d+1.
Sparse: R=h-2d-2>=0,D=d-2>=0,Y=d-lambda in[0,2d].
Dense: reuse and check the preceding dense coefficient fixture.
No floating arithmetic, interpolation, CAS or graph census is used.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
import dense_cone_polynomials as dense
from dense_cone_polynomials import constant,var,add,scale,mul,determinant3,records,evaluate


def determinant_polynomial(h,d,lam):
    gap=add(h,scale(-1,d));H=add(h,constant(-2))
    E=add(mul(d,add(h,constant(-4))),constant(2))
    g=add(d,lam);top=add(h,constant(1))
    znum=scale(2,add(scale(2,d),scale(-1,h)))
    e=add(mul(E,add(h,constant(2),scale(-1,g))),
          mul(znum,add(constant(1),scale(-1,g))))
    c=add(mul(h,d),scale(-1,mul(gap,lam)))
    b=add(scale(-1,d),scale(2,lam));k=add(mul(d,h),constant(-2))
    second=add(mul(top,c,d),scale(-1,mul(b,b)))
    correction=add(mul(top,d,d,d,H,H),mul(c,k,k),scale(-2,mul(b,k,d,H)))
    P=add(mul(d,H,H,second,e),scale(-1,mul(g,E,correction)))

    # Expand the cleared rational 3-coordinate Gram matrix directly.
    # Its third vector has squared norm g; the exact identity is in
    # Z[R,D,Y] (or Z[D,Z]), including the zero-image endpoint g=0.
    common=mul(d,H,E)
    gram=[[mul(top,common),mul(b,H,E),scale(-1,mul(k,g,E))],
          [mul(b,H,E),mul(c,H,E),scale(-1,mul(g,common))],
          [scale(-1,mul(k,g,E)),scale(-1,mul(g,common)),mul(g,e,d,H)]]
    if determinant3(gram)!=mul(g,H,E,E,P):
        raise ValueError("Cleared Leibniz determinant identity failed")
    return P


def regime(name):
    R,D,Y=[var(i) for i in range(3)];d=add(D,constant(2))
    if name=="middle":
        h=add(scale(2,d),constant(1))
        lam=add(d,constant(-1),scale(-1,Y))
        limit=add(scale(2,d),constant(-1))
    elif name=="sparse":
        h=add(scale(2,d),constant(2),R)
        lam=add(d,scale(-1,Y));limit=scale(2,d)
    else:raise ValueError("Unknown determinant regime")
    P=determinant_polynomial(h,d,lam)
    if max(k for i,j,k in P)!=3:raise ValueError("Unexpected spectral degree")
    pieces=[{(i,j,0):v for (i,j,k),v in P.items() if k==r} for r in range(4)]
    positive=[pieces[0],pieces[1],add(pieces[2],mul(limit,pieces[3])),scale(-1,pieces[3])]
    if any(not p or p.get((0,0,0),0)<=0 or any(v<=0 for v in p.values()) for p in positive):
        raise ValueError("Positive coefficient certificate failed")
    certificate=dict(zip(("P0","P1","P2_plus_limit_P3","minus_P3"),map(records,positive)))
    return P,certificate,dict(expanded_terms=len(P),degree_spectral_variable=3,
                             positive_terms=list(map(len,positive)),
                             positive_constants=[p[(0,0,0)] for p in positive])


def scalar_determinant(h,d,lam):
    g=d+lam;alpha=F(h-d,d);w=F(2*(d-1),d*(h-2));z=F(2*(2*d-h),d*(h-4)+2)
    b=-1+2*lam/d;c=h-alpha*lam;e=h+2+z-(1+z)*g
    return (h+1)*c*e+2*b*(1+w)*g-(h+1)*g-c*(1+w)**2*g-e*b*b


def verify_certificate():
    dense_summary,dense_certificate=dense.verify_certificate()
    fixture={"dense":dense_certificate};summaries={"dense":dense_summary}
    polynomials={}
    for name in ("middle","sparse"):
        P,certificate,summary=regime(name)
        polynomials[name]=P;fixture[name]=certificate;summaries[name]=summary
    samples=[]
    inputs=[(5,2),(9,4),(13,6),(17,8),(6,2),(8,2),(8,3),(12,3),
            (16,3),(18,6),(50,2),(50,15),(100,40)]
    for h,d in inputs:
        name="middle" if h==2*d+1 else "sparse"
        high=d-1 if name=="middle" else d
        for lam in (F(-d),F(high),F(high-d,2),F(2*high-d,3)):
            R=h-2*d-2 if name=="sparse" else 0
            D=d-2;Y=d-lam if name=="sparse" else d-1-lam
            det=scalar_determinant(h,d,lam)
            denominator=d**3*(h-2)**2*(d*(h-4)+2)
            if evaluate(polynomials[name],R,D,Y)!=denominator*det or det<=0:
                raise ValueError("Literal rational determinant check failed")
            samples.append([name,h,d,str(lam),str(det)])
    digest=sha256(json.dumps(fixture,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return dict(regimes=summaries,canonical_certificate_sha256=digest,
                rational_substitutions=samples),fixture


if __name__=="__main__":
    summary,fixture=verify_certificate()
    print(json.dumps(dict(verification=summary,coefficient_certificate=fixture),sort_keys=True,indent=2))
