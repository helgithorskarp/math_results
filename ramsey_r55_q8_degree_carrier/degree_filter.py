#!/usr/bin/env python3
"""Sound degree filter with a literal five-set witness; no candidate search."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path

PAIRS=list(it.combinations(range(43),2))


def read_graph(g):
    if g.get('n') != 43 or type(g.get('red_hex')) is not str:
        raise ValueError('expected n=43 and a red_hex string')
    code=g['red_hex']
    if len(code)!=226 or any(c not in '0123456789abcdef' for c in code):
        raise ValueError('canonical 226-digit lowercase hex required')
    value=int(code,16)
    if value >= 1<<903:
        raise ValueError('unused high bit is nonzero')
    matrix=[[0]*43 for _ in range(43)]
    for i,(u,v) in enumerate(PAIRS):
        matrix[u][v]=matrix[v][u]=(value>>i)&1
    return matrix,hashlib.sha256(code.encode('ascii')).hexdigest()


def check(g):
    a,digest=read_graph(g)
    degrees=[sum(row) for row in a]
    result={'graph_sha256':digest,'red_degrees':degrees}
    for root,degree in enumerate(degrees):
        if 18<=degree<=24:
            continue
        color=int(degree>24)
        neighbors=[v for v in range(43) if v!=root and a[root][v]==color][:25]
        if len(neighbors)!=25:
            raise ValueError('invalid degree obstruction')
        for four in it.combinations(neighbors,4):
            if all(a[u][v]==color for u,v in it.combinations(four,2)):
                five=sorted([root,*four]); witness_color=color
                break
        else:
            for five in it.combinations(neighbors,5):
                if all(a[u][v]!=color for u,v in it.combinations(five,2)):
                    witness_color=1-color
                    break
            else:
                raise ValueError('degree obstruction has no literal witness')
        result.update({'status':'REJECT_WITH_MONOCHROMATIC_FIVE','degree_vertex':root,
                       'vertices':list(five),'color':witness_color})
        return result
    result['status']='DEGREE_PASS_NO_RAMSEY_VERDICT'
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('graph',type=Path);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();result=check(json.loads(a.graph.read_text()))
    a.out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
