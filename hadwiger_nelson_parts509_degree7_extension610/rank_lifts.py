#!/usr/bin/env python3
"""Replay the witness-compatibility screen; this does not solve new graphs."""
import argparse
import importlib.util
import json
from pathlib import Path
from verify import geometry, proper, REPO


def compute():
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    _,edges,den,points,raw=geometry(old)
    old_edges=[(a,b) for a,b in edges if b!=610]
    spec=importlib.util.spec_from_file_location('field',REPO/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py')
    field=importlib.util.module_from_spec(spec);spec.loader.exec_module(field)
    witnesses=[]
    for v in old['forced']:
        witnesses.append(('forced',str(v),[v],old['forced_witness'][str(v)]))
    for i,row in enumerate(old['family']):
        witnesses.append(('kill',str(i),row['D'],row['witness']))
    decoded=[]
    for kind,key,D,witness in witnesses:
        proper(old['vertices'],old_edges,D,witness)
        decoded.append((kind,key,dict(zip([v for v in old['vertices'] if v not in D],witness,strict=True))))
    ranked=[];target=(den*den,)+(0,)*7
    for i,row in enumerate(raw['points']):
        if len(row['neighbors'])!=6:continue
        q=509+i
        neighbours=[v for v in old['vertices'] if field.squared_distance(points[v],points[q])==target]
        misses=[[kind,key] for kind,key,colours in decoded
                if len({colours[v] for v in neighbours if v in colours})==4]
        ranked.append(dict(q=q,degree_into_D7=len(neighbours),neighbors=neighbours,
                           failed_forced=sum(kind=='forced' for kind,key in misses),
                           failed_kills=sum(kind=='kill' for kind,key in misses),misses=misses))
    ranked.sort(key=lambda r:(r['failed_forced'],r['failed_kills'],r['q']))
    return dict(candidates=len(ranked),old_vertices=585,old_edges=len(old_edges),
                old_verified_witnesses=len(witnesses),ranked=ranked)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    result=compute();args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(candidates=result['candidates'],selected=result['ranked'][0]),indent=2))


if __name__=='__main__':main()
