#!/usr/bin/env python3
"""One frozen 512-selection pilot; all native logs and traces stay external."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
from pysat.solvers import Solver
import engine as E


def proof(w,name,n,cs,args):
    raw=E.J.dimacs(n,cs);cnf=w/(name+'.cnf');trace=w/(name+'.drat');cnf.write_bytes(raw)
    t=time.monotonic()
    with (w/(name+'.log')).open('w') as log:
        r=subprocess.run([str(args.kissat),'--seed=0','--conflicts=1000000','--time=180',str(cnf),str(trace)],stdout=log,stderr=subprocess.STDOUT)
    out={'name':name,'returncode':r.returncode,'seconds':time.monotonic()-t,'cnf_sha256':sha256(raw).hexdigest(),'verified':False}
    if r.returncode==20:
        t=time.monotonic()
        with (w/(name+'.check.log')).open('w') as log:
            chk=subprocess.run([str(args.drat),str(cnf),str(trace)],stdout=log,stderr=subprocess.STDOUT)
        out.update(check_returncode=chk.returncode,check_seconds=time.monotonic()-t,
                   verified=chk.returncode==0 and 's VERIFIED' in (w/(name+'.check.log')).read_text())
    if trace.exists():out.update(proof_bytes=trace.stat().st_size,proof_sha256=sha256(trace.read_bytes()).hexdigest())
    return out


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--kissat',type=Path,required=True);ap.add_argument('--drat',type=Path,required=True)
    args=ap.parse_args();w=args.work;w.mkdir(exist_ok=False);resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,)*2)
    start=time.monotonic();data=E.inputs();S=data['small'];ss=set(S);rows=E.initial(data);seed_count=len(rows)
    solvers=[]
    for k in range(20):
        n,cs=E.activated_case(data,k);(w/f'activation_{k:02d}.cnf').write_bytes(E.J.dimacs(n,cs));solvers.append(Solver(name='cadical195',bootstrap_with=cs))
    native=[];history=[];status='BOUND_REACHED';proofs=[];candidate=None;frontier=None
    for turn in range(513):
        n,cs=E.master(rows,S);ms=Solver(name='cadical195',bootstrap_with=cs);ms.conf_budget(100000);t=time.monotonic();ans=ms.solve_limited()
        rec={'turn':turn,'master_result':ans,'master_seconds':time.monotonic()-t,'cuts':len(rows),'forced':sum(len(r['D'])==1 for r in rows),'cases':[]}
        if ans is not True:
            ms.delete();history.append(rec)
            status='MASTER_UNKNOWN' if ans is None else 'MASTER_UNSAT_UNVERIFIED'
            if ans is False:
                proofs.append(proof(w,'master_final',n,cs,args))
                if proofs[-1]['verified']:status='FIXED_L_FAMILY_CLOSED'
            break
        positive={x for x in ms.get_model() if x>0};ms.delete();selected=[v for i,v in enumerate(S) if i+1 not in positive]
        assert len(selected)<=133
        for v in S:
            if len(selected)==133:break
            if v not in selected:selected.append(v)
        selected.sort();active=set(selected);assert all(active&set(r['D']) for r in rows)
        frontier=selected
        if turn==512:history.append(rec);break
        candidate=selected;frontier=None;winner=None
        for k,solver in enumerate(solvers):
            assumptions=[(4*len(S)+i+1)*(1 if v in active else -1) for i,v in enumerate(S)]
            solver.conf_budget(100000);t=time.monotonic();ans=solver.solve_limited(assumptions=assumptions)
            rec['cases'].append({'case':k,'answer':ans,'seconds':time.monotonic()-t})
            if ans is None:status='CASE_UNKNOWN';break
            if ans is False:continue
            pos={x for x in solver.get_model() if x>0}
            c=''.join(str(next(c for c in range(4) if 4*i+c+1 in pos)) if v in active else '.' for i,v in enumerate(S))
            winner=E.extend(c,k,data);native.append(winner);rows=E.minimal(rows+[winner]);rec['new_D']=winner['D'];break
        history.append(rec)
        (w/'progress.json').write_text(json.dumps({'history':history,'rows':rows,'last_tested':candidate},separators=(',',':'))+'\n')
        print(json.dumps({'candidate':turn+1,'case_calls':len(rec['cases']),'cuts':len(rows),'forced':sum(len(r['D'])==1 for r in rows),'D':rec.get('new_D'),'status':status}),flush=True)
        if status=='CASE_UNKNOWN':break
        if winner is None:
            status='TARGET_UNVERIFIED'
            for k in range(20):
                n,cs=E.J.small_case(selected,data['small_edges'],data['cross_edges'],data['boundary'],data['profiles'][k]['pattern'])
                proofs.append(proof(w,f'target_{k:02d}',n,cs,args))
                if not proofs[-1]['verified']:break
            if len(proofs)==20 and all(p['verified'] for p in proofs):
                V=sorted(data['large']+selected);n,cs=E.P.graph_cnf(V,data['edges'],5)
                with Solver(name='cadical195',bootstrap_with=cs) as solver:
                    assert solver.solve();positive={x for x in solver.get_model() if x>0}
                c=''.join(str(next(c for c in range(5) if 5*i+c+1 in positive)) for i,v in enumerate(V));mp=dict(zip(V,c));assert all(mp[u]!=mp[v] for u,v in data['edges'] if u in mp and v in mp)
                (w/'target_five_colouring.json').write_text(json.dumps({'vertices':V,'colouring':c})+'\n');status='TARGET_FIVE_CHROMATIC_VERIFIED'
            break
    for solver in solvers:solver.delete()
    n,cs=E.master(rows,S);(w/'master_residual.cnf').write_bytes(E.J.dimacs(n,cs))
    (w/'certificate.json').write_text(json.dumps({'rows':rows},separators=(',',':'))+'\n')
    (w/'native_witnesses.json').write_text(json.dumps(native,separators=(',',':'))+'\n')
    result={'status':status,'initial_cuts':seed_count,'final_cuts':len(rows),'forced_small_vertices':sum(len(r['D'])==1 for r in rows),'candidates':len([r for r in history if r['cases']]),'master_calls':len(history),'case_calls':sum(len(r['cases']) for r in history),'positive_extensions':len(native),'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'proofs':proofs,'master_variables':n,'master_clauses':len(cs),'master_sha256':sha256(E.J.dimacs(n,cs)).hexdigest(),'last_tested_small_selection':candidate,'untested_frontier':frontier,'history':history}
    (w/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['history','last_tested_small_selection','untested_frontier']},indent=2),flush=True)


if __name__=='__main__':main()
