"""Recognize the specified core and reject its arbitrary physical43 extension."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import re
import core


def parse(graph):
    if not isinstance(graph,dict) or type(graph.get('n')) is not int or graph['n']!=43:
        raise ValueError('n must be43')
    text=graph.get('red_hex')
    if not isinstance(text,str) or re.fullmatch('[0-9a-f]{226}',text) is None:
        raise ValueError('canonical903-bit red_hex')
    word=int(text,16)
    if word >> 903:
        raise ValueError('unused high bit')
    rows=[0]*43
    for bit,(u,v) in enumerate(combinations(range(43),2)):
        if word >> bit & 1:
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return rows


def cycle_order(vertices, adjacent):
    vertices=sorted(vertices)
    neighbors={v:sorted(u for u in vertices if u!=v and adjacent(u,v)) for v in vertices}
    if len(vertices)!=5 or any(len(ns)!=2 for ns in neighbors.values()):
        return None
    order=[vertices[0],neighbors[vertices[0]][0]]
    while len(order)<5:
        options=[v for v in neighbors[order[-1]] if v!=order[-2]]
        if len(options)!=1 or options[0] in order:
            return None
        order.append(options[0])
    return order if order[0] in neighbors[order[-1]] else None


def recognize(rows, vertices):
    """In C5[C5], within-block pair distinguishers number2, others14."""
    mask=sum(1 << v for v in vertices)
    unseen=set(vertices);blocks=[]
    while unseen:
        u=min(unseen)
        group={v for v in vertices if v==u or
               ((rows[u]^rows[v]) & mask & ~((1 << u)|(1 << v))).bit_count()==2}
        if len(group)!=5 or not group<=unseen:
            return None
        blocks.append(sorted(group));unseen-=group
    if len(blocks)!=5:
        return None
    red=lambda u,v:bool(rows[u] >> v & 1)
    inner=[cycle_order(block,red) for block in blocks]
    if any(order is None for order in inner):
        return None
    outer=cycle_order(range(5),lambda i,j:red(blocks[i][0],blocks[j][0]))
    if outer is None:
        return None
    mapping=[v for i in outer for v in inner[i]]
    # This literal final check is the soundness boundary: the special
    # recognizer is not trusted to infer any unchecked edge or automorphism.
    if any(red(mapping[i],mapping[j])!=core.core_edge(i,j)
           for i,j in combinations(range(25),2)):
        return None
    return mapping


def reject(graph, vertices):
    rows=parse(graph)
    if not isinstance(vertices,list) or len(vertices)!=25 or any(type(v) is not int or not 0<=v<43 for v in vertices) or len(set(vertices))!=25:
        raise ValueError('25 distinct core vertices')
    mapping=recognize(rows,vertices)
    if mapping is None:
        return dict(status='OUTSIDE_SPECIFIED_CORE_FAMILY',meaning='Supplied25-set is not C5[C5]; no target verdict')
    outside=min(set(range(43))-set(mapping))
    attachment=sum(((rows[outside] >> v)&1) << i for i,v in enumerate(mapping))
    local=core.obstruction(attachment)
    physical=sorted(outside if v==25 else mapping[v] for v in local['vertices'])
    certificate=dict(format='physical-monochromatic-five-v1',n=43,color=local['color'],
                     vertices=physical,red_hex_sha256=hashlib.sha256(graph['red_hex'].encode('ascii')).hexdigest())
    return dict(status='REJECTED_COMPLETE_CORE_EXTENSION_FAMILY',ordered_core=mapping,
                outside_vertex=outside,certificate=certificate)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input',type=Path);a=p.parse_args()
    request=json.loads(a.input.read_text())
    print(json.dumps(reject(request['graph'],request['core_vertices']),indent=2,sort_keys=True))
