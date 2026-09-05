#!/usr/bin/env python3
"""Replay exact positive evidence and check the compact VeriPB closure."""
import argparse
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from encoding import HERE,REPO,encode


def require(ok,detail):
    if not ok:raise ValueError(detail)


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def opb_rows(data):
    lines=data.decode('ascii').splitlines()
    require(lines[0]=='* #variable= 134 #constraint= 340 #equal= 0 intsize= 8','OPB header')
    result=[]
    for line in lines[1:]:
        lhs,rhs=line.split(' >= ');require(rhs.endswith(' ;'),'OPB terminator')
        words=lhs.split();require(len(words)%2==0,'OPB term width');terms={}
        for c,v in zip(words[::2],words[1::2],strict=True):
            require(re.fullmatch(r'x[1-9][0-9]*',v),'OPB variable')
            v=int(v[1:]);require(1<=v<=134 and v not in terms,'OPB variable range or duplicate')
            terms[v]=int(c)
        result.append((terms,int(rhs[:-2])))
    require(len(result)==340,'OPB row count');return result


def geometry_audit(old,prior):
    # Parse the independently pinned old coordinate dictionary directly.
    points={v:tuple(tuple(Fraction(x) for x in axis) for axis in old['coordinates'][str(v)])
            for v in old['vertices']}
    points[613]=((Fraction(-5,6),)+(Fraction(0),)*7,
                 (Fraction(0),)*4+(Fraction(1,6),)+(Fraction(0),)*3)
    scaled={v:tuple(tuple(int(x*288) for x in axis) for axis in p) for v,p in points.items()}
    require(all(Fraction(scaled[v][i][j],288)==points[v][i][j] for v in points for i in range(2) for j in range(8)),
            'integer scaling exact')
    field=load('integer_distance',REPO/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py')
    vertices=old['vertices']+[613];adj={v:set() for v in vertices};edges=[]
    for i,a in enumerate(vertices):
        for b in vertices[i+1:]:
            if field.squared_distance(scaled[a],scaled[b])==(288**2,)+(0,)*7:
                edges.append((a,b));adj[a].add(b);adj[b].add(a)
    # The prior digest lists A7 edges first, followed by the six q edges.
    edges=[e for e in edges if e[1]!=613]+[e for e in edges if e[1]==613]
    digest=sha256(''.join(f'{a},{b}\n' for a,b in edges).encode()).hexdigest()
    require(digest==prior['edge_sha256'],'separate coordinate-source edge match')
    omitted=set(prior['omitted_vertices'])
    fixed=set(old['forced'])|set(prior['additional_forced_vertices'])|{613}
    optional=set(vertices)-fixed-omitted
    obligations=[]
    for v in vertices:
        if v in omitted:continue
        need=4-len(adj[v]&fixed)
        if need>0:obligations.append(dict(v=v,fixed_selected=v in fixed,needed=need,
                                        optional_neighbors=sorted(adj[v]&optional),
                                        fixed_neighbors=sorted(adj[v]&fixed),
                                        omitted_neighbors=sorted(adj[v]&omitted)))
    require(obligations==[
        dict(v=184,fixed_selected=True,needed=1,optional_neighbors=[14,126],
             fixed_neighbors=[125,148,155],omitted_neighbors=[13]),
        dict(v=185,fixed_selected=False,needed=1,optional_neighbors=[14,15,126],
             fixed_neighbors=[127,156,163],omitted_neighbors=[])],'degree audit')
    return dict(fixed_selected=len(fixed),fixed_omitted=len(omitted),optional=len(optional),
                trivial_degree_vertices=len(vertices)-len(omitted)-len(obligations),
                obligations=obligations,effective_degree_clause=[14,126],
                degree_clause_required_by_final_proof=False),adj,fixed,optional,omitted


def compute(checker):
    manifest=json.loads((HERE/'manifest.json').read_text())
    for path,digest in manifest['inputs'].items():
        require(sha256((REPO/path).read_bytes()).hexdigest()==digest,('input hash',path))
    for name,key in [('residual.opb','opb_sha256'),('closure.pb','proof_sha256')]:
        require(sha256((HERE/name).read_bytes()).hexdigest()==manifest[key],('local hash',name))
    prior_dir=REPO/'hadwiger_nelson_parts509_degree6_point613_residual'
    sys.path.insert(0,str(prior_dir))
    try:prior_module=load('prior_residual_verifier',prior_dir/'verify.py');prior,cnf,meta=prior_module.compute()
    finally:sys.path.pop(0)
    require(prior==json.loads((prior_dir/'expected.json').read_text()),'prior exact reduction replay')
    require(sha256(cnf).hexdigest()==manifest['prior_cnf_sha256'],'prior CNF identity')
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    opb=encode(old);require(opb==(HERE/'residual.opb').read_bytes(),'OPB regeneration')
    rows=opb_rows(opb);free=meta['free_vertices'];var={v:i+1 for i,v in enumerate(free)}
    # Independently decode every wire row against the prior selector metadata.
    for i,source_row in enumerate(meta['hitting_rows']):
        require(rows[i]==({var[v]:1 for v in old['family'][source_row]['D']},1),('hitting row',i))
    require(rows[335:339]==[({var[v]:-1},0) for v in meta['omitted_vertices']],'omission rows')
    require(rows[339]==({i:-1 for i in range(1,135)},-meta['maximum_free_vertices']),'selection budget')
    audit,_,_,_,_=geometry_audit(old,prior)
    with tempfile.TemporaryDirectory(prefix='hn613-closure-') as directory:
        instance=Path(directory)/'residual.opb';instance.write_bytes(opb)
        checked=subprocess.run([str(Path(checker).resolve()),str(instance),str(HERE/'closure.pb')],capture_output=True,text=True)
    require(checked.returncode==0 and 's VERIFIED UNSATISFIABLE' in checked.stdout,'VeriPB rejected closure')
    return dict(status='CLOSED THROUGH 508; MINIMUM FIVE-CHROMATIC SUBGRAPH ORDER 509',
                vertices=prior['vertices'],unit_edges=prior['unit_edges'],edge_sha256=prior['edge_sha256'],
                positive_four_colour_witnesses=prior['forced_witnesses']+prior['killing_witnesses'],
                retained_four_colour_edge_checks=prior['retained_edge_checks'],
                five_colouring_verified=prior['full_support_five_colouring_verified'],
                prior_cnf_sha256=manifest['prior_cnf_sha256'],opb_variables=134,opb_constraints=340,
                opb_sha256=manifest['opb_sha256'],proof_bytes=(HERE/'closure.pb').stat().st_size,
                proof_sha256=manifest['proof_sha256'],proof_checked=True,
                degree_audit=audit,proof_uses_degree_clause=False,original_residual_unsat=True,
                closure_through508=True,minimum_five_chromatic_subgraph_order=509,
                record_improvement=False,imported_old_degree7_proof_rechecked=False)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--veripb',type=Path,required=True);args=ap.parse_args()
    result=compute(args.veripb);require(result==json.loads((HERE/'expected.json').read_text()),'expected result differs')
    print(json.dumps(result,indent=2,sort_keys=True))
