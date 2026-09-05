#!/usr/bin/env python3
"""Exact simultaneous rigid-block ambient and activation CNF."""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations,permutations
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def require(ok,detail):
    if not ok:raise ValueError(detail)


def load(path):
    spec=importlib.util.spec_from_file_location('integer_field',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def build():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for name,digest in manifest['inputs'].items():
        require(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input hash',name))
    raw=json.loads((REPO/'hadwiger_nelson_parts509_swap_closure/completion_points.json').read_text())
    original=[]
    for line in (REPO/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_text().splitlines():
        if not line or line.startswith('#'):continue
        row=list(map(int,line.split()));require(len(row)==16,'original coordinate width')
        original.append((tuple(3*x for x in row[:8]),tuple(3*x for x in row[8:])))
    require(len(original)==509,'original point count')
    points=list(original);added=[]
    for i,row in enumerate(raw['points']):
        xy=[]
        for axis in ['x','y']:
            scaled=[Fraction(c)*288 for c in row[axis]]
            require(all(c.denominator==1 for c in scaled),'integer scaling')
            xy.append(tuple(c.numerator for c in scaled))
        points.append(tuple(xy))
        if all(xy[a][j]==0 for a in [0,1] for j in [2,3,6,7]) and len(row['neighbors'])>=4:added.append(509+i)
    original_L=[v for v in range(509) if all(points[v][a][j]==0 for a in [0,1] for j in [2,3,6,7])]
    require(original_L==list(range(374)) and len(added)==602,'ambient selection')
    vertices=original_L+added;require(len({points[v] for v in vertices})==976,'ambient collisions')
    field=load(REPO/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py')
    unit=(288*288,)+(0,)*7
    edges=[(u,v) for u,v in combinations(vertices,2) if field.squared_distance(points[u],points[v])==unit]
    require(sum(v<374 for u,v in edges)==1860,'original L edges')
    # Independently verify the degree predicate used to seal the new-point list.
    incidences=0
    for v in added:
        neighbours=[u for u in range(509) if field.squared_distance(points[u],points[v])==unit]
        require(neighbours==raw['points'][v-509]['neighbors'] and len(neighbours)>=4,'completion incidences')
        incidences+=509
    interface=json.loads((REPO/'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())
    I=interface['interface_L'];In=interface['interface_L_nonorigin']
    require(I==[0]+In and len(I)==19 and interface['class_count']==len(interface['classes'])==20,'interface dimensions')
    allowed=sorted({tuple(p[int(c)] for c in row['class']) for row in interface['classes'] for p in [(0,)+p for p in permutations([1,2,3])]})
    require(len(allowed)==120 and all(len(p)==18 for p in allowed),'complete colour orbits')
    for row in interface['classes']:
        colours=row['witness_colouring_L'];require(len(colours)==374 and colours[0]=='0','old witness format')
        require(all(colours[u]!=colours[v] for u,v in edges if v<374),'old L witness')
        require(tuple(map(int,(colours[v] for v in In))) in allowed,'old witness pattern')
    pos={v:i for i,v in enumerate(vertices)}
    colour=lambda v,c:4*pos[v]+c+1
    activation={v:4*len(vertices)+i+1 for i,v in enumerate(vertices)}
    clauses=[[-activation[v]]+[colour(v,c) for c in range(4)] for v in vertices]
    clauses += [[-colour(u,c),-colour(v,c)] for u,v in edges for c in range(4)]
    clauses += [[activation[v]] for v in I]+[[colour(0,0)]]
    clauses += [[-colour(v,c) for v,c in zip(In,p,strict=True)] for p in allowed]
    adj={v:set() for v in vertices}
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    degree_new={v:len(adj[v]&set(added)) for v in original_L}
    omit=min(set(original_L)-set(I),key=lambda v:(-degree_new[v],v))
    facts=dict(ambient_vertices=len(vertices),ambient_edges=len(edges),old_L_vertices=374,new_vertices=len(added),
               interface=I,allowed_patterns=120,denominator=288,selected_new_labels=added,
               exact_completion_incidence_checks=incidences,seed_omission=omit,seed_omission_new_neighbours=degree_new[omit],
               activation_variables=5*len(vertices),activation_clauses=len(clauses),
               ambient_edge_sha256=sha256(''.join(f'{u},{v}\n' for u,v in edges).encode()).hexdigest())
    return dict(vertices=vertices,edges=edges,points=points,adj=adj,interface=I,nonorigin=In,
                allowed=allowed,activation=activation,colour=colour,clauses=clauses,omit=omit,degree_new=degree_new,facts=facts)


def direct_cnf(data,selected):
    vertices=sorted(selected);pos={v:i for i,v in enumerate(vertices)}
    edges=[(u,v) for u,v in data['edges'] if u in pos and v in pos]
    var=lambda v,c:4*pos[v]+c+1
    clauses=[[var(v,c) for c in range(4)] for v in vertices]
    clauses += [[-var(u,c),-var(v,c)] for u,v in edges for c in range(4)]
    clauses += [[var(0,0)]]
    clauses += [[-var(v,c) for v,c in zip(data['nonorigin'],p,strict=True)] for p in data['allowed']]
    raw=(f'p cnf {4*len(vertices)} {len(clauses)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in clauses)).encode()
    return raw,vertices,edges


def check_model(data,selected,model):
    positive={v for v in model if v>0};colours={v:next(c for c in range(4) if data['colour'](v,c) in positive) for v in selected}
    require(colours[0]==0 and set(data['interface'])<=set(selected),'mandatory boundary')
    require(all(colours[u]!=colours[v] for u,v in data['edges'] if u in colours and v in colours),'decoded graph colouring')
    pattern=tuple(colours[v] for v in data['nonorigin'])
    require(pattern not in data['allowed'],'decoded colouring must leave the allowed interface relation')
    return dict(labels=sorted(selected),colouring=''.join(str(colours[v]) for v in sorted(selected)),interface_pattern=list(pattern))
