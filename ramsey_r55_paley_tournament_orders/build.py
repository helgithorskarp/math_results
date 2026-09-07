#!/usr/bin/env python3
"""Deterministic standard-library producer; no external SAT solver."""
import itertools as it
import json


def paley_rows(labels):
    Q={x*x % 43 for x in range(1,43)}
    return [[u!=v and (v-u)%43 in Q for v in labels] for u in labels]


def ordering_clauses(rows,red=4,blue=5,normalize=False):
    n=len(rows)
    ids={pair:i+1 for i,pair in enumerate(it.combinations(range(n),2))}
    def lt(u,v): return ids[u,v] if u<v else -ids[v,u]
    clauses=[]
    for a,b,c in it.combinations(range(n),3):
        clauses.extend([[-lt(a,b),-lt(b,c),lt(a,c)], [lt(a,b),lt(b,c),-lt(a,c)]])
    for k in sorted({red,blue}):
        for q in it.combinations(range(n),k):
            order=sorted(q,key=lambda v:-sum(rows[v][u] for u in q))
            if not all(rows[u][v] for u,v in it.combinations(order,2)): continue
            chain=[lt(u,v) for u,v in zip(order,order[1:])]
            if k==red: clauses.append([-x for x in chain])
            if k==blue: clauses.append(chain)
    if normalize: clauses.extend([[lt(0,v)] for v in range(1,n)])
    return clauses,ids


def kernel_orders(labels):
    n=len(labels); full=(1<<n)-1; arrows=paley_rows(labels)
    incoming=[sum(1<<u for u in range(n) if arrows[u][v]) for v in range(n)]
    outgoing=[full ^ (1<<v) ^ incoming[v] for v in range(n)]
    red=[0]*n; blue=[0]*n; orders=[]
    def clique(rows,mask,k):
        if k==0: return True
        if mask.bit_count()<k: return False
        if k==1: return bool(mask)
        while mask.bit_count()>=k:
            bit=mask&-mask; mask^=bit
            if clique(rows,mask & rows[bit.bit_length()-1],k-1): return True
        return False
    def visit(order,used):
        if len(order)==n: orders.append([labels[v] for v in order]); return
        available=full^used
        while available:
            bit=available&-available; available^=bit; v=bit.bit_length()-1
            r=used & incoming[v]; b=used & outgoing[v]
            if clique(red,r,2) or clique(blue,b,4): continue
            red[v]=r; blue[v]=b
            for u in order:
                if r>>u & 1: red[u]|=bit
                else: blue[u]|=bit
            visit(order+[v],used|bit)
            for u in order: red[u]&=~bit; blue[u]&=~bit
            red[v]=blue[v]=0
    visit([],0)
    return orders


def refute(clauses):
    nodes=[]; calls=[0]
    def visit(cs):
        calls[0]+=1
        if calls[0]>20000: raise RuntimeError('INCOMPLETE: proof production budget')
        while True:
            if any(not c for c in cs): return -1
            units={c[0] for c in cs if len(c)==1}
            if any(-x in units for x in units): return -1
            if not units: break
            cs=[tuple(x for x in c if -x not in units) for c in cs if not any(x in units for x in c)]
        if not cs: raise ValueError('satisfying leaf; not an exclusion')
        weights={}
        for c in cs:
            weight=1<<(8-min(8,len(c)))
            for x in c: weights[abs(x)]=weights.get(abs(x),0)+weight
        v=max(weights,key=lambda v:(weights[v],-v))
        left=visit(cs+[(v,)]); right=visit(cs+[(-v,)])
        nodes.append([v,left,right]); return len(nodes)-1
    root=visit([tuple(c) for c in clauses])
    return nodes,root


def produce():
    Q=sorted({x*x%43 for x in range(1,43)})
    A=sorted(set(Q)&{(1+x)%43 for x in Q})
    clauses,ids=ordering_clauses(paley_rows(Q),normalize=True)
    cases=[]
    for order in kernel_orders(A):
        extra=[]
        for a,b in zip(order,order[1:]):
            u,v=Q.index(a),Q.index(b)
            extra.append([ids[u,v] if u<v else -ids[v,u]])
        nodes,root=refute(clauses+extra)
        cases.append({'order':order,'nodes':nodes,'root':root})
    if len(cases)!=51: raise ValueError('unexpected kernel census')
    return {'schema':1,'prime':43,'squares':Q,'common_outneighbors':A,'cases':cases}


if __name__=='__main__':
    print(json.dumps(produce(),sort_keys=True,separators=(',',':')))
