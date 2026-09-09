"""Exact four-row formulation; Python specification and future contact codec."""
from collections import Counter
from itertools import combinations, permutations, product
from math import factorial

def need(ok, message):
    if not ok: raise ValueError(message)

def graph(n, word):
    need(type(n) is int and 0 <= n <= 7 and type(word) is int and 0 <= word < 1 << (n*(n-1)//2), 'core word')
    a=[[0]*n for _ in range(n)]
    for k,(u,v) in enumerate(combinations(range(n),2)):a[u][v]=a[v][u]=(word>>k)&1
    need(all(len({a[u][v] for u,v in combinations(s,2)})==2 for s in combinations(range(n),4)), 'core is not Ramsey(4,4)')
    return a

def matching(a):
    used=set();answer=[]
    for u,v in combinations(range(len(a)),2):
        if a[u][v] and u not in used and v not in used:
            answer.append((u,v));used.update((u,v))
    return answer[:2]

class Domain:
    def __init__(self,n,word,augmentation=False):
        self.n=n;self.word=word;self.a=graph(n,word);self.N=1<<n
        a=self.a;N=self.N
        edges=[(1<<u)|(1<<v) for u,v in combinations(range(n),2) if a[u][v]]
        triangles=[sum(1<<u for u in s) for s in combinations(range(n),3) if all(a[u][v] for u,v in combinations(s,2))]
        self.ind=[all(s&e!=e for e in edges) for s in range(N)]
        self.tf=[all(s&t!=t for t in triangles) for s in range(N)]
        self.pair=[sum(1<<d for d in range(N) if self.tf[s&d]) for s in range(N)]
        self.triple=[sum(1<<d for d in range(N) if self.ind[s&d]) for s in range(N)]
        self.empty=[sum(1<<d for d in range(N) if not s&d) for s in range(N)]
        self.tail=[((1<<N)-1)^((1<<c)-1) for c in range(N+1)]
        self.augmentation=augmentation;self.types=[0]*N;self.pure=[0]*4
        if augmentation:
            m=matching(a);need(len(m)==2,'two matching edges')
            e,f=(sum(1<<v for v in s) for s in m)
            self.types=[int(s&e==e)+2*int(s&f==f) for s in range(N)]
            self.pure=[sum(1<<s for s in range(N) if self.types[s]==i) for i in range(4)]

    def choices(self,a,b,c,joint=True):
        ab=a&b;ac=a&c;bc=b&c;t=ab&c
        if not (self.tf[ab] and self.tf[ac] and self.tf[bc] and self.ind[t]):return 0
        d=(self.pair[a]&self.pair[b]&self.pair[c]&self.triple[ab]&self.triple[ac]&self.triple[bc]&self.empty[t]&self.tail[c])
        if joint and self.augmentation:
            types=[self.types[x] for x in (a,b,c)]
            if all(x in (1,2) for x in types):
                ones=types.count(1)
                if ones==2:d&=~self.pure[2]
                if ones==1:d&=~self.pure[1]
        return d

    @staticmethod
    def weights(a,b,c):
        denominator=1
        for v in Counter((a,b,c)).values():denominator*=factorial(v)
        high=24//denominator;tie=high//((a==c)+(b==c)+2)
        return high,tie

    def count(self):
        plain=joint=0
        for a in range(self.N):
            for b in range(a,self.N):
                for c in range(b,self.N):
                    high,tie=self.weights(a,b,c)
                    p=self.choices(a,b,c,False);d=self.choices(a,b,c,True)
                    plain+=(p>>(c+1)).bit_count()*high+((p>>c)&1)*tie
                    joint+=(d>>(c+1)).bit_count()*high+((d>>c)&1)*tie
        return plain,joint

def literal_count(n,word,augmentation=False):
    """Definition-level cube count for small controls; no row-intersection rules."""
    core=graph(n,word);m=matching(core) if augmentation else []
    need(not augmentation or len(m)==2,'matching')
    plain=joint=0
    for cross in range(1<<(4*n)):
        a=[[0]*(4+n) for _ in range(4+n)]
        for u,v in combinations(range(4),2):a[u][v]=a[v][u]=1
        for u,v in combinations(range(n),2):a[4+u][4+v]=a[4+v][4+u]=core[u][v]
        for u in range(4):
            for v in range(n):a[u][4+v]=a[4+v][u]=(cross>>(n*u+v))&1
        if any(len({a[u][v] for u,v in combinations(s,2)})==1 for s in combinations(range(4+n),5)):continue
        plain+=1
        if augmentation:
            e,f=m
            if any(all(a[u][4+v] for part,edge in ((s,e),(set(range(4))-set(s),f)) for u in part for v in edge) for s in combinations(range(4),2)):continue
        joint+=1
    return plain,joint
