#!/usr/bin/env python3
"""Independent Groebner and coefficient-norm certificate producer."""
import argparse,json,math
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import sympy as S
import flint
import colour as C
import geometry as G
X=C.X;V=C.V;HERE=Path(__file__).resolve().parent
FRONTIER_SHA='5496087ac2e75104443c73022ec58bdcc71bb3bafb4605c79aed487fdd3f1da3'


def ratcoeff(expr,var):return tuple(str(c) for c in reversed(S.Poly(expr,var).all_coeffs()))


def groebner_geometry(pairs):
    factors,normalized,unused,coeff,images=G.inventory(pairs)
    t,r,u=S.symbols('t r u');tr=[S.Integer(2),t]
    for _ in range(2,5):tr.append(S.expand(t*tr[-1]-r*tr[-2]))
    polys={}
    for c,row in coeff.items():
        value=-1+sum(a*a*r**i for i,a in enumerate(row))
        for i,a in enumerate(row):
            for j,b in enumerate(row[:i]):value+=a*b*r**j*tr[i-j]
        polys[c]=S.expand(value.subs(t,u-r))
    components={};cover=[]
    def put(q,T,R):
        key=(G.primitive(q),ratcoeff(T,u),ratcoeff(R,u));text=G.keytext(key);components[text]=key;return text
    for a,b,rotation,c,d in normalized:
        f,g=polys[c],polys[d];basis=S.groebner([f,g],r,u)
        elim=[p for p in basis.polys if p.degree(r)==0]
        X.need(elim,'zero-dimensional source system')
        eliminant=S.Poly(elim[0].as_expr(),u);keys=[]
        for q,m in S.factor_list(eliminant)[1]:
            q=S.Poly(q,u).monic();basis=S.groebner([f,g,q.as_expr()],r,u)
            radius=next(p.as_expr() for p in basis.polys if p.degree(r)>0)
            if S.degree(radius,r)==1:
                R=-radius.subs(r,0)/S.diff(radius,r)
                keys.append(put(list(reversed(q.all_coeffs())),u-R,R))
            else:
                X.need(q.degree()==1,'rational exceptional projection fibre');value=-q.nth(0)/q.nth(1)
                for h,e in S.factor_list(S.Poly(radius.subs(u,value),r))[1]:
                    keys.append(put(list(reversed(h.all_coeffs())),value-u,u))
        cover.append([[a,b],sorted(set(keys))])
    ordered=sorted(components);ids={text:i for i,text in enumerate(ordered)}
    return {'components':[components[k] for k in ordered],
            'coverage':[[pair,[ids[k] for k in keys]] for pair,keys in cover],
            'normalizations':normalized,'curve_inventory_sha256':X.digest(factors),
            'real_coefficient_curves':len(coeff),'physical_pair_exclusions':images}


def projected_rows():
    _,factors,circle,monos,rowids=V.reconstruct_inventory();t,r=S.symbols('t r')
    tr=[S.Integer(2),t];us=[S.Integer(1),t]
    for _ in range(2,5):tr.append(S.expand(t*tr[-1]-r*tr[-2]));us.append(S.expand(t*us[-1]-r*us[-2]))
    def terms(expr):return tuple((i,j,int(c)) for (i,j),c in S.Poly(expr,t,r).terms() if c)
    projections={}
    for row,c in rowids.items():
        E=-2+2*sum((a*a+a*b+b*b)*r**i for i,(a,b) in enumerate(row));O=0
        for i,ai in enumerate(row):
            for j,(a,b) in enumerate(row[:i]):
                aa,bb=V.e_mul(ai,(a+b,-b));E+=(2*aa+bb)*r**j*tr[i-j];O-=6*bb*r**j*us[i-j-1]
        es,os=terms(E),terms(O);os=min(os,tuple((i,j,-c) for i,j,c in os));key=(es,os)
        bad=sum(1<<k for k,w in enumerate(C.weights) if sum(v*(a-b) for v,(a,b) in zip(w,row))%3==0)
        projections[key]=projections.get(key,0)|bad
    projections[(terms(2*r-2),())]=sum(1<<k for k,w in enumerate(C.weights) if not all(w))
    return projections


def generate_words(components):
    projected=projected_rows();prime=1000003;words=[]
    def mr(s):
        f=Fraction(s);return f.numerator%prime*pow(f.denominator%prime,-1,prime)%prime
    for q,ts,rs in components:
        X.need(q[-1]%prime and all(Fraction(s).denominator%prime for s in ts+rs),'fixed proof prime preserves degrees and denominators')
        Q=flint.nmod_poly(list(q),prime);T=flint.nmod_poly([mr(s) for s in ts],prime);R=flint.nmod_poly([mr(s) for s in rs],prime)
        tp=[flint.nmod_poly([1],prime)];rp=list(tp)
        for _ in range(4):tp.append(tp[-1]*T%Q);rp.append(rp[-1]*R%Q)
        mon={(i,j):tp[i]*rp[j]%Q for i in range(5) for j in range(5-i)};delta=(4*R-T*T)%Q
        def ev(es):
            out=flint.nmod_poly([],prime)
            for i,j,c in es:out+=c*mon[i,j]
            return out
        forbidden=0
        for (es,os),bad in projected.items():
            E,O=ev(es),ev(os);value=(12*E*E-delta*O*O)%Q
            if value.gcd(Q).degree()!=0:forbidden|=bad
        good=[i for i in range(81) if not forbidden>>i&1]
        X.need(good,'complete three-colour gate');words.append(good[0])
    return words


def produce(frontier):
    data=json.loads(Path(frontier).read_text());X.need(X.digest(data)==FRONTIER_SHA,'pinned h4185 residual interface')
    pairs=sorted(row for mode in ('remaining_exact','remaining_six') for row in data[mode] if row[2]&56)
    geometry=groebner_geometry(pairs);words=generate_words(geometry['components'])
    return {'schema':'hn-radix-reflection-pair-stratum-v1','source_frontier_sha256':FRONTIER_SHA,'pair_rows':pairs,
            'curve_inventory_sha256':geometry['curve_inventory_sha256'],'component_inventory_sha256':X.digest(geometry['components']),
            'cover_sha256':X.digest(geometry['coverage']),'normalizations_sha256':X.digest(geometry['normalizations']),
            'expanded_pair_exclusions_sha256':X.digest(geometry['physical_pair_exclusions']),
            'prime':1000003,'colour_word_indices':words}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--frontier',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    cert=produce(a.frontier)
    with a.out.open('x') as f:json.dump(cert,f,sort_keys=True,separators=(',',':'));f.write('\n')
    print(json.dumps({'pairs':len(cert['pair_rows']),'algebraic_chart_records':len(cert['colour_word_indices']),
                      'colour_histogram':dict(Counter(cert['colour_word_indices'])),'record_improvement':False},indent=2,sort_keys=True))
