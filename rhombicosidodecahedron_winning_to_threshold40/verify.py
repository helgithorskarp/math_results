#!/usr/bin/env python3
"""Exact finite hypotheses of PROOF.md, Python3.11+ standard library.

Two fixed CLOSED proper-roll covers with one ORIGINAL source vertex per
leaf and ALL SIX source-height corners checked for that same original.
Author validation, not independent review or formalization. No search.
"""
import argparse,copy,hashlib,json,re,sys
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'rhombicosidodecahedron_mirror_cluster_obstruction'
OLD40=HERE.parent/'rhombicosidodecahedron_threshold_band40'
DEPENDENCY_SHA='f99edfab5e42e2e67fe9b7433a3efb8ab4fb90454446030fbf1d868e556aa53d'

def demand(ok,message):
    if not ok:raise ValueError(message)

DEP_RAW=(HERE/'dependencies.json').read_bytes()
demand(hashlib.sha256(DEP_RAW).hexdigest()==DEPENDENCY_SHA,'fixed complete dependency manifest')
DEPS=json.loads(DEP_RAW)

def validate_pins(rows,check_files=True):
    demand(rows==DEPS['files'] and len(rows)==69 and len({r['file'] for r in rows})==69,
        'all69 fixed distinct previous mathematical inputs')
    for r in rows:
        demand(set(r)=={'file','bytes','sha256'},'exact byte pin schema')
        p=Path(r['file'])
        demand(len(p.parts)==2 and p.parts[0] in (BASE.name,OLD40.name) and p.suffix in ('.py','.json'),
            'ordinary owned mathematical input path')
        demand(type(r['bytes']) is int and 0<r['bytes']<1000000 and
            re.fullmatch('[0-9a-f]{64}',r['sha256']),'canonical input byte commitment')
        if check_files:
            target=HERE.parent/p
            demand(target.is_file() and not target.is_symlink(),'regular published input')
            raw=target.read_bytes()
            demand(len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'],
                'published input mismatch: '+r['file'])
validate_pins(DEPS['files'])
sys.path.insert(0,str(BASE))
from verify import QPhi as Q,PHI,ZERO,dot,vertices
from torque_certificate import cross,subtract
from cell_certificate import encode,decode
from linear_roll_certificate import project
from threshold_receiver_certificate import Interval,field,root,hull_data,source_coordinates,facet_coefficients
import axial_majorization_certificate as axial
import gamma_branch_certificate as gamma83
import coupled_nonwinning_certificate as coupled

Q0=F(2,5);SAFETY=F(1,10000);CORNERS=6;DEPTH=8
REFS=((ZERO,(2-PHI)/3,Q(-1)),(ZERO,Q(1),(3*PHI-1)/11))
INPUTS=json.loads((HERE/'certificates.json').read_bytes())

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def validate_input(data):
    demand(isinstance(data,dict) and set(data)=={'schema','receiving_cutoff','strict_support_margin',
        'winning_outer_corner_count','proper_roll_quarters','max_depth',
        'actual_raw_receiving_references','both_closed_roll_covers'},'exact fixed certificate schema')
    fixed=dict(schema='rid-winning-threshold40-directional-covers-v1',receiving_cutoff='2/5',
        strict_support_margin='1/10000',winning_outer_corner_count=6,proper_roll_quarters=4,max_depth=8)
    demand(all(type(data[k]) is type(v) and data[k]==v for k,v in fixed.items()),
        'declared theorem domain and fixed witness policy')
    demand(data['actual_raw_receiving_references']==[encode(r) for r in REFS],
        'both ACTUAL raw normalizations')
    covers=data['both_closed_roll_covers']
    demand(isinstance(covers,list) and len(covers)==2,'both proper receiving classes')
    for leaves in covers:
        coupled.validate_closed_tree(leaves,192)
        demand(all(len(word)<=DEPTH for _,word,_ in leaves),'fixed depth bound')
validate_input(INPUTS)

def scalar_bridge(q=Q0):
    demand(q==Q0,'this certificate proves exactly the declared q2/5 band')
    cL,cU=axial.exact_root('mixed40_threshold_height',axial.BETA)
    c0L,c0U=axial.exact_root('mixed40_winning_height',Q(F(1,3)))
    rtL,rtU=axial.exact_root('mixed40_threshold_disk',(39+37*PHI)/29)
    rwL,rwU=axial.exact_root('mixed40_winning_disk',Q(F(8,3))+4*PHI)
    sT,sW=(cU-q)/rtL,(c0U-q)/rwL
    demand(0<sT<1 and 0<sW<1,'positive whole signed-region tangent bounds')
    zTL,zTU=axial.exact_root('mixed40_threshold_cosine',Q(1-sT*sT))
    zWL,zWU=axial.exact_root('mixed40_winning_cosine',Q(1-sW*sW))
    dT,dW=F(1001,1000)*sT,F(1001,1000)*sW
    gates=dict(reference_threshold_height_above_q=cL>q,reference_winning_height_above_q=c0L>q,
        threshold_honest_chord_conversion=F(1001,1000)**2*(1+zTL)>2,
        winning_honest_chord_conversion=F(1001,1000)**2*(1+zWL)>2,
        threshold_chord_below31over1000=dT<F(31,1000),
        winning_chord_below59over1000=dW<F(59,1000),
        original_body_radius_below9over2=7+8*PHI<Q(F(9,2)**2),
        q_squared_above_every_other_region=Q(q*q)>Q(F(1,7)))
    demand(all(gates.values()),'fresh scalar bridge unsupported')
    return dict(q=str(q),threshold_tangent_bound=str(sT),winning_tangent_bound=str(sW),
        threshold_normal_chord_upper=str(dT),winning_normal_chord_upper=str(dW),
        threshold_quadratic_remainder_upper=str(F(9,4)*dT*dT),
        winning_quadratic_remainder_upper=str(F(9,4)*dW*dW),all8_scalar_gates=gates,
        source_original_height_from_centered_shadow_diameter=True,
        initial_full_rotation_small_angle_assumed=False),dT,dW

def clip(poly,A,B,C):
    def val(p):return A*p[0]+B*p[1]+C
    out=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        vp,vq=val(p),val(q)
        if vp>=ZERO:out.append(p)
        if vp<ZERO<vq or vq<ZERO<vp:
            t=vp/(vp-vq);demand(ZERO<t<Q(1),'strict exact crossing parameter')
            u=tuple(p[k]+t*(q[k]-p[k]) for k in range(2))
            demand(val(u)==ZERO,'exact original-height boundary intersection');out.append(u)
    unique=[]
    for p in out:
        if not unique or p!=unique[-1]:unique.append(p)
    if len(unique)>1 and unique[0]==unique[-1]:unique.pop()
    demand(unique,'nonempty complete original-height domain')
    return unique

def validate_polygon(poly,r,V,lo,a,b,count):
    demand(len(poly)==len(set(poly))==count,'complete distinct outer polygon vertices')
    def det(p,q):return p[0]*q[1]-p[1]*q[0]
    tangent=(ZERO,-r[2],r[1]);record=[]
    for i,p in enumerate(poly):
        q,w=poly[(i+1)%count],poly[(i+2)%count]
        demand(det(subtract(q,p),subtract(w,q))>ZERO,'strict positive cyclic turn')
        demand(det(subtract(q,p),tuple(-x for x in p))>ZERO,'reference raw origin strictly interior')
        demand(-Q(a)<=p[0]<=Q(a) and -Q(b)<=p[1]<=Q(b),'original chart rectangle')
        u=(p[0],r[1]+p[1]*tangent[1],r[2]+p[1]*tangent[2])
        demand(dot(r,u)==dot(r,r),'actual orthogonal raw normalization')
        for v in sorted(V):
            h=dot(v,r);demand(h!=ZERO,'strict original reference signs')
            sg=1 if h>ZERO else -1;g=sg*dot(v,u)-Q(Q0*lo)
            demand(g>=ZERO,'all60 original necessary heights at every polygon vertex')
            record.append(g.encode())
    return record

def outer_polygon(name,r,V,d,norm_bound,count):
    demand(r[0]==ZERO and dot(r,r)<Q(norm_bound**2),'proper raw chart norm bound')
    lo,hi=axial.exact_root(name+'_raw_norm',dot(r,r))
    z=1-d*d/2;demand(z>0,'positive chart denominator')
    a,b=norm_bound*d/z,d/z;tangent=(ZERO,-r[2],r[1])
    poly=[(Q(-a),Q(-b)),(Q(a),Q(-b)),(Q(a),Q(b)),(Q(-a),Q(b))]
    cuts=[]
    for i,v in enumerate(sorted(V)):
        h=dot(v,r);demand(h!=ZERO,'nonzero reference original height');sg=1 if h>ZERO else -1
        C=sg*h-Q(Q0*lo);demand(C>ZERO,'raw reference strictly inside every necessary halfplane')
        nxt=clip(poly,sg*v[0],sg*dot(v,tangent),C)
        if nxt!=poly:cuts.append([i,sg,len(poly),len(nxt)])
        poly=nxt
    gates=validate_polygon(poly,r,V,lo,a,b,count)
    U=[(p[0],r[1]+p[1]*tangent[1],r[2]+p[1]*tangent[2]) for p in poly]
    return dict(name=name,raw_reference=encode(r),outward_raw_norm=[str(lo),str(hi)],
        normal_chord_upper=str(d),raw_chart_norm_bound=str(norm_bound),rectangle_alpha_gamma=[str(a),str(b)],
        ordered_tangent_polygon=[[x.encode() for x in p] for p in poly],ordered_actual_raw_polygon=[encode(u) for u in U],
        all60_original_halfplanes_intersected=True,all_original_clipping_changes=cuts,
        all_corner_original_height_gates=len(gates),height_gate_sha256=digest(gates),
        strict_cyclic_turn_and_origin_tests=2*count,
        necessary_outer_domain_is_not_sufficient_for_actual_normalized_height=True),U,poly,(lo,a,b)

def adjusted_points(B,H0,originals,WB,selected=None):
    demand(len(H0)==len(originals)==12 and len(WB)==6,'all original source points and all six corners')
    N=dot(B,B);points=[];record=[]
    for i,(p,v) in enumerate(zip(H0,originals)):
        demand(v in vertices() and project(v,B)==p and 3*dot(v,B)**2==N,
            'same actual ORIGINAL source preimage at every corner')
        for k,w in enumerate(WB):
            demand(dot(w,B)==ZERO,'source raw perturbation lies in reference tangent plane')
            a=tuple(p[t]-dot(v,B)*w[t]/N for t in range(3))
            demand(dot(a,B)==ZERO and tuple(a[t]-p[t] for t in range(3))==
                tuple(-dot(v,B)*w[t]/N for t in range(3)),'signed original source adjustment identity')
            points.append(a);record.append([i,k,encode(v),encode(a)])
    if selected is not None:demand(selected==points,'complete signed source-original corner association')
    return points,dict(original_source_vertex_count=12,source_outer_corner_count=6,adjusted_point_count=72,
        all72_signed_adjustment_identities_checked=True,complete_source_adjustment_sha256=digest(record),
        adjusted_vectors_are_auxiliary_bounds_not_original_vertices=True)

def receiving_envelope(j,n,V,H,normals,U,d):
    demand(len(V)==60 and len(H)==len(normals)==16 and len(U)==4,'complete original receiving envelope')
    N=dot(n,n);eta=[];record=[];details=[]
    for k,(p,m) in enumerate(zip(H,normals)):
        ml,mh=axial.exact_root('mixed40_facet_norm_'+str(j)+'_'+str(k),dot(m,m))
        demand(ml>0 and dot(m,p)>ZERO,'positive original unit facet')
        upper=[];linear_values=[];ties=0
        for i,v in enumerate(sorted(V)):
            g=dot(m,subtract(p,v));demand(g>=ZERO,'all original reference supports')
            ties+=g==ZERO
            signed=[-dot(v,n)*dot(m,subtract(u,n))/N for u in U]
            M=max(signed);demand(M>=ZERO,'raw origin contained in the physical outer polygon')
            L=field(M).hi/ml;gap=field(g).lo/mh
            demand(L>=0 and gap>=0,'outward signed linear bound and nonnegative reference slack')
            upper.append(L-gap);linear_values.append(M)
            record.append([k,i,g.encode(),[x.encode() for x in signed],str(L),str(gap),str(upper[-1])])
        E=max(upper)+F(9,4)*d*d;demand(E>0,'positive whole original receiving envelope')
        eta.append(E)
        details.append(dict(facet=k,reference_tied_original_count=ties,
            maximizing_original_index=max(range(60),key=lambda i:upper[i]),
            whole_original_support_error_upper=str(E),
            maximum_exact_signed_polygon_linear_numerator=max(linear_values).encode()))
    demand(len(record)==960,'all16 facets and all60 originals, including tied noncorners')
    return eta,dict(all_original_facet_envelopes=960,signed_polygon_corner_comparisons=3840,
        all16_original_facets=details,full_envelope_record_sha256=digest(record),
        actual_receiving_hull_combinatorics_presumed=False)

def coefficients(H,n,adjusted,B,eta,quadratic):
    demand(len(adjusted)==72 and len(eta)==16,'complete source-corner grouping and receiving envelopes')
    coords=source_coordinates(adjusted,B)
    raw=facet_coefficients(H,n,coords)
    demand(len(raw)==1152,'all16 facets times12 original source vertices times6 source corners')
    lifted=[(A,D,h+Interval(quadratic+eta[k//72],quadratic+eta[k//72])) for k,(A,D,h) in enumerate(raw)]
    return lifted,coords

def replay(leaves,coeff,safety=SAFETY,audit=None):
    demand(safety>0 and len(coeff)==1152,'positive margin and all original/corner coefficient triples')
    nodes=coupled.validate_closed_tree(leaves,192)
    quarters=[coupled.beta.quarter_coefficients(coeff,q) for q in range(4)]
    record=[];direct=[]
    for q,path,index in leaves:
        demand(len(path)<=DEPTH,'fixed certified closed depth')
        lo,hi=coupled.dyadic_interval(path);coupled.beta.verify_bernstein_identity(lo,hi)
        for k in range(6):
            c=quarters[q][index*6+k]
            bounds=coupled.beta.lower_coefficients(c,lo,hi,safety)
            demand(min(bounds)>0,'ALL SIX corners for the SAME original on the entire closed leaf')
            record.append([q,path,index,k,str(lo),str(hi),[str(v) for v in bounds]])
            if audit is not None:
                H,n,coords,eta,quadratic=audit
                fj,si=divmod(index,12);rawmu=cross(subtract(H[(fj+1)%16],H[fj]),n)
                MU=root(dot(rawmu,rawmu));NN=root(dot(n,n));e2=cross(n,(Q(1),ZERO,ZERO))
                mx=field(rawmu[0]).divide_positive(MU)
                my=field(dot(rawmu,e2)).divide_positive(NN).divide_positive(MU)
                href=field(dot(rawmu,H[fj])).divide_positive(MU)
                px,py=coords[si*6+k]
                for t in (lo,(lo+hi)/2,hi):
                    co,se=(1-t*t)/(1+t*t),2*t/(1+t*t)
                    for _ in range(q):co,se=-se,co
                    rx=px.scale(co)-py.scale(se);ry=px.scale(se)+py.scale(co)
                    physical=mx*rx+my*ry
                    kernel=coeff[index*6+k][0].scale(co)+coeff[index*6+k][1].scale(se)
                    demand(physical.lo<=kernel.hi and kernel.lo<=physical.hi,'direct proper planar vector audit')
                    margin=physical.lo-href.hi-eta[fj]-quadratic-safety
                    demand(margin>0,'direct signed-corner vector support at exact audit parameter')
                    direct.append([q,path,index,k,str(t),str(margin)])
    return dict(complete_closed_quarter_roots=4,tree_nodes=nodes,closed_leaves=len(leaves),
        maximum_depth=max(len(p) for _,p,_ in leaves),selected_same_original_corner_gates=len(record),
        selected_strict_Bernstein_coefficients=3*len(record),
        minimum_selected_Bernstein_lower=str(min(F(x) for r in record for x in r[-1])),
        selected_record_sha256=digest(record),direct_vector_audit_count=len(direct),
        direct_vector_audit_sha256=digest(direct),strict_actual_support_margin=str(safety),
        proper_full_roll_and_closed_seams_included=True)

def spectrum_interface():
    obj=json.loads((BASE/'global_cap_expected.json').read_bytes())
    scores=obj['diameter_and_sign_regions']['score_counts']
    values=[decode_value(r['score']) for r in scores]
    demand(sum(r['regions'] for r in scores)==436 and
        sum(r['regions'] for r,v in zip(scores,values) if v==Q(F(1,3)))==10 and
        sum(r['regions'] for r,v in zip(scores,values) if v==axial.BETA)==60 and
        max(v for v in values if v not in (Q(F(1,3)),axial.BETA))==Q(F(1,7)),
        'inherited complete signed-region spectrum interface')
    return dict(projective_strict_regions=436,winning_regions=10,threshold_regions=60,
        maximum_other_region_squared_height='1/7',q_squared='4/25',
        old436region_enumeration_rerun=False,needed_only_for_all_source_threshold_receiver_corollary=True)

def decode_value(pair):
    demand(isinstance(pair,list) and len(pair)==2,'quadratic field encoding')
    return Q(F(pair[0]),F(pair[1]))

def reject(name,call,rows):
    try:call()
    except (ValueError,AssertionError):rows.append(name);return
    raise ValueError('malformed certificate accepted: '+name)

def check():
    axial.ROOT_RECORDS.clear();V=vertices();axial.validate_body(V)
    scalar,dT,dW=scalar_bridge();quadratic=F(9,4)*dW*dW
    axial.exact_root('mixed40_sqrt5',Q(5))
    source,B,H0,originals=gamma83.source_geometry(V)
    win_geom,_=axial.winning_geometry(V)
    threshold_geom=[axial.threshold_geometry(r,V) for r in REFS]
    orbits=axial.orbit_certificate(V,B)
    source_poly,UB,polyB,poly_args=outer_polygon('mixed40_winning',B,V,dW,F(27,25),6)
    WB=[subtract(u,B) for u in UB]
    adjusted,adjustment=adjusted_points(B,H0,originals,WB)
    previous=json.loads((OLD40/'expected.json').read_bytes())
    cases=[];saved=[]
    for j,n in enumerate(REFS):
        domain,U,poly,args=outer_polygon('mixed40_threshold'+str(j),n,V,dT,F(17,16),4)
        demand(domain['ordered_actual_raw_polygon']==previous['both_complete_original_threshold_cases'][j]
            ['original_height_clipped_domain']['ordered_actual_raw_polygon'],
            'same exact previously proved necessary threshold polygon, freshly reconstructed')
        _,H,normals,*_=hull_data(n,V)
        eta,envelope=receiving_envelope(j,n,V,H,normals,U,dT)
        coeff,coords=coefficients(H,n,adjusted,B,eta,quadratic)
        leaves=INPUTS['both_closed_roll_covers'][j]
        roll=replay(leaves,coeff,audit=(H,n,coords,eta,quadratic))
        cases.append(dict(case=j,original_raw_reference=encode(n),necessary_receiving_height_polygon=domain,
            all16_facet_support_errors=[str(e) for e in eta],full_original_receiving_envelope=envelope,
            all1152_original_facet_source_corner_coefficient_sha256=
                digest([[[str(i.lo),str(i.hi)] for i in row] for row in coeff]),complete_closed_proper_roll_cover=roll))
        saved.append((leaves,coeff))
    demand([c['complete_closed_proper_roll_cover']['closed_leaves'] for c in cases]==[32,70],
        'both complete fixed certificates')
    roots=copy.deepcopy(axial.ROOT_RECORDS)
    spectrum=spectrum_interface();rejected=[]
    leaves,coeff=saved[0]
    missing=copy.deepcopy(INPUTS);missing['both_closed_roll_covers']=missing['both_closed_roll_covers'][:1]
    wrong=copy.deepcopy(INPUTS);wrong['actual_raw_receiving_references'][0][1]=['1','0']
    too_small=copy.deepcopy(INPUTS);too_small['receiving_cutoff']='399/1000'
    bad_index=copy.deepcopy(leaves);bad_index[0][2]=192
    bad_source=list(adjusted);bad_source[0]=tuple(adjusted[0][i]+Q(int(i==0)) for i in range(3))
    lo,a,b=poly_args
    bad_poly=list(polyB);bad_poly[0]=(Q(100),Q(100))
    reject('missing_old_input_pin',lambda:validate_pins(DEPS['files'][:-1],False),rejected)
    corrupt=copy.deepcopy(DEPS['files']);corrupt[-1]['sha256']='0'*64
    reject('incorrect_old_input_byte_commitment',lambda:validate_pins(corrupt,False),rejected)
    reject('missing_original_vertex',lambda:axial.validate_body(V-{min(V)}),rejected)
    reject('unsupported_receiving_cutoff',lambda:validate_input(too_small),rejected)
    reject('incorrect_actual_raw_receiving_reference',lambda:validate_input(wrong),rejected)
    reject('missing_receiving_class',lambda:validate_input(missing),rejected)
    reject('wrong_scalar_cutoff',lambda:scalar_bridge(F(399,1000)),rejected)
    reject('missing_source_height_polygon_corner',lambda:validate_polygon(polyB[:-1],B,V,lo,a,b,6),rejected)
    reject('source_polygon_outside_necessary_domain',lambda:validate_polygon(bad_poly,B,V,lo,a,b,6),rejected)
    reject('reversed_polygon_orientation',lambda:validate_polygon(list(reversed(polyB)),B,V,lo,a,b,6),rejected)
    reject('incorrect_signed_source_original_adjustment',lambda:adjusted_points(B,H0,originals,WB,bad_source),rejected)
    reject('missing_same_original_corner_group',lambda:replay(leaves,coeff[:-1]),rejected)
    reject('missing_closed_circle_quarter',lambda:replay([r for r in leaves if r[0]!=3],coeff),rejected)
    reject('missing_closed_roll_leaf',lambda:replay(leaves[:-1],coeff),rejected)
    reject('duplicate_closed_roll_leaf',lambda:replay(leaves+[leaves[0]],coeff),rejected)
    reject('invalid_original_roll_witness',lambda:replay(bad_index,coeff),rejected)
    overlap=leaves+[[leaves[0][0],leaves[0][1]+'0',leaves[0][2]]]
    reject('overlapping_leaf_and_child',lambda:replay(overlap,coeff),rejected)
    reject('false_support_margin',lambda:replay(leaves,coeff,F(100)),rejected)
    reject('nonpositive_support_margin',lambda:replay(leaves,coeff,F(0)),rejected)
    demand(len(rejected)==19,'all19 certificate rejection controls')
    totals=dict(original_vertices=60,proper_body_symmetries=60,directed_reference_sign_regions=140,
        winning_original_source_vertices=12,original_source_hull_supports=720,
        original_height_halfplanes_clipped=180,original_height_polygon_corner_gates=840,
        original_receiving_reference_supports=1920,original_facet_receiving_envelopes=1920,
        signed_receiving_polygon_corner_bounds=7680,source_original_corner_adjustments=72,
        physical_interval_coefficient_triples=2304,closed_roll_leaves=102,
        same_original_source_corner_leaf_gates=612,strict_Bernstein_coefficients=1836,
        direct_planar_vector_audits=1836,outward_root_records=len(roots),malformed_controls=19)
    return dict(agent='six-rupert-3',role='researcher',proof_status='complete_written_unformalized_author_checked',
        independently_reviewed=False,global_RID_status='OPEN',global_receiving_cutoff='83/200 unchanged',
        global_squared_height_gap='1/28 unchanged',receiving_cutoff='2/5',
        conditional_closed_exclusion='winning sources into either threshold receiving class',
        corollary='all original sources exclude strict passage into threshold receivers f(n)>=2/5',
        winning_receiver_branches_at2over5_proved=False,full_original_Q_roll_t_lambda_ge1_included=True,
        all69_old_inputs_unchanged=True,fixed_dependency_manifest_sha256=DEPENDENCY_SHA,
        all60_original_vertices=[encode(v) for v in sorted(V)],source_original_geometry=source,
        fresh_whole_region_scalar_bridge=scalar,necessary_source_height_polygon=source_poly,
        signed_source_original_adjustment=adjustment,winning_active_tangent_geometry_sha256=digest(win_geom),
        both_threshold_active_tangent_geometry_sha256=[digest(x) for x in threshold_geom],
        actual_proper_gauge_certificate=orbits,both_complete_original_receiving_cases=cases,
        complete_outward_positive_root_records=roots,outward_root_record_sha256=digest(roots),
        inherited_signed_region_spectrum=spectrum,previous_global_or_threshold_cayley_replayed=False,
        exact_totals=totals,all_malformed_controls_rejected=rejected,continuous_proof='PROOF.md')

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--emit',action='store_true')
    args=parser.parse_args();result=check();raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
    if args.emit:(HERE/'expected.json').write_bytes(raw)
    else:demand(raw==(HERE/'expected.json').read_bytes(),'every compact expected certificate byte must match')
    print(json.dumps(dict(status='generated' if args.emit else 'verified_every_expected_byte',
        bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),receiving_cutoff='2/5',
        closed_roll_leaves=102,strict_Bernstein_coefficients=1836,direct_vector_audits=1836,
        malformed_controls_rejected=19,global_RID='OPEN',global_cutoff_improved=False),sort_keys=True))

if __name__=='__main__':main()
