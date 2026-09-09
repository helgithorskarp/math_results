"""Physical packing witness transport. No Ramsey verdict or target task index."""
from itertools import combinations
import hashlib
import json
import re
import sys

def need(x, why):
    if not x:
        raise ValueError(why)

def decode(obj):
    n = obj['n']
    need(type(n) is int and 8 <= n <= 43, 'order')
    h = obj['red_hex']
    need(type(h) is str and re.fullmatch('[0-9a-f]+', h) and len(h) == (n*(n-1)//2+3)//4, 'word format')
    word = int(h, 16)
    need(word < 1 << (n*(n-1)//2), 'word padding')
    a = [set() for _ in range(n)]
    for k, (i,j) in enumerate(combinations(range(n),2)):
        if word >> k & 1:
            a[i].add(j)
            a[j].add(i)
    return a

def mono(a, vertices, color):
    return all((v in a[u]) == color for u,v in combinations(vertices,2))

def validate(obj):
    a = decode(obj)
    blocks, core, r = obj['blocks'], obj['core'], obj['r']
    need(type(r) is int and 1 <= r <= len(blocks), 'red block count')
    need(type(core) is list and all(type(b) is list and len(b)==4 for b in blocks), 'partition shape')
    flat = sum(blocks, []) + core
    need(all(type(x) is int for x in flat) and sorted(flat) == list(range(len(a))), 'partition')
    need(all(mono(a,b,i<r) for i,b in enumerate(blocks)), 'block color')
    need(all(not mono(a,s,c) for s in combinations(core,4) for c in (False,True)), 'core Ramsey(4,4)')
    remainder = sum(blocks[r:], [])+core
    need(all(not mono(a,s,True) for s in combinations(remainder,4)), 'red maximality')
    return a

def matching(a, core, size):
    available = set(core)
    edges = []
    for u,v in combinations(sorted(core),2):
        if u in available and v in available and v in a[u]:
            edges.append([u,v])
            available.remove(u)
            available.remove(v)
    need(len(edges) >= size, 'matching too short')
    return edges[:size]

def clauses(obj):
    """Physical clauses for the NEW global cover only; not Ramsey consequences."""
    a = validate(obj)
    size = {11:4,7:2}.get(len(obj['core']))
    need(size is not None and len(obj['blocks']) in (8,9) and obj['n']==43, 'global clause scope')
    m = matching(a,obj['core'],size)
    variables = {p:k+1 for k,p in enumerate(combinations(range(43),2))}
    answer = []
    for b in obj['blocks'][:obj['r']]:
        for e,f in combinations(m,2):
            for s in combinations(b,2):
                t = [v for v in b if v not in s]
                answer.append([-variables[tuple(sorted((x,y)))] for part,edge in ((s,e),(t,f)) for x in part for y in edge])
    return answer

def step(obj):
    a = validate(obj)
    size = {11:4,7:2,4:2}.get(len(obj['core']))
    need(size is not None, 'supported core order')
    m = matching(a,obj['core'],size)
    witness = None
    for i,b in enumerate(obj['blocks'][:obj['r']]):
        for e,f in combinations(m,2):
            for s in combinations(b,2):
                t = [v for v in b if v not in s]
                if all(y in a[x] for part,edge in ((s,e),(t,f)) for x in part for y in edge):
                    witness = (i,list(s)+e,t+f,e+f)
                    break
            if witness is not None:
                break
        if witness is not None:
            break
    if witness is None:
        return {'status':'NO_SELECTED_AUGMENTATION_NO_RAMSEY_VERDICT'}
    i, first, second, consumed = witness
    r = obj['r']
    red = [b[:] for j,b in enumerate(obj['blocks'][:r]) if j != i]+[first,second]
    blue = [b[:] for b in obj['blocks'][r:]]
    core = [v for v in obj['core'] if v not in consumed]
    # Keep physical labels in the witness, then give one explicit full permutation.
    physical_blocks = red+blue
    permutation = sum(physical_blocks, [])+core
    n = len(a)
    word = sum((permutation[j] in a[permutation[i]]) << k for k,(i,j) in enumerate(combinations(range(n),2)))
    new = {'n':n, 'red_hex':format(word, f'0{(n*(n-1)//2+3)//4}x'),
           'blocks':[list(range(4*j,4*j+4)) for j in range(len(physical_blocks))],
           'r':r+1, 'core':list(range(4*len(physical_blocks),n))}
    validate(new)
    binding = hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'status':'PACKING_TRANSPORT_NEEDS_CATALOG_AND_ROOT_ORDER', 'source_sha256':binding,
            'replaced_block':i, 'new_blocks_old_labels':[first,second],
            'new_to_old':permutation, 'output':new}

if __name__ == '__main__':
    obj = json.load(open(sys.argv[1], encoding='utf-8'))
    answer = {'clauses':clauses(obj), 'scope':'NEW_GLOBAL_COVER_ONLY_NOT_A_RAMSEY_IMPLICATE'} if '--clauses' in sys.argv[2:] else step(obj)
    print(json.dumps(answer, indent=2, sort_keys=True))
