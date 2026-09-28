#!/usr/bin/env python3
"""Optional exact SAT model for the revised interval construction.

Every complement point has its own colour variable; all Schur triples,
including doubling, are included. UNKNOWN never means UNSAT. No UNSAT
certificate is emitted by this exploratory runner.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path


def encoding(n, a, k):
    if a < 2 or n < 5*a-4 or not 1 <= k <= 8:
        raise ValueError('require a>=2, n>=5a-4, and 1<=k<=8')
    reserved = set(range(a,2*a-1)) | set(range(n+1-a,n+1))
    positions = sorted(set(range(1,n+1))-reserved)
    index = {v:i for i,v in enumerate(positions)}
    clauses = []
    for i in range(len(positions)):
        block = [i*k+c for c in range(1,k+1)]
        clauses.append(block)
        clauses.extend([-x,-y] for x,y in combinations(block,2))
        # Order the interchangeable colours by their first appearance.
        for c in range(2,k+1):
            clauses.append([-i*k-c]+[j*k+c-1 for j in range(i)])
    edges = set()
    for x,y in combinations(positions,2):
        if x+y in index:
            edges.add(tuple(sorted((index[x],index[y],index[x+y]))))
    for x in positions:
        if 2*x in index:
            edges.add((index[x],index[2*x]))
    for edge in sorted(edges):
        for c in range(1,k+1):
            clauses.append([-i*k-c for i in edge])
    return reserved, positions, clauses


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--n',type=int,default=537)
    p.add_argument('--a',type=int,default=78)
    p.add_argument('--k',type=int,default=5)
    p.add_argument('--budget',type=int,default=100000)
    p.add_argument('--word',default='/tmp/schur-interval-word.txt')
    args = p.parse_args()
    if args.budget < 1:
        raise ValueError('conflict budget must be positive')
    from pysat.solvers import Solver
    from verify import literal_schur
    reserved,positions,clauses = encoding(args.n,args.a,args.k)
    with Solver(name='cadical195',bootstrap_with=clauses) as solver:
        solver.conf_budget(args.budget)
        answer = solver.solve_limited()
        result = dict(status={True:'SAT',False:'UNSAT',None:'UNKNOWN'}[answer],
                      n=args.n,a=args.a,k=args.k,budget=args.budget,
                      variables=len(positions)*args.k,clauses=len(clauses),
                      stats=solver.accum_stats(),unsat_certificate=False)
        if answer:
            model = set(solver.get_model())
            values = {v:next(c for c in range(1,args.k+1) if i*args.k+c in model)
                      for i,v in enumerate(positions)}
            word = [args.k+1 if v in reserved else values[v]
                    for v in range(1,args.n+1)]
            if len(word)!=args.n or not literal_schur(word):
                raise RuntimeError('complete word failed the direct Schur checker')
            Path(args.word).write_text(''.join(map(str,word))+'\n')
            result['verified_word_file'] = args.word
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
