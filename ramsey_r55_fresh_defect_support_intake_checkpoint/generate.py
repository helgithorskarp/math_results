"""One fixed fresh edge-annealing intake. No existing graph is an input."""
from itertools import combinations
from pathlib import Path
import argparse
import json
import math
import random
import time

def decode(n,word):
    a=[0]*n
    for k,(u,v) in enumerate(combinations(range(n),2)):
        if word>>k&1:a[u]|=1<<v;a[v]|=1<<u
    full=(1<<n)-1
    b=[full^(1<<u)^a[u] for u in range(n)]
    return a,b

def encode(a):
    return sum(((a[u]>>v)&1)<<k for k,(u,v) in enumerate(combinations(range(len(a)),2)))

def triangles(a,mask):
    count=0
    while mask:
        x=mask&-mask;mask-=x
        rest=mask&a[x.bit_length()-1]
        while rest:
            y=rest&-rest;rest-=y
            count+=(rest&a[y.bit_length()-1]).bit_count()
    return count

def cliques(a,k,mask=None):
    if mask is None:mask=(1<<len(a))-1
    if k==0:return 1
    if mask.bit_count()<k:return 0
    if k==1:return mask.bit_count()
    answer=0
    while mask:
        b=mask&-mask;mask-=b
        answer+=cliques(a,k-1,mask&a[b.bit_length()-1])
    return answer

def delta(a,b,u,v):
    red=triangles(a,a[u]&a[v])
    blue=triangles(b,b[u]&b[v])
    return blue-red if a[u]>>v&1 else red-blue

def flip(a,b,u,v):
    a[u]^=1<<v;a[v]^=1<<u
    b[u]^=1<<v;b[v]^=1<<u

def one(index):
    rng=random.Random(202609090000+index)
    n=43;pairs=list(combinations(range(n),2))
    a,b=decode(n,rng.getrandbits(len(pairs)))
    energy=cliques(a,5)+cliques(b,5)
    best=energy;best_a=a[:];start=time.monotonic()
    cycles=[];proposals=0
    for cycle in range(8):
        if cycle:
            a=best_a[:];b=[((1<<n)-1)^(1<<u)^a[u] for u in range(n)];energy=best
        for j in range(65536):
            temperature=1.25*(0.08**((j//1024)/63))
            u,v=pairs[rng.randrange(len(pairs))]
            d=delta(a,b,u,v)
            if d<=0 or rng.random()<math.exp(-d/temperature):
                flip(a,b,u,v);energy+=d
                if energy<best:best=energy;best_a=a[:]
            proposals+=1
            if best==0:break
        actual=cliques(a,5)+cliques(b,5)
        if actual!=energy:raise ValueError('incremental energy mismatch')
        cycles.append(best)
        if best==0:break
    # Strict descent terminates because the integer objective decreases.
    a=best_a[:];b=[((1<<n)-1)^(1<<u)^a[u] for u in range(n)]
    while best:
        changes=[(delta(a,b,u,v),u,v) for u,v in pairs]
        d,u,v=min(changes)
        if d>=0:break
        flip(a,b,u,v);best+=d
    if best!=cliques(a,5)+cliques(b,5):raise ValueError('final score mismatch')
    return {'seed_index':index,'seed':202609090000+index,'n':n,'red_hex':format(encode(a),'0226x'),
            'score':best,'proposals':proposals,'cycle_best_scores':cycles,
            'seconds':time.monotonic()-start,'energy_checks':'PASS'}

def run(path):
    p=Path(path)
    if p.exists():raise ValueError('refuse existing registry')
    with p.open('x') as f:
        for i in range(32):
            row=one(i);f.write(json.dumps(row,sort_keys=True)+'\n');f.flush()
            print(json.dumps({k:row[k] for k in ('seed_index','score','cycle_best_scores','seconds')}),flush=True)
            if row['score']==0:break

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('registry');args=parser.parse_args();run(args.registry)
