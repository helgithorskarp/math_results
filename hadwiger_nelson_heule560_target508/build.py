"""Complete the fixed H560 target through order 508 by positive covers."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
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


def sha(raw):return hashlib.sha256(raw).hexdigest()


def proper(word,active,edges):
    need(len(word)==632 and set(word)<=set('.0123'),'colour alphabet')
    need({v for v,c in enumerate(word) if c!='.'}==active,'exact colour domain')
    need(all(word[u]!=word[v] for u,v in edges if u in active and v in active),'all unit edges')


def prepare():
    plan=json.loads((HERE/'plan.json').read_text())
    for name,digest in plan['input_files'].items():need(sha((REPO/name).read_bytes())==digest,('input identity',name))
    _,edges,_=B.geometry()
    boundary=json.loads((REPO/'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    m492=set(boundary['mandatory_vertices']);v560=m492|set(boundary['optional_vertices'])
    base=m492|set(plan['mandatory_additions']);optional=sorted(v560-base)
    erase={510,512,513,520,521,523,524,535};free=sorted(set(optional)-erase)
    pairs=plan['disjoint_pairs'];paired=set().union(*map(set,pairs));outside=sorted(set(optional)-paired)
    need(len(base)==498 and len(optional)==62 and len(free)==54 and len(outside)==44 and len(paired)==18,'packing dimensions')
    parent=json.loads((REPO/'hadwiger_nelson_heule560_global_decision/certificate.json').read_text())
    sep=json.loads((REPO/'hadwiger_nelson_heule560_separator/certificate.json').read_text())
    rel=json.loads((REPO/'hadwiger_nelson_heule560_left_relation/certificate.json').read_text())
    full={r['state']:r['colouring'] for r in sep['blocks']['full']['states']};no310=dict(full)
    for row in rel['rows']:
        if not row['inherited_full']:no310[row['state']]=next(p['colouring'] for p in row['positive_covers'] if p['mask']==510)
    right=parent['right_vertices'];q=parent['separator'];left=sep['blocks']['full']['vertices']
    need(set(right)-base==set(free) and len(right)==196 and len(full)==20,'right oracle domain')
    adj={v:set() for v in range(632)}
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    return locals()


def paste(cs,active,g):
    state=''.join(cs[v] for v in g['q']);table=g['full'] if 310 in active else g['no310']
    need(state in table,'explicit left witness')
    colors={v:c for v,c in zip(g['left'],table[state]) if v in active}
    need(all(colors[v]==cs[v] for v in g['q']),'separator agreement');colors.update(cs)
    word=''.join(colors.get(v,'.') for v in range(632));proper(word,active,g['edges']);return word


def inherited(g):
    words=[];opt=g['parent']['optional_order']
    for row in g['parent']['positive_covers']:
        cut={v for i,v in enumerate(opt) if not row['mask']>>i&1}
        cs={v:c for v,c in zip(g['right'],row['colouring']) if c!='.'}
        words.append(paste(cs,g['v560']-cut,g))
    prior=json.loads((REPO/'hadwiger_nelson_heule560_cylinder508/certificate.json').read_text())
    for row in prior['covers']:
        cut=(g['v560']-g['erase'])-{v for v,c in enumerate(row['colouring']) if c!='.'}
        cs={v:row['colouring'][v] for v in g['right'] if row['colouring'][v]!='.'}
        words.append(paste(cs,g['v560']-cut,g))
    need(len(words)==40,'inherited cover count');return words


def targets(g):
    rows=[];pairs=g['pairs']
    for chosen in product(*pairs):
        for v in g['outside']:rows.append(tuple(sorted((*chosen,v))))
    for j,pair in enumerate(pairs):
        for chosen in product(*(p for i,p in enumerate(pairs) if i!=j)):
            rows.append(tuple(sorted((*chosen,*pair))))
    rows.sort();need(len(rows)==24832 and len(set(rows))==24832,'complete two-case family')
    return rows


def formula(g):
    right=g['right'];index={v:i for i,v in enumerate(right)};col=lambda v,c:4*index[v]+c+1
    select={v:4*len(right)+i+1 for i,v in enumerate(g['free'])};top=4*len(right)+len(select);clauses=[]
    for v in right:
        names=[col(v,c) for c in range(4)];clauses.append(names);clauses.extend([[-a,-b] for a,b in combinations(names,2)])
    for u,v in g['edges']:
        if u not in index or v not in index:continue
        guard=[-select[w] for w in (u,v) if w in select]
        for c in range(4):clauses.append(guard+[-col(u,c),-col(v,c)])
    gates=[]
    for state in g['full']:
        top+=1;gates.append(top);clauses.extend([[-top,col(v,int(c))] for v,c in zip(g['q'],state)])
    clauses.append(gates)
    raw=(f'p cnf {top} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()
    return clauses,col,select,top,raw


def covermask(word,g):
    if any(word[v]=='.' for v in g['base']):return None
    return sum(1<<i for i,v in enumerate(g['optional']) if word[v]!='.')


def covered(target,mask):return mask is not None and target&~mask==0


def main():
    from pysat.solvers import Solver
    import pysat
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--resume',action='store_true');args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=args.resume);g=prepare();old=inherited(g);rows=targets(g)
    target_masks=[sum(1<<i for i,v in enumerate(g['optional']) if v in row) for row in rows]
    oldmasks=[covermask(w,g) for w in old];inherited_remaining=[i for i,t in enumerate(target_masks) if not any(covered(t,m) for m in oldmasks)]
    cls,col,select,top,raw=formula(g);(args.out/'oracle.cnf').write_bytes(raw)
    resource.setrlimit(resource.RLIMIT_AS,(g['plan']['native_memory_bytes'],g['plan']['native_memory_bytes']))
    stats=Counter();new=[];current=None;target=None;start=time.monotonic()
    if args.resume:
        saved=json.loads((args.out/'checkpoint.json').read_text());new=saved['new_covers'];stats.update(saved['stats'])
        if saved.get('current_positive') and saved['current_positive'] not in new:new.append(saved['current_positive'])
        for word in new:
            active={v for v,c in enumerate(word) if c!='.'};proper(word,active,g['edges']);need(g['base']|g['erase']<=active<=g['v560'],'resumed cover domain')
    remaining=[i for i in inherited_remaining if not any(covered(target_masks[i],covermask(w,g)) for w in new)]
    write(args.out/'initial.json',{'necessary_targets':len(rows),'outside_40_inherited_covers':len(inherited_remaining),'remaining_after_resume':len(remaining)})
    log=(args.out/'queries.jsonl').open('a' if args.resume else 'w')
    def snapshot(status):
        write(args.out/'checkpoint.json',{'status':status,'new_covers':new,'current_positive':current,'current_target_index':target,'stats':dict(stats),'remaining':len(remaining),'next_phase_started':False})
    negative=[]
    for r in g['parent']['negative_cores']:
        vertices={v for i,v in enumerate(g['parent']['optional_order']) if r['mask']>>i&1}
        negative.append(sum(1<<i for i,v in enumerate(g['free']) if v in vertices))
    snapshot('IN_PROGRESS')
    with Solver(name='g4',bootstrap_with=cls) as primary,Solver(name='g4',bootstrap_with=cls) as growth:
        def query(mask,phase):
            assumptions=[select[v] if mask>>i&1 else -select[v] for i,v in enumerate(g['free'])]
            solver=primary if phase=='target' else growth;before=time.monotonic()
            if phase=='target':answer=primary.solve(assumptions=assumptions)
            else:
                growth.conf_budget(g['plan']['growth_conflicts']);timer=threading.Timer(g['plan']['growth_seconds'],growth.interrupt);timer.start()
                try:answer=growth.solve_limited(assumptions=assumptions,expect_interrupt=True)
                finally:timer.cancel();timer.join();growth.clear_interrupt()
            stats[phase+'_queries']+=1;stats[phase+'_'+str(answer)]+=1
            log.write(json.dumps({'phase':phase,'canonical_mask':mask,'answer':answer,'seconds':time.monotonic()-before})+'\n');log.flush()
            if answer is not True:return answer
            model={x for x in solver.get_model() if x>0};active=g['base']|g['erase']|{v for i,v in enumerate(g['free']) if mask>>i&1};cs={}
            for v in active&set(g['right']):
                colors=[str(c) for c in range(4) if col(v,c) in model];need(len(colors)==1,'native one-hot');cs[v]=colors[0]
            return paste(cs,active,g)
        def grow(word):
            nonlocal current
            current=word;snapshot('GROWING_POSITIVE');mask=sum(1<<i for i,v in enumerate(g['free']) if word[v]!='.')
            for i,v in enumerate(g['free']):
                if mask>>i&1:continue
                trial=mask|(1<<i)
                if any(n&~trial==0 for n in negative):stats['known_negative_growth_skips']+=1;continue
                used={word[w] for w in g['adj'][v] if word[w]!='.'};colors=sorted(set('0123')-used)
                if colors:
                    candidate=word[:v]+colors[0]+word[v+1:];stats['direct_growth_extensions']+=1
                else:
                    candidate=query(trial,'growth')
                    if not isinstance(candidate,str):continue
                word=candidate;mask=trial;proper(word,g['base']|g['erase']|{u for j,u in enumerate(g['free']) if mask>>j&1},g['edges']);current=word;snapshot('GROWING_POSITIVE')
            return word
        try:
            while remaining:
                target=remaining[0];current=None;snapshot('DECIDING_TARGET');selected=set(rows[target]);mask=sum(1<<i for i,v in enumerate(g['free']) if v in selected)
                word=query(mask,'target')
                if word is False:
                    write(args.out/'negative_candidate.json',{'target_index':target,'vertices':sorted(g['base']|selected),'canonical_vertices':sorted((g['base']|selected)-g['erase']),'status':'NATIVE_NEGATIVE_REQUIRES_DIRECT_PROOF','record_improvement':False})
                    snapshot('NEGATIVE_REQUIRES_INDEPENDENT_PROOF');print('NEGATIVE_REQUIRES_INDEPENDENT_PROOF',target,flush=True);return
                need(isinstance(word,str),'primary complete status');word=grow(word);mask62=covermask(word,g)
                new=[w for w in new if not covered(covermask(w,g),mask62)];new.append(word)
                remaining=[i for i in remaining if not covered(target_masks[i],mask62)];current=None;snapshot('FAMILY_CLOSED' if not remaining else 'IN_PROGRESS')
                print(json.dumps({'new_covers':len(new),'new_coloured_vertices':sum(c!='.' for c in word),'remaining_targets':len(remaining),'stats':dict(stats),'seconds':time.monotonic()-start}),flush=True)
        except BaseException:
            snapshot('INTERRUPTED_OR_ERROR_INCOMPLETE');raise
    cert={'new_H560_colourings':new,'mandatory_additions':g['plan']['mandatory_additions'],'disjoint_pairs':g['pairs'],'necessary_exact508_supports':24832,'entire_H560_through508_four_colourable':True,'record_improvement':False}
    write(args.out/'certificate.json',cert)
    allmasks=oldmasks+[covermask(w,g) for w in new];assignment=bytearray();hits=Counter()
    for mask in target_masks:
        hit=next(i for i,m in enumerate(allmasks) if covered(mask,m));hits[hit]+=1;assignment.extend(hit.to_bytes(2,'little'))
    familyraw=''.join(','.join(map(str,row))+'\n' for row in rows).encode()
    (args.out/'family.txt').write_bytes(familyraw);(args.out/'coverage.bin').write_bytes(assignment)
    report={'necessary_exact508_supports':len(rows),'outside_40_inherited_covers':len(inherited_remaining),'new_covers':len(new),'new_H560_cover_orders':[sum(c!='.' for c in w) for w in new],'remaining_targets':0,'first_cover_counts':dict(hits),'family_sha256':sha(familyraw),'coverage_sha256':sha(assignment),'oracle_variables':top,'oracle_clauses':len(cls),'oracle_bytes':len(raw),'oracle_sha256':sha(raw),'stats':dict(stats),'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'python_sat':pysat.__version__,'entire_H560_through508_four_colourable':True,'record_improvement':False,'next_phase_started':False}
    write(args.out/'result.json',report);snapshot('FAMILY_CLOSED');print(json.dumps(report,sort_keys=True),flush=True)


if __name__=='__main__':main()
