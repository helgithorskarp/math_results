#!/usr/bin/env python3
"""Exact definition checks, incidence images and uniform polynomial evidence."""
import argparse
from fractions import Fraction as F
from itertools import combinations,product
import json
from pathlib import Path

import certificates as base
import deletions
import dense_cone_polynomials as polynomial
import dense_regular_cones as cone
import maxrank_mixtures as repair
from verify import check,psd_ldl,require,rejection_controls
from verify_clique_centers import matvec,combination,image_block,congruence,basis_rank
from verify_clique_centers import partition_check,core_buffer,fingerprint,maximum_stars
from verify_two_centers import maximum_intersecting_families


def rref(matrix):
    rows=[[F(x) for x in row] for row in matrix]
    columns=len(rows[0]);rank=0;pivots=[]
    for col in range(columns):
        pivot=next((i for i in range(rank,len(rows)) if rows[i][col]),None)
        if pivot is None:continue
        rows[rank],rows[pivot]=rows[pivot],rows[rank]
        value=rows[rank][col]
        rows[rank]=[x/value for x in rows[rank]]
        for i in range(len(rows)):
            if i!=rank and rows[i][col]:
                value=rows[i][col]
                rows[i]=[a-value*b for a,b in zip(rows[i],rows[rank])]
        pivots.append(col);rank+=1
        if rank==len(rows):break
    return rows[:rank],pivots


def nullspace(matrix):
    rows,pivots=rref(matrix);columns=len(matrix[0]);answer=[]
    for free in range(columns):
        if free in pivots:continue
        vector=[F(int(i==free)) for i in range(columns)]
        for row,pivot in zip(rows,pivots):vector[pivot]=-row[free]
        answer.append(vector)
    return answer


def incidence_images(h,edges,core):
    edges,d=cone.normalize(h,edges);m=len(edges)
    members=cone.family(h,edges)[1:];index={a:i for i,a in enumerate(members)}
    center=1 << h;w=cone.parameters(h,d)
    adjacency=[[F(int(tuple(sorted((i,j))) in edges)) for j in range(h)] for i in range(h)]
    incidence=[[F(int(i in edge)) for edge in edges] for i in range(h)]
    require(all(sum(incidence[i][k]*incidence[j][k] for k in range(m))==
                d*int(i==j)+adjacency[i][j] for i in range(h) for j in range(h)),
            "BB^T=dI+A failed")

    def vector(a=0,x=None,c=None,e=None):
        result=[F(0)]*len(members);result[index[center]]=F(a)
        for i in range(h):
            result[index[center|(1 << i)]]=F(x[i]) if x is not None else F(0)
            result[index[1 << i]]=F(c[i]) if c is not None else F(0)
        for k,(i,j) in enumerate(edges):
            result[index[(1 << i)|(1 << j)]]=F(e[k]) if e is not None else F(0)
        return result
    def inc(y):return [y[i]+y[j] for i,j in edges]
    def addvec(y,z,scale=1):return [a+scale*b for a,b in zip(y,z)]

    basis=[];edge_kernel=nullspace(incidence)
    for q in edge_kernel:
        require(all(not sum(a*b for a,b in zip(row,q)) for row in incidence),
                "Computed edge kernel failed")
        v=vector(e=q)
        require(matvec(core,v)==[(h+2+w['z'])*a for a in v],
                "Edge-kernel scalar image failed")
        basis.append(v)
    edge_images=[]
    for i in range(h-1):
        y=[F(int(k==i)-int(k==h-1)) for k in range(h)]
        Ay=matvec(adjacency,y);by=addvec([-a for a in y],Ay,F(2,d))
        cy=addvec([h*a for a in y],Ay,-w['alpha'])
        qy=addvec([d*a for a in y],Ay)
        ey=addvec([(h+2+w['z'])*a for a in y],qy,-(1+w['z']))
        X,C,E=vector(x=y),vector(c=y),vector(e=inc(y))
        require(matvec(core,X)==vector(x=[(h+1)*a for a in y],c=by,
                                      e=[-(1+w['w'])*a for a in inc(y)]),
                "General spoke-standard image failed")
        require(matvec(core,C)==vector(x=by,c=cy,e=[-a for a in inc(y)]),
                "General singleton-standard image failed")
        require(matvec(core,E)==vector(x=[-(1+w['w'])*a for a in qy],
                                      c=[-a for a in qy],e=inc(ey)),
                "General edge-incidence image failed")
        basis += [X,C];edge_images.append(inc(y))
    rows,_=rref(edge_images)
    basis += [vector(e=row) for row in rows]

    constants=[vector(a=1),vector(c=[1]*h),vector(x=[1]*h),vector(e=[1]*m)]
    small=[[F(h),F(-h)],[F(-h),F(h*d)]]
    gram=congruence([[1,0],[0,1],[-1,0],[0,-1]],small)
    require(psd_ldl(small)==2,"Constant top Gram block not PD")
    image_block(core,constants,gram,list(map(F,(1,h,h,m))))
    basis += constants
    require(len(basis)==len(members) and basis_rank(basis)==len(members),
            "Complete incidence basis failed to span the core")
    return dict(core_dimension=len(members),edge_kernel_dimension=len(edge_kernel),
                centered_edge_image_dimension=len(rows),complete_basis_rank=len(members))


def bipartite(t):
    return sorted((i,t+j) for i,j in product(range(t),repeat=2))


def circulant(h,steps):
    return sorted({tuple(sorted((i,(i+j)%h))) for i in range(h) for j in steps})


def complement(h,edges):
    missing=set(edges)
    return [e for e in combinations(range(h),2) if e not in missing]


def inherited_baseline():
    deleted=[e for group in (range(3),range(3,6)) for e in combinations(group,2)]
    family,matrix,s=deletions.deletion_certificate(7,deleted);n=len(family)
    require(family==cone.family(6,bipartite(3)) and n==23 and s==7,
            "Useful inherited baseline family mismatch")
    rank=check(family,matrix,s)
    Qtop,vector=deletions.regular_eigenvector(7,deleted)
    eigenvalue=(Qtop-s)/(n-s)
    require(Qtop==F(172,5) and eigenvalue==F(137,80),"Wrong inherited eigenvalue")
    require(matvec(matrix,vector)==[eigenvalue*a for a in vector],
            "Inherited M eigenvector failed")
    quadratic=sum(vector[i]*(vector[i]-a) for i,a in enumerate(matvec(matrix,vector)))
    require(quadratic==F(-95589,125),"Wrong exact negative upper quadratic")
    cap,scalar=deletions.cap_test(7,deleted)
    require(not cap and scalar==F(52,33),"Wrong inherited cap rejection")
    try:check(family,matrix,s,upper=True)
    except ValueError:pass
    else:raise RuntimeError("Failed inherited cap accepted")
    return dict(N=n,s=s,inherited_L_rank=rank,inherited_Q_top=str(Qtop),
                inherited_M_top=str(eigenvalue),cap_scalar=str(scalar),
                negative_upper_quadratic=str(quadratic),
                status="failure of inherited template; not nonexistence")


def run():
    symbolic,certificate=polynomial.verify_certificate()
    fixture=Path(__file__).with_name("dense_cone_determinants.json")
    require(json.loads(fixture.read_text())==certificate,"Coefficient certificate mismatch")
    cases=[]
    inputs=[("K2,2",4,bipartite(2)),("K3,3",6,bipartite(3)),
            ("K4,4",8,bipartite(4)),("K5,5",10,bipartite(5)),
            ("K6,6",12,bipartite(6)),
            ("triangular-prism",6,[(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)]),
            ("K6-minus-matching",6,complement(6,[(0,1),(2,3),(4,5)])),
            ("K7-minus-C7",7,complement(7,circulant(7,[1]))),
            ("C8-distance1,2",8,circulant(8,[1,2])),
            ("K8-minus-C8",8,complement(8,circulant(8,[1]))),
            ("K9-minus-C9",9,complement(9,circulant(9,[1]))),
            ("K12-minus-matching",12,complement(12,[(i,i+1) for i in range(0,12,2)]))]
    for name,h,edges in inputs:
        edges,d=cone.normalize(h,edges)
        members,centered,s=cone.centered_certificate(h,edges);n=len(members)
        core=cone.core(h,edges)
        require(base.extract_core(centered,s)==core,"Centered lift/extraction mismatch")
        require(all(sum(row)==0 for row in core),"Core not centered")
        require(all(core[i][j]>=-1 for i in range(n-1) for j in range(n-1) if i!=j),
                "Bad centered nonempty off-diagonal")
        star=[F(bool(a & (1 << h))) for a in members[1:]]
        require(not any(matvec(core,star)),"Center star core kernel failed")
        require(check(members,centered,s)==n-2,"Centered Hoffman rank failed")
        core_buffer(core,n,F(1))
        images=incidence_images(h,edges,core)
        colors=cone.colors(h,edges);counts,functional=partition_check(members,colors,s)
        require(functional>0 and n % s not in (0,1),"Partition nonconstant/congruence failed")
        repaired,epsilon=repair.repaired_core(core,colors,s)
        fam,matrix,s2=cone.certificate(h,edges)
        require(fam==members and s2==s and matrix==base.lift(repaired,s),
                "Repaired constructor/lift mismatch")
        rank=check(members,matrix,s,upper=True)
        require(rank==n-1,"Unrestricted maximal rank failed")
        core_buffer(repaired,n,F(1,2))
        require(all(matrix[i][j]>=0 for i in range(n) for j in range(n) if i!=j),
                "Negative repaired off-diagonal")
        maxima=maximum_intersecting_families(members)
        require(maxima==maximum_stars(members,s) and len(maxima)==1,
                "Unique center-star equality failed")
        cases.append(dict(name=name,h=h,d=d,N=n,s=s,centered_L_rank=n-2,
                          repaired_L_rank=rank,incidence_images=images,
                          partition_sizes=counts,partition_functional=functional,
                          epsilon=str(epsilon),maximum_families=len(maxima),
                          repaired_matrix_sha256=fingerprint(matrix)))
    products=[]
    small=cone.certificate(4,bipartite(2))
    singleton_family=[0,1 << 5,1 << 6,1 << 7]
    singleton_matrix=[[F(int(i!=j),3) for j in range(4)] for i in range(4)]
    require(check(singleton_family,singleton_matrix,1,upper=True)==1,"Rank-one factor baseline failed")
    for factors,eligible in (([small,cone.certificate(4,bipartite(2),5)],2),
                             ([small,(singleton_family,singleton_matrix,1)],1)):
        family,matrix,s=base.product_certificate(factors);n=len(family)
        rank=check(family,matrix,s,upper=True)
        require(rank==n-eligible,"Product maximal rank failed")
        require(len(maximum_stars(family,s))==eligible,"Product maximum star count failed")
        products.append(dict(N=n,s=s,L_rank=rank,maximum_stars=eligible,
                             matrix_sha256=fingerprint(matrix)))
    rejected=0
    for h,edges in ((True,[]),(3,[(0,1),(0,2),(1,2)]),
                    (4,[(0,0)]),(4,[(False,1)]),
                    (4,[(0,1),(1,0)]),(4,[(0,1)]),
                    (4,list(combinations(range(4),2))),
                    (4,[(0,1),(1,2),(2,3)]),(4,[(0,4)])):
        try:cone.certificate(h,edges)
        except (TypeError,ValueError):rejected+=1
        else:raise RuntimeError("Invalid cone input accepted")
    rejection_controls()
    return dict(agent="six-downset-1",role="researcher",symbolic_certificate=symbolic,
                cases=cases,base_N_max=max(a['N'] for a in cases),products=products,
                inherited_baseline=inherited_baseline(),
                invalid_inputs_rejected=rejected,PSD_certificate_controls=3)


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--check",action="store_true")
    args=parser.parse_args();result=run()
    if args.check:
        expected=Path(__file__).with_name("dense_regular_cones_expected.json")
        require(json.loads(expected.read_text())==result,"Expected-output mismatch")
    print(json.dumps(result,sort_keys=True,indent=2))
