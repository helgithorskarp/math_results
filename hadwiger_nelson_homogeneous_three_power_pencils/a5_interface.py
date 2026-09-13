#!/usr/bin/env python3
"""Embed the general nine pencils in A5 and pin their h4195 residual incidence."""
import argparse
from itertools import combinations,product
import hashlib
import json
from pathlib import Path
import exact as E

EXPECTED_RESIDUAL='42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d'


def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def run(residual_path):
    normals=sorted({E.canonical_normal(n) for n in product(range(4),repeat=3) if sum(bool(x) for x in n)>=2})
    general=[]
    for a,b in product((1,2,3),repeat=2):
        p=[n for n in normals if n[0]^E.gf_mul(a,n[1])^E.gf_mul(b,n[2])==0]
        E.need(len(p)==5,'five projective sections');general.append(p)
    full=[]
    for support in combinations(range(4),3):
        for p in general:
            q=[]
            for normal in p:
                vector=[0]*4
                for j,v in zip(support,normal):vector[j]=v
                q.append([vector,0])
            full.append(sorted(q))
    full=sorted(full);E.need(len({digest(p) for p in full})==36,'36 distinct A5 pencils')
    residual=json.loads(Path(residual_path).read_text())
    E.need(digest(residual)==EXPECTED_RESIDUAL,'pinned h4195 residual')
    selected=[[i,p] for i,p in enumerate(residual['remaining_pencil_signatures'])
              if all(c==0 for n,c in p) and len({j for n,c in p for j,v in enumerate(n) if v})==3]
    E.need(len(selected)==24 and all(p in full for i,p in selected),'all24 residual H3 pencils')
    return {'schema':'hn-three-power-pencil-a5-interface-v1','source_residual_sha256':EXPECTED_RESIDUAL,
            'all_a5_pencils':full,'remaining_h4195_index_pencil':selected,'all_a5_lifts':4608,
            'remaining_h4195_lifts':3072,'claim':'physical nonconcurrence; no global allowance update'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--residual',type=Path,required=True);parser.add_argument('--out',type=Path);parser.add_argument('--check-expected',action='store_true');args=parser.parse_args()
    output=run(args.residual)
    if args.out:args.out.write_text(json.dumps(output,sort_keys=True,separators=(',',':'))+'\n')
    if args.check_expected:E.need(output==json.loads((Path(__file__).parent/'A5_INTERFACE.json').read_text()),'interface mismatch')
    print(json.dumps({'status':'PASS','all_pencils':36,'residual_pencils':24,'all_lifts':4608,'residual_lifts':3072,'interface_sha256':digest(output)},sort_keys=True))
