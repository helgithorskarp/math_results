#!/usr/bin/env python3
"""Exact regular-cone checks; literal matrices and complete incidence bases."""
import argparse,copy,json
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
import certificates as base
import dense_regular_cones as dense
import maxrank_mixtures as repair
import regular_cones as cone
import regular_cone_polynomials as polynomial
from verify import check,psd_ldl,require,rejection_controls
from verify_dense_regular_cones import rref,nullspace,circulant,complement,bipartite,inherited_baseline
from verify_clique_centers import matvec,image_block,congruence,basis_rank
from verify_clique_centers import partition_check,core_buffer,fingerprint,maximum_stars
from verify_two_centers import maximum_intersecting_families


def components(h,edges):
    neighbors=[[] for _ in range(h)]
    for i,j in edges:neighbors[i].append(j);neighbors[j].append(i)
    remaining=set(range(h));answer=[];bipartite_count=0
    while remaining:
        start=min(remaining);color={start:1};stack=[start];bipartite_component=True
        while stack:
            i=stack.pop()
            for j in neighbors[i]:
                if j in color:
                    if color[j]==color[i]:bipartite_component=False
                else:color[j]=-color[i];stack.append(j)
        vertices=sorted(color);remaining.difference_update(vertices)
        answer.append((vertices,color,bipartite_component))
        bipartite_count+=int(bipartite_component)
    return answer,bipartite_count


def incidence_images(h,edges,C):
    edges,d=cone.normalize(h,edges);ell=len(edges)
    members=cone.family(h,edges)[1:];index={a:i for i,a in enumerate(members)}
    center=1 << h;w=cone.parameters(h,d)
    adjacency=[[F(int(tuple(sorted((i,j))) in edges)) for j in range(h)] for i in range(h)]
    B=[[F(int(i in edge)) for edge in edges] for i in range(h)]
    require(all(sum(B[i][k]*B[j][k] for k in range(ell))==
                d*int(i==j)+adjacency[i][j] for i in range(h) for j in range(h)),
            "Literal BB^T=dI+A failed")
    comps,b=components(h,edges)
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

    basis=[];edge_kernel=nullspace(B)
    require(len(edge_kernel)==ell-h+b,"Incidence rank/bipartite-component formula failed")
    for q in edge_kernel:
        v=vector(e=q)
        require(matvec(C,v)==[(h+2+w['z'])*a for a in v],"Edge-kernel scalar image failed")
        basis.append(v)
    edge_images=[]
    for i in range(h-1):
        y=[F(int(k==i)-int(k==h-1)) for k in range(h)]
        Ay=matvec(adjacency,y);by=addvec([-a for a in y],Ay,F(2,d))
        cy=addvec([h*a for a in y],Ay,-w['alpha']);gy=addvec([d*a for a in y],Ay)
        ey=addvec([(h+2+w['z'])*a for a in y],gy,-(1+w['z']))
        X,S,E=vector(x=y),vector(c=y),vector(e=inc(y))
        require(matvec(C,X)==vector(x=[(h+1)*a for a in y],c=by,
                                   e=[-(1+w['w'])*a for a in inc(y)]),"Spoke module image failed")
        require(matvec(C,S)==vector(x=by,c=cy,e=[-a for a in inc(y)]),"Singleton module image failed")
        require(matvec(C,E)==vector(x=[-(1+w['w'])*a for a in gy],c=[-a for a in gy],e=inc(ey)),
                "Edge-incidence module image failed")
        basis += [X,S];edge_images.append(inc(y))
    rows,_=rref(edge_images)
    require(len(rows)==h-1-b,"Nonconstant incidence image dimension failed")
    basis += [vector(e=row) for row in rows]

    # Explicit -d modes from each bipartite component; multiple components
    # are handled separately rather than assuming a unique bipartite mode.
    for vertices,color,is_bipartite in comps:
        if not is_bipartite:continue
        y=[F(color.get(i,0)) for i in range(h)]
        require(not sum(y) and not any(inc(y)),"Bipartite zero-incidence vector failed")
        require(matvec(adjacency,y)==[-d*a for a in y],"Bipartite -d eigenvector failed")
    # Component differences are genuine nonconstant d modes.
    for vertices,_,_ in comps[1:]:
        first=comps[0][0]
        y=[F(int(i in vertices),len(vertices))-F(int(i in first),len(first)) for i in range(h)]
        require(not sum(y) and matvec(adjacency,y)==[d*a for a in y],
                "Nonconstant d mode from disconnected components failed")
        require(sum(a*a for a in inc(y))==2*d*sum(a*a for a in y),"Top-mode incidence norm failed")

    constants=[vector(a=1),vector(c=[1]*h),vector(x=[1]*h),vector(e=[1]*ell)]
    norms=list(map(F,(1,h,h,ell)))
    K=[[F(h),F(-h)],[F(-h),F(h*d)]]
    gram=congruence([[1,0],[0,1],[-1,0],[0,-1]],K)
    require(psd_ldl(K)==2,"Constant active Gram is not PD")
    image_block(C,constants,gram,norms)
    require(sum(gram[i][i]/norms[i] for i in range(4))==h+d+3,"Normalized constant trace failed")
    N=len(members)+1
    upper_buffer=[[(N-1)*norms[i]*int(i==j)-norms[i]*norms[j]-gram[i][j]
                   for j in range(4)] for i in range(4)]
    require(psd_ldl(upper_buffer)==3,"Constant U-I buffer or total direction failed")
    basis += constants
    require(len(basis)==len(members) and basis_rank(basis)==len(members),"Incomplete incidence spanning basis")
    return dict(core_dimension=len(members),components=len(comps),bipartite_components=b,
                nonconstant_d_modes=len(comps)-1,edge_kernel_dimension=len(edge_kernel),
                centered_edge_image_dimension=len(rows),constant_trace=h+d+3,
                complete_basis_rank=len(members))


def disjoint_union(parts):
    offset=0;edges=[]
    for h,pairs in parts:
        edges += [(i+offset,j+offset) for i,j in pairs];offset+=h
    return offset,edges


def fixture_check(fixture):
    summary,expected=polynomial.verify_certificate()
    require(fixture==expected,"Coefficient fixture differs from the fixed polynomial")
    previous=json.loads(Path(__file__).with_name('dense_cone_determinants.json').read_text())
    require(fixture['dense']==previous,"Dense coefficient baseline changed")
    return summary


def run():
    fixture=json.loads(Path(__file__).with_name('regular_cone_determinants.json').read_text())
    symbolic=fixture_check(fixture);coefficient_rejections=0
    for mode in (0,1,2):
        corrupt=copy.deepcopy(fixture)
        if mode==0:corrupt['sparse']['P0'][0][-1]+=1
        elif mode==1:corrupt['middle']['minus_P3'][0][-1]*=-1
        else:corrupt['sparse']['P1'].pop()
        try:fixture_check(corrupt)
        except ValueError:coefficient_rejections+=1
        else:raise RuntimeError("Corrupted coefficient table accepted")
    inputs=[('C'+str(h),h,circulant(h,[1])) for h in (5,6,7,10,12)]
    inputs += [('Mobius8',8,circulant(8,[1,4])),('Mobius12',12,circulant(12,[1,6])),
               ('middle-h9-d4',9,circulant(9,[1,2]))]
    for name,parts in [('two-C3',[(3,circulant(3,[1]))]*2),
                       ('two-C4',[(4,circulant(4,[1]))]*2),
                       ('three-C4',[(4,circulant(4,[1]))]*3),
                       ('C3-and-C4',[(3,circulant(3,[1])),(4,circulant(4,[1]))]),
                       ('two-K3,3',[(6,bipartite(3))]*2)]:
        h,edges=disjoint_union(parts);inputs.append((name,h,edges))
    inputs += [('dense-K2,2',4,bipartite(2)),('dense-K3,3',6,bipartite(3)),
               ('dense-K7-minus-C7',7,complement(7,circulant(7,[1])))]
    cases=[];dense_comparisons=0
    for name,h,edges in inputs:
        edges,d=cone.normalize(h,edges);family,centered,s=cone.centered_certificate(h,edges)
        N=len(family);C=cone.core(h,edges)
        require(base.extract_core(centered,s)==C,"Centered extraction mismatch")
        require(all(sum(row)==0 for row in C),"Centering failed")
        star=[F(bool(a & (1 << h))) for a in family[1:]]
        require(not any(matvec(C,star)),"Center star kernel failed")
        require(check(family,centered,s)==N-2,"Centered rank failed")
        core_buffer(C,N,F(1));images=incidence_images(h,edges,C)
        colors=cone.colors(h,edges);counts,functional=partition_check(family,colors,s)
        require(functional>0 and N % s not in (0,1),"Partition/congruence failed")
        repaired,epsilon=repair.repaired_core(C,colors,s)
        members,M,s2=cone.certificate(h,edges)
        require(members==family and s==s2 and M==base.lift(repaired,s),"Repaired lift mismatch")
        rank=check(family,M,s,upper=True);require(rank==N-1,"Maximal lower rank failed")
        core_buffer(repaired,N,F(1,2))
        maxima=maximum_intersecting_families(family)
        require(maxima==maximum_stars(family,s) and len(maxima)==1,"Unique center star failed")
        if h<=2*d:
            require(cone.certificate(h,edges)==dense.certificate(h,edges),"Published dense matrix changed")
            require(all(M[i][j]>=0 for i in range(N) for j in range(N) if i!=j),"Dense signs changed")
            dense_comparisons+=1
        cases.append(dict(name=name,h=h,d=d,N=N,s=s,centered_L_rank=N-2,repaired_L_rank=rank,
                          incidence_images=images,partition_sizes=counts,partition_functional=functional,
                          epsilon=str(epsilon),minimum_repaired_off_diagonal=str(min(M[i][j] for i in range(N) for j in range(N) if i!=j)),
                          matrix_sha256=fingerprint(M)))
    # Two full tensors suffice to exercise a strict density comparison and
    # a tie. Their infinite rank/equality proof is separate.
    rankone_family=[0,1 << 20,1 << 21,1 << 22]
    rankone_M=[[F(int(i!=j),3) for j in range(4)] for i in range(4)]
    small=cone.certificate(5,circulant(5,[1]))
    products=[]
    for factors,c in [([small,(rankone_family,rankone_M,1)],1),
                      ([cone.certificate(4,bipartite(2)),cone.certificate(4,bipartite(2),5)],2)]:
        family,M,s=base.product_certificate(factors);N=len(family)
        require(check(family,M,s,upper=True)==N-c,"Product rank failed")
        require(len(maximum_stars(family,s))==c,"Eligible product stars failed")
        products.append(dict(N=N,s=s,L_rank=N-c,eligible_stars=c,matrix_sha256=fingerprint(M)))
    rejected=0
    bad=[(True,[]),(3,circulant(3,[1])),(4,[(0,0)]),(4,[(False,1)]),
         (4,[(0,1),(1,0)]),(4,[(0,1),(2,3)]),(4,list(combinations(range(4),2))),
         (4,[(0,1),(1,2),(2,3)]),(4,[(0,4)]),(5,[(0,1,2)])]
    for h,edges in bad:
        try:cone.certificate(h,edges)
        except (TypeError,ValueError):rejected+=1
        else:raise RuntimeError("Invalid regular graph input accepted")
    for shift in (True,-1):
        try:cone.certificate(5,circulant(5,[1]),shift)
        except ValueError:rejected+=1
        else:raise RuntimeError("Invalid shift accepted")
    rejection_controls()
    return dict(agent='six-downset-1',role='researcher',symbolic_certificate=symbolic,cases=cases,
                base_N_max=max(a['N'] for a in cases),dense_entrywise_comparisons=dense_comparisons,
                products=products,inherited_baseline=inherited_baseline(),
                malformed_inputs_rejected=rejected,coefficient_corruptions_rejected=coefficient_rejections,
                PSD_rejection_controls=3)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=run()
    if args.check:
        expected=json.loads(Path(__file__).with_name('regular_cones_expected.json').read_text())
        require(result==expected,"Expected result mismatch")
    print(json.dumps(result,sort_keys=True,indent=2))
