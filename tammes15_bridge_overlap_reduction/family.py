"""Finite graph cover and exact reflected-coordinate constructions."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from polynomial import T,ONE,need,bernstein
from rational import Rat

PAIRS=tuple(combinations(range(8),2))
BOUNDARY=frozenset((i,i+1) for i in range(7))|{(0,7)}
t,one,zero=Rat(T),Rat(ONE),Rat()
H=[[one if i==j else t for j in range(3)] for i in range(3)]
HI=[[(one/(one-t) if i==j else zero)-t/((one-t)*(one+2*t)) for j in range(3)] for i in range(3)]
DH=(one-t)**2*(one+2*t)
REF=2*t/(one+t)
KAPPA=t*(9*t*t-2*t-3)/(one+t)**2
B={8:[one,zero,zero],9:[zero,one,zero],10:[zero,zero,one],
   11:[-one,REF,REF],12:[REF,REF,-one]}
B_EDGES=frozenset(((8,9),(8,10),(9,10),(9,11),(10,11),(8,12),(9,12)))


def dot(x,y):
    return sum((x[i]*H[i][j]*y[j] for i in range(3) for j in range(3)),zero)


def cross(x,y):
    return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]


def matvec(m,x):
    return [sum((a*b for a,b in zip(row,x)),zero) for row in m]


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


def mask(edges):
    return sum(1<<k for k,e in enumerate(PAIRS) if e in edges)


def images(edges):
    return {frozenset(tuple(sorted(((shift+sign*i)%8,(shift+sign*j)%8))) for i,j in edges)
            for shift in range(8) for sign in (-1,1)}


def independent_diagonal_cover():
    diagonals=tuple(e for e in PAIRS if e not in BOUNDARY)
    def crosses(e,f):
        return len(set(e+f))==4 and ((e[0]<f[0]<e[1])!=(e[0]<f[1]<e[1]))
    return {frozenset(BOUNDARY|set(chosen)) for chosen in combinations(diagonals,5)
            if not any(crosses(e,f) for e,f in combinations(chosen,2))}


def unfolding(edges):
    remaining=set(edges);active=set(range(8));removed=[]
    while len(active)>3:
        neighbors={i:{j for j in active if tuple(sorted((i,j))) in remaining} for i in active}
        ears=sorted(i for i in active if len(neighbors[i])==2)
        need(ears,'missing triangulation ear')
        new=ears[0];i,j=sorted(neighbors[new])
        old=(neighbors[i]&neighbors[j])-{new}
        need((i,j) in remaining and len(old)==1,'invalid ear old triangle')
        removed.append((new,i,j,next(iter(old))))
        active.remove(new);remaining={e for e in remaining if new not in e}
    anchors=tuple(sorted(active));steps=tuple(reversed(removed))
    need(remaining==set(combinations(anchors,2)),'anchor graph')
    rebuilt=set(remaining);vertices=set(anchors)
    for new,i,j,old in steps:
        need(new not in vertices and {i,j,old}<=vertices,'reflection order')
        need(set(combinations(sorted((i,j,old)),2))<=rebuilt,'reflection old triangle')
        rebuilt.update((tuple(sorted((new,i))),tuple(sorted((new,j)))))
        vertices.add(new)
    need(rebuilt==set(edges),'ear reconstruction mismatch')
    return anchors,steps


@lru_cache(None)
def catalog():
    triangles=triangulations(tuple(range(8)))
    all_edges={edges_of(x) for x in triangles}
    need(len(triangles)==len(all_edges)==132,'Catalan triangulation count')
    need(all_edges==independent_diagonal_cover(),'entry-level independent triangulation cover')
    survivors={e for e in all_edges if max(Counter(i for edge in e for i in edge).values())<=5}
    need(len(survivors)==84,'degree filter')
    orbits={}
    # Preserve deterministic first Catalan representative and then sort by its canonical mask.
    for triangle_set in triangles:
        edges=edges_of(triangle_set)
        if edges in survivors:orbits.setdefault(min(map(mask,images(edges))),edges)
    need(len(orbits)==8,'dihedral orbit count')
    covered=set();records=[]
    for key,edges in sorted(orbits.items()):
        orbit=images(edges)
        need(not covered&orbit and orbit<=survivors,'dihedral quotient')
        covered|=orbit
        neighbors={i:{j for edge in edges if i in edge for j in edge if j!=i} for i in range(8)}
        candidates=[(i,j,next(iter(neighbors[i]&neighbors[j]))) for i,j in PAIRS
                    if len(neighbors[i]&neighbors[j])==1]
        gluings=[]
        for p,q in combinations(candidates,2):
            extra=Counter(p[:2]+q[:2])
            if all(len(neighbors[i])+extra[i]<=5 for i in range(8)):gluings.append((p,q))
        anchors,steps=unfolding(edges)
        records.append({'key':key,'edges':edges,'anchors':anchors,'steps':steps,
                        'candidates':candidates,'gluings':gluings})
    need(covered==survivors and sum(len(r['gluings']) for r in records)==355,'gluing cover')
    for edges in survivors:unfolding(edges)
    return records


def coefficients(record):
    a={v:[one if j==k else zero for j in range(3)] for k,v in enumerate(record['anchors'])}
    for new,i,j,old in record['steps']:
        a[new]=[REF*(x+y)-z for x,y,z in zip(a[i],a[j],a[old])]
    need(all(dot(x,x)==one for x in a.values()),'A norms')
    need(all(dot(a[i],a[j])==t for i,j in record['edges']),'A contacts')
    forced={}
    for i,j,old in record['candidates']:
        need(dot(a[i],a[old])==t and dot(a[j],a[old])==t,'old common-neighbor contacts')
        w=dot(a[i],a[j])
        need(sign_open(one+w)==1,'common-neighbor denominator')
        v=[2*t/(one+w)*(x+y)-z for x,y,z in zip(a[i],a[j],a[old])]
        need(dot(v,v)==one and dot(v,a[i])==t and dot(v,a[j])==t,'forced ear identities')
        forced[(i,j,old)]=v
    return a,forced


@lru_cache(None)
def models():
    need(dot(B[11],B[12])==KAPPA,'B ear dot')
    need(sign_open(one-KAPPA)==sign_open(one+KAPPA)==1,'B ear independence')
    result=[]
    for record in catalog():
        a,forced=coefficients(record)
        cases=[]
        for p,q in record['gluings']:
            edges=set(record['edges'])|set(B_EDGES)
            for new,triple in zip((11,12),(p,q)):
                edges.update(tuple(sorted((new,i))) for i in triple[:2])
            need(len(edges)==24,'core edge count')
            cases.append({'gluing':(p,q),'u':forced[p],'v':forced[q],
                          'residual':dot(forced[p],forced[q])-KAPPA,'edges':edges})
        result.append({'record':record,'a':a,'cases':cases})
    return result


BCROSS=cross(B[11],B[12])
BETAS={j:(dot(x,B[11]),dot(x,B[12])) for j,x in B.items()}
LAMBDA={j:DH*sum((x*y for x,y in zip(vector,BCROSS)),zero)/(one-KAPPA*KAPPA) for j,vector in B.items()}


def branch_rat(case,orientation):
    u,v=case['u'],case['v'];normal=matvec(HI,cross(u,v))
    result={}
    for j in B:
        beta1,beta2=BETAS[j]
        c1=(beta1-KAPPA*beta2)/(one-KAPPA*KAPPA)
        c2=(beta2-KAPPA*beta1)/(one-KAPPA*KAPPA)
        result[j]=[c1*x+c2*y+orientation*LAMBDA[j]*z for x,y,z in zip(u,v,normal)]
    return result


def to_field(f,x):
    return f.div(f.element(x.n),f.element(x.d))


def branch_field(model,case,orientation,f):
    a={i:tuple(to_field(f,x) for x in v) for i,v in model['a'].items()}
    u,v=[tuple(to_field(f,x) for x in vector) for vector in (case['u'],case['v'])]
    kappa=to_field(f,KAPPA);den=f.sub(f.one,f.mul(kappa,kappa))
    raw=[f.sub(f.mul(u[1],v[2]),f.mul(u[2],v[1])),f.sub(f.mul(u[2],v[0]),f.mul(u[0],v[2])),f.sub(f.mul(u[0],v[1]),f.mul(u[1],v[0]))]
    hi=[[to_field(f,x) for x in row] for row in HI]
    normal=[sum_field(f,(f.mul(x,y) for x,y in zip(row,raw))) for row in hi]
    b={}
    for j in B:
        beta1,beta2=(to_field(f,x) for x in BETAS[j])
        c1=f.div(f.sub(beta1,f.mul(kappa,beta2)),den)
        c2=f.div(f.sub(beta2,f.mul(kappa,beta1)),den)
        magnitude=f.mul(f.number(orientation),to_field(f,LAMBDA[j]))
        b[j]=tuple(sum_field(f,(f.mul(c1,x),f.mul(c2,y),f.mul(magnitude,z))) for x,y,z in zip(u,v,normal))
    need(all(f.dot(b[i],b[j])==(f.one if i==j else f.t) for i in (8,9,10) for j in (8,9,10) if i<=j),'B anchor Gram')
    need(b[11]==u and b[12]==v,'fixed B ears')
    return {**a,**b}


def sum_field(f,terms):
    result=f.zero
    for term in terms:result=f.add(result,term)
    return result
