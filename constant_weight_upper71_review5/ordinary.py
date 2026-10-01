"""Literal controls for ordinary counting bridges, not a finite proof of their universality."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
from common import canonical,require

def partitions(total,ceiling=None):
    if total==0:
        yield ()
        return
    for first in range(min(total,ceiling or total),0,-1):
        for rest in partitions(total-first,first): yield (first,)+rest

def product4(a,b):
    result=0
    while b:
        if b&1: result^=a
        b>>=1; a<<=1
        if a&4:a^=7
    return result

def affine_fixture():
    quads=[tuple(4*x+y for y in range(4)) for x in range(4)]
    quads+=[tuple(4*x+(product4(slope,x)^offset) for x in range(4)) for slope in range(4) for offset in range(4)]
    require(len(set(map(frozenset,quads)))==20,'duplicate affine lines')
    pairs=Counter(p for q in quads for p in combinations(q,2))
    require(len(pairs)==120 and set(pairs.values())=={1},'affine pair coverage fails')
    switched=[tuple(16 if y==0 else 4*x+y for y in range(4)) for x in range(4)]+quads[4:]
    switched=tuple(sorted(tuple(sorted(q)) for q in switched))
    pairs=Counter(p for q in switched for p in combinations(q,2))
    require(len(pairs)==120 and set(pairs.values())=={1},'switched pair packing invalid')
    rep=tuple(sum(x in q for q in switched) for x in range(17))
    high=frozenset(x for x,n in enumerate(rep) if n==4)
    require(len(high)==5 and sorted(rep)==[4]*5+[5]*12,'wrong switched profile')
    leave=set(combinations(range(17),2))-set(pairs)
    high_leave=tuple(sorted(p for p in leave if set(p)<=high))
    require(high_leave==tuple((x,16) for x in (0,4,8,12)) and not any(not set(p)&high for p in leave),
            'wrong sharp high-core fixture')
    return dict(quads=switched,replications=rep,high=tuple(sorted(high)),high_leave=high_leave,
                all_unit_core_edges=4)

def deficit_budget(words):
    M=len(words)
    pairs=tuple(combinations(range(18),2))
    rep=tuple(sum(x in q for q in words) for x in range(18))
    pair_count=Counter(p for q in words for p in combinations(sorted(q),2))
    require(all(pair_count[p]<=5 for p in pairs),'pair multiplicity cap fails')
    delta={p:5-pair_count[p] for p in pairs}
    D={p for p,n in delta.items() if n>0}
    excess=sum(n-1 for n in delta.values() if n>0)
    covered={t for q in words for t in combinations(sorted(q),3)}
    missing=set(combinations(range(18),3))-covered
    P=sum(sum(p in D for p in combinations(t,2)) in (0,3) for t in missing)
    local_m=[]; homogeneous=0
    for x in range(18):
        others=set(range(18))-{x}
        W={y for y in others if pair_count[tuple(sorted((x,y)))]==5}
        star_pairs={p for q in words if x in q for p in combinations(sorted(q-{x}),2)}
        leave=set(combinations(sorted(others),2))-star_pairs
        m=sum(set(p)<=W for p in leave)
        h=17-len(W);a=20-rep[x]
        e=sum(not(set(p)&W) for p in leave)
        require(e-m==h-1+6*a,'local general leave identity fails')
        local_m.append(m);homogeneous+=e+m
        if rep[x]==20: require(m==0,'literal saturated-center theorem fails')
    require(len(missing)==816-10*M and homogeneous==len(missing)+2*P,'global homogeneous identity fails')
    require(excess+P-sum(local_m)==1428-20*M,'exact all-size deficit budget fails')
    return dict(M=M,deficit_edges=len(D),excess=excess,monochromatic_uncovered_triples=P,
                total_low_low_leave=sum(local_m),point_deficit=360-5*M,
                budget_constant=1428-20*M)

def bridges(baseline_path):
    rows=baseline_path.read_text().splitlines()
    require(len(rows)==69 and len(set(rows))==69 and all(len(r)==18 and set(r)<={'0','1'} and r.count('1')==5 for r in rows),
            'invalid known69 input')
    words=tuple(frozenset(x for x,c in enumerate(r) if c=='1') for r in rows)
    maximum=max(len(a&b) for a,b in combinations(words,2))
    require(maximum==2,'known69 pair intersection fails')
    triples=tuple(Counter(t for q in words for t in combinations(sorted(q),3)).values())
    require(set(triples)=={1} and len(triples)==690,'known69 triple coverage fails')
    graphs=[]
    for edges in range(8):
        pairs=tuple(p for i,p in enumerate(combinations(range(3),2)) if edges>>i&1)
        degrees=tuple(sum(x in p for p in pairs) for x in range(3))
        homogeneous=sum(d in (0,2) for d in degrees)
        require(homogeneous==1+2*int(len(pairs)in (0,3)),'three-point identity fails')
        graphs.append(dict(edge_mask=edges,degree=degrees,homogeneous=homogeneous))
    profiles=tuple(partitions(5))
    require(len(profiles)==7,'deficit partition coverage fails')
    local=[]
    for profile in profiles:
        h=len(profile)
        cap=h-1  # The audited universal saturated-point theorem gives m=0.
        require(cap<=4,'local bound not strong enough')
        local.append(dict(deficits=profile,h=h,homogeneous_cap=cap))
    require(18*20==5*72 and 816-72*10==96 and 18*4==72,'global arithmetic fails')
    budgets=[deficit_budget(words[:count]) for count in (0,1,5,30,68,69)]
    return dict(known69=dict(words=69,max_intersection=maximum,covered_triples=690,
                            sha256=sha256(baseline_path.read_bytes()).hexdigest()),
                three_point_graphs=graphs,seven_deficit_profiles=local,
                local_all_mode_bound=4,uncovered_triples_at72=96,homogeneous_upper_at72=72,
                contradiction_gap=24,
                literal_general_budget_controls=budgets,
                proved_71_budget='sum_unsaturated_center_low_low_leaves+8=pair_deficit_excess+monochromatic_uncovered_triples',
                affine_sharp_fixture=affine_fixture())

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--baseline',type=Path,required=True)
    print(json.dumps(bridges(parser.parse_args().baseline),indent=2))
