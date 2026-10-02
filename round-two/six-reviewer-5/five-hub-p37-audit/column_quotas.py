"""Consequential new local placement refinements from ordered column caps.
All23 literal stars/full5-hub placements; no claim of packing realization.
"""
import itertools as it,math,json,pathlib,collections
import audit as a
P=pathlib.Path(__file__).resolve().parent

def run(before=None,controls=None):
    stars=json.loads((P/'fixtures.json').read_text())['stars'];raw,capped,types=a.c.raw_and_types(stars)
    if before is None:before=json.loads((P/'core-record.json').read_text())
    if controls is None:controls=json.loads((P/'controls-record.json').read_text())
    out=[]
    for cap,label in [(7,'P36'),(8,'P37'),(5,'P36_T1')]:
      count=collections.Counter();physical=0;groups=[]
      for fi,star in enumerate(stars):
       cover={tuple(sorted(e)) for b in star for e in it.combinations(b,2)}
       d=[5-sum(p in b for b in star) for p in range(17)];high=[p for p in range(17) if d[p]]
       friends={p:{q for q in range(17) if not d[q] and tuple(sorted((p,q))) not in cover} for p in high}
       deg={p:sum(tuple(sorted((p,q))) not in cover for q in high if q!=p) for p in high}
       groups.append((d,high,friends,deg))
       for hh in it.combinations(range(17),5):
        physical+=1;H=set(hh)
        if all(d[p]+len(friends[p]-H)<=(cap if p in H else 5) for p in high):count[fi,tuple(p for p in high if p in H)]+=1
      records=[];allowed=[];good=0
      for r in raw:
       d,high,friends,deg=groups[r['star']];H=set(r['hubs']);n=5-len(H)
       req={p:max(0,1+4*d[p]-deg[p]-(cap if p in H else 5)) for p in high}
       # Full binomial bucket product independently reconstructs EVERY count.
       coeff=[1]+[0]*n
       for p in high:
        nxt=[0]*(n+1)
        for used,value in enumerate(coeff):
         for j in range(req[p],min(len(friends[p]),n-used)+1):nxt[used+j]+=value*math.comb(len(friends[p]),j)
        coeff=nxt
       direct=count[r['star'],tuple(r['hubs'])]
       a.need(coeff[n]==direct and bool(direct)==(sum(req.values())<=n),'each column-cap mark full placement and binomial counts')
       records.append([r['star'],r['hubs'],[[p,req[p]] for p in high],direct])
       if direct:
        good+=1;sat=[p for p in high if p not in H]
        allowed.append(tuple([r[k] for k in a.c.FIELDS[:5]]+[sum(d[p]==1 for p in sat),sum(d[p]==2 for p in sat),r['psi'],r['I5'],r['margin']]))
        a.need(all(d[p]<=2 for p in sat) and all(d[p]<=3 for p in H),'new physical filter respects old pair caps')
      allowed=sorted(set(allowed));total=0
      for case in before['all_cases']:
       if label=='P36_T1' and case['T']!=1:continue
       for row in case['vectors']:
        if all(tuple(t) in allowed for t,n in row['population']):total+=1
      out.append(dict(scope=label,column_cap=cap,full_physical_placements=physical,positive_abstract_local_placements=sum(count.values()),positive_marks=good,types=allowed,
       full_426_mark_quotas_and_exact_counts_sha256=a.digest(records),retained_P36_vectors=(None if label=='P37' else total),
       positive_local_types_are_not_actual_codes=True))
    # Read physical arbitrary-color graph control rather than assuming metrics.
    x=controls['graph']['arbitrary_nonunit_color_control']
    adj=[set() for _ in x['roles']];c1=[0]*len(adj)
    for u,v,col in x['edges']:
      adj[u].add(v);adj[v].add(u)
      if col==1:c1[u]+=1;c1[v]+=1
    units={i for i,r in enumerate(x['roles']) if r in 'AV'};eligible={i for i,r in enumerate(x['roles']) if r in 'VB'}
    A={i for i,r in enumerate(x['roles']) if r=='A'};C={i for i,r in enumerate(x['roles']) if r=='C'};V=units-A
    a.need(all(not adj[u]&eligible for u in units),'actual arbitrary-color prohibition')
    a.need(all(col==1 for u,v,col in x['edges'] if u in units or v in units),'actual unit colors')
    roots=[r for r in A if {r}|adj[r]|set().union(*(adj[u] for u in adj[r]))==set(range(len(adj)))]
    DV=sum(len(adj[u]) for u in V);C1=sum(c1[u] for u in C)
    a.need(C1==DV+len(roots)==3,'actual color3 support graph endpoint equality')
    return dict(agent='six-reviewer-5',role='independent mathematical reviewer',after_initial_core_seal=True,new_general_column_identity_and_ordinary_caps_proved=True,
      placements=out,actual_arbitrary_color_graph_metrics=dict(DV=DV,R=len(roots),C1=C1))
if __name__=='__main__':
    r=run();(P/'column-quotas-record.json').write_bytes(a.encode(r));print(json.dumps({**r,'placements':[{k:v for k,v in row.items() if k!='types'} for row in r['placements']]},indent=2));print('sha256',a.digest(r))
