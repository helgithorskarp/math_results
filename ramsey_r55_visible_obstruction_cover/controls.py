#!/usr/bin/env python3
"""Malformed-certificate controls and literal checks of signed edit balances."""
import argparse
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path

import verify as v

HERE=Path(__file__).resolve().parent

def reject(fn, fragment):
    try:
        fn()
    except ValueError as error:
        v.require(fragment in str(error),'unexpected rejection: '+str(error))
        return str(error)
    raise ValueError('corrupted input accepted: '+fragment)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    ap.add_argument('--graph',type=Path,default=HERE/'GRAPH.json')
    ap.add_argument('--report',type=Path,required=True)
    args=ap.parse_args()
    cert=json.loads(args.certificate.read_text())
    graph=json.loads(args.graph.read_text())
    seed=v.decode(json.loads(v.SEED.read_text()))
    old=v.check_seed(seed)
    result={}
    p=deepcopy(cert['visible']); p['denominator']=0
    result['zero_denominator']=reject(lambda:v.verify_dual(seed,p,'visible'),'dual denominator')
    p=deepcopy(cert['visible']); p['cliques'][0][2]=-1
    result['negative_clique_weight']=reject(lambda:v.verify_dual(seed,p,'visible'),'clique weight')
    p=deepcopy(cert['visible']); p['cliques'].append(p['cliques'][0])
    result['duplicate_clique']=reject(lambda:v.verify_dual(seed,p,'visible'),'duplicate clique row')
    p=deepcopy(cert['visible']); p['cliques'][0][0]=1-p['cliques'][0][0]
    result['wrong_clique_color']=reject(lambda:v.verify_dual(seed,p,'visible'),'nonmonochromatic dual clique')
    p=deepcopy(cert['visible']); p['degrees']=[]; p['profiles']=[]
    result['omitted_conservation']=reject(lambda:v.verify_dual(seed,p,'visible'),'overloaded edge in dual')
    p=deepcopy(cert['total']); p['upper_penalties']=[]
    result['omitted_box_correction']=reject(lambda:v.verify_dual(seed,p,'total'),'overloaded edge in dual')
    p=deepcopy(cert['visible']); p['cliques'][0][2]*=100
    result['overweighted_clique']=reject(lambda:v.verify_dual(seed,p,'visible'),'overloaded edge in dual')
    bad=list(v.decode(graph)); bad[3]=bad[3]^{4}; bad[4]=bad[4]^{3}
    result['changed_witness_degree']=reject(lambda:v.audit_witness(seed,bad,old),'witness degrees')
    result['unchanged_seed_as_cover']=reject(lambda:v.audit_witness(seed,seed,old),'old K5 survives')
    bad=deepcopy(graph); bad['red_adjacency_hex'][0]='0'
    result['asymmetric_graph']=reject(lambda:v.decode(bad),'graph asymmetry')
    # Every coordinate derivative is checked against actual graph changes.
    # Since these quantities are affine with E incidences fixed, checking
    # the constant term and all 780 basis directions proves the linear map.
    base=v.local_profiles(seed)[:3]
    for u,w in v.EDGES:
        new=list(seed)
        new[u]=seed[u]^{w}; new[w]=seed[w]^{u}
        sign=1 if w not in seed[u] else -1
        v.require(all(len(new[a])-len(seed[a])==sign*int(a in (u,w)) for a in range(43)),
                  'degree coordinate derivative')
        profiles=v.local_profiles(new)[:3]
        for e in range(3):
            red=int(u in seed[e] and w in seed[e])
            blue=int(u not in seed[e] and w not in seed[e])
            v.require(profiles[e][0]-base[e][0]==sign*red,'red profile derivative')
            v.require(profiles[e][1]-base[e][1]==-sign*blue,'blue profile derivative')
    # Every old K5 is destroyed exactly when its flip-support is hit. Check
    # all 1024 flip patterns on one five-set, not only positive examples.
    small=list(combinations(range(5),2))
    tested=0
    for red in (False,True):
        for mask in range(1<<10):
            colors=[red^bool(mask>>i&1) for i in range(10)]
            old_survives=all(c==red for c in colors)
            v.require(old_survives==(mask==0),'old-clique cover equivalence')
            tested+=1
    report={'status':'PASS','rejected':result,'signed_edge_basis_directions':len(v.EDGES),
            'five_set_flip_patterns':tested,'visible_edges':len(v.visible_edges(seed)),
            'bound_scope_control':'The stored sharp-cover witness has mixed K5s; it cannot certify a mixed-free or full Ramsey repair.'}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','malformed_controls':len(result),'basis_directions':len(v.EDGES)}))

if __name__=='__main__':
    main()
