#!/usr/bin/env python3
"""Catalog-based discovery census and complete separator arithmetic."""
import hashlib
import json
from itertools import combinations, combinations_with_replacement, product, permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent

def require(value, message):
    if not value:
        raise ValueError(message)

def graph6(line):
    n = ord(line[0]) - 63
    require(1 <= n <= 62, 'unsupported graph6 order')
    bits = ''.join(f'{ord(c)-63:06b}' for c in line[1:])
    require(len(line) == 1 + (n*(n-1)//2+5)//6, 'graph6 length')
    require(all(63 <= ord(c) <= 126 for c in line), 'graph6 alphabet')
    require('1' not in bits[n*(n-1)//2:], 'nonzero graph6 padding')
    adj = [0] * n
    for k, (u, v) in enumerate(( (u,v) for v in range(n) for u in range(v))):
        if bits[k] == '1':
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    return adj

def independent(adj, vertices):
    return all(not (adj[u] >> v & 1) for u,v in combinations(vertices, 2))

def packed(adj):
    return sum((adj[u] >> v & 1) << k for k,(u,v) in enumerate(combinations(range(len(adj)),2)))

def census():
    raw = (HERE/'r35_12.g6').read_bytes()
    rows = []
    for index,line in enumerate(raw.decode('ascii').splitlines()):
        a = graph6(line)
        require(len(a) == 12, 'wrong catalog order')
        require(not any(all(a[u]>>v&1 for u,v in combinations(q,2)) for q in combinations(range(12),3)), 'triangle in catalog')
        require(not any(independent(a,q) for q in combinations(range(12),5)), 'independent five in catalog')
        i4 = [q for q in combinations(range(12),4) if independent(a,q)]
        special = [list(q) for q in i4 if not any(set(t).isdisjoint(q) for t in i4)]
        rows.append({'index':index, 'code':packed(a), 'independent_fours':len(i4), 'special_fours':special})
    require(len(rows) == 12, 'catalog count')
    return {'sha256':hashlib.sha256(raw).hexdigest(),'rows':rows}

def arithmetic():
    cap = {1:4,2:13,3:24}
    rows = set()
    for k in range(19):
        for length in range(2,5):
            for alphas in product(range(1,4), repeat=length):
                if sum(alphas)>4:
                    continue
                ranges = [range(max(alpha,19-k),cap[alpha]+1) for alpha in alphas]
                for sizes in product(*ranges):
                    if sum(sizes) != 43-k:
                        continue
                    rows.add((k,tuple(sorted(zip(sizes,alphas)))))
    result = []
    for k,types in sorted(rows):
        if any(a>=2 and alpha==1 for a,alpha in types):
            a = next(a for a,alpha in types if a>=2 and alpha==1)
            status = 'clique_common_neighborhood'
            detail = {'a':a,'lower':a*(19-a)-(a-1)*k,'upper':{2:13,3:4,4:0}[a]}
            require(detail['lower']>detail['upper'],'failed clique inequality')
        elif types == ((13,2),(13,2)):
            status,detail = 'two_thirteen_components',{}
        elif types == ((12,2),(13,2)):
            status,detail = 'unique_twelve_attachment',{}
        elif k==18 and types==((1,1),(24,3)):
            status,detail = 'allowed_singleton_boundary',{}
        else:
            raise ValueError(('uncovered profile',k,types))
        result.append({'separator_size':k,'component_types':[list(x) for x in types],'reason':status,**detail})
    return result

def certificate():
    return {'schema':'separator18-v1','claim':'Every separator of size at most18 in good43 has size18 and components1,24; it is the neighborhood of its isolated degree18 vertex.', 'catalog_crosscheck':census(), 'component_profiles':arithmetic()}

if __name__ == '__main__':
    print(json.dumps(certificate(),indent=2,sort_keys=True))
