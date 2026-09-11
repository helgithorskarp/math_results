#!/usr/bin/env python3
"""Independent finite cover controls; standard library. Refutations need DRAT replay."""
import ast,hashlib,json
from itertools import combinations,permutations
from pathlib import Path
from collections import Counter
from a0_inventory import profiles
from a0_independent import inventory
from verify_a2_exclusion import require
from verify_distant_partition import check_partition_control
from verify import graph,hoffman_singleton_edges

HERE=Path(__file__).resolve().parent

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def subsets(U,k):return [frozenset(x) for x in combinations(sorted(U),k)]
def linear(blocks):return all(len(a&b)<=1 for a,b in combinations(blocks,2))

def covers(existing_pairs,existing_triples):
    U=frozenset(range(8));out=[]
    for pair in subsets(U,2):
        if pair in existing_pairs:continue
        for A in subsets(U-pair,3):
            B=U-pair-A
            if tuple(sorted(A))>=tuple(sorted(B)):continue
            if linear(existing_pairs+existing_triples+[pair,A,B]):out.append((pair,A,B))
    return out

def main():
    ps=list(profiles());require(sorted(ps)==inventory(),'independent complete inventory')
    one=[i for i,(m,k,s,t) in enumerate(ps) if m==5 and s[4]+t[4]==1 and not(sum(s[5:])+sum(t[5:]))]
    require(one==[361,366,367,368,374,375,382,383,387,390],'entire one-quad cover')
    for i in one:
        m,k,s,t=ps[i]
        if i==361:require(s[4]==0 and t[4]==1,'seven quad case');continue
        require(t[4]==0 and s[4]==1 and t[3]<=2-k,'outside helper bound')
        require(7-(2-k)+t[3]<=7,'at most seven outside helpers')
        if s[1]:require(i in (374,375,387),'six singleton closing cases')
    sat=[i for i in one if i not in (361,374,375,387)]
    require(sat==[366,367,368,382,383,390],'all six residual profiles')
    for i in sat:
        m,k,s,t=ps[i];require(s==(0,0,3,12,1,0,0),'common six histogram')
    # Direct complement generation, not the hand-written grid normalization.
    pair0=frozenset((0,1));trip0=frozenset((2,3,4));trip1=frozenset((5,6,7))
    second=covers([pair0],[trip0,trip1]);require(second,'nonvacuous two-bad configuration')
    for pair,A,B in second:
        require(not pair&pair0,'bad pairs are disjoint')
        require(all(len(x&y)==1 for x in (trip0,trip1) for y in (A,B)),'four distinct grid intersections')
        require(len({next(iter(x&y)) for x in (trip0,trip1) for y in (A,B)})==4,'grid points distinct')
    B=[frozenset(x) for x in ((0,1),(2,3),(4,7))]
    T=[frozenset(x) for x in ((2,4,5),(3,6,7),(0,4,6),(1,5,7),(0,3,5),(1,2,6))]
    require(linear(B+T),'normalized three-bad family is linear')
    for i in range(3):require(B[i]|T[2*i]|T[2*i+1]==frozenset(range(8)),'exact normalized partitions')
    third=covers(B[:2],T[:4]);require(len(third)==2,'exactly the two diagonal third covers')
    require({x[0] for x in third}=={frozenset((4,7)),frozenset((5,6))},'third bad diagonal')
    require(any(p==B[2] and {A,D}==set(T[4:]) for p,A,D in third),'chosen third representative')
    # Every point permutation is tried; induced helper actions determine all
    # degree-seven assignments of weight<=2, preserving far associations.
    orbit_records={};expected_reps={2:[(),(0,),(0,1),(0,2)],3:[(),(0,),(0,1),(0,2),(0,3)]}
    for r in (2,3):
        Bs=B[:r];Ts=T[:2*r];actions=set();full=0
        for perm in permutations(range(8)):
            mappedB=[frozenset(perm[x] for x in b) for b in Bs]
            mappedT=[frozenset(perm[x] for x in t) for t in Ts]
            if set(mappedB)!=set(Bs) or set(mappedT)!=set(Ts):continue
            full+=1;act=tuple(Ts.index(t) for t in mappedT);actions.add(act)
            for j,mb in enumerate(mappedB):
                z=Bs.index(mb);require({act[2*j],act[2*j+1]}=={2*z,2*z+1},'far association preserved')
        reps=[];degrees=[]
        for w in range(3):
            words=list(combinations(range(2*r),w));canon={I:min(tuple(sorted(p[x] for x in I)) for p in actions) for I in words}
            chosen=sorted(set(canon.values()));reps+=chosen
            degrees.append({'weight':w,'assignments':len(words),'representatives':chosen})
        require(reps==expected_reps[r],'all helper degree orbits')
        orbit_records[str(r)]={'point_permutations_tested':40320,'automorphisms':full,'helper_actions':sorted(actions),'degree_orbits':degrees}
    # The only ways to spend one unit of positive charge. Degree-six c3 and
    # degree-seven c3 have zero coefficient and remain unrestricted by charge.
    cost_one=[]
    for d,c in ((6,2),(6,4),(7,0),(7,1),(7,2)):
        for e in range(2*c-(8 if d==6 else 7),c-(2 if d==6 else 0)+1):
            if d==7 and e>0:continue
            if (c-3)*e==1:cost_one.append((d,c,e))
    require(cost_one==[(6,2,-1),(6,4,1),(7,2,-1)],'complete one-unit charge cover')
    cases=[]
    for idx in sat:
        n73=ps[idx][3][3]
        for branch in ('A','B','C','D'):
            if n73==0 and branch!='A':continue
            r=2 if branch=='A' else 3
            for role,S in enumerate(expected_reps[r]):
                if len(S)<=n73:cases.append([idx,branch,role])
    require(len(cases)==38,'complete 38-case cover')
    # Check the literal normalized data consumed by the SAT source without
    # importing PySAT or trusting a solver in these combinatorial controls.
    source=ast.parse((HERE/'a0_one_quad_sat.py').read_text());constants={}
    for node in source.body:
        if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ('REPS','BAD','HELP'):
            constants[node.targets[0].id]=ast.literal_eval(node.value)
    require(constants['REPS']==expected_reps,'SAT role constants')
    require(constants['BAD']==[{x+4 for x in b} for b in B],'SAT bad-set constants')
    require(constants['HELP']==[{x+4 for x in t} for t in T],'SAT helper-set constants')
    hs=hoffman_singleton_edges();controls=[check_partition_control(graph(50,sorted(hs-deleted))) for deleted in (set(),{(0,1)},{(0,1),(2,3)})]
    fixture=json.loads((HERE/'lower_bound_54_185.json').read_text());controls.append(check_partition_control(graph(fixture['n'],fixture['edges'])))
    local_solutions=[(edge,e0,e1) for edge in (0,1) for e0 in range(-2,2) for e1 in range(-2,2)
                     if e0+edge==1 and e1+edge==2]
    require(local_solutions==[(1,0,1)],'382/A/role1 local weighted cut')
    graphs=[graph(50,sorted(hs-deleted)) for deleted in (set(),{(0,1)},{(0,1),(2,3)})]
    graphs.append(graph(fixture['n'],fixture['edges']));weighted_rows=0
    for G in graphs:
        degrees=list(map(len,G));S=sum(d-6 for d in degrees)
        ss=[sum(degrees[u]-6 for u in ns) for ns in G]
        for v in range(len(G)):
            far=[u for u in range(len(G)) if u!=v and u not in G[v] and not G[u]&G[v]]
            require(sum(ss[u] for u in G[v])==S-ss[v]+(degrees[v]-1)*(degrees[v]-6)-sum(degrees[u]-6 for u in far),
                    'local weighted identity on actual graph')
            weighted_rows+=1
    prior=json.loads((HERE/'a0_expected.json').read_text())['inventory'];remaining=[row for row in prior['remaining_profiles'] if row[0] not in one]
    require(len(remaining)==53,'53 remaining necessary profiles')
    m5=[row for row in remaining if row[1]==5]
    require([r[0] for r in m5]==[372,373,377,378,386],'all five residual m5 profiles')
    mks={(x[1],x[2]) for x in remaining};forests=[f for f in prior['high_forests'] if (f['m'],f['k']) in mks]
    require(len(forests)==10,'ten remaining high forests')
    result={'one_quad_profiles':one,'human_excluded':[361,374,375,387],'sat_profiles':sat,'cases':cases,
            'second_covers':len(second),'third_covers':len(third),'helper_degree_orbits':orbit_records,
            'one_unit_charge_types':cost_one,'local_cut_solutions':local_solutions,'local_weighted_rows':weighted_rows,'controls':controls,'remaining_profiles':remaining,'remaining_high_forests':forests}
    result=json.loads(json.dumps(result));expected=HERE/'a0_one_quad_expected.json'
    if expected.exists():require(json.loads(expected.read_text())['finite_controls']==result,'complete entrywise expected comparison')
    print(json.dumps(result,sort_keys=True));return result

if __name__=='__main__':main()
