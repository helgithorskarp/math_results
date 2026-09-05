#!/usr/bin/env python3
"""Exact fixed-library coverage audit and complete-lift closure certificate."""
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
BASE=REPO/'hadwiger_nelson_parts509_degree7_extension610'


def require(condition,detail):
    if not condition:raise ValueError(detail)


def import_file(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def available(neighbours,colouring):
    return sorted(set('0123')-{colouring[v] for v in neighbours if v in colouring})


def compute():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for name,digest in manifest['inputs'].items():
        require(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input hash',name))
    require(sha256((HERE/'catalogue.json').read_bytes()).hexdigest()==manifest['catalogue_sha256'],
            'catalogue hash')
    sys.path.insert(0,str(BASE))
    try:base=import_file('lifting_primitives',BASE/'verify.py')
    finally:sys.path.pop(0)
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    require(len(old['forced'])==451 and set(old['forced'])<=set(range(509)), 'forced original set')
    _,edges,den,points,_=base.geometry(old)
    edges=[(a,b) for a,b in edges if b!=610];vertices=old['vertices']
    require(len(vertices)==585 and len(edges)==3083,'old support')
    require(sha256(base.old_opb(old)).hexdigest()==manifest['old_OPB_sha256'],'old lower-bound input')
    field=import_file('integer_field',REPO/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py')
    family=[set(row['D']) for row in old['family']]
    minimal=[i for i,D in enumerate(family) if not any(E<D for E in family)]
    require(len(minimal)==337 and all(any(family[i]<=D for i in minimal) for D in family),
            'minimal family equivalent to the full old family')
    library={('forced',v):[old['forced_witness'][str(v)]] for v in old['forced']}
    library.update({('kill',i):[old['family'][i]['witness']] for i in minimal})
    extra=json.loads((HERE/'catalogue.json').read_text())
    prior=json.loads((BASE/'certificate.json').read_text())
    imported={(row['kind'],int(row['key'])):row['witness'][:-1] for row in prior['replacement_witnesses']}
    for row in extra:
        key=row['kind'],row['key'];require(key in library,'unknown witness key')
        require(row['index']==len(library[key]),'witness ordering')
        if row['origin']=='imported_point610':require(row['witness']==imported[key],'imported witness')
        else:require(row['origin']=='new_pilot','witness origin tag')
        library[key].append(row['witness'])
    decoded={};old_edge_checks=0
    for (kind,key),witnesses in library.items():
        D={key} if kind=='forced' else family[key]
        labels=[v for v in vertices if v not in D]
        for j,witness in enumerate(witnesses):
            old_edge_checks+=base.proper(vertices,edges,D,witness)
            decoded[kind,key,j]=dict(zip(labels,witness,strict=True))
    coverage=[];closed=[];new_edge_checks=0
    for q in manifest['selection']:
        require(q not in vertices and points[q] not in {points[v] for v in vertices},'point collision')
        neighbours=[v for v in vertices if field.squared_distance(points[v],points[q])==(den*den,)+(0,)*7]
        require(sum(v<509 for v in neighbours)==6,('original degree',q))
        initial_misses=[v for v in old['forced'] if not available(neighbours,decoded['forced',v,0])]
        require(len(initial_misses)<=3 and q!=610,('cohort selection',q))
        missing={'forced':[],'kill':[]};selected={}
        for (kind,key),witnesses in library.items():
            for j,witness in enumerate(witnesses):
                colours=available(neighbours,decoded[kind,key,j])
                if colours:
                    selected[kind,key]=(j,colours[0]);break
            else:missing[kind].append(key)
        M=missing['kill'];common=set.intersection(*(family[i] for i in M)) if M else set()
        branches={};pool=set(old['pool'])
        if not missing['forced'] and common:
            for i in M:
                groups=[(j,sorted(family[j]-family[i])) for j in minimal
                        if j not in M and family[j]-family[i] and family[j]-family[i]<=pool]
                unique=sorted({tuple(group) for j,group in groups})
                packs=[list(map(list,C)) for C in combinations(unique,4)
                       if len(set().union(*map(set,C)))==sum(map(len,C))]
                branches[str(i)]=dict(groups=[[j,g] for j,g in groups],distinct_groups=len(unique),
                                       disjoint_four_subsets=len(packs))
        if missing['forced']:status='UNCLASSIFIED_FORCED_LIFT'
        elif not M:status='CLOSED_COMPLETE_LIFT'
        elif common & pool:status='CLOSED_POOL_REPAIR'
        elif common and all(branches[str(i)]['disjoint_four_subsets'] for i in M):status='CLOSED_COMMON_REPAIR'
        else:status='UNCLASSIFIED_KILLING_LIFT'
        if status.startswith('CLOSED'):
            closed.append(q)
            full_edges=edges+[(v,q) for v in neighbours]
            for (kind,key),(j,colour) in selected.items():
                D={key} if kind=='forced' else family[key]
                new_edge_checks+=base.proper(vertices+[q],full_edges,D,library[kind,key][j]+colour)
        coverage.append(dict(q=q,neighbors=neighbours,unit_edges=len(edges)+len(neighbours),
                             initial_missing_forced=initial_misses,
                             missing_forced=missing['forced'],missing_killing=M,
                             pool_repair_vertex=min(common & pool) if common & pool else None,
                             common_repair_vertices=sorted(common),branches=branches,status=status))
    require(points[678]==((240,0,0,0,0,0,0,0),(0,0,0,0,48,0,0,0)),
            'displayed coordinates of point678')
    return dict(status='EXACT FIXED-LIBRARY AUDIT; THREE SUPPORTS CLOSED THROUGH508',
                selected_points=manifest['selection'],closed_points=closed,
                closed_support_minimum_orders={str(q):509 for q in closed},
                unclassified_points=[r['q'] for r in coverage if not r['status'].startswith('CLOSED')],
                old_vertices=585,old_edges=3083,denominator=den,forced_vertices=451,minimal_killing_sets=337,
                old_colourings=788,extra_colourings=len(extra),new_pilot_colourings=sum(r['origin']=='new_pilot' for r in extra),
                verified_A7_colourings=sum(map(len,library.values())),old_retained_edge_checks=old_edge_checks,
                closed_support_retained_edge_checks=new_edge_checks,coverage=coverage,
                native_negative_answers_used_as_proofs=False,old_PB_proof_rechecked=False,
                old_OPB_sha256=manifest['old_OPB_sha256'],record_improvement=False,
                unclassified_means_non_four_colourable=False)


def main():
    result=compute()
    require(result==json.loads((HERE/'expected.json').read_text()),'expected coverage differs')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
