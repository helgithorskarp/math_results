#!/usr/bin/env python3
"""Standard-library verification of both rational bounds and finite coverage."""
from fractions import Fraction as F
from itertools import combinations,permutations,product
from pathlib import Path
from collections import Counter
import json
from forest_constraints import model,evaluate
from forest_profiles import profiles
from verify import graph,hoffman_singleton_edges,check_girth_and_identities

HERE=Path(__file__).resolve().parent
FORESTS={'5_0':[2]*5,'5_1':[3,2,2,2],'5_2a':[4,2,2],'5_2b':[3,3,2],
 '5_3a':[5,2],'5_3b':[4,3],'6_0':[2]*6,'6_1':[3,2,2,2,2],
 '6_2a':[4,2,2,2],'6_2b':[3,3,2,2]}

def certificate(upper=False):
    ts,es,eq,eb,ub,bb=model(edge_bounds=upper);nv=len(ts)+len(es)
    data=json.loads((HERE/('forest_degree2_certificate.json' if upper else 'forest_lower_certificate.json')).read_text())
    lhs=[F(0)]*nv;bound=F(0)
    for field,rows,rhs in [('equality_multipliers',eq,eb),('inequality_multipliers',ub,bb)]:
        for i,num in data[field]:
            a=F(num,data['denominator'])
            if field.startswith('inequality'):assert a<=0
            bound+=a*rhs[i]
            for j,b in rows[i].items():lhs[j]+=a*b
    objective=[F(0)]*nv;allowed=[True]*nv
    for i,(d,ns) in enumerate(ts):
        if d==8:
            objective[i]=F(ns[2],2)
            if upper:objective[i]=-objective[i]-(ns[2]==2)
            if ns[1]+2*ns[2]!=5:allowed[i]=False
    error=max([F(0)]+[a-b for a,b,ok in zip(lhs,objective,allowed) if ok])
    # sum of nonnegative variables <=54+374=428, by type counts and
    # degree-incidence balances; this pays for every coefficient error.
    corrected=bound-428*error
    assert str(error)==data['max_coefficient_error']
    assert str(bound)==data['uncorrected_bound']
    assert str(corrected)==data['corrected_bound']
    assert corrected>(-9 if upper else 4)
    return {'objective':'-(m+k)' if upper else 'm','variables':nv,'types':len(ts),'type_edges':len(es),'corrected_lower_bound':str(corrected),'maximum_coefficient_error':str(error)}

def graph_controls():
    out=[]
    hs=set(hoffman_singleton_edges());deleted=hs-{min(hs)}
    for G in [graph(50,hs),graph(50,deleted)]:
        e=check_girth_and_identities(G);ds=list(map(len,G));sizes=tuple(ds.count(d) for d in (6,7,8))
        ts,es,eq,eb,ub,bb=model(sizes);ti={t:i for i,t in enumerate(ts)}
        typ=[ti[(ds[v],tuple(sum(ds[u]==d for u in G[v]) for d in (6,7,8)))] for v in range(len(G))]
        x=[0]*(len(ts)+len(es));ei={pair:i+len(ts) for i,pair in enumerate(es)}
        for t in typ:x[t]+=1
        for u in range(len(G)):
            for v in G[u]:
                if u<v:
                    a,b=sorted((typ[u],typ[v]));x[ei[a,b]]+=2 if a==b else 1
        assert all(evaluate(r,x)==b for r,b in zip(eq,eb))
        assert all(evaluate(r,x)<=b for r,b in zip(ub,bb))
        assert sum(x)<=len(G)+2*e
        out.append({'n':len(G),'edges':e,'all_rows_satisfied':True})
    return out

def independent_rows(d,n,total,D):
    out=set();costs=[(c-3)*(c-4)//2 if d==6 else (c-1)*(c-2)//2 for c in range(d+1)]
    def rec(c,left,weight,cost,vector):
        if c==d+1:
            if left==0 and weight==total:out.add((cost,tuple(vector)))
            return
        if weight>total or weight+c*left>total or weight+d*left<total:return
        for count in range(left+1):
            q=cost+count*costs[c]
            if q<=D:rec(c+1,left-count,weight+c*count,q,vector+[count])
    rec(0,n,0,0,[]);return out

def coverage():
    counts={}
    for m in (5,6):
        for k in range(9-m):
            D=22-3*m-k
            a=independent_rows(6,17,39+2*m,D);b=independent_rows(7,24,65-4*m,D)
            expected={(x,y) for q,x in a for r,y in b if q+r==D}
            actual={(tuple(x),tuple(y)) for x,y in profiles(m,k)}
            assert actual==expected and len(actual)==len(profiles(m,k))
            counts[f'{m},{k}']=len(actual)
    def partitions(n,maximum):
        if n==0:yield [];return
        for p in range(min(n,maximum),0,-1):
            for tail in partitions(n-p,p):yield [p]+tail
    expected=set()
    for m in (5,6):
        for p in partitions(m,m):
            if m+(m-len(p))<=8:expected.add(tuple(x+1 for x in p))
    assert expected=={tuple(sorted(v,reverse=True)) for v in FORESTS.values()}
    return {'forests':10,'profiles_by_m_k':counts,'total_profiles':sum(len(profiles(sum(x-1 for x in L),sum(x-2 for x in L))) for L in FORESTS.values())}

def symmetry_control():
    # Exhaustive 3-by-4 incidence matrices, row group {0,1}, and the
    # full colored-column action of two interchangeable reversible edges.
    cols=[]
    for order in permutations((0,1)):
        for flips in product((0,1),repeat=2):
            cols.append([2*i+(b^flips[j]) for j,i in enumerate(order) for b in (0,1)])
    for bits in product((0,1),repeat=12):
        canon=min(tuple(bits[4*r+c] for r in rows for c in p) for rows in ((0,1,2),(1,0,2)) for p in cols)
        assert canon[:4]<=canon[4:8]
        blocks=[tuple(canon[4*r+c] for r in range(3) for c in C) for C in ((0,1),(2,3))]
        assert blocks[0]<=blocks[1]
        for C,B in zip(((0,1),(2,3)),blocks):assert B<=tuple(canon[4*r+c] for r in range(3) for c in C[::-1])
    return {'block_lex_matrices':4096}

def main():
    result={'certificates':[certificate(),certificate(True)],'graph_controls':graph_controls(),'coverage':coverage(),'symmetry_control':symmetry_control()}
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
