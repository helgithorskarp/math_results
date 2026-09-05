#!/usr/bin/env python3
"""Verify positive witnesses, omission reduction data and canonical CNF."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from build import HERE,REPO,instance,load


def require(ok,detail):
    if not ok:raise ValueError(detail)


def compute():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for path,digest in manifest['inputs'].items():
        require(sha256((REPO/path).read_bytes()).hexdigest()==digest,('input hash',path))
    cert=json.loads((HERE/'certificate.json').read_text())
    require(sha256((HERE/'certificate.json').read_bytes()).hexdigest()==manifest['certificate_sha256'],'certificate hash')
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    basepath=REPO/'hadwiger_nelson_parts509_degree7_extension610'
    sys.path.insert(0,str(basepath))
    try:base=load('exact_graph_primitives',basepath/'verify.py')
    finally:sys.path.pop(0)
    _,old_edges,den,points,_=base.geometry(old)
    old_edges=[(a,b) for a,b in old_edges if b!=610]
    field=load('exact_integer_field',REPO/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py')
    vertices=old['vertices']+[613]
    require(len(set(points[v] for v in vertices))==586,'coordinate collision')
    require(points[613]==((-240,0,0,0,0,0,0,0),(0,0,0,0,48,0,0,0)) and den==288,
            'point613=(-5/6,sqrt(11)/6)')
    neighbours=[v for v in old['vertices'] if field.squared_distance(points[v],points[613])==(den*den,)+(0,)*7]
    require(neighbours==[0,8,53,148,164,195],'exact neighbourhood')
    edges=old_edges+[(v,613) for v in neighbours]
    require(len(edges)==3089,'strict edge count')
    require(old['free']==sorted(set(old['vertices'])-set(old['forced'])),'free partition')
    require(len(old['forced'])==451 and set(old['forced'])<=set(range(509)),'forced originals')
    family=[set(row['D']) for row in old['family']]
    require(all(D and D<=set(old['free']) for D in family),'killing sets in free vertices')
    minimal=[i for i,D in enumerate(family) if not any(E<D for E in family)]
    require(len(minimal)==337 and all(any(family[i]<=D for i in minimal) for D in family),'equivalent minimal family')
    library={('forced',v):[old['forced_witness'][str(v)]] for v in old['forced']}
    library.update({('kill',i):[old['family'][i]['witness']] for i in minimal})
    for row in json.loads((REPO/'hadwiger_nelson_parts509_degree6_lift_family/catalogue.json').read_text()):
        key=row['kind'],row['key'];require(key in library and len(library[key])==row['index'],'catalogue index')
        library[key].append(row['witness'])
    selected=[];missing=[];checks=0;five=None
    for (kind,key),rows in library.items():
        D={key} if kind=='forced' else family[key]
        labels=[v for v in old['vertices'] if v not in D]
        for index,witness in enumerate(rows):
            require(len(witness)==len(labels),'colour length')
            colours=dict(zip(labels,witness,strict=True))
            available=sorted(set('0123')-{colours[v] for v in neighbours if v in colours})
            if available:
                checks+=base.proper(vertices,edges,D,witness+available[0])
                selected.append((kind,key,index,available[0]));break
        else:missing.append([kind,key])
    require(missing==[['kill',245],['kill',316]],'missing witnessed constraints')
    kind,key,index,colour=selected[0]
    require(kind=='forced','first witness is a forced-vertex deletion')
    labels=[v for v in old['vertices'] if v!=key]
    five=dict(zip(labels,library[kind,key][index],strict=True));five[613]=colour;five[key]='4'
    five_checks=base.proper(vertices,edges,[],''.join(five[v] for v in vertices),'01234')
    require(family[245]=={129,518} and family[316]=={13,24},'missing deletion sets')
    require(sha256(base.old_opb(old)).hexdigest()==manifest['old_OPB_sha256'],'imported hitting bound input')
    require(cert['stage1']['omitted']==[13,24] and cert['stage2']['omitted']==[13,24,129,518],
            'staged omission labels')
    pool=set(old['pool'])
    for stage,count in [('stage1',5),('stage2',7)]:
        data=cert[stage];groups=[]
        for i in data['rows']:
            require(i in minimal and i not in [245,316],'unwitnessed group')
            D=family[i]-set(data['omitted']);require(D and D<=pool,'group is not pool-only')
            groups.append(sorted(D))
        require(groups==data['groups'] and len(groups)==count,'group certificate')
        require(sum(map(len,groups))==len(set().union(*map(set,groups))),'groups overlap')
    omit=set(cert['stage2']['omitted'])
    units=sorted(set().union(*(family[i]-omit for i in minimal if i not in [245,316] and len(family[i]-omit)==1)))
    require(units==cert['additional_forced_vertices'],'additional forced vertices')
    cnf,meta=instance(old)
    require(meta['cnf_sha256']==manifest['residual_cnf_sha256'],'canonical selector hash')
    require(meta['hitting_rows']==[i for i in minimal if i not in [245,316]],'selector family')
    facts=dict(status='NECESSARY RESIDUAL VERIFIED; SUPPORT REMAINS UNRESOLVED',point=613,
               vertices=len(vertices),unit_edges=len(edges),denominator=den,neighbors=neighbours,
               edge_sha256=sha256(''.join(f'{a},{b}\n' for a,b in edges).encode()).hexdigest(),
               forced_witnesses=451,killing_witnesses=335,retained_edge_checks=checks,
               selected_witness_sha256=sha256(json.dumps(selected,separators=(',',':')).encode()).hexdigest(),
               missing_minimal_rows=[245,316],omitted_vertices=sorted(omit),
               additional_forced_vertices=units,minimum_old_pool_points=7,minimum_total_additions=8,
               minimum_original_deletions=9,closure_through507=True,
               possible_counterexample_order=508,exact_free_vertices=56,
               minimum_five_chromatic_subgraph_order_interval=[508,509],
               full_support_five_colouring_verified=True,five_colour_edge_checks=five_checks,
               old_bound_opb_sha256=manifest['old_OPB_sha256'],old_PB_proof_rechecked=False,
               residual_variables=meta['variables'],residual_clauses=meta['clauses'],
               residual_sha256=meta['cnf_sha256'],record_improvement=False,
               native_answer_used_as_proof=False)
    return facts,cnf,meta


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cnf-out',type=Path);args=ap.parse_args()
    facts,cnf,_=compute();require(facts==json.loads((HERE/'expected.json').read_text()),'expected facts differ')
    if args.cnf_out:args.cnf_out.write_bytes(cnf)
    print(json.dumps(facts,indent=2,sort_keys=True))


if __name__=='__main__':main()
