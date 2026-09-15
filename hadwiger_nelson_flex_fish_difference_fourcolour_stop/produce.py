#!/usr/bin/env python3
"""Build the conservative graph and a four-colouring certificate.

This optional producer needs python-sat.  The standard-library verifier is
the proof replay boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

from pysat.solvers import Cadical195


HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'hadwiger_nelson_fish_flex_contact_source_loss'


def components(n,edges):
    parent=list(range(n))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]];x=parent[x]
        return x
    def union(a,b):
        a,b=find(a),find(b)
        if a!=b:parent[b]=a
    for a,b in edges:union(a,b)
    out={}
    for v in range(n):out.setdefault(find(v),[]).append(v)
    return sorted(out.values(),key=lambda x:x[0])


def squared_error(dx,dy,epsilon):
    return 2*epsilon*(abs(dx)+abs(dy))+2*epsilon*epsilon


def graph():
    source=json.loads((SOURCE/'geometry_certificate.json').read_text())
    h=source['midpoint_denominator']
    points=[(Q(x,h),Q(y,h))for x,y in source['midpoint_numerators']]
    radius=Q(1,source['radius_denominator'])
    addresses=[(i,j)for i in range(23)for j in range(23)]
    mids=[(points[i][0]-points[j][0],points[i][1]-points[j][1])
          for i,j in addresses]
    address_error=2*radius
    possible_equal=[]
    for a,b in combinations(range(len(addresses)),2):
        if all(abs(mids[a][d]-mids[b][d])<=2*address_error for d in range(2)):
            possible_equal.append((a,b))
    clusters=components(len(addresses),possible_equal)
    cluster_of={a:c for c,members in enumerate(clusters)for a in members}
    possible_edges=set()
    pair_error=2*address_error
    for a,b in combinations(range(len(addresses)),2):
        dx=mids[a][0]-mids[b][0];dy=mids[a][1]-mids[b][1]
        d2=dx*dx+dy*dy;err=squared_error(dx,dy,pair_error)
        if cluster_of[a]==cluster_of[b]:
            if not d2+err<1:raise ValueError('possible internal unit edge')
        else:
            if not d2>err:raise ValueError('possible equality crosses clusters')
            if abs(d2-1)<=err:
                possible_edges.add(tuple(sorted((cluster_of[a],cluster_of[b]))))
    edges=sorted(possible_edges)
    return addresses,clusters,edges


def var(v,c):return 4*v+c+1


def colour(n,edges):
    clauses=[]
    for v in range(n):
        clauses.append([var(v,c)for c in range(4)])
        clauses.extend([-var(v,a),-var(v,b)]for a,b in combinations(range(4),2))
    for a,b in edges:clauses.extend([[-var(a,c),-var(b,c)]for c in range(4)])
    solver=Cadical195(bootstrap_with=clauses)
    if not solver.solve():raise ValueError('conservative graph is not four-colourable')
    model={x for x in solver.get_model()if x>0}
    word=''.join(str(next(c for c in range(4)if var(v,c)in model))for v in range(n))
    solver.delete()
    if not all(word[a]!=word[b]for a,b in edges):raise ValueError('bad word')
    return word


def main():
    parser=argparse.ArgumentParser();parser.add_argument('output',type=Path)
    args=parser.parse_args()
    addresses,clusters,edges=graph()
    stream=json.dumps({'clusters':clusters,'edges':edges},separators=(',',':'))+'\n'
    source_path=SOURCE/'geometry_certificate.json'
    cert={
        'schema':'flex-fish-ordered-difference-fourcolour-stop-v1',
        'source_geometry_sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),
        'formal_address_count':len(addresses),
        'possible_equality_cluster_count':len(clusters),
        'possible_unit_cluster_edge_count':len(edges),
        'conservative_graph_sha256':hashlib.sha256(stream.encode()).hexdigest(),
        'four_colour_word':colour(len(clusters),edges),
    }
    args.output.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in cert.items()if k!='four_colour_word'},indent=2))


if __name__=='__main__':main()
