"""Independent synchronous domain proof using sparse-radical geometry."""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
sys.path.insert(0,str(REPO/'hadwiger_nelson_heule632_pair_pilot'))
import independent as I


def need(ok,why):
    if not ok:raise ValueError(why)


def fixed_point(source_adj,target_adj,pins):
    universe=set(target_adj)
    domains={v:({pins[v]} if v in pins else set(universe)) for v in source_adj}
    rounds=[]
    while True:
        # All tests in a round use the preceding round's domains. A candidate
        # needs a possible unit-edge image for every neighbour in the source.
        revised={v:{x for x in allowed if all(target_adj[x]&domains[w] for w in source_adj[v])}
                 for v,allowed in domains.items()}
        changes=sum(len(domains[v]-revised[v]) for v in domains)
        if changes==0:return domains,rounds
        rounds.append({'removed_values':changes,'remaining_values':sum(map(len,revised.values())),
                       'singleton_domains':sum(len(d)==1 for d in revised.values())})
        domains=revised


def geometry_and_source():
    plan=json.loads((HERE/'plan.json').read_text())
    for name,digest in plan['input_files'].items():
        need(hashlib.sha256((REPO/name).read_bytes()).hexdigest()==digest,('input identity',name))
    points,edges,_=I.geometry()
    boundary=json.loads((REPO/'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    original=json.loads((REPO/'hadwiger_nelson_heule560_global_decision/certificate.json').read_text())
    index=original['minimality_evidence_core_index'];need(index==plan['source_core_index']==52,'certified source')
    mask=original['negative_cores'][index]['mask'];source=set(boundary['mandatory_vertices'])
    for i,v in enumerate(original['optional_order']):
        if (mask//(2**i))%2:source.add(v)
    pins={v:v for v in source if all(all(rad%5 for rad in axis) for axis in points[v])}
    need(len(source)==516 and len(pins)==375,'fixed family')
    target_adj={v:set() for v in range(632)}
    for u,v in edges:target_adj[u].add(v);target_adj[v].add(u)
    source_adj={v:target_adj[v]&source for v in sorted(source)}
    return points,edges,source,source_adj,target_adj,pins


def inspect(cert,source,source_adj,target_adj,pins,domains):
    need(cert['source_vertices']==sorted(source),'source labels')
    need(cert['pinned_vertices']==sorted(pins),'exact fixed block')
    expected={str(v):sorted(domains[v]) for v in source if v not in pins}
    need(cert['unpinned_domains']==expected,'all unpinned domains')
    forced=sorted({next(iter(d)) for d in domains.values() if len(d)==1})
    need(cert['forced_target_vertices']==forced,'distinct forced image vertices')
    need(all(domains[v]=={v} for v in source),'identity forced at every vertex')
    need(len(forced)==516>508,'image size obstruction')
    # Show the sole permitted assignment is actually an edge-preserving map.
    count=0
    for v in source:
        for w in source_adj[v]:
            need(w in target_adj[v] and v!=w,'identity unit edge')
            if v<w:count+=1
    return count


def small_controls():
    pairs=list(combinations(range(3),2));cases=0;maps_checked=0;false_negative=0
    for smask,tmask,pmask in product(range(8),repeat=3):
        src={v:set() for v in range(3)};tgt={v:set() for v in range(3)}
        for j,(u,v) in enumerate(pairs):
            if smask>>j&1:src[u].add(v);src[v].add(u)
            if tmask>>j&1:tgt[u].add(v);tgt[v].add(u)
        pins={v:v for v in range(3) if pmask>>v&1};ds,_=fixed_point(src,tgt,pins)
        valid=0
        for f in product(range(3),repeat=3):
            if any(f[v]!=v for v in pins):continue
            if not all(f[w] in tgt[f[v]] for v in src for w in src[v]):continue
            valid+=1;maps_checked+=1
            need(all(f[v] in ds[v] for v in src),'no genuine map lost')
        if not valid and all(ds.values()):false_negative+=1
        if any(not d for d in ds.values()):need(valid==0,'empty domain implies no map')
        # Directly check the fixed-point property after termination.
        need(all(all(tgt[x]&ds[w] for w in src[v]) for v in src for x in ds[v]),'stable local support')
        cases+=1
    # A nonempty arc-consistent system need not have a homomorphism.
    need(false_negative>0,'controls include stable but unsatisfiable systems')
    return {'exhaustive_small_graph_pin_cases':cases,'actual_small_homomorphisms_retained':maps_checked,
            'stable_nonempty_but_unsatisfiable_controls':false_negative}


def mutations(cert,source,source_adj,target_adj,pins,domains):
    variants=[]
    c=copy.deepcopy(cert);c['source_vertices'].pop();variants.append(c)
    c=copy.deepcopy(cert);c['pinned_vertices'].pop();variants.append(c)
    key=next(iter(cert['unpinned_domains']))
    c=copy.deepcopy(cert);c['unpinned_domains'][key]=[];variants.append(c)
    c=copy.deepcopy(cert);c['unpinned_domains'][key].append(next(v for v in target_adj if v!=int(key)));variants.append(c)
    c=copy.deepcopy(cert);c['forced_target_vertices'].pop();variants.append(c)
    for c in variants:
        try:inspect(c,source,source_adj,target_adj,pins,domains)
        except ValueError:continue
        raise ValueError('malformed certificate accepted')
    return len(variants)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False)
    started=time.monotonic();points,edges,source,source_adj,target_adj,pins=geometry_and_source()
    domains,rounds=fixed_point(source_adj,target_adj,pins)
    cert=json.loads((HERE/'certificate.json').read_text());checks=inspect(cert,source,source_adj,target_adj,pins,domains)
    controls=small_controls();rejected=mutations(cert,source,source_adj,target_adj,pins,domains)
    report={'source_vertices':len(source),'source_unit_edges':checks,'target_vertices':len(points),'target_unit_edges':len(edges),
            'exact_host_pairs':632*631//2,'pinned_vertices':len(pins),'unpinned_vertices':len(source)-len(pins),
            'synchronous_strict_rounds':len(rounds),'domain_histogram':dict(sorted(Counter(map(len,domains.values())).items())),
            'removed_domain_values':sum(r['removed_values'] for r in rounds),'all_516_vertex_images_fixed_to_identity':True,
            'distinct_forced_image_vertices':516,'pinned_homomorphism_count':1,'at_most508_pinned_homomorphisms':0,
            'every_host_subgraph_at_most508_four_colourable':False,'record_improvement':False,'native_solver_needed':False,
            'invalid_certificates_rejected':rejected,**controls}
    (args.out/'result.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    (args.out/'rounds.json').write_text(json.dumps(rounds,indent=2,sort_keys=True)+'\n')
    (args.out/'timing.json').write_text(json.dumps({'total_seconds':time.monotonic()-started})+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':main()
