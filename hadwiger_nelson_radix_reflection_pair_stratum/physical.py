#!/usr/bin/env python3
"""Independent Cartesian/Fraction verification of the quartic physical fixtures."""
import argparse,json,math
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import colour as C
X=C.X;V=C.V;HERE=Path(__file__).resolve().parent


def poly_at(cs,x):
    value=F(0)
    for c in reversed(cs):value=value*x+F(c)
    return value


class Embedding:
    def __init__(self,q,interval):
        self.q=q;self.interval=list(map(F,interval))
        a,b=self.interval
        X.need(a<b and poly_at(q,a)*poly_at(q,b)<0 and X.root_count(q,a,b)==1,'one simple isolated real embedding')
    def sign(self,cs):
        cs=list(map(F,cs))
        if not cs:return 0
        # All nonzero degree<4 polynomials are nonzero at this root, by
        # the separately checked irreducibility. Bisection therefore ends.
        while True:
            a,b=self.interval;lo=hi=F(0)
            for c in reversed(cs):
                products=(lo*a,lo*b,hi*a,hi*b);lo,hi=min(products)+c,max(products)+c
            if lo>0:return 1
            if hi<0:return -1
            mid=(a+b)/2
            if poly_at(self.q,a)*poly_at(self.q,mid)<0:self.interval[1]=mid
            else:self.interval[0]=mid


class Arithmetic:
    def __init__(self,q,T,R):
        self.q=q;self.T=list(map(F,T));self.R=list(map(F,R))
        self.D=self.scale(self.sub(self.scale(self.R,4),self.mul(self.T,self.T)),F(1,12))
    def red(self,a):return X.rem(a,self.q)
    def add(self,a,b):return self.red(X.add(a,b))
    def sub(self,a,b):return self.red(X.add(a,b,-1))
    def scale(self,a,c):return self.red([v*c for v in a])
    def mul(self,a,b):return self.red(X.mul(a,b))
    def ya(self,a,b):return self.add(a[0],b[0]),self.add(a[1],b[1])
    def ys(self,a,b):return self.sub(a[0],b[0]),self.sub(a[1],b[1])
    def ym(self,a,b):
        return self.add(self.mul(a[0],b[0]),self.mul(self.D,self.mul(a[1],b[1]))),self.add(self.mul(a[0],b[1]),self.mul(a[1],b[0]))
    def yc(self,a,c):return self.scale(a[0],c),self.scale(a[1],c)
    def cm(self,a,b):
        return self.ys(self.ym(a[0],b[0]),self.yc(self.ym(a[1],b[1]),3)),self.ya(self.ym(a[0],b[1]),self.ym(a[1],b[0]))
    def iszero(self,value,embedding):
        a,b=value
        if not b:return not a
        if self.sub(self.mul(a,a),self.mul(self.D,self.mul(b,b))):return False
        # a+b*y=0 with y positive iff a*b<0, once a²=D*b².
        # This also handles a split quadratic extension without assuming
        # irreducibility of y²-D in the quartic field.
        return embedding.sign(self.mul(a,b))<0


def run(path):
    data=json.loads(Path(path).read_text());X.need(data['schema']=='hn-radix-reflection-pair-physical-v1','physical schema')
    q=data['q'];p=data['irreducibility_prime'];x=[0,1]
    X.need(len(q)==5 and all(type(v)is int for v in q) and math.gcd(*q)==1 and q[-1]>1,'primitive nonmonic quartic')
    X.need(type(p)is int and X.is_prime(p) and q[-1]%p,'degree-preserving prime')
    X.need(X.gcd_is_one(q,X.add(X.power_mod(x,p*p,q,p),x,-1),p),'quartic has no factors of degree one or two')
    X.need(X.trim(X.power_mod(x,p**4,q,p))==x,'quartic Frobenius criterion')
    A=Arithmetic(q,data['trace'],data['radius'])
    X.need(not A.sub(A.add(A.T,A.R),x),'u equals physical trace plus radius')
    embeddings=[Embedding(q,e['isolating_interval']) for e in data['embeddings']]
    X.need(len(embeddings)==X.root_count(q)==2 and embeddings[0].interval[1]<embeddings[1].interval[0],'both real quartic embeddings covered')
    for E in embeddings:
        X.need(E.sign(A.R)>0 and E.sign(A.D)>0,'physical nonreal point with positive radius')
        X.need(E.sign(A.sub(A.R,[1]))!=0 and E.sign(A.sub(A.R,A.mul(A.T,A.T)))!=0,'outside radial circle and remaining reflection axes')
        r2,t2,rt=A.mul(A.R,A.R),A.mul(A.T,A.T),A.mul(A.R,A.T)
        for f in (A.sub(r2,t2),A.sub(A.add(A.add(r2,rt),t2),A.scale(A.R,3)),A.sub(A.add(A.sub(r2,rt),t2),A.scale(A.R,3))):
            X.need(E.sign(f)!=0,'outside all six first-step anchor circles')
    zero=([],[]);one=([F(1)],[]);half=([F(1,2)],[])
    z=((A.scale(A.T,F(1,2)),[]),([],[F(1)]));powers=[(one,zero)]
    for _ in range(4):powers.append(A.cm(powers[-1],z))
    digits=((zero,zero),(one,zero),(half,half))
    vertices=data['vertices'];X.need(len(vertices)==243,'complete physical vertex list');coords=[]
    for label,packed in zip(V.LABELS,vertices):
        X.need(len(packed)==17 and all(type(v)is int for v in packed) and packed[-1]>0,'rational quartic coordinate encoding')
        parts=[A.red([F(v,packed[-1]) for v in packed[k:k+4]]) for k in (0,4,8,12)]
        ea=(parts[0],parts[1]);eb=(parts[2],parts[3])
        point=(A.ya(ea,A.yc(eb,F(1,2))),A.yc(eb,F(1,2)))
        actual=(zero,zero)
        for j,d in enumerate(label):
            term=A.cm(powers[j],digits[d]);actual=(A.ya(actual[0],term[0]),A.ya(actual[1],term[1]))
        X.need(actual==point,'independent exact Cartesian coordinates');coords.append(point)
    word=data['colour_word'];X.need(len(word)==5 and all(type(v)is int and 0<=v<3 for v in word),'explicit three-colour word')
    colours=[sum(w*d for w,d in zip(word,label))%3 for label in V.LABELS]
    _,factors,circle,monos,rowids=V.reconstruct_inventory();edges=[[] for E in embeddings];active=[set() for E in embeddings];cache={}
    X.need(all(a*a+a*b+b*b==1 for a,b in V.UNITS),'canonicalizing units preserve physical norm')
    for i,j in combinations(range(243),2):
        raw=tuple((V.DIGITS[a][0]-V.DIGITS[b][0],V.DIGITS[a][1]-V.DIGITS[b][1]) for a,b in zip(V.LABELS[i],V.LABELS[j]))
        row=V.canonical_row(raw)
        if row not in cache:
            dx,dy=A.ys(coords[i][0],coords[j][0]),A.ys(coords[i][1],coords[j][1])
            squared=A.ya(A.ym(dx,dx),A.yc(A.ym(dy,dy),3));minus_one=A.ys(squared,one)
            cache[row]=[(A.iszero(squared,E),A.iszero(minus_one,E)) for E in embeddings]
        for k,(collision,unit) in enumerate(cache[row]):
            X.need(not collision,'all 243 physical points distinct')
            if unit:
                X.need(colours[i]!=colours[j],'proper actual unit edge');edges[k].append((i,j));owner=V.edge_owner(i,j,monos,rowids,circle)
                if owner!='base':active[k].add(owner)
    X.need(len(cache)==2801,'all canonical physical displacement classes')
    results=[]
    for k,claim in enumerate(data['embeddings']):
        X.need(all(e in edges[k] for e in ((0,81),(0,162),(81,162))),'physical unit triangle')
        X.need(len(edges[k])==claim['unit_edges'] and X.digest(edges[k])==claim['edge_sha256'] and sorted(active[k])==claim['active_curves'],'complete exact edge sets and active curves')
        X.need({257,2133}.issubset(active[k]),'normalized source pair is physically active')
        results.append({'vertices':243,'unit_edges':len(edges[k]),'active_curves':sorted(active[k]),'edge_sha256':X.digest(edges[k]),'chromatic_number':3,'isolating_interval':claim['isolating_interval']})
    return {'verified':True,'physical_point_pair_decisions':58806,'canonical_displacement_classes':2801,
            'coordinate_sha256':X.digest(vertices),'quartic_irreducibility_prime':p,'all_real_quartic_embeddings':True,
            'outside_previously_closed_radial_reflection_and_anchor_loci':True,'nonintegral_parameter_implies_no_collision':True,
            'examples':results,'record_improvement':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--fixture',type=Path,default=HERE/'physical.json');p.add_argument('--check-expected',action='store_true');a=p.parse_args()
    result=run(a.fixture)
    if a.check_expected:X.need(result==json.loads((HERE/'PHYSICAL_EXPECTED.json').read_text()),'expected exact physical decisions')
    print(json.dumps(result,indent=2,sort_keys=True))
