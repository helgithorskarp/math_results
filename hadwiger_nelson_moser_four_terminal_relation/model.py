"""One fixed eleven-point support. All geometry uses exact integer arithmetic."""
from itertools import combinations
from hashlib import sha256
import json

# (a+b sqrt(33) + i(c sqrt(3)+d sqrt(11)))/12.
POINTS = (
    (0,0,0,0), (12,0,0,0), (6,0,6,0), (18,0,6,0),
    (10,0,0,2), (5,-1,5,1), (15,-1,5,3),
    (6,0,-6,0), (12,0,12,0), (20,0,0,4), (-5,-1,5,-1),
)
TERMINALS = (7,8,9,10)
FAILED_POINT = (25,-1,5,5)  # t*(2+rho), which fails to dominate vertex 4.

def need(ok, message):
    if not ok:
        raise ValueError(message)

def digest(obj):
    return sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()

def norm_difference(p,q):
    a,b,c,d = (x-y for x,y in zip(p,q))
    return a*a+33*b*b+3*c*c+11*d*d, 2*(a*b+c*d)

def graph(points=POINTS):
    need(len(points)==11 and all(len(p)==4 and all(type(x) is int for x in p)
                               for p in points), 'integer coordinate rows')
    # sqrt(33), sqrt(3)/sqrt(11) are irrational, so tuple equality is exact.
    need(len(set(points))==len(points), 'distinct physical points')
    distances=[(a,b,*norm_difference(points[a],points[b]))
               for a,b in combinations(range(len(points)),2)]
    edges=[(a,b) for a,b,n,s in distances if (n,s)==(144,0)]
    return edges,distances

def canonical(word):
    names={}
    return tuple(names.setdefault(c,len(names)) for c in word)

def patterns(n):
    def rec(word):
        if len(word)==n:
            yield tuple(word)
            return
        for c in range(min(3,max(word,default=-1)+1)+1):
            yield from rec(word+[c])
    yield from rec([])

def check_word(word, edges, removed=None):
    if isinstance(word,str):
        need(len(word)==11 and all(c in '0123' for c in word),'colour string')
        word=list(map(int,word))
    need(len(word)==11,'word length')
    need(all(type(c) is int and (c==-1 if i==removed else 0<=c<4)
             for i,c in enumerate(word)),'colour range/deleted vertex')
    need(all(word[a]!=word[b] for a,b in edges
             if a!=removed and b!=removed),'proper edge colours')
    return tuple(word[t] for t in TERMINALS)
