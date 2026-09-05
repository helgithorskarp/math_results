#!/usr/bin/env python3
"""Exact necessary selectors with only witnessed vertices fixed."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
POINTS=[606,621,630]


def require(ok,detail):
    if not ok:raise ValueError(detail)


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def serialize(free,rows):
    var={v:i+1 for i,v in enumerate(free)}
    lines=[' '.join(f'{c:+d} x{var[v]}' for v,c in row.items())+f' >= {rhs} ;' for row,rhs in rows]
    return (f'* #variable= {len(free)} #constraint= {len(rows)} #equal= 0 intsize= 8\n'+'\n'.join(lines)+'\n').encode()


def compute():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for name,digest in manifest['inputs'].items():
        require(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input hash',name))
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    path=REPO/'hadwiger_nelson_parts509_degree7_extension610';sys.path.insert(0,str(path))
    try:base=load('geometry_base',path/'verify.py')
    finally:sys.path.pop(0)
    _,edges,den,points,_=base.geometry(old);edges=[e for e in edges if e[1]!=610]
    field=load('exact_field',REPO/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py')
    require(old['forced']==sorted(set(old['forced'])) and len(old['forced'])==451,'old fixed set')
    require(old['free']==sorted(set(old['vertices'])-set(old['forced'])),'old free partition')
    family=[set(row['D']) for row in old['family']]
    require(all(D and D<=set(old['free']) for D in family),'deletion set labels')
    minimal=[i for i,D in enumerate(family) if not any(E<D for E in family)]
    require(len(minimal)==337,'minimal row count')
    library={('forced',v):[old['forced_witness'][str(v)]] for v in old['forced']}
    library.update({('kill',i):[old['family'][i]['witness']] for i in minimal})
    for row in json.loads((REPO/'hadwiger_nelson_parts509_degree6_lift_family/catalogue.json').read_text()):
        key=row['kind'],row['key'];require(key in library and row['index']==len(library[key]),'catalogue ordering')
        library[key].append(row['witness'])
    decoded={}
    for (kind,key),witnesses in library.items():
        D={key} if kind=='forced' else family[key]
        labels=[v for v in old['vertices'] if v not in D]
        for i,c in enumerate(witnesses):decoded[kind,key,i]=dict(zip(labels,c,strict=True))
    prior=json.loads((REPO/'hadwiger_nelson_parts509_degree6_lift_family/expected.json').read_text())
    facts=[];supports={}
    for q in POINTS:
        vertices=old['vertices']+[q]
        require(len({points[v] for v in vertices})==586,'distinct support points')
        N=[v for v in old['vertices'] if field.squared_distance(points[v],points[q])==(den*den,)+(0,)*7]
        ed=edges+[(v,q) for v in N];adj={v:set() for v in vertices}
        for a,b in ed:adj[a].add(b);adj[b].add(a)
        selected=[];missing=[];checks=0
        for (kind,key),witnesses in library.items():
            D={key} if kind=='forced' else family[key]
            for i,c in enumerate(witnesses):
                colours=decoded[kind,key,i]
                available=sorted(set('0123')-{colours[v] for v in N if v in colours})
                if available:
                    checks+=base.proper(vertices,ed,D,c+available[0])
                    selected.append([kind,key,i,available[0]]);break
            else:missing.append([kind,key])
        missing_forced=[key for kind,key in missing if kind=='forced']
        missing_kill=[key for kind,key in missing if kind=='kill']
        published=next(row for row in prior['coverage'] if row['q']==q)
        require(missing_forced==published['missing_forced'] and missing_kill==published['missing_killing'],'fixed-library coverage')
        fixed_originals=[key for kind,key,_,_ in selected if kind=='forced']
        F=set(fixed_originals)|{q};R=sorted(set(vertices)-F)
        require(set(R)==set(old['free'])|set(missing_forced),'relaxed free partition')
        hitting=[i for i in minimal if i not in missing_kill]
        rows=[({v:1 for v in sorted(family[i])},1) for i in hitting]
        budget=508-len(F)
        rows += [({v:1 for v in old['pool']},3),({v:-1 for v in R},-budget)]
        degree=[]
        for v in vertices:
            need=4-len(adj[v]&F)
            if need<=0:continue
            optional=sorted(adj[v]&set(R));coeff=dict.fromkeys(optional,1)
            rhs=need if v in F else 0
            if v not in F:coeff[v]=-need
            rows.append((coeff,rhs));degree.append(dict(v=v,fixed=v in F,need=need,free_neighbors=optional))
        opb=serialize(R,rows)
        kind,key,i,c=selected[0];require(kind=='forced','five-colouring construction')
        five=dict(decoded[kind,key,i]);five[key]='4';five[q]=c
        five_row=''.join(five[v] for v in vertices)
        five_checks=base.proper(vertices,ed,[],five_row,'01234')
        facts.append(dict(q=q,vertices=586,unit_edges=len(ed),denominator=den,coordinates_numerator=points[q],
                          neighbors=N,forced_originals=fixed_originals,free_vertices=R,budget=budget,
                          missing_forced=missing_forced,missing_killing=missing_kill,hitting_indices=hitting,
                          verified_four_colourings=len(selected),retained_edge_checks=checks,
                          five_colouring_edge_checks=five_checks,degree_obligations=degree,
                          edge_sha256=sha256(''.join(f'{a},{b}\n' for a,b in ed).encode()).hexdigest(),
                          selected_witness_sha256=sha256(json.dumps(selected,separators=(',',':')).encode()).hexdigest(),
                          OPB_variables=len(R),OPB_constraints=len(rows),OPB_sha256=sha256(opb).hexdigest(),OPB_bytes=len(opb)))
        supports[q]=dict(vertices=vertices,edges=ed,adj=adj,fixed=F,free=R,pool=old['pool'],
                         hitting_sets=[family[i] for i in hitting],rows=rows,opb=opb,degree=degree,budget=budget)
    return json.loads(json.dumps(facts)),supports
