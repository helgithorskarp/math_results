"""Check all34 literal cores and proper colors from definitions.

Standard library; no producer, prior census code or solver imported.
Input carrier completeness is the explicitly credited theorem9045.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

BRIDGE_PIN='9239f6cfcb413ff8a76eddf172ebd62abdec46aec7c8c87c788c2370e856d1d2'

def need(test,message):
    if not test:
        raise ValueError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def words_from_masks(masks):
    need(type(masks) is list and len(masks)==36,'wrong36-core population')
    need(all(type(m) is int and 0<m<2**18 for m in masks),'invalid word mask')
    words=[frozenset(p for p in range(18) if m>>p&1) for m in masks]
    need(len(set(words))==36 and all(len(w)==5 for w in words),'invalid distinct five-subsets')
    need(all(len(a&b)<=2 for a,b in itertools.combinations(words,2)),'core packing collision')
    return words

def domain_and_role(row):
    words=words_from_masks(row['word_masks'])
    x=17
    u,v,y=row['first'][1]
    need(all(type(p) is int and 0<=p<18 for p in (u,v,y)) and len({x,y,u,v})==4,'invalid marked points')
    phi=row['point_map']
    need(len(phi)==17 and all(type(p) is int for p in phi) and set(phi)==set(range(18))-{y},'relative map not bijective')
    su,sv,sx,sb=row['second'][1]
    need(all(type(p) is int and 0<=p<17 for p in (su,sv,sx,sb)),'invalid source marks')
    need((phi[su],phi[sv],phi[sx])==(u,v,x),'distinguished point images differ')
    replication={p:sum(p in w for w in words) for p in range(18)}
    need(replication[x]==replication[y]==20,'centers are not complete20 stars')
    lam=lambda p,q:sum({p,q}<=w for w in words)
    covered=lambda p,q,t:any({p,q,t}<=w for w in words)
    need(lam(x,y)==4 and lam(x,v)==5 and not covered(x,y,v),'local assumption1 fails')
    need(lam(x,u) in(3,4) and all(lam(x,p) in(4,5) for p in range(18) if p not in(x,u)),'first row differs')
    deficient={p for p in range(18) if p!=x and lam(x,p)<5}
    need(all(covered(x,u,p) for p in deficient-{u}),'hub not isolated in deficient leave')
    need(lam(y,u)==lam(y,v)==5 and all(lam(y,p) in(4,5) for p in range(18) if p!=y),'local unit-row assumption fails')
    triples=[tuple(sorted(t)) for w in words for t in itertools.combinations(w,3)]
    need(len(triples)==len(set(triples))==360,'triple ownership differs')
    used=set(triples)
    candidates=[frozenset(q) for q in itertools.combinations(sorted(set(range(18))-{x,y}),5)
                if all(t not in used for t in itertools.combinations(q,3))]
    masks=[sum(2**p for p in w) for w in candidates]
    triangles=[p for p in range(18) if p not in(x,y,u,v) and lam(x,p)==lam(y,p)==4 and not covered(x,y,p)]
    need(triangles==row['triangle_points'],'literal triangle readout differs')
    return words,candidates,masks,dict(lambda_xu=lam(x,u),triangle_count=len(triangles))

def check(bridge,certificate):
    rows=bridge['raw_positive_maps']
    need(type(rows) is list and len(rows)==34,'wrong raw carrier population')
    keys=[(r['product_index'],tuple(r['point_map'])) for r in rows]
    need(len(set(keys))==34,'duplicate actual point map')
    entries=certificate['entries']
    need(type(entries) is list and len(entries)==34,'wrong certificate population')
    need(all(type(e['index']) is int for e in entries),'invalid certificate index')
    need({e['index'] for e in entries}==set(range(34)),'certificate cover gap or duplicate')
    by_index={e['index']:e for e in entries}
    results=[]
    candidate_domains=[]
    for index,row in enumerate(rows):
        e=by_index[index]
        words,candidates,masks,role=domain_and_role(row)
        need(e['product_index']==row['product_index'],'product attribution differs')
        need(e['first_fixture']==row['first'][0],'first fixture attribution differs')
        need(e['candidate_count']==len(candidates) and e['candidate_sha256']==digest(masks),'residual universe differs')
        need(e['triangle_count']==role['triangle_count'],'triangle statistic differs')
        colors=e['colors']
        capacity=e['capacity']
        need(type(capacity) is int and 1<=capacity<=len(candidates),'invalid capacity')
        need(type(colors) is list and len(colors)==len(candidates),'color population differs')
        need(all(type(c) is int and 0<=c<capacity for c in colors),'color label outside capacity')
        need(set(colors)==set(range(capacity)),'unused or missing color class')
        edges=0
        for i,j in itertools.combinations(range(len(candidates)),2):
            if len(candidates[i]&candidates[j])<=2:
                need(colors[i]!=colors[j],'compatible candidates share a color')
                edges+=1
        need(e['edges']==edges,'edge population differs')
        need(e['upper_bound']==36+capacity,'total bound differs')
        results.append(dict(index=index,product_index=row['product_index'],candidate_count=len(candidates),
                            edges=edges,capacity=capacity,upper_bound=36+capacity,
                            candidate_sha256=digest(masks),**role))
        candidate_domains.append(masks)
    maximum=max(r['upper_bound'] for r in results)
    need(maximum<=66,'uniform upper66 certificate fails')
    census={str(k):sum(r['upper_bound']==k for r in results) for k in sorted({r['upper_bound'] for r in results})}
    subscopes={str(d):dict(interfaces=sum(r['lambda_xu']==d for r in results),
                          maximum_upper_bound=max(r['upper_bound'] for r in results if r['lambda_xu']==d))
               for d in(3,4)}
    return dict(status='PASS_ALL34_LITERAL_RESIDUAL_COLOR_CERTIFICATES',interfaces=34,
                universe_per_interface=4368,total_residual_candidates=sum(r['candidate_count'] for r in results),
                total_compatible_edges=sum(r['edges'] for r in results),maximum_upper_bound=maximum,
                color_range=[min(r['capacity'] for r in results),max(r['capacity'] for r in results)],
                upper_bound_census=census,lambda_xu_subscopes=subscopes,
                triangle_uncovered_interfaces=sum(r['triangle_count']>0 for r in results),
                triangle_witnesses=sum(r['triangle_count'] for r in results),records=results,
                candidate_domains_sha256=digest(candidate_domains),records_sha256=digest(results))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--bridge',required=True)
    parser.add_argument('--certificate',required=True)
    args=parser.parse_args()
    raw=Path(args.bridge).read_bytes()
    need(hashlib.sha256(raw).hexdigest()==BRIDGE_PIN,'credited raw carrier pin differs')
    result=check(json.loads(raw),json.loads(Path(args.certificate).read_text()))
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    main()
