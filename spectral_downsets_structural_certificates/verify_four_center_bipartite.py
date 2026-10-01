"""Definition-level literal checks, complete images, and exact certificates."""
import argparse,copy,json,sys
from pathlib import Path
from fractions import Fraction as F
import certificates as base
import clique_bipartite_face as face
import four_center_bipartite as cone
import four_center_bipartite_polynomials as poly
import three_center_bipartite as old_cone
import maxrank_mixtures as repair
from bipartite_cones import make_nonconstant
from verify import require,check,psd_ldl,rejection_controls
from verify_clique_centers import matvec,basis_rank,core_buffer,partition_check,maximum_stars,fingerprint
from verify_three_center_bipartite import invariants,literal_images
from verify_two_centers import maximum_intersecting_families


def fixture_check(fixture):
    summary,expected=poly.verify_certificate()
    require(fixture==expected,'Coefficient or finite LDL certificate differs')
    return summary


def corner_check():
    D,M,s=cone.certificate(2,2);N=len(D)
    expected=[0]+[1 << i for i in range(8)]
    expected += [(1 << i)|(1 << j) for i in range(8) for j in range(i+1,8) if (i,j) not in ((0,1),(2,3))]
    require(D==sorted(expected),'Matching corner labeling differs')
    old,part,colors=cone.matching_corner_data();eps=F(1,128);C=cone.matching_corner_core()
    reference=[[F(7) if a==b else F(-1) if a&b or a.bit_count()==b.bit_count()==1 else F(1,3)
                for b in D[1:]] for a in D[1:]]
    require(old==reference,'Inherited projection corner entries differ')
    require(C==[[(1-eps)*a+eps*b for a,b in zip(row,other)] for row,other in zip(reference,part)],'Corner mixture differs')
    counts,functional=partition_check(D,colors,s)
    for c in range(4,8):
        require(sorted(color for a,color in zip(D[1:],colors) if a & (1 << c))==list(range(s)),'Corner maximum-star partition fails')
    star=lambda k:[F(bool(a & (1 << k))) for a in D[1:]]
    x=[a-b for a,b in zip(star(0),star(1))];y=[a-b for a,b in zip(star(2),star(3))]
    z=[1-a-b for a,b in zip(star(1),star(3))];extra=(x,y,z)
    inherited_basis=[star(k) for k in range(4,8)]+list(extra)
    require(basis_rank(inherited_basis)==7 and all(not any(matvec(old,w)) for w in inherited_basis),'Corner kernel basis differs')
    gram=[[sum(a[i]*part[i][j]*b[j] for i in range(N-1) for j in range(N-1)) for b in extra] for a in extra]
    require(gram==[[16,0,8],[0,16,8],[8,8,16]] and psd_ldl(gram)==3,'Corner repair quotient Gram differs')
    require(psd_ldl(old)==27 and psd_ldl(part)==7 and psd_ldl(C)==30,'Corner core ranks differ')
    require(check(D,M,s)==31,'Corner literal H/maximal rank fails')
    require(psd_ldl([[F(i==j)-M[i][j] for j in range(N)] for i in range(N)])==34,'Corner upper endpoint differs')
    core_buffer(C,N,F(323,672))
    maxima=maximum_intersecting_families(D)
    require(maxima==maximum_stars(D,s) and len(maxima)==4,'Corner equality families differ')
    raw_colors=[]
    for a in D[1:]:
        vertices=[i for i in range(8) if a & (1 << i)]
        raw_colors.append((2*vertices[0] if len(vertices)==1 else sum(vertices))%8)
    unmodified=repair.mix_cores(old,repair.partition_core(raw_colors,s),eps)
    require(psd_ldl(unmodified)==28,'Unrecolored repair obstruction differs')
    return dict(u=2,v=2,N=N,s=s,epsilon=str(eps),inherited_rank=27,partition_rank=7,
                repaired_core_rank=30,L_rank=31,upper_rank=34,cap_buffer='323/672',
                quotient_gram=[[str(a) for a in row] for row in gram],
                partition_sizes=counts,partition_functional=functional,maximum_families=4,
                unrecolored_core_rank=28,matrix_sha256=fingerprint(M))


def recoloring_control():
    u,v=2,5;s=u+v+4;D=cone.family(u,v)
    balanced=base.equitable_colors(s,D,cone.colors(u,v),s)
    require([balanced.count(c) for c in range(s)]==[5]*s,'Balanced control differs')
    colors=make_nonconstant(D[1:],balanced,s);counts,functional=partition_check(D,colors,s)
    require(functional==2*s,'Recoloring did not remove total kernel')
    for c in range(u+v,u+v+4):
        require(all(a==b for x,a,b in zip(D[1:],balanced,colors) if x & (1 << c)),'Center-star color changed')
    return dict(u=u,v=v,before_sizes=[5]*s,after_sizes=counts,partition_functional=functional)


def published_baseline():
    prior=json.loads(Path(__file__).with_name('three_center_bipartite_expected.json').read_text())
    D,M,s=old_cone.certificate(2,2);N=len(D)
    require(check(D,M,s,upper=True)==N-3,'Published three-center baseline fails')
    record=next(x for x in prior['cases'] if (x['u'],x['v'])==(2,2))
    require(fingerprint(M)==record['matrix_sha256'],'Published three-center fingerprint differs')
    return dict(u=2,v=2,N=N,s=s,L_rank=N-3,matrix_sha256=fingerprint(M))


def run():
    fixture=json.loads(Path(__file__).with_name('four_center_bipartite_determinants.json').read_text())
    symbolic=fixture_check(fixture);corruptions=0
    for mode in range(3):
        bad=copy.deepcopy(fixture)
        if mode==0:bad['regimes']['u_ge_4']['constant_active'][-1][0][-1]+=1
        elif mode==1:bad['regimes']['u2_v_ge_21']['right'][2].pop()
        else:bad['boundary_cores'][0]['pivots']['left'][0]='-1'
        try:fixture_check(bad)
        except ValueError:corruptions+=1
        else:raise RuntimeError('Corrupt coefficient or LDL fixture accepted')
    corner=corner_check();print('corner complete',file=sys.stderr)
    cases=[]
    for u,v in ((2,3),(2,4),(2,13),(2,21),(3,3),(3,4),(4,4)):
        D,M0,s=cone.centered_certificate(u,v);N=len(D);C=cone.core(u,v);w=cone.parameters(u,v)
        invariants(4,u,v,C);images=literal_images(4,u,v,w,C)
        require(check(D,M0,s)==N-5,'Centered literal H/rank fails')
        require(base.extract_core(M0,s)==C,'Core extraction differs');core_buffer(C,N,F(1))
        colors=cone.colors(u,v);counts,functional=partition_check(D,colors,s)
        require(functional>0,'Partition keeps total kernel')
        for c in range(u+v,u+v+4):
            require(sorted(color for a,color in zip(D[1:],colors) if a & (1 << c))==list(range(s)),'Maximum star fails partition')
        patched,eps=repair.repaired_core(C,colors,s);D2,M,s2=cone.certificate(u,v)
        require(D2==D and s2==s and M==base.lift(patched,s),'Production repair/lift differs')
        require(check(D,M,s)==N-4,'Repaired literal H/maximal rank fails')
        require(psd_ldl([[F(i==j)-M[i][j] for j in range(N)] for i in range(N)])==N-1,'Upper endpoint not simple')
        core_buffer(patched,N,F(1,2))
        census=None
        if N<=80:
            maxima=maximum_intersecting_families(D)
            require(maxima==maximum_stars(D,s) and len(maxima)==4,'Base maximum families differ');census=4
        cases.append(dict(u=u,v=v,N=N,s=s,centered_L_rank=N-5,repaired_L_rank=N-4,
            images=images,partition_sizes=counts,partition_functional=functional,epsilon=str(eps),
            literal_maximum_family_census=census,matrix_sha256=fingerprint(M)))
        print('literal complete '+str((u,v,N)),file=sys.stderr)
    # This rank-one factor strictly dominates the new factor's star fraction.
    rankone_D=[0,1 << 20,1 << 21]
    rankone_M=[[F(i!=j,2) for j in range(3)] for i in range(3)]
    D,M,s=base.product_certificate([cone.certificate(2,2),(rankone_D,rankone_M,1)]);N=len(D)
    require((N,s)==(105,35) and check(D,M,s)==N-2,'Literal tensor H/rank fails')
    require(psd_ldl([[F(i==j)-M[i][j] for j in range(N)] for i in range(N)])==N-1,'Tensor upper endpoint differs')
    require(len(maximum_stars(D,s))==2,'Tensor eligible-star count differs')
    products=[dict(N=N,s=s,L_rank=N-2,eligible_stars=2,matrix_sha256=fingerprint(M))]
    require(cone.certificate(2,3,10)[1]==cone.certificate(2,3)[1],'Shift changes matrix')
    require(cone.certificate(2,2,10)[1]==cone.certificate(2,2)[1],'Corner shift changes matrix')
    rejections=0
    for args in ((True,2),(1,2),(2,1),(2,True),(2,2.0),(-2,2),(2,3,True),(2,3,-1)):
        try:cone.certificate(*args)
        except ValueError:rejections+=1
        else:raise RuntimeError('Invalid family parameter accepted')
    for weights in ({},dict(cone.parameters(2,3),bL=0.5),dict(cone.parameters(2,3),z=0)):
        try:cone.core(2,3,weights)
        except ValueError:rejections+=1
        else:raise RuntimeError('Malformed affine weights accepted')
    try:cone.centered_certificate(2,2)
    except ValueError:rejections+=1
    else:raise RuntimeError('Undeclared centered matching recipe accepted')
    rejection_controls()
    generic=face.centered_face(4,2,3,jL=F(1,7),jR=F(-2,9),eta=F(3,11),kT=F(2,5),bT=F(-4,7))
    C=face.core(4,2,3,generic);invariants(4,2,3,C)
    arbitrary=dict(r=4,u=2,v=3,complete_images=literal_images(4,2,3,generic,C),PSD_claim=False,cap_claim=False)
    # Negative control: the tail seed does not cover the isolated (3,3) point.
    bad=face.centered_face(4,3,3,eta=F(-3,2),jR=F(3,4),kL=1,kR=F(1,4),tR=F(1,2),bR=F(-1,4),qR=F(-3,2))
    try:psd_ldl(face.blocks(4,3,3,bad)['constant_active'])
    except ValueError:pass
    else:raise RuntimeError('Indefinite tail boundary control accepted')
    return dict(agent='six-downset-1',role='researcher',symbolic_certificate=symbolic,corner=corner,cases=cases,
        base_N_max=max(a['N'] for a in cases),products=products,general_affine_face=arbitrary,
        recoloring_control=recoloring_control(),published_baseline=published_baseline(),
        malformed_inputs_rejected=rejections,corrupted_fixtures_rejected=corruptions,
        PSD_rejection_controls=3,failed_tail_boundary=dict(u=3,v=3,block='constant_active',scope='This recipe only, not H nonexistence'))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=run()
    if args.check:
        expected=json.loads(Path(__file__).with_name('four_center_bipartite_expected.json').read_text())
        require(result==expected,'Expected output differs')
    print(json.dumps(result,sort_keys=True,indent=2))
