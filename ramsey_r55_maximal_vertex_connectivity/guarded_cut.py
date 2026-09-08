#!/usr/bin/env python3
"""Symbolic universally valid degree-guarded cut clause; no solver numbering."""
import argparse,json

def clause(a,b,color):
    for vertices in (a,b):
        if not isinstance(vertices,list) or not vertices or any(type(v) is not int or not 0<=v<43 for v in vertices) or vertices!=sorted(set(vertices)):
            raise ValueError('nonempty sorted physical vertex lists required')
    if set(a)&set(b) or color not in ('red','blue'):raise ValueError('disjoint parts and a valid color required')
    k=43-len(a)-len(b)
    if not 0<=k<=23:raise ValueError('degree-guard threshold exceeds the good43 degree window')
    return {'operator':'OR','negated_degree_guards':[{'vertex':v,'color':color,'degree_at_least':k+1} for v in range(43)],'physical_edge_literals':[{'pair':sorted([u,v]),'red_value':color=='red'} for u in a for v in b],'separator_size':k,'scope':'Valid under good43 constraints; no contradiction unless all degree guards hold and every cross edge has the opposite color.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('a',help='comma-separated sorted labels');p.add_argument('b');p.add_argument('--color',choices=('red','blue'),default='red');args=p.parse_args()
    print(json.dumps(clause([int(x) for x in args.a.split(',')],[int(x) for x in args.b.split(',')],args.color),indent=2,sort_keys=True))
