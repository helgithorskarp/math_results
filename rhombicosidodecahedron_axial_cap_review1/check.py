"""six-reviewer-1: exact RID signed-hull optimizer census.

No researcher modules or candidate fixtures. Nearest-point simplex tests,
independently reconstructed proper vertex group, Q(sqrt(5)) arithmetic.
"""
from collections import Counter
from fractions import Fraction as F
from functools import total_ordering
from itertools import combinations, product
import argparse, hashlib, json, resource, sys, time
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)

@total_ordering
class Q:
    __slots__=('a','b')
    def __init__(self,a=0,b=0):self.a,self.b=F(a),F(b)
    @staticmethod
    def cast(x):return x if isinstance(x,Q) else Q(x)
    def __add__(self,x):
        x=Q.cast(x);return Q(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self):return Q(-self.a,-self.b)
    def __sub__(self,x):return self+-Q.cast(x)
    def __rsub__(self,x):return Q.cast(x)+-self
    def __mul__(self,x):
        x=Q.cast(x);return Q(self.a*x.a+5*self.b*x.b,self.a*x.b+self.b*x.a)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=Q.cast(x);n=x.a*x.a-5*x.b*x.b
        need(n!=0,'quadratic inverse zero')
        return self*Q(x.a/n,-x.b/n)
    def __rtruediv__(self,x):return Q.cast(x)/self
    def __eq__(self,x):
        try:x=Q.cast(x)
        except (TypeError,ValueError):return False
        return (self.a,self.b)==(x.a,x.b)
    def __hash__(self):return hash((self.a,self.b))
    def sign(self):
        a,b=self.a,self.b
        if not b:return (a>0)-(a<0)
        if not a:return (b>0)-(b<0)
        if a>0 and b>0:return 1
        if a<0 and b<0:return -1
        n=a*a-5*b*b
        need(n!=0,'irrational order separation')
        return ((a>0)-(a<0)) if n>0 else ((b>0)-(b<0))
    def __lt__(self,x):return (self-Q.cast(x)).sign()<0
    def __abs__(self):return self if self.sign()>=0 else -self
    def encode(self):return [str(self.a),str(self.b)]
    def __repr__(self):return '('+str(self.a)+')+('+str(self.b)+')sqrt5'

Z=Q();ONE=Q(1);PHI=Q(F(1,2),F(1,2));R2=7+8*PHI

def dot(x,y):return sum((a*b for a,b in zip(x,y)),Z)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def scale(x,c):return tuple(a*c for a in x)
def cross(x,y):return (x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0])
def det(M):return dot(M[0],cross(M[1],M[2]))
def mv(M,x):return tuple(dot(row,x) for row in M)
def encode(x):return [q.encode() for q in x]
def canonical(x):
    first=next((a.sign() for a in x if a!=Z),0)
    need(first!=0,'zero projective point')
    return x if first>0 else scale(x,-1)

def vertices():
    seeds=[(ONE,ONE,PHI*PHI*PHI),(PHI*PHI,PHI,2*PHI),(2+PHI,Z,PHI*PHI)]
    result=set()
    for seed in seeds:
        for s in range(3):
            q=seed[s:]+seed[:s]
            for signs in product([-1,1],repeat=3):result.add(tuple(x*t for x,t in zip(q,signs)))
    result=sorted(result)
    need(len(result)==60 and all(dot(x,x)==R2 for x in result),'RID vertex model/radii')
    need(all(scale(x,-1) in result for x in result),'central symmetry')
    return result

def group(V):
    need(len(V)==60 and len(set(V))==60,'complete original vertex set')
    adj={i:[j for j in range(60) if i!=j and dot(sub(V[i],V[j]),sub(V[i],V[j]))==4]
         for i in range(60)}
    need(all(len(q)==4 for q in adj.values()),'edge-two adjacency')
    triangles=[(i,j,k) for i,j,k in combinations(range(60),3) if j in adj[i] and k in adj[i] and k in adj[j]]
    need(len(triangles)==20,'equilateral face count')
    for ids in triangles:
        p,q,r=[V[i] for i in ids];n=cross(sub(q,p),sub(r,p));h=dot(n,p)
        if h<0:n=scale(n,-1);h=-h
        need(h>0 and all(dot(n,v)<=h for v in V),'triangular supporting face')
    ref=triangles[0];a,b,c=[V[i] for i in ref];d=dot(a,cross(b,c))
    need(d!=0,'anchor frame rank')
    inv=[scale(cross(b,c),1/d),scale(cross(c,a),1/d),scale(cross(a,b),1/d)]
    lookup={p:i for i,p in enumerate(V)};G={};raw=0
    for i in range(60):
        for j in adj[i]:
            for k in adj[i]:
                if k==j or k not in adj[j]:continue
                raw+=1;columns=[V[q] for q in (i,j,k)]
                M=tuple(tuple(sum((columns[l][r]*inv[l][s] for l in range(3)),Z)
                               for s in range(3)) for r in range(3))
                if det(M)!=1:continue
                need(all(dot(M[r],M[s])==(ONE if r==s else Z) for r in range(3) for s in range(3)),
                     'proper orthogonal vertex frame')
                image=[mv(M,p) for p in V]
                need(set(image)==set(V),'body symmetry point permutation')
                G[M]=tuple(lookup[p] for p in image)
    need(raw==120 and len(G)==60,'complete proper group')
    need(len({perm[0] for perm in G.values()})==60,'reference vertex transitivity')
    return G,{'order':60,'ordered_triangular_frames':raw,'triangular_faces':20,'anchor':list(ref),
              'reference_vertex_orbit':60,'vertex_degrees':dict(Counter(len(q) for q in adj.values()))}

def optimizers(V,G):
    # Every closest signed-hull point lies in an active simplex of size<=3.
    # Vertex transitivity sends one active vertex to V[0]. No direction grid.
    anchor=V[0];raw=0;valid={};kind=Counter();rejected=Counter()
    def keep(q,source):
        nonlocal raw
        raw+=1;score=dot(q,q)
        if score==Z:rejected['zero_projection']+=1;return
        products=[dot(v,q) for v in V]
        if min(map(abs,products))!=score:rejected['violates_signed_hull_support']+=1;return
        kind[len(source)]+=1;valid.setdefault(q,source)
    keep(anchor,(0,))
    for j in range(1,60):keep(scale(add(anchor,V[j]),F(1,2)),(0,j))
    for j,k in combinations(range(1,60),2):
        raw+=1;p,r=V[j],V[k];n=cross(sub(p,anchor),sub(r,anchor));nn=dot(n,n)
        need(nn>0,'three distinct equal-radius points noncollinear')
        d=dot(n,anchor)
        weights=[dot(cross(p,r),n),dot(cross(r,anchor),n),dot(cross(anchor,p),n)]
        need(sum(weights,Z)==nn,'affine barycentric numerator sum')
        if any(w<0 for w in weights):rejected['outside_active_triangle']+=1;continue
        if d==0:rejected['zero_projection']+=1;continue
        # |v.q|>=q.q iff |v.n|>=|d|, avoiding field inversions here.
        values=[dot(v,n) for v in V]
        if min(map(abs,values))!=abs(d):rejected['violates_signed_hull_support']+=1;continue
        q=scale(n,d/nn);need(dot(q,q)>0,'positive hull distance')
        convex=tuple(sum((weights[i]*v[t]/nn for i,v in enumerate((anchor,p,r))),Z)
                     for t in range(3))
        need(convex==q,'closest point is an explicit convex combination')
        kind[3]+=1;valid.setdefault(q,(0,j,k))
    need(raw==1771 and sum(kind.values())+sum(rejected.values())==raw,'complete anchored simplex cover')
    allq={}
    for q in valid:
        for M in G:
            x=canonical(mv(M,q));allq[x]=dot(x,x)
    reps=[p for p in V if canonical(p)==p]
    need(len(reps)==30,'antipodal representatives')
    regions={}
    for q,score in allq.items():
        products=[dot(v,q) for v in reps]
        need(all(p!=Z for p in products) and min(map(abs,products))==score,'positive signed region support')
        signs=tuple(p.sign() for p in products)
        need(signs not in regions,'unique signed-hull closest point per region')
        active=[i for i,v in enumerate(V) if dot(v,q)==score]
        regions[signs]=(q,score,active)
    need(len(regions)==436,'complete optimizer region count')
    spectrum=Counter(score for q,score,active in regions.values())
    ordered=sorted(spectrum,reverse=True);beta=(19-8*PHI)/29
    need(len(ordered)==11 and ordered[0]==Q(F(1,3)) and spectrum[ordered[0]]==10,'global axial optimum')
    need(ordered[1]==beta and spectrum[beta]==60 and Q(F(1,3))-beta>Q(F(1,1000)),'sharp runner-up gap')
    def ray(p):return scale(p,1/next(x for x in p if x!=Z))
    d=(Z,ONE,-PHI*PHI)
    need({ray(p) for p,score,a in regions.values() if score==Q(F(1,3))}
         =={ray(mv(M,d)) for M in G},'all ten optimal axes equal the threefold orbit')
    diameter2=4*(R2-Q(F(1,3)));scale2=R2/(R2-Q(F(1,3)))
    need(diameter2==Q(F(80,3))+32*PHI and scale2==(87-6*PHI)/76 and scale2>1,
         'exact minimum diameter and strict-passage scale bound')
    records=[{'signs':''.join('+' if q>0 else '-' for q in signs),'closest_point':encode(p),
              'height_squared':score.encode(),'active_vertices':active}
             for signs,(p,score,active) in sorted(regions.items())]
    digest=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    summary={'anchored_simplex_cases':raw,'passing_cases_by_simplex_size':dict(kind),
             'rejected_cases':dict(rejected),'passing_distinct_anchor_points':len(valid),
             'projective_regions':len(regions),'spectrum':[{'height_squared':q.encode(),'regions':spectrum[q]}
                                                         for q in ordered],
             'active_count_histogram':dict(Counter(len(a) for p,q,a in regions.values())),
             'minimum_squared_shadow_diameter':diameter2.encode(),
             'strict_passage_squared_scale_upper':scale2.encode(),
             'optimizer_records_sha256':digest}
    return regions,summary,records

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);p.add_argument('--records',type=Path)
    args=p.parse_args();start=time.monotonic();V=vertices();G,gs=group(V)
    print('proper group complete',file=sys.stderr,flush=True)
    regions,rs,records=optimizers(V,G)
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer','field':'Q(sqrt5)',
            'vertices':60,'group':gs,'axial':rs}
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(text)
    if args.records:args.records.write_text(json.dumps(records,indent=2,sort_keys=True)+'\n')
    print(text);print(json.dumps({'seconds':time.monotonic()-start,
                                'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}),file=sys.stderr)

if __name__=='__main__':main()
