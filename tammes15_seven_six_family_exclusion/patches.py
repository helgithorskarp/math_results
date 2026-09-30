"""Complete 7/6 marked-patch cover and exact reflected coordinates."""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from polynomial import T,ONE,need,bernstein
from rational import Rat

t,one,zero=Rat(T),Rat(ONE),Rat()
H=[[one if i==j else t for j in range(3)] for i in range(3)]
REF=2*t/(one+t)

def dot(x,y):
    return sum((x[i]*H[i][j]*y[j] for i in range(3) for j in range(3)),zero)

def sign_open(x):
    def sign(p):
        b=bernstein(p)
        return 1 if b and all(v>=0 for v in b) and any(v>0 for v in b) else -1 if b and all(v<=0 for v in b) and any(v<0 for v in b) else 0
    return sign(x.n)*sign(x.d)

@lru_cache(None)
def triangulations(polygon):
    if len(polygon)<3:return (frozenset(),)
    return tuple(left|right|{tuple(sorted((polygon[0],polygon[k],polygon[-1])))}
                 for k in range(1,len(polygon)-1)
                 for left in triangulations(polygon[:k+1])
                 for right in triangulations(polygon[k:]))

def edges_of(triangles):
    return frozenset(e for triangle in triangles for e in combinations(triangle,2))

def dihedral(n):
    return [tuple((s+e*i)%n for i in range(n)) for s in range(n) for e in (-1,1)]


def image(edges,p):
    return frozenset(tuple(sorted((p[i],p[j]))) for i,j in edges)


def mask(edges,n):
    return sum(1<<k for k,e in enumerate(combinations(range(n),2)) if e in edges)


def cover(n):
    boundary=frozenset((i,i+1) for i in range(n-1))|{(0,n-1)}
    diagonals=tuple(e for e in combinations(range(n),2) if e not in boundary)
    def crossing(e,f):
        return len(set(e+f))==4 and ((e[0]<f[0]<e[1])!=(e[0]<f[1]<e[1]))
    independent={boundary|frozenset(chosen) for chosen in combinations(diagonals,n-3)
                 if not any(crossing(e,f) for e,f in combinations(chosen,2))}
    catalan={edges_of(tris) for tris in triangulations(tuple(range(n)))}
    need(catalan==independent,'independent noncrossing cover')
    return catalan,len(diagonals),len(tuple(combinations(diagonals,n-3)))


def unfolding(edges,n):
    remaining=set(edges);active=set(range(n));removed=[]
    while len(active)>3:
        neighbors={i:{j for j in active if tuple(sorted((i,j))) in remaining} for i in active}
        ears=sorted(i for i in active if len(neighbors[i])==2)
        need(ears,'no ear')
        new=ears[0];i,j=sorted(neighbors[new]);old=(neighbors[i]&neighbors[j])-{new}
        need((i,j) in remaining and len(old)==1,'old ear triangle')
        removed.append((new,i,j,next(iter(old))))
        active.remove(new);remaining={e for e in remaining if new not in e}
    anchors=tuple(sorted(active));steps=tuple(reversed(removed))
    need(remaining==set(combinations(anchors,2)),'anchor triangle')
    rebuilt=set(remaining);vertices=set(anchors)
    for new,i,j,old in steps:
        need(new not in vertices and {i,j,old}<=vertices,'reflection order')
        need(set(combinations(sorted((i,j,old)),2))<=rebuilt,'reflection triangle')
        rebuilt.update((tuple(sorted((new,i))),tuple(sorted((new,j)))))
        vertices.add(new)
    need(rebuilt==set(edges),'unfolding reconstruct')
    return anchors,steps


def coords(edges,n):
    anchors,steps=unfolding(edges,n)
    a={v:[one if j==k else zero for j in range(3)] for k,v in enumerate(anchors)}
    for new,i,j,old in steps:
        a[new]=[REF*(x+y)-z for x,y,z in zip(a[i],a[j],a[old])]
    need(all(dot(x,x)==one for x in a.values()),'norm identities')
    need(all(dot(a[i],a[j])==t for i,j in edges),'contact identities')
    return a


def neighbors(edges,n):
    return {i:{j for e in edges if i in e for j in e if j!=i} for i in range(n)}


@lru_cache(None)
def catalog():
    aset,adiags,asubsets=cover(7);bset,bdiags,bsubsets=cover(6)
    need(len(aset)==42 and len(bset)==14,'Catalan counts')
    aset_ok={e for e in aset if max(Counter(i for edge in e for i in edge).values())<=5}
    areps={}
    for edges in sorted(aset_ok,key=lambda e:mask(e,7)):
        key=min(mask(image(edges,p),7) for p in dihedral(7))
        areps.setdefault(key,edges)
    marked={}
    all_marked=set()
    for edges in sorted(bset,key=lambda e:mask(e,6)):
        nb=neighbors(edges,6);ears=[i for i in range(6) if len(nb[i])==2]
        for pair in combinations(ears,2):
            orbit={(image(edges,p),tuple(sorted(p[i] for i in pair))) for p in dihedral(6)}
            key=min((mask(e,6),q) for e,q in orbit)
            marked.setdefault(key,(edges,pair))
            all_marked.add((edges,pair))
    covered=set()
    bmodels=[]
    for key,(edges,pair) in sorted(marked.items()):
        orbit={(image(edges,p),tuple(sorted(p[i] for i in pair))) for p in dihedral(6)}
        need(not covered&orbit,'marked orbit overlap');covered|=orbit
        swap=any(image(edges,p)==edges and tuple(p[i] for i in pair)==pair[::-1] for p in dihedral(6))
        b=coords(edges,6);kappa=dot(b[pair[0]],b[pair[1]])
        bmodels.append({'key':key,'edges':edges,'ears':pair,'swap':swap,'b':b,'kappa':kappa})
    need(covered==all_marked,'marked B cover')
    covered=set();amodels=[]
    for key,edges in sorted(areps.items()):
        orbit={image(edges,p) for p in dihedral(7)}
        need(not covered&orbit,'A orbit overlap');covered|=orbit
        nb=neighbors(edges,7)
        candidates=[(i,j,next(iter(nb[i]&nb[j]))) for i,j in combinations(range(7),2)
                    if len(nb[i]&nb[j])==1]
        pairs=[]
        for p,q in combinations(candidates,2):
            extra=Counter(p[:2]+q[:2])
            if all(len(nb[i])+extra[i]<=5 for i in range(7)):pairs.append((p,q))
        a=coords(edges,7)
        forced={}
        for i,j,old in candidates:
            w=dot(a[i],a[j]);v=[2*t/(one+w)*(x+y)-z for x,y,z in zip(a[i],a[j],a[old])]
            need(dot(v,v)==one and dot(v,a[i])==t and dot(v,a[j])==t,'forced ear')
            forced[(i,j,old)]=v
        amodels.append({'key':key,'edges':edges,'candidates':candidates,'pairs':pairs,'a':a,'forced':forced})
    need(covered==aset_ok,'A cover')
    for e in aset|bset:unfolding(e,7 if e in aset else 6)
    need(len(aset_ok)==35 and len(amodels)==3 and len(all_marked)==18 and len(bmodels)==3,'degree/marked orbit counts')
    need(all(b['swap'] for b in bmodels),'marked-ear swapping automorphism')
    return amodels,bmodels,{'A_triangulations':len(aset),'A_degree_compatible':len(aset_ok),
           'A_dihedrals':len(amodels),'A_diagonals':adiags,'A_subsets':asubsets,
           'B_triangulations':len(bset),'B_marked_pairs':len(all_marked),'B_marked_dihedrals':len(bmodels),
           'B_diagonals':bdiags,'B_subsets':bsubsets}


@lru_cache(None)
def models():
    aa,bb,counts=catalog();result=[]
    for ai,a in enumerate(aa):
        for bi,b in enumerate(bb):
            kappa=b['kappa']
            need(sign_open(one-kappa)==sign_open(one+kappa)==1,'B ear rank')
            cases=[]
            for ci,(p,q) in enumerate(a['pairs']):
                choices=[(p,q)] if b['swap'] else [(p,q),(q,p)]
                for orientation,(p,q) in enumerate(choices):
                    for pair in (p,q):
                        i,j,_=pair
                        need(sign_open(one+dot(a['a'][i],a['a'][j]))==1,'A forced-ear denominator')
                    u,v=a['forced'][p],a['forced'][q]
                    residual=dot(u,v)-kappa
                    edges=set(a['edges'])|{(i+7,j+7) for i,j in b['edges']}
                    for new,triple in zip(b['ears'],(p,q)):
                        edges.update((i,new+7) for i in triple[:2])
                    need(len(edges)==24,'edge count')
                    cases.append({'index':ci,'order':orientation,'p':p,'q':q,'u':u,'v':v,'residual':residual,'edges':edges})
            result.append({'ai':ai,'bi':bi,'A':a,'B':b,'cases':cases})
    need(sum(len(m['cases']) for m in result)==336,'gluing cover count')
    return result
