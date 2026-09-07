#!/usr/bin/env python3
"""Check all geometry, all deletion words, and the integer degree-count certificate."""
import argparse
import json
from pathlib import Path
from collections import Counter
import cover

HERE=Path(__file__).resolve().parent

def weighted_bound(proof,g,mandatory):
    need=cover.need;n=len(g['points']);M=set(mandatory)
    need(proof.get('version')=='t721-weighted-neighbour-v1','weight version')
    need(type(proof.get('minimum_degree'))is int and proof['minimum_degree']==4,'minimum degree')
    need(type(proof.get('outside_capacity'))is int and proof['outside_capacity']==2,'capacity')
    rows=proof.get('weights');need(type(rows)is list and rows,'weight rows')
    weights={}
    for row in rows:
        need(type(row)is list and len(row)==2,'weight row')
        v=cover.integer(row[0],0,n,'weight vertex');w=cover.integer(row[1],1,3,'weight value')
        need(v in M and v not in weights,'weight support or duplicate');weights[v]=w
    incidence=[0]*n
    for u,v in g['edges']:
        incidence[u]+=weights.get(v,0);incidence[v]+=weights.get(u,0)
    exceptional=[u for u in range(n)if u not in M and incidence[u]>2]
    provided=proof.get('exceptional_outside')
    need(type(provided)is list and all(type(u)is int for u in provided)and provided==exceptional,'outside exceptions')
    # For any minimal non-four-colourable S, M is contained in S and each
    # weighted vertex has at least four neighbours in S.
    total=sum(weights.values());inside=sum(incidence[u]for u in M)
    excess=sum(max(0,incidence[u]-2)for u in range(n)if u not in M)
    deficit=4*total-inside-excess
    required_extra=max(0,-(-deficit//2));bound=len(M)+required_extra
    return {'weighted_vertices':len(weights),'weight_multiplicities':dict(sorted(Counter(weights.values()).items())),
            'total_weight':total,'required_incidence':4*total,'incidence_in_mandatory':inside,
            'exceptional_outside_vertices':exceptional,'outside_excess':excess,
            'required_extra_vertices':required_extra,'minimum_critical_order':bound,
            'four_colourable_through':bound-1}

def moser_audit(g):
    n=len(g['points']);A=[set()for _ in range(n)]
    for u,v in g['edges']:A[u].add(v);A[v].add(u)
    arms=[set()for _ in range(n)];diamonds=0
    for u,v in g['edges']:
        common=A[u]&A[v];cover.need(len(common)<=2,'unit base common neighbours')
        if len(common)==2:
            a,b=sorted(common);cover.need(b not in A[a],'unit diamond tips')
            arms[a].add(b);arms[b].add(a);diamonds+=1
    contacts=sum(len(A[u]&tips)for tips in arms for u in tips)//2
    cover.need(contacts==0,'Moser arm contact')
    return {'moser_free':True,'unit_diamonds':diamonds,'moser_arm_contacts':contacts}

def verify(path,certificate=None,weights=None):
    g=cover.geometry(path)
    certificate=certificate if certificate is not None else json.loads((HERE/'certificate.json').read_text())
    weights=weights if weights is not None else json.loads((HERE/'weights.json').read_text())
    result=cover.full_cover(certificate,g,require_target=False)
    result['deletion_cover_through']=result.pop('four_colourable_through')
    result.update(weighted_bound(weights,g,result['mandatory_global_vertices']))
    result.update(moser_audit(g))
    cover.need(result['minimum_critical_order']>508,'target not excluded')
    result.update(arbitrary_target_subsets_classified=True,verified=True,record_improvement=False)
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True,type=Path);ap.add_argument('--check-expected',action='store_true');a=ap.parse_args()
    result=verify(a.input)
    # JSON canonicalization makes numeric dictionary keys comparable to files.
    result=json.loads(json.dumps(result))
    if a.check_expected:cover.need(result==json.loads((HERE/'expected.json').read_text()),'expected mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))
