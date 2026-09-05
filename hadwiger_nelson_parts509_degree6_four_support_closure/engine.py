#!/usr/bin/env python3
"""Exact witnesses and direct PB instances for four fixed single extensions."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
SELECTION=[637,643,675,689]


def require(ok,detail):
    if not ok:raise ValueError(detail)


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def encode(old,hitting,degree):
    R=old['free'];var={v:i+1 for i,v in enumerate(R)}
    rows=[({v:1 for v in sorted(old['family'][i]['D'])},1) for i in hitting]
    rows += [({v:1 for v in old['pool']},3),({v:-1 for v in R},-56)]
    for entry in degree:
        coeff={v:1 for v in entry['free_neighbors']};rhs=entry['need'] if entry['fixed'] else 0
        if not entry['fixed']:coeff[entry['v']]=-entry['need']
        rows.append((coeff,rhs))
    lines=[' '.join(f'{c:+d} x{var[v]}' for v,c in coeff.items())+f' >= {rhs} ;' for coeff,rhs in rows]
    return (f'* #variable= {len(R)} #constraint= {len(rows)} #equal= 0 intsize= 8\n'+'\n'.join(lines)+'\n').encode()


def compute():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for path,digest in manifest['inputs'].items():
        require(sha256((REPO/path).read_bytes()).hexdigest()==digest,('input hash',path))
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    bp=REPO/'hadwiger_nelson_parts509_degree7_extension610';sys.path.insert(0,str(bp))
    try:base=load('base_exact',bp/'verify.py')
    finally:sys.path.pop(0)
    _,ed,den,points,_=base.geometry(old);ed=[e for e in ed if e[1]!=610]
    field=load('integer_field',REPO/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py')
    require(len(old['forced'])==451 and set(old['forced'])<=set(range(509)),'forced originals')
    require(old['free']==sorted(set(old['vertices'])-set(old['forced'])),'free partition')
    family=[set(r['D']) for r in old['family']]
    require(all(D and D<=set(old['free']) for D in family),'killing set labels')
    minimal=[i for i,D in enumerate(family) if not any(E<D for E in family)]
    require(len(minimal)==337,'minimal killing rows')
    library={('forced',v):[old['forced_witness'][str(v)]] for v in old['forced']}
    library.update({('kill',i):[old['family'][i]['witness']] for i in minimal})
    for row in json.loads((REPO/'hadwiger_nelson_parts509_degree6_lift_family/catalogue.json').read_text()):
        key=row['kind'],row['key'];require(key in library and row['index']==len(library[key]),'catalogue index')
        library[key].append(row['witness'])
    decoded={}
    for (kind,key),witnesses in library.items():
        D={key} if kind=='forced' else family[key];labels=[v for v in old['vertices'] if v not in D]
        for i,c in enumerate(witnesses):decoded[kind,key,i]=dict(zip(labels,c,strict=True))
    published=json.loads((REPO/'hadwiger_nelson_parts509_degree6_lift_family/expected.json').read_text())
    facts=[];instances={};graphs={}
    for q in SELECTION:
        vertices=old['vertices']+[q]
        require(len({points[v] for v in vertices})==586,'coordinate collision')
        N=[v for v in old['vertices'] if field.squared_distance(points[v],points[q])==(den*den,)+(0,)*7]
        edges=ed+[(v,q) for v in N];adj={v:set() for v in vertices}
        for a,b in edges:adj[a].add(b);adj[b].add(a)
        selected=[];missing=[];checks=0
        for (kind,key),witnesses in library.items():
            D={key} if kind=='forced' else family[key]
            for i,c in enumerate(witnesses):
                available=sorted(set('0123')-{decoded[kind,key,i][v] for v in N if v in decoded[kind,key,i]})
                if available:
                    checks+=base.proper(vertices,edges,D,c+available[0]);selected.append([kind,key,i,available[0]]);break
            else:missing.append([kind,key])
        M=[key for kind,key in missing if kind=='kill']
        require(all(kind=='kill' for kind,key in missing),'forced witness coverage')
        prior=next(r for r in published['coverage'] if r['q']==q)
        require(M==prior['missing_killing'] and N==prior['neighbors'],'published fixed-library coverage')
        first,key,i,c=selected[0];require(first=='forced','first forced witness')
        five=dict(decoded['forced',key,i]);five[key]='4';five[q]=c
        five_checks=base.proper(vertices,edges,[],''.join(five[v] for v in vertices),'01234')
        F=set(old['forced'])|{q};R=set(old['free']);degree=[]
        for v in vertices:
            need=4-len(adj[v]&F)
            if need>0:degree.append(dict(v=v,fixed=v in F,need=need,free_neighbors=sorted(adj[v]&R)))
        require(degree==[
            dict(v=184,fixed=False,need=2,free_neighbors=[13,14,125,126]),
            dict(v=185,fixed=False,need=2,free_neighbors=[14,15,126,127]),
            dict(v=186,fixed=False,need=2,free_neighbors=[13,15,125,127])],'complete degree inventory')
        hitting=[i for i in minimal if i not in M];opb=encode(old,hitting,degree)
        require(sha256(opb).hexdigest()==manifest['instances'][str(q)]['OPB_sha256'],'instance identity')
        require((HERE/'instances'/f'{q}.opb').read_bytes()==opb,'committed instance differs')
        instances[q]=opb;graphs[q]=(adj,F,R,degree)
        facts.append(dict(q=q,vertices=len(vertices),unit_edges=len(edges),coordinates_numerator=points[q],
                          denominator=den,neighbors=N,forced_witnesses=451,killing_witnesses=len(hitting),
                          retained_edge_checks=checks,five_colour_edge_checks=five_checks,
                          edge_sha256=sha256(''.join(f'{a},{b}\n' for a,b in edges).encode()).hexdigest(),
                          selected_witness_sha256=sha256(json.dumps(selected,separators=(',',':')).encode()).hexdigest(),
                          missing_killing=M,degree_obligations=degree,OPB_variables=134,
                          OPB_constraints=len(hitting)+5,OPB_sha256=sha256(opb).hexdigest(),
                          OPB_bytes=len(opb)))
    # JSON normalization makes tuple-based exact coordinate rows reproducible.
    return json.loads(json.dumps(facts)),instances,graphs
