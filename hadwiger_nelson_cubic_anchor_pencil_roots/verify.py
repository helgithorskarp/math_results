#!/usr/bin/env python3
"""Resultant/fiber coverage, all active events, and direct physical unit graphs.

No producer, event-edge-owner table, SAT solver, or numerical tolerance is used
for physical graph verification. The two algebraic routes share norm inputs and
canonical field encodings, not elimination algorithms.
"""
import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
from pathlib import Path
from interface import A,HERE,physical,build,selection,pair_interface,colour_word
import roots


def root_task(pair_factors):
    x,y,s=A.sp.symbols('x y s')
    return roots.resultant(*pair_factors,x,y,s)


def check_pair_record(pair,components,claimed):
    expected={'pair':list(pair),'components':sorted(A.digest(c) for c in components)}
    A.need(claimed==expected,'complete pair-component coverage')


def coverage(pairs,factors,certificate,jobs):
    A.need(len(certificate['pairs'])==len(pairs),'number of anchor pairs')
    fields={}
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        out=pool.map(root_task,((factors[a],factors[b]) for a,b in pairs),chunksize=1)
        for pair,cc,claimed in zip(pairs,out,certificate['pairs']):
            check_pair_record(pair,cc,claimed)
            for c in cc:fields[A.digest(c)]=c
    records={c['key']:c for c in certificate['components']}
    A.need(len(records)==len(certificate['components']) and set(records)==set(fields),'complete distinct fields')
    for key,c in fields.items():
        A.need(all(records[key][k]==v for k,v in c.items()),'exact component coordinates')
    return fields,records


def concurrency(selected,incidence,records):
    bypair={tuple(r['pair']):r['components'] for r in incidence};transcript=[]
    for idx,domains,pairs in selected:
        for pair in pairs:
            for key in bypair[pair]:
                active=set(records[key]['active_curves'])
                sections=[[i for i in d if i in active] for d in domains]
                A.need(not all(sections),'full five-section complex concurrence')
                transcript.append([idx,list(pair),key,sections])
    return len(transcript),A.digest(transcript)


FACTORS=None

def initialize(factors):
    global FACTORS
    FACTORS=factors


def check_field(c):
    field={k:c[k] for k in ('q','x','y')};key=A.digest(field)
    A.need(c['key']==key,'component key')
    nr=roots.nreal(field);A.need(c['real_embeddings']==nr,'real embedding count')
    # These canonical shapes make distinct component records disjoint in (x,y).
    deg=len(c['q'])-1
    A.need((deg==1 and c['q']==['0','1'] and len(c['x'])==len(c['y'])==1) or
           (deg>1 and (c['x']==['0','1'] or (len(c['x'])==1 and c['y']==['0','1']))),'canonical separating coordinate')
    ev=A.evaluator(field);active=[i for i,f in enumerate(FACTORS) if ev(f)]
    A.need(c['active_curves']==active,'all active norm events')
    if not nr:return {'key':key,'nreal':0,'degree':deg,'active':len(active)}
    points,labels,edges,triangle=physical.graph(field)
    A.need(c['point_count']==len(points) and c['edge_count']==len(edges),'physical graph counts')
    A.need(c['edge_sha256']==A.digest(edges),'complete direct physical unit edges')
    A.need(c['label_map_sha256']==A.digest(labels),'complete physical collision quotient')
    word=colour_word(c['colour_weights'],labels,len(points))
    physical.check_word(word,len(points),edges)
    circle=((c['point_count']<243))
    if circle:
        # Every exceptional component lies on |z|=1 and |1 +/- z^3|=1.
        A.need(ev(((0,0,-1),(2,0,1),(0,2,3))),'exceptional unit-circle parameter')
        A.need(len(active)==101 and len(points) in (108,147),'exceptional incidence/physical size')
    else:A.need(len(active)==2 and len(points)==243,'nonexceptional exactly-two-event injective graph')
    return {'key':key,'nreal':nr,'degree':deg,'active':len(active),'vertices':len(points),'edges':len(edges),'weights':c['colour_weights']}


def verify(residual,certificate_path,jobs):
    certificate=json.loads(Path(certificate_path).read_text())
    A.need(certificate['schema']=='hn-cubic-anchor-pencils-v1','schema')
    factors,_,_,buckets,_=build();pencils=selection(buckets,residual);selected,pairs=pair_interface(pencils,buckets)
    A.need(certificate['source_residual_sha256']==A.RESIDUAL_HASH and certificate['curve_inventory_sha256']==A.digest(factors),'source hashes')
    A.need(certificate['pencil_interface_sha256']==A.digest([[i,p] for i,p in pencils]),'pencil interface')
    fields,records=coverage(pairs,factors,certificate,jobs)
    with ProcessPoolExecutor(max_workers=jobs,initializer=initialize,initargs=(factors,)) as pool:
        results=list(pool.map(check_field,[records[k] for k in sorted(records)],chunksize=1))
    ninc,transcript=concurrency(selected,certificate['pairs'],records)
    graph_hist=Counter();degree_hist=Counter();active_hist=Counter();weight_hist=Counter()
    for c in results:
        n=c['nreal']
        if n:
            graph_hist[f"{c['vertices']}v_{c['edges']}e"]+=n
            degree_hist[str(c['degree'])]+=n;active_hist[str(c['active'])]+=n
            weight_hist[''.join(map(str,c['weights']))]+=n
    return {'status':'PASS','pencils':len(pencils),'raw_lifts':1024000,'anchor_pairs':len(pairs),'distinct_complex_components':len(fields),
            'components_with_pair_incidence':sum(len(r['components']) for r in certificate['pairs']),
            'components_with_pencil_pair_incidence':ninc,'complex_concurrences':0,'real_components':sum(c['nreal']>0 for c in results),
            'distinct_real_parameters':sum(c['nreal'] for c in results),'all_physical_chromatic_numbers':3,
            'physical_graph_histogram_by_parameter':dict(sorted(graph_hist.items())),
            'active_curve_histogram_by_parameter':dict(sorted(active_hist.items())),
            'degree_histogram_by_parameter':dict(sorted(degree_hist.items())),
            'linear_colour_weight_histogram_by_parameter':dict(sorted(weight_hist.items())),
            'concurrency_transcript_sha256':transcript,'physical_transcript_sha256':A.digest(results),
            'certificate_sha256':hashlib.sha256(Path(certificate_path).read_bytes()).hexdigest()}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--residual',type=Path);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--jobs',type=int,default=2);p.add_argument('--check-expected',action='store_true');args=p.parse_args()
    A.need(1<=args.jobs<=8,'bounded worker count');result=verify(args.residual,args.certificate,args.jobs)
    if args.check_expected:A.need(result==json.loads((HERE/'EXPECTED.json').read_text()),'expected complete result')
    print(json.dumps(result,sort_keys=True,indent=2))
