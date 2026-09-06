"""One exact criticality-screen optimization, with a checked SAT lower bound."""
import argparse
import hashlib
from itertools import combinations
import json
from math import comb
from pathlib import Path
import resource
import subprocess
import sys
import threading
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
sys.path.insert(0,str(REPO/'hadwiger_nelson_heule632_pair_pilot'))
import build as B


def need(ok,why):
    if not ok:raise ValueError(why)


def write(path,data):
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')


def sha(raw):return hashlib.sha256(raw).hexdigest()


def packing_certificate(covers):
    # Extracted after the bounded optimization; these constants are a short
    # certificate, not an assumption made by the native search.
    pairs=[[358,362],[361,379],[406,455],[407,440],[409,542],
           [431,505],[434,530],[500,571],[604,613]]
    need(all(pair in covers for pair in pairs),'published pair clauses')
    need(len({v for pair in pairs for v in pair})==18,'disjoint cover pairs')
    return {'disjoint_cover_pairs':pairs,
            'outer_exact508_support_count':sum(comb(9,d)*2**(9-d)*comb(39,4-d) for d in range(5)),
            'outer_family_only':True}


def prepare():
    plan=json.loads((HERE/'plan.json').read_text())
    for path,digest in plan['input_files'].items():need(sha((REPO/path).read_bytes())==digest,('input',path))
    points,host_edges,_=B.geometry()
    boundary=json.loads((REPO/'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    m=set(boundary['mandatory_vertices'])|set(plan['mandatory_added'])
    u=sorted(set(boundary['optional_vertices'])-{510,512,513,520,521,523,524,535}-set(plan['mandatory_added']))
    vertices=m|set(u);edges=[(a,b) for a,b in host_edges if a in vertices and b in vertices]
    adj={v:set() for v in vertices}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    parent=json.loads((REPO/'hadwiger_nelson_heule560_global_decision/certificate.json').read_text())
    old=json.loads((REPO/'hadwiger_nelson_heule560_kempe/certificate.json').read_text())
    omitted=[]
    for row in parent['positive_covers']:
        missing={v for i,v in enumerate(parent['optional_order']) if not row['mask']>>i&1}
        if not missing&m:omitted.append(sorted(missing))
    for row in old['maximal_extending_cover_colourings']:
        missing=set(row['omitted_optional'])
        if not missing&m:omitted.append(sorted(missing&set(u)))
    clauses=sorted({tuple(c) for c in omitted},key=lambda c:(len(c),c))
    # Drop a clause only when another stored clause implies it.
    clauses=[list(c) for c in clauses if not any(set(d)<set(c) for d in clauses)]
    need(len(m)==495 and len(u)==57 and len(edges)==2726,'family dimensions')
    return plan,m,u,edges,adj,clauses


def core_formula(m,u,adj,covers,gallai):
    selector={v:i+1 for i,v in enumerate(u)};clauses=[[selector[v] for v in c] for c in covers]
    top=len(u);low={};threshold={}
    for v in sorted(m|set(u)):
        neighbours=sorted(adj[v]&set(u));b=len(adj[v]&m);d=4-b
        if d>0:
            if len(neighbours)<d:
                clauses.append([-selector[v]] if v in selector else [])
            else:
                for group in combinations(neighbours,len(neighbours)-d+1):
                    clauses.append(([-selector[v]] if v in selector else [])+[selector[x] for x in group])
        if b>4:continue
        top+=1;high=top;threshold[v]=high
        top+=1;low[v]=top
        k=5-b;n=len(neighbours)
        if k>n:clauses.append([-high])
        else:
            clauses.extend([[-high]+[selector[x] for x in group] for group in combinations(neighbours,n-k+1)])
            clauses.extend([[high]+[-selector[x] for x in group] for group in combinations(neighbours,k)])
        if v in selector:
            clauses.extend([[-low[v],selector[v]],[-low[v],-high],[-selector[v],high,low[v]]])
        else:clauses.extend([[low[v],high],[-low[v],-high]])
    for block in gallai:clauses.append([-low[v] for v in block])
    return clauses,top,selector,low


def cardinality(base,top,selectors,budget):
    clauses=[list(c) for c in base];xs=list(selectors.values());n=len(xs)
    z={}
    for i in range(n+1):
        for j in range(budget+2):top+=1;z[i,j]=top
    for i in range(n+1):clauses.append([z[i,0]])
    for j in range(1,budget+2):clauses.append([-z[0,j]])
    for i,x in enumerate(xs,1):
        for j in range(1,budget+2):
            a=z[i-1,j];b=z[i-1,j-1];c=z[i,j]
            clauses.extend([[-a,c],[-b,-x,c],[-c,a,b],[-c,a,x]])
    clauses.append([-z[n,budget+1]])
    return clauses,top


def dimacs(clauses,top):return (f'p cnf {top} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')


def blocks(vertices,adj):
    clock=0;disc={};lo={};stack=[];answer=[]
    def dfs(v,parent):
        nonlocal clock
        clock+=1;disc[v]=lo[v]=clock
        for w in sorted(adj[v]&vertices):
            if w==parent:continue
            if w not in disc:
                stack.append((v,w));dfs(w,v);lo[v]=min(lo[v],lo[w])
                if lo[w]>=disc[v]:
                    block=set()
                    while True:
                        e=stack.pop();block.update(e)
                        if e==(v,w):break
                    answer.append(sorted(block))
            elif disc[w]<disc[v]:stack.append((v,w));lo[v]=min(lo[v],disc[w])
    for v in sorted(vertices):
        if v not in disc:
            if not adj[v]&vertices:answer.append([v])
            else:dfs(v,None)
    return sorted(answer,key=lambda b:(len(b),b))


def is_allowed(block,adj):
    co=set(block);n=len(co);ds=[len(adj[v]&co) for v in co]
    return all(d==n-1 for d in ds) or (n>=3 and n%2==1 and all(d==2 for d in ds))


def witness(chosen,m,adj,covers):
    vs=m|chosen;degrees={v:len(adj[v]&vs) for v in vs}
    need(all(d>=4 for d in degrees.values()),'actual minimum degree')
    need(all(chosen&set(c) for c in covers),'actual cover clauses')
    low={v for v,d in degrees.items() if d==4};parts=blocks(low,adj)
    return {'selected_optional':sorted(chosen),'vertices':len(vs),'low_vertices':sorted(low),
            'low_edges':[[a,b] for a in sorted(low) for b in sorted(adj[a]&low) if a<b],
            'low_blocks':parts,'bad_blocks':[b for b in parts if not is_allowed(b,adj)]}


def limits():
    resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3));resource.setrlimit(resource.RLIMIT_FSIZE,(512*1024**2,512*1024**2))


def main():
    from pysat.solvers import Solver
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path)
    ap.add_argument('--kissat',default='/scratch/researcher3-kissat/build/kissat');ap.add_argument('--drat-trim',default='/scratch/drat-trim-package/usr/bin/drat-trim')
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False)
    plan,m,u,edges,adj,covers=prepare();limits();started=time.monotonic();gallai=[];queries=0;result=None;last_unsat=-1;log=[];stopped=None
    for budget in range(plan['target_budget']+1):
        base,top,selectors,low=core_formula(m,u,adj,covers,gallai);cs,nv=cardinality(base,top,selectors,budget)
        with Solver(name='g4',bootstrap_with=cs) as solver:
            while True:
                if time.monotonic()-started>=plan['search_seconds'] or queries>=plan['master_query_cap'] or len(gallai)>=plan['gallai_cut_cap']:
                    stopped='GLOBAL_LIMIT';break
                solver.conf_budget(plan['query_conflicts']);timer=threading.Timer(plan['query_seconds'],solver.interrupt);timer.start()
                try:answer=solver.solve_limited(expect_interrupt=True)
                finally:timer.cancel();timer.join()
                solver.clear_interrupt();queries+=1;log.append({'budget':budget,'answer':answer,'gallai_cuts':len(gallai)})
                if answer is None:stopped='QUERY_LIMIT';break
                if not answer:last_unsat=budget;break
                model={x for x in solver.get_model() if x>0};selected={v for v in u if selectors[v] in model}
                need(len(selected)<=budget,'actual budget');w=witness(selected,m,adj,covers)
                need({v for v in low if low[v] in model}==set(w['low_vertices']),'encoded low flags')
                if not w['bad_blocks']:result=w;break
                block=w['bad_blocks'][0];need(block not in gallai,'new Gallai block')
                gallai.append(block);solver.add_clause([-low[v] for v in block])
            write(args.out/'checkpoint.json',{'last_unsat':last_unsat,'witness':result,'gallai_cuts':gallai,'queries':queries,'seconds':time.monotonic()-started,'status':stopped or 'SEARCHING'})
        if stopped or result is not None:break
    report={'last_unsat_budget':last_unsat,'minimum_if_attained':None if result is None else len(result['selected_optional']),
            'gallai_cuts':gallai,'queries':queries,'search_seconds':time.monotonic()-started,'status':stopped or ('OPTIMUM_FOUND' if result else 'TARGET_INFEASIBLE'),
            'cover_clauses':covers,'record_improvement':False,'lower_bound_verified':False,'next_phase_started':False}
    cert={'witness':result,'gallai_cuts':gallai,'lower_bound_budget':last_unsat,'mandatory_added':plan['mandatory_added']}
    cert.update(packing_certificate(covers))
    write(args.out/'certificate.json',cert);write(args.out/'queries.json',log);write(args.out/'result.json',report)
    if last_unsat>=0:
        base,top,selectors,low=core_formula(m,u,adj,covers,gallai);cs,nv=cardinality(base,top,selectors,last_unsat);raw=dimacs(cs,nv)
        cnf=args.out/'lower.cnf';cnf.write_bytes(raw);proof=args.out/'lower.drat'
        with (args.out/'kissat.log').open('wb') as out:
            r=subprocess.run([args.kissat,'--seed=0','--conflicts=4000000','--time=180',str(cnf),str(proof)],stdout=out,stderr=subprocess.STDOUT,timeout=200,preexec_fn=limits)
        need(r.returncode==20,'lower bound UNSAT')
        with (args.out/'drat.log').open('wb') as out:
            r=subprocess.run([args.drat_trim,str(cnf),str(proof)],stdout=out,stderr=subprocess.STDOUT,timeout=200,preexec_fn=limits)
        need(r.returncode==0 and b's VERIFIED' in (args.out/'drat.log').read_bytes().splitlines(),'lower bound DRAT')
        manifest={'cnf_sha256':sha(raw),'cnf_bytes':len(raw),'variables':nv,'clauses':len(cs),'proof_sha256':sha(proof.read_bytes()),'proof_bytes':proof.stat().st_size,
                  'solver_sha256':sha(Path(args.kissat).read_bytes()),'checker_sha256':sha(Path(args.drat_trim).read_bytes()),'verified':True}
        write(args.out/'proof_manifest.json',manifest);report['lower_bound_verified']=True
    report['total_seconds']=time.monotonic()-started;write(args.out/'result.json',report);write(args.out/'checkpoint.json',report)
    print(json.dumps(report,sort_keys=True),flush=True)


if __name__=='__main__':main()
