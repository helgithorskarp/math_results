#!/usr/bin/env python3
"""Exact literal matrices, complete grid images and coefficient certificates."""
import argparse,copy,json
from fractions import Fraction as F
from pathlib import Path
import bipartite_cones as cone
import bipartite_cone_polynomials as poly
import certificates as base
import regular_cones as regular
from maxrank_mixtures import repaired_core
from verify import check,psd_ldl,require,rejection_controls
from verify_clique_centers import matvec,image_block,basis_rank,core_buffer
from verify_clique_centers import partition_check,maximum_stars,fingerprint
from verify_two_centers import maximum_intersecting_families
from verify_dense_regular_cones import bipartite


def literal_grid_images(u,v,C):
    h=u+v;members=cone.family(u,v)[1:];index={x:i for i,x in enumerate(members)};a=1 << h
    w=cone.parameters(u,v);L,R,K,G,norms=poly.numeric_blocks(u,v);basis=[]
    def vector(entries):
        z=[F(0)]*len(members)
        for mask,value in entries:z[index[mask]]+=value
        return z
    for i in range(u-1):
        x=[int(k==i)-int(k==u-1) for k in range(u)]
        for j in range(v-1):
            y=[int(k==j)-int(k==v-1) for k in range(v)]
            z=vector([((1 << p)|(1 << (u+q)),x[p]*y[q]) for p in range(u) for q in range(v)])
            require(matvec(C,z)==[(h+2+w['z'])*b for b in z],'Double-centered grid scalar image failed')
            basis.append(z)
    for i in range(u-1):
        x=[int(k==i)-int(k==u-1) for k in range(u)]
        directions=[vector([(a|(1 << k),x[k]) for k in range(u)]),
                    vector([(1 << k,x[k]) for k in range(u)]),
                    vector([((1 << k)|(1 << (u+j)),x[k]) for k in range(u) for j in range(v)])]
        image_block(C,directions,L,[F(1),F(1),F(v)])
        require(sum(directions[2][index[(1 << k)|(1 << (u+j))]]**2 for k in range(u) for j in range(v))==v*sum(t*t for t in x),
                'Left incidence norm failed')
        basis+=directions
    for j in range(v-1):
        y=[int(k==j)-int(k==v-1) for k in range(v)]
        directions=[vector([(a|(1 << (u+k)),y[k]) for k in range(v)]),
                    vector([(1 << (u+k),y[k]) for k in range(v)]),
                    vector([((1 << i)|(1 << (u+k)),y[k]) for i in range(u) for k in range(v)])]
        image_block(C,directions,R,[F(1),F(1),F(u)])
        require(sum(directions[2][index[(1 << i)|(1 << (u+k))]]**2 for i in range(u) for k in range(v))==u*sum(t*t for t in y),
                'Right incidence norm failed')
        basis+=directions
    constants=[vector([(a,1)]),vector([(a|(1 << i),1) for i in range(u)]),
               vector([(a|(1 << (u+j)),1) for j in range(v)]),
               vector([(1 << i,1) for i in range(u)]),vector([(1 << (u+j),1) for j in range(v)]),
               vector([((1 << i)|(1 << (u+j)),1) for i in range(u) for j in range(v)])]
    image_block(C,constants,G,norms)
    require(psd_ldl(K)==4,'Active constant Gram not PD')
    require(sum(G[i][i]/norms[i] for i in range(6))==
            4*u+3*v+5-F(v*(u-1),u*u)+F(u,v)+F(2*u-1,u*u),'Normalized constant trace failed')
    for z in basis:
        require(all(not sum(x*y for x,y in zip(z,c)) for c in constants),'Nonconstant direction not orthogonal to constants')
    basis+=constants
    require(len(basis)==len(members) and basis_rank(basis)==len(members),'Grid spanning basis incomplete')
    return dict(double_centered_dimension=(u-1)*(v-1),left_blocks=u-1,right_blocks=v-1,
                constant_dimension=6,constant_active_rank=4,complete_basis_rank=len(members),
                normalized_constant_trace=str(sum(G[i][i]/norms[i] for i in range(6))))


def fixture_check(fixture):
    summary,expected=poly.verify_certificate()
    require(fixture==expected,'Coefficient or small-constant certificate changed')
    return summary


def seven_parameter_face_checks():
    records=[]
    for u,v in ((2,3),(3,4)):
        # Arbitrary rational face points; no PSD assertion.
        w=cone.centered_face(u,v,aL=F(1,3),aR=F(-2,5),tL=F(7,11),tR=F(-3,7),
                             bL=F(2,13),bR=F(-4,9),bT=F(3,8))
        C=cone.core(u,v,w);D=cone.family(u,v)[1:];a=1 << (u+v)
        require(all(sum(row)==0 for row in C),'Affine-face centering failed')
        require(not any(matvec(C,[F(bool(x & a)) for x in D])),'Affine-face star equation failed')
        records.append(dict(u=u,v=v,centered=True,star_kernel=True,PSD_claim=False))
    return records


def failed_imbalanced_face():
    u,v=2,20;h=u+v;a=1 << h
    w=cone.centered_face(u,v,tL=F(2,v),tR=F(2,u),bT=-1)
    C=cone.core(u,v,w);D=cone.family(u,v)[1:]
    z=[F(1 if x & 1 else -1) if x.bit_count()==2 and not x & a else F(0) for x in D]
    image=matvec(C,z);scalar=F(-41,10)
    require(all(b==scalar*x for mask,x,b in zip(D,z,image) if mask.bit_count()==2 and not mask & a),
            'Failed ansatz edge compression changed')
    quadratic=sum(x*y for x,y in zip(z,image))
    require(quadratic==F(-164),'Failed ansatz negative quadratic changed')
    try:psd_ldl(C)
    except ValueError:pass
    else:raise RuntimeError('Non-PSD face accepted')
    return dict(u=u,v=v,edge_compression_scalar=str(scalar),negative_quadratic=str(quadratic),
                status='Old centered face fails PSD; no mathematical nonexistence inference')


def recoloring_control():
    u,v=3,9;s=u+v+1;D=cone.family(u,v)
    equitable=base.equitable_colors(s,D,cone.colors(u,v),s)
    require([equitable.count(c) for c in range(s)]==[4]*s,'Equitable input control failed')
    colors=cone.make_nonconstant(D[1:],equitable,s)
    counts,functional=partition_check(D,colors,s)
    a=1 << (u+v)
    require(functional>0 and any(x!=4 for x in counts),'Singleton recoloring failed')
    require(all(x==y for mask,x,y in zip(D[1:],equitable,colors) if mask & a),'Center-star colors changed')
    return dict(u=u,v=v,before_sizes=[4]*s,after_sizes=counts,partition_functional=functional)


def run():
    fixture=json.loads(Path(__file__).with_name('bipartite_cone_determinants.json').read_text())
    symbolic=fixture_check(fixture);corruptions=0
    for mode in range(3):
        corrupt=copy.deepcopy(fixture)
        if mode==0:corrupt['constant_active'][-1][0][-1]+=1
        elif mode==1:corrupt['right'][2].pop()
        else:corrupt['small_constant_buffers'][0]['pivots'][0]='-1'
        try:fixture_check(corrupt)
        except ValueError:corruptions+=1
        else:raise RuntimeError('Corrupt coefficient/small-buffer fixture accepted')
    inputs=[(2,v) for v in range(2,8)]+[(3,v) for v in range(3,6)]+[(4,4)]
    inputs += [(2,8),(2,20),(3,6),(3,9),(3,10),(4,5),(5,5)]
    cases=[]
    for u,v in inputs:
        D,M0,s=cone.centered_certificate(u,v);N=len(D);C=cone.core(u,v);a=1 << (u+v)
        require(all(sum(row)==0 for row in C),'Literal centering failed')
        require(not any(matvec(C,[F(bool(x & a)) for x in D[1:]])),'Center-star kernel failed')
        require(check(D,M0,s,upper=True)==N-2,'Centered H/rank failed')
        require(base.extract_core(M0,s)==C,'Centered extraction failed')
        core_buffer(C,N,F(1));images=literal_grid_images(u,v,C)
        colors=cone.colors(u,v);counts,functional=partition_check(D,colors,s)
        require(functional>0,'Partition did not remove total kernel')
        patched,epsilon=repaired_core(C,colors,s)
        D2,M,s2=cone.certificate(u,v)
        require(D==D2 and s==s2 and M==base.lift(patched,s),'Repaired constructor differs')
        require(check(D,M,s,upper=True)==N-1,'Repaired H/maximal rank failed')
        core_buffer(patched,N,F(1,2))
        maxima=maximum_intersecting_families(D)
        require(maxima==maximum_stars(D,s) and len(maxima)==1,'Unique center extremizer failed')
        minimum=min(M[i][j] for i in range(N) for j in range(N) if i!=j)
        if v<=u*u:require(minimum>=0,'Moderate-imbalance nonnegative signs failed')
        cases.append(dict(u=u,v=v,N=N,s=s,centered_L_rank=N-2,repaired_L_rank=N-1,
                          grid_images=images,partition_sizes=counts,epsilon=str(epsilon),
                          nonnegative_scope=v<=u*u,minimum_off_diagonal=str(minimum),matrix_sha256=fingerprint(M)))
    strict=cone.certificate(2,3);small=cone.certificate(2,2)
    rankone_D=[0,1 << 20,1 << 21,1 << 22];rankone_M=[[F(int(i!=j),3) for j in range(4)] for i in range(4)]
    products=[]
    for factors,c in (([strict,(rankone_D,rankone_M,1)],1),([small,cone.certificate(2,2,5)],2)):
        D,M,s=base.product_certificate(factors);N=len(D)
        require(check(D,M,s,upper=True)==N-c,'Tensor cap/rank failed')
        require(len(maximum_stars(D,s))==c,'Eligible tensor stars failed')
        products.append(dict(N=N,s=s,L_rank=N-c,eligible_stars=c,matrix_sha256=fingerprint(M)))
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
        else:raise RuntimeError('Inexact face coordinate accepted')
    rejection_controls()
    baselines=[]
    previous=json.loads(Path(__file__).with_name('dense_regular_cones_expected.json').read_text())
    for t in (2,3):
        D,M,s=regular.certificate(2*t,bipartite(t));N=len(D)
        require(D==cone.family(t,t) and check(D,M,s,upper=True)==N-1,'Published balanced baseline failed')
        old=next(x for x in previous['cases'] if x['name']=='K'+str(t)+','+str(t))
        require(fingerprint(M)==old['repaired_matrix_sha256'],'Published balanced fingerprint changed')
        baselines.append(dict(t=t,N=N,s=s,L_rank=N-1,matrix_sha256=fingerprint(M)))
    return dict(agent='six-downset-1',role='researcher',symbolic_certificate=symbolic,cases=cases,
                base_N_max=max(x['N'] for x in cases),products=products,seven_parameter_face=seven_parameter_face_checks(),
                failed_imbalanced_face=failed_imbalanced_face(),recoloring_control=recoloring_control(),
                published_balanced_baselines=baselines,malformed_inputs_rejected=rejected,
                corrupted_fixtures_rejected=corruptions,PSD_rejection_controls=3)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=run()
    if args.check:
        expected=json.loads(Path(__file__).with_name('bipartite_cones_expected.json').read_text())
        require(result==expected,'Expected result differs')
    print(json.dumps(result,sort_keys=True,indent=2))
