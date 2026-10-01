"""Exact domain transfer across a shared J77 original-contact cone.

six-rupert-2, researcher. Python3.11+ standard library, positive Q(sqrt5).
Complete written continuous intermediate proof: PROOF.md.
Unformalized, independently unreviewed; global J77 remains OPEN.
"""
import argparse
import copy
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
def require(ok,message):
    if not ok:raise ValueError(message)
PARENT='convex_geometry/rupert_j77_three_sector_closed_cap'
COMMIT='9c44a91c07371a24b7225a6f1e6a7003b323ddf7'
manifest=json.loads((HERE/'dependencies.json').read_text())
require(len(manifest)==1,'one complete exact parent')
dep=manifest[0]
require(set(dep)=={'source_directory','source_commit','sha256'} and dep['source_directory']==PARENT and dep['source_commit']==COMMIT and set(dep['sha256'])=={'.gitignore','README.md','PROOF.md','verify.py','certificates.json','dependencies.json','expected.json'},'all seven direct-parent source pins')
for name,digest in dep['sha256'].items():require(sha256((REPO/PARENT/name).read_bytes()).hexdigest()==digest,'changed complete parent '+name)
spec=importlib.util.spec_from_file_location('j77_shared_contact_exact_parent',REPO/PARENT/'verify.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
P,A,R,Q=S.P,S.A,S.R,S.Q;M,PB,V=S.M,S.PB,S.V
dot,cross,add,sub,scale=S.dot,S.cross,S.add,S.sub,S.scale
sg,pos,nonneg,enc,decode=S.sg,S.pos,S.nonneg,S.enc,S.decode
D,CR,AMIN,E,THETA,L0=S.D,S.CR,S.AMIN,S.E,S.THETA,S.L0
e=(Q(1),Q(),Q())
def gate(x,label):pos(Q(x),label);return x
RAW=[[['1', '0'], ['0', '0'], ['0', '0']], [['1', '0'], ['-3/100', '1/100'], ['1/100', '-1/100']], [['1', '0'], ['-1/100', '-1/500'], ['-1/100', '1/500']]]
SEAM=[['0','0'],['-31/38','5/38'],['-7/38','-5/38']]
def configuration(data):
    require(set(data)=={'agent','role','closed_receiving_sectors','new_shared_receiving_sectors','physical_chord_upper','outer_coefficient_sum','raw_outer_triangle','actual_seam_ray'},'complete shared-cone certificate grammar')
    require(data['agent']=='six-rupert-2' and data['role']=='researcher' and data['closed_receiving_sectors']==[23,28,31,30] and data['new_shared_receiving_sectors']==[31,30],'actual author and complete four-sector union')
    require(data['physical_chord_upper']=='1/200' and data['outer_coefficient_sum']=='1/50' and data['raw_outer_triangle']==RAW and data['actual_seam_ray']==SEAM,'entire stated closed physical cone and original seam')
    require((D,CR,AMIN,E,THETA,L0)==(F(1,200),F(1001,1000),F(7,10),F(377,10000),F(207,20),F(259,50)),'same verified constants, no parent guard modified')
    return tuple(tuple(Q(*map(F,q)) for q in row) for row in RAW)

def geometry(raw):
    V,core,axis,lift,integer_vertices=A.originals()
    require(tuple(V)==tuple(P.V),'identical actual original55 vertices')
    d0=(Q(),Q(F(-3,2),F(1,2)),Q(F(1,2),F(-1,2)));d1=(Q(),Q(F(-1,2),F(-1,10)),Q(F(-1,2),F(1,10)))
    require(raw==(e,add(e,scale(Q(1)/50,d0)),add(e,scale(Q(1)/50,d1))),'actual receiver rays and enclosing triangle')
    difference=sub(d1,d0);den=dot(difference,difference);gate(den,'distinct actual receiving rays')
    parameter=-dot(d0,difference)/den
    candidates=[dot(d,d) for d in (d0,d1)]
    if sg(parameter)>=0 and sg(1-parameter)>=0:
        point=add(d0,scale(parameter,difference));candidates.append(dot(point,point))
    for value in candidates:gate(value-AMIN*AMIN,'whole actual receiving ray segment norm above7over10')
    for ray in (d0,d1):nonneg(1-dot(ray,ray),'actual receiving rays have norm at most1')
    gates={'physical_to_raw_ratio':CR*(1-D*D/2)-1,
           'entire_sector_outer_coefficient_sum':4*AMIN-CR,
           'strict_outer_triangle_enclosure':F(1,50)*AMIN-CR*D,
           'raw_radius_inside_parent_stress_domain':Q(P.CR*P.D)-Q(CR*D)}
    # Equality of the two raw-ball budgets, never an extrapolation.
    require(gates.pop('raw_radius_inside_parent_stress_domain')==0,'same certified receiving stress radius')
    for name,value in gates.items():gate(value,name)
    facets,generators,counts,edges,rank=A.all_facets(V,lift,integer_vertices)
    middle=scale(Q(1)/3,tuple(sum((u[j] for u in raw),Q()) for j in range(3)))
    signs=[];fan=[]
    for record in facets:
        vector=record['area_vector'];sign=sg(dot(vector,middle))
        require(sign!=0,'generic sector interior not on original physical area wall')
        corners=[sign*dot(vector,u) for u in raw]
        for value in corners:nonneg(value,'entire outer triangle in one closed actual physical area cell')
        signs.append(sign);fan.append(corners)
    C=scale(Q(1)/2,tuple(sum((row['area_vector'][j]*sign for row,sign in zip(facets,signs)),Q()) for j in range(3)))
    require(C==(Q(49,25)/8,Q(-25)/8-Q(0,F(47,40)),Q(-3)/2-Q(0,F(17,20))),'fresh physical area vector')
    for u in raw:gate(dot(C,u),'physical area numerator positive on entire outer triangle')
    # Independent area reconstruction from the actual perturbed shadow hull.
    f1=(-middle[1],Q(1),Q());f2=(-middle[2],Q(),Q(1))
    require(cross(f1,f2)==middle,'actual positive projection chart')
    labels={}
    for j,v in enumerate(V):labels.setdefault((dot(f1,v),dot(f2,v)),j)
    points=sorted(labels)
    def hull_chain(items):
        out=[]
        for point in items:
            while len(out)>=2:
                a,b=out[-2:]
                turn=(b[0]-a[0])*(point[1]-a[1])-(b[1]-a[1])*(point[0]-a[0])
                if sg(turn)>0:break
                out.pop()
            out.append(point)
        return out
    hull=hull_chain(points)[:-1]+hull_chain(list(reversed(points)))[:-1]
    ids=[labels[point] for point in hull];cycle=list(zip(ids,ids[1:]+ids[:1]))
    C2=scale(Q(1)/2,tuple(sum((cross(V[a],V[b])[j] for a,b in cycle),Q()) for j in range(3)))
    require(C2==C,'actual original shadow cycle and Cauchy physical area agree')
    support_count=0
    for a,b in cycle:
        for u in raw:
            normal=cross(sub(V[b],V[a]),u)
            for v in V:
                nonneg(dot(normal,sub(V[a],v)),'every original receiving support on complete outer triangle')
                support_count+=1
    require(d1==(Q(),Q(F(-1,2),F(-1,10)),Q(F(-1,2),F(1,10))),'actual shared closed wall with old receiving-sector28')
    return {'raw_outer_triangle':raw,'actual_receiver_rays':[d0,d1],
        'entire_receiving_segment_norm_squared_candidates':candidates,'segment_stationary_parameter':parameter,
        'whole_sector_enclosure_gates':gates,'complete_original_facets':len(facets),
        'original_hull_counts':dict(counts),'area_fan_corner_gates':fan,
        'physical_area_vector':C,'independent_actual_shadow_hull':ids,
        'complete_actual_shadow_support_comparisons':support_count},C


def seam_split(raw,data,area_record):
    d0,d1=area_record['actual_receiver_rays'];mid=tuple(Q(*map(F,q)) for q in data['actual_seam_ray'])
    weights=M.P.solve([[d0[j],d1[j]] for j in (1,2)],list(mid[1:]))
    for x in weights:gate(x,'actual shared seam strictly between the two outer rays')
    require(sum(weights,Q())==1 and add(scale(weights[0],d0),scale(weights[1],d1))==mid,'exact positive original seam convex combination')
    fan=json.loads((REPO/'convex_geometry/rupert_j77_effective_mirror_cap/expected.json').read_text())
    require(fan['fan_coverage']['ordered_parents']==[21,23,28,31,30,32,33],'actual complete pinned fan order')
    by={r['parent']:r for r in fan['stratum_records']}
    require(by[30]['receiver_rays']==enc([d0,mid]) and by[31]['receiver_rays']==enc([mid,d1]),'both complete original receiving sectors and coordinate orders')
    return {'actual_seam_ray':mid,'exact_positive_barycentric_weights':weights,'actual_fan_order':fan['fan_coverage']['ordered_parents'],'closed_sector30_rays':[d0,mid],'closed_sector31_rays':[mid,d1],'entire_shared_cone_equals_union_of_both_closed_sectors':True}

def shared_cases(a,b):
    require(a['parent']==31 and b['parent']==30,'two actual incident original sectors')
    keys=['direction','contacts','extreme_motions','common_indices','common_weights','rank_rows','rank_coordinates','facet_rows']
    for key in keys:require(a[key]==b[key],'same full original-contact interface '+key)
    require(len(a['contacts'])==32 and len(a['common_indices'])==6,'all original contacts and common sources')
    # Their historical one-dimensional dual covers differ. Those are not
    # required for this new all-source entry and signed stress argument.
    return {'identical_original_fields':keys,'original_contacts':a['contacts'],'common_indices':a['common_indices'],'old_local_dual_covers_identical':a['dual_covers']==b['dual_covers'],'old_local_dual_covers_used':False}

def attach(old,stress,duals,chis,norms,chain,moving,contacts):
    require(enc(stress)==old['fresh_receiving_stress'],'EVERY fresh original receiving stress field identical; whole raw-ball bounds retained')
    require(enc(duals)==old['fresh_positive_coordinate_stresses'],'EVERY actual signed coordinate moment and universal identity identical')
    require(enc(chis)==old['coordinate_covector_norms'] and enc(norms)==old['direct_own_row_norms'],'both unchanged Euclidean bounds')
    require(enc(chain)==old['directed_signed_chain'],'EVERY full coupled inverse/bootstrap/signed corner field identical')
    require(enc(moving)==old['fresh_moving_and_same_gauge'],'EVERY moving source entry and actual companion gauge field identical')
    require(enc(contacts['original_contacts'])==old['fresh_original_contact_geometry']['original_contacts'] and enc(contacts['actual_motion_rays'])==old['fresh_original_contact_geometry']['actual_motion_rays'],'same actual ordered original supports and motion rays')
    return {'receiving_stress_sha256':S.digest(stress),'signed_coordinate_moments_sha256':S.digest(duals),'five_stage_signed_chain_sha256':S.digest(chain),'all_source_entry_sha256':S.digest(moving),'every_named_parent_interface_field_exactly_identical':True,'raw_ball_receiver_chord_budget':'1001/200000','five_stage_signed_contradiction_gap':'3157942313279/323680000000000'}

def malformed(data,a,b,old,stress,duals,chis,norms,chain,moving,contacts):
    tests=[]
    for field in ['radius','coverage','triangle','endpoint','seam','coefficient','role']:
        bad=copy.deepcopy(data)
        if field=='radius':bad['physical_chord_upper']='1/100'
        elif field=='coverage':bad['closed_receiving_sectors'].pop()
        elif field=='triangle':bad['raw_outer_triangle'].pop()
        elif field=='endpoint':bad['raw_outer_triangle'][1][1]=['1/50','0']
        elif field=='seam':bad['actual_seam_ray'][1]=['1','0']
        elif field=='coefficient':bad['outer_coefficient_sum']='1/10'
        else:bad['role']='reviewer'
        tests.append(lambda bad=bad:configuration(bad))
    for field in ['contact','motion','common']:
        bad=copy.deepcopy(b)
        if field=='contact':bad['contacts'][0][2]=55
        elif field=='motion':bad['extreme_motions'].reverse()
        else:bad['common_indices'].pop()
        tests.append(lambda bad=bad:shared_cases(a,bad))
    for field in ['receiving','moment']:
        bad=copy.deepcopy(old)
        if field=='receiving':bad['fresh_receiving_stress']['critical_corners'][0][1]=['-1','0']
        else:bad['fresh_positive_coordinate_stresses'][0]['b'][0]=['0','0']
        tests.append(lambda bad=bad:attach(bad,stress,duals,chis,norms,chain,moving,contacts))
    for test in tests:
        try:test()
        except (ValueError,KeyError,IndexError,TypeError,ZeroDivisionError):continue
        raise ValueError('Malformed shared original-contact cone certificate accepted')
    return len(tests)

def parent_interface():
    # This exact public interface is a theorem dependency. Its complete
    # replay is a separate required command, not a private receipt input.
    old_bytes=(REPO/PARENT/'expected.json').read_bytes()
    old=json.loads(old_bytes)
    require((json.dumps(old,indent=1)+'\n').encode()==old_bytes,'canonical complete pinned parent interface')
    require(old['whole_closed_receiving_sectors']==[23,28,31] and old['new_closed_sector31_strict_passage_excluded'] and old['all_original_sources_full_roll_arbitrary_physical_translation_scale_ge1'],'all three old entire closed branches and quantifiers retained')
    require(len(old_bytes)==73789 and sha256(old_bytes).hexdigest()==dep['sha256']['expected.json'],'complete public parent expected bytes pinned')
    return old,old_bytes

def check_parent():
    # All original parent branches, recursive prerequisites and malformed
    # controls are replayed unchanged in this bounded mathematical job.
    computed=S.check(True)
    computed_bytes=(json.dumps(computed,indent=1)+'\n').encode()
    old,old_bytes=parent_interface()
    require(computed_bytes==old_bytes,'EVERY complete direct-parent byte replayed')
    require(computed['malformed_controls']==33,'all direct-parent malformed controls retained')
    return {'agent':'six-rupert-2','role':'researcher','phase':'complete_parent_replay',
        'source_directory':PARENT,'source_commit':COMMIT,'expected_bytes':len(old_bytes),
        'expected_sha256':sha256(old_bytes).hexdigest(),'every_parent_expected_byte_matched':True,
        'all_recursive_parent_proof_obligations_replayed':True,'parent_malformed_controls':33,
        'closed_parent_sectors':old['whole_closed_receiving_sectors'],
        'new_domain_checked_in_this_job':False,'private_receipt_required_by_new_domain':False}

def check(self_test):
    # Run --parent separately before crediting the complete extension.
    # Read only the byte-pinned public theorem interface in this domain job.
    old,old_bytes=parent_interface()
    data=json.loads((HERE/'certificates.json').read_text());raw=configuration(data)
    area_record,C=geometry(raw);split=seam_split(raw,data,area_record)
    source=json.loads((REPO/'convex_geometry/rupert_j77_uniform_local_exclusion/certificates.json').read_text())['cases']
    a=next(r for r in source if r['parent']==31);b=next(r for r in source if r['parent']==30);shared=shared_cases(a,b)
    index={v:i for i,v in enumerate(V)};permutation=[index[M.rotate(v)] for v in V]
    pinned=json.loads((REPO/PARENT/'certificates.json').read_text())
    stress=S.receiving_stress(b,pinned['receiving_common_stress'],permutation)
    duals,chis,norms,contacts=S.fresh_geometry(b,permutation,raw,stress,pinned)
    expected_slacks=[[Q(),Q(),Q(1)/50],[Q(),Q(1)/50,Q()]]
    require(contacts['actual_closed_receiving_mirror_slack_corners']==expected_slacks,'both original mirror-root slacks on whole shared cone')
    chain=S.chain(pinned,duals,chis,norms,stress)
    near=[dict(row,**{key:Q(*map(F,row[key])) for key in ['physical_contact_height','norm_upper','directed_torque']}) for row in old['fresh_complete_O2_roll_cover']['signed_near_records']]
    moving=S.moving_and_gauge(C,near)
    attached=attach(old,stress,duals,chis,norms,chain,moving,contacts)
    controls=malformed(data,a,b,old,stress,duals,chis,norms,chain,moving,contacts) if self_test else 0
    for registry in [M.area,P.C.A]:
        for pair,sign in tuple(registry.SIGNS.items()):require(registry.interval_sign(pair)==sign,'independent positive-sqrt5 rational sign enclosure')
    return enc({'agent':'six-rupert-2','role':'researcher','target':'original asymmetric55vertex unit-edge J77','proof_status':'continuous domain-transfer theorem depends on the separately replayed complete public parent; unformalized','independent_review_asserted':False,'global_J77_Rupert_resolved':False,'whole_closed_receiving_sectors':[23,28,31,30],'physical_chord_upper':'1/200','entire_closed_shared_contact_cone_30_31_proved_given_parent':True,'new_closed_sector30_strict_passage_excluded_given_parent':True,'all_original_sources_full_roll_arbitrary_physical_translation_scale_ge1':True,'closed_classification':'lambda1,t0,Qh=I or M_nM_q; actual RIGHT C5 body factor; both equal shadows','whole_one_over200_mirror_cap_proved':False,'complete_direct_parent_replay_in_this_job':False,'full_parent_reproduction_required_separately':True,'complete_pinned_direct_parent_interface':{'directory':PARENT,'commit':COMMIT,'bytes':len(old_bytes),'sha256':sha256(old_bytes).hexdigest()},'whole_shared_cone_geometry':area_record,'actual_seam_and_complete_sector_split':split,'same_actual_original_case_interface':shared,'fresh_entire_shared_cone_original_contact_geometry':contacts,'exact_parent_hypothesis_attachment':attached,'final_signed_gap':chain['final_positive_gap'],'malformed_controls':controls,'fixture_sha256':S.digest(data),'registered_independent_sign_counts_by_parent_registry':[len(M.area.SIGNS),len(P.C.A.SIGNS)],'remaining_frontier':'three primitive receiving sectors21,32,33, complete larger mirror cap and global J77 remain OPEN'})
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--parent',action='store_true',help='separate complete pinned parent replay, including all controls');p.add_argument('--self-test',action='store_true');p.add_argument('--emit',action='store_true');args=p.parse_args()
    require(not (args.parent and args.emit),'parent replay emits its own receipt and cannot build domain expected bytes')
    output=(json.dumps(check_parent() if args.parent else check(args.self_test),indent=1)+'\n').encode()
    if not args.parent and not args.emit:require(output==(HERE/'expected.json').read_bytes(),'EVERY domain expected byte; use --self-test and separately run --parent')
    print(output.decode(),end='')
