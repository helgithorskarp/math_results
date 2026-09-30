"""Complete contact-triangulated polygon covers and exact reflected coordinates."""
from collections import Counter
from polynomial import T,ONE,need,bernstein
from rational import Rat
from functools import lru_cache
from itertools import combinations


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
def catalog(n):
    need(n in (5,6,7,8),'patch size')
    all_edges,diagonals,subsets=cover(n)
    eligible={e for e in all_edges if max(Counter(i for pair in e for i in pair).values())<=5}
    reps={}
    for e in sorted(eligible,key=lambda e:mask(e,n)):
        key=min(mask(image(e,p),n) for p in dihedral(n))
        reps.setdefault(key,e)
    models=[];covered=set()
    for ai,(key,e) in enumerate(sorted(reps.items())):
        orbit={image(e,p) for p in dihedral(n)}
        need(not covered&orbit and orbit<=eligible,'dihedral cover')
        covered|=orbit
        a=coords(e,n);nb=neighbors(e,n)
        pairs=[(i,j) for i,j in combinations(range(n),2)
               if not nb[i]&nb[j] and max(len(nb[i]),len(nb[j]))<=4]
        models.append({'n':n,'type':ai,'edges':e,'a':a,'pairs':pairs})
    need(covered==eligible,'degree-compatible orbit coverage')
    for e in all_edges:unfolding(e,n)
    counts={'n':n,'triangulations':len(all_edges),'degree_compatible':len(eligible),
            'dihedral_models':len(models),'diagonals':diagonals,'diagonal_subsets':subsets,
            'eligible_empty_common_pairs':sum(len(m['pairs']) for m in models)}
    return models,counts


@lru_cache(None)
def models():
    result=[];counts=[]
    for n in (5,6,7,8):
        mm,cc=catalog(n);result.extend(mm);counts.append(cc)
    need([c['triangulations'] for c in counts]==[5,14,42,132],'Catalan counts')
    need([c['degree_compatible'] for c in counts]==[5,14,35,84],'degree counts')
    need([c['dihedral_models'] for c in counts]==[1,3,3,8],'orbit counts')
    need([c['eligible_empty_common_pairs'] for c in counts]==[0,1,6,32],'pair counts')
    return result,counts
