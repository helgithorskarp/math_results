#!/usr/bin/env python3
"""Reconstruct exact H514 and decode its 516 published positive witnesses."""
import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
FRONTIER_SHA='6098161a878f17d4eb0f102124e1ea193543d15e4120c1ca0269a28baf0e6c80'


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def prepare(out,frontier):
    manifest=json.loads((HERE/'manifest.json').read_text())
    for name,digest in manifest.items():
        if sha256((REPO/name).read_bytes()).hexdigest()!=digest:raise ValueError(('input digest',name))
    E=module('published_H514_producer',REPO/'hadwiger_nelson_heule514_interface/engine.py')
    data=E.inputs();cert=json.loads((REPO/'hadwiger_nelson_heule514_interface/certificate.json').read_text())
    rows=[]
    for index,tail,fills in cert['transport']:
        c=list(data['source'][index][-1][:510]+tail)
        for v,x in fills:
            if c[v]!='.':raise ValueError('fill was not omitted')
            c[v]=x
        c=''.join(c);rows.append((E.check(c,data['edges']),c))
    for row in cert['native']:
        D=E.check(row['colouring'],data['edges'])
        if D!=row['D']:raise ValueError('native omissions')
        rows.append((D,row['colouring']))
    rows.sort(key=lambda r:(len(r[0]),r[0]))
    if len(rows)!=516 or len({tuple(D) for D,c in rows})!=516:raise ValueError('library count')
    ds=[set(D) for D,c in rows]
    if any(d<e for d in ds for e in ds):raise ValueError('antichain')
    raw=frontier.read_bytes()
    if sha256(raw).hexdigest()!=FRONTIER_SHA:raise ValueError('frozen frontier digest')
    previous=None;count=0
    for line in raw.decode('ascii').splitlines():
        O=tuple(map(int,line.split(',')))
        if len(O)!=6 or list(O)!=sorted(set(O)) or (previous is not None and previous>=O):raise ValueError('frontier order')
        omitted=set(O)
        if any(D<=omitted for D in ds):raise ValueError('frontier already covered')
        previous=O;count+=1
    if count!=258914:raise ValueError('frontier rows')
    graph=f'514 {len(data["edges"])}\n'+''.join(f'{u} {v}\n' for u,v in data['edges'])
    witnesses='516\n'+''.join(str(len(D))+' '+ ' '.join(map(str,D))+' '+c+'\n' for D,c in rows)
    (out/'graph.txt').write_text(graph);(out/'witnesses.txt').write_text(witnesses)
    checks=sum(sum(c[u]!='.' and c[v]!='.' for u,v in data['edges']) for D,c in rows)
    result=dict(vertices=514,unit_edges=len(data['edges']),colourings=516,positive_edge_checks=checks,
                cut_histogram={str(k):v for k,v in sorted(Counter(len(D) for D,c in rows).items())},
                large=data['large'],frontier_rows=count,frontier_bytes=len(raw),frontier_sha256=FRONTIER_SHA,
                graph_sha256=sha256(graph.encode()).hexdigest(),witnesses_sha256=sha256(witnesses.encode()).hexdigest(),
                graph_bytes=len(graph.encode()),witnesses_bytes=len(witnesses.encode()))
    (out/'inputs.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='large'},sort_keys=True))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--frontier',type=Path,required=True);a=p.parse_args();a.out.mkdir(exist_ok=False);prepare(a.out,a.frontier)
