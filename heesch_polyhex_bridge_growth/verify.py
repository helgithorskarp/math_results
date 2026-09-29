"""Check the family, every finite certificate, and every periodic witness."""
from pathlib import Path
import argparse,collections,hashlib,json,subprocess,time
from geometry import contacts,halo,normalize,orientations
from exact_cover import first_decision
from family import family
from local_support import Cover
from restricted_corona import encode
from pysat.solvers import Solver

HERE=Path(__file__).resolve().parent

def check_periodic(cells,certificate):
    w,s,h=certificate['lattice'];os=orientations(cells);points=[]
    assert all(type(v) is int for v in [w,s,h]) and w>0 and h>0
    for i,x,y in certificate['poses']:
        assert all(type(v) is int for v in [i,x,y])
        assert 0<=i<len(os)
        points.extend((a+x,b+y) for a,b in os[i])
    assert len(points)==w*h
    for i,(x,y) in enumerate(points):
        for a,b in points[:i]:
            dy=y-b
            assert dy%h or (x-a-s*(dy//h))%w,'Repeated lattice coset'

def certified_unsat(cnf,nv,work,checker):
    with Solver(name='g4',bootstrap_with=cnf,with_proof=True) as solver:
        assert not solver.solve(),'Certificate formula is satisfiable'
        proof=solver.get_proof()
    cp=work/'instance.cnf';pp=work/'proof.drat'
    with cp.open('w') as f:
        f.write(f'p cnf {nv} {len(cnf)}\n')
        for clause in cnf:f.write(' '.join(map(str,clause))+' 0\n')
    pp.write_text('\n'.join(proof)+'\n')
    checked=subprocess.run([str(checker),str(cp),str(pp),'-t','60'],
                           capture_output=True,text=True,timeout=65)
    assert checked.returncode==0 and 's VERIFIED' in checked.stdout,checked.stdout[-1000:]
    return dict(cnf_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),
                proof_sha256=hashlib.sha256(pp.read_bytes()).hexdigest(),
                variables=nv,clauses=len(cnf),proof_bytes=pp.stat().st_size)

def evidence(record):
    # Formula identity is stable; exact proof bytes need not be.
    out=[record['index'],record['status']]
    for tag in ['zero','exclusion','two']:
        if tag in record:
            r=record[tag]
            out.append([tag,'trivial'] if r.get('trivial') else
                       [tag,r['cnf_sha256'],r['variables'],r['clauses']])
    if 'support_size' in record:out.append(['support',record['support_size'],record['support_sha256']])
    return out

def run(args):
    fs=family();metadata=json.loads((HERE/'summary.json').read_text())
    digest=hashlib.sha256(json.dumps(fs,separators=(',',':')).encode()).hexdigest()
    assert len(fs)==metadata['family_size']==1557 and digest==metadata['family_sha256']
    periodic=json.loads((HERE/'periodic_witnesses.json').read_text())
    checker=Path(args.checker).resolve();work=Path(args.work_dir).resolve()
    assert work!=HERE and HERE not in work.parents,'Keep generated proofs outside source'
    work.mkdir(parents=True,exist_ok=True)
    stop=len(fs) if args.stop is None else args.stop
    assert 0<=args.start<stop<=len(fs)
    start=time.perf_counter();counts=collections.Counter();records=[];proofs=0
    with (work/'evidence.jsonl').open('w') as f:
        for i in range(args.start,stop):
            cells=fs[i];record=dict(index=i)
            if str(i) in periodic:
                check_periodic(cells,periodic[str(i)]);record['status']='infinite'
            else:
                decision=first_decision(cells)
                cnf,ps,z,fp,ds,nv=encode(cells,1)
                if decision['status']=='H0':
                    record.update(status='Hh0',zero=certified_unsat(cnf,nv,work,checker));proofs+=1
                else:
                    occupied=set(cells)
                    for t in decision['witness']:
                        assert normalize(t) in orientations(cells) and occupied.isdisjoint(t)
                        assert set(t)&halo(cells);occupied.update(t)
                    assert halo(cells)<=occupied
                    support=Cover(halo(cells),contacts(cells)).support()
                    bad=[z[p,1] for p in ps if ds[p]==1 and tuple(fp(p)) not in support]
                    exclusion=certified_unsat(cnf+[bad],nv,work,checker) if bad else dict(trivial=True)
                    proofs+=bool(bad)
                    cnf2,_,_,_,_,nv2=encode(cells,2,local_override=support)
                    record.update(status='Hh1',support_size=len(support),
                        support_sha256=hashlib.sha256(json.dumps(sorted(support),separators=(',',':')).encode()).hexdigest(),
                        exclusion=exclusion,two=certified_unsat(cnf2,nv2,work,checker));proofs+=1
            counts[record['status']]+=1;records.append(record)
            f.write(json.dumps(record,separators=(',',':'))+'\n');f.flush()
            if (i-args.start+1)%100==0:print('Checked',i+1,'seconds',round(time.perf_counter()-start,3),flush=True)
    evidence_sha=hashlib.sha256(json.dumps([evidence(r) for r in records],separators=(',',':')).encode()).hexdigest()
    full=args.start==0 and stop==len(fs)
    if full:
        assert dict(counts)==metadata['classifications']
        assert proofs==metadata['proofs_checked']
        assert evidence_sha==metadata['evidence_sha256']
    print(json.dumps(dict(verified_interval=[args.start,stop],full_family_verified=full,
          counts=counts,proofs_checked=proofs,evidence_sha256=evidence_sha,
          seconds=round(time.perf_counter()-start,3)),sort_keys=True))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--checker',required=True)
    p.add_argument('--work-dir',required=True);p.add_argument('--start',type=int,default=0)
    p.add_argument('--stop',type=int);run(p.parse_args())
