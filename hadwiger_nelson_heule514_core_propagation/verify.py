#!/usr/bin/env python3
"""Independent simultaneous-round cores and direct colouring restoration.

Imports no queue-peeling/producer implementation. Geometry and compressed
witnesses are reconstructed with the separate published checker/decoder.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import struct
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
FRONTIER_SHA='6098161a878f17d4eb0f102124e1ea193543d15e4120c1ca0269a28baf0e6c80'
RECORD=struct.Struct('<h65s')


def need(ok,message):
    if not ok:raise ValueError(message)


def load(path):return json.loads(path.read_text())


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def indices(bits):
    while bits:
        bit=bits & -bits;yield bit.bit_length()-1;bits-=bit


def inputs(work):
    for name,digest in load(HERE/'manifest.json').items():need(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input hash',name))
    V=module('independent_H514_geometry',REPO/'hadwiger_nelson_heule514_path_projection/verify.py')
    edges,_,_=V.geometry()
    P=module('public_H514_recipe_decoder',REPO/'hadwiger_nelson_heule514_interface/verify.py')
    R=module('reviewed_inherited_decoder',REPO/'hadwiger_nelson_heule517_whole_decision_review1/independent_check.py')
    old=load(REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json')
    labels=[v for v in range(553) if '510' in old['provenance'][v]]
    L={i for i,v in enumerate(labels) if all(Fraction(old['coordinates'][str(v)][a][k])==0 for a in(0,1) for k in(2,3,6,7))}
    groups=R.inherited_witnesses(REPO,old,labels,L,set(range(517))-L)
    source=[c for name in ['prior','small','large2','large3','large4'] for row,c in groups[name]]
    source += [r['colouring'] for r in load(REPO/'hadwiger_nelson_heule517_whole_decision/certificate.json')['rows']]
    need(len(source)==963,'inherited source indexing')
    cert=load(REPO/'hadwiger_nelson_heule514_interface/certificate.json')
    colours=[P.decode(r,source) for r in cert['transport']]+[r['colouring'] for r in cert['native']]
    rows=sorted([([v for v,c in enumerate(s) if c=='.'],s) for s in colours],key=lambda row:(len(row[0]),row[0]))
    need(len(rows)==516 and len({tuple(D) for D,c in rows})==516,'canonical positive library')
    checks=0
    for D,c in rows:checks+=P.check(c,D,edges)
    graph=f'514 {len(edges)}\n'+''.join(f'{u} {v}\n' for u,v in edges)
    witnesses='516\n'+''.join(str(len(D))+' '+' '.join(map(str,D))+' '+c+'\n' for D,c in rows)
    need((work/'graph.txt').read_text()==graph,'entrywise actual native graph')
    need((work/'witnesses.txt').read_text()==witnesses,'entrywise actual native colourings and cut indexing')
    meta=load(work/'inputs.json');need(meta['large']==sorted(L),'block labels')
    for key,raw in [('graph',graph),('witnesses',witnesses)]:need(meta[key+'_sha256']==sha256(raw.encode()).hexdigest(),'native packet digest')
    public=HERE/'certificate.json'
    if public.exists():
        used=load(public)['witnesses'];need([r['canonical_index'] for r in used]==[288,370],'used witness indexing')
        for row in used:need((row['D'],row['colouring'])==rows[row['canonical_index']],'compact witness equals decoded public source')
    return edges,rows,L,checks


def simultaneous_core(adjacency,selected,initial_possible=None):
    """Synchronous rounds; only neighbours of a removed round can change."""
    live=selected;possible=selected if initial_possible is None else selected & initial_possible;peeled=[]
    while possible:
        remove=0
        for v in indices(possible):
            if (adjacency[v]&live).bit_count()<4:remove |= 1<<v
        if not remove:break
        peeled.extend(indices(remove));live &= ~remove;possible=0
        for v in indices(remove):possible |= adjacency[v]
        possible &= live
    return live,peeled


def restore(adjacency,edges,original,core,peeled,seed):
    c=bytearray(seed.encode('ascii'))
    for v in indices(((1<<len(adjacency))-1) ^ core):c[v]=46
    for v in reversed(peeled):
        used={c[u] for u in indices(adjacency[v]) if c[u]!=46}
        coloured=sum(c[u]!=46 for u in indices(adjacency[v]))
        need(coloured<=3,'reverse synchronous peeling degree')
        c[v]=min(set(range(48,52))-used)
    need(sum(1<<v for v,x in enumerate(c) if x!=46)==original,'original omissions preserved')
    checks=0
    for u,v in edges:
        if c[u]!=46 and c[v]!=46:
            need(c[u]!=c[v],'restored full graph edge');checks+=1
    return checks


def controls():
    clique=list(combinations(range(5),2));path=clique+[(0,5),(5,6),(6,7)];two=clique+[(u+5,v+5) for u,v in clique]
    cases=[(5,clique,[],[0],'.0123',31,False),(5,clique,[1],[0],'.0123',0,True),
           (8,path,[],[0],'.0123010',31,False),(8,path,[1],[0],'.0123010',0,True),
           (8,path,[5],[0],'.0123010',31,False),(8,path,[0],[0],'.0123010',0,True),
           (10,two,[],[0,5],'.0123.0123',1023,False),(10,two,[1],[0,5],'.0123.0123',992,False),
           (10,two,[1,6],[0,5],'.0123.0123',0,True),(4,[],[],[0],'.012',0,True)]
    subset_checks=restored=0
    for n,edges,O,D,seed,expected,covered in cases:
        adj=[0]*n
        for u,v in edges:adj[u]|=1<<v;adj[v]|=1<<u
        selected=((1<<n)-1)^sum(1<<v for v in O)
        core,peeled=simultaneous_core(adj,selected)
        union=0;sub=selected
        while True:
            if all((adj[v]&sub).bit_count()>=4 for v in indices(sub)):union |= sub
            subset_checks+=1
            if sub==0:break
            sub=(sub-1)&selected
        need(core==expected==union,'maximum core by exhaustive valid-subset union')
        need((not any(core & (1<<v) for v in D))==covered,'entire positive cut required')
        if covered:restore(adj,edges,selected,core,peeled,seed);restored+=1
    return dict(graph_cases=len(cases),induced_subset_checks=subset_checks,restoration_cases=restored)


def verify(work,frontier):
    start=time.monotonic();edges,rows,L,seed_checks=inputs(work)
    control_report=controls();raw=frontier.read_bytes();need(sha256(raw).hexdigest()==FRONTIER_SHA,'frozen whole frontier')
    adj=[0]*514
    for u,v in edges:adj[u]|=1<<v;adj[v]|=1<<u
    all_vertices=(1<<514)-1
    # Six original omissions cannot lower an original degree>=10 below four.
    initial_possible=sum(1<<v for v in range(514) if adj[v].bit_count()<=9)
    single={D[0]:i for i,(D,c) in enumerate(rows) if len(D)==1};forced=sum(1<<v for v in single)
    other=[(i,sum(1<<v for v in D)) for i,(D,c) in enumerate(rows) if len(D)>1]
    need(len(single)==484 and len(other)==32,'library partition')
    counter=covered=restored_checks=peeled_sum=0;hist=Counter();cut_hist=Counter();large_hist=Counter();new_mask_hist=Counter();examples=[]
    digest=sha256();core_digest=sha256();core_bytes=0
    with (work/'cores.bin').open('rb') as records,(work/'survivors.txt').open('rb') as surviving:
        for line in raw.splitlines(keepends=True):
            O=tuple(map(int,line.decode('ascii').strip().split(',')));omitted=sum(1<<v for v in O);selected=all_vertices ^ omitted
            core,peeled=simultaneous_core(adj,selected,initial_possible)
            entry=records.read(RECORD.size);need(len(entry)==RECORD.size,'complete native core record')
            core_digest.update(entry);core_bytes+=len(entry);tag,bits=RECORD.unpack(entry)
            need(int.from_bytes(bits,'little')==core,'entrywise independent core equality')
            missing_forced=forced & ~core
            if missing_forced:certificate=single[(missing_forced & -missing_forced).bit_length()-1]
            else:certificate=next((i for i,D in other if not D & core),-1)
            need(certificate==tag,'first canonical positive certificate')
            if certificate>=0:
                covered+=1;cut_hist[certificate]+=1
                restored_checks+=restore(adj,edges,selected,core,peeled,rows[certificate][1])
            else:
                need(surviving.readline()==line,'entrywise exact surviving frontier')
                digest.update(line);large_hist[len(set(O)&L)]+=1
                new_mask_hist[sum(1<<(v-510) for v in O if v>=510)]+=1
                if len(examples)<3:examples.append(list(O))
            hist[len(peeled)]+=1;peeled_sum+=len(peeled);counter+=1
            if counter%32768==0:print(json.dumps(dict(checked=counter,covered=covered)),flush=True)
        need(not records.read(1) and not surviving.read(1),'both streams terminated')
    need(counter==258914,'complete family size')
    native=load(work/'summary.json')
    for k,value in dict(rows=counter,covered=covered,survivors=counter-covered,peeled_vertices_total=peeled_sum,
                        peel_histogram={str(k):v for k,v in sorted(hist.items())},cut_histogram={str(k):v for k,v in sorted(cut_hist.items())}).items():
        need(native[k]==value,('native aggregate',k))
    result=dict(status='COMPLETE EXACT H514 CORE-CERTIFICATE PROPAGATION VERIFIED',record_improvement=False,
                family_closed=(covered==counter),vertices=514,unit_edges=len(edges),public_colourings=516,
                seed_edge_checks=seed_checks,rows=counter,covered=covered,survivors=counter-covered,
                peeled_vertices_total=peeled_sum,peel_histogram={str(k):v for k,v in sorted(hist.items())},
                cut_histogram={str(k):v for k,v in sorted(cut_hist.items())},restored_full_graph_edge_checks=restored_checks,
                complete_core_records=counter,core_record_bytes=core_bytes,core_records_sha256=core_digest.hexdigest(),
                survivor_sha256=digest.hexdigest(),survivor_bytes=(work/'survivors.txt').stat().st_size,
                survivors_by_large_omissions={str(k):v for k,v in sorted(large_hist.items())},
                survivors_by_new_omission_mask={str(k):v for k,v in sorted(new_mask_hist.items())},
                first_survivors=examples,controls=control_report,solver_used=False,seconds=time.monotonic()-start)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--frontier',type=Path,required=True);p.add_argument('--report',type=Path);a=p.parse_args()
    r=verify(a.work,a.frontier)
    if a.report:a.report.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,sort_keys=True))
