#!/usr/bin/env python3
"""Four fixed certificate-repair queries for A7 plus point 610."""
from pathlib import Path
from hashlib import sha256
import argparse
import importlib.util
import itertools
import json
import resource
import time
from pysat.solvers import Solver
import pysat

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def save(work, name, data):
    path=work/name; tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n');tmp.replace(path)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
    args=ap.parse_args();work=args.work.resolve();work.mkdir(parents=True,exist_ok=True)
    start=time.monotonic()
    assert not (work/'repairs.json').exists()
    assert pysat.__version__=='1.8.dev24'
    resource.setrlimit(resource.RLIMIT_AS,(4<<30,4<<30))
    spec=importlib.util.spec_from_file_location('geometry',REPO/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py')
    geo=importlib.util.module_from_spec(spec);spec.loader.exec_module(geo)
    den,points,_,_,_=geo.read_geometry()
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    vertices=old['vertices']+[610]
    target=(den*den,)+(0,)*7
    edges=[(a,b) for a,b in itertools.combinations(vertices,2) if geo.squared_distance(points[a],points[b])==target]
    assert len(vertices)==586 and len(edges)==3089
    tasks=[('forced','44',[44]),('forced','56',[56]),('kill','94',old['family'][94]['D']),('kill','188',old['family'][188]['D'])]
    result=dict(status='running',vertices=vertices,edges=len(edges),queries=[],native_seconds=0.0,
                native_negative_answers_independently_certified=False)
    for kind,key,D in tasks:
        keep=[v for v in vertices if v not in D];pos={v:i for i,v in enumerate(keep)}
        ee=[(a,b) for a,b in edges if a in pos and b in pos]
        rows=[[4*i+c+1 for c in range(4)] for i in range(len(keep))]
        rows += [[-(4*pos[a]+c+1),-(4*pos[b]+c+1)] for a,b in ee for c in range(4)]
        triangle=[0,149,152]
        assert all(tuple(sorted(e)) in ee for e in itertools.combinations(triangle,2))
        rows += [[4*pos[v]+c+1] for c,v in enumerate(triangle)]
        cnf=(f'p cnf {4*len(keep)} {len(rows)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in rows)).encode()
        (work/f'{kind}_{key}.cnf').write_bytes(cnf)
        with Solver(name='cadical195',bootstrap_with=rows,use_timer=True) as solver:
            solver.conf_budget(100000)
            answer=solver.solve_limited()
            native=solver.time()
            row=dict(kind=kind,key=key,D=D,status={True:'SAT',False:'UNSAT',None:'UNKNOWN'}[answer],
                     native_seconds=native,variables=4*len(keep),clauses=len(rows),cnf_sha256=sha256(cnf).hexdigest())
            if answer is True:
                positive={v for v in solver.get_model() if v>0}
                colours={v:next(c for c in range(4) if 4*pos[v]+c+1 in positive) for v in keep}
                assert all(colours[a]!=colours[b] for a,b in ee)
                row['witness']=''.join(str(colours[v]) for v in keep)
            result['queries'].append(row);result['native_seconds']+=native
            result['wall_seconds']=time.monotonic()-start
            result['maximum_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            save(work,'repairs.json',result)
            print(json.dumps({k:v for k,v in row.items() if k!='witness'}),flush=True)
    result['status']='completed';save(work,'repairs.json',result)


if __name__=='__main__': main()
