#!/usr/bin/env python3
"""Definition-level identities, a sphere on the boundary, and encoder audits."""
import itertools as it
import json
import random
import tempfile
from pathlib import Path
from math import comb
from pysat.formula import IDPool
from pysat.solvers import Solver
from cases import enumerate_cases
from encoding import Model, build
from strict_rup import check as check_rup, InvalidProof


def faces(adj, available):
    yield ()
    def rec(S, mask):
        while mask:
            bit=mask&-mask; v=bit.bit_length()-1; mask^=bit
            T=S+(v,); yield T
            yield from rec(T,mask&~adj[v])
    yield from rec((),available)


def adjacency(edges,n=18):
    adj=[0]*n
    for u,v in edges: adj[u]|=1<<v; adj[v]|=1<<u
    return adj


def link_mask(adj,S):
    mask=(1<<len(adj))-1
    for v in S: mask&=~((1<<v)|adj[v])
    return mask


def rank(columns):
    pivots={}
    for c in columns:
        while c:
            p=c.bit_length()-1
            if p in pivots: c^=pivots[p]
            else: pivots[p]=c; break
    return len(pivots)


def reduced_betti(face_list):
    levels=[[] for _ in range(max(map(len,face_list))+1)]
    for S in face_list: levels[len(S)].append(S)
    ranks=[0]*(len(levels)+1)
    for k in range(1,len(levels)):
        index={S:i for i,S in enumerate(levels[k-1])}
        columns=[sum(1<<index[S[:j]+S[j+1:]] for j in range(k)) for S in levels[k]]
        ranks[k]=rank(columns)
    return [len(levels[k])-ranks[k]-ranks[k+1] for k in range(len(levels))]


def boundary_sphere():
    # A flag 2-sphere on nine vertices, then its join with a second copy.
    original={p for p in it.combinations(range(6),2) if p[0]//2!=p[1]//2}
    for new,(a,b) in enumerate([(0,2),(3,4),(1,5)],start=6):
        common=[u for u in range(new) if tuple(sorted((a,u))) in original
                and tuple(sorted((b,u))) in original]
        assert len(common)==2
        original.remove(tuple(sorted((a,b))))
        original.update(tuple(sorted((u,new))) for u in [a,b]+common)
    H={p for p in it.combinations(range(9),2) if p not in original}
    return H|{(u+9,v+9) for u,v in H}


def normalize(H):
    adj=adjacency(H); C={v for v in range(18) if adj[v].bit_count()==3}
    F=[S for S in faces(adj,(1<<18)-1) if len(S)==6]
    A=list(max(F,key=lambda S:len(set(S)&C)))
    A.sort(key=lambda v:adj[v].bit_count())
    B=[next(v for v in range(18) if v not in A and
            {a for a in A if adj[v]>>a&1}=={a}) for a in A]
    R=sorted(set(range(18))-set(A)-set(B)); k=len(set(A)&C)
    assert k==6  # This concrete boundary fixture has an all-cubic facet.
    for case in enumerate_cases():
        if case['k']!=k: continue
        target={tuple(row) for row in case['edges']}
        for p in it.permutations(range(6)):
            rows=[tuple(sorted(p[i] for i,r in enumerate(R) if adj[a]>>r&1)) for a in A]
            if set(rows)!=target: continue
            orderA=[rows.index(tuple(row)) for row in case['edges']]
            order=[A[i] for i in orderA]+[B[i] for i in orderA]
            order += [R[p.index(i)] for i in range(6)]
            mapping={v:i for i,v in enumerate(order)}
            return case,{tuple(sorted((mapping[u],mapping[v]))) for u,v in H}
    raise AssertionError('Fixture escaped the case classification')


def identities():
    rng=random.Random(20260924); checks=0
    pairs=list(it.combinations(range(18),2))
    for sample in range(256):
        threshold=(sample%17+1)/20
        H={p for p in pairs if rng.random()<threshold}; adj=adjacency(H)
        q=[x.bit_count() for x in adj]; M=len(H)
        T=sum(all(tuple(sorted(p)) in H for p in it.combinations(S,2))
              for S in it.combinations(range(18),3))
        f1=153-M
        f2=sum(all(p not in H for p in it.combinations(S,2))
               for S in it.combinations(range(18),3))
        a=f1-9*18+48; b=f2-6*f1+22*18-64
        assert a==39-M
        assert b==230+sum(x*(x-11)//2 for x in q)-T
        L=[]
        for v in range(18):
            ns=[u for u in range(18) if adj[v]>>u&1]
            tv=sum(p in H for p in it.combinations(ns,2))
            B=[u for u in range(18) if u!=v and not(adj[v]>>u&1)]
            lv=sum(p not in H for p in it.combinations(B,2))-7*len(B)+30
            assert lv==a+8+q[v]*(q[v]-19)//2+sum(q[u] for u in ns)-tv
            L.append(lv); checks+=1
        assert sum(L)==3*b+4*a
    return checks


def shell():
    m=Model.__new__(Model); m.pool=IDPool(); m.fixed={}; m.clauses=[]
    m.solver=None; m.done=set()
    vs=[m.pool.id(i) for i in range(5)]
    m.true=m.pool.id('true'); m.fix(m.true,True)
    return m,vs


def encoder_truth_tables():
    count=0
    # Signed literals, repeated terms, negative weights, fixed constants,
    # both inequality directions, and conditional cardinality bounds.
    for op in ('ge','le'):
        for bound in range(-4,10):
            m,vs=shell(); x,y,z,w,c=vs
            terms=[(2,x),(-3,-y),(1,z),(4,-z),(2,m.true),(-1,x)]
            m.pb(terms,bound,op)
            with Solver(name='glucose4',bootstrap_with=m.clauses) as s:
                for values in it.product((False,True),repeat=5):
                    val={v:values[i] for i,v in enumerate(vs)}; val[m.true]=True
                    total=sum(a*(val[abs(l)] if l>0 else not val[abs(l)]) for a,l in terms)
                    expected=total>=bound if op=='ge' else total<=bound
                    assert s.solve(assumptions=[v if val[v] else -v for v in vs])==expected
                    count+=1
        for bound in range(-1,6):
            m,vs=shell(); x,y,z,w,c=vs
            m.card([x,-y,z,m.true,-m.true],bound,op,[c])
            with Solver(name='glucose4',bootstrap_with=m.clauses) as s:
                for values in it.product((False,True),repeat=5):
                    val=dict(zip(vs,values)); total=val[x]+(not val[y])+val[z]+1
                    expected=val[c] or (total>=bound if op=='ge' else total<=bound)
                    assert s.solve(assumptions=[v if val[v] else -v for v in vs])==expected
                    count+=1
    return count


def checker_controls():
    controls=[
        ('p cnf 1 2\n1 0\n-1 0\n','3 0 1 2 0\n',True),
        ('p cnf 1 2\n1 0\n-1 0\n','3 0 0\n',False),
        ('p cnf 1 1\n1 0\n','2 0 0\n',False),
        ('p cnf 2 1\n1 2 0\n','2 0 1 0\n',False),
        ('p cnf 1 1\n1 0\n','2 -1 0 1 0\n',False),
        ('p cnf 1 2\n1 0\n-1 0\n','3 d 1 0\n4 0 1 2 0\n',False),
        ('p cnf 1 2\n1 0\n-1 0\n','3 1 0 1 0\n',False),
        ('p cnf 1 2\n1 0\n-1 0\n','3 0 -1 2 0\n',False),
    ]
    with tempfile.TemporaryDirectory(prefix='cd18-rup-') as name:
        cnf=Path(name)/'test.cnf';proof=Path(name)/'test.lrat'
        for text,trace,expected in controls:
            cnf.write_text(text);proof.write_text(trace)
            try: accepted=check_rup(cnf,proof)['verified']
            except InvalidProof: accepted=False
            assert accepted==expected
    return {'valid_accepted':1,'invalid_rejected':7}


def main():
    case,H=normalize(boundary_sphere()); adj=adjacency(H)
    all_faces=list(faces(adj,(1<<18)-1)); f=[sum(len(S)==k for S in all_faces) for k in range(7)]
    assert f==[1,18,123,406,693,588,196]
    for S in all_faces:
        betti=reduced_betti(list(faces(adj,link_mask(adj,S))))
        expected=[0]*(7-len(S)); expected[-1]=1
        assert betti==expected
    # The graph also satisfies the nonsuspension-derived common-neighbor bound.
    C=[v for v in range(18) if adj[v].bit_count()==3]
    assert all((adj[u]&adj[v]).bit_count()<=1 for u,v in it.combinations(C,2) if (u,v) not in H)
    m=build(case['edges'],positive=True)
    with Solver(name='glucose4',bootstrap_with=m.clauses) as s:
        assert s.solve(assumptions=[e if p in H else -e for p,e in m.edges.items()])
    bad=build(case['edges'])
    with Solver(name='glucose4',bootstrap_with=bad.clauses) as s:
        assert not s.solve(assumptions=[e if p in H else -e for p,e in bad.edges.items()])
    result={'cases':len(enumerate_cases()),'labelled_patterns':3471,
            'identity_vertex_checks':identities(),'encoder_truth_assignments':encoder_truth_tables(),
            'strict_checker_controls':checker_controls(),
            'boundary_fixture_case':case['id'],'boundary_f_vector_with_empty':f,
            'boundary_gamma':[1,6,9,0],'homology_links_checked_over_F2':len(all_faces),
            'positive_cnf':'SAT','negative_cnf_fixed_fixture':'UNSAT'}
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
