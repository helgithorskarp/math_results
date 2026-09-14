"""Exact producer model for the quadratic paired-circle kernel."""
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json


# K=Q(sqrt(3),i), tensor basis 1,sqrt(3),i,i*sqrt(3).
def ka(x,y): return tuple(a+b for a,b in zip(x,y))
def kn(x): return tuple(-a for a in x)
def ks(x,y): return ka(x,kn(y))
def km(x,y):
    out=[F(0)]*4
    for m,a in enumerate(x):
        for n,b in enumerate(y):
            if not a or not b: continue
            s=(m&1)+(n&1); j=((m>>1)&1)+((n>>1)&1); c=a*b
            if s>=2: c*=3; s-=2
            if j>=2: c=-c; j-=2
            out[s+2*j]+=c
    return tuple(out)
def kc(x): return (x[0],x[1],-x[2],-x[3])


K0=(F(0),)*4;K1=(F(1),F(0),F(0),F(0));K53=(F(5,3),F(0),F(0),F(0))
# L=K[t]/(t^2-(5/3)t+1), represented as a+b*t.
def add(x,y): return (ka(x[0],y[0]),ka(x[1],y[1]))
def neg(x): return (kn(x[0]),kn(x[1]))
def sub(x,y): return add(x,neg(y))
def mul(x,y):
    a,b=x;c,d=y;bd=km(b,d)
    return (ks(km(a,c),bd),ka(ka(km(a,d),km(b,c)),km(K53,bd)))
def conj(x):
    a,b=x;cb=kc(b)
    return (ka(kc(a),km(K53,cb)),kn(cb))
def norm(x): return mul(x,conj(x))


ZERO=(K0,K0);ONE=(K1,K0);T=(K0,K1)
OMEGA=((F(1,2),F(0),F(0),F(1,2)),K0)
ROOTS=[ONE]
for _ in range(5): ROOTS.append(mul(ROOTS[-1],OMEGA))
assert mul(ROOTS[-1],OMEGA)==ONE and norm(T)==ONE


def enc(x): return [[[q.numerator,q.denominator] for q in part] for part in x]
def raw(x): return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x): return hashlib.sha256(raw(x)).hexdigest()
def orbit(direction):
    candidates=[mul(direction,u) for u in ROOTS];rep=min(candidates)
    return rep,next(k for k,u in enumerate(ROOTS) if mul(rep,u)==direction)


def colour(vertices,edges,k,pins=None):
    adj=[set() for _ in vertices]
    for a,b in edges: adj[a].add(b);adj[b].add(a)
    val=[-1]*len(vertices)
    for v,c in (pins or {}).items(): val[v]=c
    if any(val[a]>=0 and val[a]==val[b] for a,b in edges): return None
    def visit(left):
        if not left:return val.copy()
        v=max(left,key=lambda x:(len({val[y] for y in adj[x] if val[y]>=0}),len(adj[x]),-x))
        forbidden={val[y] for y in adj[v] if val[y]>=0}
        for c in range(k):
            if c in forbidden:continue
            val[v]=c;answer=visit(left-{v})
            if answer is not None:return answer
        val[v]=-1;return None
    return visit({v for v in range(len(vertices)) if val[v]<0})


def base_patterns():
    out=set()
    for word in product(range(4),repeat=4):
        if word[0]==word[1] or word[2]==word[3]:continue
        rename={};canonical=[]
        for c in word:
            if c not in rename:rename[c]=len(rename)
            canonical.append(rename[c])
        out.add(tuple(canonical))
    return sorted(out)


def build():
    # In slot order 00,01,10,11: (A-variable,k,l).  The B direction
    # always belongs to the other orbit.  Here all A directions use U and
    # all B directions use tU.
    spec=((0,0,0),(0,0,1),(0,4,4),(0,4,3));cross=((0,0),(0,1),(1,0),(1,1))
    us=[ROOTS[k] for _,k,_ in spec];vs=[mul(ROOTS[l],T) for _,_,l in spec]
    ds=[sub(u,v) for u,v in zip(us,vs)]
    centres=(ZERO,sub(ds[0],ds[2]),ds[0],ds[1])
    if sub(centres[3],centres[1])!=ds[3] or norm(centres[1])!=ONE or norm(sub(centres[3],centres[2]))!=ONE:
        raise ValueError('centre geometry')
    if len(set(centres))!=4:raise ValueError('centre collision')
    intersections=[];clauses=[];reps={}
    forbidden=(ZERO,ONE,((F(3),F(0),F(0),F(0)),K0),((F(4),F(0),F(0),F(0)),K0))
    for (i,j),u,v in zip(cross,us,vs):
        if u in (v,neg(v)) or norm(sub(u,v)) in forbidden:raise ValueError('nonregular slot')
        p=add(centres[i],u);q=sub(add(centres[i],centres[2+j]),p)
        if p==q or any(norm(sub(x,centres[i]))!=ONE or norm(sub(x,centres[2+j]))!=ONE for x in (p,q)):
            raise ValueError('bad circle intersection')
        intersections.append((p,q));ru,k=orbit(u);rv,l=orbit(v);reps[ru]=None;reps[rv]=None;s=(1+i+j)&1
        clauses.append(((ru,(s+k)&1),(rv,(1+s+l)&1)))
    ordered=sorted(reps);oi={r:i for i,r in enumerate(ordered)}
    clauses=[sorted([[oi[r],v] for r,v in row]) for row in clauses]
    phase_solutions=sum(all(any(a[v]==value for v,value in row) for row in clauses)
                        for a in product(range(2),repeat=len(ordered)))
    directions=[set(),set()]
    for g in range(2):
        seeds=[sub(centres[2*g+1],centres[2*g])]
        for (i,j),row in zip(cross,intersections):
            owner=centres[i if g==0 else 2+j];seeds.extend(sub(p,owner) for p in row)
        for seed in seeds:directions[g].update(mul(seed,u) for u in ROOTS)
    points=set()
    for h,c in enumerate(centres):points.update(add(c,u) for u in directions[h//2])
    vertices=sorted(points);vi={p:i for i,p in enumerate(vertices)}
    edges=[list(e) for e in combinations(range(len(vertices)),2) if norm(sub(vertices[e[0]],vertices[e[1]]))==ONE]
    centre_indices=[vi[c] for c in centres];patterns=base_patterns();words={}
    for pattern in patterns:
        answer=colour(vertices,edges,4,dict(zip(centre_indices,pattern)))
        if answer is None:raise ValueError('missing terminal word')
        words[''.join(map(str,pattern))]=''.join(map(str,answer))
    colouring=colour(vertices,edges,4)
    if colouring is None:raise ValueError('missing four-colouring')
    moser=[25,33,38,39,40,41,44]
    return {'schema':1,'field':'Q(sqrt(3),i)[t]/(t^2-(5/3)t+1)',
            'parameter_polynomial':['1','-5/3','1'],'directions':[list(x) for x in spec],
            'centres':[enc(x) for x in centres],'centre_indices':centre_indices,
            'cross_squared_norms':[enc(norm(d)) for d in ds],
            'orbit_variables':len(ordered),'clauses':clauses,'phase_solutions':phase_solutions,
            'direction_sizes':list(map(len,directions)),'vertices':[enc(x) for x in vertices],'edges':edges,
            'patch_vertices':len(vertices),'patch_edges':len(edges),'point_sha256':digest([enc(x) for x in vertices]),
            'edge_sha256':digest(edges),'common_plane_unit_neighbour':False,
            'base_terminal_patterns':[''.join(map(str,x)) for x in patterns],
            'terminal_relation':[''.join(map(str,x)) for x in patterns],'terminal_words':words,
            'moser_spindle_indices':moser,'chromatic_number':4,'four_colouring':''.join(map(str,colouring)),
            'interface_stronger_than_base':False,'record_improved':False}
