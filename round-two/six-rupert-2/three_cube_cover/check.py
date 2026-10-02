#!/usr/bin/env python3
"""Exact J74 three-frame source-cover audit; ordinary proof in PROOF.md.

This is a configuration reduction, not a global Rupert decision. Every
geometric/symbolic check uses explicit exceptions, also under python -O.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,sys
from itertools import product
from poly import Poly,dot,cross,qmul,conj,rotation_homogeneous,mm,transpose,act,scaled,det,identity
HERE=Path(__file__).resolve().parent
DEPENDENCIES=json.loads((HERE/'DEPENDENCIES.json').read_text())
for relative,pin in DEPENDENCIES['sha256'].items():
    if hashlib.sha256((HERE/relative).read_bytes()).hexdigest()!=pin:
        raise ValueError('before-import exact named prerequisite changed: '+relative)
sys.path.insert(0,str(HERE.parent))
import model,q5
if Path(model.__file__).resolve()!=HERE.parent/'model.py' or Path(q5.__file__).resolve()!=HERE.parent/'q5.py':
    raise ValueError('wrong arithmetic/named-model source imported')
Q=q5.Q;V=tuple(model.VERTICES);I=identity();H=((-1,0,0),(0,-1,0),(0,0,1));MX=((-1,0,0),(0,1,0),(0,0,1))
L=F(7,4)
# Every frame is a fixed proper signed permutation, not assumed a body symmetry.
FRAMES=[('x',((0,0,1),(0,1,0),(-1,0,0)),(1,0,1,0),0),
        ('y',((1,0,0),(0,0,1),(0,-1,0)),(1,-1,0,0),1),
        ('z',I,(1,0,0,0),2)]
def require(ok,label):
    if not ok:raise ValueError(label)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def abs_exact(x):return -x if x<0 else x
def enc(x):
    x=Q(x);return [str(x.a),str(x.b)]
def matrix_rotation(q):
    q=tuple(F(x) if type(x) is int else x for x in q)
    return scaled(rotation_homogeneous(q),1/dot(q,q))
def projection(a):
    r2=dot(a,a)
    return tuple(tuple(I[i][j]-a[i]*a[j]/r2 for j in range(3)) for i in range(3))
def projected_vertices(a,R):
    combined=mm(projection(a),R)
    return {act(combined,v) for v in V}
def permutation(A):
    images=[act(A,v) for v in V]
    require(set(images)==set(V),'claimed FULL original body symmetry')
    return [V.index(p) for p in images]
def proper(A):require(mm(A,transpose(A))==I and det(A)==1,'actual proper frame/body rotation')
def validate_frames(frames=FRAMES):
    require(len(frames)==3 and {x[3] for x in frames}=={0,1,2},'all three receiving coordinate faces required')
    for name,S,p,axis in frames:
        proper(S);require(act(S,(0,0,1))==tuple(int(i==axis) for i in range(3)),'literal receiving face normal')
        require(matrix_rotation(p)==S,'fixed proper frame quaternion lift')
def audit_actions(right=1):
    variables=[Poly.variable(i) for i in range(7)];r=tuple(variables[:3]);q=tuple(variables[3:]);r2=dot(r,r);nq=dot(q,q)
    pr=(0,*r);px=tuple(int(i==right) for i in range(4));pz=(0,0,0,1)
    D=lambda x:qmul(x,pz)
    C=lambda x:qmul(qmul(pr,x),px)
    rows=[]
    def verify(label,a,b):
        aa=list(a) if isinstance(a,(tuple,list)) else [a];bb=list(b) if isinstance(b,(tuple,list)) else [b]
        require(len(aa)==len(bb) and all(x==y for x,y in zip(aa,bb)),label)
        coeffs=[[x.coefficients(),y.coefficients()] for x,y in zip(aa,bb)]
        rows.append({'identity':label,'scalar_equalities':len(aa),'full_coefficient_pair_sha256':digest(coeffs)})
    def flat(A):return tuple(x for row in A for x in row)
    rx,ry,rz=r;h,x,y,z=q
    verify('Hamilton right halfturn literal components',D(q),(-z,y,-x,h))
    verify('Hamilton receiver/body reflection literal components',C(q),(-rx*h-ry*z+rz*y,-rx*x-ry*y-rz*z,rz*h-ry*x+rx*y,-ry*h-rz*x+rx*z))
    verify('D squared equals negative identity',D(D(q)),tuple(-x for x in q))
    verify('raw C squared equals r squared times identity',C(C(q)),tuple(r2*x for x in q))
    verify('raw C D anticommutes with D C',C(D(q)),tuple(-x for x in D(C(q))))
    verify('D preserves quaternion norm',dot(D(q),D(q)),nq)
    verify('raw C norm has exact r squared factor',dot(C(q),C(q)),r2*nq)
    verify('fourth scalar probe',C(D(q))[0],-ry*h+rx*z-rz*x)
    R=rotation_homogeneous(q);RC=rotation_homogeneous(C(q));RD=rotation_homogeneous(D(q))
    P=tuple(tuple(r2*I[i][j]-r[i]*r[j] for j in range(3)) for i in range(3))
    reflection_numerator=tuple(tuple(r2*I[i][j]-2*r[i]*r[j] for j in range(3)) for i in range(3))
    verify('proper quaternion full orthogonality',flat(mm(transpose(R),R)),flat(scaled(I,nq*nq)))
    verify('proper quaternion determinant',det(R),nq*nq*nq)
    verify('right body halfturn rotation matrix',flat(RD),flat(mm(R,H)))
    verify('full raw reflection rotation matrix',flat(RC),flat(mm(mm(reflection_numerator,R),MX)))
    verify('entire projected source matrix preserved after right Mx',flat(mm(P,RC)),flat(scaled(mm(mm(P,R),MX),r2)))
    # Independent finite evaluations test the polynomial arithmetic/encoding.
    sample_count=0
    for rr,qq in [((1,2,-1),(1,2,3,4)),((0,0,1),(0,1,0,0)),((1,1,1),(1,0,1,0)),((-1,0,1),(1,1,1,1))]:
        values=tuple(map(F,rr+qq));actual=[[p.evaluate(values) for p in row] for row in RC]
        numeric=rotation_homogeneous(qmul(qmul((0,*rr),qq),(0,1,0,0)))
        require(actual==[list(row) for row in numeric],'direct numeric Hamilton versus expanded polynomial')
        sample_count+=9
    return rows,sample_count
def audit_gauge():
    x,y,u,v,w=[Poly.variable(i,n=5) for i in range(5)];r=(x,y,Poly(1,n=5));q=(Poly(1,n=5),L*v-y+x*w,x+y*w-L*u,w);pr=(0,*r)
    cr=qmul(qmul(pr,q),(0,1,0,0));cd=qmul(qmul(pr,qmul(q,(0,0,0,1))),(0,1,0,0))
    require(cr[0]==-L*u and cd[0]==-L*v,'actual adapted scalar coordinates')
    require(qmul(q,(0,0,0,1))[0]==-w,'adapted closed source halfturn coordinate')
    require(x+y*w-q[2]==L*u and y-x*w+q[1]==L*v,'exact affine parameter inverse')
    require(L>0 and L*L-3==F(1,16),'whole receiver face radial bound')
    degrees=[z.bidegree({0,1}) for row in rotation_homogeneous(q) for z in row]
    require(all(a<=2 and b<=2 for a,b in degrees),'source homogeneous rotation bidegree(2,2)')
    generic_quartic=x*x*dot(q,q)
    require(generic_quartic.bidegree({0,1})==[4,2],'generic transformed joint cut needs receiver degree4')
    # The vector q is affine in each variable separately. Its squared norm
    # is separately convex; the ordinary proof reduces its maximum to32 corners.
    corner_norms=[]
    for xx,yy,uu,vv,ww in product((-1,1),repeat=5):
        qq=(F(1),L*vv-yy+xx*ww,xx+yy*ww-L*uu,F(ww))
        corner_norms.append(dot(qq,qq))
    require(max(corner_norms)==F(153,8),'entire closed cube sharp quaternion norm bound')
    t=Poly.variable(0,n=1);qc=(t+1,Poly(0,n=1),Poly(-1,n=1),Poly(1,n=1));factor=t*t-3
    rc=qmul(qmul((0,1,1,1),qc),(0,1,0,0))
    require(tuple(a+t*b for a,b in zip(rc,qc))==(factor,Poly(0,n=1),Poly(0,n=1),Poly(0,n=1)),'sharp radial counterexample reflection identity modulo t squared minus3')
    RR=rotation_homogeneous(qc);nn=dot(qc,qc)
    require(tuple(t*RR[i][0]-nn for i in range(3))==(factor*(t+1),factor,factor),'explicit source x axis aligns with triple-tie receiver')
    coeffs=[z.coefficients() for z in q]+[cr[0].coefficients(),cd[0].coefficients(),generic_quartic.coefficients()]
    return {'sharp_whole_source_cube_squared_quaternion_norm':'153/8','source_scalar_squared_lower_bound':'8/153','all32_corner_norms':[str(x) for x in corner_norms],'sharp_orbit_radial_parameter_lower_bound':'sqrt3','counterexample_quaternion':'(sqrt3+1,0,-1,1)','radial_counterexample_polynomial_scalar_identities':7,'adapted_scalar_identities':3,'affine_inverse_identities':2,'radial_squared_margin':'1/16','canonical_adapted_polynomial_sha256':digest(coeffs),'homogeneous_source_rotation_bidegrees':degrees,'generic_transformed_cut_degree':[4,2]}
def cover_parameters(a,q,frames=FRAMES,strict_receiver=False,strict_source=False):
    require(dot(a,a)>0 and dot(q,q)>0,'nonzero original receiving vector/source quaternion')
    name,S,p,axis=next(t for t in frames if abs_exact(a[t[3]])==max(abs_exact(v) for v in a))
    ar=act(transpose(S),a);r=tuple(v/ar[2] for v in ar)
    bound=max(abs_exact(r[0]),abs_exact(r[1]))
    require(bound<1 if strict_receiver else bound<=1,'all closed receiving face boundaries')
    rel=qmul(conj(p),q);pr=(0,*r);r2=dot(r,r)
    raw=[rel,qmul(rel,(0,0,0,1)),qmul(qmul(pr,rel),(0,1,0,0)),qmul(qmul(pr,qmul(rel,(0,0,0,1))),(0,1,0,0))]
    scores=[z[0]*z[0]/d for z,d in zip(raw,(1,1,r2,r2))]
    index=max(range(4),key=lambda i:scores[i]);selected=raw[index]
    if selected[0]<0:selected=tuple(-z for z in selected)
    require(selected[0]>0,'finite representative INCLUDING original source halfturns')
    c=tuple(z/selected[0] for z in selected[1:]);cx,cy,w=c;x,y,_=r
    u=(x+y*w-cy)/L;v=(y-x*w+cx)/L
    require(max(abs_exact(u),abs_exact(v))<1,'whole closed cube radial slack')
    require(abs_exact(w)<1 if strict_source else abs_exact(w)<=1,'all closed source boundaries')
    require(L*L*u*u<=r2 and L*L*v*v<=r2,'both closed exact source gauge inequalities')
    reconstructed=(1,L*v-y+x*w,x+y*w-L*u,w)
    require(reconstructed==(1,*c),'literal adapted source reconstruction')
    result=mm(S,matrix_rotation(reconstructed));proper(result)
    require(projected_vertices(a,result)==projected_vertices(a,matrix_rotation(q)),'original ENTIRE projected source preserved')
    return {'frame':name,'receiver':[enc(x),enc(y)],'source':[enc(u),enc(v),enc(w)],'selected_action':index,'source_scalar_nonzero':True}
def regional_canonical_branches():
    """Quadratic Bernstein dominance on the ENTIRE prior9531 raw box."""
    from math import comb
    s=Q(0,1);a=(s-1)/4;b=(s+1)/4;c=Q(1)/2
    aa=((b,a,c),(-a,-c,b),(c,-b,-a));bb=((-a,-c,-b),(c,-b,a),(-b,-a,c))
    seeds=[('I',(Q(1),Q(),Q(),Q()),I,3),('A',(c,-b,Q(),-a),aa,0),('B',(a,-c,Q(),b),bb,2)]
    center=((2315-453*s)/1798,(2211+205*s)/1798);eta=Q(F(1,1000));frame=FRAMES[1]
    corners=[(center[0]+i*eta,center[1]+j*eta) for i,j in product((-1,1),repeat=2)]
    for x,y in corners:require(y-x>0 and y+x>0 and y-1>0,'whole9531 box selects receiving y face strictly')
    def power(x,n):
        z=Q(1)
        for _ in range(n):z*=x
        return z
    def square_linear(ax,ay,constant):
        return {(2,0):ax*ax,(0,2):ay*ay,(0,0):constant*constant,(1,1):2*ax*ay,(1,0):2*ax*constant,(0,1):2*ay*constant}
    def bernstein(poly):
        shifted={}
        for (px,py),coef in poly.items():
            for ix in range(px+1):
                for iy in range(py+1):
                    value=coef*comb(px,ix)*comb(py,iy)*power(center[0]-eta,px-ix)*power(center[1]-eta,py-iy)*power(2*eta,ix+iy)
                    shifted[ix,iy]=shifted.get((ix,iy),Q())+value
        return [sum((coef*F(comb(ix,px),comb(2,px))*F(comb(iy,py),comb(2,py)) for (px,py),coef in shifted.items() if px<=ix and py<=iy),Q()) for ix,iy in product(range(3),repeat=2)]
    rows=[];all_controls=[]
    for name,q,R,winner in seeds:
        require(dot(q,q)==1 and matrix_rotation(q)==R,'literal proper seed quaternion is the stated named motion')
        h,x,y,z=qmul(conj(frame[2]),q)
        scores=[{(2,0):h*h,(0,2):h*h,(0,0):h*h},{(2,0):z*z,(0,2):z*z,(0,0):z*z},square_linear(-h,y,-z),square_linear(z,-x,-h)]
        gaps=[]
        for j in range(4):
            if j==winner:continue
            keys=set(scores[winner])|set(scores[j]);gap={k:scores[winner].get(k,Q())-scores[j].get(k,Q()) for k in keys}
            controls=bernstein(gap);require(min(controls)>0,'unique whole-box canonical winning action: '+name)
            # Independent corner and midpoint evaluation checks the bivariate
            # power-to-Bernstein conversion, including its box endpoints.
            for ix,iy in product((0,2),repeat=2):
                px=center[0]+(ix-1)*eta;py=center[1]+(iy-1)*eta
                actual=sum((v*power(px,i)*power(py,k) for (i,k),v in gap.items()),Q())
                require(controls[3*ix+iy]==actual,'regional Bernstein literal corner evaluation')
            actual_mid=sum((v*power(center[0],i)*power(center[1],k) for (i,k),v in gap.items()),Q())
            control_mid=sum((controls[3*i+k]*F(comb(2,i)*comb(2,k),16) for i,k in product(range(3),repeat=2)),Q())
            require(actual_mid==control_mid,'regional Bernstein independent midpoint evaluation')
            all_controls.extend(controls);gaps.append({'losing_action':j,'all9_strict_Bernstein_controls':[enc(v) for v in controls]})
        rows.append({'seed':name,'unique_winning_action':winner,'all_three_score_gaps':gaps})
    require(len(all_controls)==81,'all whole-box scalar-score controls checked')
    return {'scope':'entire prior9531 raw phase-crossing box, both normal orientations and all boundaries','receiving_face':'y','receiving_face_strict_corner_comparisons':12,'positive_quadratic_Bernstein_controls':81,'independent_polynomial_corner_and_midpoint_evaluations':45,'literal_proper_seed_quaternions':3,'unique_canonical_physical_equal_shadow_motions':['M_n H Mx','A','M_n B Mx'],'source_motion_count_is_for_canonical_representatives_only':True,'all12_original_equal_shadows_retained_by_projection_equivalence':True,'minimum_strict_control':enc(min(all_controls)),'complete_winner_records':rows,'record_sha256':digest(rows),'uses_prior9531_only_for_full_closed_fit_classification':True}

def full_record():
    validate_frames();proper(H);require(mm(H,MX)==mm(MX,H),'true body halfturn and reflection commute')
    require(len(V)==60 and len(set(V))==60,'original60 distinct named vertices')
    require(model.cupola_construction()[3]==set(V),'original two cupola replacement identity')
    hp,mp=permutation(H),permutation(MX)
    require({tuple(-x for x in v) for v in V}!=set(V),'no whole body centrality assumption')
    identities,evaluations=audit_actions();gauge=audit_gauge()
    s=Q(0,1)
    receiving=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1),(1,1,1),(-1,1,-1),(2,2,1),(3,0,4),((2315-453*s)/1798,(2211+205*s)/1798,-1),((-183+101*s)/58,(329-109*s)/58,-1)]
    quaternions=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,1,1),(1,0,1,0),(1,2,-1,3),(0,1,1,0)]
    # Convert numeric fixtures to exact Q(sqrt5) before any division.
    results=[cover_parameters(tuple(Q(v) for v in a),tuple(Q(v) for v in q)) for a in receiving for q in quaternions]
    return {'agent':'six-rupert-2','role':'researcher','kind':'exact named geometry/universal polynomial audit of ordinary three-closed-cube reduction','global_J74_Rupert_status':'OPEN','no_Rupert_decision':True,'original_translation_and_scale_preserved':True,'all_closed_receiver_and_source_boundaries_retained':True,'original_halfturns_retained':True,'proper_frame_count':3,'source_cubes_per_receiving_frame':1,'rational_source_parameter':'7/4','full_body_halfturn_permutation':hp,'full_body_x_reflection_permutation':mp,'universal_polynomial_identities':identities,'independent_numeric_polynomial_evaluations':evaluations,'gauge':gauge,'entire_original_source_fixture_count':len(results),'all96_fixture_parameters':results,'whole_fixture_record_sha256':digest(results),'centrality_assumption':False,'partial_shadow_quotient':False,'performance_gain_claimed':False,'regional_canonical_branches':regional_canonical_branches()}
def controls():
    rejected=[]
    def reject(label,call):
        try:call()
        except (ValueError,StopIteration):rejected.append(label);return
        raise ValueError('semantic damage not rejected: '+label)
    reject('missing receiving face',lambda:validate_frames(FRAMES[1:]))
    bad=list(FRAMES);bad[0]=('x',((-1,0,0),(0,1,0),(0,0,1)),(1,0,0,0),0)
    reject('improper receiving frame',lambda:validate_frames(bad))
    reject('wrong right reflection in literal lift',lambda:audit_actions(right=3))
    s=Q(0,1);a=(s-1)/4;b=(s+1)/4;c=Q(1)/2
    partial=((b,a,c),(-a,-c,b),(c,-b,-a))
    reject('partial shadow mistaken for body symmetry',lambda:permutation(partial))
    reject('open receiver faces omit real triple tie',lambda:cover_parameters(tuple(map(Q,(1,1,1))),tuple(map(Q,(1,0,0,0))),strict_receiver=True))
    reject('open source cube omits maximal scalar tie',lambda:cover_parameters(tuple(map(Q,(0,0,1))),tuple(map(Q,(1,0,0,1))),strict_source=True))
    reject('false body centrality',lambda:require({tuple(-x for x in v) for v in V}==set(V),'false centrality'))
    reject('source parameter below the stated radial bound',lambda:require(F(3,2)**2>=3,'radial bound'))
    # Fixed identity frame alone fails at an actual equatorial halfturn.
    r=(1,0,0);q=(0,1,0,0);pr=(0,*r);raw=(q,qmul(q,(0,0,0,1)),qmul(qmul(pr,q),(0,1,0,0)),qmul(qmul(pr,qmul(q,(0,0,0,1))),(0,1,0,0)))
    require(all(x[0]==0 for x in raw),'actual fixed-frame equatorial zero-scalar counterexample')
    return {'semantic_damages_rejected':rejected,'fixed_identity_frame_zero_scalar_counterexample':{'original_receiving_vector':list(r),'original_halfturn_quaternion':list(q)},'distinct_eight_lifts_assumed':False}
def main():
    p=argparse.ArgumentParser();p.add_argument('--emit',action='store_true');args=p.parse_args()
    record={'mathematics':full_record(),'controls':controls()}
    if not args.emit:require(record==json.loads((HERE/'expected.json').read_text()),'whole mathematical/semantic record differs')
    print(json.dumps(record,sort_keys=True,indent=2))
if __name__=='__main__':main()
