#!/usr/bin/env python3
"""Standalone exact edge-capacity dual and graph verifier; no solver imports."""
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = HERE.parent/'ramsey_r55_k5_neutral_component/EXIT_GRAPH.json'
SEED_SHA = '9f4bd3853e985697f7fc496c0544f9d800235c2ece4a25cb718a2c3181559916'
V = frozenset(range(43))
C = frozenset(range(3,43))
EDGES = tuple(combinations(range(3,43),2))

def require(ok, message):
    if not ok:
        raise ValueError(message)

def integer(x):
    return type(x) is int

def digest(value):
    return hashlib.sha256((json.dumps(value,separators=(',',':'))+'\n').encode()).hexdigest()

def decode(doc):
    require(type(doc) is dict and set(doc)=={'format','red_adjacency_hex'},'graph schema')
    require(doc['format']=='r55-triple-degree-exact-mixed-graph-v1','graph format')
    text=doc['red_adjacency_hex']
    require(type(text) is list and len(text)==43,'graph row count')
    require(all(type(x) is str and x and all(c in '0123456789abcdef' for c in x) for x in text),'graph hex')
    rows=[int(x,16) for x in text]
    require(all(0<=r<1<<43 and not (r>>u&1) for u,r in enumerate(rows)),'graph range or loop')
    require(all((rows[u]>>v&1)==(rows[v]>>u&1) for u,v in combinations(range(43),2)),'graph asymmetry')
    return tuple(frozenset(v for v in range(43) if row>>v&1) for row in rows)

def mono_literal(adj):
    result=[[],[]]  # red, blue
    for S in combinations(range(43),5):
        first=S[1] in adj[S[0]]
        if all((v in adj[u])==first for u,v in combinations(S,2)):
            result[int(not first)].append(S)
    return tuple(tuple(g) for g in result)

def mono_recursive(adj,red):
    neighbors=adj if red else tuple(V-adj[u]-{u} for u in range(43))
    out=[]
    def visit(prefix,candidates):
        if len(prefix)==5:
            out.append(prefix)
            return
        if len(prefix)+len(candidates)<5:
            return
        for u in sorted(candidates):
            visit(prefix+(u,),{v for v in candidates if v>u}&neighbors[u])
    visit((),set(V))
    return tuple(out)

def all_fives(adj):
    result=mono_literal(adj)
    require(result==tuple(mono_recursive(adj,red) for red in (True,False)),'five-set algorithms disagree')
    return result

def local_profiles(adj):
    return tuple((sum(v in adj[u] for u,v in combinations(sorted(adj[e]),2)),
                  sum(v not in adj[u] for u,v in combinations(sorted(V-adj[e]-{e}),2))) for e in range(43))

def visible_edges(seed):
    # Definition as a union of six induced graphs, not a signature test.
    result=set()
    for root in range(3):
        for side in (seed[root],V-seed[root]-{root}):
            result.update(combinations(sorted(side&C),2))
    signatures=[sum(1<<e for e in range(3) if e in seed[u]) for u in range(43)]
    require(result=={(u,v) for u,v in EDGES if signatures[u]^signatures[v]!=7},'visibility identity')
    return result

@lru_cache(None)
def upper(a,b):
    if min(a,b)==1:
        return 1
    left,right=upper(a-1,b),upper(a,b-1)
    return left+right-int(left%2==right%2==0)

def check_pointwise(adj):
    count=0
    slacks=[]
    for assignment in product(range(3),repeat=3):
        A={u for u,w in enumerate(assignment) if w==1}
        B={u for u,w in enumerate(assignment) if w==2}
        if not A|B or any(v not in adj[u] for u,v in combinations(sorted(A),2)) or any(v in adj[u] for u,v in combinations(sorted(B),2)):
            continue
        S={u for u in V-A-B if A<=adj[u] and not B&adj[u]}
        for u in V-A-B:
            if A<=adj[u]:
                cap=upper(4-len(A),5-len(B))-1
                slacks.append(cap-len((S-{u})&adj[u]))
                count+=1
            if not B&adj[u]:
                cap=upper(5-len(A),4-len(B))-1
                slacks.append(cap-len((S-{u})-adj[u]))
                count+=1
    require(min(slacks)>=0,'pointwise inequality failed')
    require(count==884,'pointwise coverage')
    return {'rows':count,'minimum_slack':min(slacks)}

def check_seed(seed):
    require(tuple(map(len,seed))==(20,)*3+(21,)*40,'seed degrees')
    require(all(v in seed[u] for u,v in combinations(range(3),2)),'exceptional triangle')
    require(local_profiles(seed)[:3]==((92,107),)*3,'seed profiles')
    fives=all_fives(seed)
    require(tuple(map(len,fives))==(176,177),'seed K5 counts')
    require(all(min(S)>=3 for group in fives for S in group),'seed mixed K5')
    return fives

def verify_dual(seed,proof,objective):
    require(type(proof) is dict and set(proof)=={'denominator','cliques','degrees','profiles','upper_penalties'},'dual schema')
    D=proof['denominator']
    require(integer(D) and D>0,'dual denominator')
    loads={e:0 for e in EDGES}
    seen=set()
    total=0
    for entry in proof['cliques']:
        require(type(entry) is list and len(entry)==3,'clique row')
        red,S,a=entry
        require(integer(red) and red in (0,1) and type(S) is list and all(integer(v) for v in S)
                and len(S)==5 and S==sorted(set(S)) and set(S)<=C,'clique vertices or color')
        require(integer(a) and a>0,'clique weight')
        key=(red,tuple(S))
        require(key not in seen,'duplicate clique row')
        seen.add(key)
        require(all((v in seed[u])==bool(red) for u,v in combinations(S,2)),'nonmonochromatic dual clique')
        total+=a
        for e in combinations(S,2):
            loads[e]+=a
    degrees={}
    for entry in proof['degrees']:
        require(type(entry) is list and len(entry)==2,'degree row')
        u,b=entry
        require(integer(u) and u in C and integer(b) and b!=0 and u not in degrees,'degree multiplier')
        degrees[u]=b
    profiles={}
    for entry in proof['profiles']:
        require(type(entry) is list and len(entry)==3,'profile row')
        u,red,b=entry
        require(integer(u) and 0<=u<3 and integer(red) and red in (0,1) and integer(b) and b!=0
                and (u,red) not in profiles,'profile multiplier')
        profiles[u,red]=b
    for u,v in EDGES:
        sign=1 if v not in seed[u] else -1
        charge=degrees.get(u,0)+degrees.get(v,0)
        for (root,red),b in profiles.items():
            side=seed[root] if red else V-seed[root]-{root}
            if u in side and v in side:
                charge+=b
        loads[u,v]+=sign*charge
    penalties={}
    for entry in proof['upper_penalties']:
        require(type(entry) is list and len(entry)==3,'upper row')
        u,v,p=entry
        require(integer(u) and integer(v) and (u,v) in loads and integer(p) and p>0
                and (u,v) not in penalties,'upper penalty')
        penalties[u,v]=p
    visible=visible_edges(seed)
    residual=[D*int(objective=='total' or e in visible)-loads[e]+penalties.get(e,0) for e in EDGES]
    require(min(residual)>=0,'overloaded edge in dual')
    numerator=total-sum(penalties.values())
    require(numerator>0,'nonpositive bound')
    bound=Fraction(numerator,D)
    integer_bound=-(-bound.numerator//bound.denominator)
    if objective=='total':
        integer_bound+=integer_bound%2
    return {'bound':[bound.numerator,bound.denominator],'integer_bound':integer_bound,
            'weighted_cliques':len(seen),'sum_clique_weights':total,'denominator':D,
            'degree_equalities':len(degrees),'profile_equalities':len(profiles),
            'upper_penalties':len(penalties),'sum_upper_penalties':sum(penalties.values()),
            'minimum_edge_residual':min(residual),'maximum_edge_residual':max(residual),
            'canonical_edge_residual_sha256':digest(residual)}

def audit_witness(seed,new,old_fives):
    require(tuple(map(len,new))==tuple(map(len,seed)),'witness degrees')
    require(all(new[e]==seed[e] for e in range(3)),'exceptional incidences changed')
    require(local_profiles(new)[:3]==local_profiles(seed)[:3],'exceptional profiles changed')
    pointwise=check_pointwise(new)
    current=all_fives(new)
    require(all(not set(old)&set(after) for old,after in zip(old_fives,current)),'old K5 survives')
    flips=[e for e in EDGES if (e[1] in new[e[0]])!=(e[1] in seed[e[0]])]
    visible=visible_edges(seed)
    signatures=[tuple(sorted(seed[u]&{0,1,2})) for u in range(43)]
    def quotas(adj):
        return Counter(tuple(sorted((signatures[u],signatures[v]))) for u,v in EDGES if v in adj[u])
    before,after=quotas(seed),quotas(new)
    quota_changes=[[list(a),list(b),after[a,b]-before[a,b]] for a,b in sorted(set(before)|set(after)) if after[a,b]!=before[a,b]]
    return {'total_flips':len(flips),'visible_flips':len(set(flips)&visible),'unexposed_flips':len(set(flips)-visible),
            'removed_red':sum(v in seed[u] for u,v in flips),'added_red':sum(v not in seed[u] for u,v in flips),
            'edge_count':sum(map(len,new))//2,'pointwise':pointwise,
            'old_K5s_destroyed':list(map(len,old_fives)),'new_K5s':list(map(len,current)),
            'new_mixed_K5s':[sum(min(S)<3 for S in group) for group in current],
            'first_new_mixed_K5s':[next((S for S in group if min(S)<3),None) for group in current],
            'central_hard_cap_failures':sum(max(p)>100 for p in local_profiles(new)[3:]),
            'exceptional_profiles':local_profiles(new)[:3],'cell_quota_changes':quota_changes,
            'flipped_edges':flips,'canonical_new_K5_lists_sha256':digest(current),
            'status':'COVER_RELAXATION_WITNESS_ONLY; NOT a Ramsey graph or a mixed-free repair'}

def verify(certificate,graph,seed_path=SEED):
    require(hashlib.sha256(seed_path.read_bytes()).hexdigest()==SEED_SHA,'seed hash')
    seed=decode(json.loads(seed_path.read_text()))
    old_fives=check_seed(seed)
    require(type(certificate) is dict and set(certificate)=={'format','seed_sha256','visible','total'},'certificate schema')
    require(certificate['format']=='r55-visible-obstruction-cover-duals-v1'
            and certificate['seed_sha256']==SEED_SHA,'certificate provenance')
    duals={name:verify_dual(seed,certificate[name],name) for name in ('visible','total')}
    require(certificate['visible']['degrees']==[[u,12] for u in range(3,11)]+[[u,-12] for u in range(39,43)]
            and certificate['visible']['profiles']==[[0,1,-12],[0,0,12]],'displayed visible conservation identity')
    witness=audit_witness(seed,decode(graph),old_fives)
    require(duals['visible']['integer_bound']==witness['visible_flips'],'visible optimum not matched')
    require(duals['total']['integer_bound']<=witness['total_flips'],'total bound exceeds witness')
    return {'status':'VERIFIED_EXACT_VISIBLE_COVER_OPTIMUM','seed_sha256':SEED_SHA,
            'seed_K5s':list(map(len,old_fives)),'central_edges':len(EDGES),'visible_edges':len(visible_edges(seed)),
            'duals':duals,'witness':witness}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    ap.add_argument('--graph',type=Path,default=HERE/'GRAPH.json')
    ap.add_argument('--report',type=Path,required=True)
    args=ap.parse_args()
    report=verify(json.loads(args.certificate.read_text()),json.loads(args.graph.read_text()))
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':report['status'],'visible_optimum':report['witness']['visible_flips'],
                      'total_lower_bound':report['duals']['total']['integer_bound']}))

if __name__=='__main__':
    main()
