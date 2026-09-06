"""Complete arc consistency for one pinned finite-host homomorphism family."""
import argparse
from collections import Counter, deque
import hashlib
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
sys.path.insert(0,str(REPO/'hadwiger_nelson_heule632_pair_pilot'))
import build as B


def need(ok,why):
    if not ok:raise ValueError(why)


def bits(mask):
    while mask:
        low=mask&-mask;yield low.bit_length()-1;mask-=low


def prepare():
    plan=json.loads((HERE/'plan.json').read_text())
    for name,digest in plan['input_files'].items():
        need(hashlib.sha256((REPO/name).read_bytes()).hexdigest()==digest,('input identity',name))
    points,edges,large=B.geometry()
    old=json.loads((REPO/'hadwiger_nelson_heule560_global_decision/certificate.json').read_text())
    boundary=json.loads((REPO/'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    index=plan['source_core_index'];need(index==old['minimality_evidence_core_index'],'critical source index')
    mask=old['negative_cores'][index]['mask']
    source=set(boundary['mandatory_vertices'])|{v for i,v in enumerate(old['optional_order']) if mask>>i&1}
    pins=source&large
    need(len(source)==516 and len(pins)==375,'source and fixed block')
    target=[0]*632;adj={v:[] for v in source};source_edges=[]
    for u,v in edges:
        target[u]|=1<<v;target[v]|=1<<u
        if u in source and v in source:adj[u].append(v);adj[v].append(u);source_edges.append((u,v))
    return plan,sorted(source),sorted(pins),target,adj,source_edges


def propagate(source,pins,target,adj):
    domains={v:(1<<v if v in pins else (1<<len(target))-1) for v in source}
    queue=deque((v,w) for v in source for w in adj[v]);queued=set(queue)
    cache={};revisions=0;changes=0;removed=0
    while queue:
        v,w=queue.popleft();queued.remove((v,w));revisions+=1
        key=domains[w]
        if key not in cache:
            possible=0
            for x in bits(key):possible|=target[x]
            cache[key]=possible
        new=domains[v]&cache[key]
        if new==domains[v]:continue
        changes+=1;removed+=(domains[v]^new).bit_count();domains[v]=new
        for u in adj[v]:
            if (u,v) not in queued:queue.append((u,v));queued.add((u,v))
    return domains,{'arc_revisions':revisions,'strict_domain_revisions':changes,'removed_values':removed,'cached_neighbour_unions':len(cache)}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=False)
    start=time.monotonic();plan,source,pins,target,adj,es=prepare();prepared=time.monotonic()
    domains,stats=propagate(source,set(pins),target,adj)
    need(all(domains[v]>>v&1 for v in source),'identity homomorphism retained')
    forced=sorted({next(bits(d)) for d in domains.values() if d.bit_count()==1})
    report={'source_vertices':len(source),'source_edges':len(es),'target_vertices':len(target),'target_edges':sum(x.bit_count() for x in target)//2,'pins':len(pins),'domain_histogram':dict(sorted(Counter(d.bit_count() for d in domains.values()).items())),
            'remaining_mapping_values':sum(d.bit_count() for d in domains.values()),'forced_distinct_images':len(forced),'identity_only':all(domains[v]==1<<v for v in source),
            'at_most508_family_closed_by_domains':len(forced)>plan['image_budget'],'record_improvement':False,'native_queries':0,
            'preparation_seconds':prepared-start,'propagation_seconds':time.monotonic()-prepared,**stats}
    cert={'source_vertices':source,'pinned_vertices':pins,'unpinned_domains':{str(v):list(bits(domains[v])) for v in source if v not in pins},'forced_target_vertices':forced}
    for name,data in [('result.json',report),('certificate.json',cert)]:
        (args.out/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':main()
