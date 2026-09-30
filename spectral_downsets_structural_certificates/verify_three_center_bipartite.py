"""Exact literal matrices, complete module images and uniform certificates."""
import argparse,copy,json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import certificates as base
import clique_bipartite_face as face
import three_center_bipartite as cone
import three_center_bipartite_polynomials as poly
import maxrank_mixtures as repair
import two_center_bipartite as old_cone
from bipartite_cones import make_nonconstant
from verify import require,check,psd_ldl,rejection_controls
from verify_clique_centers import matvec,image_block,basis_rank,core_buffer
from verify_clique_centers import partition_check,maximum_stars,fingerprint
from verify_two_centers import maximum_intersecting_families


def invariants(r,u,v,C):
    D=face.family(r,u,v);h=u+v
    require(len(D)==1+r+r*(r-1)//2+(r+1)*h+u*v,'Wrong family dimension')
    expected=[0]+[1 << i for i in range(h+r)]
    expected += [(1 << i)|(1 << j) for i,j in combinations(range(h+r),2)
                 if j>=h or (i<u<=j<h)]
    require(D==sorted(expected),'Literal graph/downset construction differs')
    require(all(sum(row)==0 for row in C),'Core is not centered')
    for c in range(h,h+r):
        require(not any(matvec(C,[F(bool(x & (1 << c))) for x in D[1:]])),'Center star kernel failed')


def literal_images(r,u,v,w,C):
    D=face.family(r,u,v)[1:];h=u+v;A=[1 << (h+i) for i in range(r)];edges=list(combinations(range(r),2))
    idx={x:i for i,x in enumerate(D)};b=face.blocks(r,u,v,w);basis=[]
    def vector(entries):
        ans=[F(0)]*len(D)
        for mask,value in entries:ans[idx[mask]]+=value
        return ans
    if r>=4:
        pivots={(0,1),(0,2),(1,2)}|{(0,i) for i in range(3,r)}
        for i,j in edges:
            if (i,j) in pivots:continue
            entries=[(A[i]|A[j],1),(A[0]|A[1],int(1 not in (i,j))),
                     (A[0]|A[2],int(2 not in (i,j))),(A[1]|A[2],-1)]
            entries += [(A[0]|A[k],-int(k in (i,j))) for k in range(3,r)]
            z=vector(entries)
            require(all(not sum(z[idx[A[i]|A[j]]] for i,j in edges if c in (i,j)) for c in range(r)),'Invalid center-edge kernel basis')
            require(matvec(C,z)==[b['scalars'][3]*x for x in z],'Center-edge kernel image failed');basis.append(z)
    for i in range(u-1):
        x=[int(k==i)-int(k==u-1) for k in range(u)]
        for j in range(v-1):
            y=[int(k==j)-int(k==v-1) for k in range(v)]
            z=vector([((1 << p)|(1 << (u+q)),x[p]*y[q]) for p in range(u) for q in range(v)])
            require(matvec(C,z)==[b['scalars'][2]*a for a in z],'Double-grid image failed');basis.append(z)
    for q,side,offset,size in ((v,'left',0,u),(u,'right',u,v)):
        for k in range(size-1):
            x=[int(j==k)-int(j==size-1) for j in range(size)]
            spoke=vector([(a|(1 << (offset+j)),x[j]) for a in A for j in range(size)])
            single=vector([(1 << (offset+j),x[j]) for j in range(size)])
            edge=vector([((1 << i)|(1 << (u+j)),x[i] if side=='left' else x[j]) for i in range(u) for j in range(v)])
            image_block(C,[spoke,single,edge],b[side],[F(r),F(1),F(q)]);basis += [spoke,single,edge]
            for c in range(r-1):
                y=[int(t==c)-int(t==r-1) for t in range(r)]
                z=vector([(a|(1 << (offset+j)),y[t]*x[j]) for t,a in enumerate(A) for j in range(size)])
                scalar=b['scalars'][0 if side=='left' else 1]
                require(matvec(C,z)==[scalar*a for a in z],'Center-times-leaf image failed');basis.append(z)
    for c in range(r-1):
        x=[int(t==c)-int(t==r-1) for t in range(r)]
        standard=[vector([(a,x[t]) for t,a in enumerate(A)]),vector([(A[i]|A[j],x[i]+x[j]) for i,j in edges])]
        standard += [vector([(a|(1 << j),x[t]) for t,a in enumerate(A) for j in ranges]) for ranges in (range(u),range(u,h))]
        image_block(C,standard,b['center'],b['center_norms']);basis+=standard
    const=[vector([(a,1) for a in A]),vector([(A[i]|A[j],1) for i,j in edges])]
    const += [vector([(a|(1 << j),1) for a in A for j in ranges]) for ranges in (range(u),range(u,h))]
    const += [vector([(1 << j,1) for j in ranges]) for ranges in (range(u),range(u,h))]
    const += [vector([((1 << i)|(1 << (u+j)),1) for i in range(u) for j in range(v)])]
    image_block(C,const,b['constant'],b['constant_norms']);basis+=const
    require(len(basis)==len(D) and basis_rank(basis)==len(D),'Incomplete module basis')
    return dict(complete_basis_rank=len(D),center_standard_copies=r-1,center_edge_kernel=r*(r-3)//2,
                left_standard_copies=u-1,right_standard_copies=v-1,constant_norms=list(map(str,b['constant_norms'])))


def fixture_check(fixture):
    summary,expected=poly.verify_certificate()
    require(fixture==expected,'Coefficient or rational LDL certificate differs')
    return summary


def affine_face_checks():
    cases=[]
    for r,u,v in ((3,2,2),(3,2,3),(3,3,4),(4,2,2),(5,2,3)):
        w=face.centered_face(r,u,v,jL=F(1,7),jR=F(-2,9),eta=F(3,11) if r>=4 else 0,
            kL=F(1,3),kR=F(-2,5),kT=F(7,11),aL=F(-3,7),aR=F(2,13),tL=F(-4,9),tR=F(3,8),
            bL=F(1,17),bR=F(-2,19),bT=F(5,23),qL=F(-7,29),qR=F(11,31))
        C=face.core(r,u,v,w);invariants(r,u,v,C)
        cases.append(dict(r=r,u=u,v=v,free_orbits=14 if r==3 else 15,
            centered=True,center_star_kernels=r,complete_images=literal_images(r,u,v,w,C),PSD_claim=False,cap_claim=False))
    return cases


def failed_boundary_recipe():
    # The u=2,v>=3 formula cannot simply be used at v=2.
    u=v=2;D=cone.family(u,v);h=u+v
    w=face.centered_face(3,u,v,jR=F(1,2),kL=F(3,2),kR=F(3,2),tR=F(3,4),bR=-1,qR=-1)
    C=face.core(3,u,v,w);invariants(3,u,v,C);centers=7 << h;z=[]
    for x in D[1:]:
        y=int(bool(x & 4))-int(bool(x & 8))
        z.append(F(97,44)*y if x & centers else F(10,11)*y if x.bit_count()==1 else F(y))
    quadratic=sum(a*b for a,b in zip(z,matvec(C,z)))
    require(quadratic==F(-1357,44),'Failed boundary quadratic differs')
    try:psd_ldl(C)
    except ValueError:pass
    else:raise RuntimeError('Indefinite boundary formula accepted')
    return dict(u=u,v=v,right_block_coordinates=['97/44','10/11','1'],full_negative_quadratic=str(quadratic),
        status='Obstruction to unmodified recipe at the boundary; no H nonexistence claim')


def recoloring_control():
    u,v=2,3;s=u+v+3;D=cone.family(u,v)
    balanced=base.equitable_colors(s,D,cone.colors(u,v),s)
    require([balanced.count(c) for c in range(s)]==[4]*s,'Balanced control differs')
    colors=make_nonconstant(D[1:],balanced,s);counts,functional=partition_check(D,colors,s)
    require(functional==2*s,'Recoloring did not remove the total kernel')
    for c in range(u+v,u+v+3):
        require(all(a==b for x,a,b in zip(D[1:],balanced,colors) if x & (1 << c)),'Center-star color changed')
    return dict(u=u,v=v,before_sizes=[4]*s,after_sizes=counts,partition_functional=functional)


def published_baselines():
    prior=json.loads(Path(__file__).with_name('two_center_bipartite_expected.json').read_text());rows=[]
    for u,v in ((2,2),(2,3)):
        D,M,s=old_cone.certificate(u,v);N=len(D)
        require(check(D,M,s,upper=True)==N-2,'Published two-center baseline failed')
        record=next(x for x in prior['cases'] if (x['u'],x['v'])==(u,v))
        require(fingerprint(M)==record['matrix_sha256'],'Published two-center fingerprint differs')
        rows.append(dict(u=u,v=v,N=N,s=s,L_rank=N-2,matrix_sha256=fingerprint(M)))
    return rows


def run():
    fixture=json.loads(Path(__file__).with_name('three_center_bipartite_determinants.json').read_text())
    symbolic=fixture_check(fixture);corruptions=0
    for mode in range(3):
        bad=copy.deepcopy(fixture)
        if mode==0:bad['regimes']['u_ge_3']['constant_active'][-1][0][-1]+=1
        elif mode==1:bad['regimes']['u2_v_ge_3']['right'][2].pop()
        else:bad['boundary_cores'][0]['pivots']['left'][0]='-1'
        try:fixture_check(bad)
        except ValueError:corruptions+=1
        else:raise RuntimeError('Corrupt coefficient or LDL fixture accepted')
    inputs=[(2,2),(2,3),(2,11),(2,12),(3,3),(3,7),(3,8),(4,4),(4,5),(4,6),(5,5),(6,6)]
    cases=[]
    for u,v in inputs:
        D,M0,s=cone.centered_certificate(u,v);N=len(D);C=cone.core(u,v);w=cone.parameters(u,v)
        invariants(3,u,v,C);images=literal_images(3,u,v,w,C)
        require(check(D,M0,s)==N-4,'Centered literal H/rank failed')
        require(base.extract_core(M0,s)==C,'Core extraction failed');core_buffer(C,N,F(1))
        b=face.blocks(3,u,v,w);trace=sum(b['constant'][i][i]/norm for i,norm in enumerate(b['constant_norms']))
        if (u,v)!=(2,2):
            require(trace==5*(u+v)+16+F(u+2,v)+F(9,2*u)-(3 if u==2 else 0),'Constant trace formula differs')
        colors=cone.colors(u,v);counts,functional=partition_check(D,colors,s)
        require(functional>0,'Partition leaves total kernel')
        for c in range(u+v,u+v+3):
            require(sorted(color for mask,color in zip(D[1:],colors) if mask & (1 << c))==list(range(s)),
                    'Center star does not meet each color once')
        patched,epsilon=repair.repaired_core(C,colors,s);D2,M,s2=cone.certificate(u,v)
        require(D2==D and s2==s and M==base.lift(patched,s),'Production repair/lift differs')
        require(check(D,M,s)==N-3,'Repaired literal H/maximal rank failed')
        require(psd_ldl([[F(i==j)-M[i][j] for j in range(N)] for i in range(N)])==N-1,'Upper endpoint is not simple')
        core_buffer(patched,N,F(1,2))
        maxima=maximum_intersecting_families(D)
        require(maxima==maximum_stars(D,s) and len(maxima)==3,'Base maximum families differ')
        cases.append(dict(u=u,v=v,N=N,s=s,centered_L_rank=N-4,repaired_L_rank=N-3,images=images,
            normalized_constant_trace=str(trace),partition_sizes=counts,partition_functional=functional,
            epsilon=str(epsilon),maximum_families=3,matrix_sha256=fingerprint(M)))
    # A small literal tensor. The new factor strictly dominates density1/4.
    rankone_D=[0,1 << 20,1 << 21,1 << 22]
    rankone_M=[[F(i!=j,3) for j in range(4)] for i in range(4)]
    D,M,s=base.product_certificate([cone.certificate(2,2),(rankone_D,rankone_M,1)]);N=len(D)
    require((N,s)==(108,28) and check(D,M,s)==N-3,'Literal tensor H/rank failed')
    require(psd_ldl([[F(i==j)-M[i][j] for j in range(N)] for i in range(N)])==N-1,'Literal tensor upper endpoint differs')
    require(len(maximum_stars(D,s))==3,'Tensor eligible-star count differs')
    products=[dict(N=N,s=s,L_rank=N-3,eligible_stars=3,matrix_sha256=fingerprint(M))]
    require(cone.certificate(2,3,10)[1]==cone.certificate(2,3)[1],'Shift changed the matrix')
    rejections=0
    for args in ((True,2),(1,2),(2,1),(2,True),(2,2.0),(-2,2),(2,3,True),(2,3,-1)):
        try:cone.certificate(*args)
        except ValueError:rejections+=1
        else:raise RuntimeError('Invalid family parameters accepted')
    for r,u,v,kw in ((True,2,3,{}),(2,2,3,{}),(3,True,3,{}),(3,2,3,{'eta':1}),
                      (3,2,3,{'jR':True}),(3,2,3,{'bL':0.5})):
        try:face.centered_face(r,u,v,**kw)
        except ValueError:rejections+=1
        else:raise RuntimeError('Invalid affine coordinates accepted')
    for weights in ({},dict(cone.parameters(2,3),bL=0.5),dict(cone.parameters(2,3),z=0)):
        try:cone.core(2,3,weights)
        except ValueError:rejections+=1
        else:raise RuntimeError('Invalid custom weights accepted')
    rejection_controls()
    return dict(agent='six-downset-1',role='researcher',symbolic_certificate=symbolic,cases=cases,
        base_N_max=max(x['N'] for x in cases),products=products,general_affine_face=affine_face_checks(),
        failed_boundary_recipe=failed_boundary_recipe(),recoloring_control=recoloring_control(),
        published_baselines=published_baselines(),malformed_inputs_rejected=rejections,
        corrupted_fixtures_rejected=corruptions,PSD_rejection_controls=3)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=run()
    if args.check:
        expected=json.loads(Path(__file__).with_name('three_center_bipartite_expected.json').read_text())
        require(result==expected,'Expected output differs')
    print(json.dumps(result,sort_keys=True,indent=2))
