"""Independent definition-level multiset audit of the recombination CNF."""
import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

HERE=Path(__file__).resolve().parent
N=537
NAMES=('W','190','359','best3','347')


def audit(cnf):
    sources=json.loads((HERE/'sources.json').read_text(encoding='ascii'))
    assert tuple(sources)==NAMES
    expected_hashes={
        'W':'58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3',
        'best3':'73e5780b9163f79d0bba3a63bfb327561b83e944cb0b8f3064c140d2dacdbf49',
    }
    aligned=[]
    source_defects={}
    for name,row in sources.items():
        word=row['word']
        assert len(word)==N and set(word)==set('123456')
        assert len(row['permutation'])==6 and set(row['permutation'])==set('123456')
        if name in expected_hashes:
            assert hashlib.sha256((word+'\n').encode('ascii')).hexdigest()==expected_hashes[name]
        bad=[]
        for z in range(2,N+1):
            for x in range(1,z//2+1):
                y=z-x
                if word[x-1]==word[y-1]==word[z-1]:
                    bad.append([x,y,z])
        assert bad==row['expected_bad'],(name,bad)
        source_defects[name]=len(bad)
        aligned.append([int(row['permutation'][int(d)-1]) for d in word])
    domains=[()] + [tuple(sorted({word[v-1] for word in aligned}))
                    for v in range(1,N+1)]
    variables={}
    for v in range(1,N+1):
        for c in domains[v]:
            variables[v,c]=len(variables)+1
    expected=Counter()
    for v in range(1,N+1):
        choices=tuple(variables[v,c] for c in domains[v])
        expected[choices]+=1
        for a,b in combinations(choices,2):
            expected[-a,-b]+=1
    triple_count=0
    doubling=0
    constrained=0
    schur_count=0
    for z in range(2,N+1):
        for x in range(1,z//2+1):
            y=z-x
            triple_count+=1
            if x==y: doubling+=1
            support=sorted({x,y,z})
            common=set.intersection(*(set(domains[v]) for v in support))
            if common: constrained+=1
            for c in sorted(common):
                clause=tuple(-variables[v,c] for v in support)
                expected[clause]+=1
                schur_count+=1
    assert triple_count==72092 and doubling==268
    actual=Counter()
    with Path(cnf).open(encoding='ascii') as stream:
        assert stream.readline().split()==['p','cnf',str(len(variables)),
                                            str(sum(expected.values()))]
        for line in stream:
            row=tuple(map(int,line.split()))
            assert row and row[-1]==0
            clause=row[:-1]
            assert all(1<=abs(lit)<=len(variables) for lit in clause)
            actual[clause]+=1
    assert actual==expected,(sum((expected-actual).values()),
                             sum((actual-expected).values()))
    histogram=[sum(len(d)==k for d in domains[1:]) for k in range(1,7)]
    assert histogram==[2,112,285,134,4,0]
    assert constrained==45807 and schur_count==58292
    print(f'PASS sources=5 source_defects={source_defects} '
          f'triples={triple_count} doubling={doubling} '
          f'variables={len(variables)} clauses={sum(actual.values())} '
          f'domain_histogram={histogram} exact_clause_multiset=yes',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--cnf',type=Path,required=True)
    audit(p.parse_args().cnf)
