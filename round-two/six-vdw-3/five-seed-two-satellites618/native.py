#!/usr/bin/env python3
"""Untrusted native candidate interface, adapted from source b18c33b5.

The parent's single-satellite618/reproduce.py has SHA256
096dcdfaa75c5e1779cad8862d7b19f9d41557e728ab68f0232317b082535b74.
This copy lowers the request from100000 to99900, so any small native budget
overshoot remains inside the same100000 hard observed-conflict ceiling.
Native answers alone are never mathematical certificates.
"""
import argparse
import ctypes
import json
import time
from pathlib import Path


def need(condition,message):
    if not condition:
        raise ValueError(message)


def native(cnf):
    import pysat
    from pysat.solvers import Solver
    need(pysat.__version__ == '1.8.dev24', 'Use python-sat1.8.dev24')
    rows = [list(map(int,line.split()[:-1])) for line in cnf.read_text().splitlines()[1:]]
    started = time.monotonic()
    with Solver(name='cadical195',bootstrap_with=rows,with_proof=True) as solver:
        solver.conf_budget(99900)
        answer = solver.solve_limited()
        stats = solver.accum_stats()
        if answer is False:
            need(ctypes.CDLL(None).fflush(None) == 0, 'Native ASCII trace flush failed')
            cnf.with_suffix('.drat').write_text('\n'.join(solver.get_proof())+'\n')
        if answer is True:
            cnf.with_suffix('.assignment.json').write_text(json.dumps(solver.get_model())+'\n')
    status = {None:'UNKNOWN',False:'UNSAT_PENDING_CHECK',True:'SAT_PENDING_CHECK'}[answer]
    if stats['conflicts'] > 100000:
        status = 'RESOURCE_CONFLICT_CAP_EXCEEDED'
    return {'status':status,'conflict_budget_requested':99900,'observed_conflict_ceiling':100000,
            'stats':stats,'seconds':time.monotonic()-started,'mathematical_exclusion':False}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--solve',type=Path,required=True)
    a = p.parse_args()
    print(json.dumps(native(a.solve)))
