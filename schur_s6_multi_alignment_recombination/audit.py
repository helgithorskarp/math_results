"""Independent source and exact-clause audit for fixed alignment unions."""
import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

HERE=Path(__file__).resolve().parent
N=537


def domains_for(alignment,sources):
    aligned=[]
    for name,perm in alignment:
        word=sources[name]['word']
        assert len(word)==N and set(word)==set('123456')
        assert len(perm)==6 and set(perm)==set('123456')
        aligned.append([int(perm[int(d)-1]) for d in word])
    return [set()] + [{word[v-1] for word in aligned} for v in range(1,N+1)]


def audit(case,cnf):
    sources=json.loads((HERE/'sources.json').read_text(encoding='ascii'))
    cases=json.loads((HERE/'cases.json').read_text(encoding='ascii'))
    assert set(sources)=={'W','190','359','best3','347'}
    defects={}
    for name,row in sources.items():
        word=row['word']
        assert len(word)==N and set(word)==set('123456')
        bad=[]
        for z in range(2,N+1):
            for x in range(1,z//2+1):
                y=z-x
                if word[x-1]==word[y-1]==word[z-1]: bad.append([x,y,z])
        assert bad==row['expected_bad'],(name,bad)
        defects[name]=len(bad)
    assert hashlib.sha256((sources['W']['word']+'\n').encode()).hexdigest()==\
        '58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3'
    domains=domains_for(cases[case],sources)
    first=domains_for(cases['two_347_alignments'][:5],sources)
    two=domains_for(cases['two_347_alignments'],sources)
    assert all(first[v]<=two[v] for v in range(1,N+1))
    assert any(first[v]<two[v] for v in range(1,N+1))
    assert sum(len(two[v])-len(first[v]) for v in range(1,N+1))==81
    assert [v for v in range(1,N+1) if len(two[v])==1]==[17,62]
    if case!='two_347_alignments':
        assert all(two[v]<=domains[v] for v in range(1,N+1))
        assert any(two[v]<domains[v] for v in range(1,N+1))
    variable={}
    for v in range(1,N+1):
        for c in sorted(domains[v]): variable[v,c]=len(variable)+1
    expected=Counter()
    for v in range(1,N+1):
        positive=tuple(variable[v,c] for c in sorted(domains[v]))
        expected[positive]+=1
        for a,b in combinations(positive,2): expected[-a,-b]+=1
    triple_count=0
    doubling=0
    constrained=0
    schur_clauses=0
    for z in range(2,N+1):
        for x in range(1,z//2+1):
            y=z-x
            triple_count+=1
            doubling+=(x==y)
            support=sorted({x,y,z})
            common=set.intersection(*(domains[v] for v in support))
            if common: constrained+=1
            for c in sorted(common):
                expected[tuple(-variable[v,c] for v in support)]+=1
                schur_clauses+=1
    assert triple_count==72092 and doubling==268
    actual=Counter()
    with Path(cnf).open(encoding='ascii') as stream:
        header=stream.readline().split()
        assert header==['p','cnf',str(len(variable)),str(sum(expected.values()))]
        for line in stream:
            cl=tuple(map(int,line.split()))
            assert cl and cl[-1]==0
            assert all(1<=abs(lit)<=len(variable) for lit in cl[:-1])
            actual[cl[:-1]]+=1
    assert actual==expected,(sum((expected-actual).values()),
                             sum((actual-expected).values()))
    histogram=[sum(len(domains[v])==k for v in range(1,N+1))
               for k in range(1,7)]
    print(f'PASS case={case} sources=5 defects={defects} triples={triple_count} '
          f'doubling={doubling} variables={len(variable)} clauses={sum(actual.values())} '
          f'constrained_triples={constrained} schur_clauses={schur_clauses} '
          f'domain_histogram={histogram} exact_clause_multiset=yes',flush=True)
    return {'variables':len(variable),'clauses':sum(actual.values()),
            'constrained_triples':constrained,'schur_clauses':schur_clauses,
            'domain_histogram':histogram}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--case',required=True)
    p.add_argument('--cnf',type=Path,required=True)
    a=p.parse_args()
    audit(a.case,a.cnf)
