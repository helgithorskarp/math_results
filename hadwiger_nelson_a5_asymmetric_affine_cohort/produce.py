#!/usr/bin/env python3
"""Restartable exact Groebner producer; no numerical root selection."""
import argparse
import json
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import model as M


def solve(pair):
    _,polys=M.load_cohort()
    return list(pair),M.charts(pair,polys,'groebner')


def colour(n,edges,triangle,k):
    from pysat.solvers import Solver
    var=lambda v,c:k*v+c+1
    cnf=[[var(v,c) for c in range(k)] for v in range(n)]
    cnf += [[-var(v,a),-var(v,b)] for v in range(n) for a in range(k) for b in range(a)]
    cnf += [[-var(a,c),-var(b,c)] for a,b in edges for c in range(k)]
    cnf += [[var(v,c)] for c,v in enumerate(triangle)]
    with Solver(name='cadical195',bootstrap_with=cnf) as solver:
        if not solver.solve(): return None
        positive={x for x in solver.get_model() if x>0}
    word=[next(c for c in range(k) if var(v,c) in positive) for v in range(n)]
    M.check_colour(word,n,edges,k)
    return word


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--scratch',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True);parser.add_argument('--workers',type=int,default=2);parser.add_argument('--full-out',type=Path)
    args=parser.parse_args();args.scratch.mkdir(exist_ok=True,parents=True)
    data,polys=M.load_cohort();start=time.monotonic()
    pending=[pair for pair in data['pairs'] if not (args.scratch/('%d_%d.json'%tuple(pair))).exists()]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for pair,cc in pool.map(solve,pending):
            dest=args.scratch/('%d_%d.json'%tuple(pair));tmp=dest.with_suffix('.tmp')
            tmp.write_text(json.dumps({'pair':pair,'charts':cc},sort_keys=True)+'\n');tmp.replace(dest)
            print('ROOTS',pair,len(cc),sum(c['real_embeddings'] for c in cc),round(time.monotonic()-start,2),flush=True)
    components={};pairs=[];sources={}
    for pair in data['pairs']:
        record=json.loads((args.scratch/('%d_%d.json'%tuple(pair))).read_text())
        M.need(record['pair']==pair,'cached pair identity')
        ids=[]
        for c in record['charts']:
            key=M.digest(c);components[key]=c;sources.setdefault(key,[]).append(pair);ids.append(key)
        pairs.append({'pair':pair,'charts':sorted(ids)})
    # Producer builds event-owned edges; verifier independently tests all pairs.
    _,_,factors,owners,base,*_=M.A.architecture.build()
    records=[]
    for i,key in enumerate(sorted(components)):
        c=components[key];ev=M.A.evaluator(c)
        active=[j for j,f in enumerate(factors) if ev(f)]
        points,labels=M.physical.coordinates(c)
        edges=sorted({tuple(sorted((labels[a],labels[b]))) for a,b in base+[e for j in active for e in owners[j]]})
        edges=[list(e) for e in edges];M.need(all(a!=b for a,b in edges),'no unit loop')
        triangle=[labels[j] for j in (0,81,162)]
        word=colour(len(points),edges,triangle,3);k=3
        if word is None:word=colour(len(points),edges,triangle,4);k=4
        if word is None:
            signal=dict(chart=c,points=M.point_stream(points),labels=labels,edges=edges)
            (args.scratch/'NONFOUR_SIGNAL.json').write_text(json.dumps(signal)+'\n')
            raise RuntimeError('Ordinary non-four signal: freeze and certify before continuing.')
        records.append(dict(c,key=key,source_pairs=sources[key],root_intervals=M.root_intervals(c),
                            point_count=len(points),edge_count=len(edges),point_sha256=M.digest(M.point_stream(points)),
                            label_map_sha256=M.digest(labels),edge_sha256=M.digest(edges),colour_count=k,colour_word=word))
        print('GRAPH',i+1,len(components),len(points),len(edges),k,round(time.monotonic()-start,2),flush=True)
    out={'schema':'hn-a5-affine-cohort-physical-v1','cohort_sha256':M.digest(data),'pairs':pairs,'components':records}
    if args.full_out:args.full_out.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    out['schema']='hn-a5-affine-cohort-physical-v2'
    for c in out['components']:
        del c['x'];del c['y']
    args.out.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print('COMPLETE',len(records),sum(c['real_embeddings'] for c in records),round(time.monotonic()-start,3),flush=True)


if __name__=='__main__':main()
