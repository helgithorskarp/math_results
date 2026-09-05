"""Exact aggregate edge-count relaxation for the degree-20 triple profile."""
from itertools import combinations,combinations_with_replacement,product,permutations
from functools import lru_cache

@lru_cache(None)
def upper(a,b):
    if min(a,b)==1:return 1
    x,y=upper(a-1,b),upper(a,b-1)
    return x+y-int(x%2==y%2==0)

def graph(mask):
    E=[set() for _ in range(3)]
    for j,(a,b) in enumerate(combinations(range(3),2)):
        if mask>>j&1:E[a].add(b);E[b].add(a)
    return E

def roots(E):
    for w in product(range(3),repeat=3):
        A={i for i in range(3) if w[i]==1};B={i for i in range(3) if w[i]==2}
        if not A|B:continue
        if any(j not in E[i] for i,j in combinations(A,2)):continue
        if any(j in E[i] for i,j in combinations(B,2)):continue
        F={i for i in range(3) if i not in A|B and A<=E[i] and not B&E[i]}
        yield sum(1<<i for i in A),sum(1<<i for i in B),F,5-len(A),5-len(B)

def vectors(mask):
    E=graph(mask);rr=list(roots(E));dem=[20-len(s) for s in E]
    ans=[]
    for a,b,c,t in product(range(17),range(17),range(17),range(9)):
        if a+b+c+2*t!=sum(dem)-40:continue
        y=[0,dem[0]-a-b-t,dem[1]-a-c-t,a,dem[2]-b-c-t,b,c,t]
        if min(y)<0:continue
        if any(len(F)+sum(y[x] for x in range(8) if x&A==A and not x&B)>upper(p,q)-1
               for A,B,F,p,q in rr):continue
        ans.append(tuple(y))
    return ans

def model(mask,y,density=True,lifted=True):
    E=graph(mask);cells=[x for x in range(8) if y[x]]
    pairs=[(a,b) for a,b in combinations_with_replacement(cells,2) if a!=b or y[a]>=2]
    boxes=[y[a]*y[b] if a!=b else y[a]*(y[a]-1)//2 for a,b in pairs]
    rows=[]
    def add(name,row,lo,hi):rows.append((name,row,lo,hi))
    for x in cells:
        row=[int(a==x)+int(b==x) for a,b in pairs];target=(21-x.bit_count())*y[x]
        add(('degree',x),row,target,target)
    for i in range(3):
        fixed=sum(b in E[a] for a,b in combinations(E[i],2))
        fixed+=sum(y[x]*sum(x>>j&1 for j in E[i]) for x in cells if x>>i&1)
        local=201-len(E[i]);row=[int(bool(a&b&(1<<i))) for a,b in pairs]
        add(('local',i),row,local-107-fixed,93-fixed)
    for A,B,F,p,q in roots(E):
        selected={x for x in cells if x&A==A and not x&B}
        size=len(F)+sum(y[x] for x in selected)
        if not selected:continue
        for x in cells:
            if not lifted and x not in selected:continue
            row=[int(a==x and b in selected)+int(b==x and a in selected) for a,b in pairs]
            fixedR=y[x]*sum(x>>i&1 for i in F)
            capacity=sum(c*z for c,z in zip(row,boxes))
            if x&A==A:
                add(('root-red',A,B,x),row,0,(upper(p-1,q)-1)*y[x]-fixedR)
            if not x&B:
                fixedB=y[x]*sum(not(x>>i&1) for i in F)
                add(('root-blue',A,B,x),row,capacity-(upper(p,q-1)-1)*y[x]+fixedB,capacity)
        # Constant rows at exceptional members of the root set's fixed part.
        for i in F:
            degree=sum(j in E[i] for j in F)+sum(y[x] for x in selected if x>>i&1)
            add(('fixed-root',A,B,i),[0]*len(pairs),max(0,size-upper(p,q-1))-degree,
                upper(p-1,q)-1-degree)
        if density and p==q==4 and size in (15,16):
            lo,hi=(50,55) if size==15 else (58,62)
            fixed=sum(b in E[a] for a,b in combinations(F,2))
            fixed+=sum(y[x]*sum(x>>i&1 for i in F) for x in selected)
            add(('density',A,B,size),[int(a in selected and b in selected) for a,b in pairs],lo-fixed,hi-fixed)
    return pairs,boxes,rows


def move(y,perm):
    result=[0]*8
    for x,v in enumerate(y):
        result[sum(1<<perm[i] for i in range(3) if x>>i&1)]=v
    return tuple(result)

def core_image(mask,perm):
    E=graph(mask);pairs=list(combinations(range(3),2))
    return sum(1<<pairs.index(tuple(sorted((perm[a],perm[b]))))
               for a,b in pairs if b in E[a])

def orbit(mask,y):
    return {(core_image(mask,p),move(y,p)) for p in permutations(range(3))}

def canonical_rows(pairs,boxes,rows):
    bound={}
    for name,row,lo,hi in rows:
        for a,b in ((tuple(row),hi),(tuple(-v for v in row),-lo)):
            bound[a]=min(b,bound.get(a,b))
    for i,box in enumerate(boxes):
        row=tuple(int(j==i) for j in range(len(pairs)))
        bound[row]=min(box,bound.get(row,box))
        row=tuple(-v for v in row);bound[row]=min(0,bound.get(row,0))
    return sorted(bound.items())

def system(mask,y,stage):
    return canonical_rows(*model(mask,y,stage>=1,stage>=2))
