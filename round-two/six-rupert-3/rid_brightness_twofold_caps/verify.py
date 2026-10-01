#!/usr/bin/env python3
"""Exact finite hypotheses for PROOF.md; no numerical passage search.

Exhaust all original vertex triples, reconstruct physical facet area
vectors, enumerate all area-zonotope facet normals, check the exact
minimum orbit and tangent coercivity, and independently compute every
candidate shadow area by a two-dimensional monotone-chain hull.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

from field import (F, ZERO, ONE, PHI, require, dot, cross, sub, neg, key,
                   encode, ray, vertices, proper_group, act)


def ia(x,y):
    return (x[0]+y[0],x[1]+y[1])


def im(x,y):
    return (x[0]*y[0]+x[1]*y[1],
            x[0]*y[1]+x[1]*y[0]+x[1]*y[1])


def isn(x):
    A,B=2*x[0]+x[1],x[1]
    if not B: return (A>0)-(A<0)
    if not A: return (B>0)-(B<0)
    if A>0 and B>0: return 1
    if A<0 and B<0: return -1
    delta=A*A-5*B*B
    require(delta!=0,"integer sign unexpectedly meets sqrt(5)")
    return (1 if delta>0 else -1)*(1 if A>0 else -1)


def idot(v,w):
    z=(0,0)
    for x,y in zip(v,w): z=ia(z,im(x,y))
    return z


def isub(v,w):
    return tuple((x[0]-y[0],x[1]-y[1]) for x,y in zip(v,w))


def icross(v,w):
    pairs=((1,2),(2,0),(0,1))
    return tuple((im(v[i],w[j])[0]-im(v[j],w[i])[0],
                  im(v[i],w[j])[1]-im(v[j],w[i])[1]) for i,j in pairs)


def vertex_guard(V):
    require(len(V)==60 and len(set(V))==60,"sixty distinct originals required")
    R2=7+8*PHI
    require(all(dot(v,v)==R2 for v in V),"original radii differ")
    require(all(neg(v) in V for v in V),"central symmetry missing")
    require(dot(V[0],cross(V[1],V[2]))!=ZERO,"original span is not three-dimensional")
    return R2


def complete_facets(V):
    # A separate integer-ring representation makes exhaustive hull
    # completeness inexpensive; the rest uses Fraction field arithmetic.
    W=[]
    for v in V:
        require(all(x.a.denominator==x.b.denominator==1 for x in v),
                "original is outside Z[phi]")
        W.append(tuple((int(x.a),int(x.b)) for x in v))
    planes={}
    triples=supporting=through_origin=side_comparisons=0
    for i,j,k in combinations(range(len(W)),3):
        triples+=1
        n=icross(isub(W[j],W[i]),isub(W[k],W[i]))
        require(any(x!=(0,0) for x in n),"collinear original triple")
        h=idot(n,W[i])
        s=isn(h)
        if not s:
            through_origin+=1
            continue
        if s<0:
            n=tuple((-a,-b) for a,b in n)
            h=(-h[0],-h[1])
        coplanar=[]
        for t,w in enumerate(W):
            val=idot(n,w)
            sign=isn((val[0]-h[0],val[1]-h[1]))
            side_comparisons+=1
            if sign>0: break
            if not sign: coplanar.append(t)
        else:
            supporting+=1
            normal=tuple(F(*x)/F(*h) for x in n)
            inds=tuple(coplanar)
            require(normal not in planes or planes[normal]==inds,
                    "same facet plane has inconsistent originals")
            planes[normal]=inds
    require(triples==34220 and supporting==260,"incomplete facet triple enumeration")
    require(len(planes)==62,"wrong number of original facets")
    require(Counter(map(len,planes.values()))=={3:20,4:30,5:12},
            "original facet sizes differ")
    return planes,dict(vertex_triples=triples,supporting_triples=supporting,
                       through_origin_triples=through_origin,
                       integer_side_comparisons=side_comparisons)


def area_generators(V,planes):
    neighbors={i:[] for i in range(len(V))}
    for i,j in combinations(range(len(V)),2):
        d2=dot(sub(V[i],V[j]),sub(V[i],V[j]))
        require(d2>=F(4),"original shortest distance is below two")
        if d2==F(4):
            neighbors[i].append(j)
            neighbors[j].append(i)
    require(all(len(a)==4 for a in neighbors.values()),"edge degree is not four")
    records=[]
    boundary_comparisons=support_comparisons=0
    for normal,inds in sorted(planes.items(),key=lambda item:key(item[0])):
        adj={i:sorted(j for j in neighbors[i] if j in inds) for i in inds}
        require(all(len(a)==2 for a in adj.values()),"facet edges do not give a cycle")
        cycle=[min(inds)]
        cur=adj[cycle[0]][0]
        while cur!=cycle[0]:
            require(cur not in cycle,"facet cycle repeats before closing")
            cycle.append(cur)
            cur=next(j for j in adj[cur] if j!=cycle[-2])
        require(set(cycle)==set(inds),"facet cycle omits an original")
        area=tuple(sum((cross(V[a],V[b])[q]
                       for a,b in zip(cycle,cycle[1:]+cycle[:1])),ZERO)/2
                   for q in range(3))
        if dot(area,normal)<ZERO:
            cycle=cycle[:1]+list(reversed(cycle[1:]))
            area=neg(area)
        require(cross(area,normal)==(ZERO,ZERO,ZERO) and dot(area,normal)>ZERO,
                "facet area vector has wrong direction")
        require(dot(area,area)=={3:F(3),4:F(16),5:15+20*PHI}[len(inds)],
                "physical facet area differs")
        for a,b in zip(cycle,cycle[1:]+cycle[:1]):
            require(dot(sub(V[b],V[a]),sub(V[b],V[a]))==F(4),"facet edge not two")
            for t in inds:
                if t not in (a,b):
                    require(dot(normal,cross(sub(V[b],V[a]),sub(V[t],V[a])))>ZERO,
                            "cyclic face is not its entire convex boundary")
                    boundary_comparisons+=1
        for t,v in enumerate(V):
            value=dot(normal,v)
            require(value<=ONE and (value==ONE)==(t in inds),
                    "Fraction facet support disagrees with integer enumeration")
            support_comparisons+=1
        records.append(dict(indices=cycle,normal=encode(normal),area=encode(area)))
    vectors=[tuple(F(*x) for x in record['area']) for record in records]
    require(all(neg(c) in vectors for c in vectors),"facet area vectors not antipodal")
    C=sorted((c for c in vectors if next(x.sign() for x in c if x!=ZERO)>0),key=key)
    require(len(C)==31 and len(set(C))==31,"area generator representatives differ")
    require(dot(C[0],cross(C[1],C[2]))!=ZERO or
            any(dot(C[0],cross(c,d))!=ZERO for c,d in combinations(C[1:],2)),
            "area zonotope is not full-dimensional")
    return C,records,dict(fraction_facet_support_checks=support_comparisons,
                          facet_boundary_orientation_checks=boundary_comparisons)


def brightness_raw(C,r):
    require(dot(r,r)>ZERO,"zero projection normal")
    return sum((abs(dot(c,r)) for c in C),ZERO)


def direct_shadow_raw(V,r):
    # b and r cross b are orthogonal plane coordinates. Their Jacobian
    # is ||b||^2 ||r||. Thus shoelace area / ||b||^2 equals A(r/||r||)||r||.
    b=(-r[1],r[0],ZERO) if r[0]!=ZERO or r[1]!=ZERO else (ONE,ZERO,ZERO)
    c=cross(r,b)
    points=sorted({(dot(b,v),dot(c,v)) for v in V})
    def turn(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def half(seq):
        hull=[]
        for p in seq:
            while len(hull)>=2 and turn(hull[-2],hull[-1],p)<=ZERO:
                hull.pop()
            hull.append(p)
        return hull
    H=half(points)[:-1]+half(reversed(points))[:-1]
    require(len(H)>=3,"projected polygon is degenerate")
    area=sum((a[0]*b[1]-a[1]*b[0] for a,b in zip(H,H[1:]+H[:1])),ZERO)/2
    require(area>ZERO,"direct projected hull has nonpositive area")
    return area/dot(b,b),len(H)


def local_corollary(V):
    # Recheck the finite hypotheses of the published paired/singleton
    # mirror-cluster theorem, without importing its program or outputs.
    a,b,c=PHI**3,PHI**2,2+PHI
    points=set()
    for sx in (-1,1):
        for sy in (-1,1):
            points.update(((sx*a,F(sy)),(F(sx),sy*a),(sx*b,sy*c)))
    comparisons=0
    minimum=None
    for p in sorted(points,key=key):
        cluster=[v for v in V if v[:2]==p]
        require(len(cluster) in (1,2),"local radial cluster multiplicity differs")
        require({v[2] for v in cluster}==({ZERO} if len(cluster)==1 else {-ONE,ONE}),
                "local cluster original heights differ")
        for v in V:
            if v[:2]!=p:
                gap=dot(p,sub(p,v[:2]))
                require(gap>ZERO,"local radial exposure fails")
                minimum=gap if minimum is None or gap<minimum else minimum
                comparisons+=1
    require(comparisons==700 and minimum==ONE,"local radial gap is not one")
    eta=Fraction(1,100)
    R2=7+8*PHI
    coefficient=a*a*b*b-c*c
    require(a>ONE and ONE<=b<c and c<a*b,"local parameter signs differ")
    require(a*a+2==R2 and b*b+c*c==R2,"local common-radius identities fail")
    require(4*R2*eta+2*R2*eta*eta<ONE,"local support perturbation exceeds gap")
    require(F(1-eta*eta)>(a*a+1)*eta*eta,"local height sign not preserved")
    require(coefficient>ZERO and
            coefficient*coefficient*(1-eta*eta)>
            (a*a+1)*eta*eta*(c*c-b*b)**2,"local quadratic stress condition fails")
    return dict(radial_gap_checks=comparisons,minimum_radial_gap=minimum.encode(),
                published_frame_radius=str(eta))


def scalar_and_roll_gates(V,C,R2,A0,A1sq):
    delta=Fraction(1,30000)
    eta_max=Fraction(1,20)
    require(50<A0<Fraction(115,2) and A0+eta_max<58 and A1sq>F(58**2),
            "global polar threshold not separated")
    require(2*eta_max/Fraction(50)<Fraction(1,20)**2,
            "polar budget does not force initial chord below 1/20")
    require(F(3)<F(Fraction(7,4)**2) and 15+20*PHI<F(Fraction(69,10)**2),
            "surface-area positive root upper bounds fail")
    Lupper=10*Fraction(7,4)+60+6*Fraction(69,10)
    require(Lupper<120,"brightness Lipschitz constant not below 120")
    require(Fraction(999,1000)**2<1-Fraction(1,20)**2/4,
            "tangent positive-root lower bound fails")
    require(14*Fraction(999,1000)-Fraction(115,2)/40>12,
            "linear source coercivity not above twelve")
    require(120*delta<=eta_max and 120*delta/12==Fraction(1,3000),
            "receiving cap outside linear source budget")
    require(Fraction(1,3000)**2+2*delta==Fraction(601,9000000),
            "equatorial support error differs")
    require(601<25**2 and Fraction(27,3000)==Fraction(9,1000)<Fraction(1,100),
            "full source-frame bound exceeds local radius")
    require(R2<25 and R2*Fraction(601,9000000)<ONE,
            "non-equatorial original can pass radial support test")
    require(5*Fraction(26,3000)<Fraction(1,20),"circle matching error not below 1/20")
    b,c=PHI**2,2+PHI
    require(4*(c*c-b*b)>2 and 4*b*b>2 and 4*b*c>Fraction(1,2),
            "proper circle pair gaps not separated")
    qplus,qminus=(b,c),(b,-c)
    circle=[qplus,qminus,neg(qplus),neg(qminus)]
    originals=[v[:2] for v in V if v[2]==ZERO]
    require(set(originals)==set(circle) and len(originals)==4,
            "equatorial original set differs")
    require(all(v[2]==ZERO or v[2]*v[2]>=ONE for v in V),
            "other top-view originals lack the squared-radius gap one")
    allowed=[]
    for p in circle:
        for q in circle:
            if p==q: continue
            if dot(sub(p,q),sub(p,q))==4*c*c and p[0]*q[1]-p[1]*q[0]<ZERO:
                allowed.append((p,q))
    require(set(allowed)=={(qplus,qminus),(neg(qplus),neg(qminus))},
            "a residual proper circle pair survives beyond zero or pi")
    return dict(receiver_chord_radius=str(delta),brightness_lipschitz_upper="120",
                linear_area_budget_max=str(eta_max),linear_source_coercivity_lower="12",
                source_chord_upper="1/3000",source_frame_upper="9/1000",
                pair_matching_absolute_error_upper="1/20",proper_pair_survivors=len(allowed))


def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def self_tests(V):
    rejected=0
    for bad in (V[:-1],V+[V[0]],V[:-1]+[tuple(2*x for x in V[-1])]):
        try: vertex_guard(bad)
        except ValueError: rejected+=1
        else: raise ValueError("malformed original set accepted")
    try: ray((ZERO,ZERO,ZERO))
    except ValueError: rejected+=1
    else: raise ValueError("zero ray accepted")
    require(PHI*PHI==PHI+1 and PHI.inverse()==PHI-1,"field identities fail")
    for x in (PHI-Fraction(8,5),Fraction(13,8)-PHI,2-PHI):
        require(x>ZERO and -x<ZERO,"field positive embedding fails")
    # Definition-level area checks for a cube, independent of the RID.
    cube=[(F(x),F(y),F(z)) for x in (-1,1) for y in (-1,1) for z in (-1,1)]
    for r in ((ONE,ZERO,ZERO),(ONE,ONE,ZERO),(ONE,ONE,ONE)):
        value,_=direct_shadow_raw(cube,r)
        require(value==4*sum((abs(x) for x in r),ZERO),"direct cube area regression fails")
    return rejected


def verify():
    V=vertices()
    R2=vertex_guard(V)
    controls=self_tests(V)
    planes,counts=complete_facets(V)
    C,face_records,face_counts=area_generators(V,planes)
    axes={ray(cross(c,d)) for c,d in combinations(C,2) if cross(c,d)!=(ZERO,ZERO,ZERO)}
    require(len(axes)==121,"complete area-zonotope axis count differs")
    candidates=[]
    direct_sizes=Counter()
    for r in sorted(axes,key=key):
        raw=brightness_raw(C,r)
        direct,size=direct_shadow_raw(V,r)
        require(raw==direct,"Cauchy area and direct original hull disagree")
        direct_sizes[size]+=1
        candidates.append(dict(ray=encode(r),raw_area=raw.encode(),
                               squared_area=(raw*raw/dot(r,r)).encode(),
                               zero_generators=sum(dot(c,r)==ZERO for c in C)))
    for r in ((ONE,F(2),F(3)),(PHI,ONE,F(2)),(F(2),-PHI,ONE)):
        require(brightness_raw(C,r)==direct_shadow_raw(V,r)[0],
                "noncandidate direct original area audit fails")
    A0=12+28*PHI
    A1sq=940+1520*PHI
    spec=Counter(tuple(item['squared_area']) for item in candidates)
    prescribed=[(928+1456*PHI,15),(A1sq,6),(960+1536*PHI,10),
                ((4848+7744*PHI)/5,30),(986+1584*PHI,30),
                (F(Fraction(2960,3))+1584*PHI,30)]
    require(A0*A0==928+1456*PHI,"minimum positive square root differs")
    require(spec==Counter({tuple(x.encode()):count for x,count in prescribed}),
            "complete squared-area spectrum differs")
    require(all(x<y for (x,_),(y,_) in zip(prescribed,prescribed[1:])),
            "squared-area levels are not strictly ordered")
    require(all(x>=A1sq for x,count in prescribed[1:]),"second polar norm level differs")
    minima={tuple(F(*p) for p in item['ray']) for item in candidates
            if item['squared_area']==(A0*A0).encode()}
    G=proper_group(V)
    ez=(ZERO,ZERO,ONE)
    orbit={act(g,ez) for g in G}
    require(len(orbit)==30 and {ray(n) for n in orbit}==minima,
            "minimum brightness axes differ from the proper twofold orbit")
    tangent=[c for c in C if c[2]==ZERO]
    require(len(tangent)==6,"wrong number of equatorial area generators")
    signed_sum=tuple(sum((c[j]*c[2].sign() for c in C),ZERO) for j in range(3))
    require(signed_sum==(ZERO,ZERO,A0),"nonzero-generator signed sum is not axial")
    rho2=F(Fraction(288,5),Fraction(464,5))
    tangent_distances=[]
    for c in tangent:
        r=cross(ez,c)
        raw=brightness_raw(tangent,r)
        tangent_distances.append(raw*raw/dot(r,r))
    require(min(tangent_distances)==rho2 and rho2>196,
            "tangent area inradius is not above fourteen")
    local=local_corollary(V)
    gates=scalar_and_roll_gates(V,C,R2,A0,A1sq)
    return dict(agent="six-rupert-3",role="researcher",
                claim_status="written_geometric_proof_with_exact_finite_hypotheses",
                global_RID_Rupert_status="unresolved",arithmetic="Q(phi), exact rational signs",
                vertex_count=60,facet_sizes={str(k):v for k,v in sorted(Counter(map(len,planes.values())).items())},
                area_generators=31,projective_polar_vertices=121,directed_polar_vertices=242,
                minimum_area=A0.encode(),minimum_squared_area=(A0*A0).encode(),
                second_squared_area=A1sq.encode(),minimum_projective_axes=len(minima),
                proper_body_group=60,directed_minimum_axis_orbit=30,
                candidate_squared_area_spectrum=[dict(value=x.encode(),count=c) for x,c in prescribed],
                direct_shadow_candidate_checks=121,direct_shadow_other_checks=3,
                direct_shadow_hull_sizes={str(k):v for k,v in sorted(direct_sizes.items())},
                tangent_generators=len(tangent),tangent_minimum_squared_inradius=rho2.encode(),
                facet_record_sha256=digest(face_records),candidate_record_sha256=digest(candidates),
                minimum_axes=[encode(r) for r in sorted(minima,key=key)],
                malformed_controls_rejected=controls,**counts,**face_counts,**local,**gates)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--emit',action='store_true',help='print freshly regenerated compact expected JSON')
    args=parser.parse_args()
    result=verify()
    out=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if not args.emit:
        expected=(Path(__file__).parent/'expected.json').read_text()
        require(out==expected,"regenerated expected record differs")
    print(out,end='')


if __name__=='__main__':
    main()
