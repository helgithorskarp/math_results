#!/usr/bin/env python3
"""Reconstruct positive colouring certificates and prove the Parts a=6 cover.

The only finite-instance inputs are positive killing clauses and small
interface-colouring hints. Complete colourings and DRAT traces are generated
in the requested work directory, and checked before success is reported.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from pysat.solvers import Solver

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
sys.path.insert(0,str(REPO/'hadwiger_nelson_parts509_pool_shape_closure'))
import cardenc
import exactgeom


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()


def dimacs(nv,clauses):
    return (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()


def load_family():
    with (HERE/'killing_clauses.cnf').open() as f:
        head=f.readline().split();assert head[:3]==['p','cnf','303']
        rows=[]
        for line in f:
            c=list(map(int,line.split()));assert c[-1]==0
            c=c[:-1];assert c and c==sorted(set(c)) and all(1<=x<=303 for x in c)
            rows.append(c)
    assert len(rows)==int(head[3])==6777 and len({tuple(c) for c in rows})==len(rows)
    hints=json.loads((HERE/'interface_hints.json').read_text());assert len(hints)==len(rows)
    return rows,hints


def master(U,L,edges,killing):
    S=[v for v in U if v<509];Q=[v for v in U if v>=509]
    ls,us=set(L),set(U);x={v:i+1 for i,v in enumerate(U)};nv=len(U)
    clauses=[list(c) for c in killing]
    rows,nv=cardenc.equals_tot([-x[v] for v in S],7,nv);clauses.extend(rows)
    rows,nv=cardenc.equals_tot([x[v] for v in Q],6,nv);clauses.extend(rows)
    adj={v:set() for v in L+U}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    for w in Q:
        need=4-len(adj[w]&ls);neighbors=sorted(adj[w]&us)
        if need<=0:continue
        if need>len(neighbors):clauses.append([-x[w]]);continue
        rows,nv=cardenc.atmost_tot([-x[v] for v in neighbors],len(neighbors)-need,nv)
        clauses.extend([[-x[w]]+c for c in rows])
    return nv,clauses


def reconstruct(out,U,L,edges,wl,killing,hints,conflicts):
    n=len(U);us,ls=set(U),set(L);pos={v:i for i,v in enumerate(U)}
    inner=[(pos[a],pos[b]) for a,b in edges if a in us and b in us]
    cross=[(a,pos[b]) if a in ls else (b,pos[a]) for a,b in edges if (a in ls)!=(b in ls)]
    for w in wl:
        assert len(w)==len(L) and set(w)<=set('0123')
        assert all(w[a]!=w[b] for a,b in edges if a in ls and b in ls)
    def check(row):
        i,p,c=row['i'],row['p'],row['c']
        assert type(i) is int and 0<=i<len(killing) and p==hints[i]
        assert type(p) is int and 0<=p<len(wl)
        assert len(c)==n and set(c)<=set('.0123')
        assert [j+1 for j,a in enumerate(c) if a=='.']==killing[i]
        assert all(c[a]=='.' or c[b]=='.' or c[a]!=c[b] for a,b in inner)
        assert all(c[u]=='.' or c[u]!=wl[p][l] for l,u in cross)
    cached={};path=out/'colourings.jsonl'
    if path.exists():
        for line in path.open():
            row=json.loads(line);check(row);assert row['i'] not in cached;cached[row['i']]=row
    def act(i):return 2*n+i+1
    def unequal(i,c):return [-(2*i+b+1) if c>>b&1 else 2*i+b+1 for b in range(2)]
    z=[3*n+p+1 for p in range(len(wl))];formula=[z]
    for a,b in inner:
        for c in range(4):formula.append([-act(a),-act(b)]+unequal(a,c)+unequal(b,c))
    for p,w in enumerate(wl):
        for l,u in cross:formula.append([-z[p],-act(u)]+unequal(u,int(w[l])))
    start=time.monotonic();generated=0
    with Solver(name='cadical195',bootstrap_with=formula) as solver,path.open('a',buffering=1) as sink:
        for i,(D,p) in enumerate(zip(killing,hints)):
            if i in cached:continue
            assert type(p) is int and 0<=p<len(wl)
            deleted=set(D)
            assumptions=[-act(j) if j+1 in deleted else act(j) for j in range(n)]
            assumptions.extend(t if j==p else -t for j,t in enumerate(z))
            solver.conf_budget(conflicts)
            verdict=solver.solve_limited(assumptions=assumptions)
            if verdict is not True:
                sink.flush();os.fsync(sink.fileno())
                raise RuntimeError(f'Colouring {i} unresolved or incompatible: {verdict}; increase --conflicts to retry an unresolved case')
            model=set(solver.get_model())
            c=''.join('.' if j+1 in deleted else str(sum(1<<b for b in range(2) if 2*j+b+1 in model)) for j in range(n))
            row=dict(i=i,p=p,c=c);check(row);cached[i]=row
            sink.write(json.dumps(row,separators=(',',':'),sort_keys=True)+'\n');generated+=1
            if (i+1)%250==0:
                sink.flush();os.fsync(sink.fileno());print('Verified colourings',i+1,'of',len(killing),'seconds',round(time.monotonic()-start,1),flush=True)
        sink.flush();os.fsync(sink.fileno())
    assert set(cached)==set(range(len(killing)))
    return dict(verified=len(cached),generated_this_run=generated,seconds=time.monotonic()-start,cache_sha256=digest(path))


def main():
    if not __debug__:raise RuntimeError('Run without Python optimization flags')
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--kissat',default='kissat');ap.add_argument('--drat-trim',default='drat-trim')
    ap.add_argument('--conflicts',type=int,default=200000);ap.add_argument('--solver-seconds',type=int,default=900)
    args=ap.parse_args();assert args.conflicts>0 and args.solver_seconds>0
    out=args.work;out.mkdir(parents=True,exist_ok=True);started=time.monotonic()
    killing,hints=load_family()
    print('Reconstructing all exact points and unit edges',flush=True)
    pts,_=exactgeom.build(REPO);den,ipts=exactgeom.scale_points(pts)
    U=sorted(json.loads((REPO/'hadwiger_nelson_parts509_s_replacement_budget/pool_S.json').read_text())['W_S']);L=list(range(374))
    assert len(U)==303 and U[:135]==list(range(374,509)) and all(v>=509 for v in U[135:])
    assert len({(tuple(pts[v][0]),tuple(pts[v][1])) for v in L+U})==677
    edges=exactgeom.unit_pairs(ipts,den,L+U);assert len(edges)==3400
    wl=[r['witness_colouring_L'] for r in json.loads((REPO/'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())['classes']]
    positive=reconstruct(out,U,L,edges,wl,killing,hints,args.conflicts)
    nv,clauses=master(U,L,edges,killing);cnf=out/'master.cnf';cnf.write_bytes(dimacs(nv,clauses))
    expected_path=HERE/'expected.json'
    facts=dict(points=677,unit_edges=3400,killing_clauses=len(killing),variables=nv,clauses=len(clauses),
               cnf_sha256=digest(cnf),killing_instance_sha256=digest(HERE/'killing_clauses.cnf'),
               interface_hints_sha256=digest(HERE/'interface_hints.json'))
    if expected_path.exists():assert facts==json.loads(expected_path.read_text())
    (out/'facts.json').write_text(json.dumps(facts,indent=2,sort_keys=True)+'\n')
    print('All positive certificates checked; generating UNSAT proof',json.dumps(facts,sort_keys=True),flush=True)
    proof=out/'master.drat';t=time.monotonic()
    with (out/'solver.log').open('w') as f:
        p=subprocess.run([args.kissat,'--seed=20609','-f',str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT,timeout=args.solver_seconds)
    assert p.returncode==20,p.returncode
    solve_seconds=time.monotonic()-t;print('UNSAT; checking DRAT',flush=True);t=time.monotonic()
    with (out/'verify.log').open('w') as f:
        p=subprocess.run([args.drat_trim,str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT)
    assert p.returncode==0 and 's VERIFIED' in (out/'verify.log').read_text()
    result=dict(facts,status='a=6 COLOURING COVER AND DRAT VERIFIED',positive_certificates=positive,
                proof_sha256=digest(proof),proof_bytes=proof.stat().st_size,solver_seconds=solve_seconds,
                checker_seconds=time.monotonic()-t,total_seconds=time.monotonic()-started)
    (out/'result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True),flush=True)


if __name__=='__main__':main()
