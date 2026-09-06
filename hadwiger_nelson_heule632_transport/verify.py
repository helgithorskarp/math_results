#!/usr/bin/env python3
"""Independent library decoding, exact geometry and component decisions.

Imports no producing run/oracle. Positive recipes use the independent
reviewer's raw decoder. Geometry uses the prior sparse integer norm checker.
"""
import argparse
from collections import Counter
from contextlib import redirect_stdout
from hashlib import sha256
import importlib.util
from itertools import combinations
import io
import json
from pathlib import Path
import time
import independent

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


def verify(out,run=None):
    start=time.monotonic();out.mkdir(parents=True,exist_ok=True)
    plan=json.loads((HERE/'plan.json').read_text())
    for path,digest in plan['input_files'].items():
        independent.check(sha256((REPO/path).read_bytes()).hexdigest()==digest,('input identity',path))
    G=module('sparse_geometry',REPO/'hadwiger_nelson_heule_fresh122_incidence/verify.py')
    with redirect_stdout(io.StringIO()):G.audit(out/'geometry')
    old=json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json').read_text())
    labels=[v for v in range(553) if '510' in old['provenance'][v]]
    points=[G.scaled(G.rational(old['coordinates'][str(v)]),96) for v in labels]
    large={i for i,p in enumerate(points) if all(all(r%5 for r in a) for a in p)}
    old_edges=[(u,v) for u,v in combinations(range(510),2) if G.squared_distance(points[u],points[v])==(9216,0,0,0,0,0,0,0)]
    independent.check(len(old_edges)==2504,'old unit edges')
    fresh=json.loads((REPO/'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json').read_text())
    structure=json.loads((REPO/'hadwiger_nelson_heule_fresh122_incidence/certificate.json').read_text())
    ids=structure['centre_ids'];cycle=structure['unique_cycle'];edges=structure['fresh_edges'];components=structure['components']
    neighbors={r['centre_index']:r['neighbors'] for r in fresh}
    small=[170,436,1239,1527];tail_index={v:510+i for i,v in enumerate(small)}
    h514=old_edges+[(u,tail_index[v]) for v in small for u in neighbors[v]]+[(tail_index[u],tail_index[v]) for u,v in edges if u in tail_index and v in tail_index]
    R=module('reviewed_raw_decoder',REPO/'hadwiger_nelson_heule514_whole_decision_review1/independent_check.py')
    rows,inherited_checks=R.load_positive_library(REPO,h514,old,labels,large)
    library=''.join(f'{w["group"]}:{w["index"]} '+w['colouring'][:510]+'\n' for w in rows).encode('ascii')
    independent.check(sha256(library).hexdigest()==plan['old_library_sha256'],'independent old library bytes')
    packets=[]
    for comp in components:
        cs=set(comp['centres']);packets.append((comp['centres'],[(u,v) for u,v in edges if u in cs],cycle if set(cycle)<=cs else ()))
    expected_lines=[];list_lines=[];counts=[0]*66;failures=Counter();empty_counts=Counter();old_sizes=Counter();full_rows=[]
    own_positive_checks=0;nonempty_failures=[]
    for i,row in enumerate(rows):
        c=row['colouring'][:510];D=[v for v,x in enumerate(c) if x=='.'];old_sizes[len(D)]+=1
        masks={v:sum(1<<k for k in range(4) if str(k) not in {c[u] for u in neighbors[v] if c[u]!='.'}) for v in ids}
        list_lines.append(''.join(format(masks[v],'x') for v in ids)+'\n');empty_counts[sum(m==0 for m in masks.values())]+=1
        bits=0;full={}
        for j,(vertices,es,cyc) in enumerate(packets):
            selected={v:masks[v] for v in vertices};a=independent.solve(vertices,es,selected,cyc)
            if a is None:failures['empty_list' if 0 in selected.values() else 'coupled_lists']+=1
            else:bits|=1<<j;counts[j]+=1;full.update(a)
        tag=f'{row["group"]}:{row["index"]}'
        expected_lines.append(f'{i}\t{tag}\t'+','.join(map(str,D))+f'\t{bits:017x}\n')
        if bits!=(1<<66)-1 and all(masks.values()):
            nonempty_failures.append({'index':i,'tag':tag,'failed_components':[j for j in range(66) if not bits&(1<<j)]})
        if i==462:
            independent.check(D==[486] and all(masks.values()) and masks[809]==masks[1041]==2 and [809,1041] in edges,'explicit forced-equal edge example')
        if len(full)==122:
            full_rows.append(i)
            for v in ids:
                for u in neighbors[v]:
                    if c[u]!='.':independent.check(str(full[v])!=c[u],'independent old-new edge');own_positive_checks+=1
            for u,v in edges:independent.check(full[u]!=full[v],'independent fresh edge');own_positive_checks+=1
    table=''.join(expected_lines).encode('ascii');lists=''.join(list_lines).encode('ascii')
    independent.check(table==(HERE/'cases.tsv').read_bytes(),'all35904 component results entrywise')
    public=json.loads((HERE/'positive.json').read_text());independent.check([r['index'] for r in public]==full_rows,'exact full-extension set')
    public_checks=0
    for record in public:
        i=record['index'];row=rows[i];c=row['colouring'][:510];D=[v for v,x in enumerate(c) if x=='.'];tail=record['fresh_colouring']
        independent.check(record['old_omissions']==D and record['tag']==f'{row["group"]}:{row["index"]}','positive provenance')
        independent.check(len(tail)==122 and set(tail)<=set('0123'),'fresh colour domain');answer=dict(zip(ids,tail))
        for u,v in old_edges:
            if c[u]!='.' and c[v]!='.':independent.check(c[u]!=c[v],'positive old edge');public_checks+=1
        for v in ids:
            for u in neighbors[v]:
                if c[u]!='.':independent.check(answer[v]!=c[u],'positive attachment');public_checks+=1
        for u,v in edges:independent.check(answer[u]!=answer[v],'positive fresh edge');public_checks+=1
    forced=sorted({r['old_omissions'][0] for r in public if len(r['old_omissions'])==1})
    result={'status':'COMPLETE FIXED-LIBRARY H632 TRANSPORT','old_rows':544,'component_tests':35904,
            'full_extensions':len(public),'failed_extensions':544-len(public),'valid_old_singleton_cuts':forced,
            'component_success_counts':counts,'component_failures_by_reason':dict(sorted(failures.items())),
            'empty_centres_per_row_histogram':{str(k):v for k,v in sorted(empty_counts.items())},
            'old_omission_histogram':{str(k):v for k,v in sorted(old_sizes.items())},
            'full_support_edge_count':3112,'full_positive_edge_checks':public_checks,
            'cases_sha256':sha256(table).hexdigest(),'old_library_sha256':sha256(library).hexdigest(),
            'lists_sha256':sha256(lists).hexdigest(),'family_closed_through508':len(forced)>=509,
            'native_solver_calls':0,'record_improvement':False,
            'decision':'FAMILY CLOSED' if len(forced)>=509 else 'NO-GO for this fixed-library transport' if not public else 'INCOMPLETE: checkpoint without adaptive refinement'}
    independent.check(result==json.loads((HERE/'result.json').read_text()),'full mathematical summary')
    if run is not None:
        independent.check(table==(run/'cases.tsv').read_bytes() and lists==(run/'lists.txt').read_bytes(),'raw per-entry streams')
    report={'status':'VERIFIED ALL544 WHOLE-SUPPORT TRANSPORT DECISIONS','exact_coordinate_pairs':199396,
            'component_decisions_compared_entrywise':35904,'old_library_sha256':sha256(library).hexdigest(),
            'inherited_H514_positive_edge_checks':inherited_checks,'full_extensions':len(public),
            'independent_positive_attachment_checks':own_positive_checks,'public_positive_edge_checks':public_checks,
            'cases_sha256':sha256(table).hexdigest(),'lists_sha256':sha256(lists).hexdigest(),
            'nonempty_list_failed_rows':nonempty_failures,
            'raw_streams_compared':run is not None,'native_solver_calls':0,'record_improvement':False,
            'independent_author_review_claimed':False,'seconds':time.monotonic()-start}
    (out/'verification.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--run',type=Path)
    a=ap.parse_args();verify(a.out,a.run)
