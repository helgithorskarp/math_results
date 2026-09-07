"""Independent certificate checker: full permutations, physical arrows, Boolean UP."""
import hashlib
from functools import lru_cache
import itertools as it
import json
from pathlib import Path
import sys


def need(ok,reason):
    if not ok: raise ValueError(reason)


def integer(x,lo,hi):
    return type(x) is int and lo<=x<=hi


def arrow(u,v):
    return u!=v and pow((v-u)%43,21,43)==1


def transitive_order(labels):
    # Remove a source repeatedly, independently of producer score sorting.
    left=list(labels); order=[]
    while left:
        choices=[u for u in left if all(u==v or arrow(u,v) for v in left)]
        if len(choices)!=1: return None
        u=choices[0]; order.append(u); left.remove(u)
    return order


@lru_cache(maxsize=4)
def all_kernel_orders(A):
    # Direct complete permutation census; no prefix pruning or producer code.
    triples=[]; fives=[]
    for k,seqs in [(3,triples),(5,fives)]:
        for q in it.combinations(range(10),k):
            # Try physical orders locally, independent of source elimination.
            for order in it.permutations(q):
                if all(arrow(A[u],A[v]) for u,v in it.combinations(order,2)):
                    seqs.append(order); break
    good=[]; total=redfree=0
    for order in it.permutations(range(10)):
        total+=1; pos=[0]*10
        for i,v in enumerate(order): pos[v]=i
        if any(pos[a]<pos[b]<pos[c] for a,b,c in triples): continue
        redfree+=1
        if any(pos[a]>pos[b]>pos[c]>pos[d]>pos[e] for a,b,c,d,e in fives): continue
        good.append([A[v] for v in order])
    return good,{'permutations':total,'red_triangle_free_orders':redfree,
                 'admissible_orders':len(good),'transitive_triples':len(triples),
                 'transitive_fives':len(fives)}


def formula(Q):
    ids={pair:i+1 for i,pair in enumerate(it.combinations(Q,2))}
    def lt(u,v): return ids[u,v] if u<v else -ids[v,u]
    clauses=[]
    for a,b,c in it.combinations(Q,3):
        clauses.append([-lt(a,b),-lt(b,c),lt(a,c)])
        clauses.append([lt(a,b),lt(b,c),-lt(a,c)])
    counts=[]
    for k,sign in [(4,-1),(5,1)]:
        number=0
        for q in it.combinations(Q,k):
            ordered=transitive_order(q)
            if ordered is None: continue
            number+=1
            clauses.append([sign*lt(a,b) for a,b in zip(ordered,ordered[1:])])
        counts.append(number)
    clauses.extend([[lt(1,v)] for v in Q if v!=1])
    return clauses,ids,counts


def propagation(clauses,values):
    """Scan original clauses; separate Boolean valuation, no clause deletion."""
    values=values.copy()
    while True:
        changed=False
        for clause in clauses:
            pending=[]
            for lit in clause:
                v=abs(lit); value=values[v]
                if value and (value>0)==(lit>0): break
                if not value: pending.append(lit)
            else:
                if not pending: return None
                if len(pending)==1:
                    lit=pending[0]; values[abs(lit)]=1 if lit>0 else -1; changed=True
        if not changed: return values


def check_tree(clauses,case,nv):
    need(type(case) is dict and set(case)=={'order','nodes','root'},'case fields')
    nodes=case['nodes']; root=case['root']
    need(type(nodes) is list and integer(root,-1,len(nodes)-1),'tree root')
    need(root==len(nodes)-1,'root must be last')
    for i,node in enumerate(nodes):
        need(type(node) is list and len(node)==3,'tree node')
        v,a,b=node
        need(integer(v,1,nv) and integer(a,-1,i-1) and integer(b,-1,i-1),'branch variable/children')
    seen=set(); leaves=[0]
    def visit(index,values):
        out=propagation(clauses,values)
        if index==-1:
            need(out is None,'noncontradictory leaf'); leaves[0]+=1; return
        need(out is not None,'unnecessary node')
        need(index not in seen,'tree node reused'); seen.add(index)
        v,a,b=nodes[index]
        need(out[v]==0,'branch already assigned')
        for value,child in [(1,a),(-1,b)]:
            trial=out.copy(); trial[v]=value; visit(child,trial)
    visit(root,[0]*(nv+1))
    need(seen==set(range(len(nodes))),'unreachable nodes')
    return len(nodes),leaves[0]


def verify(cert):
    need(type(cert) is dict and set(cert)=={'schema','prime','squares','common_outneighbors','cases'},'certificate fields')
    need(integer(cert['schema'],1,1) and integer(cert['prime'],43,43),'schema/prime')
    Q=[v for v in range(1,43) if arrow(0,v)]
    need(Q==cert['squares'] and all(type(v) is int for v in cert['squares']),'squares')
    need(len(Q)==21 and all(arrow(u,v)!=arrow(v,u) for u,v in it.combinations(range(43),2)),'physical tournament')
    need(all(arrow(u,v)==arrow((a+u)%43,(a+v)%43)
             for a in range(43) for u,v in it.combinations(range(43),2)),'translations')
    need(all(sorted(a*v%43 for v in Q)==Q for a in Q),'multiplicative action on Q')
    need(all(arrow(u,v)==arrow(a*u%43,a*v%43)
             for a in Q for u,v in it.combinations(range(43),2)),'square multipliers')
    need(all(arrow(u,v)!=arrow((-u)%43,(-v)%43)
             for u,v in it.combinations(range(43),2)),'negation reverses arrows')
    A=[v for v in Q if arrow(1,v)]
    need(A==cert['common_outneighbors'] and all(type(v) is int for v in cert['common_outneighbors']) and len(A)==10,'common neighbors')
    orders,census=all_kernel_orders(tuple(A))
    cases=cert['cases']
    need(type(cases) is list and len(cases)==51,'case count')
    need(all(type(c) is dict and type(c.get('order')) is list and
             all(type(v) is int for v in c['order']) for c in cases),'case orders')
    need([c['order'] for c in cases]==orders,'incomplete/incorrect order census')
    cs,ids,counts=formula(Q)
    def lt(u,v): return ids[u,v] if u<v else -ids[v,u]
    branches=leaves=0; branch_counts=[]
    for case in cases:
        extra=[[lt(a,b)] for a,b in zip(case['order'],case['order'][1:])]
        b,l=check_tree(cs+extra,case,len(ids)); branches+=b; leaves+=l; branch_counts.append(b)
    return {'status':'VERIFIED_PALEY43_ORDERING_OBSTRUCTION','local_vertices':Q,'kernel_vertices':A,
            'census':census,'local_variables':len(ids),'local_clauses':len(cs),
            'transitive_four_five_counts':counts,'branch_counts':branch_counts,
            'total_branches':branches,'total_contradiction_leaves':leaves,
            'guaranteed_distinct_monochromatic_fives':2,'ramsey43_constructed':False,
            'ramsey_bound_improved':False}


if __name__=='__main__':
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('certificate.json')
    result=verify(json.loads(path.read_text()))
    result['certificate_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps(result,sort_keys=True,indent=2))
