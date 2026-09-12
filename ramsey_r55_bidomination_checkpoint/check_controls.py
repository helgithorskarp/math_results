#!/usr/bin/env python3
"""Definition-level positive/negative controls for the complete-class formula.
Uses closed-neighborhood unions for domination, not common-neighbor tests.
This is an internal validation, not an independent mathematical review.
"""
import collections, itertools, json, time
from bi_domination import clauses,shape

def adj_control(name,n):
    if name.startswith('quadratic'):
        res={x*x%n for x in range(1,n)}
        return [set(v for v in range(n) if (u-v)%n in res) for u in range(n)]
    assert name=='C5_lex_C5' and n==25
    def adj(u,v):
        i,a=divmod(u,5);j,b=divmod(v,5)
        return ((a-b)%5 in (1,4)) if i==j else ((i-j)%5 in (1,4))
    return [set(v for v in range(n) if u!=v and adj(u,v)) for u in range(n)]

def check(name,n,expected_good,expected_both_gamma4):
    old=adj_control(name,n)
    q=next(t for t in itertools.combinations(range(n),4) if all(v in old[u] for u,v in itertools.combinations(t,2)))
    perm=list(q)+[v for v in range(n) if v not in q]
    adj=[set(v for v in range(n) if perm[v] in old[perm[u]]) for u in range(n)]
    universe=set(range(n));bar=[universe-adj[u]-{u} for u in range(n)]
    bad=[0,0];dom=[0,0]
    for color,g in enumerate((adj,bar)):
        for t in itertools.combinations(range(n),5):
            if all(v in g[u] for u,v in itertools.combinations(t,2)):bad[color]+=1
        closed=[g[u]|{u} for u in range(n)]
        for u,v,w in itertools.combinations(range(n),3):
            if closed[u]|closed[v]|closed[w]==universe:dom[color]+=1
    model=[False]+[v in adj[u] for u,v in itertools.combinations(range(n),2)]
    for color in (True,False):
        for t in itertools.combinations(range(n),3):
            for w in range(n):
                if w not in t:model.append(all((w in adj[u])==color for u in t))
    failed=collections.Counter();seen=0
    for c in clauses(n):
        seen+=1
        if not any(model[abs(x)]==(x>0) for x in c):failed[len(c)]+=1
    assert seen==shape(n)[1] and len(model)-1==shape(n)[0]
    assert failed[1]==failed[2]==0
    assert failed[10]==sum(bad) and failed[n-3]==sum(dom)
    assert (sum(bad)==0)==expected_good
    assert (sum(dom)==0)==expected_both_gamma4
    return {'name':name,'n':n,'monochromatic_five_sets_by_color':bad,'dominating_triples_by_color':dom,'failed_generated_clauses_by_width':dict(failed),'generated_clauses_evaluated':seen,'variables':shape(n)[0],'all_comparisons_passed':True}

start=time.monotonic()
results=[check('quadratic29',29,True,True),check('quadratic37',37,True,True),check('quadratic41',41,False,True),check('C5_lex_C5',25,True,False)]
print(json.dumps({'controls':results,'elapsed_seconds':time.monotonic()-start,'independent_peer_review':False},indent=2))
