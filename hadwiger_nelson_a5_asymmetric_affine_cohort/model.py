"""Exact A5 cohort definitions and algebraic chart operations over Q.

Geometry is z=x+i*sqrt(3)*y. The eliminating coordinate is u=x+2*y.
The algebraic and Cartesian helpers are credited reusable public routines;
none of their previous finite-family conclusions is used here.
"""
import importlib.util
import itertools
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OLD=ROOT/'hadwiger_nelson_radix_c0_physical_star'
sys.path.insert(0,str(OLD))
import algebra as A
import physical
spec=importlib.util.spec_from_file_location('affine_cohort_resultant_helper',OLD/'verify.py')
COVER=importlib.util.module_from_spec(spec);spec.loader.exec_module(COVER)
sp=A.sp
need=A.need
digest=A.digest


def load_cohort():
    data=json.loads((HERE/'COHORT.json').read_text())
    need(data['pencil_index']==2377 and len(data['pairs'])==64,'frozen cohort')
    left=(35,40,78,80,135,139,177,180)
    right=(1798,1799,1810,1811,2387,2388,2435,2436)
    need(data['pairs']==[[a,b] for a in left for b in right],'complete Cartesian cohort')
    polys={int(i):A.geometry.distance_event(tuple(map(tuple,row))) for i,row in data['source_rows'].items()}
    need(all(polys[a]!=polys[b] for a,b in data['pairs']),'distinct equations')
    signs=list(itertools.product((-1,1),repeat=3))
    named_left={A.geometry.distance_event(((0,0),(1,0),(-a,a),(0,b),(c,0))) for a,b,c in signs}
    named_right={A.geometry.distance_event(((1,0),(0,0),(a,0),(b,0),(c,0))) for a,b,c in signs}
    need(named_left=={polys[i] for i in left} and named_right=={polys[i] for i in right},'explicit signed norm family')
    return data,polys


def projected(poly,u,v):
    f=A.expression(poly,u,v).subs(u,u-2*v).expand()
    return tuple(sorted((i,j,int(c)) for (i,j),c in sp.Poly(f,u,v).terms()))


def physical_chart(chart):
    s=sp.Symbol('s')
    q=sp.Poly(sum(sp.Rational(c)*s**i for i,c in enumerate(chart['q'])),s,domain=sp.QQ)
    a=sp.Poly(sum(sp.Rational(c)*s**i for i,c in enumerate(chart['x'])),s,domain=sp.QQ)
    b=sp.Poly(sum(sp.Rational(c)*s**i for i,c in enumerate(chart['y'])),s,domain=sp.QQ)
    return A.encode(q,(a-2*b).rem(q),b,s)


def charts(pair,polys,method):
    u,v,s=sp.symbols('u v s')
    ff,gg=[projected(polys[i],u,v) for i in pair]
    result=[]
    if method=='groebner':
        for q,a,b in A.groebner_components(A.expression(ff,u,v),A.expression(gg,u,v),u,v,s):
            nr=int(q.count_roots(-sp.oo,sp.oo))
            if nr: result.append((A.encode(q,a,b,s),nr))
    elif method=='resultant':
        result=COVER.resultant_components(ff,gg,u,v,s)
    else: raise ValueError('unknown decomposition')
    out=[]
    for c,nr in result:
        c=physical_chart(c)
        ev=A.evaluator(c)
        need(all(ev(polys[i]) for i in pair),'substitution into both original equations')
        out.append(dict(c,real_embeddings=nr))
    out.sort(key=lambda c:digest(c))
    need(len({digest(c) for c in out})==len(out),'duplicate chart')
    return out


def root_intervals(chart):
    s=sp.Symbol('s')
    q=sp.Poly(sum(sp.Rational(c)*s**i for i,c in enumerate(chart['q'])),s,domain=sp.QQ)
    need(q.is_irreducible,'irreducible chart field')
    intervals=q.intervals(eps=sp.Rational(1,10**10))
    need(all(m==1 for interval,m in intervals),'simple characteristic-zero roots')
    need(len(intervals)==chart['real_embeddings'],'complete real root isolation')
    return [[str(a),str(b)] for (a,b),m in intervals]


def check_colour(word,n,edges,k):
    need(isinstance(word,list) and len(word)==n and all(type(c)==int and 0<=c<k for c in word),'colour word domain')
    need(all(word[a]!=word[b] for a,b in edges),'proper full physical colour word')


def point_stream(points):
    return [[list(physical.coefficients(a)),list(physical.coefficients(b))] for a,b in points]
