#!/usr/bin/env python3
"""Exact H21 triangle-isometry union in the power basis of zeta_42.

The field arithmetic and H formulas derive from the earlier heptagon
difference package. This is a new assembly, not a sum or a ball extraction.
Only Python's standard library is required.
"""
import argparse
from fractions import Fraction as Q
from itertools import permutations,combinations
import json
from math import lcm
from pathlib import Path

PHI=(1,1,0,-1,-1,0,1,0,-1,-1,0,1,1)
ZERO=(0,)*12;ONE=(1,)+(0,)*11
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,c):return tuple(c*x for x in a)
def reduce(v):
    v=list(v)+[0]*max(0,12-len(v))
    for j in range(len(v)-1,11,-1):
        for k in range(12):v[j-12+k]-=v[j]*PHI[k]
    return tuple(v[:12])
def mul(a,b):
    v=[0]*23
    for i,x in enumerate(a):
        for j,y in enumerate(b):v[i+j]+=x*y
    return reduce(v)
POW=tuple(reduce([0]*j+[1]) for j in range(42))
def conj(a):
    out=ZERO
    for i,x in enumerate(a):out=add(out,scale(POW[-i%42],x))
    return out
def norm(a):return mul(a,conj(a))
def inverse(a):
    columns=[mul(a,POW[j]) for j in range(12)]
    mat=[[Q(columns[j][i]) for j in range(12)]+[Q(i==0)] for i in range(12)]
    for j in range(12):
        k=next(i for i in range(j,12) if mat[i][j])
        mat[j],mat[k]=mat[k],mat[j]
        u=mat[j][j];mat[j]=[x/u for x in mat[j]]
        for i in range(12):
            if i!=j:
                u=mat[i][j];mat[i]=[x-u*y for x,y in zip(mat[i],mat[j])]
    out=tuple(row[-1] for row in mat)
    if mul(a,out)!=ONE:raise ValueError('inverse')
    return out
def seed():
    p=inverse(sub(POW[24],POW[18]))
    q=scale(mul(POW[35],inverse(sub(POW[6],POW[36]))),-1)
    r=scale(mul(POW[7],inverse(sub(POW[12],POW[30]))),-1)
    return [mul(a,POW[6*j]) for a in [p,q,r] for j in range(7)]

def build():
    H=seed();copies=[];maps=[]
    for j in range(7):
        tri=(j,j+7,j+14);a,b,c=(H[i] for i in tri);v=sub(b,a)
        for perm in permutations(tri):
            aa,bb,cc=(H[i] for i in perm);w=sub(bb,aa)
            for reflect in (False,True):
                vv=conj(v) if reflect else v
                alpha=mul(w,conj(vv))
                def image(z):
                    delta=sub(z,a)
                    return add(aa,mul(alpha,conj(delta) if reflect else delta))
                if image(c)==cc:
                    if norm(alpha)!=ONE:raise ValueError('isometry')
                    cp=[image(z) for z in H]
                    if perm!=tri:
                        copies.append(cp);maps.append({'triangle':j,'permutation':list(perm),'reflection':reflect})
                    elif cp!=H:raise ValueError('identity image')
                    break
            else:raise ValueError('triangle map incomplete')
    points=sorted(set(H).union(*(set(cp) for cp in copies)))
    denominator=lcm(*(x.denominator if isinstance(x,Q) else 1 for z in points for x in z))
    V=[tuple(int(x*denominator) for x in z) for z in points]
    p=1009
    t=next(r for r in range(2,p) if pow(r,42,p)==1 and all(pow(r,k,p)!=1 for k in [1,2,3,6,7,14,21]))
    ev=lambda z,r:sum(a*pow(r,i,p) for i,a in enumerate(z))%p
    pos=[ev(z,t) for z in V];neg=[ev(z,pow(t,-1,p)) for z in V]
    E=[];survivors=0
    for i,j in combinations(range(len(V)),2):
        if (pos[i]-pos[j])*(neg[i]-neg[j])%p!=denominator**2%p:continue
        survivors+=1
        if norm(sub(V[i],V[j]))==scale(ONE,denominator**2):E.append([i,j])
    index={z:i for i,z in enumerate(points)}
    return {'denominator':denominator,'coordinates':V,'edges':E,
            'seed_indices':[index[z] for z in H],
            'copies':[[index[z] for z in cp] for cp in copies],'maps':maps,
            'filter':{'prime':p,'root':t,'survivors':survivors}}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    g=build();args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'graph.json').write_text(json.dumps(g,separators=(',',':'))+'\n')
    print(json.dumps({'vertices':len(g['coordinates']),'edges':len(g['edges']),
                      'nonidentity_copies':len(g['copies']),'denominator':g['denominator']}))
if __name__=='__main__':main()
