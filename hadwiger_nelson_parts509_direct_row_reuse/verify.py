#!/usr/bin/env python3
"""Replay published killing witnesses and their implication for 47 deletion rows.

Every unit edge is reconstructed from exact coordinates. No SAT solver or
completeness assumption on the interface-colouring list is required.
"""
import argparse
from collections import Counter
import hashlib
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
sys.path.insert(0,str(REPO/'hadwiger_nelson_parts509_pool_shape_closure'))
import exactgeom


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_colouring(colours,vertices,edges):
    assert set(colours)==set(vertices), 'colouring domain mismatch'
    assert set(colours.values())<=set(range(4)), 'not a four-colouring'
    for a,b in edges:
        if a in colours and b in colours:
            assert colours[a]!=colours[b], f'monochromatic edge {a}-{b}'


def main():
    if not __debug__:raise RuntimeError('Run without Python optimization flags')
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    record=json.loads((HERE/'direct_rows.json').read_text())
    source=HERE/record['source']
    assert source.resolve()==(REPO/'hadwiger_nelson_parts509_s_replacement_budget/certificate.json').resolve()
    assert digest(source)==record['source_sha256']
    cert=json.loads(source.read_text());rows=record['rows']
    assert len(rows)==47 and rows==sorted(rows,key=lambda r:r['R'])
    assert len({tuple(r['R']) for r in rows})==len(rows)
    points,_=exactgeom.build(REPO);den,ipts=exactgeom.scale_points(points)
    U=sorted(json.loads((REPO/'hadwiger_nelson_parts509_s_replacement_budget/pool_S.json').read_text())['W_S'])
    L=list(range(374));S=list(range(374,509));Q=[v for v in U if v>=509]
    assert U==cert['pool']==S+Q and len(Q)==168
    assert cert['S']==S and cert['Q5']==Q
    V=L+U
    assert len({(tuple(points[v][0]),tuple(points[v][1])) for v in V})==len(V)==677
    edges=exactgeom.unit_pairs(ipts,den,V)
    assert len(edges)==3400
    wl=[r['witness_colouring_L'] for r in json.loads((REPO/'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())['classes']]
    decoded={};sizes=Counter();cases=[]
    for row in rows:
        R=row['R'];D=row['D'];i=row['source_index']
        assert R==sorted(set(R)) and len(R)==3 and set(R)<=set(S)
        assert D==sorted(set(D)) and D and set(D)<=set(R)
        assert type(i) is int and 0<=i<len(cert['killing_sets'])
        w=cert['killing_sets'][i];assert w['D']==D
        if i not in decoded:
            p=w['class_index'];c=w['colouring_U_minus_D']
            assert type(p) is int and 0<=p<len(wl)
            active=[v for v in U if v not in D]
            assert len(c)==len(active) and set(c)<=set('0123')
            assert len(wl[p])==len(L) and set(wl[p])<=set('0123')
            colour={v:int(a) for v,a in zip(L,wl[p])}
            colour.update({v:int(a) for v,a in zip(active,c)})
            verify_colouring(colour,L+active,edges)
            decoded[i]=colour;sizes[len(D)]+=1
        restricted={v:a for v,a in decoded[i].items() if v not in R}
        verify_colouring(restricted,[v for v in V if v not in R],edges)
        cases.append({'R':R,'D':D,'source_index':i,'vertices':len(restricted),
                      'unit_edges':sum(a not in R and b not in R for a,b in edges)})
    edge_bytes=''.join(f'{a} {b}\n' for a,b in edges).encode()
    result={'status':'EXACT PUBLISHED COLOURINGS AND 47 RESTRICTIONS VERIFIED',
            'pool_points':len(V),'unit_edges':len(edges),'target_rows':len(rows),
            'source_witnesses':len(decoded),'source_set_sizes':dict(sorted(sizes.items())),
            'source_sha256':digest(source),'rows_sha256':digest(HERE/'direct_rows.json'),
            'exact_edges_sha256':hashlib.sha256(edge_bytes).hexdigest(),'cases':cases}
    data=json.dumps(result,indent=2,sort_keys=True)+'\n'
    expected=HERE/'expected.json'
    assert json.loads(data)==json.loads(expected.read_text())
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(data)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},sort_keys=True))


if __name__=='__main__':main()
