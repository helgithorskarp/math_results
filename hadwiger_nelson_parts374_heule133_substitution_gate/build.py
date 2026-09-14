#!/usr/bin/env python3
"""Reconstruct the selected support from pinned upstream coordinates."""
import argparse
import hashlib
import importlib.util
import json
import urllib.request
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent

def require(ok,message):
    if not ok: raise ValueError(message)

def main(directory,download):
    manifest=json.loads((HERE/'inputs.json').read_text())
    for name,h in manifest['inputs'].items():
        require(hashlib.sha256((REPO/name).read_bytes()).hexdigest()==h,'input hash: '+name)
    spec=importlib.util.spec_from_file_location('native',REPO/'hadwiger_nelson_heule_catalogue_atoms/native.py')
    native=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    upstream=json.loads((REPO/'hadwiger_nelson_heule_catalogue_atoms/inputs.json').read_text())
    if download: directory.mkdir(parents=True,exist_ok=True)
    for item in upstream['sources']:
        path=directory/item['name']
        if download and not path.exists():
            url=item['url'].replace('/master/','/'+upstream['source_commit']+'/')
            data=urllib.request.urlopen(url,timeout=30).read()
            require(hashlib.sha256(data).hexdigest()==item['sha256'],'download hash')
            path.write_bytes(data)
    paths=native.source_files(directory)
    sources=[set(native.parse(p.read_text())) for p in paths]
    h553=sources[3]
    small={p for p in h553 if any(p[k] for k in native.SQRT5_POSITIONS)}
    table=(REPO/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_text()
    rows=[tuple(map(int,line.split())) for line in table.splitlines() if not line.startswith('#')]
    require(len(rows)==509 and all(len(p)==16 for p in rows),'Parts table shape')
    parts=[tuple(3*x for x in p) for p in rows]
    large=set(parts[:374])
    require(len(h553)==553 and len(small)==133 and len(large)==374,'source partition')
    require(all(not any(p[k] for k in native.SQRT5_POSITIONS) for p in large),'large sigma5 membership')
    require(not large&small,'block disjointness')
    points=sorted(large|small)
    require(points==[tuple(p) for p in json.loads((HERE/'points.json').read_text())],'every published point matches source')
    sigma=lambda p:tuple(-x if i in native.SQRT5_POSITIONS else x for i,x in enumerate(p))
    switch=set(parts)|{sigma(p) for p in parts[374:]}
    result={'all_checks':True,'parts_large':374,'native_heule_small_without_origin':133,'points':len(points),
            'outside_native_catalogue_host':len(set(points)-set.union(*sources)),
            'outside_parts_switching_host':len(set(points)-switch),'every_point_matches':True}
    require(result['outside_native_catalogue_host']==15 and result['outside_parts_switching_host']==17,'containment gate')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--inputs',type=Path,required=True)
    ap.add_argument('--download',action='store_true')
    a=ap.parse_args()
    main(a.inputs,a.download)
