#!/usr/bin/env python3
"""Verify lifted positive evidence and a full-graph negative certificate.

The degree-seven hitting bound and earlier small-augmentation closures are
explicit imported theorem dependencies, not re-proved by this entrypoint.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from math import lcm
from pathlib import Path
import subprocess
import tempfile
from build_residual import compute as residual_cnf

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def require(ok, detail):
    if not ok:raise ValueError(detail)


def geometry(old):
    path=REPO/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py'
    spec=importlib.util.spec_from_file_location('integer_field',path)
    field=importlib.util.module_from_spec(spec);spec.loader.exec_module(field)
    originals=[]
    for line in (REPO/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_text().splitlines():
        if not line or line.startswith('#'):continue
        row=list(map(int,line.split()));require(len(row)==16,'original point width')
        originals.append((row[:8],row[8:]))
    raw=json.loads((REPO/'hadwiger_nelson_parts509_swap_closure/completion_points.json').read_text())
    completion=[];den=96
    for row in raw['points']:
        point=tuple(tuple(Fraction(x) for x in row[axis]) for axis in ('x','y'))
        require(all(len(axis)==8 for axis in point),'completion width')
        for axis in point:
            for x in axis:den=lcm(den,x.denominator)
        completion.append(point)
    require(len(originals)==509 and len(completion)==1158 and den==288,'coordinate dimensions')
    points=[tuple(tuple(x*(den//96) for x in axis) for axis in p) for p in originals]
    points += [tuple(tuple(int(x*den) for x in axis) for axis in p) for p in completion]
    require(points[610]==((-120,0,0,0,0,-24,0,0),(0,120,0,0,-24,0,0,0)),
            'displayed radical coordinates of point610')
    require(old['vertices']==list(range(585)) and old['pool']==list(range(509,585)),'old label sets')
    require([509+i for i,row in enumerate(raw['points']) if len(row['neighbors'])>=7]==old['pool'],'pool/census indexing')
    for v in old['vertices']:
        imported=tuple(tuple(Fraction(a) for a in axis) for axis in old['coordinates'][str(v)])
        require(all(Fraction(points[v][i][j],den)==imported[i][j] for i in range(2) for j in range(8)),('old coordinate',v))
    vertices=old['vertices']+[610]
    require(len({points[v] for v in vertices})==586,'coordinate collision')
    target=(den*den,)+(0,)*7
    edges=[(a,b) for a,b in combinations(vertices,2) if field.squared_distance(points[a],points[b])==target]
    require(len(edges)==3089,'new edge count')
    require([a for a,b in edges if b==610]==[0,1,63,163,171,198],'new point neighbourhood')
    require(sum(b!=610 for a,b in edges)==3083,'old edge count')
    require(sum(b<509 for a,b in edges)==2442,'original Parts edge count')
    return vertices,edges,den,points,raw


def proper(vertices, edges, D, witness, palette='0123'):
    keep=[v for v in vertices if v not in set(D)]
    require(len(witness)==len(keep) and set(witness)<=set(palette),'witness format')
    colours=dict(zip(keep,witness,strict=True));checked=0
    for a,b in edges:
        if a in colours and b in colours:
            require(colours[a]!=colours[b],('monochromatic edge',a,b,D));checked+=1
    return checked


def old_opb(old):
    R=old['free'];var={v:i+1 for i,v in enumerate(R)}
    family=[sorted(row['D']) for row in old['family']]
    keys=set(frozenset(D) for D in family)
    minimal=[D for D in family if not any(K < frozenset(D) for K in keys)]
    require(len(minimal)==337,'old minimal killing family')
    lines=[' '.join(f'+1 x{var[v]}' for v in D)+' >= 1 ;' for D in minimal]
    lines.append(' '.join(f'+1 x{var[v]}' for v in old['pool'])+' >= 4 ;')
    lines.append(' '.join(f'-1 x{var[v]}' for v in R)+' >= -57 ;')
    return (f'* #variable= {len(R)} #constraint= {len(lines)} #equal= 0 intsize= 8\n'+'\n'.join(lines)+'\n').encode()


def compute():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for name,digest in manifest['inputs'].items():
        require(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input hash',name))
    raw=(HERE/'certificate.json').read_bytes()
    require(sha256(raw).hexdigest()==manifest['certificate_sha256'],'certificate hash')
    cert=json.loads(raw)
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    vertices,edges,den,_,_=geometry(old)
    require(cert['added_point']==610 and cert['excluded_killing_indices']==[188],'selected extension')
    require(cert['neighbors_of_added_point']==[0,1,63,163,171,198],'neighbour certificate')
    require(old['forced']==sorted(set(old['forced'])) and len(old['forced'])==451,'forced labels')
    require(old['free']==sorted(set(old['vertices'])-set(old['forced'])),'free labels')
    require(old['family'][188]['D']==[15,23] and len(old['family'])==425,'omitted killing row')
    require(set(old['forced'])<=set(range(509)),'forced vertices original')
    replacements={(r['kind'],r['key']):r['witness'] for r in cert['replacement_witnesses']}
    require(len(replacements)==len(cert['replacement_witnesses'])==3,'replacement count')
    require(set(replacements)=={('forced','44'),('forced','56'),('kill','94')},'replacement coverage')
    require(len(cert['forced_append'])==451 and len(cert['killing_append'])==425,'append lengths')
    checks=0
    for i,v in enumerate(old['forced']):
        c=cert['forced_append'][i]
        if c=='.':witness=replacements[('forced',str(v))]
        else:
            require(c in '0123','appended colour');witness=old['forced_witness'][str(v)]+c
        checks+=proper(vertices,edges,[v],witness)
    for i,row in enumerate(old['family']):
        D=row['D'];require(D==sorted(set(D)) and set(D)<=set(old['free']),'killing set labels')
        if i==188:
            require(cert['killing_append'][i]=='.','omitted marker');continue
        c=cert['killing_append'][i]
        if c=='.':witness=replacements[('kill',str(i))]
        else:
            require(c in '0123','appended colour');witness=row['witness']+c
        checks+=proper(vertices,edges,D,witness)
    proper(vertices,edges,[],cert['five_colouring'],'01234')
    require(cert['non_four_colourable_deletion']==[15,23],'negative graph deletion')
    labels=[v for v in vertices if v not in (15,23)];pos={v:i for i,v in enumerate(labels)}
    ee=[(a,b) for a,b in edges if a in pos and b in pos]
    triangle=[0,149,152]
    require(all(tuple(sorted(e)) in ee for e in combinations(triangle,2)),'negative pin triangle')
    rows=[[4*i+c+1 for c in range(4)] for i in range(len(labels))]
    rows += [[-(4*pos[a]+c+1),-(4*pos[b]+c+1)] for a,b in ee for c in range(4)]
    rows += [[4*pos[v]+c+1] for c,v in enumerate(triangle)]
    cnf=(f'p cnf {4*len(labels)} {len(rows)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in rows)).encode()
    pb=old_opb(old)
    require(sha256(pb).hexdigest()=='03dfd3601258be7899c607696b96bf9b0ddba77784db404cca045e7b8dfdda9d','imported bound OPB')
    residual,meta=residual_cnf(old)
    facts=dict(vertices=586,unit_edges=3089,denominator=den,
               edge_sha256=sha256(''.join(f'{a},{b}\n' for a,b in edges).encode()).hexdigest(),
               forced_vertices_verified=451,killing_sets_verified=424,retained_edge_checks=checks,
               positive_replacements=3,five_colouring_verified=True,
               negative_graph_vertices=len(labels),negative_graph_edges=len(ee),
               negative_cnf_variables=4*len(labels),negative_cnf_clauses=len(rows),
               negative_cnf_sha256=sha256(cnf).hexdigest(),
               old_bound_opb_sha256=sha256(pb).hexdigest(),old_bound_proof_rechecked=False,
               residual_variables=meta['variables'],residual_clauses=meta['clauses'],
               residual_sha256=meta['sha256'],residual_raw_support_pairs=meta['raw_support_pairs'],
               graph_order_lower_bound_with_imported_theorems=508,
               graph_order_upper_bound_with_imported_Parts_graph=509,
               residual_formula_solved=False)
    return facts,cnf,residual,pb


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--negative-cnf',type=Path)
    ap.add_argument('--residual-cnf',type=Path);ap.add_argument('--old-opb',type=Path)
    ap.add_argument('--proof',type=Path);ap.add_argument('--drat-trim',type=Path)
    args=ap.parse_args();require(bool(args.proof)==bool(args.drat_trim),'proof and checker must be supplied together')
    facts,cnf,residual,pb=compute()
    require(facts==json.loads((HERE/'expected.json').read_text()),'expected facts differ')
    for path,data in [(args.negative_cnf,cnf),(args.residual_cnf,residual),(args.old_opb,pb)]:
        if path:path.write_bytes(data)
    result=dict(facts=facts,negative_barrier_checked=False,
                status='NEW POSITIVE EVIDENCE AND FORMULAS VERIFIED; DEGREE-SEVEN THEOREMS IMPORTED')
    if args.proof:
        with tempfile.TemporaryDirectory(prefix='degree7-lift-check-') as directory:
            path=Path(directory)/'negative.cnf';path.write_bytes(cnf)
            check=subprocess.run([str(args.drat_trim.resolve()),str(path),str(args.proof.resolve())],capture_output=True,text=True)
        require(check.returncode==0 and 's VERIFIED' in check.stdout,'negative proof rejected')
        result.update(negative_barrier_checked=True,
                      status='NEW POSITIVE EVIDENCE AND FIVE-CHROMATIC LIFTING BARRIER VERIFIED; DEGREE-SEVEN THEOREMS IMPORTED')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
