#!/usr/bin/env python3
"""Two exact eight-active physical fixtures; generator uses FLINT, checker Q[t]."""
import argparse
from fractions import Fraction as F
from itertools import combinations
from math import lcm
import json
from pathlib import Path
import common as C
X=C.X;HERE=Path(__file__).resolve().parent
Q=[-1,0,21]
DIGITS=((0,0),(1,0),(0,1))


def pack(a,b):
    vals=[F(str(v)) for v in list(a)+[0]*(2-len(a))+list(b)+[0]*(2-len(b))]
    den=lcm(*(v.denominator for v in vals))
    return [int(v*den) for v in vals]+[den]


def produce():
    from flint import fmpq_poly as P
    q=P(Q);zero=P([]);one=P([1])
    def mul(u,v):return ((u[0]*v[0]-u[1]*v[1])%q,(u[0]*v[1]+u[1]*v[0]+u[1]*v[1])%q)
    examples=[]
    for sign,word in ((1,[1,0,1,1,2]),(-1,[1,0,1,2,2])):
        z=(P([-sign,-7*sign])/4,P([0,7*sign])/2);ps=[(one,zero)]
        for _ in range(4):ps.append(mul(ps[-1],z))
        vertices=[]
        for label in C.LABELS:
            a,b=zero,zero
            for j,d in enumerate(label):
                u,v=mul(ps[j],(P([DIGITS[d][0]]),P([DIGITS[d][1]])));a+=u;b+=v
            vertices.append(pack(a,b))
        examples.append({'sign':sign,'vertices':vertices,'colour_word':word})
    return {'schema':'hn-radix-first-anchor-physical-v1','real_parameter_polynomial':Q,
            'isolating_interval':['1/5','1/4'],'examples':examples}


def unpack(row):
    X.need(len(row)==5 and all(type(a)is int for a in row) and row[4]>0,'rational coordinate encoding')
    return [F(a,row[4]) for a in row[:2]],[F(a,row[4]) for a in row[2:4]]


def reduced(poly):return X.rem(poly,Q)


def run(path):
    import verify
    data=json.loads(Path(path).read_text());X.need(data['schema']=='hn-radix-first-anchor-physical-v1','fixture schema')
    X.need(data['real_parameter_polynomial']==Q and data['isolating_interval']==['1/5','1/4'],'specified positive embedding')
    X.need(X.is_prime(11) and Q[-1]%11 and all(sum(c*a**i for i,c in enumerate(Q))%11 for a in range(11)),'irreducible quadratic modulo 11')
    X.need(X.root_count(Q,F(1,5),F(1,4))==1,'unique isolated positive real root')
    X.need([e['sign'] for e in data['examples']]==[1,-1],'two physical representatives')
    _,factors,circle,monos,rowids=verify.V.reconstruct_inventory();results=[]
    for example in data['examples']:
        sign=example['sign'];vertices=example['vertices'];word=example['colour_word']
        X.need(len(vertices)==243 and len(word)==5 and all(type(v)is int and 0<=v<3 for v in word),'complete fixture vertices and colours')
        coords=list(map(unpack,vertices));hp=C.powers(C.H,4)
        # Independently check every coordinate from z=2st/(1-st), using its
        # real denominator and the original digit word, not generator powers.
        for label,(a,b) in zip(C.LABELS,coords):
            row=tuple(DIGITS[d] for d in label)
            if not any(label):na,nb=[],[];k=0
            else:na,nb=C.real_denominator_row(row,sign);k=max(j for j,d in enumerate(label) if d)
            X.need(not reduced(X.add(X.mul(a,hp[k]),na,-1)) and not reduced(X.add(X.mul(b,hp[k]),nb,-1)),'exact physical coordinate')
        colours=[sum(w*a for w,a in zip(word,label))%3 for label in C.LABELS]
        edges=[];active=set()
        for i,j in combinations(range(243),2):
            a=X.add(coords[i][0],coords[j][0],-1);b=X.add(coords[i][1],coords[j][1],-1)
            X.need(reduced(a) or reduced(b),'all physical vertices distinct')
            # 4|a+b*omega|^2=(2a+b)^2+3b^2; t is real.
            real=X.add([2*v for v in a],b)
            norm4=reduced(X.add(X.mul(real,real),X.mul(b,b),3))
            if norm4==[F(4)]:
                X.need(colours[i]!=colours[j],'proper actual physical unit edge');edges.append((i,j))
                owner=verify.V.edge_owner(i,j,monos,rowids,circle)
                if owner!='base':active.add(owner)
        X.need(all(e in edges for e in ((0,81),(0,162),(81,162))),'physical unit triangle')
        restricted={c for c,f in enumerate(factors) if not reduced(C.bivariate_pull(f,sign))}
        X.need(active==restricted and len(active)==8,'all eight active curves match exact physical edges')
        results.append({'sign':sign,'vertices':243,'unit_edges':len(edges),'edge_sha256':X.digest(edges),
                        'coordinates_sha256':X.digest(vertices),'active_curves':sorted(active),'colour_word':word,'chromatic_number':3})
    return {'verified':True,'physical_pair_checks':58806,'examples':results,'record_improvement':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--produce',type=Path);p.add_argument('--fixture',type=Path,default=HERE/'physical.json');p.add_argument('--check-expected',action='store_true');a=p.parse_args()
    if a.produce:
        with a.produce.open('x') as f:json.dump(produce(),f,sort_keys=True,separators=(',',':'));f.write('\n')
    else:
        result=run(a.fixture)
        if a.check_expected:X.need(result==json.loads((HERE/'PHYSICAL_EXPECTED.json').read_text()),'expected physical graphs')
        print(json.dumps(result,indent=2,sort_keys=True))
