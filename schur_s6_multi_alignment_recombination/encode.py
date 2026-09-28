"""Exact CNF for positionwise choices among several aligned near-colourings."""
import argparse
import json
from itertools import combinations
from pathlib import Path

HERE=Path(__file__).resolve().parent
N=537


def make(case):
    sources=json.loads((HERE/'sources.json').read_text(encoding='ascii'))
    cases=json.loads((HERE/'cases.json').read_text(encoding='ascii'))
    alignment=cases[case]
    aligned=[]
    for name,perm in alignment:
        word=sources[name]['word']
        assert len(word)==N and set(word)==set('123456')
        assert len(perm)==6 and set(perm)==set('123456')
        aligned.append(''.join(perm[int(d)-1] for d in word))
    domains=[()] + [tuple(sorted({int(word[v-1]) for word in aligned}))
                    for v in range(1,N+1)]
    var={}
    for v in range(1,N+1):
        for c in domains[v]: var[v,c]=len(var)+1
    clauses=[]
    for v in range(1,N+1):
        choices=[var[v,c] for c in domains[v]]
        clauses.append(choices)
        clauses.extend([-a,-b] for a,b in combinations(choices,2))
    triple_count=0
    constrained=0
    schur_clauses=0
    for x in range(1,N+1):
        for y in range(x,N+1-x):
            z=x+y
            triple_count+=1
            vertices=sorted({x,y,z})
            common=set.intersection(*(set(domains[v]) for v in vertices))
            if common: constrained+=1
            for c in sorted(common):
                clauses.append([-var[v,c] for v in vertices])
                schur_clauses+=1
    assert triple_count==72092
    return alignment,domains,var,clauses,constrained,schur_clauses


def write(case,target):
    alignment,domains,var,clauses,constrained,schur_clauses=make(case)
    with Path(target).open('w',encoding='ascii',newline='\n') as out:
        out.write(f'p cnf {len(var)} {len(clauses)}\n')
        for clause in clauses: out.write(' '.join(map(str,clause))+' 0\n')
    print(f'case={case} aligned_words={len(alignment)} variables={len(var)} '
          f'clauses={len(clauses)} constrained_triples={constrained} '
          f'schur_clauses={schur_clauses} '
          f'domain_histogram={[sum(len(d)==k for d in domains[1:]) for k in range(1,7)]}',
          flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--case',required=True)
    p.add_argument('--cnf',type=Path,required=True)
    a=p.parse_args()
    write(a.case,a.cnf)
