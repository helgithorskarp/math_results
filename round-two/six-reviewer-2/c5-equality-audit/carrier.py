"""Independent integer-mask carrier for LEMMA9351; no author imports."""
from itertools import permutations, product
from collections import Counter
import hashlib, json

CYCLES=((1,8,12,10,15),(2,3,11,7,13),(4,6,5,14,9))
FIXED=(0,16,17)
G=list(range(18))
for cyc in CYCLES:
    for i,p in enumerate(cyc): G[p]=cyc[(i+1)%5]
G=tuple(G)

def require(ok, message):
    if not ok: raise ValueError(message)

def masks(n,k):
    """Gosper's integer successor exhausts every k-bit mask below 2**n."""
    x=(1<<k)-1
    while x<1<<n:
        yield x
        a=x&-x; b=x+a
        x=b|(((b^x)>>2)//a)

def bits(x):
    while x:
        b=x&-x; yield b.bit_length()-1; x-=b

def image(x,p):
    return sum(1<<p[i] for i in bits(x))

def transformer(p):
    table=[]
    for block in range(3):
        row=[0]*64
        for x in range(1,64):
            b=x&-x
            row[x]=row[x-b]|(1<<p[6*block+b.bit_length()-1])
        table.append(row)
    return lambda x:table[0][x&63]|table[1][(x>>6)&63]|table[2][x>>12]

def code_image(code,p):
    f=transformer(p)
    return tuple(sorted(f(x) for x in code))

def orbit(x):
    out=[]
    while x not in out:
        out.append(x);x=image(x,G)
    require(len(out) in (1,5),'order-five carrier')
    return tuple(sorted(out))

def universe():
    seen=set();out=[]
    for x in masks(18,5):
        if x in seen:continue
        o=orbit(x);seen.update(o);out.append(o)
    require(len(seen)==8568,'complete weight-five carrier')
    return tuple(out)

def admissible(words,bound=2):
    return all((a&b).bit_count()<=bound for i,a in enumerate(words) for b in words[:i])

def packing(code,size=68):
    require(len(code)==size and len(set(code))==size,'word count/distinctness')
    require(all(isinstance(x,int) and 0<=x<1<<18 and x.bit_count()==5 for x in code),'word domain')
    require(admissible(code),'intersection packing')
    require(set(image(x,G) for x in code)==set(code),'g invariance')
    return tuple(sum((x>>p)&1 for x in code)for p in range(18))

def group_maps(multiplier=1,root=False):
    fixed_images=(FIXED,(0,17,16)) if root else permutations(FIXED)
    fixed_images=tuple(fixed_images)
    for sig in permutations(range(3)):
        for shifts in product(range(5),repeat=3):
            for fixed in fixed_images:
                p=list(range(18))
                for j,cyc in enumerate(CYCLES):
                    for i,x in enumerate(cyc):p[x]=CYCLES[sig[j]][(multiplier*i+shifts[j])%5]
                for x,y in zip(FIXED,fixed):p[x]=y
                p=tuple(p)
                require(sorted(p)==list(range(18)),'group bijection')
                gpow=G
                for _ in range(multiplier-1):gpow=tuple(G[x]for x in gpow)
                require(all(p[G[x]]==gpow[p[x]]for x in range(18)),'normalizer conjugacy')
                yield p

def digest(obj):
    return hashlib.sha256(json.dumps(obj,separators=(',',':'),sort_keys=True).encode()).hexdigest()

def graph(orbits):
    """Cross compatibility uses five relative rotations; simultaneous g is an isometry."""
    adj=[0]*len(orbits)
    for i,a in enumerate(orbits):
        for j in range(i):
            if all((a[0]&x).bit_count()<=2 for x in orbits[j]):
                adj[i]|=1<<j;adj[j]|=1<<i
    return adj

def exact_cliques(adj,target):
    """Direct complete search, independent of the author's counting DAG.

    A greedy proper coloring orders vertices by color. At each recursive
    state, deletion/inclusion uses the last vertex; the remaining prefix
    has its recorded proper coloring. Once colors<need no clique is lost.
    """
    out=[];stats=Counter()
    def visit(P,need,chosen):
        stats['nodes']+=1
        if need==0:
            out.append(tuple(sorted(chosen)));stats['positive']+=1;return
        if P.bit_count()<need:stats['cardinality_prunes']+=1;return
        left=P;ordered=[];colors=[];c=0
        while left:
            c+=1;independent=left
            while independent:
                b=independent&-independent;v=b.bit_length()-1
                ordered.append(v);colors.append(c)
                left-=b;independent-=b;independent&=~adj[v]
        for v,color in reversed(list(zip(ordered,colors))):
            if color<need:stats['color_prunes']+=1;return
            b=1<<v
            require(P&b,'search deletion domain')
            P-=b
            visit(P&adj[v],need-1,chosen+(v,))
    visit((1<<len(adj))-1,target,())
    require(len(out)==len(set(out)),'duplicate clique')
    return tuple(sorted(out)),dict(sorted(stats.items()))
