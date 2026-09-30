#!/usr/bin/env python3
"""Exact matrices, complete rational module images, partitions and mixtures."""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

import certificates as base
import clique_centers as clique
import friendship
import maxrank_mixtures as repair
import two_centers
from verify import check, psd_ldl, require, direct_partition_matrix, rejection_controls
from verify_two_centers import maximum_intersecting_families


def matvec(matrix,vector):
    return [sum(x*y for x,y in zip(row,vector)) for row in matrix]


def combination(basis,coefficients):
    return [sum(v[i]*a for v,a in zip(basis,coefficients))
            for i in range(len(basis[0]))]


def image_block(core,basis,gram,norms):
    for j,vector in enumerate(basis):
        require(matvec(core,vector)==combination(
            basis,[gram[i][j]/norms[i] for i in range(len(basis))]),
            "Invariant block image failed")


def congruence(factor,small):
    return [[sum(F(factor[i][a])*small[a][b]*factor[j][b]
                 for a in range(len(small)) for b in range(len(small)))
             for j in range(len(factor))] for i in range(len(factor))]


def basis_rank(vectors):
    rows=[[F(x) for x in row] for row in vectors]
    rank=0
    for col in range(len(rows[0])):
        pivot=next((i for i in range(rank,len(rows)) if rows[i][col]),None)
        if pivot is None: continue
        rows[rank],rows[pivot]=rows[pivot],rows[rank]
        value=rows[rank][col]
        for j in range(col,len(rows[0])): rows[rank][j]/=value
        for i in range(rank+1,len(rows)):
            value=rows[i][col]
            if value:
                for j in range(col,len(rows[0])):
                    rows[i][j]-=value*rows[rank][j]
        rank+=1
    return rank


def invariant_images(r,t,core):
    members=clique.family(r,t)[1:]
    index={a:i for i,a in enumerate(members)}
    edges=list(combinations(range(r),2))
    ell=len(edges)
    weights=clique.parameters(r,t)
    alpha,q,eta,p,beta,u,v,w,h,z=[weights[a] for a in
        ("alpha","q","eta","p","beta","u","v","w","h","z")]
    d=r+t-1
    require(all(sum(int(i in e)*int(j in e) for e in edges)==
                (r-2 if i==j else 0)+1 for i in range(r) for j in range(r)),
            "Center-edge incidence identity failed")

    def vector(entries):
        answer=[F(0) for _ in members]
        for a,b in entries: answer[index[a]]+=b
        return answer
    all_basis=[]
    pivot_edges={(0,1),(0,2),(1,2)}|{(0,i) for i in range(3,r)}
    for i,j in edges:
        if (i,j) in pivot_edges: continue
        entries=[((1 << i)|(1 << j),1), (3,int(1 not in (i,j))),
                 (5,int(2 not in (i,j))), (6,-1)]
        entries += [((1 << 0)|(1 << k),-int(k in (i,j))) for k in range(3,r)]
        direction=vector(entries)
        require(all(sum(direction[index[(1 << a)|(1 << b)]]
                        for a,b in edges if k in (a,b))==0 for k in range(r)),
                "Edge-kernel basis not in incidence kernel")
        scalar=d+2+eta
        require(matvec(core,direction)==[scalar*a for a in direction],
                "Edge incidence-kernel eigenvalue failed")
        all_basis.append(direction)

    for i in range(r-1):
        x=[int(k==i)-int(k==r-1) for k in range(r)]
        for j in range(t-1):
            y=[int(k==j)-int(k==t-1) for k in range(t)]
            direction=vector([((1 << a)|(1 << (r+b)),x[a]*y[b])
                              for a in range(r) for b in range(t)])
            scalar=d+2+z
            require(matvec(core,direction)==[scalar*a for a in direction],
                    "Center-standard leaf-standard eigenvalue failed")
            all_basis.append(direction)

    leaf_gram=[[d-beta,-r*(1+h)],[-r*(1+h),r*(t+1-(r-1)*z)]]
    require(psd_ldl(leaf_gram)==2,"Leaf-standard block not positive definite")
    for j in range(t-1):
        y=[int(k==j)-int(k==t-1) for k in range(t)]
        directions=[vector([(1 << (r+b),y[b]) for b in range(t)]),
                    vector([((1 << a)|(1 << (r+b)),y[b])
                            for a in range(r) for b in range(t)])]
        image_block(core,directions,leaf_gram,[F(1),F(r)])
        all_basis+=directions

    std_gram=[[d-alpha,-(r-2)*(1+q),-t*(1+v)],
              [-(r-2)*(1+q),(r-2)*(t+3-(r-3)*eta),-(r-2)*t*(1+w)],
              [-t*(1+v),-(r-2)*t*(1+w),t*(r+1-(t-1)*z)]]
    small=[row[:2] for row in std_gram[:2]]
    require(std_gram==congruence([[1,0],[0,1],[-1,-1]],small),
            "Center-standard Gram factorization failed")
    require(psd_ldl(small)==2,"Center-standard top block not positive definite")
    for i in range(r-1):
        x=[int(k==i)-int(k==r-1) for k in range(r)]
        directions=[vector([(1 << a,x[a]) for a in range(r)]),
                    vector([((1 << a)|(1 << b),x[a]+x[b]) for a,b in edges]),
                    vector([((1 << a)|(1 << (r+b)),x[a])
                            for a in range(r) for b in range(t)])]
        image_block(core,directions,std_gram,[F(1),F(r-2),F(t)])
        all_basis+=directions

    A,E,C,X=[vector(entries) for entries in (
        [(1 << a,1) for a in range(r)],
        [((1 << a)|(1 << b),1) for a,b in edges],
        [(1 << (r+b),1) for b in range(t)],
        [((1 << a)|(1 << (r+b)),1) for a in range(r) for b in range(t)])]
    gram=[[r*(d+(r-1)*alpha),r*t*p,r*t*p,r*t*(-1+(r-1)*v)],
          [r*t*p,ell*t*u,ell*t*u,ell*t*(-2+(r-2)*w)],
          [r*t*p,ell*t*u,t*(d+(t-1)*beta),r*t*(-1+(t-1)*h)],
          [r*t*(-1+(r-1)*v),ell*t*(-2+(r-2)*w),r*t*(-1+(t-1)*h),
           r*t*(1+(r-1)*(t-1)*z)]]
    small=[row[:2] for row in gram[:2]]
    require(gram==congruence([[1,0],[0,1],[0,1],[-1,-2]],small),
            "Trivial Gram factorization failed")
    require(psd_ldl(small)==2,"Trivial top block not positive definite")
    image_block(core,[A,E,C,X],gram,list(map(F,(r,ell,t,r*t))))
    all_basis += [A,E,C,X]
    m=len(members)
    require(len(all_basis)==m and basis_rank(all_basis)==m,
            "Rational invariant images do not span the whole core")
    return m


def partition_check(members,colors,s):
    require(len(colors)==len(members)-1,"Wrong partition dimensions")
    require(all(isinstance(c,int) and not isinstance(c,bool) and 0<=c<s for c in colors),
            "Invalid colors")
    for i,a in enumerate(members[1:]):
        for j,b in enumerate(members[1:]):
            if i!=j and a & b:
                require(colors[i]!=colors[j],"Intersecting members share a class")
    counts=[colors.count(c) for c in range(s)]
    require(min(counts)>0,"Empty partition class")
    matrix=base.coloring_certificate(colors,s)
    require(matrix==direct_partition_matrix(colors,s),"Partition entry/lift mismatch")
    functional=s*sum(a*a for a in counts)-(len(members)-1)**2
    return counts,functional


def core_buffer(core,n,buffer):
    m=len(core)
    slack=[[(F(n)-buffer if i==j else 0)-1-core[i][j]
            for j in range(m)] for i in range(m)]
    psd_ldl(slack)


def fingerprint(matrix):
    return sha256(json.dumps([[str(x) for x in row] for row in matrix],
                             separators=(",",":")).encode()).hexdigest()


def maximum_stars(members,s):
    return {tuple(a for a in members if a & (1 << i))
            for i in range(max(members).bit_length())
            if sum(bool(a & (1 << i)) for a in members)==s}


def run():
    cases=[]
    inputs=[(3,2),(3,3),(3,4),(3,6),(4,2),(4,3),(4,4),(4,5),
            (5,2),(5,3),(5,4),(6,2),(6,5),(8,2),(10,2)]
    for r,t in inputs:
        members,centered,s=clique.centered_certificate(r,t)
        n=len(members); core=base.extract_core(centered,s)
        require(core==clique.core(r,t),"Core extraction failed")
        require(all(sum(row)==0 for row in core),"Core not centered")
        require(all(core[i][j]>=-1 for i in range(n-1) for j in range(n-1) if i!=j),
                "Negative nonempty off-diagonal weight")
        require(check(members,centered,s)==n-r-1,"Centered rank failed")
        core_buffer(core,n,F(1))
        dimension=invariant_images(r,t,core)
        colors=clique.colors(r,t)
        counts,functional=partition_check(members,colors,s)
        require(functional>0,"Partition cannot remove extra kernel")
        repaired,epsilon=repair.repaired_core(core,colors,s)
        family,matrix,s2=clique.certificate(r,t)
        require(family==members and s2==s and matrix==base.lift(repaired,s),
                "Constructor/mixture mismatch")
        rank=check(members,matrix,s,upper=True)
        require(rank==n-r,"Repaired rank failed")
        core_buffer(repaired,n,F(1,2))
        require(all(matrix[i][j]>=0 for i in range(n) for j in range(n) if i!=j),
                "Mixture has a negative off-diagonal")
        maxima=maximum_intersecting_families(members)
        require(maxima==maximum_stars(members,s) and len(maxima)==r,
                "Base equality classification failed")
        cases.append(dict(r=r,t=t,N=n,s=s,centered_L_rank=n-r-1,
                          repaired_L_rank=rank,checked_basis_dimension=dimension,
                          partition_sizes=counts,partition_functional=functional,
                          epsilon=str(epsilon),maximum_families=len(maxima),
                          repaired_matrix_sha256=fingerprint(matrix)))

    companions=[]
    for name,values in (("two-center",(2,3,5,20)),("friendship",(2,3,10))):
        for value in values:
            if name=="two-center":
                original=two_centers.certificate(value)
                colors=repair.two_center_colors(value)
                product=repair.two_center_certificate(value)
                count=2; epsilon=F(1,(value+1)**2); buffer=F(2,value+1)
                expected_sizes=[2]*(value+1)+[value+1]
                expected_functional=(value+1)*(value-1)**2
            else:
                original=friendship.certificate(value)
                colors=repair.friendship_colors(value)
                product=repair.friendship_certificate(value)
                count=1; epsilon=F(1,2*(value+2)); buffer=F(1,2)
                expected_sizes=[2]*(value+2)+[3]*(value-1)
                expected_functional=(value-1)*(value+2)
            members,matrix,s=product; n=len(members)
            require(check(*original)==n-count-1,"Prior centered baseline rank failed")
            original_core=base.extract_core(original[1],s)
            core_buffer(original_core,n,F(1))
            counts,functional=partition_check(members,colors,s)
            require(sorted(counts)==expected_sizes and functional==expected_functional,
                    "Explicit equitable partition counts failed")
            core=base.extract_core(matrix,s)
            part=(repair.two_center_partition_average(value) if name=="two-center"
                  else repair.partition_core(colors,s))
            require(core==repair.mix_cores(original_core,part,epsilon),"Companion mixture differs")
            rank=check(*product,upper=True)
            require(rank==n-count,"Companion maximal rank failed")
            core_buffer(core,n,buffer)
            require(all(matrix[i][j]>=0 for i in range(n) for j in range(n) if i!=j),
                    "Companion off-diagonal sign failed")
            if name=="two-center":
                require(matrix[0][0]==F(-2*value,(value+1)**2),"Two-center empty loop failed")
                indices={a:i for i,a in enumerate(members)}
                require(all(matrix[indices[1 << i]][indices[1 << j]]==0
                            for i in range(value) for j in range(value) if i!=j),
                        "Two-center leaf weight not zero")
            else:
                require(matrix[0][0]==F(-1,2),"Friendship empty loop failed")
            require(maximum_intersecting_families(members)==maximum_stars(members,s),
                    "Companion equality classification failed")
            companions.append(dict(family=name,parameter=value,N=n,s=s,L_rank=rank,
                                   epsilon=str(epsilon),core_cap_buffer=str(buffer),
                                   partition_sizes=counts,partition_functional=functional,
                                   repaired_matrix_sha256=fingerprint(matrix)))

    # Independently expand all leaf permutations of the original partition.
    average_cases=[]
    for t in (2,3,4,5):
        members=two_centers.family(t)[1:]; s=t+2
        indexed={a:i for i,a in enumerate(members)}
        colors=repair.two_center_colors(t)
        original=repair.partition_core(colors,s)
        average=[[F(0) for _ in members] for _ in members]
        count=0
        for perm in permutations(range(t)):
            def rename(a):
                return (a & ~((1 << t)-1)) | sum(1 << perm[i] for i in range(t) if a & (1 << i))
            mapping=[indexed[rename(a)] for a in members]
            for i,x in enumerate(mapping):
                for j,y in enumerate(mapping): average[x][y]+=original[i][j]
            count+=1
        average=[[x/count for x in row] for row in average]
        require(average==repair.two_center_partition_average(t),"Leaf-permutation average differs")
        average_cases.append(dict(t=t,permutations=count))

    products=[]
    for factors,expected_nullity in (
        ([clique.certificate(3,2),repair.two_center_certificate(2,5)],2),
        ([repair.two_center_certificate(2),repair.friendship_certificate(2,4)],1)):
        combined=base.product_certificate(factors)
        rank=check(*combined,upper=True)
        require(rank==len(combined[0])-expected_nullity,"Mixed tensor rank failed")
        products.append(dict(N=len(combined[0]),s=combined[2],L_rank=rank))

    # A genuinely balanced proper partition needs the singleton recoloring.
    r,t=3,3; members=clique.family(r,t); s=r+t
    balanced=base.equitable_colors(s,members,clique.colors(r,t),s)
    counts,functional=partition_check(members,balanced,s)
    require(counts==[3]*6 and functional==0,"Balanced branch fixture failed")
    recolored=clique.unbalance_if_needed(members[1:],balanced,s,1 << r)
    _,functional=partition_check(members,recolored,s)
    require(functional==2*s,"Balanced singleton recoloring failed")
    fixed,_=repair.repaired_core(clique.core(r,t),recolored,s)
    require(check(members,base.lift(fixed,s),s,upper=True)==len(members)-r,
            "Recolored partition did not recover maximal rank")

    rejections=0
    for args in ((2,2),(3,1),(True,2),(3,2.0),(3,2,-1),(3,2,True)):
        try: clique.certificate(*args)
        except ValueError: rejections+=1
        else: raise ValueError("Malformed clique input accepted")
    for epsilon in (0,1,F(-1)):
        try: repair.mix(clique.core(3,2),clique.colors(3,2),5,epsilon)
        except ValueError: rejections+=1
        else: raise ValueError("Invalid mixture coefficient accepted")
    # Remove the positive delta in the small-leaf regime: PSD/cap survive,
    # but the lower rank is one smaller, showing why the delta is necessary.
    r,t=4,2; members=clique.family(r,t); bad=clique.core(r,t)
    mask=(1 << r)-1
    for i,a in enumerate(members[1:]):
        for j,b in enumerate(members[1:]):
            if i==j or a & b: continue
            ta="A" if a.bit_count()==1 and a & mask else "C" if a.bit_count()==1 else "E" if a & mask == a else "X"
            tb="A" if b.bit_count()==1 and b & mask else "C" if b.bit_count()==1 else "E" if b & mask == b else "X"
            types="".join(sorted((ta,tb)))
            if types=="AA": bad[i][j]=F(-1)
            elif types=="AX": bad[i][j]=F(2,r-1)
            elif types=="XX": bad[i][j]=F(0)
    bad_rank=check(members,base.lift(bad,r+t),r+t,upper=True)
    require(bad_rank==len(members)-r-2,"Zero-delta control rank failed")
    rejection_controls()

    return dict(agent="six-downset-1",role="researcher",
                scope="Finite exact validation; all-parameter proof in CLIQUE_CENTERS.md",
                clique_cases=cases,companion_mixtures=companions,full_matrix_products=products,
                expanded_partition_averages=average_cases,
                balanced_recoloring_functional=functional,invalid_input_rejections=rejections,
                invalid_PSD_or_certificate_rejections=3,
                zero_delta_control_L_rank=bad_rank,base_N_max=max(a["N"] for a in cases),
                full_matrix_N_max=max(a["N"] for a in cases+products))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    result=run()
    if args.check:
        require(result==json.loads(Path(__file__).with_name("clique_centers_expected.json").read_text()),
                "Output differs from the checked expected file")
    print(json.dumps(result,sort_keys=True,indent=2))
