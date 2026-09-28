"""Independent semantic clause and small-model audit for both 537 encodings."""
import argparse
from collections import Counter
from itertools import product
from pathlib import Path
N=537;K=6

def x(v,c):return 6*v-6+c
def u(v,c):return 3222+5*v-5+c

def audit(path,mode):
    assert mode in ('plain','rgs')
    V=3222 if mode=='plain' else 5907
    C=441145 if mode=='plain' else 451879
    actual=Counter()
    with Path(path).open() as f:
        assert f.readline().split()==['p','cnf',str(V),str(C)]
        for line in f:
            lits=list(map(int,line.split()));assert lits[-1]==0
            row=tuple(sorted(lits[:-1]))
            assert row and all(1<=abs(t)<=V for t in row)
            actual[row]+=1
    assert sum(actual.values())==C
    assert all(n==1 for n in actual.values())
    expect=Counter()
    def add(row):expect[tuple(sorted(row))]+=1
    if mode=='plain':add([x(1,1)])
    for v in range(N,0,-1):
        add([x(v,c) for c in range(K,0,-1)])
        for d in range(K,0,-1):
            for c in range(1,d):add([-x(v,d),-x(v,c)])
    triples=doubling=0
    for a in range(1,N+1):
        for b in range(a,N-a+1):
            z=a+b;triples+=1;doubling+=(a==b)
            for c in range(K,0,-1):
                add([-x(v,c) for v in {a,b,z}])
    if mode=='rgs':
        for c in range(K-1,0,-1):
            for v in range(N,0,-1):
                add([-x(v,c),u(v,c)])
                if v==1:add([-u(v,c),x(v,c)])
                else:
                    add([-u(v-1,c),u(v,c)])
                    add([-u(v,c),u(v-1,c),x(v,c)])
        for c in range(K,1,-1):
            for v in range(N,0,-1):
                add([-x(v,c)] if v==1 else [-x(v,c),u(v-1,c-1)])
    assert triples==72092 and doubling==268
    assert actual==expect,(sum((expect-actual).values()),sum((actual-expect).values()))
    print('PASS mode',mode,'exact_clauses',C,'triples',triples,
          'doubling',doubling,'vars',V,flush=True)

def small():
    n=4;k=3;tested=accepted=0
    for word in product(range(1,k+1),repeat=n):
        first={}
        for i,c in enumerate(word):first.setdefault(c,i)
        canonical=all(first.get(c-1,n)<first[c] for c in range(2,k+1) if c in first)
        canonical=canonical and set(word)==set(range(1,max(word)+1))
        for bits in product((False,True),repeat=n*(k-1)):
            tested+=1
            def u0(v,c):return False if v==0 else bits[(v-1)*(k-1)+(c-1)]
            exact=all(u0(v,c)==(c in word[:v]) for v in range(1,n+1) for c in range(1,k))
            rgs=all(c==1 or u0(v-1,c-1) for v,c in enumerate(word,1))
            model=exact and rgs
            if model:accepted+=1
            assert not model or canonical
            if canonical and exact:assert model
    print('PASS small_words',k**n,'assignments',tested,'accepted',accepted,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('cnf',type=Path)
    p.add_argument('--mode',choices=('plain','rgs'),default='rgs')
    a=p.parse_args();audit(a.cnf,a.mode)
    if a.mode=='rgs':small()
