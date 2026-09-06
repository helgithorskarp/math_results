#!/usr/bin/env python3
"""One bounded selector-SAT sweep; only positive decisions are certificates here."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import resource
import sys
from threading import Timer
import time

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'hadwiger_nelson_heule632_pair_pilot'
sys.path.insert(0,str(PARENT))
import build as B
import independent as I


def save(p,x):
    q=p.with_suffix(p.suffix+'.tmp');q.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');q.replace(p)


def selector_formula(n,edges,triangle,k=4):
    clauses=[];a=lambda v:k*n+v+1;x=lambda v,c:k*v+c+1
    for v in range(n):
        clauses.append([x(v,c) for c in range(k)])
        clauses.extend([[-x(v,c),-x(v,d)] for c,d in combinations(range(k),2)])
    for u,v in edges:
        clauses.extend([[-a(u),-a(v),-x(u,c),-x(v,c)] for c in range(k)])
    clauses.extend([[-a(v),x(v,c)] for c,v in enumerate(triangle)])
    return clauses


def positive(text,active,edges):
    I.check(len(text)==632,'positive host length')
    I.check({v for v,c in enumerate(text) if c!='.'}==set(active),'positive exact support')
    return I.colouring(text,sorted(set(range(632))-set(active)),edges,4)


def controls(out):
    from pysat.solvers import Glucose4
    start=time.monotonic();out.mkdir(parents=True,exist_ok=False);possible=list(combinations(range(3),2));count=0
    for bits in range(8):
        es=[e for j,e in enumerate(possible) if bits>>j&1];tri=[0,1,2] if len(es)==3 else []
        clauses=selector_formula(3,es,tri)
        for word in product((False,True),repeat=15):
            actual=all(any(word[abs(x)-1]==(x>0) for x in c) for c in clauses)
            sets=[{c for c in range(4) if word[4*v+c]} for v in range(3)]
            expected=all(len(s)==1 for s in sets)
            if expected:
                colours=[next(iter(s)) for s in sets];active={v for v in range(3) if word[12+v]}
                expected=all(u not in active or v not in active or colours[u]!=colours[v] for u,v in es)
                expected=expected and all(v not in active or colours[v]==c for c,v in enumerate(tri))
            I.check(actual==expected,'selector Boolean semantics');count+=1
    clauses=selector_formula(5,list(combinations(range(5),2)),[0,1,2]);statuses=Counter()
    with Glucose4(bootstrap_with=clauses) as solver:
        for mask in range(32):
            active={v for v in range(5) if mask>>v&1};ans=solver.solve(assumptions=[(21+v)*(1 if v in active else -1) for v in range(5)])
            I.check(ans==(len(active)<=4),'K5 every selected subset');statuses[str(ans)]+=1
    report={'status':'ALL SELECTOR CONTROLS VERIFIED','boolean_assignments':count,'K5_activation_masks':dict(statuses),'seconds':time.monotonic()-start}
    save(out/'controls.json',report);print(json.dumps(report,indent=2))


def run(out,control_path):
    from pysat.solvers import Glucose4
    import pysat,pysolvers
    start=time.monotonic();plan=json.loads((HERE/'plan.json').read_text())
    tests=json.loads(control_path.read_text());I.check(tests['boolean_assignments']==262144 and tests['status']=='ALL SELECTOR CONTROLS VERIFIED','controls first')
    I.check(pysat.__version__==plan['search_solver']['python_sat_version'],'solver package version')
    I.check(sha256(Path(pysolvers.__file__).read_bytes()).hexdigest()==plan['search_solver']['native_module_sha256'],'solver executable identity')
    for rel,digest in plan['input_files'].items():I.check(sha256((HERE.parent/rel).read_bytes()).hexdigest()==digest,'input identity')
    resource.setrlimit(resource.RLIMIT_AS,(plan['limits']['address_space_bytes'],)*2)
    resource.setrlimit(resource.RLIMIT_FSIZE,(plan['limits']['output_file_bytes'],)*2)
    _,edges,_=B.geometry();_,ind_edges,_=I.geometry();I.check(edges==ind_edges,'independent exact graph')
    active=set(range(632))-set(plan['seed_omissions']);degree={v:sum(u in active and w in active and v in (u,w) for u,w in edges) for v in active}
    I.check(plan['order']==sorted(active,key=lambda v:(v<510,degree[v],v)),'frozen initial order')
    adjacency={v:set() for v in range(632)}
    for u,v in edges:adjacency[u].add(v);adjacency[v].add(u)
    rows=json.loads((HERE/'initial_positive.json').read_text());library=[]
    for row in rows:
        text=row['colouring'];domain={v for v,c in enumerate(text) if c!='.'};positive(text,domain,edges)
        library.append((row['source'],domain,text))
    out.mkdir(parents=True,exist_ok=False);events=[];native_queries=0;unknown=[];witnesses=[]
    def checkpoint(index,phase):
        save(out/'checkpoint.json',{'phase':phase,'next_order_index':index,'retained':sorted(active),'native_queries':native_queries,'unknown':unknown,'events':len(events),'positive_rows':len(witnesses)})
        save(out/'events.json',events)
    formula=selector_formula(632,edges,[0,143,146]);var_count=5*632
    raw=(f'p cnf {var_count} {len(formula)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in formula)).encode()
    (out/'selector.cnf').write_bytes(raw)
    with Glucose4(bootstrap_with=formula) as solver, (out/'positive.jsonl').open('w') as stream:
        for index,v in enumerate(plan['order']):
            # These removals preserve non-four-colourability by colour restoration.
            while True:
                low=next((u for u in sorted(active) if len(adjacency[u]&active)<=3),None)
                if low is None:break
                deg=len(adjacency[low]&active);active.remove(low);events.append({'index':index,'vertex':low,'status':'DEGREE_REMOVED','degree':deg,'vertices_after':len(active)})
            if len(active)<=508:checkpoint(index,'TARGET SIZE REACHED;FINAL CERTIFICATE REQUIRED');break
            if v not in active:continue
            witness=next(((tag,domain,text) for tag,domain,text in library if active-domain=={v}),None)
            if witness is not None:
                events.append({'index':index,'vertex':v,'status':'POSITIVE_COVER','source':witness[0],'vertices_after':len(active)});continue
            trial=active-{v};assumptions=[(2529+u)*(1 if u in trial else -1) for u in range(632)]
            checkpoint(index,'SELECTOR QUERY IN FLIGHT')
            solver.clear_interrupt();solver.conf_budget(plan['search_solver']['conflicts_per_query']);before=solver.accum_stats();begin=time.monotonic()
            timer=Timer(plan['search_solver']['interrupt_seconds_per_query'],solver.interrupt);timer.daemon=True;timer.start()
            try:answer=solver.solve_limited(assumptions=assumptions,expect_interrupt=True)
            finally:timer.cancel();timer.join();solver.clear_interrupt()
            elapsed=time.monotonic()-begin;after=solver.accum_stats();native_queries+=1
            info={'index':index,'vertex':v,'status':'UNSAT_PROVISIONAL' if answer is False else 'SAT_VERIFIED' if answer else 'UNKNOWN','seconds':elapsed,'conflicts':after['conflicts']-before['conflicts']}
            if answer is False:active.remove(v)
            elif answer is True:
                model=solver.get_model();truth={abs(x):x>0 for x in model}
                I.check(all(truth[abs(x)]==(x>0) for x in assumptions),'all selector assumptions')
                I.check(all(any(truth[abs(x)]==(x>0) for x in clause) for clause in formula),'every model clause')
                text=['.']*632
                for u in trial:
                    colours=[c for c in range(4) if truth[4*u+c+1]];I.check(len(colours)==1,'model one-hot');text[u]=str(colours[0])
                text=''.join(text);info['edge_checks']=positive(text,trial,edges)
                row={'source':'query:'+str(native_queries-1),'vertex':v,'colouring':text};witnesses.append(row);stream.write(json.dumps(row,sort_keys=True)+'\n');stream.flush()
                library.append((row['source'],trial,text))
            else:unknown.append(v)
            info['vertices_after']=len(active);events.append(info)
            if answer is False or native_queries%25==0:print(json.dumps({'queries':native_queries,'vertex':v,'status':info['status'],'retained':len(active),'elapsed':time.monotonic()-start}),flush=True)
            checkpoint(index+1,'SWEEP CHECKPOINT')
        else:checkpoint(len(plan['order']),'SWEEP COMPLETE;FINAL CERTIFICATE REQUIRED')
    final_witnesses={};checks=0
    for v in sorted(active):
        row=next(((tag,text) for tag,domain,text in library if active-domain=={v}),None)
        if row is not None:
            tag,text=row;text=''.join(c if u in active-{v} else '.' for u,c in enumerate(text));checks+=positive(text,active-{v},edges)
            final_witnesses[str(v)]={'source':tag,'colouring':text}
    save(out/'final_deletions.json',final_witnesses)
    inherited=json.loads((PARENT/'certificate.json').read_text())['five_colouring']
    five=''.join(c if v in active else '.' for v,c in enumerate(inherited));I.colouring(five,sorted(set(range(632))-active),edges,5)
    report={'status':'ONE SWEEP COMPLETE;FINAL NON-FOUR-COLOURABILITY UNVERIFIED','retained':sorted(active),'omitted':sorted(set(range(632))-active),'vertices':len(active),'unit_edges':sum(u in active and v in active for u,v in edges),'five_colouring':five,'native_queries':native_queries,'events':dict(Counter(e['status'] for e in events)),'singleton_witnesses':len(final_witnesses),'unresolved_singletons':sorted(active-set(map(int,final_witnesses))),'deletion_edge_checks':checks,'selector_cnf_sha256':sha256(raw).hexdigest(),'seconds':time.monotonic()-start,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    save(out/'search_result.json',report);checkpoint(len(plan['order']),'SEARCH COMPLETE;FINAL CERTIFICATE REQUIRED');print(json.dumps({k:v for k,v in report.items() if k not in ('retained','omitted','five_colouring')},indent=2),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--controls',action='store_true');g.add_argument('--run-with-controls',type=Path)
    a=ap.parse_args();controls(a.out) if a.controls else run(a.out,a.run_with_controls)
