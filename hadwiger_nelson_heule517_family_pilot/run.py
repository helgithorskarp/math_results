#!/usr/bin/env python3
"""One bounded simultaneous family pilot; large native output stays external."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
from pysat.solvers import Solver
import engine as E


def proof(work,name,raw,kissat,drat):
    cnf=work/(name+'.cnf');trace=work/(name+'.drat');cnf.write_bytes(raw)
    command=[str(kissat),'--seed=0','--conflicts=1000000','--time=180',str(cnf),str(trace)]
    start=time.monotonic()
    with (work/(name+'.log')).open('w') as log:r=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
    out={'returncode':r.returncode,'seconds':time.monotonic()-start,'cnf_sha256':sha256(raw).hexdigest(),'proof_bytes':trace.stat().st_size if trace.exists() else 0,'verified':False}
    if r.returncode==20:
        start=time.monotonic()
        with (work/(name+'.check.log')).open('w') as log:check=subprocess.run([str(drat),str(cnf),str(trace)],stdout=log,stderr=subprocess.STDOUT)
        out.update(check_returncode=check.returncode,check_seconds=time.monotonic()-start,verified=check.returncode==0 and 's VERIFIED' in (work/(name+'.check.log')).read_text(),proof_sha256=sha256(trace.read_bytes()).hexdigest())
    return out


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--work',type=Path,required=True);ap.add_argument('--kissat',type=Path,required=True);ap.add_argument('--drat',type=Path,required=True)
    args=ap.parse_args();args.work.mkdir(parents=True,exist_ok=False);w=args.work
    resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,)*2)
    start=time.monotonic();data=E.geometry();seeds=E.inherited(data);rows=E.minimal(seeds)
    (w/'inherited.json').write_text(json.dumps(seeds,separators=(',',':'))+'\n')
    vars_,act=E.activated(data['edges']);(w/'activation.cnf').write_bytes(E.dimacs(vars_,act))
    graph=Solver(name='cadical195',bootstrap_with=act);history=[];native=[];final_proof=None;candidate=None;status='BOUND_REACHED'
    master_seconds=0.;graph_seconds=0.
    for turn in range(65):
        mv,mc=E.master(rows);ms=Solver(name='cadical195',bootstrap_with=mc);ms.conf_budget(100000);t=time.monotonic();answer=ms.solve_limited();elapsed=time.monotonic()-t;master_seconds+=elapsed
        record={'turn':turn,'cut_count':len(rows),'forced_count':sum(len(r['D'])==1 for r in rows),'master_result':answer,'master_seconds':elapsed}
        if answer is not True:
            ms.delete();history.append(record)
            if answer is False:
                final_proof=proof(w,'master_final',E.dimacs(mv,mc),args.kissat,args.drat)
                status='FAMILY_CLOSED' if final_proof['verified'] else 'MASTER_NEGATIVE_UNVERIFIED'
            else:status='MASTER_UNKNOWN'
            break
        positive={l for l in ms.get_model() if l>0};ms.delete();omitted={v for v in range(517) if v+1 in positive}
        E.require(len(omitted)>=9 and all(not set(r['D'])<=omitted for r in rows),'master model decoding')
        selected=sorted(set(range(517))-omitted)
        for v in sorted(omitted):
            if len(selected)==508:break
            selected.append(v)
        selected.sort();E.require(len(selected)==508 and all(set(r['D'])&set(selected) for r in rows),'monotone candidate enlargement')
        if turn==64:history.append(record);break
        candidate=selected;active=set(selected);assumptions=[(2069+v)*(1 if v in active else -1) for v in range(517)]
        graph.conf_budget(100000);t=time.monotonic();answer=graph.solve_limited(assumptions=assumptions);elapsed=time.monotonic()-t;graph_seconds+=elapsed
        record.update(graph_result=answer,graph_seconds=elapsed,selected_sha256=sha256(json.dumps(selected,separators=(',',':')).encode()).hexdigest())
        if answer is not True:
            history.append(record)
            if answer is False:
                gv,gc=E.graph_cnf(selected,data['edges']);final_proof=proof(w,'target_final',E.dimacs(gv,gc),args.kissat,args.drat)
                status='TARGET_NONFOUR_VERIFIED' if final_proof['verified'] else 'TARGET_NEGATIVE_UNVERIFIED'
                if final_proof['verified']:
                    gv,gc=E.graph_cnf(selected,data['edges'],5);five=Solver(name='cadical195',bootstrap_with=gc);E.require(five.solve(),'five-colour upper bound');pos={l for l in five.get_model() if l>0};colour=''.join(str(next(c for c in range(5) if 5*i+c+1 in pos)) for i,v in enumerate(selected));mapping=dict(zip(selected,colour));E.require(all(mapping[u]!=mapping[v] for u,v in data['edges'] if u in mapping and v in mapping),'proper five-colouring');five.delete();(w/'five_colouring.json').write_text(json.dumps({'vertices':selected,'colouring':colour})+'\n')
            else:status='GRAPH_UNKNOWN'
            break
        pos={l for l in graph.get_model() if l>0};colour=''.join(str(next(c for c in range(4) if 4*v+c+1 in pos)) if v in active else '.' for v in range(517))
        E.check_colouring(colour,data['edges']);colour=E.extend(colour,data['adj'],range(517));D=E.check_colouring(colour,data['edges'])
        row={'D':list(D),'source':'native','colouring':colour,'turn':turn};native.append(row);rows=E.minimal(rows+[row]);record['new_killing_set']=list(D);history.append(record)
        (w/'progress.json').write_text(json.dumps({'history':history,'rows':rows},separators=(',',':'))+'\n')
        print(json.dumps(record),flush=True)
        if not D:status='WHOLE_GRAPH_FOUR_COLOURABLE';break
    graph.delete();result={'status':status,'initial_rows':len(seeds),'initial_minimal_cuts':len(E.minimal(seeds)),'final_minimal_cuts':len(rows),'final_forced':sum(len(r['D'])==1 for r in rows),'graph_queries':sum('graph_result' in r for r in history),'master_queries':len(history),'master_seconds':master_seconds,'graph_seconds':graph_seconds,'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'final_proof':final_proof,'history':history,'candidate':candidate}
    (w/'certificate.json').write_text(json.dumps({'rows':rows},separators=(',',':'))+'\n');(w/'native_witnesses.json').write_text(json.dumps(native,separators=(',',':'))+'\n');(w/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('history','candidate')},indent=2),flush=True)


if __name__=='__main__':main()
