"""six-reviewer-1: linear-contact and Householder reconstruction; dual facets.

No author imports or coordinate/certificate inputs. SymPy quotient arithmetic,
independent rational interval signs, and complete supporting-plane census.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import resource
import sys
import time
import sympy as sp
from sympy.polys.polyclasses import ANP

P = [-1,-17,-69,403,4323,10179,-24449,-171609,-279635,119709,
     843073,671593,-148047,348145,1374277,823837]
A_EDGES = {(0,1),(0,4),(0,5),(0,6),(0,7),(1,2),(1,3),(1,4),
           (2,3),(3,4),(4,5),(5,6),(6,7)}
B_EDGES = {(0,1),(0,2),(0,3),(0,4),(1,2),(2,3),(3,4)}

def need(ok,message):
    if not ok:
        raise ValueError(message)

def poly_value(p,x):
    ans=F(0)
    for v in reversed(p):
        ans=ans*x+v
    return ans

def root_interval():
    x=sp.Symbol('x')
    p=sp.Poly.from_list(list(reversed(P)),x,domain=sp.QQ)
    lo,hi=F(2196767,3802339),F(535329,926590)
    need(p.count_roots(sp.Rational(1,2),sp.Rational(3,5))==1,'whole interval root count')
    need(p.count_roots(sp.Rational(lo.numerator,lo.denominator),
                       sp.Rational(hi.numerator,hi.denominator))==1,'root bracket count')
    sl=poly_value(P,lo)
    need(sl*poly_value(P,hi)<0,'root bracket signs')
    for _ in range(160):
        mid=(lo+hi)/2;sm=poly_value(P,mid)
        need(sm!=0,'rational midpoint root')
        if sl*sm>0:
            lo,sl=mid,sm
        else:
            hi=mid
    return lo,hi

class Algebra:
    def __init__(self):
        self.lo,self.hi=root_interval()
        self.mod=[sp.QQ(v) for v in reversed(P)]
        self.zero=self.number(0);self.one=self.number(1)
        self.t=ANP([sp.QQ(1),sp.QQ(0)],self.mod,sp.QQ)
        self.H=[[self.one if i==j else self.t for j in range(3)] for i in range(3)]
        self.HI=[[(self.one/(self.one-self.t) if i==j else self.zero)-
                   self.t/((self.one-self.t)*(self.one+2*self.t))
                   for j in range(3)] for i in range(3)]

    def number(self,x):
        x=F(x)
        return ANP([sp.QQ(x.numerator,x.denominator)],self.mod,sp.QQ)

    def interval(self,a):
        lo=hi=F(0)
        for v in a.to_list():
            v=F(int(v.numerator),int(v.denominator))
            vals=[lo*self.lo,lo*self.hi,hi*self.lo,hi*self.hi]
            lo,hi=min(vals)+v,max(vals)+v
        return lo,hi

    def sign(self,a):
        if a==self.zero:
            return 0
        lo,hi=self.interval(a)
        if lo>0:
            return 1
        if hi<0:
            return -1
        raise ValueError('fixed root bracket does not certify sign')

    def raw_dot(self,a,b):
        return sum((x*y for x,y in zip(a,b)),self.zero)

    def dot(self,a,b):
        # Full bilinear matrix expression; all arithmetic is exact.
        return self.raw_dot(a,self.mv(self.H,b))

    def mv(self,M,x):
        return tuple(self.raw_dot(row,x) for row in M)

    def cross(self,a,b):
        return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

    def solve(self,M,b):
        # Fraction-free elimination is unnecessary for 3x3; pivoted exact
        # Gaussian elimination is different from active-triple Cramer solves.
        rows=[list(row)+[v] for row,v in zip(M,b)]
        for j in range(3):
            piv=next((i for i in range(j,3) if rows[i][j]!=self.zero),None)
            need(piv is not None,'singular linear contact system')
            rows[j],rows[piv]=rows[piv],rows[j]
            d=rows[j][j];rows[j]=[v/d for v in rows[j]]
            for i in range(3):
                if i!=j:
                    d=rows[i][j]
                    rows[i]=[a-d*b for a,b in zip(rows[i],rows[j])]
        return tuple(row[3] for row in rows)

    def householder(self,x,y,points):
        d=tuple(a-b for a,b in zip(x,y));n=self.dot(d,d)
        need(self.sign(n)>0,'Householder denominator')
        return [tuple(a-2*self.dot(d,p)/n*b for a,b in zip(p,d)) for p in points]

def core(f):
    z,o,t=f.zero,f.one,f.t
    basis=[(o,z,z),(z,o,z),(z,z,o)]
    a={0:basis[0],6:basis[1],7:basis[2]}
    r=2*t/(o+t)
    for v,i,j,k in [(5,0,6,7),(4,0,5,6),(1,0,4,5),(3,1,4,0),(2,1,3,4)]:
        a[v]=tuple(r*(x+y)-q for x,y,q in zip(a[i],a[j],a[k]))
    b={0:basis[0],3:basis[1],4:basis[2]}
    b[2]=tuple(r*(x+y)-q for x,y,q in zip(b[0],b[3],b[4]))
    b[1]=tuple(r*(x+y)-q for x,y,q in zip(b[0],b[2],b[3]))
    need(all(f.dot(x,x)==o for x in [*a.values(),*b.values()]),'patch unit identities')
    need(all(f.dot(a[i],a[j])==t for i,j in A_EDGES),'A prescribed contacts')
    need(all(f.dot(b[i],b[j])==t for i,j in B_EDGES),'B prescribed contacts')
    k=f.dot(b[1],b[4])
    need(k==t*(9*t*t-2*t-3)/(o+t)**2,'ear Gram identity')
    w=f.dot(a[5],a[6])
    v=tuple(2*t/(o+w)*(x+y)-q for x,y,q in zip(a[5],a[6],a[0]))
    # The first ear is determined by THREE original contact equations.
    # We neither square an ear radical nor use the author's frame formula.
    u=f.solve([f.mv(f.H,a[2]),f.mv(f.H,a[7]),f.mv(f.H,v)],[t,t,k])
    need(f.dot(u,u)==f.dot(v,v)==o and f.dot(u,v)==k,'ear unit/Gram identities')
    originals=[b[j] for j in range(5)]
    first=f.householder(b[1],u,originals)
    plus=f.householder(first[4],v,first)
    need(plus[1]==u and plus[4]==v,'two-reflection contact alignment')
    h=f.mv(f.HI,f.cross(u,v));nn=f.dot(h,h)
    need(f.sign(nn)>0,'fixed-ear normal positive')
    minus=[tuple(x-2*f.dot(h,p)/nn*y for x,y in zip(p,h)) for p in plus]
    need(minus[1]==u and minus[4]==v,'normal reflection preserves ears')
    edges=A_EDGES|{(i+8,j+8) for i,j in B_EDGES}|{(2,9),(7,9),(5,12),(6,12)}
    branches={}
    for label,B in [('proper',plus),('improper',minus)]:
        points=[a[i] for i in range(8)]+B
        need(all(f.dot(p,p)==o for p in points),'all frame unit norms')
        need(all(f.dot(points[i],points[j])==t for i,j in edges),'24 full contacts')
        collisions=[list(pair) for pair in combinations(range(13),2)
                    if f.sign(f.dot(points[pair[0]],points[pair[1]])-t)>0]
        branches[label]=(points,collisions)
    need(branches['proper'][1] and not branches['improper'][1],'frame packing classification')
    points=branches['improper'][0]
    contacts=[list(pair) for pair in combinations(range(13),2)
              if f.dot(points[pair[0]],points[pair[1]])==t]
    need(len(contacts)==24,'exact contact count')
    return points,{'rejected_frame_collisions':branches['proper'][1],
                   'packing_contacts':contacts,'points':13}

def facets(f,points,selftest=False):
    # Positive origin relation from a normalized 4x4 affine linear solve.
    labels=[0,1,4,8]
    # Solve the first three weights using the fourth as affine base.
    base=points[labels[3]]
    cols=[tuple(x-y for x,y in zip(points[i],base)) for i in labels[:3]]
    M=[list(row) for row in zip(*cols)]
    w=list(f.solve(M,tuple(-x for x in base)));w.append(f.one-sum(w,f.zero))
    need(all(f.sign(x)>0 for x in w),'origin tetrahedron positivity')
    need(all(sum((q*points[i][j] for q,i in zip(w,labels)),f.zero)==f.zero
             for j in range(3)),'exact origin relation')
    planes={};nonfacets=0;total=0;supporting=0
    for tri in combinations(range(13),3):
        total+=1;i,j,k=tri
        v=tuple(x-y for x,y in zip(points[j],points[i]))
        u=tuple(x-y for x,y in zip(points[k],points[i]))
        c=f.cross(v,u);d=f.raw_dot(c,points[i])
        need(f.sign(d)!=0,'origin-coplanar triple')
        signs=[f.sign(f.raw_dot(c,p)-d) for p in points]
        if any(x>0 for x in signs) and any(x<0 for x in signs):
            nonfacets+=1;continue
        supporting+=1
        if any(x>0 for x in signs):
            c=tuple(-x for x in c);d=-d
        need(f.sign(d)>0,'supporting plane positive offset')
        coplanar=tuple(i for i,q in enumerate(signs) if q==0)
        denominator=f.raw_dot(c,f.mv(f.HI,c))
        need(f.sign(denominator)>0,'facet normal norm')
        rho2=d*d/denominator
        # Every supporting plane stays farther than the forbidden threshold.
        need(f.sign(rho2-f.t*f.t)>0,'facet saturation margin')
        need(f.sign(rho2-f.t*f.t*f.number(F(200,199)))>0,'author norm margin')
        need(f.sign(rho2*f.number(174)-f.t*f.t*f.number(175))>0,'sharper norm margin')
        if coplanar in planes:
            need(rho2==planes[coplanar],'coplanar triple consistency')
        else:
            planes[coplanar]=rho2
    need(total==286 and nonfacets==262 and supporting==24 and len(planes)==21,'complete dual-facet census')
    best=next(iter(planes.values()))
    for rho in planes.values():
        if f.sign(rho-best)<0:
            best=rho
    minimizers=[list(face) for face,rho in planes.items() if f.sign(rho-best)==0]
    counts={str(k):v for k,v in Counter(len(face) for face in planes).items()}
    # Rational gap: max_i dot(x_i,y) > theta+1/625 for every unit y.
    need(f.sign(best-(f.t+f.number(F(1,625)))**2)>0,'uniform additive covering gap')
    compact=[F(335708431733,10**12),F(335708431734,10**12)]
    lo,hi=f.interval(best)
    need(compact[0]<lo<=hi<compact[1],'compact squared-offset enclosure')
    edges=[list(pair) for pair in combinations(range(13),2)
           if sum(set(pair)<=set(face) for face in planes)>=2]
    need(len(edges)==32 and 13-len(edges)+len(planes)==2,'dual hull Euler check')
    if selftest:
        # A plausible but false stronger gap must be rejected at the exact
        # minimizing normal; this is a consequential negative bound control.
        need(f.sign(best-(f.t+f.number(F(1,600)))**2)<0,'false 1/600 gap rejected')
        # Independent exact-arithmetic root and sign controls.
        need(f.sign(f.t-f.number(F(1,2)))>0 and
             f.sign(f.number(F(3,5))-f.t)>0,'root/sign controls')
        # Householder on anchor basis: swapping e0/e1 preserves H exactly.
        basis=[tuple(f.one if i==j else f.zero for j in range(3)) for i in range(3)]
        swapped=f.householder(basis[0],basis[1],basis)
        need(swapped==[basis[1],basis[0],basis[2]],'known anchor reflection control')
        # The least facet, oriented outward, must attain the universal bound.
        face=minimizers[0];p,q,r=[points[i] for i in face[:3]]
        c=f.cross(tuple(x-y for x,y in zip(q,p)),tuple(x-y for x,y in zip(r,p)))
        d=f.raw_dot(c,p)
        if f.sign(d)<0:c=tuple(-x for x in c);d=-d
        need(all(f.sign(f.raw_dot(c,p)-d)<=0 for p in points),'minimizer support control')
        need(d*d/f.raw_dot(c,f.mv(f.HI,c))==best,'exact minimizing normal control')
    return {'active_triples':total,'nonsupporting':nonfacets,'supporting_triples':supporting,
            'facets':[list(q) for q in sorted(planes)],'facet_size_histogram':counts,
            'minimum_offset_faces':minimizers,'origin_tetrahedron':labels,
            'hull_edges':edges,'norm_squared_strict_upper_bound':[174,175],
            'covering_gap':[1,625],'minimum_squared_offset_interval':list(map(str,compact))}

def main():
    p=argparse.ArgumentParser();p.add_argument('--phase',choices=['core','all'],default='all')
    p.add_argument('--output',type=Path);p.add_argument('--selftest',action='store_true')
    p.add_argument('--expected',type=Path);args=p.parse_args();start=time.monotonic()
    f=Algebra();points,report=core(f)
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'sympy':sp.__version__,'root_polynomial':P,'root_bisections':160,'core':report}
    print('core complete',file=sys.stderr,flush=True)
    if args.phase=='all':
        from templates import verify
        result['templates']=verify()
        result['dual_cover']=facets(f,points,args.selftest)
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text)
    if args.expected:
        need(json.loads(args.expected.read_text())==result,'expected output equality')
    print(text)
    print(json.dumps({'seconds':time.monotonic()-start,'peak_rss_kib':
                     resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}),file=sys.stderr)

if __name__=='__main__':
    main()
