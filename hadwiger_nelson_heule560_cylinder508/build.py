"""Classify the complete 194580-member exact-508 cylinder by positive covers."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from math import comb
from pathlib import Path
import resource
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
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n');tmp.replace(path)


def sha(data):return hashlib.sha256(data).hexdigest()


def prepare():
    plan=json.loads((HERE/'plan.json').read_text())
    for name,digest in plan['input_files'].items():need(sha((REPO/name).read_bytes())==digest,('input',name))
    _,host_edges,_=B.geometry()
    boundary=json.loads((REPO/'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    parent=json.loads((REPO/'hadwiger_nelson_heule560_global_decision/certificate.json').read_text())
    expected=json.loads((REPO/'hadwiger_nelson_heule560_global_decision/expected.json').read_text())
    sep=json.loads((REPO/'hadwiger_nelson_heule560_separator/certificate.json').read_text())
    m=set(boundary['mandatory_vertices']);fixed=set(plan['base_optional']);optional=parent['optional_order']
    need(sorted(fixed)==expected['residual_required_vertices'],'published cylinder')
    free=sorted(set(optional)-fixed);base=m|fixed;vertices=m|set(optional)
    right=parent['right_vertices'];q=parent['separator'];es=[(u,v) for u,v in host_edges if u in right and v in right]
    states={row['state']:row for row in sep['blocks']['full']['states']}
    need(len(m)==492 and len(base)==504 and len(free)==48 and len(states)==20,'family dimensions')
    need(set(free)==set(right)-base and len(right)==196 and len(es)==806,'exact right split')
    oldmask=sum(1<<i for i,v in enumerate(optional) if v in fixed)
    need(all(oldmask&~row['mask'] for row in parent['positive_covers']),'outside all35 covers')
    kempe=json.loads((REPO/'hadwiger_nelson_heule560_kempe/certificate.json').read_text())
    need(all(fixed&set(row['omitted_optional']) for row in kempe['maximal_extending_cover_colourings']),'outside all10 Kempe covers')
    adj={v:set() for v in range(632)}
    for u,v in host_edges:adj[u].add(v);adj[v].add(u)
    neg=[]
    for row in parent['negative_cores']:
        chosen={v for i,v in enumerate(optional) if row['mask']>>i&1}
        neg.append(sum(1<<i for i,v in enumerate(free) if v in chosen))
    return {'plan':plan,'base':base,'free':free,'right':right,'q':q,'es':es,'states':states,
            'left':sep['blocks']['full']['vertices'],'adj':adj,'host_edges':host_edges,'negative_free_masks':neg}


def formula(g):
    right=g['right'];index={v:i for i,v in enumerate(right)}
    col=lambda v,c:4*index[v]+c+1
    select={v:4*len(right)+i+1 for i,v in enumerate(g['free'])};top=4*len(right)+len(select)
    clauses=[]
    for v in right:
        names=[col(v,c) for c in range(4)];clauses.append(names)
        clauses.extend([[-a,-b] for a,b in combinations(names,2)])
    for u,v in g['es']:
        guard=[-select[w] for w in (u,v) if w in select]
        for c in range(4):clauses.append(guard+[-col(u,c),-col(v,c)])
    gates=[]
    for state in g['states']:
        top+=1;gates.append(top)
        clauses.extend([[-top,col(v,int(c))] for v,c in zip(g['q'],state)])
    clauses.append(gates)
    return clauses,col,select,top


def dimacs(clauses,top):return (f'p cnf {top} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()


def check_full(text,mask,g):
    support=g['base']|{v for i,v in enumerate(g['free']) if mask>>i&1}
    need(len(text)==632 and {v for v,c in enumerate(text) if c!='.'}==support,'colouring support')
    need(set(text)<=set('.0123'),'colour domain')
    need(all(text[u]!=text[v] for u,v in g['host_edges'] if u in support and v in support),'every whole-graph unit edge')


def decode(solver,mask,g,col):
    model={x for x in solver.get_model() if x>0};active=g['base']|{v for i,v in enumerate(g['free']) if mask>>i&1}
    cs={}
    for v in set(g['right'])&active:
        colours=[c for c in range(4) if col(v,c) in model];need(len(colours)==1,'native one-hot');cs[v]=str(colours[0])
    state=''.join(cs[v] for v in g['q']);need(state in g['states'],'P20 boundary word')
    left={v:c for v,c in zip(g['left'],g['states'][state]['colouring']) if v in active}
    need(all(left[v]==cs[v] for v in g['q']),'boundary agreement');left.update(cs)
    text=''.join(left.get(v,'.') for v in range(632));check_full(text,mask,g)
    return {'mask':mask,'colouring':text}


def main():
    from pysat.solvers import Solver
    import pysat
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--resume',action='store_true');args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=args.resume);g=prepare();clauses,col,select,top=formula(g)
    raw=dimacs(clauses,top);(args.out/'oracle.cnf').write_bytes(raw)
    resource.setrlimit(resource.RLIMIT_AS,(g['plan']['native_memory_bytes'],g['plan']['native_memory_bytes']))
    start=time.monotonic();covers=[];stats=Counter();current=None
    if args.resume:
        saved=json.loads((args.out/'checkpoint.json').read_text());covers=saved['covers'];stats.update(saved['stats']);current=saved.get('current_positive')
        if current and all(current['mask']!=r['mask'] for r in covers):covers.append(current)
        for row in covers:check_full(row['colouring'],row['mask'],g)
        current=None
    all_targets=[sum(1<<i for i in t) for t in combinations(range(48),4)]
    need(len(all_targets)==comb(48,4)==194580,'complete family enumeration')
    remaining=[t for t in all_targets if not any(t&~r['mask']==0 for r in covers)]
    log=(args.out/'queries.jsonl').open('a' if args.resume else 'w')
    def snapshot(status):
        write(args.out/'checkpoint.json',{'status':status,'covers':covers,'current_positive':current,'stats':dict(stats),
              'remaining':len(remaining),'seconds_this_execution':time.monotonic()-start,'next_phase_started':False})
    snapshot('IN_PROGRESS')
    with Solver(name='g4',bootstrap_with=clauses) as primary, Solver(name='g4',bootstrap_with=clauses) as growth:
        def query(mask,phase):
            assumptions=[select[v] if mask>>i&1 else -select[v] for i,v in enumerate(g['free'])]
            before=time.monotonic();solver=primary if phase=='target' else growth
            if phase=='target':answer=primary.solve(assumptions=assumptions)
            else:
                growth.conf_budget(g['plan']['growth_conflicts']);timer=threading.Timer(g['plan']['growth_seconds'],growth.interrupt);timer.start()
                try:answer=growth.solve_limited(assumptions=assumptions,expect_interrupt=True)
                finally:timer.cancel();timer.join();growth.clear_interrupt()
            stats[phase+'_queries']+=1;stats[phase+'_'+str(answer)]+=1
            log.write(json.dumps({'phase':phase,'mask':mask,'answer':answer,'seconds':time.monotonic()-before})+'\n');log.flush()
            if answer is True:return decode(solver,mask,g,col)
            return answer

        def grow(row):
            nonlocal current
            current=row;snapshot('GROWING_POSITIVE')
            for i,v in enumerate(g['free']):
                if row['mask']>>i&1:continue
                trial=row['mask']|(1<<i)
                if any(neg&~trial==0 for neg in g['negative_free_masks']):stats['known_negative_growth_skips']+=1;continue
                text=row['colouring'];used={text[w] for w in g['adj'][v] if text[w]!='.'};available=sorted(set('0123')-used)
                if available:
                    row={'mask':trial,'colouring':text[:v]+available[0]+text[v+1:]};check_full(row['colouring'],trial,g);stats['direct_growth_extensions']+=1
                else:
                    candidate=query(trial,'growth')
                    if not isinstance(candidate,dict):continue
                    row=candidate
                current=row;snapshot('GROWING_POSITIVE')
            return row

        try:
            while remaining:
                mask=0 if not covers and stats['target_queries']==0 else remaining[0]
                current=None;snapshot('DECIDING_BASE' if mask==0 else 'DECIDING_TARGET')
                row=query(mask,'target')
                if row is False:
                    write(args.out/'negative_candidate.json',{'free_mask':mask,'selected_free':[v for i,v in enumerate(g['free']) if mask>>i&1],
                          'vertices':504+mask.bit_count(),'status':'NATIVE_NEGATIVE_REQUIRES_DIRECT_PROOF','record_improvement':False})
                    snapshot('NEGATIVE_REQUIRES_INDEPENDENT_PROOF');print('NEGATIVE_REQUIRES_INDEPENDENT_PROOF',mask,flush=True);return
                need(isinstance(row,dict),'primary complete solver status')
                row=grow(row)
                covers=[old for old in covers if old['mask']&~row['mask']]
                if not any(row['mask']&~old['mask']==0 for old in covers):covers.append(row)
                remaining=[t for t in remaining if t&~row['mask']]
                current=None;snapshot('FAMILY_CLOSED' if not remaining else 'IN_PROGRESS')
                print(json.dumps({'covers':len(covers),'new_cover_free_size':row['mask'].bit_count(),'remaining_targets':len(remaining),'stats':dict(stats),'seconds':time.monotonic()-start}),flush=True)
        except BaseException:
            snapshot('INTERRUPTED_OR_ERROR_INCOMPLETE');raise
    cert={'base_optional':g['plan']['base_optional'],'free_optional':g['free'],'choose_free':4,'family_size':194580,'covers':covers,
          'entire_defined_family_four_colourable':True,'whole_h560_target_family_closed':False,'record_improvement':False}
    write(args.out/'certificate.json',cert)
    report={'family_size':194580,'remaining_targets':len(remaining),'positive_covers':len(covers),'cover_free_sizes':[r['mask'].bit_count() for r in covers],
            'oracle_variables':top,'oracle_clauses':len(clauses),'oracle_sha256':sha(raw),'oracle_bytes':len(raw),'stats':dict(stats),
            'python_sat':pysat.__version__,'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'entire_defined_family_four_colourable':True,'whole_h560_target_family_closed':False,'record_improvement':False,'next_phase_started':False}
    write(args.out/'result.json',report);snapshot('FAMILY_CLOSED');print(json.dumps(report,sort_keys=True),flush=True)


if __name__=='__main__':main()
