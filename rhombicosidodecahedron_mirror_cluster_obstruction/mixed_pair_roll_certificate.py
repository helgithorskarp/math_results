#!/usr/bin/env python3
"""Exact finite hypotheses of MIXED_PAIR_ROLL_PROOF.md; Python3.11+ stdlib.

All original threshold sources into winning receivers with f(n)>=83/200.
The global receiving gap remains1/31; no wider GLOBAL theorem is claimed.
No floating point, solver, private diagnostic or sampled continuum premise.
"""
import argparse,copy,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent

def demand(ok,message):
    if not ok:raise ValueError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def validate_pins(rows):
    demand(len(rows)==56 and len({r['file'] for r in rows})==56,
           'complete distinct56published mathematical inputs')
    for row in rows:
        name=row['file']
        demand(Path(name).name==name and name.endswith(('.py','.json')),
               'ordinary same-directory mathematical input')
        raw=(HERE/name).read_bytes()
        demand(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],
               'published mathematical input byte mismatch: '+name)

INPUT_BYTES=(HERE/'mixed_pair_roll_inputs.json').read_bytes()
INPUTS=json.loads(INPUT_BYTES)
validate_pins(INPUTS['files'])

from verify import PHI,QPhi as Q,ZERO,act,dot,matmul,symmetry_group,vertices
from torque_certificate import cross,determinant,subtract
from cell_certificate import encode
from linear_roll_certificate import project
from contact_collar_certificate import LOW
from threshold_receiver_certificate import BETA,REFS,I
import axial_majorization_certificate as axial

Q0=F(83,200);CANDIDATE=F(2,5);FLAT=F(9,20)
R0SQ=7+8*PHI;RS=R0SQ-BETA;RT=R0SQ-Q(F(1,3))

def neg(v):return tuple(-x for x in v)

def canonical(v):
    first=next(x for x in v if x!=ZERO)
    return v if first>ZERO else neg(v)

def scalar(q=Q0,candidate=CANDIDATE,flat=FLAT):
    demand(q==Q0 and candidate==CANDIDATE and flat==FLAT,
           'fixed new mixed-branch scalar policy')
    cTL,cTU=axial.exact_root('mixed_threshold_height',BETA)
    cWL,cWU=axial.exact_root('mixed_winning_height',Q(F(1,3)))
    rhoTL,rhoTU=axial.exact_root('mixed_threshold_disk',(39+37*PHI)/29)
    rhoWL,rhoWU=axial.exact_root('mixed_winning_disk',Q(F(8,3))+4*PHI)
    st=(cTU-q)/rhoTL;sw=(cWU-q)/rhoWL
    ztL,ztU=axial.exact_root('mixed_threshold_cosine',Q(1-st*st))
    zwL,zwU=axial.exact_root('mixed_winning_cosine',Q(1-sw*sw))
    dT=F(1001,1000)*st;dW=F(1001,1000)*sw
    etaT=cTU*dT+F(9,4)*dT*dT;etaW=cWU*dW+F(9,4)*dW*dW
    height2=BETA+Q(9*etaT)
    hL,hU=axial.exact_root('mixed_actual_radial_candidate_height',height2)
    gates=dict(
        height_square_above_other366_regional_maxima=Q(q*q)>Q(F(1,7)),
        positive_bounded_threshold_and_winning_tangents=0<st<F(1,10) and 0<sw<F(1,10),
        positive_source_circle_radius_after_transport=Q(etaT*etaT)<RS,
        threshold_actual_chord_conversion=F(1001,1000)**2*(1+ztL)>2,
        winning_actual_chord_conversion=F(1001,1000)**2*(1+zwL)>2,
        all_original_radii_below_nine2=R0SQ<Q(F(9,2)**2),
        actual_radial_candidate_distance_below_two5=BETA-Q(q*q)+Q(9*etaT)<Q(candidate*candidate),
        eight_actual_source_candidates_distinct=F(3,2)-2*etaT>2*candidate,
        actual_flat_proper_frame_error_below_nine20=candidate+etaT+etaW<flat,
        positive_required_pair_mean_correlation=(RS+RT-Q(flat*flat))/2>ZERO,
        branch_beta_minus_one28_band_strictly_above_q_squared=BETA-Q(F(1,28))>Q(q*q))
    demand(all(gates.values()),'all11 fresh mixed-branch scalar gates')
    return dict(q=str(q),all11_fresh_scalar_gates=gates,
        threshold_tangent_upper=str(st),winning_tangent_upper=str(sw),
        threshold_source_normal_chord_upper=str(dT),winning_receiver_normal_chord_upper=str(dW),
        source_circle_transport_upper=str(etaT),eligible_winning_original_transport_upper=str(etaW),
        actual_original_candidate_distance_upper=str(candidate),
        actual_flat_error_upper=str(candidate+etaT+etaW),fixed_reference_match_error_upper=str(flat),
        actual_radial_candidate_height_squared_upper=height2.encode(),
        actual_radial_candidate_height_upper=str(hU),
        both_source_threshold_reference_radius_squared=RS.encode(),
        receiving_winning_reference_radius_squared=RT.encode(),
        threshold_four_positive_height_majorization_used=False),dT,dW,etaT,etaW,hU

def circle(n,V):
    N=dot(n,n);originals=sorted(v for v in V if dot(v,n)**2/N==BETA)
    P={project(v,n):v for v in V}
    demand(len(P)==len(V)==60,'all sixty original projections distinct at threshold reference')
    points=sorted(project(v,n) for v in originals)
    demand(len(originals)==len(points)==len(set(points))==8,
           'eight unique original threshold circle preimages')
    demand(all(dot(p,n)==ZERO and dot(p,p)==RS and neg(p) in points for p in points),
           'complete antipodal equal-radius threshold source circle')
    demand(set(points)=={p for p in P if dot(p,p)==RS},'full maximum-radius source circle')
    demand(all(dot(subtract(p,q),subtract(p,q))>Q(F(3,2)**2)
               for p,q in itertools.combinations(points,2)),
           'all28 distinct source-circle pair lengths exceed three2')
    return points,originals

def proper_source_transfer(V,supplied=None):
    a=(2*PHI-1)/5
    R=((Q(-1),ZERO,ZERO),(ZERO,a,-2*a),(ZERO,-2*a,-a))
    if supplied is not None:R=supplied
    demand(matmul(tuple(zip(*R)),R)==I and determinant(*R)==Q(1),
           'proper orthogonal threshold circle transfer')
    L,H=LOW,REFS[1];image=act(R,L);factor=image[1]/H[1]
    demand(L[1]>ZERO and L==tuple(L[1]*x for x in REFS[0]),
           'LOW is the positive directed first threshold reference')
    demand(factor>ZERO and image==tuple(factor*x for x in H),
           'positive directed threshold normal alignment')
    demand(matmul(R,R)==I,'same proper inverse transfer for both ordered threshold classes')
    lo,ol=circle(L,V);hi,oh=circle(H,V)
    demand({act(R,v) for v in ol}==set(oh) and {act(R,p) for p in lo}==set(hi),
           'all8 ORIGINAL preimages and circle points transfer properly')
    return dict(proper_matrix=[encode(r) for r in R],positive_raw_alignment_factor=factor.encode(),
        both_original_circle_counts=[8,8],original_circle_preimages_transferred=True,
        proper_directed_circle_point_bijection=True,body_symmetry_assumed=False,
        low_original_circle=[encode(v) for v in ol],high_original_circle=[encode(v) for v in oh]),lo

def eligible_pool(V,B,dW,heightU,supplied=None):
    N=dot(B,B)
    exact=sorted(v for v in V if dot(v,B)**2/N<=Q((heightU+F(9,2)*dW)**2))
    active=sorted(v for v in V if dot(v,B)**2/N==Q(F(1,3)))
    chosen=exact if supplied is None else supplied
    demand(chosen==exact==active and len(chosen)==12,
           'complete eligible pool is exactly12 ORIGINAL winning active vertices')
    pool=sorted(project(v,B) for v in chosen)
    demand(len(pool)==len(set(pool))==12 and all(neg(p) in pool for p in pool),
           'twelve distinct antipodal original candidate projections')
    demand(all(dot(p,B)==ZERO and dot(p,p)==RT for p in pool),
           'all winning eligible candidate reference radii and planes')
    excluded=sorted(V-set(chosen))
    demand(len(excluded)==48 and min(dot(v,B)**2/N for v in excluded)==Q(F(5,3)),
           'all48 nonactive receiving ORIGINALS accounted for')
    return dict(complete_original_candidates=12,excluded_originals=48,
        maximum_eligible_reference_height_squared=Q(F(1,3)).encode(),
        minimum_excluded_reference_height_squared=Q(F(5,3)).encode(),
        all_original_candidate_indices=[sorted(V).index(v) for v in chosen],
        all_original_candidate_preimages=[encode(v) for v in chosen],
        all_original_candidate_reference_points=[encode(p) for p in pool],
        original_height_eligibility_upper=str(heightU+F(9,2)*dW)),pool

# A small generic Fraction polynomial kernel; eight unconstrained 2D coordinates.
def padd(*polys):
    out={}
    for poly in polys:
        for e,c in poly.items():out[e]=out.get(e,F(0))+c
    return {e:c for e,c in out.items() if c}

def pscale(p,c):return {e:v*c for e,v in p.items() if v*c}

def pmul(a,b):
    out={}
    for e,c in a.items():
        for f,d in b.items():
            k=tuple(x+y for x,y in zip(e,f));out[k]=out.get(k,F(0))+c*d
    return {e:c for e,c in out.items() if c}

def variable(i):return {tuple(int(k==i) for k in range(8)):F(1)}

def pdot(a,b):return padd(*(pmul(x,y) for x,y in zip(a,b)))

def pdet(a,b):return padd(pmul(a[0],b[1]),pscale(pmul(a[1],b[0]),F(-1)))

def symbolic_pair_identity(area_coefficient=F(2)):
    x=[variable(i) for i in range(8)];s0,s1,t0,t1=x[:2],x[2:4],x[4:6],x[6:8]
    A=pscale(padd(pdot(s0,t0),pdot(s1,t1)),F(1,2))
    B=pscale(padd(pdet(s0,t0),pdet(s1,t1)),F(1,2))
    lhs=padd(pmul(A,A),pmul(B,B))
    rhs=pscale(padd(pmul(pdot(s0,s0),pdot(t0,t0)),
        pmul(pdot(s1,s1),pdot(t1,t1)),
        pscale(pmul(pdot(s0,s1),pdot(t0,t1)),F(2)),
        pscale(pmul(pdet(s0,s1),pdet(t0,t1)),area_coefficient)),F(1,4))
    demand(padd(lhs,pscale(rhs,F(-1)))=={},'generic oriented two-point correlation identity')
    lagrange=padd(pmul(pdot(s0,s0),pdot(s1,s1)),
        pscale(pmul(pdot(s0,s1),pdot(s0,s1)),F(-1)),
        pscale(pmul(pdet(s0,s1),pdet(s0,s1)),F(-1)))
    demand(lagrange=={},'generic 2D dot/determinant Gram identity')
    return dict(unconstrained_coordinates=8,proper_pair_identity_all_coefficients_zero=True,
        dot_determinant_Gram_identity_all_coefficients_zero=True,
        full_two_point_square_monomials=len(lhs),
        exact_full_expanded_pair_polynomial_sha256=digest([[list(e),str(c)] for e,c in sorted(lhs.items())]))

def assignments(patterns=None,axis_orders=None):
    signs=list(itertools.product((-1,1),repeat=4)) if patterns is None else patterns
    axes=list(itertools.permutations(range(6),4)) if axis_orders is None else axis_orders
    demand(len(signs)==16 and set(signs)==set(itertools.product((-1,1),repeat=4)),
           'all16 signed antipodal assignment patterns')
    demand(len(axes)==360 and set(axes)==set(itertools.permutations(range(6),4)),
           'all360 injective four-of-six antipodal axis assignments')
    return itertools.product(axes,signs)

def mapping(ids,signs):
    demand(len(ids)==len(signs)==4 and len(set(ids))==4 and
           all(type(i) is int and 0<=i<6 for i in ids) and all(s in (-1,1) for s in signs),
           'complete signed four-axis injection')
    out=[]
    for i,s in zip(ids,signs):
        offset=0 if s==1 else 1;out.extend((2*i+offset,2*i+1-offset))
    demand(len(set(out))==8 and all((out[i]^1)==out[i^1] for i in range(8)),
           'all8 distinct original antipodal destinations')
    return out

def metric_filter(source,dest):
    pairkeys=list(itertools.combinations(range(8),2));sr=[];dr={};roots=[]
    for a,b in pairkeys:
        d=subtract(source[a],source[b]);sq=dot(d,d)
        lo,hi=axial.exact_root('mixed_source_pair'+str(a)+'_'+str(b),sq)
        sr.append((lo,hi));roots.append(['source',a,b,sq.encode(),str(lo),str(hi)])
    for a,b in itertools.combinations(range(12),2):
        d=subtract(dest[a],dest[b]);sq=dot(d,d)
        lo,hi=axial.exact_root('mixed_destination_pair'+str(a)+'_'+str(b),sq)
        dr[a,b]=(lo,hi);roots.append(['destination',a,b,sq.encode(),str(lo),str(hi)])
    count=rejected=0;survivors=[];h=hashlib.sha256()
    for ids,signs in assignments():
        count+=1;mp=mapping(ids,signs);failure=None
        for k,(a,b) in enumerate(pairkeys):
            x,y=sorted((mp[a],mp[b]));sl,su=sr[k];dl,du=dr[x,y]
            lower=max(sl-du,dl-su)
            if lower>2*FLAT:failure=[a,b,x,y,str(lower)];break
        if failure is None:survivors.append(dict(destination_axes=list(ids),signs=list(signs)))
        else:rejected+=1
        h.update(json.dumps([list(ids),list(signs),failure],separators=(',',':')).encode())
    demand(count==5760 and rejected==5748 and len(survivors)==12,
           'complete metric enumeration yields exactly12 surviving injections')
    return dict(all_signed_antipodal_injections=count,metric_rejections=rejected,
        complete_metric_survivors=survivors,metric_survivors=len(survivors),
        all5760_first_witness_record_sha256=h.hexdigest(),
        outward_pair_root_count=len(roots),all94_outward_pair_root_audit_sha256=digest(roots)),survivors

def directed_pair_upper(si,sj,ti,tj,ms,mt,nL,nU):
    demand(nL>0 and nL<=nU,'positive outward normal-product root endpoints')
    N=dot(ms,ms)*dot(mt,mt)
    demand(Q(nL*nL)<=N<=Q(nU*nU),'outward directed normal-product root brackets')
    demand(all(dot(p,ms)==ZERO and dot(p,p)==RS for p in (si,sj)) and
           all(dot(p,mt)==ZERO and dot(p,p)==RT for p in (ti,tj)),
           'actual per-point source/target plane and equal-radius assumptions')
    D=dot(si,sj)*dot(ti,tj)
    S=dot(ms,cross(si,sj))*dot(mt,cross(ti,tj))
    upper=(RS*RT+D+S/(nL if S>=ZERO else nU))/2
    demand(upper>=ZERO,'nonnegative outward proper pair correlation square')
    return upper,D,S

def pair_filter(source,dest,ms,mt,survivors):
    N=dot(ms,ms)*dot(mt,mt)
    demand(N==(31-17*PHI)/3,'exact positive directed raw-normal product')
    nL,nU=axial.exact_root('mixed_pair_normal_product',N)
    L=(RS+RT-Q(FLAT*FLAT))/2;demand(L>ZERO,'positive necessary pair mean correlation')
    records=[];audits=0;survived=0
    for row in survivors:
        mp=mapping(row['destination_axes'],row['signs']);target=[dest[k] for k in mp]
        witnesses=[];h=hashlib.sha256()
        for i,j in itertools.combinations(range(8),2):
            audits+=1
            upper,D,S=directed_pair_upper(source[i],source[j],target[i],target[j],ms,mt,nL,nU)
            margin=L*L-upper
            h.update(json.dumps([i,j,upper.encode(),margin.encode()],separators=(',',':')).encode())
            if margin>ZERO:
                if not witnesses:demand(margin>Q(1),'every first exact pair witness has margin above one')
                witnesses.append(dict(source_pair=[i,j],destination_pair=[mp[i],mp[j]],
                    exact_dot_product=D.encode(),signed_raw_oriented_area_product=S.encode(),
                    max_proper_pair_mean_correlation_squared_upper=upper.encode(),
                    exact_positive_common_roll_margin=margin.encode()))
        if not witnesses:survived+=1
        records.append(dict(**row,all28_pair_moments_sha256=h.hexdigest(),
            rejecting_source_pairs=len(witnesses),first_exact_pair_witness=witnesses[0] if witnesses else None))
    demand(len(records)==12 and audits==336 and survived==0,
           'every complete metric survivor has an exact common-proper-roll obstruction')
    return dict(normal_product_squared=N.encode(),outward_normal_product_root=[str(nL),str(nU)],
        positive_required_pair_mean_correlation=L.encode(),
        all12_mapping_records=records,all28_pairs_per_mapping=28,all_pair_moments=audits,
        survivors_after_common_proper_roll_filter=survived,
        every_first_exact_common_roll_margin_strictly_above_one=True)

def validate_pair_witness(row,source,dest,ms,mt):
    mp=mapping(row['destination_axes'],row['signs'])
    witness=row['first_exact_pair_witness'];i,j=witness['source_pair']
    demand(type(i) is int and type(j) is int and 0<=i<j<8,'ordinary ordered source pair')
    demand(witness['destination_pair']==[mp[i],mp[j]],'original pair witness decoding')
    N=dot(ms,ms)*dot(mt,mt);nL,nU=axial.exact_root('mixed_pair_witness_root',N)
    upper,D,S=directed_pair_upper(source[i],source[j],dest[mp[i]],dest[mp[j]],ms,mt,nL,nU)
    L=(RS+RT-Q(FLAT*FLAT))/2;margin=L*L-upper
    demand(witness['exact_dot_product']==D.encode() and witness['signed_raw_oriented_area_product']==S.encode() and
           witness['max_proper_pair_mean_correlation_squared_upper']==upper.encode() and
           witness['exact_positive_common_roll_margin']==margin.encode() and margin>ZERO,
           'exact positive properly oriented original pair witness')

def new_receiving_direction(V,B):
    u=(Q(F(1,25)),B[1],B[2])
    values=[dot(v,u)**2/dot(u,u) for v in V];f2=min(values)
    demand(all(dot(v,u)*dot(v,B)>ZERO for v in V),
           'all60 original winning signed-region inequalities persist')
    demand(Q(Q0*Q0)<=f2<Q(F(21,50)**2),
           'actual new winning receiver lies strictly below old branch height cutoff')
    return dict(raw_original_receiving_direction=encode(u),
        actual_minimum_original_squared_height=f2.encode(),
        all60_original_signs_and_heights_checked=True,
        old21over50_mixed_branch_does_not_cover_this_receiver=True,
        outside_every_other_old_geometric_domain_claimed=False)

def transport_regressions(V,normals):
    """Actual inverse-frame evaluations complement the written Rodrigues proof."""
    def upper_root(x):
        out=axial.inherited_root(x)
        demand(out.lo>=0 and out.lo<=out.hi and out.hi-out.lo<=F(1,10**12) and
               Q(out.lo*out.lo)<=x<=Q(out.hi*out.hi),'regression outward positive root')
        return out.hi
    rows=[];matrices=0
    for m in normals:
        N=dot(m,m)
        heights={v:upper_root(dot(v,m)**2/N) for v in V}
        for axis in ((Q(1),ZERO,ZERO),(ZERO,-m[2],m[1])):
            demand(dot(axis,m)==ZERO,'actual minimal-transport axis perpendicular to reference')
            for t in (F(-1,100),F(0),F(1,100)):
                w=tuple(t*x for x in axis);w2=dot(w,w)
                skew=((ZERO,-w[2],w[1]),(w[2],ZERO,-w[0]),(-w[1],w[0],ZERO))
                A=tuple(tuple(((1-w2)*I[i][j]+2*w[i]*w[j]+2*skew[i][j])/(1+w2)
                              for j in range(3)) for i in range(3))
                At=tuple(zip(*A));image=act(A,m)
                demand(matmul(At,A)==I and determinant(*A)==Q(1) and dot(image,image)==N,
                       'actual proper normal transport matrix')
                d2=2*(1-dot(m,image)/N)
                demand(d2==4*w2/(1+w2) and d2<Q(F(1,10)**2),
                       'exact chord of actual minimal normal transport')
                dU=upper_root(d2);matrices+=1
                for v in sorted(V):
                    diff=subtract(project(act(At,v),m),project(v,m));sq=dot(diff,diff)
                    bound=heights[v]*dU+F(9,4)*dU*dU
                    demand(sq<=Q(bound*bound),'height-dependent ORIGINAL inverse-frame transport bound')
                    rows.append([encode(m),encode(axis),str(t),encode(v),sq.encode(),str(bound)])
    demand(matrices==18 and len(rows)==1080,'all18proper matrices and1080original transport regressions')
    return dict(proper_minimal_transport_matrices=18,all_original_inverse_frame_regressions=1080,
        positive_and_negative_tilts_and_identity=True,all60circle_and_noncircle_originals=True,
        complete_exact_regression_sha256=digest(rows),universal_Rodrigues_identity_proved_in_written_argument=True)

def controls(V,B,dW,hU,source,dest,pair):
    rejected=[]
    def reject(name,action):
        try:action()
        except (ValueError,AssertionError,KeyError):rejected.append(name);return
        raise ValueError('malformed evidence accepted: '+name)
    reject('missing_input_pin',lambda:validate_pins(INPUTS['files'][:-1]))
    pins=copy.deepcopy(INPUTS['files']);pins[0]['sha256']='0'*64
    reject('wrong_input_bytes',lambda:validate_pins(pins))
    reject('missing_original_body_vertex',lambda:axial.validate_body(V-{min(V)}))
    pool=sorted(v for v in V if dot(v,B)**2/dot(B,B)==Q(F(1,3)))
    reject('missing_eligible_original',lambda:eligible_pool(V,B,dW,hU,supplied=pool[:-1]))
    reject('added_noneligible_original',lambda:eligible_pool(V,B,dW,hU,supplied=sorted(pool+[min(V-set(pool))])))
    reject('missing_sign_pattern',lambda:assignments(patterns=list(itertools.product((-1,1),repeat=4))[:-1]))
    reject('missing_axis_assignment',lambda:assignments(axis_orders=list(itertools.permutations(range(6),4))[:-1]))
    reject('duplicate_destination_axis',lambda:mapping([0,0,1,2],[1]*4))
    reject('unsupported_smaller_height',lambda:scalar(q=F(2,5)))
    reject('unsafe_original_candidate_error',lambda:scalar(candidate=F(1,100)))
    reject('unsafe_flattened_match_error',lambda:scalar(flat=F(1,100)))
    improper=((Q(1),ZERO,ZERO),(ZERO,Q(-1),ZERO),(ZERO,ZERO,Q(1)))
    reject('improper_threshold_class_transfer',lambda:proper_source_transfer(V,supplied=improper))
    R=((Q(-1),ZERO,ZERO),(ZERO,(2*PHI-1)/5,-2*(2*PHI-1)/5),
       (ZERO,-2*(2*PHI-1)/5,-(2*PHI-1)/5))
    half_x=((Q(1),ZERO,ZERO),(ZERO,Q(-1),ZERO),(ZERO,ZERO,Q(-1)))
    reject('reversed_directed_threshold_transfer',lambda:proper_source_transfer(V,supplied=matmul(half_x,R)))
    reject('missing_oriented_area_term',lambda:symbolic_pair_identity(F(0)))
    reject('improper_area_sign',lambda:symbolic_pair_identity(F(-2)))
    reject('wrong_area_coefficient',lambda:symbolic_pair_identity(F(1)))
    ms,mt=LOW,B;N=dot(ms,ms)*dot(mt,mt);nL,nU=axial.exact_root('control_positive_normal_product',N)
    reject('inward_normal_root',lambda:directed_pair_upper(source[0],source[2],dest[0],dest[2],ms,mt,nU+1,nU+2))
    reject('wrong_per_point_radius',lambda:directed_pair_upper(tuple(2*x for x in source[0]),source[2],dest[0],dest[2],ms,mt,nL,nU))
    reject('wrong_source_plane',lambda:directed_pair_upper(tuple(source[0][i]+ms[i] for i in range(3)),source[2],dest[0],dest[2],ms,mt,nL,nU))
    row=copy.deepcopy(pair['all12_mapping_records'][0]);row['first_exact_pair_witness']['exact_positive_common_roll_margin']=['0','0']
    reject('nonstrict_pair_obstruction',lambda:validate_pair_witness(row,source,dest,ms,mt))
    row=copy.deepcopy(pair['all12_mapping_records'][0]);row['first_exact_pair_witness']['signed_raw_oriented_area_product']=['0','0']
    reject('false_directed_area_witness',lambda:validate_pair_witness(row,source,dest,ms,mt))
    row=copy.deepcopy(pair['all12_mapping_records'][0]);row['first_exact_pair_witness']['destination_pair'].reverse()
    reject('wrong_original_pair_decoding',lambda:validate_pair_witness(row,source,dest,ms,mt))
    demand(len(rejected)==22,'all22 malformed evidence controls rejected')
    return rejected

def check(self_test=False):
    axial.ROOT_RECORDS.clear();V=vertices();axial.validate_body(V)
    scalars,dT,dW,etaT,etaW,hU=scalar()
    W,B=axial.winning_geometry(V)
    T=[axial.threshold_geometry(n,V) for n in (LOW,REFS[1])]
    transfer,points=proper_source_transfer(V)
    pool_record,pool=eligible_pool(V,B,dW,hU)
    srep=sorted({canonical(v) for v in points});drep=sorted({canonical(v) for v in pool})
    demand(len(srep)==4 and len(drep)==6,'complete four source and six target antipodal axes')
    source=[p for v in srep for p in (v,neg(v))];dest=[p for v in drep for p in (v,neg(v))]
    identity=symbolic_pair_identity();metric,survivors=metric_filter(source,dest)
    pair=pair_filter(source,dest,LOW,B,survivors)
    for row in pair['all12_mapping_records']:validate_pair_witness(row,source,dest,LOW,B)
    proper_gauges=axial.orbit_certificate(V,B)
    new_receiver=new_receiving_direction(V,B)
    transport=transport_regressions(V,(LOW,REFS[1],B))
    roots=dict(axial.ROOT_RECORDS)
    rejected=controls(V,B,dW,hU,source,dest,pair) if self_test else []
    return dict(agent='six-rupert-3',role='researcher',
        proof_status='complete_written_unformalized_author_checked_mixed_source_branch_exclusion',
        independently_reviewed=False,global_RID_status='OPEN',
        branch='both threshold signed-region ORIGINAL sources into winning receivers f(n)>=83/200',
        closed_containment_excluded_for_every_proper_Q_planar_t_and_lambda_at_least_one=True,
        branch_beta_minus_one28_receiving_band_included=True,
        current_published_GLOBAL_height_upper='21/50',current_published_GLOBAL_squared_height_gap='1/31',
        wider_GLOBAL_height_band_proved=False,all60_original_body_vertices=[encode(v) for v in sorted(V)],
        fresh_scalar_bounds=scalars,complete_winning_original_geometry=W,
        both_complete_threshold_original_geometries=T,proper_threshold_source_transfer=transfer,
        complete_receiving_original_pool=pool_record,
        source_antipodal_order=[encode(p) for p in source],destination_antipodal_order=[encode(p) for p in dest],
        symbolic_two_point_identities=identity,complete_metric_filter=metric,
        exact_common_proper_roll_pair_filter=pair,directed_actual_proper_gauges=proper_gauges,
        actual_new_receiving_direction=new_receiver,original_transport_regressions=transport,
        all_positive_outward_roots=roots,published56mathematical_input_pins_checked=True,
        input_manifest_sha256=hashlib.sha256(INPUT_BYTES).hexdigest(),malformed_controls_rejected=rejected,
        original_global_436_signed_regions_reenumerated=False,
        universal_original_matching_and_directed_plane_proof='MIXED_PAIR_ROLL_PROOF.md')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emit',action='store_true');args=p.parse_args()
    record=check(self_test=True);raw=(json.dumps(record,indent=2)+'\n').encode()
    if args.emit:print(raw.decode(),end='')
    else:
        demand(raw==(HERE/'mixed_pair_roll_expected.json').read_bytes(),
               'every exact expected certificate byte must match')
        print(json.dumps(dict(status='verified_every_expected_byte',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
            original_injections=5760,metric_survivors=12,exact_pair_moments=336,common_roll_survivors=0,
            malformed_controls=22,global_RID='OPEN',GLOBAL_gap='1/31 unchanged')))

if __name__=='__main__':main()
