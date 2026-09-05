"""Independent row reconstruction by expanding the 43 named vertices.

Every linear-form coefficient is recovered from literal unordered vertex
pairs. Same-cell-pair coefficients must be uniform before aggregation.
"""
from itertools import combinations,product
from functools import lru_cache


def require(ok,detail):
    if not ok:raise ValueError(detail)


@lru_cache(None)
def ramsey(a,b):
    if min(a,b)==1:return 1
    left,right=ramsey(a-1,b),ramsey(a,b-1)
    return left+right-int(left%2==right%2==0)


def vectors(mask):
    """Independent coordinates: two singletons and the triple cell."""
    edges=list(combinations(range(3),2))
    E=[{j for j in range(3) if i!=j and mask>>edges.index(tuple(sorted((i,j))))&1}
       for i in range(3)]
    if min(map(len,E))<1:return set()
    demand=[20-len(s) for s in E];answer=set()
    roots=[]
    for a in range(8):
        A={i for i in range(3) if a>>i&1}
        for b in range(8):
            B={i for i in range(3) if b>>i&1}
            if A&B or not A|B:continue
            if any(j not in E[i] for i,j in combinations(A,2)):continue
            if any(j in E[i] for i,j in combinations(B,2)):continue
            F={i for i in range(3) if i not in A|B and A<=E[i] and not B&E[i]}
            roots.append((a,b,ramsey(5-len(A),5-len(B))-1-len(F)))
    for t in range(21):
        total_singles=80-sum(demand)+t
        for s0 in range(41):
            for s1 in range(41):
                s2=total_singles-s0-s1
                if not 0<=s2<=40:continue
                r=[d-s-t for d,s in zip(demand,(s0,s1,s2))]
                nums=[r[0]+r[1]-r[2],r[0]+r[2]-r[1],r[1]+r[2]-r[0]]
                if any(v<0 or v%2 for v in nums):continue
                y=(0,s0,s1,nums[0]//2,s2,nums[1]//2,nums[2]//2,t)
                if any(sum(y[x] for x in range(8) if x&a==a and not x&b)>cap for a,b,cap in roots):continue
                require(sum(y)==40 and all(sum(y[x] for x in range(8) if x>>i&1)==demand[i]
                                           for i in range(3)),'independent margins')
                answer.add(y)
    return answer


def system(mask,y,stage):
    core_pairs=list(combinations(range(3),2))
    E=[{j for j in range(3) if i!=j and mask>>core_pairs.index(tuple(sorted((i,j))))&1}
       for i in range(3)]
    labels=[None]*3+[x for x in range(1,8) for _ in range(y[x])]
    require(len(labels)==43,'literal vertex count')
    cells=sorted(set(labels[3:]))
    pairs=[(a,b) for i,a in enumerate(cells) for b in cells[i:] if a!=b or y[a]>=2]
    index={pair:i for i,pair in enumerate(pairs)}
    cell_vertices={x:{i for i in range(3,43) if labels[i]==x} for x in cells}
    entries=[];boxes=[0]*len(pairs)
    for a,b in combinations(range(43),2):
        if a>=3:
            k=index[tuple(sorted((labels[a],labels[b])))];boxes[k]+=1
            entries.append((a,b,k,None))
        else:
            color=(b in E[a]) if b<3 else bool(labels[b]>>a&1)
            entries.append((a,b,None,color))
    def form(left,right=None):
        coefficients=[None]*len(pairs);constant=0;possible=0
        for a,b,k,color in entries:
            weight=(int(a in left and b in left) if right is None
                    else int(a in left and b in right)+int(b in left and a in right))
            possible+=weight
            if k is None:constant+=weight*color
            elif coefficients[k] is None:coefficients[k]=weight
            else:require(coefficients[k]==weight,'nonuniform aggregate edge coefficient')
        require(all(v is not None for v in coefficients),'nonempty variable boxes')
        return coefficients,constant,possible
    bound={}
    def add(row,lo,hi):
        for a,b in ((tuple(row),hi),(tuple(-v for v in row),-lo)):
            bound[a]=min(b,bound.get(a,b))
    for x,T in cell_vertices.items():
        row,fixed,total=form(T,set(range(43)))
        add(row,21*len(T)-fixed,21*len(T)-fixed)
    for i in range(3):
        neighborhood=E[i]|{v for v in range(3,43) if labels[v]>>i&1}
        row,fixed,total=form(neighborhood)
        add(row,201-len(E[i])-107-fixed,93-fixed)
    for word in product(range(3),repeat=3):
        A={i for i in range(3) if word[i]==1};B={i for i in range(3) if word[i]==2}
        if not A|B:continue
        if any(j not in E[i] for i,j in combinations(A,2)):continue
        if any(j in E[i] for i,j in combinations(B,2)):continue
        F={i for i in range(3) if i not in A|B and A<=E[i] and not B&E[i]}
        S=F|{v for v in range(3,43) if all(labels[v]>>i&1 for i in A)
             and all(not(labels[v]>>i&1) for i in B)}
        if not S-set(range(3)):continue
        p,q=5-len(A),5-len(B)
        for x,T in cell_vertices.items():
            if stage<2 and not T<=S:continue
            row,fixed,total=form(T,S);capacity=sum(a*b for a,b in zip(row,boxes))
            if all(x>>i&1 for i in A):
                add(row,0,(ramsey(p-1,q)-1)*len(T)-fixed)
            if all(not(x>>i&1) for i in B):
                add(row,total-fixed-(ramsey(p,q-1)-1)*len(T),capacity)
        for i in F:
            neighbors=E[i]|{v for v in range(3,43) if labels[v]>>i&1}
            degree=len(neighbors&S)
            add([0]*len(pairs),max(0,len(S)-ramsey(p,q-1))-degree,ramsey(p-1,q)-1-degree)
        if stage>=1 and p==q==4 and len(S) in (15,16):
            low,high=(50,55) if len(S)==15 else (58,62)
            row,fixed,total=form(S);add(row,low-fixed,high-fixed)
    for i,cap in enumerate(boxes):
        row=[int(i==j) for j in range(len(pairs))];add(row,0,cap)
    return pairs,sorted(bound.items())
