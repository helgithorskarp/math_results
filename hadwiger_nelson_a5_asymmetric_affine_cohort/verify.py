#!/usr/bin/env python3
"""Resultant/quotient-gcd coverage; direct all-pairs physical graph checker."""
import argparse
from collections import Counter,defaultdict
from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path
import time
import model as M


def check_physical(c):
    M.need(c['colour_count'] in (3,4),'ordinary four-colour upper bound required')
    M.need(c['root_intervals']==M.root_intervals(c),'exact real root isolation')
    points,labels,edges,triangle=M.physical.graph(c)
    M.need((len(points),len(edges))==(c['point_count'],c['edge_count']),'complete physical graph size')
    M.need(M.digest(M.point_stream(points))==c['point_sha256'],'exact physical coordinate stream')
    M.need(M.digest(labels)==c['label_map_sha256'],'collision quotient')
    M.need(M.digest(edges)==c['edge_sha256'],'complete all-pairs unit graph')
    M.check_colour(c['colour_word'],len(points),edges,c['colour_count'])
    return points,labels,edges


def physical_job(task):
    c,export=task
    points,labels,edges=check_physical(c)
    if export:
        out={'chart':{k:c[k] for k in ('q','x','y','real_embeddings')},'isolating_intervals':c['root_intervals'],
             'points':M.point_stream(points),'labels':labels,'edges':edges,'colour_word':c['colour_word']}
        (export/(c['key']+'.json')).write_text(json.dumps(out,sort_keys=True)+'\n')
    return c['key'],len(points),len(edges)


def coverage_job(pair):
    _,polys=M.load_cohort()
    return pair,M.charts(pair,polys,'resultant')


def verify(certificate,export=None,progress=False,workers=1):
    data,polys=M.load_cohort();cert=json.loads(Path(certificate).read_text())
    M.need(cert['schema']=='hn-a5-affine-cohort-physical-v2' and cert['cohort_sha256']==M.digest(data),'schema and cohort')
    charts={};sources=defaultdict(list);pairs=[];start=time.monotonic()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for pair,cc in pool.map(coverage_job,data['pairs']):
            ids=[]
            for c in cc:
                key=M.digest(c);charts[key]=c;sources[key].append(pair);ids.append(key)
            pairs.append({'pair':pair,'charts':sorted(ids)})
            if progress:print('COVER',pair,len(cc),round(time.monotonic()-start,2),flush=True)
    M.need(cert['pairs']==pairs,'complete real root cover')
    records={c['key']:c for c in cert['components']}
    M.need(len(records)==len(cert['components']) and set(records)==set(charts),'complete component list')
    hist=Counter();colours=Counter();degrees=Counter();real=0
    if export:export.mkdir(parents=True,exist_ok=True)
    for key in sorted(charts):
        c=records[key];expected=charts[key]
        M.need(all(c[k]==expected[k] for k in ('q','real_embeddings')),'exact chart identity')
        M.need('x' not in c and 'y' not in c,'coordinate charts must be reconstructed')
        records[key]=dict(c,x=expected['x'],y=expected['y'])
        M.need(c['source_pairs']==sources[key],'source pair cover')
    tasks=[(records[key],export) for key in sorted(charts)]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for i,(key,n,e) in enumerate(pool.map(physical_job,tasks)):
            c=records[key];nr=c['real_embeddings'];real+=nr;hist[f'{n}v_{e}e']+=nr
            colours[str(c['colour_count'])]+=nr;degrees[str(len(c['q'])-1)]+=nr
            if progress:print('PHYSICAL',i+1,len(charts),round(time.monotonic()-start,2),flush=True)
    return {'status':'PASS','pair_count':len(pairs),'component_count':len(charts),'distinct_real_parameters':real,
            'physical_graph_histogram_by_parameter':dict(sorted(hist.items())),
            'checked_colour_bounds_by_parameter':dict(sorted(colours.items())),
            'field_degrees_by_parameter':dict(sorted(degrees.items(),key=lambda x:int(x[0]))),
            'all_chromatic_numbers':3 if set(colours)=={'3'} else None,'every_graph_contains_triangle':True,'all_four_colourable':True,'record_candidate':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--certificate',type=Path,default=M.HERE/'certificate.json')
    parser.add_argument('--export',type=Path);parser.add_argument('--progress',action='store_true');parser.add_argument('--check-expected',action='store_true')
    parser.add_argument('--workers',type=int,default=1);parser.add_argument('--summary',type=Path);parser.add_argument('--metrics',type=Path)
    args=parser.parse_args();start=time.monotonic();r=verify(args.certificate,args.export,args.progress,args.workers)
    if args.check_expected:M.need(r==json.loads((M.HERE/'EXPECTED.json').read_text()),'expected summary')
    if args.summary:args.summary.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    if args.metrics:args.metrics.write_text(json.dumps({'elapsed_seconds':time.monotonic()-start,'workers':args.workers},indent=2)+'\n')
    print(json.dumps(r,sort_keys=True,indent=2))
