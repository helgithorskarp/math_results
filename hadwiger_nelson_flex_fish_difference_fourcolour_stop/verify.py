#!/usr/bin/env python3
"""Exact conservative verifier for the flexible-fish difference body.

The support is {p_i-p_j: 0<=i,j<23}, where the p_i are the unique exact
points isolated by the source contraction certificate.  Rational interval
bounds group every potentially coincident address, include every potentially
unit pair between groups, and then check a proper four-colouring of that
supergraph.  Thus unresolved identities can only make the actual graph easier
to colour.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path


HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'hadwiger_nelson_fish_flex_contact_source_loss'


def need(ok,message):
    if not ok:raise ValueError(message)


def source_replay():
    path=SOURCE/'verify.py'
    spec=importlib.util.spec_from_file_location('fish_contact_source_verify',path)
    need(spec is not None and spec.loader is not None,'source verifier import')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    summary=module.verify(SOURCE/'geometry_certificate.json',
                          SOURCE/'relation_certificate.json')
    need(summary['chromatic_number']==4,'source chromaticity')
    need(summary['complete_unit_edges']==43,'source edge count')
    return summary


def components(n,edges):
    parent=list(range(n))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]];x=parent[x]
        return x
    for a,b in edges:
        a,b=find(a),find(b)
        if a!=b:parent[b]=a
    out={}
    for v in range(n):out.setdefault(find(v),[]).append(v)
    return sorted(out.values(),key=lambda x:x[0])


def distance_error(dx,dy,coordinate_error):
    # If both coordinate errors have absolute value <= e, expand
    # (dx+ex)^2+(dy+ey)^2 exactly and bound the linear and quadratic terms.
    return 2*coordinate_error*(abs(dx)+abs(dy))+2*coordinate_error**2


def verify(cert_path=HERE/'certificate.json',check_expected=True):
    cert_path=Path(cert_path);cert=json.loads(cert_path.read_text())
    need(cert['schema']=='flex-fish-ordered-difference-fourcolour-stop-v1','schema')
    geometry_path=SOURCE/'geometry_certificate.json'
    geometry_hash=hashlib.sha256(geometry_path.read_bytes()).hexdigest()
    need(cert['source_geometry_sha256']==geometry_hash,'source geometry hash')
    source_summary=source_replay()
    geometry=json.loads(geometry_path.read_text())
    h=geometry['midpoint_denominator']
    points=[(Q(x,h),Q(y,h))for x,y in geometry['midpoint_numerators']]
    need(len(points)==23,'source order')
    radius=Q(1,geometry['radius_denominator'])

    addresses=[(i,j)for i in range(23)for j in range(23)]
    need(len(addresses)==cert['formal_address_count']==529,'address count')
    mids=[(points[i][0]-points[j][0],points[i][1]-points[j][1])
          for i,j in addresses]
    address_error=2*radius
    possible_equal=[]
    for a,b in combinations(range(529),2):
        if (abs(mids[a][0]-mids[b][0])<=2*address_error and
            abs(mids[a][1]-mids[b][1])<=2*address_error):
            possible_equal.append((a,b))
    clusters=components(529,possible_equal)
    need(len(clusters)==cert['possible_equality_cluster_count']==433,'cluster count')
    cluster_of={a:c for c,members in enumerate(clusters)for a in members}

    pair_error=2*address_error
    possible_edges=set();within_upper=Q(0)
    separation_lower=None;excluded_unit_gap=None
    pair_checks=0
    for a,b in combinations(range(529),2):
        dx=mids[a][0]-mids[b][0];dy=mids[a][1]-mids[b][1]
        d2=dx*dx+dy*dy;err=distance_error(dx,dy,pair_error)
        pair_checks+=1
        if cluster_of[a]==cluster_of[b]:
            upper=d2+err
            need(upper<1,'possible within-cluster unit pair')
            within_upper=max(within_upper,upper)
            continue
        need(d2>err,'possible equality crosses clusters')
        gap=d2-err
        separation_lower=gap if separation_lower is None else min(separation_lower,gap)
        if abs(d2-1)<=err:
            possible_edges.add(tuple(sorted((cluster_of[a],cluster_of[b]))))
        else:
            gap=abs(d2-1)-err
            excluded_unit_gap=gap if excluded_unit_gap is None else min(excluded_unit_gap,gap)
    edges=sorted(possible_edges)
    need(len(edges)==cert['possible_unit_cluster_edge_count']==1646,'possible edge count')
    stream=json.dumps({'clusters':clusters,'edges':edges},separators=(',',':'))+'\n'
    digest=hashlib.sha256(stream.encode()).hexdigest()
    need(digest==cert['conservative_graph_sha256'],'conservative graph hash')
    word=cert['four_colour_word']
    need(len(word)==433 and set(word)<=set('0123'),'four-colour word')
    need(all(word[a]!=word[b]for a,b in edges),'improper four-colour word')

    # Every diagonal address (i,i) is the same exact zero point, independently
    # of the isolating intervals.  This alone lowers the trivial 529 bound by 22.
    diagonal=[23*i+i for i in range(23)]
    need(all(mids[a]==(0,0)for a in diagonal),'diagonal midpoint')
    need(len({cluster_of[a]for a in diagonal})==1,'diagonal cluster')
    summary={
        'status':'EXACT FLEX-FISH DIFFERENCE-BODY FOUR-COLOUR STOP VERIFIED',
        'scope':'complete strict graph on all ordered differences of the exact 23-point contact source',
        'source_geometry_sha256':geometry_hash,
        'source_chromatic_number':source_summary['chromatic_number'],
        'formal_addresses':529,
        'distinct_physical_point_upper_bound':507,
        'possible_equality_clusters':len(clusters),
        'formal_address_pair_checks':pair_checks,
        'possible_unit_cluster_edges':len(edges),
        'within_cluster_squared_distance_upper':str(within_upper),
        'different_cluster_squared_separation_lower':str(separation_lower),
        'excluded_squared_unit_gap_lower':str(excluded_unit_gap),
        'conservative_graph_sha256':digest,
        'actual_chromatic_number':4,
        'proper_four_colouring':True,
        'record_candidate':False,
    }
    if check_expected:
        expected=json.loads((HERE/'EXPECTED.json').read_text())
        need(summary==expected,'expected summary')
    return summary


def main():
    parser=argparse.ArgumentParser();parser.add_argument('certificate',nargs='?',type=Path,default=HERE/'certificate.json')
    parser.add_argument('--no-expected',action='store_true');args=parser.parse_args()
    print(json.dumps(verify(args.certificate,not args.no_expected),indent=2,sort_keys=True))


if __name__=='__main__':main()
