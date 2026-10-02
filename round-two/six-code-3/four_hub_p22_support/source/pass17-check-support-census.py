"""Separate necessary polynomial check, literal semantic and symmetry audits.

No author producer import. Lambda carriers come from bounded sum
recursion, and the light action is forward relabeling, rather than the
producer's backwards lookup. Repeated type factors are weak compositions,
not successive one-center state products. For a fixed deficit pattern,
coordinatewise minima of the support lower bounds give an EVEN WEAKER
relaxation. Its emptiness suffices, including the two-positive-hub type26.
"""
import hashlib
import itertools
import json
import time
from pathlib import Path

S=Path('round-two/six-code-3/scratch')
R=Path('round-two/six-code-3/four_hub_p21_endpoint_cut')
P=list(itertools.combinations(range(4),2))
T=list(itertools.combinations(range(4),3))

def need(c,m):
    if not c:raise ValueError(m)

def bounded_sum(total,n):
    if n==0:
        if total==0:yield ()
        return
    for x in range(max(0,total-5*(n-1)),min(5,total)+1):
        for tail in bounded_sum(total-x,n-1):yield (x,)+tail

def forward(triple,lam,mapping):
    new=[None]*6
    for old,pair in enumerate(P):
        new[P.index(tuple(sorted(mapping[a] for a in pair)))]=lam[old]
    return tuple(sorted(mapping[a] for a in triple)),tuple(new)

def carriers(triple_domain):
    raw=set()
    for tri in triple_domain:
        for lam in bounded_sum(21,6):
            leaves=tuple(14+int(all(a in tri for a in pair))-3*l for pair,l in zip(P,lam))
            D=tuple(sum(lam[i] for i,pair in enumerate(P) if a in pair)-(2 if a==0 else 6) for a in range(4))
            if min(leaves)<0 or max(leaves)>14 or min(D)<0:continue
            raw.add((tuple(tri),lam))
    groups={}
    for tri,lam in sorted(raw):
        orbit={forward(tri,lam,(0,)+p) for p in itertools.permutations((1,2,3))}
        need(orbit<=raw,'light relabeling leaves literal carrier')
        key=min(orbit)
        groups.setdefault(key,set()).add((tri,lam))
    for key,orbit in groups.items():
        need(orbit=={forward(*key,(0,)+p) for p in itertools.permutations((1,2,3))},'full joint light orbit')
    return groups

def physical_audit(rows,types,fixtures):
    checks=0
    for row in rows:
        w=row['witness'];roles=w['hub_roles'];blocks=[set(q) for q in fixtures[w['fixture']]]
        need(len(roles)==len(set(roles))==4,'four distinct physical roles')
        rep=[sum(p in q for q in blocks) for p in range(17)]
        d=[5-r for r in rep];high={p for p in range(17) if d[p]};H=set(roles)
        leave={(a,b) for a,b in itertools.combinations(range(17),2) if not any({a,b}<=q for q in blocks)}
        high_leave={edge for edge in leave if set(edge)<=high}
        q=sum(bool(set(edge)&H) for edge in high_leave)
        need(q==types[row['type_id']]['q'],'literal q semantics')
        need([d[p] for p in roles]==row['hub_deficits'],'literal ordered deficits')
        mask=sum(1<<i for i,(a,b) in enumerate(P) if tuple(sorted((roles[a],roles[b]))) in leave)
        need(mask==row['HH_leave_mask'],'literal HH leaves')
        for a,point in enumerate(roles):
            if not d[point]:continue
            neighbors={b if c==point else c for c,b in leave if point in (c,b)}
            need(len(neighbors)==1+3*d[point],'literal local leave degree')
            low_sat=neighbors-high-H
            hh=sum(bool(mask>>i&1) for i,p in enumerate(P) if a in p)
            bound=1+3*d[point]-hh-q
            need(bound<=len(low_sat),'ordinary support lower bound exceeds actual friends')
            checks+=1
    return checks

def local_factor(options,n,target):
    # For equal d-patterns the separate coordinate minima are a necessary
    # super-relaxation; they need not share a single physical witness.
    minimum={}
    for d,lb in options:
        minimum[d]=tuple(min(a,b) for a,b in zip(minimum.get(d,lb),lb))
    patterns=sorted((d,lb) for d,lb in minimum.items() if all(lb[a]<=target[a] for a in range(4)))
    output=set()
    def distribute(i,left,D,N,req):
        if i==len(patterns):
            if left==0:output.add(D+N+req)
            return
        d,lb=patterns[i]
        for amount in range(left+1):
            dd=tuple(D[a]+amount*d[a] for a in range(4))
            if any(dd[a]>target[a] for a in range(4)):break
            nn=tuple(N[a]+amount*int(d[a]>0) for a in range(4))
            rr=tuple(max(req[a],lb[a] if amount else 0) for a in range(4))
            distribute(i+1,left-amount,dd,nn,rr)
    distribute(0,n,(0,)*4,(0,)*4,(0,)*4)
    return output

def run_one(pop,groups,rows,types):
    start=time.monotonic();visited=0;answer=[]
    for tri,lam in sorted(groups):
        leave=tuple(14+int(all(a in tri for a in p))-3*l for p,l in zip(P,lam))
        target=tuple(sum(lam[i] for i,p in enumerate(P) if a in p)-(2 if a==0 else 6) for a in range(4))
        tmask=1<<T.index(tri) if tri else 0
        factors=[]
        for typ,n in pop:
            opts=set()
            for row in rows:
                if row['type_id']!=typ or row['HHH_covered_mask'] not in (0,tmask):continue
                if any(not leave[i] and row['HH_leave_mask']>>i&1 for i in range(6)):continue
                d=tuple(row['hub_deficits'])
                lb=tuple(2+3*d[a]-sum(bool(row['HH_leave_mask']>>i&1) for i,p in enumerate(P) if a in p)-types[typ]['q']
                         if d[a] else 0 for a in range(4))
                opts.add((d,lb))
            factors.append(local_factor(opts,n,target))
        factors.sort(key=len)
        poly={(0,)*12}
        for factor in factors:
            nxt=set()
            for x in poly:
                for y in factor:
                    D=tuple(x[a]+y[a] for a in range(4))
                    if any(D[a]>target[a] for a in range(4)):continue
                    N=tuple(x[4+a]+y[4+a] for a in range(4))
                    req=tuple(max(x[8+a],y[8+a]) for a in range(4))
                    nxt.add(D+N+req);visited+=1
                    need(visited<=500000 and time.monotonic()-start<=20,'INCOMPLETE fixed checker guard; no absence')
            poly=nxt
        valid=sorted(x for x in poly if x[:4]==target and all(x[4+a]>=x[8+a] for a in range(4)))
        if valid:answer.append(dict(triple=list(tri),pair_replications=list(lam),states=valid))
    return dict(carriers=len(groups),visited=visited,surviving_states=answer,elapsed_seconds=time.monotonic()-start)

def main():
    rows=json.loads((S/'pass16-hub-role-catalogue.json').read_text())['records']
    types=json.loads((R/'expected.json').read_text())['types']
    fixtures=json.loads((R/'fixtures.json').read_text())['stars']
    semantics=physical_audit(rows,types,fixtures)
    groups={0:carriers([()]),1:carriers(T)}
    # Full physical table closure is required for the joint light orbit.
    table={(r['type_id'],tuple(r['hub_deficits']),r['HH_leave_mask'],r['HHH_covered_mask']) for r in rows}
    transports=0
    for r in rows:
        for perm in itertools.permutations((1,2,3)):
            p=(0,)+perm;inv=tuple(p.index(a) for a in range(4))
            d=tuple(r['hub_deficits'][inv[a]] for a in range(4))
            hh=sum(1<<P.index(tuple(sorted(p[a] for a in pair))) for i,pair in enumerate(P) if r['HH_leave_mask']>>i&1)
            hhh=sum(1<<T.index(tuple(sorted(p[a] for a in tri))) for i,tri in enumerate(T) if r['HHH_covered_mask']>>i&1)
            need((r['type_id'],d,hh,hhh) in table,'actual signature forward light closure')
            transports+=1
    populations=json.loads((S/'pass16-p21-unit-graphs.json').read_text())['survivors']
    first=json.loads((S/'pass17-support-census-exact.json').read_text())['records']
    records=[]
    for r in populations:
        checked=run_one(r['population'],groups[r['branch'][1]],rows,types)
        other=next(x for x in first if x['ordinal']==r['ordinal'])
        need(other['status']=='COMPLETE_SUPPORT_CENSUS','producer incomplete')
        need(checked['carriers']==other['tested_lambdas'],'every joint canonical carrier differs')
        need(not checked['surviving_states'] and not other['surviving_ordered_states'],'nonempty necessary support census')
        checked.update(ordinal=r['ordinal'],population=r['population'],branch=r['branch'])
        records.append(checked)
        print(json.dumps({k:v for k,v in checked.items() if k!='surviving_states'},sort_keys=True),flush=True)
    result=dict(agent='six-code-3',role='researcher',status='PRIVATE_TWO_ALGORITHM_COMPLETE_SUPPORT_EMPTINESS',records=records,
                literal_high_hub_friend_audits=semantics,forward_physical_light_transports=transports,
                carrier_statistics={str(t):dict(raw=sum(map(len,g.values())),orbits=len(g),orbit_sizes=dict(sorted(__import__('collections').Counter(map(len,g.values())).items()))) for t,g in groups.items()},
                coordinatewise_minimum_is_weaker_necessary_relaxation=True,ordinary_bridge_formalized=False,
                independent_peer_review=False,new_pair_total_claim=None)
    out=S/'pass17-independent-support.json';need(not out.exists(),'fresh independent support output')
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},sort_keys=True))

if __name__=='__main__':main()
