#!/usr/bin/env python3
"""Direct whole-H514 certificate: 503 forced vertices and 462 omissions.

The default proof needs no residual census, native solver or archived run.
Optional run auditing checks all 8974 historical rows and every native model.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations,product
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def need(ok,why):
    if not ok:raise ValueError(why)
def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def module(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


def check_colour(c,D,edges):
    need(len(c)==514 and set(c)<=set('.0123'),'colour domain')
    need([v for v,x in enumerate(c) if x=='.']==list(D),'exact omissions')
    checks=0
    for u,v in edges:
        if c[u]!='.' and c[v]!='.':need(c[u]!=c[v],'unit inequality');checks+=1
    return checks


def public_inputs():
    for name,digest in load(HERE/'manifest.json').items():
        need(sha256((REPO/name).read_bytes()).hexdigest()==digest,('pinned input',name))
    # Reuse the independently published exact norm checker, not native packets.
    G=module('exact_squarefree_geometry',REPO/'hadwiger_nelson_heule514_path_projection/verify.py')
    edges,boundary_checks,boundary=G.geometry()
    P=module('public_recipe_decoder',REPO/'hadwiger_nelson_heule514_interface/verify.py')
    R=module('reviewed_positive_decoder',REPO/'hadwiger_nelson_heule517_whole_decision_review1/independent_check.py')
    old=load(REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json')
    labels=[v for v in range(553) if '510' in old['provenance'][v]]
    large={i for i,v in enumerate(labels) if all(Fraction(old['coordinates'][str(v)][a][k])==0 for a in (0,1) for k in (2,3,6,7))}
    groups=R.inherited_witnesses(REPO,old,labels,large,set(range(517))-large)
    source=[c for name in ['prior','small','large2','large3','large4'] for row,c in groups[name]]
    source += [r['colouring'] for r in load(REPO/'hadwiger_nelson_heule517_whole_decision/certificate.json')['rows']]
    need(len(source)==963,'source recipe indexing')
    parent=load(REPO/'hadwiger_nelson_heule514_interface/certificate.json')
    colours=[P.decode(r,source) for r in parent['transport']]+[r['colouring'] for r in parent['native']]
    initial=sorted([([v for v,c in enumerate(s) if c=='.'],s) for s in colours],key=lambda r:(len(r[0]),r[0]))
    need(len(initial)==516 and len({tuple(D) for D,c in initial})==516,'initial positive library')
    rows=[dict(group='interface',index=i,D=D,colouring=c) for i,(D,c) in enumerate(initial)]
    prior=load(REPO/'hadwiger_nelson_heule514_profile_pilot/certificate.json')
    fresh=load(HERE/'certificate.json')
    need(len(prior)==15 and len(fresh)==13,'new certificate groups')
    rows += [dict(group='profile',index=r['index'],D=r['D'],colouring=r['colouring']) for r in prior]
    rows += [dict(group='whole',index=r['index'],D=r['D'],colouring=r['colouring']) for r in fresh]
    checks=0
    for row in rows:
        D=row['D'];need(D==sorted(set(D)) and set(D)<=set(range(514)),'omission domain')
        checks+=check_colour(row['colouring'],D,edges)
    return edges,rows,checks,boundary_checks


def direct_closure(edges,rows,out):
    adjacency=[set() for _ in range(514)]
    for u,v in edges:adjacency[u].add(v);adjacency[v].add(u)
    forced={r['D'][0] for r in rows if len(r['D'])==1};free=sorted(set(range(514))-forced)
    need(len(forced)==503 and len(free)==11,'singleton forcing size')
    domains=[set(r['D']) for r in rows];hist=Counter();special=[];edge_checks=0;tags=[]
    cases=0
    for O in combinations(free,6):
        cases+=1;missing=set(O);live=set(range(514))-missing
        witness=next((i for i,D in enumerate(domains) if D<=missing),None);rounds=[]
        if witness is None:
            while True:
                remove=sorted(v for v in live if len(adjacency[v]&live)<=3)
                if not remove:break
                rounds.append(remove);live.difference_update(remove)
            witness=next((i for i,D in enumerate(domains) if not D.intersection(live)),None)
            need(witness is not None,'uncovered direct whole-support case')
            hist['peeled']+=1
        else:hist['direct']+=1
        seed=rows[witness];c=[seed['colouring'][v] if v in live else '.' for v in range(514)]
        for round_ in reversed(rounds):
            for v in reversed(round_):
                coloured=[c[u] for u in adjacency[v] if c[u]!='.']
                need(len(coloured)<=3,'reverse peeling degree')
                c[v]=min(set('0123')-set(coloured))
        edge_checks+=check_colour(c,O,edges)
        tags.append(f'{seed["group"]}:{seed["index"]}')
        if rounds:special.append(dict(omitted=list(O),rounds=rounds,witness_group=seed['group'],witness_index=seed['index'],seed_D=seed['D']))
    need(cases==462 and hist==Counter(direct=458,peeled=4),'complete 11-choose-6 certificate')
    tag_raw=''.join(t+'\n' for t in tags).encode('ascii');(out/'direct_tags.txt').write_bytes(tag_raw)
    result=dict(forced_vertices=len(forced),free_vertices=free,omissions_per_case=6,cases=cases,
                directly_covered=hist['direct'],peeling_cases=hist['peeled'],all_508_vertex_colourings_checked=cases,
                target_edge_checks=edge_checks,peeling_witnesses=special,
                direct_tag_bytes=len(tag_raw),direct_tag_sha256=sha256(tag_raw).hexdigest())
    save(out/'direct_certificate.json',result)
    return result


def audit_run(frontier,run,edges,out):
    plan=load(HERE/'plan.json');raw=frontier.read_bytes()
    need(sha256(raw).hexdigest()==plan['frontier']['sha256'],'historical input frontier')
    candidates=[tuple(map(int,l.split(','))) for l in raw.decode('ascii').splitlines()]
    need(len(candidates)==len(set(candidates))==8974 and candidates==sorted(candidates,key=lambda O:(len(O),O)),'complete canonical historical input')
    cert=load(HERE/'certificate.json');cuts={tuple(r['D']):r['index'] for r in cert};sizes=sorted({len(D) for D in cuts})
    coverage=[];edge_checks=0;hist=Counter()
    for O in candidates:
        indices=[cuts[D] for k in sizes for D in combinations(O,k) if D in cuts]
        need(bool(indices),'historical residual uncovered');i=min(indices);coverage.append(i);hist[i]+=1
        c=['.' if v in O else cert[i]['colouring'][v] for v in range(514)]
        edge_checks+=check_colour(c,O,edges)
    tags=''.join(str(i)+'\n' for i in coverage).encode('ascii')
    result=load(HERE/'result.json')
    need(result['covered']==result['input_rows']==8974 and result['unresolved']==0 and result['family_closed'],'public closure result')
    need(sha256(tags).hexdigest()==result['coverage_sha256'] and len(tags)==result['coverage_bytes'],'historical final tags')
    need((run/'coverage.txt').read_bytes()==tags and (run/'survivors.txt').read_bytes()==b'','native final streams')
    need(result['first_cover_histogram']=={str(k):v for k,v in sorted(hist.items())},'final witness census')
    native=load(run/'native.json');native_by_index={r['index']:r for r in native};raw_witnesses=load(run/'raw_witnesses.json')
    need(len(native_by_index)==len(native)==25 and all(r['status']=='SAT' for r in native),'native25 SAT outcomes')
    prior=load(REPO/'hadwiger_nelson_heule514_profile_pilot/certificate.json');prefix=[]
    for i,r in enumerate(prior):
        need(raw_witnesses[i]==dict(id=i,kind='inherited',source_index=r['index'],D=r['D'],colouring=r['colouring']),'initial trace witnesses');prefix.append(raw_witnesses[i])
    F=module('independent_projected_formula',REPO/'hadwiger_nelson_heule514_profile_pilot/verify.py')
    kernel=load(REPO/'hadwiger_nelson_heule514_path_projection/certificate.json')
    records=[json.loads(l) for l in (run/'records.jsonl').read_text().splitlines()]
    need(len(records)==8974,'complete chronological trace')
    native_count=clause_checks=raw_edges=restorations=0;counts=Counter()
    for i,(O,record) in enumerate(zip(candidates,records)):
        need(record['index']==i,'trace row order');Oset=set(O)
        eligible=next((r['id'] for r in prefix if not set(r['D']).difference(Oset)),None)
        if eligible is not None:
            need(record==dict(index=i,status='COVERED',witness=eligible),'first eligible chronological witness')
        else:
            need(record['status']=='SAT' and i in native_by_index,'native row necessity')
            row=native_by_index[i];wid=record['witness'];need(wid==len(prefix)==row['witness'],'native witness order')
            witness=raw_witnesses[wid];need(witness['id']==wid and witness['kind']=='native' and witness['source_index']==i,'native provenance')
            clauses,formula,nb=F.formula(edges,Oset,kernel)
            need(formula==(run/f'{i:04d}.cnf').read_bytes() and sha256(formula).hexdigest()==row['cnf_sha256'],'independent formula bytes')
            answer_raw=(run/f'{i:04d}.model.json').read_bytes();need(sha256(answer_raw).hexdigest()==row['model_file_sha256'],'native answer hash')
            answer=json.loads(answer_raw);model=answer['model']
            need(answer['status']=='SAT' and len(model)==2052 and {abs(x) for x in model}==set(range(1,2053)),'native Boolean domain')
            truth={x for x in model if x>0}
            for cl in clauses:need(any(x in truth if x>0 else -x not in truth for x in cl),'model clause');clause_checks+=1
            c=['.']*514
            for v in range(510):
                if v not in Oset:c[v]=str(next(k for k in range(4) if 4*v+k+1 in truth))
            selected=[j for j in range(4) if 510+j not in Oset];extension=None
            for values in product('123',repeat=len(selected)):
                trial=c.copy()
                for j,x in zip(selected,values):trial[510+j]=x
                if all(trial[u]=='.' or trial[v]=='.' or trial[u]!=trial[v] for u,v in edges if v>=510):extension=trial;break
            need(extension is not None and ''.join(extension)==witness['candidate_colouring'],'independent path reconstruction')
            raw_edges+=check_colour(extension,O,edges)
            for v,x in witness['fills']:
                need(v in Oset and extension[v]=='.' and x in '0123','restoration domain');extension[v]=x;restorations+=1
            need(''.join(extension)==witness['colouring'],'restored colour bytes')
            raw_edges+=check_colour(extension,witness['D'],edges)
            need(row['final_omissions']==witness['D'],'native omission record')
            prefix.append(witness);native_count+=1
        counts[record['status']]+=1
    need(native_count==25 and len(prefix)==len(raw_witnesses)==40,'complete native archive')
    for row in cert:
        source=next(r for r in prefix if r['kind']=='native' and r['source_index']==row['source_index'])
        need(row['D']==source['D'] and row['colouring']==source['colouring'],'public witness provenance')
    stable=['index','omitted','variables','clauses','cnf_sha256','cnf_bytes','status','final_omissions']
    need([{k:r[k] for k in stable} for r in native]==[{k:r[k] for k in stable} for r in load(HERE/'cases.json')],'public mathematical case records')
    return dict(input_rows=8974,full_core_colourings_checked=8974,full_core_edge_checks=edge_checks,
                chronological_rows_checked=len(records),status_counts=dict(counts),native_models_checked=native_count,
                independently_rebuilt_formulas=native_count,Boolean_clause_checks=clause_checks,
                raw_candidate_restored_edge_checks=raw_edges,restoration_steps=restorations,
                coverage_sha256=sha256(tags).hexdigest(),native_solver_called=False)


def verify(out,frontier=None,run=None):
    start=time.monotonic();out.mkdir(exist_ok=True)
    edges,rows,positive_checks,boundary_checks=public_inputs()
    direct=direct_closure(edges,rows,out)
    rejected=0
    for c,D in [(rows[0]['colouring'][:-1],rows[0]['D']),('x'+rows[0]['colouring'][1:],rows[0]['D'])]:
        try:check_colour(c,D,edges)
        except ValueError:rejected+=1
        else:raise ValueError('invalid colouring accepted')
    c=list(rows[0]['colouring']);u,v=next((u,v) for u,v in edges if c[u]!='.' and c[v]!='.');c[v]=c[u]
    try:check_colour(c,rows[0]['D'],edges)
    except ValueError:rejected+=1
    else:raise ValueError('monochromatic edge accepted')
    report=dict(status='EVERY H514 SUBGRAPH ON AT MOST508 VERTICES IS FOUR-COLOURABLE',family_closed=True,record_improvement=False,
                vertices=514,unit_edges=len(edges),exact_coordinate_pairs=131841,
                positive_witnesses_checked=len(rows),positive_edge_checks=positive_checks,boundary_witness_edge_checks=boundary_checks,
                direct_whole_support=direct,malformed_colourings_rejected=rejected,
                residual_census_required_for_direct_proof=False,solver_used=False,seconds=time.monotonic()-start)
    if frontier is not None or run is not None:
        need(frontier is not None and run is not None,'both archive inputs required')
        report['historical_run_audit']=audit_run(frontier,run,edges,out);report['seconds_with_historical_audit']=time.monotonic()-start
    save(out/'verification.json',report);print(json.dumps(report,sort_keys=True))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--frontier',type=Path);p.add_argument('--run',type=Path);a=p.parse_args();verify(a.out,a.frontier,a.run)
