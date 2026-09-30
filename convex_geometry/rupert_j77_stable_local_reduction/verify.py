#!/usr/bin/env python3
"""Exact stable-local reduction for J77; Python 3.11+, standard library."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'rupert_j77_fixed_outer_local'
BASE_COMMIT='11645dc3c95a20c41d08e5a8d8c28215b6838d88'


def require(condition,message):
    if not condition:raise ValueError(message)


def load_base():
    manifest=json.loads((ROOT/'dependencies.json').read_text())
    require(manifest['source_commit']==BASE_COMMIT,'unexpected dependency provenance')
    require(set(manifest['sha256'])=={'verify.py','q5.py','model.py','chamber.py','certificates.json','PROOF.md'},
            'incomplete dependency manifest')
    for name,digest in manifest['sha256'].items():
        require(hashlib.sha256((BASE/name).read_bytes()).hexdigest()==digest,'dependency bytes differ: '+name)
    sys.path.insert(0,str(BASE))
    spec=importlib.util.spec_from_file_location('j77_fixed_base',BASE/'verify.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


base=load_base()
from q5 import Q, cross, dot, sub
from chamber import partition, rotation
from model import VERTICES, C5


def projective(v):
    require(any(x!=0 for x in v),'zero projective direction')
    first=next(x for x in v if x!=0)
    return tuple(x/first for x in v)


def exceptional_directions():
    return {(Q(),Q(1),Q()),
            (Q(5,-3),Q(5,-1),Q(0,-2)),
            (Q(9,-7),Q(-5,13),Q(22,-8)),
            (Q(-16,6),Q(25,-7),Q(23,-11))}


def orbit(u):
    axis=(Q(),C5,Q(1));seen={projective(u)};pending=list(seen)
    while pending:
        v=pending.pop()
        for w in (rotation(v,axis,Q(-1,1)/4,Q(1)/2),(-v[0],v[1],v[2])):
            w=projective(w)
            if w not in seen:seen.add(w);pending.append(w)
    require(len(seen)<=10,'invalid C5v projective orbit')
    return seen


def coverage(data,bad_corners,bad_edges):
    directions=[base.decode(u) for u in data['exceptional_chamber_directions']]
    canonical={projective(u) for u in directions}
    require(len(directions)==len(canonical)==4 and canonical=={projective(u) for u in exceptional_directions()},
            'exceptional directions differ from the stated four rays')
    require(set(directions)<={u for p,u in bad_corners},'exceptional ray is not a mesh vertex')
    points=[(r['parent'],base.decode(r['direction'])) for r in data['points']]
    required_points={(p,u) for p,u in bad_corners if u not in set(directions)}
    require(len(points)==len(set(points)) and set(points)==required_points,
            'stable point coverage is incomplete, duplicate, or extraneous')
    edges=[(r['parent'],tuple(sorted(base.decode(u) for u in r['endpoints']))) for r in data['edges']]
    require(len(edges)==len(set(edges)) and set(edges)==bad_edges,
            'stable edge coverage is incomplete, duplicate, or extraneous')
    return directions


def point_certificate(record,parent,audit):
    u=base.decode(record['direction']);bases=record['bases'];weights_seen=[]
    require(u[1]>0,'invalid translation coordinate chart')
    require(len(bases)==6 and {(b['axis'],b['sign']) for b in bases}=={(k,s) for k in range(3) for s in (1,-1)},
            'missing signed rotation target')
    for b in bases:
        columns=[]
        for ids in b['contacts']:
            audit.contact(ids,parent,'full')
            a,z,j=ids;m=cross(sub(VERTICES[z],VERTICES[a]),u);h=dot(m,VERTICES[j])
            require(h>0,'zero limiting support probe')
            m=tuple(x/h for x in m);columns.append(cross(VERTICES[j],m)+m)
        target=[0]*6;target[b['axis']]=b['sign']
        weights=base.solve_equilibrium(columns,target)
        # The solver is absent: every coefficient is reconstructed exactly.
        audit.values.extend(weights);weights_seen.extend(weights)
    return weights_seen


def check(data,self_test=False):
    base.check_model();part=partition()
    parents=[tuple(base.decode(u) for u in t) for t in part['triangles']]
    original=json.loads((BASE/'certificates.json').read_text())
    canonical=hashlib.sha256(json.dumps(original,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    require(canonical=='92823c79eb47d8886031a6f4989406b6d50ec2693879802bcae4b4b5365c8781',
            'original certificate differs from the verified source')
    require(original['parent_cells_sha256']==part['cells_sha256'],'parent partition changed')
    base.leaf_paths(original,len(parents))
    audit=base.Audit();bad_corners=set();bad_edges=set()
    for leaf in original['leaves']:
        p=leaf['parent'];triangle=base.child_triangle(parents[p],leaf['path'])
        require(leaf['certificates'],'uncertified leaf interior')
        corners=[False]*3;edges=[False]*3
        for c in leaf['certificates']:
            cc,ee=audit.simplex(c,triangle,[p,leaf['path']])
            corners=[x or y for x,y in zip(corners,cc)];edges=[x or y for x,y in zip(edges,ee)]
        bad_corners.update((p,u) for u,yes in zip(triangle,corners) if not yes)
        for k,yes in enumerate(edges):
            if not yes:bad_edges.add((p,tuple(sorted(u for j,u in enumerate(triangle) if j!=k))))
    directions=coverage(data,bad_corners,bad_edges)
    old_counts=dict(audit.simplex_counts);old_coefficients=audit.coefficients
    weights=[]
    for r in data['points']:weights.extend(point_certificate(r,parents[r['parent']],audit))
    for i,r in enumerate(data['edges']):
        p=r['parent'];edge=tuple(sorted(base.decode(u) for u in r['endpoints']));c=r['certificate']
        # Support over the whole incident parent matters for approach from
        # its interior, rather than merely for sequences lying on the edge.
        for ids in c['contacts']:audit.contact(ids,parents[p],c['kind'])
        _,ee=audit.simplex(c,(edge[0],edge[1],edge[1]),['stable edge',p,i])
        require(ee[2],'open edge is not strictly covered')
    orbits=[orbit(u) for u in directions];union=set().union(*orbits)
    require([len(o) for o in orbits]==data['projective_orbit_sizes'],'incorrect orbit sizes')
    require(len(union)==25==data['projective_exceptional_axis_count'],'incorrect exceptional axis count')
    sign_count=base.independent_sign_audit(audit.values)
    digest=hashlib.sha256(json.dumps(audit.coefficient_records,separators=(',',':')).encode()).hexdigest()
    certificate_digest=hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if self_test:malformed_tests(data,bad_corners,bad_edges,parents)
    return {'agent':'six-rupert-2','role':'researcher',
            'claim_status':'stable_local_exclusion_away_from_25_J77_axes',
            'both_projection_directions_may_vary':True,'arbitrary_planar_translations':True,
            'scales_covered':'lambda >= 1','global_rupert_status_resolved':False,
            'exceptional_axes_asserted_to_admit_passages':False,'global_uniform_angle_claimed':False,
            'dependency_source_commit':BASE_COMMIT,'vertex_count':len(VERTICES),
            'projective_polygons':part['polygon_count'],'parent_triangles':len(parents),'leaf_triangles':len(original['leaves']),
            'original_leaf_simplex_counts':old_counts,'original_leaf_coefficients':old_coefficients,
            'original_bad_corner_parent_incidences':len(bad_corners),'original_bad_corner_rays':len({u for p,u in bad_corners}),
            'original_bad_open_edge_parent_incidences':len(bad_edges),
            'new_stable_point_parent_incidences':len(data['points']),'new_signed_rotation_equilibria':6*len(data['points']),
            'new_positive_equilibrium_weights':len(weights),'new_stable_edge_certificates':len(data['edges']),
            'new_edge_coefficients':audit.coefficients-old_coefficients,
            'exceptional_chamber_rays':len(directions),'projective_orbit_sizes':data['projective_orbit_sizes'],
            'exceptional_projective_axes':len(union),'support_comparisons':audit.comparisons,
            'nonnegative_cofactor_coefficients':audit.coefficients,'positive_cofactor_coefficients':audit.positive_coefficients,
            'independent_Leibniz_replays':audit.reference_replays,'independent_rational_sign_audits':sign_count,
            'canonical_certificate_sha256':certificate_digest,'exact_coefficients_sha256':digest}


def malformed_tests(data,bad_corners,bad_edges,parents):
    def copy():return json.loads(json.dumps(data))
    a=copy();a['points'].pop()
    b=copy();b['edges'].pop()
    c=copy();c['exceptional_chamber_directions'].pop()
    edge=copy()['edges'][0];x,y,j=edge['certificate']['contacts'][0];edge['certificate']['contacts'][0]=[y,x,j]
    point=copy()['points'][0];point['bases'].pop()
    failures=[lambda:coverage(a,bad_corners,bad_edges),lambda:coverage(b,bad_corners,bad_edges),
              lambda:coverage(c,bad_corners,bad_edges),
              lambda:base.Audit().contact(edge['certificate']['contacts'][0],parents[edge['parent']],edge['certificate']['kind']),
              lambda:point_certificate(point,parents[point['parent']],base.Audit())]
    for invalid in failures:
        try:invalid()
        except ValueError:pass
        else:raise ValueError('malformed certificate accepted')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args();data=json.loads((ROOT/'certificates.json').read_text())
    print(json.dumps(check(data,args.self_test),indent=2,sort_keys=True))
