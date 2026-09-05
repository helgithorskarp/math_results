#!/usr/bin/env python3
"""Solver-free checking of three primary models and actual graph colourings."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from engine import HERE,REPO,POINTS,compute,load,require
from controls import check


def model_check(fact,support,certificate,edges):
    X=set(certificate['selector'])
    require(certificate['selector']==sorted(X) and X<=set(support['free']),'selector domain')
    # Decode each published input line directly, without the producer's row map.
    lines=(HERE/'instances'/f'{fact["q"]}.opb').read_text().splitlines()[1:]
    for line in lines:
        left,right=line.split(' >= ');rhs=int(right.removesuffix(' ;'));tokens=left.split()
        value=sum(int(c) for c,v in zip(tokens[::2],tokens[1::2],strict=True)
                  if support['free'][int(v[1:])-1] in X)
        require(value>=rhs,'primary model violates OPB')
    labels=sorted(support['fixed']|X);colouring=certificate['colouring']
    require(len(labels)<=508 and len(colouring)==len(labels) and set(colouring)<=set('0123'),'colouring format')
    colours=dict(zip(labels,colouring,strict=True));kept=set(labels)
    candidate_edges=[(u,v) for u,v in edges if u in kept and v in kept]
    require(all(colours[u]!=colours[v] for u,v in candidate_edges),'monochromatic candidate edge')
    degrees=Counter(v for edge in candidate_edges for v in edge)
    require(all(degrees[v]>=4 for v in labels),'candidate minimum degree')
    require(len(kept&set(support['pool']))>=3,'candidate pool quota')
    pos={v:i for i,v in enumerate(labels)}
    triangle=next((u,v,w) for u,v in support['edges'] if u in pos and v in pos
                  for w in sorted(support['adj'][u]&support['adj'][v]) if w>v and w in pos)
    ordered_edges=[e for e in support['edges'] if e[0] in pos and e[1] in pos]
    rows=[[4*i+c+1 for c in range(4)] for i in range(len(labels))]
    rows += [[-(4*pos[u]+c+1),-(4*pos[v]+c+1)] for u,v in ordered_edges for c in range(4)]
    rows += [[4*pos[v]+c+1] for c,v in enumerate(triangle)]
    cnf=(f'p cnf {4*len(labels)} {len(rows)}\n'+''.join(' '.join(map(str,C))+' 0\n' for C in rows)).encode()
    require(sha256(cnf).hexdigest()==certificate['candidate_cnf_sha256'],'executed candidate CNF identity')
    return dict(q=fact['q'],selector_size=len(X),retained_pool_points=len(X&set(support['pool'])),
                retained_previously_unforced=sorted(X&set(fact['missing_forced'])),candidate_vertices=len(labels),
                candidate_edges=len(candidate_edges),minimum_degree=min(degrees.values()),
                degree_histogram={str(k):v for k,v in sorted(Counter(degrees.values()).items())},
                OPB_model_verified=True,four_colouring_verified=True,candidate_cnf_sha256=sha256(cnf).hexdigest())


def verify():
    facts,supports=compute();require(facts==json.loads((HERE/'expected.json').read_text()),'exact facts')
    control=check(facts,supports)
    require(control==json.loads((HERE/'controls_expected.json').read_text()),'preflight controls')
    # Alternate arithmetic and a fresh parse/pair scan audit the actual supports.
    audit=load('alternate_arithmetic',REPO/'hadwiger_nelson_parts509_point613_closure_review1/independent_check.py')
    points={}
    lines=(REPO/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_text().splitlines()
    originals=[list(map(int,line.split())) for line in lines if line and not line.startswith('#')]
    require(len(originals)==509 and all(len(row)==16 for row in originals),'original coordinate dimensions')
    for v,row in enumerate(originals):points[v]=(tuple(3*x for x in row[:8]),tuple(3*x for x in row[8:]))
    completions=json.loads((REPO/'hadwiger_nelson_parts509_swap_closure/completion_points.json').read_text())['points']
    for v in list(range(509,585))+POINTS:
        p=completions[v-509];xy=[]
        for axis in ['x','y']:
            terms=[Fraction(c)*288 for c in p[axis]]
            require(len(terms)==8 and all(c.denominator==1 for c in terms),'exact coordinate scale')
            xy.append(tuple(c.numerator for c in terms))
        points[v]=tuple(xy)
    raw=(HERE/'certificates.json').read_bytes()
    require(sha256(raw).hexdigest()==json.loads((HERE/'manifest.json').read_text())['certificates_sha256'],'certificate identity')
    certificates=json.loads(raw)
    require([x['q'] for x in certificates]==POINTS,'certificate coverage')
    result=[];pair_checks=0;rejected=0
    for fact,certificate in zip(facts,certificates,strict=True):
        q=fact['q'];s=supports[q]
        require((HERE/'instances'/f'{q}.opb').read_bytes()==s['opb'],'published OPB identity')
        require(len({points[v] for v in s['vertices']})==586,'audit coordinate collisions')
        pairs=list(combinations(s['vertices'],2));pair_checks+=len(pairs)
        edges=[(u,v) for u,v in pairs if audit.squared_distance(points[u],points[v])==(288*288,)+(0,)*7]
        require(set(edges)==set(s['edges']),'alternate complete unit-edge scan')
        result.append(model_check(fact,s,certificate,edges))
        # Domain corruption and a genuine monochromatic edge must be rejected.
        bad=dict(certificate,selector=certificate['selector']+[q])
        try:model_check(fact,s,bad,edges)
        except ValueError:rejected+=1
        else:raise ValueError('invalid selector accepted')
        labels=sorted(s['fixed']|set(certificate['selector']));pos={v:i for i,v in enumerate(labels)}
        u,v=next(e for e in edges if e[0] in pos and e[1] in pos)
        colours=list(certificate['colouring']);colours[pos[v]]=colours[pos[u]]
        bad=dict(certificate,colouring=''.join(colours))
        try:model_check(fact,s,bad,edges)
        except ValueError:rejected+=1
        else:raise ValueError('monochromatic edge accepted')
    return dict(status='THREE SAT SELECTORS AND FOUR-COLOURABLE ORDER-508 CANDIDATES VERIFIED',
                supports=result,alternate_exact_pair_checks=pair_checks,malformed_certificates_rejected=rejected,
                new_native_queries=0,all_three_support_closures_remain_open=True,record_improvement=False)


if __name__=='__main__':
    result=verify();require(result==json.loads((HERE/'verification.json').read_text()),'verification report differs')
    print(json.dumps(result,indent=2,sort_keys=True))
