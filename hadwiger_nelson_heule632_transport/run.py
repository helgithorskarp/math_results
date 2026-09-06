#!/usr/bin/env python3
"""Frozen 544-colouring simultaneous extension assessment for H632."""
import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import time
import oracle

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def module(name, path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def run(out, controls):
    start=time.monotonic();plan=json.loads((HERE/'plan.json').read_text())
    tests=json.loads(controls.read_text())
    oracle.require(tests['status']=='EXHAUSTIVE ORACLE CONTROLS PASSED' and tests['cases']==182667,'controls first')
    for path,digest in plan['input_files'].items():
        oracle.require(sha256((REPO/path).read_bytes()).hexdigest()==digest,('input identity',path))
    P=module('published_positive_inputs',REPO/'hadwiger_nelson_heule514_whole_decision/verify.py')
    h514,rows,old_checks,_=P.public_inputs()
    library=''.join(f'{w["group"]}:{w["index"]} '+w['colouring'][:510]+'\n' for w in rows).encode('ascii')
    oracle.require(len(rows)==544 and sha256(library).hexdigest()==plan['old_library_sha256'],'fixed old library')
    fresh=json.loads((REPO/'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json').read_text())
    structure=json.loads((REPO/'hadwiger_nelson_heule_fresh122_incidence/certificate.json').read_text())
    ids=structure['centre_ids'];edges=structure['fresh_edges'];components=structure['components'];cycle=structure['unique_cycle']
    oracle.require(ids==[r['centre_index'] for r in fresh] and len(ids)==122 and len(components)==66,'fixed components')
    neighbors={r['centre_index']:r['neighbors'] for r in fresh}
    adjacency=oracle.graph(ids,edges)
    packets=[]
    for comp in components:
        selected=comp['centres'];cs=set(selected)
        packets.append((selected,{v:adjacency[v] for v in selected},cycle if set(cycle)<=cs else ()))
    old_edges=[(u,v) for u,v in h514 if v<510]
    pos={v:510+i for i,v in enumerate(ids)}
    full_edges=old_edges+[(u,pos[v]) for v in ids for u in neighbors[v]]+[(pos[u],pos[v]) for u,v in edges]
    oracle.require(len(full_edges)==3112,'complete assembled H632 graph')
    out.mkdir(parents=True,exist_ok=True)
    cases=[];positive=[];table=[];component_pass=[0]*66
    failures=Counter();empty_counts=Counter();old_sizes=Counter();edge_checks=0
    with (out/'lists.txt').open('w') as stream:
        for i,row in enumerate(rows):
            c=row['colouring'][:510];D=[v for v,x in enumerate(c) if x=='.'];old_sizes[len(D)]+=1
            masks={v:15 for v in ids}
            for v in ids:
                for u in neighbors[v]:
                    if c[u]!='.':masks[v]&=~(1<<int(c[u]))
            stream.write(''.join(format(masks[v],'x') for v in ids)+'\n')
            empty=[v for v in ids if not masks[v]];empty_counts[len(empty)]+=1
            answer={};bits=0;failed=[]
            for j,(selected,graph,loop) in enumerate(packets):
                lists={v:masks[v] for v in selected}
                colouring=oracle.extend(graph,lists,loop)
                if colouring is None:
                    failed.append(j)
                    failures['empty_list' if any(masks[v]==0 for v in selected) else 'coupled_lists']+=1
                else:
                    oracle.check_answer(graph,lists,colouring)
                    answer.update(colouring);bits|=1<<j;component_pass[j]+=1
            tag=f'{row["group"]}:{row["index"]}'
            table.append(f'{i}\t{tag}\t'+','.join(map(str,D))+f'\t{bits:017x}\n')
            cases.append({'index':i,'tag':tag,'old_omissions':D,'failed_components':failed,'empty_centres':empty})
            if not failed:
                tail=''.join(str(answer[v]) for v in ids);full=c+tail
                for u,v in full_edges:
                    if full[u]!='.' and full[v]!='.':
                        oracle.require(full[u]!=full[v],'full H632 positive edge');edge_checks+=1
                positive.append({'index':i,'tag':tag,'old_omissions':D,'fresh_colouring':tail})
    table_raw=''.join(table).encode('ascii');(out/'cases.tsv').write_bytes(table_raw)
    (out/'cases_detailed.json').write_text(json.dumps(cases,separators=(',',':'))+'\n')
    (out/'positive.json').write_text(json.dumps(positive,indent=2,sort_keys=True)+'\n')
    forced=sorted({r['old_omissions'][0] for r in positive if len(r['old_omissions'])==1})
    result={'status':'COMPLETE FIXED-LIBRARY H632 TRANSPORT','old_rows':544,'component_tests':544*66,
            'full_extensions':len(positive),'failed_extensions':544-len(positive),'valid_old_singleton_cuts':forced,
            'component_success_counts':component_pass,'component_failures_by_reason':dict(sorted(failures.items())),
            'empty_centres_per_row_histogram':{str(k):v for k,v in sorted(empty_counts.items())},
            'old_omission_histogram':{str(k):v for k,v in sorted(old_sizes.items())},
            'full_support_edge_count':len(full_edges),'full_positive_edge_checks':edge_checks,
            'cases_sha256':sha256(table_raw).hexdigest(),'old_library_sha256':sha256(library).hexdigest(),
            'lists_sha256':sha256((out/'lists.txt').read_bytes()).hexdigest(),
            'family_closed_through508':len(forced)>=509,'native_solver_calls':0,'record_improvement':False,
            'decision':'FAMILY CLOSED' if len(forced)>=509 else 'NO-GO for this fixed-library transport' if not positive else 'INCOMPLETE: checkpoint without adaptive refinement'}
    (out/'result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (out/'runtime.json').write_text(json.dumps({'seconds':time.monotonic()-start,'inherited_H514_positive_edge_checks':old_checks},indent=2)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--controls',type=Path,required=True)
    a=ap.parse_args();run(a.out,a.controls)
