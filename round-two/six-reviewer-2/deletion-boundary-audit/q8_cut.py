"""Independent invariant-coordinate Rayleigh witness for the q8 cap.

This reconstructs a new witness from actual matrices. It does not read a
researcher vector or invoke an optimizer, solver or unpublished engine.
"""
from fractions import Fraction as F
from math import gcd,lcm
import json
import core as c
from cases import base

def negative_column(G):
    n=len(G);B=[row[:] for row in G]
    columns=[[F(i==j) for j in range(n)] for i in range(n)]
    while B:
        m=len(B)
        neg=next((i for i in range(m) if B[i][i]<0),None)
        if neg is not None:return columns[neg]
        p=max(range(m),key=lambda i:B[i][i]);d=B[p][p]
        if d==0:
            pair=next(((i,j) for i in range(m) for j in range(i+1,m) if B[i][j]),None)
            c.need(pair is not None,'no negative direction in the selected Gram')
            i,j=pair;sign=-1 if B[i][j]>0 else 1
            return [a+sign*b for a,b in zip(columns[i],columns[j])]
        ix=[i for i in range(m) if i!=p]
        ratios=[B[i][p]/d for i in ix]
        columns=[[a-ratio*b for a,b in zip(columns[i],columns[p])]
                 for i,ratio in zip(ix,ratios)]
        B=[[B[i][j]-ri*B[p][j] for j in ix] for i,ri in zip(ix,ratios)]
    raise ValueError('selected Gram is positive definite')

def record():
    sets,C,D,R,U,Sa,out=base(8,3);non=sets[1:];Z={3,4,5}
    def label(A):return int(0 in A),len(A&{1,2}),len(A&Z),len(A-({0,1,2}|Z))
    labels=sorted(set(map(label,non)))
    blocks=[[i for i,A in enumerate(non) if label(A)==v] for v in labels]
    G=[[sum(U[i][j] for i in left for j in right) for right in blocks] for left in blocks]
    coefficient=negative_column(G)
    # Compact exact rounding after the Schur direction is obtained. Each
    # candidate is accepted only by all original rational Rayleigh tests.
    scale=max(abs(v) for v in coefficient)
    if next(v for v in coefficient if v)<0:coefficient=[-v for v in coefficient]
    for resolution in [1,2,4,8,16,32,64,128,256,512,1024]:
        integers=[int(v*resolution/scale+F(1,2)) for v in coefficient]
        vector=[integers[labels.index(label(A))] for A in non]
        A=c.quad(U,vector);derivative=c.quad(D,vector);repair=c.quad(R,vector)
        if A<0 and derivative>0 and repair<0 and derivative/(-repair)>F(1,24):break
    else:raise ValueError('bounded exact compact witness search incomplete')
    common=gcd(*integers);integers=[v//common for v in integers]
    vector=[v//common for v in vector]
    A=c.quad(U,vector);derivative=c.quad(D,vector);repair=c.quad(R,vector)
    c.need(A<0 and derivative>0 and repair<0,'literal original negative cap Rayleigh witness')
    intercept=(-A)/(-repair);slope=derivative/(-repair)
    out.update({'coordinate_blocks':[{'signature':v,'size':len(ix),'coefficient':t}
                                   for v,ix,t in zip(labels,blocks,integers)],
        'rounding_resolution':resolution,'integer_original_vector':vector,'original_pairings':{'U0':A,'Delta':derivative,'R':repair},
        'necessary_real_halfplane':{'t_intercept':intercept,'kappa_coefficient':slope},
        'excludes_conventional_interval':derivative>0 and slope>F(1,24),
        'method':'Actual set-orbit Gram, exact rational Schur negative-column reconstruction, original-coordinate pairings.'})
    c.need(c.quad(G,[F(v) for v in integers])==A,'entire orbit-to-original Rayleigh bridge')
    return out

if __name__=='__main__':print(json.dumps(c.canonical(record()),sort_keys=True,indent=2))
