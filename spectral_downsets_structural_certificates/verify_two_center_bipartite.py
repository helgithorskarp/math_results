#!/usr/bin/env python3
"""Exact literal H/cap/rank checks, complete images and uniform certificates."""
import argparse,copy,json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import certificates as base
import deletions
import maxrank_mixtures as repair
import two_center_bipartite as cone
import two_center_bipartite_polynomials as poly
from verify import check,psd_ldl,require,rejection_controls
from verify_clique_centers import matvec,image_block,basis_rank,core_buffer
from verify_clique_centers import partition_check,maximum_stars,fingerprint
from verify_two_centers import maximum_intersecting_families


def invariants(u,v,C):
    D=cone.family(u,v)[1:];h=u+v
    require(all(sum(row)==0 for row in C),'Literal core not centered')
    for c in (1 << h,1 << (h+1)):
        require(not any(matvec(C,[F(bool(x & c)) for x in D])),'Center star not killed')


def literal_images(u,v,w,C):
    D=cone.family(u,v)[1:];idx={x:i for i,x in enumerate(D)};h=u+v;A=[1 << h,1 << (h+1)]
    L,R,Kstd,Hstd,K,G,norms,scalars=poly.numeric_blocks(u,v,w);basis=[]
    def vector(entries):
        ans=[F(0)]*len(D)
        for mask,value in entries:ans[idx[mask]]+=value
        return ans
    for i in range(u-1):
        x=[int(k==i)-int(k==u-1) for k in range(u)]
        for j in range(v-1):
            y=[int(k==j)-int(k==v-1) for k in range(v)]
            z=vector([((1 << p)|(1 << (u+q)),x[p]*y[q]) for p in range(u) for q in range(v)])
            require(matvec(C,z)==[scalars[2]*a for a in z],'Double grid image failed');basis.append(z)
    for q,side,matrix,offset,size in ((v,'L',L,0,u),(u,'R',R,u,v)):
        for k in range(size-1):
            x=[int(j==k)-int(j==size-1) for j in range(size)]
            entries=[(a|(1 << (offset+j)),x[j]) for a in A for j in range(size)]
            spoke=vector(entries);single=vector([(1 << (offset+j),x[j]) for j in range(size)])
            edge=vector([((1 << i)|(1 << (u+j)),x[i] if side=='L' else x[j]) for i in range(u) for j in range(v)])
            image_block(C,[spoke,single,edge],matrix,[F(2),F(1),F(q)]);basis += [spoke,single,edge]
            center_standard=vector([(a|(1 << (offset+j)),(1 if c==0 else -1)*x[j]) for c,a in enumerate(A) for j in range(size)])
            scalar=scalars[0 if side=='L' else 1]
            require(matvec(C,center_standard)==[scalar*a for a in center_standard],'Center-times-leaf image failed');basis.append(center_standard)
    std=[vector([(a,1 if c==0 else -1) for c,a in enumerate(A)])]
    std += [vector([(a|(1 << j),1 if c==0 else -1) for c,a in enumerate(A) for j in ranges]) for ranges in (range(u),range(u,h))]
    image_block(C,std,Hstd,[F(2),F(2*u),F(2*v)]);basis+=std
    const=[vector([(a,1) for a in A]),vector([(A[0]|A[1],1)])]
    const += [vector([(a|(1 << j),1) for a in A for j in ranges]) for ranges in (range(u),range(u,h))]
    const += [vector([(1 << j,1) for j in ranges]) for ranges in (range(u),range(u,h))]
    const += [vector([((1 << i)|(1 << (u+j)),1) for i in range(u) for j in range(v)])]
    image_block(C,const,G,norms);basis+=const
    require(len(basis)==len(D) and basis_rank(basis)==len(D),'Incomplete basis')
    return dict(complete_basis_rank=len(D),constant_norms=list(map(str,norms)))


def fixture_check(fixture):
    summary,expected=poly.verify_certificate()
    require(fixture==expected,'Coefficient or exact LDL certificate changed')
    return summary


def affine_face_checks():
    records=[]
    for u,v in ((2,2),(2,3),(3,4)):
        w=cone.centered_face(u,v,kL=F(1,3),kR=F(-2,5),kT=F(7,11),
            aL=F(-3,7),aR=F(2,13),tL=F(-4,9),tR=F(3,8),
            bL=F(1,17),bR=F(-2,19),bT=F(5,23),qL=F(-7,29),qR=F(11,31))
        C=cone.core(u,v,w);invariants(u,v,C)
        records.append(dict(u=u,v=v,centered=True,both_star_kernels=True,
                            complete_images=literal_images(u,v,w,C),PSD_claim=False))
    return records


def failed_boundary_tail():
    u=v=2;h=u+v;A=(1 << h)|(1 << (h+1));D=cone.family(u,v)[1:]
    w=cone._tail_face(u,v);C=cone.core(u,v,w);invariants(u,v,C)
    z=[]
    for mask in D:
        if mask & A:
            value=F(18,29) if mask & 1 else F(-18,29) if mask & 2 else F(0)
        elif mask.bit_count()==1:
            value=F(-4,29) if mask & 1 else F(4,29) if mask & 2 else F(0)
        else:value=F(1) if mask & 1 else F(-1) if mask & 2 else F(0)
        z.append(value)
    quadratic=sum(x*y for x,y in zip(z,matvec(C,z)))
    require(quadratic==F(-451,87),'Unmodified boundary tail obstruction changed')
    try:psd_ldl(C)
    except ValueError:pass
    else:raise RuntimeError('Indefinite boundary tail accepted')
    return dict(u=u,v=v,left_block_coordinates=['18/29','-4/29','1'],
        full_negative_quadratic=str(quadratic),
        status='Unmodified tail fails PSD; repaired boundary recipe is separate; no H nonexistence inference')


def recoloring_control():
    u,v=2,7;s=u+v+2;D=cone.family(u,v)
    equitable=base.equitable_colors(s,D,cone.colors(u,v),s)
    require([equitable.count(c) for c in range(s)]==[4]*s,'Equitable input control failed')
    colors=cone.make_nonconstant(D[1:],equitable,s)
    counts,functional=partition_check(D,colors,s)
    require(functional==2*s,'Balanced singleton recoloring functional failed')
    for c in (1 << (u+v),1 << (u+v+1)):
        require(all(x==y for mask,x,y in zip(D[1:],equitable,colors) if mask & c),'Center star recolored')
    return dict(u=u,v=v,before_sizes=[4]*s,after_sizes=counts,partition_functional=functional)


def published_baselines():
    records=[]
    D,M,s=repair.two_center_certificate(5);N=len(D)
    require(check(D,M,s,upper=True)==N-2,'Earlier independent-leaf two-center baseline failed')
    previous=json.loads(Path(__file__).with_name('clique_centers_expected.json').read_text())
    old=next(x for x in previous['companion_mixtures'] if x['family']=='two-center' and x['parameter']==5)
    require(fingerprint(M)==old['repaired_matrix_sha256'],'Earlier two-center baseline fingerprint changed')
    records.append(dict(name='K2 join I_5',N=N,s=s,L_rank=N-2,matrix_sha256=fingerprint(M)))
    for u,v in ((2,2),(2,3),(2,4)):
        deleted=list(combinations(range(u),2))+list(combinations(range(u,u+v),2))
        D,M,s=deletions.deletion_certificate(u+v+2,deleted);N=len(D)
        require(D==cone.family(u,v),'Inherited deletion family differs')
        rank=check(D,M,s);passes,scalar=deletions.cap_test(s,deleted)
        if passes:require(check(D,M,s,upper=True)==rank,'Inherited cap test mismatch')
        else:
            try:psd_ldl([[F(i==j)-M[i][j] for j in range(N)] for i in range(N)])
            except ValueError:pass
            else:raise RuntimeError('Failed inherited cap accepted')
        records.append(dict(name='inherited K2 join K_'+str(u)+','+str(v),N=N,s=s,L_rank=rank,
            cap_passes=passes,cap_scalar=str(scalar),matrix_sha256=fingerprint(M),
            scope='Checks the inherited template only'))
    return records


def run():
    fixture=json.loads(Path(__file__).with_name('two_center_bipartite_determinants.json').read_text())
    symbolic=fixture_check(fixture);corruptions=0
    for mode in range(3):
        corrupt=copy.deepcopy(fixture)
        if mode==0:corrupt['regimes']['u_ge_3']['constant_active'][-1][0][-1]+=1
        elif mode==1:corrupt['regimes']['u2_v_ge_5']['right'][2].pop()
        else:corrupt['boundary_cores'][0]['pivots']['left'][0]='-1'
        try:fixture_check(corrupt)
        except ValueError:corruptions+=1
        else:raise RuntimeError('Corrupt coefficient or LDL fixture accepted')
    inputs=[(2,2),(2,3),(2,4),(2,5),(2,6),(2,15),(2,16),(2,20),
            (3,3),(3,9),(3,10),(4,4),(4,7),(4,8),(5,5),(5,6),(6,6)]
    cases=[]
    for u,v in inputs:
        D,M0,s=cone.centered_certificate(u,v);N=len(D);C=cone.core(u,v);w=cone.parameters(u,v)
        require(N==4+3*(u+v)+u*v,'Wrong family dimension');invariants(u,v,C)
        require(check(D,M0,s,upper=True)==N-3,'Centered H/rank failed')
        require(base.extract_core(M0,s)==C,'Centered core extraction failed')
        core_buffer(C,N,F(1));images=literal_images(u,v,w,C)
        L,R,Kstd,Hstd,K,G,norms,scalars=poly.numeric_blocks(u,v)
        trace=sum(G[i][i]/norms[i] for i in range(7))
        if u!=2 or v>=5:
            expected_trace=5*u+4*v+15-F(v*(u-1),u*u)+F(u+3,v)+F(19,3*u)-F(1,u*u)
            require(trace==expected_trace,'Tail constant trace changed')
        colors=cone.colors(u,v);counts,functional=partition_check(D,colors,s)
        require(functional>0,'Partition leaves total kernel')
        for c in (1 << (u+v),1 << (u+v+1)):
            require(sorted(color for mask,color in zip(D[1:],colors) if mask & c)==list(range(s)),
                    'Center star does not meet every color once')
        patched,epsilon=repair.repaired_core(C,colors,s);D2,M,s2=cone.certificate(u,v)
        require(D==D2 and s==s2 and M==base.lift(patched,s),'Repaired constructor differs')
        require(check(D,M,s,upper=True)==N-2,'Repaired H/maximal rank failed')
        require(psd_ldl([[F(i==j)-M[i][j] for j in range(N)] for i in range(N)])==N-1,'Upper endpoint not simple')
        core_buffer(patched,N,F(1,2))
        maxima=maximum_intersecting_families(D)
        require(maxima==maximum_stars(D,s) and len(maxima)==2,'Two center extremizers failed')
        minimum=min(M[i][j] for i in range(N) for j in range(N) if i!=j)
        require((minimum>=0)==(v<=u*u),'Construction sign boundary failed')
        cases.append(dict(u=u,v=v,N=N,s=s,centered_L_rank=N-3,repaired_L_rank=N-2,
            images=images,normalized_constant_trace=str(trace),partition_sizes=counts,
            partition_functional=functional,epsilon=str(epsilon),maximum_families=len(maxima),
            nonnegative_off_diagonal=minimum>=0,minimum_off_diagonal=str(minimum),matrix_sha256=fingerprint(M)))
    rankone_D=[0,1 << 20,1 << 21,1 << 22]
    rankone_M=[[F(int(i!=j),3) for j in range(4)] for i in range(4)]
    products=[]
    for u,v in ((2,2),(2,3)):
        factors=[cone.certificate(u,v),(rankone_D,rankone_M,1)]
        D,M,s=base.product_certificate(factors);N=len(D)
        require(check(D,M,s,upper=True)==N-2,'Tensor cap/rank failed')
        require(len(maximum_stars(D,s))==2,'Eligible tensor stars failed')
        products.append(dict(N=N,s=s,L_rank=N-2,eligible_stars=2,matrix_sha256=fingerprint(M)))
    rejected=0
    for u,v in ((True,2),(1,2),(2,1),(2,True),(2,2.0),(-2,2)):
        try:cone.certificate(u,v)
        except ValueError:rejected+=1
        else:raise RuntimeError('Invalid part sizes accepted')
    for shift in (True,-1):
        try:cone.certificate(2,3,shift)
        except ValueError:rejected+=1
        else:raise RuntimeError('Invalid shift accepted')
    for value in (True,0.5):
        try:cone.centered_face(2,3,bL=value)
        except ValueError:rejected+=1
        else:raise RuntimeError('Inexact affine coordinate accepted')
    for w in ({},dict(cone.parameters(2,3),bL=0.5)):
        try:cone.core(2,3,w)
        except ValueError:rejected+=1
        else:raise RuntimeError('Invalid custom weights accepted')
    rejection_controls()
    return dict(agent='six-downset-1',role='researcher',symbolic_certificate=symbolic,cases=cases,
        base_N_max=max(x['N'] for x in cases),products=products,twelve_parameter_face=affine_face_checks(),
        failed_boundary_tail=failed_boundary_tail(),recoloring_control=recoloring_control(),
        published_baselines=published_baselines(),malformed_inputs_rejected=rejected,
        corrupted_fixtures_rejected=corruptions,PSD_rejection_controls=3)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=run()
    if args.check:
        expected=json.loads(Path(__file__).with_name('two_center_bipartite_expected.json').read_text())
        require(result==expected,'Expected result differs')
    print(json.dumps(result,sort_keys=True,indent=2))
