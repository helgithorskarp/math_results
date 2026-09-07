#!/usr/bin/env python3
"""Secondary, frozen 100000-conflict/query 4-colouring pilot (python-sat)."""
import argparse
import json
import ctypes
import time
from pathlib import Path
from pysat.solvers import Cadical195, Solver
from produce import graph, prime_powers


def clauses(n,edges,k=4):
    out = [[k*v+c+1 for c in range(k)] for v in range(n)]
    out += [[-k*v-c-1,-k*v-d-1] for v in range(n)
            for c in range(k) for d in range(c+1,k)]
    out += [[-k*u-c-1,-k*v-c-1] for u,v in edges for c in range(k)]
    # Colour names can always be permuted to pin the first edge.
    u,v = edges[0]
    out += [[k*u+1],[k*v+2]]
    return out


def finished_proof(solver):
    # CaDiCaL's C stream is buffered. get_proof() before destruction can omit
    # the final block, including the empty clause. Explicitly flush the C
    # streams on the documented POSIX platform. Destruction alone did not
    # flush this PySAT build. Do not strip meaningful binary bytes.
    if ctypes.CDLL(None).fflush(None) != 0:
        raise OSError('C proof stream flush failed')
    solver.prfile.seek(0)
    return Solver._proof_bin2text(bytearray(solver.prfile.read()))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--q11-only',action='store_true')
    args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    rows=[]
    for q,p,f in prime_powers():
        if args.q11_only and q!=11:continue
        F,S,E=graph(q,p,f);cnf=clauses(q*q,E)
        start=time.monotonic()
        with Cadical195(bootstrap_with=cnf,with_proof=True) as solver:
            solver.conf_budget(100000)
            result=solver.solve_limited()
            row={'q':q,'vertices':q*q,'edges':len(E),
                 'result':{True:'SAT',False:'UNSAT',None:'UNKNOWN'}[result],
                 'statistics':solver.accum_stats(),'elapsed_seconds':time.monotonic()-start}
            if result is True:
                model=set(solver.get_model())
                row['colouring']=[next(c for c in range(4) if 4*v+c+1 in model) for v in range(q*q)]
                if any(row['colouring'][u]==row['colouring'][v] for u,v in E):
                    raise ValueError('invalid solver model')
            elif result is False:
                proof=finished_proof(solver)
                (args.output/f'q{q}.drat').write_text('\n'.join(proof)+'\n')
                (args.output/f'q{q}.cnf').write_text(f'p cnf {4*q*q} {len(cnf)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in cnf))
                row['proof_lines']=len(proof)
        rows.append(row);print(json.dumps({k:v for k,v in row.items() if k!='colouring'}),flush=True)
        (args.output/'pilot.json').write_text(json.dumps({'conflict_cap':100000,'cases':rows},indent=2)+'\n')
    F,S,E=graph(11,11,1)
    with Cadical195(bootstrap_with=clauses(121,E,5)) as solver:
        solver.conf_budget(100000)
        result=solver.solve_limited()
        if result is not True:raise ValueError('five-colouring witness not found within cap')
        model=set(solver.get_model())
        word=[next(c for c in range(5) if 5*v+c+1 in model) for v in range(121)]
        if any(word[u]==word[v] for u,v in E):raise ValueError('bad five-colouring')
        (args.output/'q11_five_colouring.json').write_text(json.dumps(word)+'\n')


if __name__=='__main__':
    main()
