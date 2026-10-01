#!/usr/bin/env python3
"""Exact finite hypotheses of PROOF.md; Python3.11+ standard library.

Fresh q=2/5 threshold matching, original-height clipping and fixed signed
Cayley covers. Reuses pinned author kernels; not an independent review.
No old cutoff, guard or module global is changed. No adaptive public search.
"""
import argparse,copy,hashlib,itertools,json,re,sys
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'rhombicosidodecahedron_mirror_cluster_obstruction'
DEPENDENCY_SHA='e069c0b8d8bcaafa0a75aee9d7ec0e2e4c1c7711ef5744439e9d43175b5191f3'

def demand(ok,message):
    if not ok:raise ValueError(message)

DEPS_RAW=(HERE/'dependencies.json').read_bytes()
demand(hashlib.sha256(DEPS_RAW).hexdigest()==DEPENDENCY_SHA,'fixed complete dependency manifest')
DEPS=json.loads(DEPS_RAW)

def validate_pins(rows,check_files=True):
    demand(rows==DEPS['files'] and len(rows)==65 and len({r['file'] for r in rows})==65,
        'all65 fixed distinct previously published mathematical inputs')
    for r in rows:
        demand(set(r)=={'file','bytes','sha256'},'exact input pin schema')
        p=Path(r['file'])
        demand(len(p.parts)==2 and p.parts[0]==BASE.name and p.suffix in ('.py','.json'),
            'ordinary original mathematical input path')
        demand(type(r['bytes']) is int and 0<r['bytes']<1000000 and
            re.fullmatch('[0-9a-f]{64}',r['sha256']),'canonical input byte commitment')
        if check_files:
            path=HERE.parent/p
            demand(path.is_file() and not path.is_symlink(),'regular published input')
            raw=path.read_bytes()
            demand(len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'],
                'published input mismatch: '+r['file'])
validate_pins(DEPS['files'])
sys.path.insert(0,str(BASE))
from verify import QPhi as Q,PHI,ZERO,act,dot,vertices,symmetry_group
from cell_certificate import encode,decode
from torque_certificate import cross,subtract
from linear_roll_certificate import project
from contact_collar_certificate import complete_contacts
from threshold_receiver_certificate import I
from global_band83_certificate import neg,canonical,digest
import axial_majorization_certificate as axial
import coupled_nonwinning_certificate as coupled
import weighted_global_band_certificate as weighted
import threshold_cayley_certificate as tc
import global_band83_certificate as parent

Q0=F(2,5);CANDIDATE40=F(9,20);MATCH40=F(13,25)
THETA=F(47,400);RADIUS=F(59,1000);DEPTH=5
REFS=((ZERO,(2-PHI)/3,Q(-1)),(ZERO,Q(1),(3*PHI-1)/11))
INPUTS=json.loads((HERE/'certificates.json').read_bytes())

def validate_input(data):
    demand(isinstance(data,dict) and set(data)=={'schema','receiving_cutoff','candidate_distance',
        'reference_match_buffer','full_angle_bound','Cayley_radius','max_cover_depth',
        'actual_raw_references','both_clipped_polygon_signed_covers'},'exact fresh certificate schema')
    expected={'schema':'rid-threshold40-clipped-signed-covers-v1','receiving_cutoff':'2/5',
        'candidate_distance':'9/20','reference_match_buffer':'13/25','full_angle_bound':'47/400',
        'Cayley_radius':'59/1000','max_cover_depth':5}
    demand(all(data.get(k)==v and type(data.get(k)) is type(v) for k,v in expected.items()),
        'fixed new theorem constants and domain')
    demand(data['actual_raw_references']==[encode(r) for r in REFS],
        'both actual raw normalizations, not merely proportional rays')
    covers=data['both_clipped_polygon_signed_covers']
    demand(isinstance(covers,list) and len(covers)==2,'both receiving classes')
    for rows in covers:parent.validate_covers(rows,16,DEPTH)
validate_input(INPUTS)

def phase():
    cL,cU=axial.exact_root('threshold40_height',axial.BETA)
    rhoL,rhoU=axial.exact_root('threshold40_active_disk',(39+37*PHI)/29)
    s=(cU-Q0)/rhoL
    demand(0<s<1,'positive original regional tangent bound')
    zL,zU=axial.exact_root('threshold40_cosine',Q(1-s*s))
    d=F(1001,1000)*s;eta=cU*d+F(9,4)*d*d
    candidate2=axial.BETA-Q(Q0*Q0)+Q(9*eta)
    height2=axial.BETA+Q(9*eta)
    hL,hU=axial.exact_root('threshold40_candidate_height',height2)
    lx,lt=(49+45*PHI)/29,(135+195*PHI)/29
    chord=F(94,25)*d
    gates=dict(actual_regional_chord_conversion=F(1001,1000)**2*(1+zL)>2,
        all_original_reference_signs_persist_on_caps=cL>F(9,2)*d,
        actual_original_candidate_distance=candidate2<Q(CANDIDATE40**2),
        eight_original_candidates_distinct=F(3,2)-2*eta>2*CANDIDATE40,
        proper_circle_arcs_disjoint=2*MATCH40<F(3,2),
        reviewer94over25_full_moment_constant=Q(F(94,25)**2)*(axial.BETA+lx)>4*lt,
        full_spatial_chord_below13over100=chord<F(13,100),
        inverse_sine_derivative_on_whole_domain=F(101,100)**2*(1-F(13,200)**2)>1,
        actual_full_spatial_angle=F(101,100)*chord<THETA,
        actual_angle_to_Cayley_radius=RADIUS*(1-THETA**2/8)-THETA/2>0,
        body_radius_bound=7+8*PHI<Q(F(9,2)**2))
    demand(all(gates.values()),'fresh q2/5 scalar bridge unsupported')
    return dict(q=str(Q0),both_original_normal_chords_upper=str(d),
        source_circle_transport_upper=str(eta),original_candidate_squared_distance_upper=candidate2.encode(),
        original_candidate_distance_upper=str(CANDIDATE40),candidate_squared_height_upper=height2.encode(),
        outward_candidate_height=[str(hL),str(hU)],full_original_moment_coefficient='94/25',
        full_spatial_chord_upper=str(chord),full_spatial_angle_upper=str(THETA),
        actual_Cayley_radius_upper=str(RADIUS),all11_exact_scalar_gates=gates,
        metric26over25_and_moment94over25_credited_to_review8346=True),d,eta,hU

def height_polygon(j,r,V,d):
    lo,hi=axial.exact_root('threshold40_raw_norm'+str(j),dot(r,r))
    z=1-d*d/2;a,b=F(17,16)*d/z,d/z;tangent=(ZERO,-r[2],r[1])
    demand(z>0 and dot(r,r)<Q(F(17,16)**2),'raw cap normalization')
    poly=[(Q(-a),Q(-b)),(Q(a),Q(-b)),(Q(a),Q(b)),(Q(-a),Q(b))]
    original_cuts=[]
    for v in sorted(V):
        h=dot(v,r);demand(h!=ZERO,'nonzero original reference height');sg=1 if h>ZERO else -1
        A,B,C=sg*v[0],sg*dot(v,tangent),sg*h-Q(Q0*lo)
        def val(p):return A*p[0]+B*p[1]+C
        demand(C>ZERO,'regional center strictly inside every necessary halfplane')
        clipped=[]
        for u,w in zip(poly,poly[1:]+poly[:1]):
            hu,hw=val(u),val(w)
            if hu>=ZERO:clipped.append(u)
            if (hu<ZERO<hw) or (hw<ZERO<hu):
                t=hu/(hu-hw);demand(ZERO<t<Q(1),'exact crossing parameter')
                p=tuple(u[k]+t*(w[k]-u[k]) for k in range(2))
                demand(val(p)==ZERO,'exact original-height boundary intersection');clipped.append(p)
        dedup=[]
        for p in clipped:
            if not dedup or p!=dedup[-1]:dedup.append(p)
        if len(dedup)>1 and dedup[0]==dedup[-1]:dedup.pop()
        demand(dedup,'nonempty complete original-height outer domain')
        if dedup!=poly:original_cuts.append(dict(original=encode(v),sign=sg,
            old_vertices=len(poly),new_vertices=len(dedup)))
        poly=dedup
    demand(len(poly)==len(set(poly))==4,'four distinct actual clipped vertices')
    def det(p,q):return p[0]*q[1]-p[1]*q[0]
    for i in range(4):
        p,q,w=poly[i],poly[(i+1)%4],poly[(i+2)%4]
        demand(det(subtract(q,p),subtract(w,q))>ZERO,'positive strict cyclic polygon turns')
        demand(det(subtract(q,p),tuple(-x for x in p))>ZERO,'raw origin strictly inside polygon')
    U=[(p[0],r[1]+p[1]*tangent[1],r[2]+p[1]*tangent[2]) for p in poly]
    gates=[]
    for p,u in zip(poly,U):
        demand(-Q(a)<=p[0]<=Q(a) and -Q(b)<=p[1]<=Q(b) and dot(r,u)==dot(r,r),
            'complete clipped domain remains in actual raw cap chart')
        for v in sorted(V):
            sg=1 if dot(v,r)>ZERO else -1;g=sg*dot(v,u)-Q(Q0*lo)
            demand(g>=ZERO,'every original height halfplane at every polygon vertex');gates.append(g.encode())
    return dict(case=j,actual_raw_reference=encode(r),raw_norm_squared=dot(r,r).encode(),
        outward_raw_norm=[str(lo),str(hi)],blanket_cap_alpha_gamma=[str(a),str(b)],
        ordered_tangent_polygon=[[x.encode() for x in p] for p in poly],
        ordered_actual_raw_polygon=[encode(u) for u in U],all60_originals_clipped=True,
        actual_clipping_cuts=original_cuts,complete_original_height_gates=len(gates),
        exact_original_height_gates_sha256=digest(gates),strict_turns_and_origin_tests=8,
        blanket_rectangle_is_not_the_new_support_domain=True),U

def reject(label,action,rejected):
    try:action()
    except (ValueError,AssertionError):rejected.append(label);return
    raise ValueError('malformed evidence accepted: '+label)

def enlargement_witnesses(V):
    rows=[]
    for j,r in enumerate(REFS):
        u=(Q(F(1,50)),r[1],r[2])
        demand(all(dot(v,u)*dot(v,r)>ZERO for v in V),'every original sign of the new receiving witness')
        f2=min(dot(v,u)**2/dot(u,u) for v in V)
        demand(Q(Q0**2)<=f2<Q(F(83,200)**2),'actual original receiver in the newly covered height band')
        rows.append(dict(case=j,actual_original_raw_receiver=encode(u),actual_minimum_squared_height=f2.encode(),
            all60_original_signs_and_heights_checked=True,below_old83over200_height_band=True,
            outside_every_preceding_geometric_exclusion_claimed=False))
    return rows

def controls(data,saved,V,d,eta,heightU):
    rejected=[]
    def change(k,value):
        out=copy.deepcopy(data);out[k]=value;return out
    for k,value,label in [('receiving_cutoff','41/100','wrong_original_cutoff'),
        ('candidate_distance','1/10','understated_original_candidate_distance'),
        ('reference_match_buffer','9/20','wrong_proved_match_buffer'),
        ('full_angle_bound','9/100','understated_full_spatial_angle'),
        ('Cayley_radius','1/22','old_Cayley_radius_substituted'),
        ('max_cover_depth',3,'old_cover_depth_substituted'),
        ('max_cover_depth',True,'boolean_cover_depth')]:
        reject(label,lambda k=k,value=value:validate_input(change(k,value)),rejected)
    reject('missing_published_input',lambda:validate_pins(DEPS['files'][:-1],False),rejected)
    wrong=copy.deepcopy(data);wrong['actual_raw_references'][0]=encode((ZERO,Q(1),-3-3*PHI))
    reject('historical_proportional_LOW_normalization',lambda:validate_input(wrong),rejected)
    wrong=copy.deepcopy(data);wrong['both_clipped_polygon_signed_covers'].pop()
    reject('missing_receiving_class',lambda:validate_input(wrong),rejected)
    wrong=copy.deepcopy(data);wrong['both_clipped_polygon_signed_covers'][0].pop()
    reject('missing_signed_axis_face',lambda:validate_input(wrong),rejected)
    wrong=copy.deepcopy(data);wrong['both_clipped_polygon_signed_covers'][0][0]['leaves'].pop()
    reject('missing_closed_axis_leaf',lambda:validate_input(wrong),rejected)
    wrong=copy.deepcopy(data);wrong['both_clipped_polygon_signed_covers'][0][0]['leaves'].append(
        wrong['both_clipped_polygon_signed_covers'][0][0]['leaves'][0])
    reject('duplicated_closed_axis_leaf',lambda:validate_input(wrong),rejected)
    bad=copy.deepcopy(data['both_clipped_polygon_signed_covers'][0][0]);bad['leaves'][0][2]='0'
    reject('understated_cube_face_norm',lambda:parent.replay(saved[0]['contacts'],bad,RADIUS,DEPTH),rejected)
    bad=copy.deepcopy(data['both_clipped_polygon_signed_covers'][0][0]);bad['leaves'][0][1]=16
    reject('nonexistent_original_contact',lambda:parent.validate_cover(bad,16,DEPTH),rejected)
    reject('wrong_mixed_Bernstein_coefficient',lambda:parent.bernstein_identities(F(1,3)),rejected)
    s=saved[1];r=s['m'];ordered=s['ordered'];originals=s['originals']
    reject('omitted_eligible_non_circle_originals',lambda:pool_filter40(1,r,V,ordered,originals,d,eta,heightU,
        pool_override=sorted(originals)),rejected)
    reject('missing_antipodal_sign_pattern',lambda:pool_filter40(1,r,V,ordered,originals,d,eta,heightU,
        patterns_override=list(itertools.product((-1,1),repeat=4))[:-1]),rejected)
    reject('understated_actual_eligible_height',lambda:pool_filter40(1,r,V,ordered,originals,d,eta,heightU,
        eligible_height_squared_override=axial.BETA),rejected)
    reject('nonpositive_original_moment_weight',lambda:weighted.moment_certificate(r,V,
        supplied_weights=[ZERO,Q(1),ZERO,ZERO]),rejected)
    probes=copy.deepcopy(s['probes']);probes[0]=((ZERO,ZERO,ZERO),probes[0][1])
    reject('nonoriginal_contact_source',lambda:tc.original_contacts(V,s['U'],probes),rejected)
    demand(len(rejected)==21,'all21 new malformed-evidence controls reject')
    return rejected

def check():
    validate_input(INPUTS);validate_pins(DEPS['files'])
    V=vertices();axial.validate_body(V);G=symmetry_group(V,return_matrices=True)
    L=((Q(1),ZERO,ZERO),(ZERO,Q(-1),ZERO),(ZERO,ZERO,Q(-1)))
    demand(L in G and all(act(L,r)==neg(r) for r in REFS),'both normal reversals are actual proper body gauges')
    axial.ROOT_RECORDS.clear();scalar,d,eta,heightU=phase();parent.bernstein_identities()
    cases=[];saved=[]
    old=json.loads((BASE/'global_band83_expected.json').read_bytes())['both_threshold_original_cases']
    for j,r in enumerate(REFS):
        original=axial.threshold_geometry(r,V)
        circle,ordered,originals,hull=coupled.circle_geometry(r,V)
        pool=pool_filter40(j,r,V,ordered,originals,d,eta,heightU)
        demand(pool['exact_original_pool_sha256']==old[j]['native_complete_candidate_pool']['exact_original_pool_sha256'],
            'fresh complete original pool equals the independently reviewed8/12 pool')
        moment,M,weights=weighted.moment_certificate(r,V);audit=weighted.moment_trace_audit(r,M)
        polygon,U=height_polygon(j,r,V,d)
        reference,probes,T,unused=complete_contacts(r,V,I)
        contacts,contact_record=tc.original_contacts(V,U,probes)
        covers=INPUTS['both_clipped_polygon_signed_covers'][j]
        faces=[parent.replay(contacts,row,RADIUS,DEPTH) for row in covers]
        cases.append(dict(case=j,complete_original_threshold_tangent_geometry_sha256=digest(original),
            original_active_tangent_disk=original['tangent_disk'],
            all60_original_heights_and28_circle_pairs_freshly_checked=True,
            complete_original_circle_geometry_sha256=digest(circle),
            original_circle_order=[encode(v) for v in originals],
            minimum_original_circle_pair_squared_distance=circle['minimum_reference_circle_pair_squared_distance'],
            all52_non_circle_reference_heights_checked=True,
            native_complete_original_candidate_pool=pool,
            original_weighted_moment=moment,used_full_moment_coefficient='94/25',
            full_original_moment_trace_audit=audit,original_height_clipped_domain=polygon,
            exact_original_polygon_vertex_contacts=contact_record,all_six_signed_axis_replays=faces))
        saved.append(dict(m=r,ordered=ordered,originals=originals,probes=probes,U=U,contacts=contacts,M=M,weights=weights))
    align=tc.proper_alignments(V,G,saved)
    roots=copy.deepcopy(axial.ROOT_RECORDS)
    enlarged=enlargement_witnesses(V)
    rejected=controls(INPUTS,saved,V,d,eta,heightU)
    return dict(agent='six-rupert-3',role='researcher',claim_status='author_checked_unformalized_conditional_theorem',
        original_named_body='standard60vertex_edge_two_RID',receiving_cutoff='2/5',
        source_and_receiver_domain='proper_body_images_of_both_original_threshold_signed_regions',
        all_original_proper_Q_rolls_planar_translations_and_scales_ge1=True,
        conclusion='strict_passage_excluded_in_all_four_threshold_to_threshold_pairings',
        centered_closed_conclusion='after_actual_body_and_LEFT_receiver_halfturn_gauges_local_rotation_is_identity',
        winning_and_mixed_branches_at2over5_proved=False,global_cutoff_improved=False,global_RID='OPEN',
        current_global_cutoff='83/200',current_global_squared_gap='1/28',
        fixed_dependency_manifest_sha256=DEPENDENCY_SHA,all65published_inputs_unchanged=True,
        direct_parent_global_or_closed_classifier_replayed=False,fresh_scalar_bridge=scalar,
        both_complete_original_threshold_cases=cases,all_four_actual_original_proper_alignments=align,
        two_actual_receiving_height_enlargement_witnesses=enlarged,
        complete_new_outward_root_records_sha256=digest(roots),complete_new_outward_roots=len(roots),
        primary_scalar_root_records={k:v for k,v in roots.items() if k.startswith('threshold40')},
        exact_totals=dict(originals=60,proper_body_rotations=60,receiving_polygon_vertices=8,
            original_height_polygon_vertex_gates=480,original_support_comparisons=7680,
            signed_displacement_identities=128,matching_assignments=6144,
            matched_non_circle_survivors=0,complete_signed_axis_leaves=sum(f['closed_leaves'] for c in cases for f in c['all_six_signed_axis_replays']),
            strict_signed_coefficients=sum(f['strict_positive_coefficients'] for c in cases for f in c['all_six_signed_axis_replays']),
            direct_vector_and_Bernstein_audits=sum(f['direct_vector_and_Bernstein_audits'] for c in cases for f in c['all_six_signed_axis_replays'])),
        actual_proper_normal_reversal_matrix=[encode(row) for row in L],
        new_malformed_controls_rejected=rejected,continuous_proof='PROOF.md',independent_review=False)

def main():
    p=argparse.ArgumentParser();p.add_argument('--emit',action='store_true');a=p.parse_args()
    raw=(json.dumps(check(),sort_keys=True,indent=2)+'\n').encode()
    if a.emit:(HERE/'expected.json').write_bytes(raw)
    else:demand(raw==(HERE/'expected.json').read_bytes(),'every complete expected byte must match')
    print(json.dumps(dict(status='generated_every_expected_byte' if a.emit else 'verified_every_expected_byte',
        bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),malformed_controls_rejected=21,
        threshold_pairings=4,global_cutoff_improved=False,global_RID='OPEN')))

# The complete pool filter below is adapted from the pinned q83 author source.
# Only fresh literal constants and an exact completeness guard differ.
def pool_filter40(j,m,V,circle,originals,cap,eta,heightU,pool_override=None,patterns_override=None,eligible_height_squared_override=None):
    eligible=sorted(v for v in V if dot(v,m)**2/dot(m,m)<=Q((heightU+F(9,2)*cap)**2))
    demand(set(originals)<=set(eligible),'all original circle candidates retained')
    if pool_override is not None:
        demand(pool_override==eligible,'complete actual original pool cannot be altered')
        eligible=pool_override
    pool=sorted({project(v,m) for v in eligible})
    demand(len(pool)==len(eligible) and all(neg(p) in pool for p in pool),
        'distinct complete antipodal eligible original projections')
    reps=sorted({canonical(p) for p in circle})
    dest=sorted({canonical(p) for p in pool})
    demand(len(reps)==4 and len(circle)==8 and len(dest)*2==len(pool),
        'four source pairs and complete destination antipodal axes')
    max2=max(dot(v,m)**2/dot(m,m) for v in eligible)
    if eligible_height_squared_override is not None:
        demand(eligible_height_squared_override>=max2,'actual complete eligible maximum height cannot be understated')
        max2=eligible_height_squared_override
    hL,hU=axial.exact_root('eligible_pool_height'+str(j),max2)
    receive_eta=hU*cap+F(9,4)*cap*cap
    flat=CANDIDATE40+eta+receive_eta
    demand(flat<MATCH40,'flat error uses actual maximum eligible NONCIRCLE height')
    tolerance=2*flat
    source=[p for v in reps for p in (v,neg(v))]
    destination=[p for v in dest for p in (v,neg(v))]
    pairkeys=list(itertools.combinations(range(8),2))
    sroots=[];droots={};root_audit=[]
    for a,b in pairkeys:
        sq=dot(subtract(source[a],source[b]),subtract(source[a],source[b]))
        lo,hi=axial.exact_root('pool_source_pair'+str(j)+'_'+str(a)+'_'+str(b),sq)
        sroots.append((lo,hi));root_audit.append(['source',a,b,sq.encode(),str(lo),str(hi)])
    for a,b in itertools.combinations(range(len(destination)),2):
        sq=dot(subtract(destination[a],destination[b]),subtract(destination[a],destination[b]))
        lo,hi=axial.exact_root('pool_dest_pair'+str(j)+'_'+str(a)+'_'+str(b),sq)
        droots[a,b]=(lo,hi);root_audit.append(['destination',a,b,sq.encode(),str(lo),str(hi)])
    patterns=list(itertools.product((-1,1),repeat=4))
    if patterns_override is not None:patterns=patterns_override
    demand(len(patterns)==16 and set(patterns)==set(itertools.product((-1,1),repeat=4)),
        'all sixteen signed antipodal choices required')
    counts=[0,0,0,0];survivors=[];record_hash=hashlib.sha256()
    for ids in itertools.permutations(range(len(dest)),4):
        for signs in patterns:
            counts[0]+=1;mapping=[]
            for i,sg in zip(ids,signs):
                offset=0 if sg==1 else 1;mapping.extend((2*i+offset,2*i+1-offset))
            failure=None
            for k,(a,b) in enumerate(pairkeys):
                p,q=sorted((mapping[a],mapping[b]));sl,su=sroots[k];dl,du=droots[p,q]
                lower=max(sl-du,dl-su)
                if lower>tolerance:failure=[a,b,p,q,str(lower)];break
            images={destination[t] for t in mapping};outside=not images<=set(circle)
            if failure is not None:counts[1]+=1
            else:
                counts[2]+=1;counts[3]+=outside
                pairs={source[i]:destination[k] for i,k in enumerate(mapping)}
                shifts=[s for s in range(8) if all(pairs[circle[i]]==circle[(i+s)%8] for i in range(8))]
                reversals=[s for s in range(8) if all(pairs[circle[i]]==circle[(s-i)%8] for i in range(8))]
                demand(outside or (len(shifts)+len(reversals)==1),
                    'each circle survivor has one verified cyclic order or reversed order')
                survivors.append(dict(destination_axes=list(ids),signs=list(signs),uses_non_circle_original=outside,
                    proper_cyclic_shifts=shifts,reversed_cyclic_offsets=reversals))
            record_hash.update(json.dumps([list(ids),list(signs),failure],separators=(',',':')).encode())
    expected=16
    for k in range(4):expected*=len(dest)-k
    demand(counts[0]==expected==counts[1]+counts[2],'complete all signed injective antipodal assignments')
    demand(counts[2]==4 and counts[3]==0,'only four circle mappings survive every finite metric test')
    proper=[s for r in survivors for s in r['proper_cyclic_shifts']]
    demand(sorted(proper)==[0,4],'the only proper circle survivors are actual shifts zero and four')
    minimum_other=min(dot(v,m)**2/dot(m,m) for v in V-set(originals))
    ol,ou=axial.exact_root('minimum_other_height'+str(j),minimum_other)
    other=ol-F(9,2)*cap
    old_separation=other>0 and Q(other*other)>axial.BETA+Q(9*eta)
    return dict(case=j,eligible_original_count=len(eligible),eligible_antipodal_axes=len(dest),
        eligible_non_circle_originals=[encode(v) for v in eligible if v not in originals],
        exact_original_pool_sha256=digest([encode(v) for v in eligible]),
        maximum_eligible_original_squared_height=max2.encode(),outward_eligible_original_height=[str(hL),str(hU)],
        actual_receiver_candidate_transport_upper=str(receive_eta),flat_proper_frame_match_upper=str(flat),
        pair_length_tolerance=str(tolerance),all_outward_pair_length_roots=len(root_audit),
        complete_pair_length_root_record_sha256=digest(root_audit),
        signed_injective_antipodal_assignments=counts[0],exact_pair_length_rejections=counts[1],
        metric_survivors=counts[2],non_circle_metric_survivors=counts[3],all_metric_survivors=survivors,
        complete_assignment_and_first_witness_sha256=record_hash.hexdigest(),
        legacy_all_non_circle_height_separation_passes=old_separation,
        proper_cyclic_surviving_shifts=[0,4],circle_originals_forced_by_COMPLETE_metric_filter=True)


if __name__=='__main__':main()
