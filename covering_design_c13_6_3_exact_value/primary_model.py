"""Primary balanced roots and cached complete point-link joins."""
from collections import Counter,defaultdict
from itertools import combinations
from math import factorial
from catalogue import CAT,point_automorphisms
from row_maps import columns,key,embeddings,PAIRLIST,BITS,PAIRS,pointed_templates
P=12
CACHE={}
def prepare():
    templates=pointed_templates()
    roots=[]
    for d in CAT:
        actions=point_automorphisms(d)
        left=set(combinations(range(12),3))
        while left:
            high=min(left)
            left-={tuple(sorted(a[x] for x in high)) for a in actions}
            def score(r):
                rows=[b&~(1<<r) for b in d['blocks'] if b>>r&1]
                cell_sizes=Counter(columns(rows,[x for x in range(12) if x!=r]))
                free=1
                for n in cell_sizes.values():free*=factorial(n)
                return (len(rows),-free,-r)
            r=max((x for x in range(12) if x not in high),key=score)
            k=d['point_signatures'][r].bit_count()
            assert k in (4,5)
            roots.append(dict(id=len(roots),design=d['id'],high=high,r=r,k=k))
    assert len(roots)==12819
    return roots,templates

def uncoloured(design,r,templates):
    cachekey=(design,r)
    if cachekey in CACHE:return CACHE[cachekey]
    for k in list(CACHE):
        if k[0]!=design:del CACHE[k]
    d=CAT[design]
    fixed=tuple(b|(1<<P) for b in d['blocks'])
    shared=tuple(b&~(1<<r) for b in d['blocks'] if b>>r&1)
    vertices=tuple(x for x in range(13) if x not in (P,r))
    raw=0;seen={}
    for temp in templates[(len(shared),key(shared,vertices))]:
        for action in embeddings(temp,shared,vertices):
            raw+=1
            second=tuple((1<<r)|sum(1<<action[x] for x in range(12) if b>>x&1) for b in temp['blocks'])
            union=tuple(sorted(set(fixed+second)))
            assert len(union)==18-len(shared)
            if union in seen:
                assert seen[union][0]==temp['design']
                continue
            seen[union]=(temp['design'],action)
    records=[]
    for union,(second,action) in sorted(seen.items()):
        degrees=[0]*13;paircounts=[0]*78
        for b in union:
            for x in BITS[b]:degrees[x]+=1
            for t in PAIRS[b]:paircounts[t]+=1
        needed=20-len(union)
        if any(n>10 or n<9-needed for n in degrees):continue
        mandatory=sum(1<<x for x,n in enumerate(degrees) if n>9)
        for (a,b),n in zip(PAIRLIST,paircounts):
            if n>5:mandatory |= (1<<a)|(1<<b)
        if mandatory.bit_count()>3:continue
        forbidden=sum(1<<x for x,n in enumerate(degrees) if n<10-needed)
        records.append((union,second,mandatory,forbidden))
    result=(records,raw,len(seen))
    CACHE[cachekey]=result
    return result

def joined(root,templates,normalize=True):
    records,raw,unique=uncoloured(root['design'],root['r'],templates)
    high=sum(1<<x for x in root['high'])
    configurations=[]
    for union,second,mandatory,forbidden in records:
        if normalize and second>root['design']:continue
        if mandatory&~high or forbidden&high:continue
        configurations.append(union)
    return configurations,dict(raw=raw,unique=unique,uncoloured_compatible=len(records))
