#!/usr/bin/env python3
"""Exact graph and positive witnesses; optional independent full-graph DRAT check."""
import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def compute():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for name,digest in manifest['inputs'].items():
        require(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input hash',name))
    raw=(HERE/'certificate.json').read_bytes()
    require(sha256(raw).hexdigest()==manifest['certificate_sha256'],'certificate hash')
    cert=json.loads(raw)
    path=REPO/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py'
    spec=importlib.util.spec_from_file_location('audited_integer_geometry',path)
    geometry=importlib.util.module_from_spec(spec);spec.loader.exec_module(geometry)
    den,points,all_labels,U,all_edges=geometry.read_geometry()
    selected=cert['pool_labels']
    require(selected==sorted(set(selected)) and set(selected)<=set(U),'selected pool labels')
    labels=list(range(374))+selected
    require(len({points[v] for v in labels})==len(labels),'distinct points')
    H=set(labels)
    edges=[(a,b) for a,b in all_edges if a in H and b in H]
    position={v:i for i,v in enumerate(labels)}
    five=cert['five_colouring']
    require(len(five)==len(labels) and set(five)<=set('01234'),'five-colouring format')
    require(all(five[position[a]]!=five[position[b]] for a,b in edges),'five-colouring edge')
    table=json.loads((REPO/'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())
    left=[r['witness_colouring_L'] for r in table['classes']]
    require(len(cert['deletions'])==len(selected),'deletion count')
    require([r['vertex'] for r in cert['deletions']]==selected,'deletion label order')
    checked_edges=0
    for row in cert['deletions']:
        v=row['vertex'];p=row['pattern'];c=row['pool_colours']
        require(type(p) is int and 0<=p<len(left),'L witness index')
        require(len(left[p])==374 and set(left[p])<=set('0123'),'L witness format')
        require(len(c)==len(selected) and set(c)<=set('.0123'),'pool witness format')
        require([selected[i] for i,x in enumerate(c) if x=='.']==[v],'one omitted vertex')
        full=left[p]+c
        require(all(full[position[a]]!=full[position[b]] for a,b in edges if v not in (a,b)),
                ('deletion-colouring edge',v))
        checked_edges+=sum(v not in e for e in edges)
    degree=Counter(v for e in edges for v in e)
    require(min(degree[v] for v in selected)>=4,'selected minimum degree')
    triangle=[0,149,152]
    require(all(tuple(sorted(e)) in edges for e in itertools.combinations(triangle,2)),
            'symmetry triangle edges')
    rows=[[4*i+c+1 for c in range(4)] for i in range(len(labels))]
    rows += [[-(4*position[a]+c+1),-(4*position[b]+c+1)]
             for a,b in edges for c in range(4)]
    rows += [[4*position[v]+c+1] for c,v in enumerate(triangle)]
    cnf=(f'p cnf {4*len(labels)} {len(rows)}\n'+
         ''.join(' '.join(map(str,row))+' 0\n' for row in rows)).encode()
    facts=dict(vertices=len(labels),edges=len(edges),fixed_L_vertices=374,
               selected_pool_vertices=len(selected),selected_S=sum(v<509 for v in selected),
               selected_Q5=sum(v>=509 for v in selected),omitted_S=[v for v in range(374,509) if v not in H],
               coordinate_denominator=den,
               edge_sha256=sha256(''.join(f'{a},{b}\n' for a,b in edges).encode()).hexdigest(),
               five_colouring_verified=True,pool_deletion_colourings_verified=len(selected),
               deletion_edge_checks=checked_edges,
               minimum_pool_degree=min(degree[v] for v in selected),
               minimum_L_degree=min(degree[v] for v in range(374)),
               cnf_variables=4*len(labels),cnf_clauses=len(rows),
               cnf_sha256=sha256(cnf).hexdigest(),
               interface_class_completeness_required_for_certificate=False)
    return facts,cnf


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--cnf',type=Path)
    ap.add_argument('--proof',type=Path)
    ap.add_argument('--drat-trim',type=Path)
    args=ap.parse_args()
    require(bool(args.proof)==bool(args.drat_trim),'supply both proof and checker')
    facts,cnf=compute()
    require(facts==json.loads((HERE/'expected.json').read_text()),'expected graph facts differ')
    if args.cnf:
        args.cnf.write_bytes(cnf)
    result=dict(facts=facts,non_four_colourability_checked=False,
                status='POSITIVE COLOURINGS AND EXACT CNF VERIFIED; NON-FOUR-COLOURABILITY NOT CHECKED')
    if args.proof:
        with tempfile.TemporaryDirectory(prefix='parts574-check-') as directory:
            path=Path(directory)/'core4.cnf';path.write_bytes(cnf)
            check=subprocess.run([str(args.drat_trim.resolve()),str(path),str(args.proof.resolve())],
                                 capture_output=True,text=True)
        require(check.returncode==0 and 's VERIFIED' in check.stdout,'DRAT verification failed')
        result.update(non_four_colourability_checked=True,
                      status='574-VERTEX GRAPH AND ALL 200 POOL DELETIONS VERIFIED',
                      proof_sha256=sha256(args.proof.read_bytes()).hexdigest())
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
