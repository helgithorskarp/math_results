#!/usr/bin/env python3
"""Exact cardinality gate; no edge reconstruction or chromatic claim."""
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

def reflect(p):
    return p[:8]+tuple(-a for a in p[8:])

def count_orbits(points):
    require(len(points)==len(set(points)), 'duplicate source point')
    source=set(points)
    closure=source|{reflect(p) for p in source}
    fixed=sum(reflect(p)==p for p in closure)
    # Burnside's lemma on the reflection-closed support.
    require((len(closure)+fixed)%2==0,'orbit parity')
    return (len(closure)+fixed)//2,len(closure),fixed

def load_parser(relative,alias,pin):
    path=REPO/relative
    require(hashlib.sha256(path.read_bytes()).hexdigest()==pin,'parser hash')
    spec=importlib.util.spec_from_file_location(alias,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def verify(path,download):
    manifest=json.loads((HERE/'inputs.json').read_text())
    if download and not path.exists():
        data=urllib.request.urlopen(manifest['source_url'],timeout=30).read()
        require(hashlib.sha256(data).hexdigest()==manifest['source_file_sha256'],'download hash')
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
    data=path.read_bytes()
    require(len(data)==manifest['source_file_bytes'],'input size')
    require(hashlib.sha256(data).hexdigest()==manifest['source_file_sha256'],'input hash')
    parsers={name:load_parser(name,'reflection_'+str(i),pin) for i,(name,pin) in enumerate(manifest['parser_pins'].items())}
    dense=parsers['hadwiger_nelson_heule_catalogue_atoms/native.py'].parse(data.decode())
    sparse=parsers['hadwiger_nelson_heule_catalogue_atoms/verify.py'].read_points(data.decode())
    require(dense==sparse,'entrywise source parser comparison')
    require(len(sparse)==610,'source order')
    n,closure,fixed=count_orbits(sparse)
    # Separate direct accounting: only two-sided source pairs save a point.
    source=set(dense)
    pairs=sorted((p,reflect(p)) for p in dense if p<reflect(p) and reflect(p) in source)
    require(len(dense)-len(pairs)==n,'direct pair versus Burnside count')
    representatives=sorted({min(p,reflect(p)) for p in sparse})
    require(len(representatives)==n,'explicit minimum-image transversal')
    return {'all_checks':True,'source_vertices':610,'reflection_closure_vertices':closure,
            'axis_points':fixed,'source_mirror_pairs':len(pairs),'source_orbits':n,
            'unconstrained_minimum_images':n,'edge_preserving_minimum_lower_bound':n,
            'edge_preserving_minimum_exact_value_known':False,'target':508,'target_possible':n<=508,
            'complete_source_points_compared_entrywise':True,
            'point_sha256':hashlib.sha256((json.dumps(sparse,separators=(',',':'))+'\n').encode()).hexdigest(),
            'transversal_sha256':hashlib.sha256((json.dumps(representatives,separators=(',',':'))+'\n').encode()).hexdigest(),
            'new_edges_or_colourings_computed':False,'record_candidate':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',type=Path,required=True)
    ap.add_argument('--download',action='store_true')
    a=ap.parse_args()
    result=verify(a.input,a.download)
    if (HERE/'expected.json').exists():require(result==json.loads((HERE/'expected.json').read_text()),'expected result')
    print(json.dumps(result,sort_keys=True))
