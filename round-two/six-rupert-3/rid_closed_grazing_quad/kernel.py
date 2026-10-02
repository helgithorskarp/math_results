"""Exact literal RID cut evaluation, polarization and semantic controls.

Every original scale>=1 and physical translation is retained in PROOF.md.
Python3.11+, standard library only; no private or numerical input.
"""
from functools import lru_cache
from pathlib import Path
from time import monotonic
from collections import Counter
import argparse,copy,hashlib,json,platform,resource
from geometry import build,OUT,F,Q,Z,O,phi,dot,cross,sub,midpoint,need,encode,neg
from domain import make_domain
from forest import read_certificate


@lru_cache(maxsize=50000)
def scalar(x,y):return dot(x,y)


def coefficients(cut,T,domain):
    R=domain['R'];rpairs=[(i,j) for i in range(3) for j in range(i,3)]
    if cut['kind']=='support':
        support=domain['supports'][cut['support']];v=cut['v'];vs=[dot(v,c) for c in T]
        at=[]
        for raw,h in zip(support['raw'],support['H']):
            a=dot(raw,v);f=cross(v,raw);ns=[dot(raw,c) for c in T];fs=[dot(f,c) for c in T]
            at.append([(a-h)-(a+h)*scalar(x,y)+ns[i]*vs[j]+ns[j]*vs[i]+fs[i]+fs[j]
                       for i,x in enumerate(T) for j,y in enumerate(T) if i<=j])
        return [(at[a][j]+at[b][j])/2 for a,b in rpairs for j in range(10)]
    k=cut['k'];vals=[[dot(r,k[1:])+k[0]*dot(r,c)+dot(cross(k[1:],r),c) for c in T] for r in R]
    return [(vals[a][i]*vals[b][j]+vals[a][j]*vals[b][i])/2-dot(R[a],R[b])
            for a,b in rpairs for i in range(4) for j in range(i,4)]


def literal_gap(cut,c,r,domain):
    if cut['kind']=='gauge':
        k=cut['k'];s=-dot(r,c)*k[0]-dot(tuple(r[j]+cross(r,c)[j] for j in range(3)),k[1:])
        return s*s-dot(r,r)
    support=domain['supports'][cut['support']];v=cut['v'];raw=cross(support['E'],r);h=dot(raw,DATA['V'][support['source_endpoints'][0]])
    c2=dot(c,c);cxv=cross(c,v)
    Rv=tuple(((1-c2)*v[j]+2*c[j]*dot(c,v)+2*cxv[j])/(1+c2) for j in range(3))
    return (1+c2)*(dot(raw,Rv)-h)


def independent_check(cut,T,values,domain):
    R=domain['R']
    def source(r):
        val=[literal_gap(cut,c,r,domain) for c in T]
        return [val[i] if i==j else 2*literal_gap(cut,midpoint(T[i],T[j]),r,domain)-(val[i]+val[j])/2
                for i in range(4) for j in range(i,4)]
    at=[source(r) for r in R];exact=[]
    for a in range(3):
        for b in range(a,3):
            mid=at[a] if a==b else source(midpoint(R[a],R[b]))
            exact.extend(at[a] if a==b else [2*x-(y+z)/2 for x,y,z in zip(mid,at[a],at[b])])
    need(exact==values,'literal two-stage Cayley/Hamilton polarization differs')


def structural(forest):
    allrows=forest['internal_nodes']+forest['leaves'];keys={(x['root'],x['path']) for x in allrows}
    need(len(keys)==len(allrows),'duplicate subdivision node')
    need(all((ri,'') in keys for ri in range(108)),'omitted quotient face/shell root')
    for row in forest['internal_nodes']:
        need((row['root'],row['path']+'0') in keys and (row['root'],row['path']+'1') in keys,'omitted closed bisection child')


def negative_controls(forest,example,domain):
    controls=[]
    for title,mutation in [
        ('omit complete shell root',lambda f: f['internal_nodes'].__setitem__(slice(None),[x for x in f['internal_nodes'] if x['root']!=0]) or f['leaves'].__setitem__(slice(None),[x for x in f['leaves'] if x['root']!=0])),
        ('omit a closed leaf child',lambda f:f['leaves'].pop(next(i for i,x in enumerate(f['leaves']) if x['path']))),
        ('duplicate literal subdivision leaf',lambda f:f['leaves'].append(copy.deepcopy(f['leaves'][0])))] :
        bad=copy.deepcopy(forest);mutation(bad)
        try:structural(bad)
        except ValueError as e:controls.append({'control':title,'rejection':str(e)});continue
        raise ValueError('coverage damage accepted')
    cut,T=example;bad=copy.copy(cut);bad['v']=neg(cut['v'])
    need(any(x<=Z for x in coefficients(bad,T,domain)),'wrong actual antipodal source accepted as same witness')
    controls.append({'control':'replace actual source by its antipodal original','rejection':'same cut leaf has a nonpositive actual coefficient'})
    need(Q(9,8)**2*392/4>1,'unsupported half-unit local collar accepted')
    controls.append({'control':'unsupported local collar1/2','rejection':'exact uniform squared closure exceeds one'})
    # Actual central equal-shadow branch is outside the local gate and inside D;
    # removing central-shadow gauge comparisons cannot establish source isolation.
    r=tuple(sum((x[j] for x in domain['R']),Z)/3 for j in range(3));c=(-r[1],r[0],Z);c2=dot(c,c);V=DATA['V']
    plane=(-r[1],r[0],Z);second=cross(r,plane)
    original={(dot(plane,v),dot(second,v)) for v in V};rotated=set()
    for v in V:
        t=tuple(((1-c2)*v[j]+2*c[j]*dot(c,v)+2*cross(c,v)[j])/(1+c2) for j in range(3))
        rotated.add((dot(plane,t),dot(second,t)))
    need(original==rotated and c2>F(Q(1,625)),'literal central companion negative control differs')
    need(all(dot(n,c)<=DATA['height'] for n in DATA['normals']),'central companion is outside nearest-body chart')
    kz=(Z,Z,Z,O);L=dot(r,kz[1:])+dot(cross(kz[1:],r),c)
    need(L*L>dot(r,r),'actual central companion not excluded by closest-shadow gauge')
    controls.append({'control':'drop central-shadow comparisons or omit H_n G equality branches',
                     'rejection':'actual nonzero body-chart equal shadow survives; closest-shadow gauge excludes this representative'})
    return controls

