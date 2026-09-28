"""Exact Schur CNF for per-position recombination of five 537-words."""
import argparse
import json
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 537
NAMES = ('W', '190', '359', 'best3', '347')


def load(overrides=None):
    sources = json.loads((HERE / 'sources.json').read_text(encoding='ascii'))
    assert tuple(sources) == NAMES
    overrides = overrides or {}
    assert set(overrides) <= set(NAMES)
    aligned = []
    for name in NAMES:
        row = sources[name]
        word = row['word']
        perm = overrides.get(name, row['permutation'])
        assert len(word) == N and set(word) == set('123456')
        assert len(perm) == 6 and set(perm) == set('123456')
        aligned.append(''.join(perm[int(d)-1] for d in word))
    return sources, aligned


def make(overrides=None):
    sources, aligned = load(overrides)
    domains = [()] + [tuple(sorted({int(word[v-1]) for word in aligned}))
                      for v in range(1, N+1)]
    var = {}
    for v in range(1, N+1):
        for c in domains[v]:
            var[v,c] = len(var)+1
    clauses = []
    for v in range(1, N+1):
        choices = [var[v,c] for c in domains[v]]
        clauses.append(choices)
        clauses.extend([-a,-b] for a,b in combinations(choices,2))
    triples = 0
    constrained = 0
    schur_clauses = 0
    for x in range(1,N+1):
        for y in range(x,N+1-x):
            z=x+y
            triples+=1
            vertices=sorted({x,y,z})
            common=set.intersection(*(set(domains[v]) for v in vertices))
            if common: constrained+=1
            for c in sorted(common):
                clauses.append([-var[v,c] for v in vertices])
                schur_clauses+=1
    assert triples==72092
    return sources, aligned, domains, var, clauses, constrained, schur_clauses


def write(path, overrides=None):
    _, _, domains, var, clauses, constrained, schur_clauses = make(overrides)
    with Path(path).open('w',encoding='ascii',newline='\n') as out:
        out.write(f'p cnf {len(var)} {len(clauses)}\n')
        for clause in clauses:
            out.write(' '.join(map(str,clause))+' 0\n')
    print(f'variables={len(var)} clauses={len(clauses)} '
          f'constrained_triples={constrained} schur_clauses={schur_clauses} '
          f'domain_histogram={[sum(len(d)==k for d in domains[1:]) for k in range(1,7)]}',
          flush=True)


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--cnf',type=Path,required=True)
    p.add_argument('--set',action='append',default=[],metavar='NAME=PERM',
                   help='override one source permutation for exploratory search')
    a=p.parse_args()
    overrides=dict(item.split('=',1) for item in a.set)
    assert len(overrides)==len(a.set)
    write(a.cnf,overrides)
