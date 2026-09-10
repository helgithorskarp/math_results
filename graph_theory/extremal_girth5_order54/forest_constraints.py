"""Exact sparse necessary constraints for degree-class/type incidences."""
from fractions import Fraction
from itertools import combinations
from math import comb

def model(sizes=(17,24,13),edge_bounds=False):
    n=sum(sizes);types=[]
    for d in (6,7,8):
        if not sizes[d-6]:continue
        for a in range(d+1):
            for b in range(d-a+1):
                c=d-a-b;ns=(a,b,c)
                if 6*a+7*b+8*c>n-1:continue
                if any(ns[j]>sizes[j]-(d==j+6) for j in range(3)):continue
                types.append((d,ns))
    nt=len(types)
    edges=[(i,j) for i in range(nt) for j in range(i,nt)
           if types[i][1][types[j][0]-6] and types[j][1][types[i][0]-6]]
    eq=[];eb=[];ub=[];bb=[]
    for j in range(3):
        eq.append({i:1 for i,(d,ns) in enumerate(types) if d==j+6});eb.append(sizes[j])
    for a,b in combinations(range(3),2):
        eq.append({i:(d==a+6)*ns[b]-(d==b+6)*ns[a] for i,(d,ns) in enumerate(types)});eb.append(0)
    for a in range(3):
        ub.append({i:2*comb(ns[a],2)+(d==a+6)*ns[a] for i,(d,ns) in enumerate(types)});bb.append(2*comb(sizes[a],2))
    for a,b in combinations(range(3),2):
        ub.append({i:ns[a]*ns[b]+(d==a+6)*ns[b] for i,(d,ns) in enumerate(types)});bb.append(sizes[a]*sizes[b])
    for i,(d,ns) in enumerate(types):
        for a in range(3):
            eq.append({i:-ns[a]});eb.append(0)
            ub.append({i:ns[a]-sizes[a]-(d-1)*(d==a+6)});bb.append(0)
    for e,(i,j) in enumerate(edges,nt):
        di,ni=types[i];dj,nj=types[j]
        eq[6+3*i+dj-6][e]=1
        for a in range(3):ub[6+3*i+a][e]=nj[a]
        if i!=j:
            eq[6+3*j+di-6][e]=1
            for a in range(3):ub[6+3*j+a][e]=ni[a]
    if edge_bounds:
        m={i:Fraction(ns[2],2) for i,(d,ns) in enumerate(types) if d==8}
        ub.extend([{i:-x for i,x in m.items()},m]);bb.extend([-5,6])
    return types,edges,eq,eb,ub,bb

def evaluate(row,x):return sum(a*x[i] for i,a in row.items())
