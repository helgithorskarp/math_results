"""Reproduce the family and check every finite upper bound and plane tiling."""
import argparse,csv,hashlib,json,subprocess,sys
from collections import Counter
from pathlib import Path
from time import perf_counter
from pysat.solvers import Solver
from family import family
from geometry import orientations,halo
from exact_cover import first_decision
from corona import encode

HERE=Path(__file__).resolve().parent

def check_periodic(cells,certificate):
    # Difference-vector membership in L; independent of search residue masks.
    w,s,h=certificate['lattice']
    assert all(isinstance(i,int) for i in [w,s,h]) and w>0 and h>0
    os=orientations(cells);points=[]
    for i,x,y in certificate['poses']:
        assert 0<=i<len(os)
        points.extend((a+x,b+y) for a,b in os[i])
    assert len(points)==w*h
    for i,(x,y) in enumerate(points):
        for a,b in points[:i]:
            dy=y-b
            assert dy%h or (x-a-s*(dy//h))%w, 'Repeated lattice coset'
    # Exactly [Z^2:L] distinct classes implies exact plane coverage by L shifts.

def check_surround(cells,tiles):
    occupied=set(cells)
    for tile in tiles:
        assert occupied.isdisjoint(tile)
        assert set(tile)&halo(cells)
        occupied.update(tile)
    assert halo(cells)<=occupied

def run(args):
    shapes=family()
    digest=hashlib.sha256(json.dumps(shapes,separators=(',',':')).encode()).hexdigest()
    metadata=json.loads((HERE/'summary.json').read_text())
    assert len(shapes)==metadata['family_size']==324
    assert digest==metadata['family_sha256']
    rows=list(csv.DictReader((HERE/'bounds.csv').open()))
    assert [int(r['index']) for r in rows]==list(range(len(shapes)))
    certificates=json.loads((HERE/'periodic_witnesses.json').read_text())
    counts=Counter();start=perf_counter()
    if not args.quick:
        assert args.checker and args.work_dir, 'Specify --checker and --work-dir'
        checker=Path(args.checker).resolve();work=Path(args.work_dir).resolve()
        work.mkdir(parents=True,exist_ok=True)
        assert HERE not in work.parents and work!=HERE, 'Keep proof outputs outside source'
    for row,cells in zip(rows,shapes):
        idx=int(row['index']);status=row['status'];counts[status]+=1
        if status=='infinite':
            check_periodic(cells,certificates[str(idx)])
            continue
        result=first_decision(cells)
        if status=='Hh0':assert result['status']=='H0'
        elif status=='Hh1':
            assert result['status']=='surrounded'
            check_surround(cells,result['witness'])
        else:raise ValueError('Unknown classification')
        if args.quick:continue
        k=int(row['unsat_level']);cnf,ps,z,fp,ds,nv=encode(cells,k)
        instance=work/'instance.cnf';proof_path=work/'proof.drat'
        with instance.open('w') as f:
            f.write(f'p cnf {nv} {len(cnf)}\n')
            for clause in cnf:f.write(' '.join(map(str,clause))+' 0\n')
        assert hashlib.sha256(instance.read_bytes()).hexdigest()==row['cnf_sha256']
        with Solver(name='g4',bootstrap_with=cnf,with_proof=True) as solver:
            assert not solver.solve()
            proof=solver.get_proof()
        proof_path.write_text('\n'.join(proof)+'\n')
        checked=subprocess.run([str(checker),str(instance),str(proof_path),'-t','60'],
                               capture_output=True,text=True,timeout=65)
        assert checked.returncode==0 and 's VERIFIED' in checked.stdout,checked.stdout
        if idx%25==0:print(f'Checked through index {idx}',flush=True)
    assert dict(counts)==metadata['classifications']
    print(json.dumps(dict(counts=counts,seconds=round(perf_counter()-start,3),
                         upper_bounds_checked=not args.quick),sort_keys=True))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--quick',action='store_true')
    parser.add_argument('--checker');parser.add_argument('--work-dir')
    run(parser.parse_args())
