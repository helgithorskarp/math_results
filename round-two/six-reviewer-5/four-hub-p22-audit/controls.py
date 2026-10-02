"""Nonvacuous support/count controls and exhaustive small distinct-edge flows."""
from independent import *
from unit_flow import flow
from support import convolution,carriers,permute_carrier

def compute():
    # A positive exact-sum polynomial, followed by failures due to insufficient
    # support and a missing deficit quota. N counts centers, never deficit mass.
    simple={0:[((2,0,0,0),(1,0,0,0),(2,0,0,0))]}
    positive=convolution([2],simple,(4,0,0,0));need(positive['retained']==1,'nonempty support kernel control')
    highbound={0:[((2,0,0,0),(1,0,0,0),(3,0,0,0))]}
    negative=convolution([2],highbound,(4,0,0,0));need(negative['retained']==0,'support two is below three though deficit mass four')
    wrongquota=convolution([2],simple,(3,0,0,0));need(wrongquota['retained']==0,'exact integer deficit quota control')
    # All2x3 simple allowed graphs, right endpoint capacities0..2 and left
    # demands0..2. Subset Hall arithmetic independently checks exact max flow.
    flow_checks=0
    for mask in range(64):
        allowed=[(u,c) for u in range(2) for c in range(3) if mask>>(3*u+c)&1]
        for cap in it.product(range(3),repeat=3):
            for demand in it.product(range(3),repeat=2):
                hall=all(sum(demand[u] for u in range(2) if J>>u&1)<=sum(min(cap[c],sum((u,c) in allowed for u in range(2) if J>>u&1)) for c in range(3)) for J in range(4))
                need((flow(cap,allowed,demand)==sum(demand))==hall,'whole small-network maxflow versus all Hall subsets')
                flow_checks+=1
    support=json.loads((P/'independent-support.json').read_text());sigs=support['selected_signatures'];lookup={tuple_key(s['signature']):s['frequency'] for s in sigs};transports=0
    for row in sigs:
        typ,d,hh,hhh,wc,iso=row['signature']
        for p in [(0,)+q for q in it.permutations((1,2,3))]:
            nd=[0]*4
            for a in range(4):nd[p[a]]=d[a]
            nh=sum(1<<PAIRS.index(tuple(sorted((p[a],p[b])))) for j,(a,b) in enumerate(PAIRS) if hh>>j&1)
            nt=sum(1<<TRIPLES.index(tuple(sorted(p[a] for a in t))) for j,t in enumerate(TRIPLES) if hhh>>j&1)
            ni=sum(1<<p[a] for a in range(4) if iso>>a&1)
            need(lookup[tuple_key((typ,nd,nh,nt,wc,ni))]==row['frequency'],'every projected signature frequency transported under all light bijections')
            transports+=1
    carrier_counts=[]
    for T in (0,1):
        raw=carriers(T)
        actual=[r for r in raw if r[0] is None or all(l>=1 for pair,l in zip(PAIRS,r[1]) if set(pair)<=set(TRIPLES[r[0]]))]
        perms=[(0,)+q for q in it.permutations((1,2,3))]
        orbits={min(permute_carrier(r,p) for p in perms) for r in actual}
        carrier_counts.append({'T':T,'all_audited_raw':len(raw),'covered_triple_pairs_positive':len(actual),'proper_orbits_diagnostic':len(orbits),'extra_relaxed_carriers':len(raw)-len(actual)})
    result={'positive_support_control':positive,'negative_support_vs_mass_control':negative,'negative_exact_quota_control':wrongquota,'whole2x3flow_Hall_controls':flow_checks,'every_signature_light_transport':transports,'carrier_counts':carrier_counts}
    (P/'independent-controls.json').write_bytes(enc(result));print(json.dumps({'flow_checks':flow_checks,'transports':transports,'carrier_counts':carrier_counts,'sha256':sha(result)}),flush=True)
    return result

def tuple_key(s):
    typ,d,hh,hhh,wc,iso=s;return typ,tuple(d),hh,hhh,tuple(wc),iso
if __name__=='__main__':compute()
