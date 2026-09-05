#!/usr/bin/env python3
"""Exhaust all small omission assignments against the threshold encoding."""
from itertools import product
import json
from pysat.solvers import Solver
import engine as E


def main():
    assignments=0;instances=0
    for n in range(7):
        for bound in range(n+1):
            _,clauses=E.atleast(n,bound);solver=Solver(name='cadical195',bootstrap_with=clauses);instances+=1
            for bits in product((False,True),repeat=n):
                answer=solver.solve(assumptions=[(i+1)*(1 if b else -1) for i,b in enumerate(bits)])
                E.require(answer==(sum(bits)>=bound),'threshold equivalence control');assignments+=1
            solver.delete()
    # Five single-deletion colourings of K5 force all five vertices.
    _,clauses=E.atleast(5,1);clauses += [[-v] for v in range(1,6)]
    solver=Solver(name='cadical195',bootstrap_with=clauses);E.require(not solver.solve(),'forced K5 size bound');solver.delete()
    print(json.dumps({'status':'CONTROLS PASSED','threshold_instances':instances,'omission_assignments':assignments,'forced_K5_control':True},indent=2))


if __name__=='__main__':main()
