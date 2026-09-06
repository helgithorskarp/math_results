#!/usr/bin/env python3
"""Generate the twenty exact small-side instances; does not call a solver."""
import argparse
import json
from pathlib import Path
import engine as E

ap=argparse.ArgumentParser()
ap.add_argument('--vertices-json',type=Path,required=True,help='JSON list of selected G indices in the142small block')
ap.add_argument('--out',type=Path,required=True)
args=ap.parse_args()
vertices=json.loads(args.vertices_json.read_text())
assert isinstance(vertices,list) and all(type(v) is int for v in vertices)
assert vertices==sorted(set(vertices))
data,sep=E.geometry();assert set(vertices)<=set(sep['small'])
args.out.mkdir(exist_ok=False)
small_edges=[e for e in data['edges'] if set(e)<=set(sep['small'])]
rows=json.loads((E.HERE/'certificate.json').read_text())['rows']
for i,row in enumerate(rows):
    n,cs=E.small_case(vertices,small_edges,sep['cross_edges'],sep['boundary'],row['pattern'])
    (args.out/f'case_{i:02d}.cnf').write_bytes(E.dimacs(n,cs))
print(json.dumps({'selected_small_vertices':len(vertices),'union_vertices':375+len(vertices),'cases':len(rows),'solver_calls':0}))
