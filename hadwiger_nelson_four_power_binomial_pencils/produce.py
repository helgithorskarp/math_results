#!/usr/bin/env python3
"""Generate an exact certificate locally; large root output is not committed."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path
import time
from interface import A,physical,build,selection,pair_interface,linear_weights,colour_word
import roots


def root_task(args):
    left,right,method=args;x,y,s=A.sp.symbols('x y s')
    return getattr(roots,method)(left,right,x,y,s)


def solve(pairs,factors,method,jobs):
    fields={};incidence=[]
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        output=pool.map(root_task,((factors[a],factors[b],method) for a,b in pairs),chunksize=1)
        for (a,b),cc in zip(pairs,output):
            keys=[]
            for field in cc:
                ev=A.evaluator(field);A.need(ev(factors[a]) and ev(factors[b]),'anchor substitution')
                key=A.digest(field);fields[key]=field;keys.append(key)
            A.need(len(keys)==len(set(keys)),'distinct pair components')
            incidence.append({'pair':[a,b],'components':sorted(keys)})
    return fields,incidence


DATA=None

def initialize(data):
    global DATA
    DATA=data


def field_task(item):
    key,c=item;factors,owners,base,buckets,curve_rows=DATA
    ev=A.evaluator(c);active=[i for i,f in enumerate(factors) if ev(f)];nr=roots.nreal(c)
    rec=dict(c,key=key,active_curves=active,real_embeddings=nr)
    if nr:
        points,labels=physical.coordinates(c)
        edges=sorted({tuple(sorted((labels[a],labels[b]))) for a,b in base+[e for i in active for e in owners[i]]})
        A.need(all(a!=b for a,b in edges),'no collapsed unit loop')
        edges=[list(e) for e in edges]
        weights=linear_weights(active,curve_rows)
        word=colour_word(weights,labels,len(points));physical.check_word(word,len(points),edges)
        rec.update(point_count=len(points),edge_count=len(edges),edge_sha256=A.digest(edges),label_map_sha256=A.digest(labels),colour_weights=weights)
    return rec


def run(residual,method,jobs):
    data=build();factors,owners,base,buckets,curve_rows=data
    pencils=selection(buckets,residual);selected,pairs=pair_interface(pencils,buckets)
    fields,incidence=solve(pairs,factors,method,jobs)
    with ProcessPoolExecutor(max_workers=jobs,initializer=initialize,initargs=(data,)) as pool:
        records=list(pool.map(field_task,sorted(fields.items()),chunksize=1))
    return {'schema':'hn-four-power-binomial-pencils-v1','source_residual_sha256':A.RESIDUAL_HASH,'curve_inventory_sha256':A.digest(factors),
            'pencil_interface_sha256':A.digest([[idx,p] for idx,p in pencils]),'pairs':incidence,'components':records}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--residual',type=Path);p.add_argument('--method',choices=('resultant',),default='resultant');p.add_argument('--jobs',type=int,default=2);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    A.need(1<=args.jobs<=8,'bounded worker count');start=time.monotonic();result=run(args.residual,args.method,args.jobs)
    args.out.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'pairs':len(result['pairs']),'components':len(result['components']),'real_parameters':sum(c['real_embeddings'] for c in result['components']),'certificate_bytes':args.out.stat().st_size,'certificate_sha256':__import__('hashlib').sha256(args.out.read_bytes()).hexdigest(),'seconds':time.monotonic()-start},indent=2))
