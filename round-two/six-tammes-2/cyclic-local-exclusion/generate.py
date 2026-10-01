#!/usr/bin/env python3
"""Derive an invariant exact stress and propose a rational inverse.

Only the standard library is used. Floating-point elimination chooses contact
rows and proposes inverse entries; check.py certifies the resulting artifact.
"""
import argparse
import json
import math
from pathlib import Path
import check as c


def inverse(p):
    """Exact multiplication-matrix inversion in Q[t]/(F)."""
    cols = [c.mul(p, tuple(c.Q(i==j) for i in range(5))) for j in range(5)]
    A = [[cols[j][i] for j in range(5)]+[c.Q(i==0)] for i in range(5)]
    for k in range(5):
        pivot = next((i for i in range(k,5) if A[i][k]), None)
        c.require(pivot is not None, 'exact field inversion pivot')
        A[k], A[pivot] = A[pivot], A[k]
        z = A[k][k]
        A[k] = [x/z for x in A[k]]
        for i in range(5):
            if i != k:
                z = A[i][k]
                A[i] = [x-z*y for x,y in zip(A[i],A[k])]
    out = tuple(row[-1] for row in A)
    c.require(c.mul(p,out) == c.ONE, 'exact field inverse identity')
    return out


def generate():
    H = tuple(tuple(c.ONE if i==j else c.T for j in range(3)) for i in range(3))
    a = tuple(map(c.Q,('-27/2','-3','35','-24','117/2')))
    b = tuple(map(c.Q,('-31/4','-19/2','34','-53/2','195/4')))
    d = tuple(map(c.Q,('81/4','21/2','-69','101/2','-429/4')))
    M = ((a,b,d),(d,a,b),(b,d,a))
    # H^{-1}=(1-t)^{-1}I-t/((1-t)(1+2t))J.
    u = inverse(c.sub(c.ONE,c.T))
    v = c.mul(c.T,inverse(c.mul(c.sub(c.ONE,c.T),c.add(c.ONE,c.scale(c.T,c.Q(2))))))
    C = [[c.sub(c.mul(u,M[i][j]),c.mul(v,c.vsum(M[k][j] for k in range(3))))
          for j in range(3)] for i in range(3)]
    V = {i:tuple(c.ONE if k==j else c.ZERO for k in range(3))
         for j,i in enumerate((0,5,11))}
    for j,i in enumerate((1,2,4)):
        V[i] = tuple(C[k][j] for k in range(3))
    r = c.mul(c.scale(c.T,c.Q(2)),inverse(c.add(c.ONE,c.T)))
    for n,i,j,o in ((6,0,11,5),(7,0,5,11),(9,5,11,0),(14,0,6,11),
                    (12,5,7,0),(13,11,9,5),(3,1,4,2),(8,2,4,1),(10,1,2,4)):
        V[n] = tuple(c.sub(c.mul(r,c.add(x,y)),z) for x,y,z in zip(V[i],V[j],V[o]))
    V = [V[i] for i in range(15)]
    HV = [c.matvec(H,v) for v in V]
    edges = [(i,j) for i in range(15) for j in range(i+1,15) if c.dot(V[i],HV[j])==c.T]
    c.require(len(edges)==30, 'thirty contacts in the derived cyclic packing')
    permutation = list(range(15))
    for cycle in ((0,5,11),(1,2,4),(6,7,9),(14,12,13),(3,10,8)):
        for i,j in zip(cycle,cycle[1:]+cycle[:1]):permutation[i]=j
    orbits=[];remaining=set(edges)
    while remaining:
        edge=min(remaining);orbit=[]
        while edge not in orbit:
            orbit.append(edge);edge=tuple(sorted((permutation[edge[0]],permutation[edge[1]])))
        c.require(len(orbit)==3 and set(orbit)<=remaining, 'contact orbit')
        orbits.append(orbit);remaining-=set(orbit)
    E=[[c.ZERO for _ in orbits] for _ in range(45)]
    for col,orbit in enumerate(orbits):
        for i,j in orbit:
            for k in range(3):
                E[3*i+k][col]=c.add(E[3*i+k][col],c.sub(V[j][k],c.mul(c.T,V[i][k])))
                E[3*j+k][col]=c.add(E[3*j+k][col],c.sub(V[i][k],c.mul(c.T,V[j][k])))
    A=[row[:] for row in E];pivots=[];row=0
    for col in range(len(orbits)):
        pivot=next((i for i in range(row,len(A)) if A[i][col]!=c.ZERO),None)
        if pivot is None:continue
        A[row],A[pivot]=A[pivot],A[row]
        z=inverse(A[row][col]);A[row]=[c.mul(x,z) for x in A[row]]
        for i in range(len(A)):
            if i!=row and A[i][col]!=c.ZERO:
                z=A[i][col];A[i]=[c.sub(x,c.mul(z,y)) for x,y in zip(A[i],A[row])]
        pivots.append(col);row+=1
    c.require(pivots==list(range(9)), 'rank-nine invariant equilibrium system')
    weights=[c.scale(A[i][9],c.Q(-1)) for i in range(9)]+[c.ONE]
    z=inverse(weights[3]);weights=[c.mul(x,z) for x in weights]
    byedge={edge:w for orbit,w in zip(orbits,weights) for edge in orbit}
    result={'vectors':[[list(map(str,p)) for p in v] for v in V],
            'edges':[list(e) for e in edges], 'orbits':[[list(e) for e in orbit] for orbit in orbits],
            'weights':[list(map(str,byedge[e])) for e in edges]}
    norm=[];contact=[];gauge=[]
    for i in range(15):
        row=[c.ZERO]*45;row[3*i:3*i+3]=HV[i];norm.append(row)
    for i,j in edges:
        row=[c.ZERO]*45;row[3*i:3*i+3]=HV[j];row[3*j:3*j+3]=HV[i];contact.append(row)
    for k in (1,2,17):
        row=[c.ZERO]*45;row[k]=c.ONE;gauge.append(row)
    def numeric(row):return [float(sum(c.interval(p))/2) for p in row]
    def residual(v,orth):
        v=v[:]
        for _ in range(2):
            for u in orth:
                z=sum(a*b for a,b in zip(v,u));v=[a-z*b for a,b in zip(v,u)]
        return v
    norm_float=list(map(numeric,norm));contact_float=list(map(numeric,contact));gauge_float=list(map(numeric,gauge))
    orth=[]
    for row in norm_float+gauge_float:
        v=residual(row,orth);s=math.sqrt(sum(x*x for x in v));orth.append([x/s for x in v])
    chosen=[]
    for _ in range(27):
        candidates=[]
        for k,row in enumerate(contact_float):
            if k not in chosen:
                v=residual(row,orth);s=sum(x*x for x in v);candidates.append((s,k,v))
        s,k,v=max(candidates);chosen.append(k);orth.append([x/math.sqrt(s) for x in v])
    chosen.sort();rows=norm_float+[contact_float[k] for k in chosen]+gauge_float
    R=[row+[float(i==j) for j in range(45)] for i,row in enumerate(rows)]
    for col in range(45):
        pivot=max(range(col,45),key=lambda i:abs(R[i][col]));R[col],R[pivot]=R[pivot],R[col]
        z=R[col][col];R[col]=[x/z for x in R[col]]
        for i in range(45):
            if i!=col:
                z=R[i][col];R[i]=[x-z*y for x,y in zip(R[i],R[col])]
    result.update(selected_edges=chosen,inverse_scale=10**8,
                  inverse_numerators=[[round(x*10**8) for x in row[45:]] for row in R])
    c.verify(result,False)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    data=generate()
    args.output.write_text(json.dumps(data,separators=(',',':'))+'\n')
    print(json.dumps(c.verify(data,False),sort_keys=True))
