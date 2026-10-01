#!/usr/bin/env python3
"""Exact finite hypotheses of PROOF.md, Python3.11+ standard library.

Two fixed CLOSED full proper-roll covers. Each leaf checks ALL FOUR source
polygon corners for the SAME original threshold vertex and receiving facet.
All16 original source hull preimages have their actual signed heights.
No search. Author checked; unformalized and independently unreviewed.
"""
import argparse,copy,hashlib,importlib.util,json,re,sys
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'rhombicosidodecahedron_mirror_cluster_obstruction'
PREV=HERE.parent/'rhombicosidodecahedron_winning_to_threshold40'
OLD40=HERE.parent/'rhombicosidodecahedron_threshold_band40'
DEPENDENCY_SHA='6528456028046e8ea4e0ca8275a2b11b30c9a77a7de62203c0af97c2ff2bd96d'

def demand(ok,message):
    if not ok:raise ValueError(message)

def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

RAW=(HERE/'dependencies.json').read_bytes()
demand(hashlib.sha256(RAW).hexdigest()==DEPENDENCY_SHA,'fixed complete dependency manifest')
DEPS=json.loads(RAW)

def validate_pins(rows,check_files=True):
    demand(rows==DEPS['files'] and len(rows)==73 and len({r['file'] for r in rows})==73,
        'all73 fixed distinct prior mathematical inputs')
    for r in rows:
        demand(set(r)=={'file','bytes','sha256'},'exact byte pin schema')
        p=Path(r['file'])
        demand(len(p.parts)==2 and p.parts[0] in (BASE.name,PREV.name,OLD40.name) and p.suffix in ('.py','.json'),
            'ordinary published mathematical input path')
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
from linear_roll_certificate import exact_hull,project
from cell_certificate import encode
from threshold_receiver_certificate import Interval,field,root,source_coordinates,facet_coefficients
import axial_majorization_certificate as axial
import gamma_branch_certificate as gamma83
import coupled_nonwinning_certificate as coupled
spec=importlib.util.spec_from_file_location('pinned_rid_mixed40',PREV/'verify.py')
previous=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=previous;spec.loader.exec_module(previous)

Q0=F(2,5);SAFETY=F(1,10000);K=4;NS=16;NR=12;DEPTH=3
REFS=((ZERO,(2-PHI)/3,Q(-1)),(ZERO,Q(1),(3*PHI-1)/11))
B=(ZERO,2-PHI,Q(1))
INPUTS=json.loads((HERE/'certificates.json').read_bytes())

def validate_input(data):
    fixed=dict(schema='rid-threshold-winning40-directional-covers-v1',receiving_cutoff='2/5',
        strict_support_margin='1/10000',source_original_count=16,source_outer_corner_count=4,
        receiving_original_facets=12,receiving_outer_corner_count=6,proper_roll_quarters=4,max_depth=3)
    demand(isinstance(data,dict) and set(data)==set(fixed)|{'actual_raw_source_references',
        'actual_raw_receiving_reference','both_closed_roll_covers'},'exact fixed input schema')
    demand(all(type(data[k]) is type(v) and data[k]==v for k,v in fixed.items()),'declared theorem and fixed witness policy')
    demand(data['actual_raw_source_references']==[encode(r) for r in REFS] and
        data['actual_raw_receiving_reference']==encode(B),'actual source and receiving raw normalizations')
    covers=data['both_closed_roll_covers']
    demand(isinstance(covers,list) and len(covers)==2,'both threshold source classes')
    for leaves in covers:
        coupled.validate_closed_tree(leaves,NS*NR)
        demand(all(len(word)<=DEPTH for _,word,_ in leaves),'fixed depth bound')
validate_input(INPUTS)

def original_source_geometry(r,V,selected=None,claimed_common_height=None):
    axial.validate_body(V);N=dot(r,r)
    S={project(v,r) for v in V};H=exact_hull(S,r)
    demand(len(S)==60 and len(H)==len(set(H))==NS,'full original threshold reference hull')
    originals=[];gaps=[];heights=[]
    for i,p in enumerate(H):
        preimages=[v for v in V if project(v,r)==p]
        demand(len(preimages)==1,'unique original source preimage')
        v=preimages[0];originals.append(v);heights.append(dot(v,r)**2/N)
        demand(dot(p,r)==ZERO,'source tangent point')
        mu=cross(subtract(H[(i+1)%NS],p),r)
        demand(dot(mu,p)>ZERO and dot(mu,mu)>ZERO,'positive original source facet')
        vals=[dot(mu,subtract(p,w)) for w in sorted(V)]
        demand(all(g>=ZERO for g in vals),'every original threshold source support')
        gaps.extend(g.encode() for g in vals)
    if selected is not None:demand(selected==originals,'all16 source hull corners with same ORIGINAL associations')
    if claimed_common_height is not None:
        demand(all(h==claimed_common_height for h in heights),'all source originals do not share the circle height')
    demand(sum(h==axial.BETA for h in heights)==8 and len(set(heights))>1,
        'eight circle originals and eight noncircle ORIGINAL source points with actual heights')
    return H,originals,dict(raw_reference=encode(r),all60_projections_distinct=True,
        all16_original_source_preimages=[dict(index=i,original=encode(v),reference_projection=encode(p),
            signed_raw_axial_height=dot(v,r).encode(),squared_unit_axial_height=h.encode())
            for i,(p,v,h) in enumerate(zip(H,originals,heights))],circle_originals=8,noncircle_originals=8,
        original_reference_supports=960,all960_support_slack_sha256=digest(gaps),
        noncircle_heights_assumed_equal_to_beta=False)

def adjusted_points(r,H,originals,U,selected=None):
    demand(len(H)==len(originals)==NS and len(U)==K,'all16 same-original preimages and all4 source corners')
    N=dot(r,r);points=[];record=[]
    for i,(p,v) in enumerate(zip(H,originals)):
        demand(v in vertices() and project(v,r)==p,'actual source ORIGINAL preimage')
        for s,u in enumerate(U):
            w=subtract(u,r);demand(dot(w,r)==ZERO,'source raw tangent perturbation')
            a=tuple(p[k]-dot(v,r)*w[k]/N for k in range(3))
            demand(dot(a,r)==ZERO and subtract(a,p)==tuple(-dot(v,r)*w[k]/N for k in range(3)),
                'signed same-original adjustment identity')
            points.append(a);record.append([i,s,encode(v),dot(v,r).encode(),encode(a)])
    if selected is not None:demand(points==selected,'complete signed same-original source adjustments')
    return points,dict(original_source_vertices=NS,source_polygon_corners=K,adjusted_vectors=len(points),
        all64_signed_original_adjustment_identities_checked=True,complete_record_sha256=digest(record),
        auxiliary_vectors_are_bounds_not_original_source_points=True)

def receiving_envelope(n,V,H,U,d):
    demand(n==B and len(V)==60 and len(H)==NR and len(U)==6,'complete original winning receiving domain')
    N=dot(n,n);eta=[];record=[];details=[]
    for j,p in enumerate(H):
        mu=cross(subtract(H[(j+1)%NR],p),n)
        ml,mh=axial.exact_root('reverse40_receiving_facet_norm_'+str(j),dot(mu,mu))
        demand(ml>0 and dot(mu,p)>ZERO,'positive original winning unit facet')
        upper=[];ties=0
        for i,v in enumerate(sorted(V)):
            g=dot(mu,subtract(p,v));demand(g>=ZERO,'every original receiving reference support')
            ties+=g==ZERO
            vals=[-dot(v,n)*dot(mu,subtract(u,n))/N for u in U]
            M=max(vals);demand(M>=ZERO,'raw origin included in the receiving polygon')
            L=field(M).hi/ml;G=field(g).lo/mh
            demand(L>=0 and G>=0,'outward signed linear envelope and nonnegative reference slack')
            upper.append(L-G);record.append([j,i,g.encode(),[x.encode() for x in vals],str(L),str(G),str(L-G)])
        E=max(upper)+F(9,4)*d*d;demand(E>0,'positive full original receiving support envelope')
        eta.append(E)
        details.append(dict(facet=j,reference_tied_originals=ties,
            maximizing_original_index=max(range(60),key=lambda i:upper[i]),support_error_upper=str(E)))
    demand(len(record)==720,'all12 facets and all60 receiving originals including tied noncorners')
    return eta,dict(original_reference_supports=720,whole_original_envelopes=720,
        signed_receiving_polygon_corner_bounds=4320,all12_receiving_facets=details,
        complete_envelope_sha256=digest(record),actual_receiving_hull_combinatorics_presumed=False)

def coefficients(H,n,adjusted,r,eta,quadratic):
    demand(len(H)==len(eta)==NR and len(adjusted)==NS*K,'all physical facets and original corner groups')
    coords=source_coordinates(adjusted,r);raw=facet_coefficients(H,n,coords)
    demand(len(raw)==NR*NS*K,'all12 facets times16 original sources times4 source corners')
    lifted=[(A,D,h+Interval(eta[i//(NS*K)]+quadratic,eta[i//(NS*K)]+quadratic))
        for i,(A,D,h) in enumerate(raw)]
    return lifted,coords

def replay(leaves,coeff,safety=SAFETY,audit=None):
    demand(safety>0 and len(coeff)==NR*NS*K,'positive margin and every original/corner coefficient')
    nodes=coupled.validate_closed_tree(leaves,NR*NS)
    quarters=[coupled.beta.quarter_coefficients(coeff,q) for q in range(4)]
    records=[];direct=[]
    for q,word,index in leaves:
        demand(len(word)<=DEPTH,'fixed certificate depth')
        lo,hi=coupled.dyadic_interval(word);coupled.beta.verify_bernstein_identity(lo,hi)
        for s in range(K):
            c=quarters[q][index*K+s];vals=coupled.beta.lower_coefficients(c,lo,hi,safety)
            demand(min(vals)>0,'ALL FOUR corners for SAME original vertex/facet on full closed leaf')
            records.append([q,word,index,s,str(lo),str(hi),[str(v) for v in vals]])
            if audit is not None:
                H,n,coords,eta,quadratic=audit;j,i=divmod(index,NS)
                mu=cross(subtract(H[(j+1)%NR],H[j]),n);MU=root(dot(mu,mu));NN=root(dot(n,n))
                e2=cross(n,(Q(1),ZERO,ZERO))
                mx=field(mu[0]).divide_positive(MU);my=field(dot(mu,e2)).divide_positive(NN).divide_positive(MU)
                h=field(dot(mu,H[j])).divide_positive(MU);px,py=coords[i*K+s]
                for t in (lo,(lo+hi)/2,hi):
                    co,se=(1-t*t)/(1+t*t),2*t/(1+t*t)
                    for _ in range(q):co,se=-se,co
                    rx=px.scale(co)-py.scale(se);ry=px.scale(se)+py.scale(co)
                    physical=mx*rx+my*ry
                    algebra=coeff[index*K+s][0].scale(co)+coeff[index*K+s][1].scale(se)
                    demand(physical.lo<=algebra.hi and algebra.lo<=physical.hi,'direct proper planar vector interface')
                    gap=physical.lo-h.hi-eta[j]-quadratic-safety
                    demand(gap>0,'direct physical auxiliary vector support margin')
                    direct.append([q,word,index,s,str(t),str(gap)])
    return dict(complete_closed_quarter_roots=4,tree_nodes=nodes,closed_leaves=len(leaves),
        maximum_depth=max(len(w) for _,w,_ in leaves),same_original_source_corner_gates=len(records),
        strict_Bernstein_coefficients=3*len(records),
        minimum_selected_Bernstein_lower=str(min(F(x) for row in records for x in row[-1])),
        complete_Bernstein_record_sha256=digest(records),direct_vector_audits=len(direct),
        direct_vector_audit_sha256=digest(direct),strict_physical_support_margin=str(safety),
        full_proper_roll_closed_seams_and_cutoff_boundary_included=True)

def reject(name,call,rows):
    try:call()
    except (ValueError,AssertionError):rows.append(name);return
    raise ValueError('malformed control accepted: '+name)

def check():
    axial.ROOT_RECORDS.clear();V=vertices();axial.validate_body(V)
    scalar,dT,dW=previous.scalar_bridge();quad=F(9,4)*dT*dT
    axial.exact_root('reverse40_sqrt5',Q(5))
    receiving,r,H,preimages=gamma83.source_geometry(V)
    demand(r==B and len(H)==NR,'actual full winning receiving reference')
    activeW,_=axial.winning_geometry(V);activeT=[axial.threshold_geometry(r,V) for r in REFS]
    orbits=axial.orbit_certificate(V,B)
    domain,UB,poly,argsB=previous.outer_polygon('reverse40_winning',B,V,dW,F(27,25),6)
    oldexpected=json.loads((PREV/'expected.json').read_bytes())
    demand(domain['ordered_actual_raw_polygon']==oldexpected['necessary_source_height_polygon']['ordered_actual_raw_polygon'],
        'same previously proved winning necessary height polygon with new receiving role')
    eta,envelope=receiving_envelope(B,V,H,UB,dW)
    cases=[];saved=[];source_data=[]
    for j,r in enumerate(REFS):
        source_domain,U,polyS,argsS=previous.outer_polygon('reverse40_threshold'+str(j),r,V,dT,F(17,16),4)
        demand(source_domain['ordered_actual_raw_polygon']==oldexpected['both_complete_original_receiving_cases'][j]
            ['necessary_receiving_height_polygon']['ordered_actual_raw_polygon'],
            'same previously proved threshold height polygon with new original SOURCE role')
        HS,originals,geo=original_source_geometry(r,V)
        adjusted,assoc=adjusted_points(r,HS,originals,U)
        coeff,coords=coefficients(H,B,adjusted,r,eta,quad)
        leaves=INPUTS['both_closed_roll_covers'][j]
        roll=replay(leaves,coeff,audit=(H,B,coords,eta,quad))
        cases.append(dict(class_index=j,actual_raw_source_reference=encode(r),original_source_geometry=geo,
            necessary_source_height_polygon=source_domain,source_original_corner_adjustments=assoc,
            all768_physical_interval_coefficient_sha256=digest([[[str(i.lo),str(i.hi)] for i in row] for row in coeff]),
            complete_closed_proper_roll_cover=roll))
        saved.append((leaves,coeff));source_data.append((r,HS,originals,U,polyS,argsS,adjusted))
    demand([c['complete_closed_proper_roll_cover']['closed_leaves'] for c in cases]==[26,26],
        'both fixed complete closed original source covers')
    example=(Q(F(21,500)),B[1],B[2]);example_sq=min(dot(v,example)**2/dot(example,example) for v in V)
    demand(all(dot(v,example)*dot(v,B)>ZERO for v in V) and
        Q(Q0*Q0)<=example_sq<Q(F(83,200)**2), 'actual original winning receiver in new height band')
    roots=copy.deepcopy(axial.ROOT_RECORDS);rejected=[];leaves,coeff=saved[0]
    r,HS,originals,U,polyS,argsS,adjusted=source_data[0]
    corrupt=copy.deepcopy(DEPS['files']);corrupt[-1]['sha256']='0'*64
    lower=copy.deepcopy(INPUTS);lower['receiving_cutoff']='399/1000'
    swapped=copy.deepcopy(INPUTS);swapped['actual_raw_source_references'][0]=encode(B)
    missing=copy.deepcopy(INPUTS);missing['both_closed_roll_covers']=missing['both_closed_roll_covers'][:1]
    bad_index=copy.deepcopy(leaves);bad_index[0][2]=NR*NS
    bad_originals=list(originals);bad_originals[0]=originals[1]
    bad_adj=list(adjusted);bad_adj[0]=tuple(adjusted[0][i]+Q(int(i==0)) for i in range(3))
    lo,a,b=argsS;bad_poly=list(polyS);bad_poly[0]=(Q(100),Q(100))
    reject('missing_prior_input_pin',lambda:validate_pins(DEPS['files'][:-1],False),rejected)
    reject('incorrect_prior_input_bytes',lambda:validate_pins(corrupt,False),rejected)
    reject('missing_original_vertex',lambda:axial.validate_body(V-{min(V)}),rejected)
    reject('unsupported_receiving_cutoff',lambda:validate_input(lower),rejected)
    reject('interchanged_actual_source_and_receiver',lambda:validate_input(swapped),rejected)
    reject('missing_source_class',lambda:validate_input(missing),rejected)
    wrong_facets=copy.deepcopy(INPUTS);wrong_facets['receiving_original_facets']=16
    reject('wrong_actual_winning_receiving_facet_count',lambda:validate_input(wrong_facets),rejected)
    reject('unsupported_new_scalar_cutoff',lambda:previous.scalar_bridge(F(399,1000)),rejected)
    reject('missing_original_source_preimage',lambda:original_source_geometry(r,V,originals[:-1]),rejected)
    reject('incorrect_same_original_source_preimage',lambda:original_source_geometry(r,V,bad_originals),rejected)
    reject('noncircle_source_heights_assumed_beta',lambda:original_source_geometry(r,V,claimed_common_height=axial.BETA),rejected)
    reject('missing_original_source_polygon_corner',lambda:previous.validate_polygon(polyS[:-1],r,V,lo,a,b,4),rejected)
    reject('outside_necessary_original_height_domain',lambda:previous.validate_polygon(bad_poly,r,V,lo,a,b,4),rejected)
    reject('reversed_polygon_orientation',lambda:previous.validate_polygon(list(reversed(polyS)),r,V,lo,a,b,4),rejected)
    reject('incorrect_signed_original_adjustment',lambda:adjusted_points(r,HS,originals,U,bad_adj),rejected)
    reject('missing_same_original_corner_group',lambda:replay(leaves,coeff[:-1]),rejected)
    reject('missing_closed_circle_quarter',lambda:replay([row for row in leaves if row[0]!=3],coeff),rejected)
    reject('missing_closed_roll_leaf',lambda:replay(leaves[:-1],coeff),rejected)
    reject('duplicate_closed_roll_leaf',lambda:replay(leaves+[leaves[0]],coeff),rejected)
    reject('invalid_original_facet_vertex_witness',lambda:replay(bad_index,coeff),rejected)
    reject('overlapping_leaf_and_child',lambda:replay(leaves+[[leaves[0][0],leaves[0][1]+'0',leaves[0][2]]],coeff),rejected)
    reject('false_support_margin',lambda:replay(leaves,coeff,F(100)),rejected)
    reject('nonpositive_support_margin',lambda:replay(leaves,coeff,F(0)),rejected)
    demand(len(rejected)==23,'all23 rejection controls')
    totals=dict(original_vertices=60,proper_body_rotations=60,directed_original_sign_regions=140,
        original_source_hull_preimages=32,original_source_hull_supports=1920,
        original_receiving_reference_facets=12,original_receiving_reference_supports=720,
        original_height_halfplanes_clipped=180,original_height_polygon_corner_gates=840,
        whole_original_receiving_envelopes=720,signed_receiving_polygon_corner_bounds=4320,
        signed_same_original_source_corner_adjustments=128,physical_interval_coefficient_triples=1536,
        closed_roll_leaves=52,same_original_corner_leaf_gates=208,strict_Bernstein_coefficients=624,
        direct_planar_vector_audits=624,outward_root_records=len(roots),malformed_controls=23)
    return dict(agent='six-rupert-3',role='researcher',proof_status='complete_written_unformalized_author_checked',
        independently_reviewed=False,global_RID_status='OPEN',receiving_cutoff='2/5',
        conditional_closed_exclusion='either original threshold source class into any original winning receiving region',
        all_proper_original_Q_full_roll_physical_planar_t_lambda_ge1_included=True,
        all_mixed_branches_at2over5_closed_excluded_with_previous=True,
        threshold_to_threshold_strict_exclusion_at2over5_inherited=True,
        remaining2over5_branch='winning sources into winning receivers',winning_to_winning_at2over5_proved=False,
        global_receiving_cutoff='83/200 unchanged',global_squared_height_gap='1/28 unchanged',
        global_cutoff_improved=False,all73_previous_inputs_unchanged=True,fixed_dependency_manifest_sha256=DEPENDENCY_SHA,
        all60_original_vertices=[encode(v) for v in sorted(V)],winning_original_receiving_reference_geometry=receiving,
        fresh_original_height_scalar_bridge=scalar,necessary_original_receiving_height_polygon=domain,
        all12_original_receiving_support_errors=[str(x) for x in eta],whole_original_receiving_envelope=envelope,
        winning_active_original_tangent_geometry_sha256=digest(activeW),
        both_threshold_active_original_tangent_geometry_sha256=[digest(x) for x in activeT],
        actual_proper_original_gauge_certificate=orbits,both_complete_original_source_cases=cases,
        actual_new_band_winning_receiver=dict(raw_normal=encode(example),minimum_squared_original_height=example_sq.encode(),
            all60_strict_winning_reference_signs_checked=True,q_squared_at_most_height_squared_below_old83over200_squared=True),
        complete_outward_positive_root_records=roots,outward_root_record_sha256=digest(roots),
        previous436region_global_cayley_or_majorization_proofs_replayed=False,
        exact_totals=totals,all_malformed_controls_rejected=rejected,continuous_proof='PROOF.md')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--emit',action='store_true');a=p.parse_args()
    result=check();raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
    if a.emit:(HERE/'expected.json').write_bytes(raw)
    else:demand(raw==(HERE/'expected.json').read_bytes(),'every compact expected byte must match')
    print(json.dumps(dict(status='generated' if a.emit else 'verified_every_expected_byte',bytes=len(raw),
        sha256=hashlib.sha256(raw).hexdigest(),receiving_cutoff='2/5',closed_roll_leaves=52,
        strict_Bernstein_coefficients=624,direct_vector_audits=624,malformed_controls_rejected=23,
        global_RID='OPEN',global_cutoff_improved=False),sort_keys=True))

if __name__=='__main__':main()
