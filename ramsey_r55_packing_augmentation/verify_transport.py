"""Separate certificate verifier; imports no transport producer."""
from itertools import combinations
import hashlib
import json
import sys

def check(source, certificate):
    def need(x, why):
        if not x:
            raise ValueError(why)
    def graph(obj):
        n = obj['n']; h = obj['red_hex']
        need(type(n) is int and 8 <= n <= 43, 'n')
        need(type(h) is str and len(h)==(n*(n-1)//2+3)//4 and all(c in '0123456789abcdef' for c in h), 'hex')
        w = int(h,16)
        need(w < 2**(n*(n-1)//2), 'padding')
        return {p:(w>>k)&1 for k,p in enumerate(combinations(range(n),2))}
    def edge(g,u,v):
        return g[tuple(sorted((u,v)))]
    def packing(obj,g):
        n,r = obj['n'],obj['r']; bs=obj['blocks']; core=obj['core']
        need(type(r) is int and 1<=r<=len(bs), 'r')
        need(all(len(b)==4 for b in bs), 'block size')
        flat=[v for b in bs for v in b]+core
        need(all(type(v) is int for v in flat) and sorted(flat)==list(range(n)), 'partition')
        for i,b in enumerate(bs):
            need(all(edge(g,u,v)==int(i<r) for u,v in combinations(b,2)), 'block color')
        for s in combinations(core,4):
            need(len({edge(g,u,v) for u,v in combinations(s,2)})==2, 'core')
        remaining=[v for b in bs[r:] for v in b]+core
        need(all(any(edge(g,u,v)==0 for u,v in combinations(s,2)) for s in combinations(remaining,4)), 'maximality')
    need(certificate['status']=='PACKING_TRANSPORT_NEEDS_CATALOG_AND_ROOT_ORDER','status')
    expected=hashlib.sha256(json.dumps(source,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    need(certificate['source_sha256']==expected,'binding')
    dest=certificate['output']; a=graph(source); b=graph(dest)
    packing(source,a); packing(dest,b)
    p=certificate['new_to_old']; n=source['n']
    need(dest['n']==n and all(type(v) is int for v in p) and sorted(p)==list(range(n)), 'bijection')
    need(all(b[i,j]==edge(a,p[i],p[j]) for i,j in combinations(range(n),2)), 'physical edge transport')
    old=source['blocks']; new=[frozenset(p[v] for v in block) for block in dest['blocks']]
    r=source['r']; ix=certificate['replaced_block']
    need(type(ix) is int and 0<=ix<r,'replaced index')
    need(dest['r']==r+1 and len(new)==len(old)+1,'packing increase')
    certified=[frozenset(x) for x in certificate['new_blocks_old_labels']]
    need(len(certified)==2 and all(len(s)==4 for s in certified) and not certified[0]&certified[1],'new disjoint fours')
    expected_blocks=[frozenset(v) for j,v in enumerate(old[:r]) if j!=ix]+certified+[frozenset(v) for v in old[r:]]
    need(new==expected_blocks,'block replacement')
    oldblock=set(old[ix]); consumed=(set.union(*(set(x) for x in certified))-oldblock)
    need(len(consumed)==4 and consumed<=set(source['core']), 'consumed core vertices')
    need(all(len(set(x)&oldblock)==2 for x in certified),'two plus two')
    need({p[v] for v in dest['core']}==set(source['core'])-consumed,'core shrink')
    return {'status':'PHYSICAL_PACKING_TRANSPORT_VERIFIED_NO_RAMSEY_VERDICT','edges':n*(n-1)//2}

if __name__=='__main__':
    print(json.dumps(check(json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))),sort_keys=True))
