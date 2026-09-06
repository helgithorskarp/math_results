#!/usr/bin/env python3
"""Exact component convolution for the fixed H514 boundary, no SAT queries."""
import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
NEIGHBOURS = [[361,417,495,503,509],[418,498,506,508],[359,362,502],[358,416,507]]


def load(path):
    return json.loads(path.read_text())


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def stream(counts):
    return ''.join(str(counts.get(i,0))+'\n' for i in range(4096)).encode('ascii')


def path_count(lists):
    previous=[int(bool(lists[0] & (1<<c))) for c in range(3)]
    for i in range(1,4):
        previous=[sum(previous[d] for d in range(3) if d!=c) if lists[i] & (1<<c) else 0 for c in range(3)]
    return sum(previous)


def build(out):
    start=time.monotonic()
    V=module('parent_exact_graph',REPO/'hadwiger_nelson_heule514_path_projection/verify.py')
    edges,_,B=V.geometry(); index={v:i for i,v in enumerate(B)}
    boundary_edges=[(index[u],index[v]) for u,v in edges if u in index and v in index]
    groups=[next((i for i,n in enumerate(NEIGHBOURS) if v in n),-1) for v in B]
    adjacent={i:set() for i in range(16)}
    for a,b in boundary_edges:adjacent[a].add(b);adjacent[b].add(a)
    pending=set(range(1,16)); components=[]
    while pending:
        component={min(pending)}; queue=list(component)
        for v in queue:
            for u in sorted(adjacent[v]-component):component.add(u);queue.append(u)
        pending-=component;components.append(sorted(component))
    assert sorted(map(len,components))==[2,3,4,6] and not adjacent[0]
    geometry=dict(vertices=B,groups=groups,edges=[list(e) for e in boundary_edges],components=components)
    (out/'boundary.json').write_text(json.dumps(geometry,indent=2)+'\n')
    graph=f'16 {len(boundary_edges)} 0\n'+''.join(f'{v} {g}\n' for v,g in zip(B,groups))+''.join(f'{u} {v}\n' for u,v in boundary_edges)
    (out/'boundary.txt').write_text(graph)
    counts=Counter({0:1}); witnesses={0:'0'+'.'*15};component_stats=[]
    for component in components:
        local=Counter(); local_witness={}; es=[(component.index(u),component.index(v)) for u,v in boundary_edges if u in component and v in component]
        for colours in product(range(4),repeat=len(component)):
            if any(colours[u]==colours[v] for u,v in es):continue
            blocked=0; row=['.']*16
            for i,c in zip(component,colours):
                row[i]=str(c)
                if c:blocked |= 1 << (3*groups[i]+c-1)
            local[blocked]+=1; text=''.join(row)
            if blocked not in local_witness or text<local_witness[blocked]:local_witness[blocked]=text
        following=Counter(); fw={}
        for a,x in counts.items():
            for b,y in local.items():
                key=a|b; following[key]+=x*y
                text=''.join(v if v!='.' else u for u,v in zip(witnesses[a],local_witness[b]))
                if key not in fw or text<fw[key]:fw[key]=text
        counts,witnesses=following,fw
        component_stats.append(dict(vertices=[B[i] for i in component],colourings=sum(local.values()),blocked_profiles=len(local),cumulative_profiles=len(counts)))
    counts={4095^k:v for k,v in counts.items()};witnesses={4095^k:v for k,v in witnesses.items()}
    raw=stream(counts);(out/'profiles.counts').write_bytes(raw)
    kernel=load(REPO/'hadwiger_nelson_heule514_path_projection/certificate.json')['obstructions']
    bad_counts=Counter();profile_hist=Counter();extension_hist=Counter()
    claim_rows=[dict(clause=i,boundary_colourings=0,unique_violation_colourings=0,witness=None,unique_witness=None) for i in range(37)]
    good_witness=None;bad_witness=None
    for key,count in sorted(counts.items()):
        lists=[(key>>(3*i))&7 for i in range(4)]
        bad=[j for j,row in enumerate(kernel) if not any(key & (1<<(x-5)) for x in row['clause'] if x>0)]
        extensions=path_count(lists);assert bool(extensions)==(not bad)
        bad_counts[len(bad)]+=count;profile_hist[len(bad)]+=1;extension_hist[extensions]+=count
        for j in bad:
            r=claim_rows[j];r['boundary_colourings']+=count
            if r['witness'] is None:r['witness']=witnesses[key]
        if len(bad)==1:
            r=claim_rows[bad[0]];r['unique_violation_colourings']+=count
            if r['unique_witness'] is None:r['unique_witness']=witnesses[key]
        if bad and bad_witness is None:bad_witness=dict(colouring=witnesses[key],lists=lists,violated_clauses=bad)
        if not bad and good_witness is None:
            tail=next(c for c in product(range(1,4),repeat=4) if all(lists[i] & (1<<(x-1)) for i,x in enumerate(c)) and all(c[i]!=c[i+1] for i in range(3)))
            good_witness=dict(boundary_colouring=witnesses[key],path_colouring=''.join(map(str,tail)),lists=lists)
    # Prefer a counterexample requiring the entire P4: each proper selected
    # subpath still extends. This separates the path interaction from an
    # individual vertex simply having an empty list.
    j=next(j for j,r in enumerate(kernel) if r['mask']==15 and claim_rows[j]['unique_witness'] is not None)
    c=claim_rows[j]['unique_witness']
    lists=[sum(1<<(x-1) for x in range(1,4) if str(x) not in {c[index[v]] for v in neighbours}) for neighbours in NEIGHBOURS]
    bad_witness=dict(colouring=c,lists=lists,violated_clauses=[j])
    result=dict(status='COMPLETE FIXED BOUNDARY PROFILE CENSUS',universal_extension=(bad_witness is None),record_improvement=False,
                boundary_vertices=16,boundary_edges=len(boundary_edges),local_vertices=20,local_edges=len(boundary_edges)+22,
                component_stats=component_stats,proper_boundary_colourings=sum(counts.values()),attainable_list_profiles=len(counts),
                extending_boundary_colourings=bad_counts[0],nonextending_boundary_colourings=sum(counts.values())-bad_counts[0],
                attainable_extending_profiles=profile_hist[0],attainable_nonextending_profiles=len(counts)-profile_hist[0],
                full_local_colourings=sum(k*v for k,v in extension_hist.items()),
                violation_histogram={str(k):v for k,v in sorted(bad_counts.items())},profile_violation_histogram={str(k):v for k,v in sorted(profile_hist.items())},
                extension_count_histogram={str(k):v for k,v in sorted(extension_hist.items())},
                attainable_obstruction_clauses=[r['clause'] for r in claim_rows if r['boundary_colourings']],
                individually_necessary_clauses=[r['clause'] for r in claim_rows if r['unique_violation_colourings']],
                profiles_sha256=sha256(raw).hexdigest(),profiles_bytes=len(raw),native_graph_queries=0)
    certificate=dict(boundary_order=B,nonextension=bad_witness,extension=good_witness,clauses=claim_rows)
    (out/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'run.json').write_text(json.dumps(dict(seconds=time.monotonic()-start,python_method='four exact component convolutions',native_graph_queries=0),indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(exist_ok=False);build(a.out)
