#!/usr/bin/env python3
"""Consume the pinned HN3 frontier; return global deletions and exact-five moves."""
import argparse
from collections import Counter
from functools import lru_cache
from itertools import product,combinations
import json,math
from pathlib import Path
import common as C
import verify
X=C.X;V=verify.V;HERE=Path(__file__).resolve().parent
SOURCE_SHA='1db1ecc86c993bbe22a83127b85c6d9467d385bdb7dba085193ad47308e1676a'
INCIDENCE_SHA='c9cb33688915d282b9d410898eeeb22d4bd33e242b3d28b7703ca4fe2111c477'
E1=(1,0,0,0)


def canonical(n,c):
    inv=next(a for a in (1,2,3) if V.gf4_mul(a,next(v for v in n if v))==1)
    return tuple(V.gf4_mul(inv,v) for v in n),V.gf4_mul(inv,c)


@lru_cache(None)
def span(left,right):
    out=set()
    for a,b in product(range(4),repeat=2):
        n=tuple(V.gf4_mul(a,x)^V.gf4_mul(b,y) for x,y in zip(left[0],right[0]))
        c=V.gf4_mul(a,left[1])^V.gf4_mul(b,right[1])
        if any(n):out.add(canonical(n,c))
    X.need(len(out)==5,'five directions in nonparallel pencil')
    return tuple(sorted(out))


def run(interface,incidence,export=None):
    data=json.loads(Path(interface).read_text());inc=json.loads(Path(incidence).read_text())
    X.need(X.digest(data)==SOURCE_SHA and X.digest(inc)==INCIDENCE_SHA,'pinned complete input interfaces')
    rows,factors,circle,monos,rowids=V.reconstruct_inventory()
    X.need(X.digest(factors)==data['curve_inventory_sha256'],'original curve numbering')
    sigs={c:canonical(tuple((a%2)+2*(b%2) for a,b in r[1:]),(r[0][0]%2)+2*(r[0][1]%2)) for r,c in rowids.items()}
    supports={c:{j for j,d in enumerate(r) if j and d!=(0,0)} for r,c in rowids.items()}
    anchors=sorted(c for r,c in rowids.items() if r[0]!=(0,0) and r[1]!=(0,0) and all(d==(0,0) for d in r[2:]))
    X.need(anchors==[591,592,1277,1278,2208,2209],'all six first-step anchor curves')
    buckets={}
    for c,s in sigs.items():buckets.setdefault(s,[]).append(c)
    X.need({c for s,cs in buckets.items() if s[0]==E1 for c in cs}==set(anchors),'all realizable first-coordinate sections are exactly the closed anchors')
    oldexact=data['pair_modes']['exact_five_compatible']
    prior=[r for r in oldexact if len(supports[r[0]]|supports[r[1]])==2]
    X.need(X.digest(prior)=='8eb2ca8fbd0342f6939d57cf60d3f32bedda21ac2e6cf8dc6079d89a3afbb73a','h4181 prior exact-five moves')
    oldset={tuple(r[:2]) for r in prior}
    exact=[r for r in oldexact if tuple(r[:2]) not in oldset]
    six=[r for k,rs in data['pair_modes'].items() if k!='exact_five_compatible' for r in rs]+prior
    allrows=exact+six
    X.need(len({tuple(r[:2]) for r in allrows})==len(allrows)==131356,'complete disjoint source modes')
    degrees=[max(i+j for i,j,c in f) for f in factors]
    for a,b,mask,bound,allowance in allrows:
        X.need(0<=a<b<len(factors) and 0<mask<64,'valid pair and named action mask')
        X.need(bound==degrees[a]*degrees[b]//2 and allowance==bound//mask.bit_count(),'every imported 2kl and stabilizer allowance')
    closed=set(anchors)
    removed=sorted(r for r in allrows if closed.intersection(r[:2]));removedset={tuple(r[:2]) for r in removed}
    moved=sorted(r for r in exact if tuple(r[:2]) not in removedset and any(n==E1 for n,c in span(sigs[r[0]],sigs[r[1]])))
    movedset={tuple(r[:2]) for r in moved}
    kept_exact=sorted(r for r in exact if tuple(r[:2]) not in removedset|movedset)
    kept_six=sorted([r for r in six if tuple(r[:2]) not in removedset]+moved)
    # Reconstruct precisely those full pencils with an e1 section. No search
    # through other support profiles or physical parameters occurs here.
    normals=sorted({canonical((0,)+tail,0)[0] for tail in product(range(4),repeat=3) if any(tail)})
    pencils=set();oldpencils=set()
    for n in normals:
        for a,b in product(range(1,4),range(4)):
            pen=span((E1,a),(n,b))
            if not all(s in buckets for s in pen):continue
            (oldpencils if sum(bool(v) for v in n)==1 else pencils).add(pen)
    forbidden2={tuple(s) for s in inc['monic_degree_four_excluded_pairs']}|{tuple(s) for s in inc['injectivity_excluded_sets'] if len(s)==2}
    forbidden3={tuple(s) for s in inc['injectivity_excluded_sets'] if len(s)==3}
    def count(pen):
        domains=sorted((buckets[s] for s in pen),key=lambda v:(len(v),v))
        def visit(selected,k):
            if k==5:return 1
            total=0
            for c in domains[k]:
                if any(tuple(sorted((a,c))) in forbidden2 for a in selected):continue
                if any(tuple(sorted((a,b,c))) in forbidden3 for a,b in combinations(selected,2)):continue
                total+=visit(selected+[c],k+1)
            return total
        return visit([],0)
    transcript=[[pen,math.prod(len(buckets[s]) for s in pen),count(pen)] for pen in sorted(pencils)]
    summary={'verified':True,'anchor_curves':anchors,'removed_whole_pairs':len(removed),'removed_orbit_allowance':sum(r[4] for r in removed),
        'remaining_global_pairs':len(kept_exact)+len(kept_six),'remaining_global_allowance':sum(r[4] for r in kept_exact+kept_six),
        'exact_five_pairs_removed_globally':sum(tuple(r[:2]) in removedset for r in exact),
        'at_least_six_pairs_removed_globally':sum(tuple(r[:2]) in removedset for r in six),
        'new_pairs_requiring_at_least_six':len(moved),'moved_allowance':sum(r[4] for r in moved),
        'remaining_exact_five_pairs':len(kept_exact),'remaining_exact_five_allowance':sum(r[4] for r in kept_exact),
        'remaining_at_least_six_pairs':len(kept_six),'remaining_at_least_six_allowance':sum(r[4] for r in kept_six),
        'new_closed_pencils':len(pencils),'previously_closed_two_coordinate_pencils':len(oldpencils),
        'new_closed_raw_lifts':sum(r[1] for r in transcript),'new_closed_h4171_survivors':sum(r[2] for r in transcript),
        'remaining_pencils':5328-len(pencils),'remaining_quintets':132225984-sum(r[2] for r in transcript)}
    exported={'schema':'hn-radix-first-anchor-frontier-v1','curve_inventory_sha256':X.digest(factors),'anchor_curves':anchors,
              'removed':removed,'moved':moved,'remaining_exact':kept_exact,'remaining_six':kept_six,
              'pencils':sorted(pencils),'lift_transcript':transcript}
    summary['row_and_pencil_sha256']={k:X.digest(exported[k]) for k in ('removed','moved','remaining_exact','remaining_six','pencils','lift_transcript')}
    summary['export_interface_sha256']=X.digest(exported)
    summary['record_improvement']=False;summary['all_five_active_cases_closed']=False
    if export:
        with Path(export).open('x') as f:json.dump(exported,f,sort_keys=True,separators=(',',':'));f.write('\n')
    return summary


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--interface',type=Path,required=True);p.add_argument('--incidence',type=Path,required=True)
    p.add_argument('--export-interface',type=Path);p.add_argument('--check-expected',action='store_true');a=p.parse_args()
    result=run(a.interface,a.incidence,a.export_interface)
    if a.check_expected:X.need(result==json.loads((HERE/'FRONTIER_EFFECT.json').read_text()),'expected complete frontier update')
    print(json.dumps(result,indent=2,sort_keys=True))
