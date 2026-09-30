#!/usr/bin/env python3
"""Exact entire north triangle, directional receiving bounds, wider source range."""
import argparse,hashlib,importlib.util,itertools,json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent.parent

def require(ok,message):
    if not ok:raise ValueError(message)

manifest=json.loads((ROOT/'dependencies.json').read_text())
require(len(manifest['sources'])==1,'Missing direct balanced parent')
parent=manifest['sources'][0]
require(parent['source_directory']=='convex_geometry/rupert_j77_balanced_torque_caps'
        and parent['source_commit']=='788a042adb636949eaf06a5825e9f439d47e48de','Wrong balanced parent')
require(set(parent['sha256'])=={'.gitignore','README.md','PROOF.md','verify.py','certificates.json','dependencies.json','expected.json'},'Incomplete direct pins')
for name,h in parent['sha256'].items():
    require(hashlib.sha256((REPO/parent['source_directory']/name).read_bytes()).hexdigest()==h,'Changed direct parent: '+name)
spec=importlib.util.spec_from_file_location('j77_north_balanced_parent',REPO/parent['source_directory']/'verify.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
m,z,Q,V,D,N=b.m,b.z,b.Q,b.V,b.D,b.N
dot,cross,sub,scale,add=b.dot,b.cross,b.sub,b.scale,b.add
encode,decode,root,absq=b.encode,b.decode,b.root,b.absq

def digest(value):return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()

def pins():
    result=b.pins()
    for name,h in parent['sha256'].items():result[parent['source_directory']+'/'+name]=h
    require(len(result)==57,'Incomplete57file source boundary')
    return result

def quadratic_coefficients(corners,g):
    diagonal=[g(u) for u in corners]
    off=[(g(add(corners[i],corners[j]))-diagonal[i]-diagonal[j])/2 for i,j in [(0,1),(0,2),(1,2)]]
    return diagonal+off

def corner_gates(corners,flower,delta,audit):
    require(flower>0 and 0<delta<Q(F(1,20)),'Invalid receiving bounds')
    core=[v for v in V if scale(-1,v) in V]
    require(len(core)==50,'Wrong actual antipodal core')
    signs=[1 if dot(D,v)>0 else -1 for v in core]
    values=[s*dot(v,u) for u in corners for s,v in zip(signs,core)]
    require(all(x>0 for x in values),'Core signs not fixed on entire triangle')
    heights=[];caps=[]
    for u in corners:
        square=dot(u,u);h=min(absq(dot(v,u)) for v in core)
        margin=h*h-flower*flower*square
        cap=dot(D,u)*dot(D,u)-N*square*(1-delta*delta/2)*(1-delta*delta/2)
        require(margin>0 and dot(D,u)>0 and cap>0,'Corner fails continuous height/cap cone gate')
        heights.append(margin);caps.append(cap)
    audit.extend(values+heights+caps)
    return {'fixed_core_sign_comparisons':len(values),'minimum_corner_height_margin':encode(min(heights)),
            'minimum_corner_chord_cone_margin':encode(min(caps))}

def receiving_geometry(corners,probes,flower,delta,audit):
    gates=corner_gates(corners,flower,delta,audit);support=[];diameter=[];strict=0
    for i,p in probes:
        require(dot(p,D)==0 and dot(p,p)>0,'Reference probe is not a nonzero tangent support')
        for j,v in enumerate(V):
            if i==j:continue
            diff=sub(V[i],v);gap=dot(p,diff)
            coeff=quadratic_coefficients(corners,lambda u:dot(u,u)*gap-dot(p,u)*dot(diff,u))
            require(all(x>=0 for x in coeff),'Actual support fails on the entire closed receiver triangle')
            strict+=sum(x>0 for x in coeff);support.extend(coeff)
    d0=4*(m.caps.R2-m.caps.B)
    for i in range(55):
        for j in range(i):
            if V[i]==scale(-1,V[j]):continue
            diff=sub(V[i],V[j]);constant=d0-dot(diff,diff)
            coeff=quadratic_coefficients(corners,lambda u:constant*dot(u,u)+dot(diff,u)*dot(diff,u))
            require(all(x>0 for x in coeff),'Full-body nonantipodal diameter gate fails continuously')
            diameter.extend(coeff)
    require(len(support)==11016 and len(diameter)==8760,'Incomplete six-coefficient original comparisons')
    audit.extend(support+diameter)
    return {**gates,'original_support_comparisons':1836,'support_quadratic_Bernstein_coefficients':len(support),
            'strict_support_coefficients':strict,'minimum_support_coefficient':encode(min(support)),
            'nonantipodal_diameter_comparisons':1460,'diameter_quadratic_Bernstein_coefficients':len(diameter),
            'minimum_diameter_coefficient':encode(min(diameter)),
            'complete_original_geometry_sha256':digest([[encode(x) for x in support],[encode(x) for x in diameter]])}

def source_range(flower,a,limit,c0lo,c0hi,rhi,rholo,audit):
    beta=Q(F(101,100));expr=beta*(Q(c0hi)-flower)/Q(rholo)
    margins={'winning_source_gap':flower*flower-Q(F(1,12)),
             'source_chord_enclosure':a-expr,'a_priori_source_range':limit-a,
             'positive_active_source_signs':Q(c0lo)-Q(rhi)*limit,
             'source_radical_factor':beta*beta*(1-limit*limit/4)-1}
    require(0<a<limit<Q(1) and all(x>0 for x in margins.values()),'Wider-source coercivity hypothesis fails')
    audit.extend(margins.values())
    return expr,margins

def receiving_first_order(corners,normals,signed,nlo,nhi,audit):
    normlo=min(dot(D,u) for u in corners)/Q(nhi)
    require(normlo>0,'Receiving cone denominator not positive')
    result={};records=[]
    for i in [11,12,13]:
        terms=[]
        for sign in [-1,1]:
            raw=max(Q(),max(-sign*dot(normals[i],u) for u in corners))
            tau=raw/normlo
            term=signed[i,sign]['raw_height']*tau/Q(nlo)
            require(raw>=0 and term>=0,'Invalid directional receiving term')
            audit.extend([raw,term]);terms.append(term)
            records.append([i,sign,encode(raw),encode(term)])
        result[i]=max(terms)
    return result,{'positive_norm_denominator_lower':encode(normlo),'signed_physical_branch_bounds':6,
                   'first_order_bounds':{str(i):encode(v) for i,v in result.items()},'branch_sha256':digest(records)}

def remote_shape(remote):
    require(len(remote)==12 and {s for s,p,c in remote}=={-1,1},'Missing extended signed remote intervals')
    for sign in [-1,1]:
        ints=sorted((F(p['interval'][0]),F(p['interval'][1])) for s,p,c in remote if s==sign)
        require(len(ints)==6 and ints[0][0]==m.B and ints[-1][1]==1,'Wrong full closed cover endpoints')
        require(all(a<b for a,b in ints) and all(x[1]==y[0] for x,y in zip(ints,ints[1:])),'Closed signed cover has a gap or overlap')

def extended_remote(old,data,normals,nlo,nhi,audit):
    require(data['late_original_split']=='17/20' and data['near_quarter_original_pairs']==[[1,11,[10,12]],[-1,13,[14,8]]],
            'Unexpected extended original witness fixture')
    remote=[]
    for sign,p,c in old:
        p=dict(p)
        if p['interval']==['13/20','1']:p['interval']=['13/20','17/20']
        remote.append((sign,p,c))
    for sign,index,ids in data['near_quarter_original_pairs']:
        require(all(type(i) is int and 0<=i<55 for i in ids),'Source original index out of range')
        p={'probe':index,'orientation':1,'source_pair':ids,'point':sub(V[ids[0]],V[ids[1]]),'interval':['17/20','1']}
        remote.append((sign,p,z.polynomial(sign,p,normals,nlo,nhi,audit)))
    remote_shape(remote)
    return remote

def selected_error(p,a,delta,deficit,receiving,signed,gauges,nlo,rhi):
    i=p['probe'];point=p['point'];height=absq(dot(D,point))/Q(nlo)
    source=Q(rhi)*a*a
    if point in gauges:
        require(height==0,'Directional source rule used at nonzero height')
        source=min(source,Q(F(101,200))*a*gauges[point]*deficit)
    return receiving[i]+signed[i,1]['norm_upper']*(height*a+source+Q(rhi)*delta*delta)

def inverse_bound(K,T,E,epsilon,audit):
    bound,bracket=m.residual_inverse(K,T,E,audit)
    require(bound<epsilon,'Chosen residual-angle bound misses the inverse small branch')
    audit.extend([bracket,epsilon-bound])
    return bracket,epsilon-bound

def closed_interval(c,E,interval,audit):
    coeff=(c[0]-E,c[1],c[2]-E);lo,hi=[Q(F(x)) for x in interval]
    value=lambda x:coeff[0]+x*(coeff[1]+x*coeff[2])
    vals=(value(lo),value(lo)+(hi-lo)*(coeff[1]+2*coeff[2]*lo)/2,value(hi))
    reconstructed=(vals[0],2*(vals[1]-vals[0]),vals[0]-2*vals[1]+vals[2])
    substituted=(value(lo),(hi-lo)*(coeff[1]+2*coeff[2]*lo),(hi-lo)*(hi-lo)*coeff[2])
    require(reconstructed==substituted and coeff[2]<=0,'Closed roll Bernstein identity/concavity fails')
    margin=min(vals[0],vals[2]);require(margin>0 and vals[1]>=margin,'A closed signed remote interval survives this certificate')
    audit.extend(list(vals)+[vals[1]-margin])
    return margin,[encode(x) for x in vals]

def full_composition(a,delta,epsilon,theta,audit):
    require(0<=a<Q(F(3,20)) and 0<=delta<Q(F(1,20)) and 0<=epsilon<Q(F(1,10)),
            'Unsupported wider perpendicular-axis ranges')
    polynomial=m.composition_identity();frame=m.frame_audits()
    beta=Q(F(101,100));P=(1-a*a/4)*(1-delta*delta/4)*(1-epsilon*epsilon/4)
    plo,_=root(P,audit);square=(a+delta)*(a+delta)+epsilon*epsilon;_,X=root(square,audit)
    margins={'positive_quaternion_lift':Q(plo)-a*delta/4,
             'full_arcsin_derivative':beta*beta*(1-Q(X)*Q(X)/4)-1,
             'full_angle_enclosure':theta-beta*Q(X)}
    require(all(x>0 for x in margins.values()),'Full proper composition extension fails')
    audit.extend(margins.values())
    return margins,{'polynomial_residual_terms':polynomial,'exact_frame_gauge_audits':frame,
                    'orthogonal_chord_squared_upper':encode(square),'principal_spatial_angle_upper':encode(theta)}

def complete_phase(data,corners,constants,structure,gauges,signed,audit):
    nlo,nhi,rhi,c0lo,c0hi,rholo,normals,pi,gap=constants
    flower=Q(F(data['receiving_F_lower']));a=Q(F(data['source_chord_upper']))
    limit=Q(F(data['a_priori_source_chord_range']));delta=Q(F(data['receiving_chord_upper']))
    epsilon=Q(F(data['residual_angle_upper']));theta=Q(F(data['full_angle_upper']))
    expr,margins=source_range(flower,a,limit,c0lo,c0hi,rhi,rholo,audit)
    receiving,receiving_record=receiving_first_order(corners,normals,signed,nlo,nhi,audit)
    first,remote=structure;remote_shape(remote);deficit=Q(c0hi)-flower
    error=lambda p:selected_error(p,a,delta,deficit,receiving,signed,gauges,nlo,rhi)
    inverse=[inverse_bound(K,T,error(p),epsilon,audit) for sign,p,K,T in first]
    records=[];remote_margins=[]
    for sign,p,c in remote:
        margin,coefs=closed_interval(c,error(p),p['interval'],audit)
        remote_margins.append(margin);records.append([sign,p['probe'],p['interval'],coefs])
    transport=sum((p['weight']*p['norm_upper']*(p['source_height_upper']*a+p['kappa_upper']*delta
                   +Q(rhi)*(a*a+delta*delta)/2) for p in pi),Q())
    margins['asymmetric_even_half_turn']=gap-transport-m.G*epsilon*epsilon/2
    composition_margins,composition=full_composition(a,delta,epsilon,theta,audit)
    margins.update(composition_margins)
    margins['balanced_translated_torque']=Q(F(1,7))-delta-theta/2
    margins['explicit_torque_margin_over_1_40']=margins['balanced_translated_torque']-Q(F(1,40))
    require(all(v>0 for v in margins.values()),'Source/half-turn/full-angle/translation gate fails')
    # Failure of the obsolete sufficient witness on the same triangle is not nonexistence.
    old_endpoint=[]
    for sign,p,c in remote:
        if p['interval']==['13/20','17/20']:old_endpoint.append(sum(c,Q())-2*error(p))
    require(len(old_endpoint)==2 and all(v<0 for v in old_endpoint),'Advertised old-quarter witness failure absent')
    audit.extend(list(margins.values())+old_endpoint)
    return {'F_lower':data['receiving_F_lower'],'source_chord_upper':data['source_chord_upper'],
            'source_coercivity_expression':encode(expr),'receiver_chord_upper':data['receiving_chord_upper'],
            'residual_angle_upper':data['residual_angle_upper'],'full_angle_upper':data['full_angle_upper'],
            'signed_closed_remote_intervals':len(remote),'remote_Bernstein_coefficients':3*len(remote),
            'minimum_remote_margin':encode(min(remote_margins)),'remote_cover_sha256':digest(records),
            'minimum_inverse_bracket':encode(min(v[0] for v in inverse)),
            'minimum_residual_enclosure_margin':encode(min(v[1] for v in inverse)),
            'margins':{k:encode(v) for k,v in margins.items()},'directional_receiving':receiving_record,
            'wider_proper_composition':composition,'obsolete_quarter_endpoint_margins':[encode(x) for x in old_endpoint]}

def scope_ray(corners,audit):
    u=corners[1];square=dot(u,u);delta=Q(F(1,40));capgaps=[];cones=[]
    prior=[D,(Q(),Q(F(-13,11)),D[2]),(Q(F(1,10)),Q(F(-25,24)),D[2])];center=D
    for k in range(5):
        gap=(1-delta*delta/2)*(1-delta*delta/2)*square*N-dot(u,center)*dot(u,center)
        require(gap>0,'New north ray is in a retained winning-axis cap');capgaps.append(gap)
        for reflected in [False,True]:
            cols=[(-v[0],v[1],v[2]) if reflected else v for v in prior]
            weights=b.solve(cols,u)
            require(any(x<0 for x in weights) and any(x>0 for x in weights),'North ray is in a retained projective triangle image')
            cones.append([k,reflected,[encode(x) for x in weights]]);audit.extend(weights)
        center=m.sharp.rotate(center);prior=[m.sharp.rotate(v) for v in prior]
    audit.extend(capgaps)
    return {'original_chart_ray':[encode(x) for x in u],'retained_1_40_axis_caps_excluded':5,
            'retained_projective_triangle_images_excluded':10,'minimum_cap_exclusion_margin':encode(min(capgaps)),
            'retained_triangle_cone_sha256':digest(cones)}

def controls(data,corners,constants,structure,gauges,signed,probes,costs):
    nlo,nhi,rhi,c0lo,c0hi,rholo,normals,pi,gap=constants;first,remote=structure
    flower=Q(F(data['receiving_F_lower']));a=Q(F(data['source_chord_upper']))
    recv,_=receiving_first_order(corners,normals,signed,nlo,nhi,[])
    p,c=remote[-1][1:];E=selected_error(p,a,Q(F(data['receiving_chord_upper'])),Q(c0hi)-flower,recv,signed,gauges,nlo,rhi)
    wrong=list(remote);s,p0,c0=wrong[-1];p0=dict(p0);p0['interval']=['9/10','1'];wrong[-1]=(s,p0,c0)
    badpair=dict(p);badpair['point']=scale(-1,p['point']);badc=z.polynomial(-1,badpair,normals,nlo,nhi,[])
    tests=[lambda:corner_gates(corners,flower,Q(F(1,50)),[]),
           lambda:source_range(flower,Q(F(1,10)),Q(F(3,20)),c0lo,c0hi,rhi,rholo,[]),
           lambda:source_range(Q(F(1,4)),a,Q(F(3,20)),c0lo,c0hi,rhi,rholo,[]),
           lambda:source_range(flower,a,Q(F(1,5)),c0lo,c0hi,rhi,rholo,[]),
           lambda:remote_shape(remote[:-1]),lambda:remote_shape(wrong),
           lambda:closed_interval(badc,E,['17/20','1'],[]),
           lambda:inverse_bound(first[0][2],first[0][3],selected_error(first[0][1],a,Q(F(33,1000)),Q(c0hi)-flower,recv,signed,gauges,nlo,rhi),Q(F(1,20)),[]),
           lambda:full_composition(Q(F(1,5)),Q(F(33,1000)),Q(F(69,1000)),Q(F(21,125)),[]),
           lambda:full_composition(a,Q(F(33,1000)),Q(F(69,1000)),Q(F(1,10)),[]),
           lambda:b.balanced_point([0,0,1],probes,costs,[]),
           lambda:b.balanced_point([32,16,30],probes,costs,[],[Q(F(1,3))]*3),
           lambda:m.old.root_check(Q(2),F(1),F(1),[])]
    for test in tests:
        try:test()
        except ValueError:pass
        else:raise ValueError('Malformed north-domain proof evidence accepted')
    return len(tests)

def check(data,self_test=False):
    source_pins=pins();audit=[]
    require(data['chart_area']=='3/800' and data['receiving_F_lower']=='31351/100000'
            and data['receiving_chord_upper']=='33/1000' and data['source_chord_upper']=='59/500'
            and data['a_priori_source_chord_range']=='3/20' and data['residual_angle_upper']=='69/1000'
            and data['full_angle_upper']=='21/125' and data['root_grid_denominator']==10**12,'Changed fixed exact certificate parameters')
    corners=[tuple(decode(x) for x in u) for u in data['receiving_corners']]
    require(corners==[D,(Q(),Q(F(-17,20)),D[2]),(Q(F(1,20)),Q(F(-17,20)),D[2])]
            and absq(m.chart_area(corners))==Q(F(3,800)),'Wrong actual entire north triangle')
    require(len(V)==55 and len(set(V))==55 and all(dot(v,v)==m.caps.R2 for v in V),'Wrong original body model')
    require({(-v[0],v[1],v[2]) for v in V}==set(V) and {m.sharp.rotate(v) for v in V}==set(V),'Required actual body symmetries fail')
    nlo,nhi=root(N,audit);_,rhi=root(m.caps.R2,audit);c0lo,c0hi=root(m.caps.B,audit);rholo,_=root(Q(233,-10)/596,audit)
    probes=m.local.make_probes();prior=json.loads((REPO/parent['source_directory']/'certificates.json').read_text())
    costs,hull=b.center_hull(prior['balanced_probe_triples'],probes,audit)
    geometry=receiving_geometry(corners,probes,Q(F(data['receiving_F_lower'])),Q(F(data['receiving_chord_upper'])),audit)
    normals=m.caps.reference_geometry(audit)[0]
    zfixture=json.loads((REPO/b.parent['source_directory']/'certificates.json').read_text())
    first,oldremote,points=z.structures(zfixture,normals,nlo,nhi,audit)
    gauges,directional=b.tangent_gauges(points,[decode(prior['first_directional_gauge']),decode(prior['late_directional_gauge'])],audit)
    remote=extended_remote(oldremote,data,normals,nlo,nhi,audit)
    signed,pc,ec,envelope_sha=z.signed_envelopes(normals,nlo,audit)
    _,_,pi,gap,pc0,ec0,sc0,se0=m.old.transport_data(normals,z.RANGE,nlo,audit)
    even=m.even_stress(normals,pi,m.G,audit)
    constants=(nlo,nhi,rhi,c0lo,c0hi,rholo,normals,pi,gap);structure=(first,remote)
    phase=complete_phase(data,corners,constants,structure,gauges,signed,audit)
    ray=scope_ray(corners,audit);rodrigues=z.rodrigues_controls()
    tests=controls(data,corners,constants,structure,gauges,signed,probes,costs) if self_test else 0
    values=sorted(set(audit),key=lambda q:(q.a,q.b));m.local.independent_sign_audit(values)
    return {'agent':'six-rupert-2','role':'researcher','claim_status':'entire_closed_J77_north_triangle_all_original_sources',
            'global_Rupert_resolved':False,'independent_review_asserted':False,'full_parent_outputs_replayed':False,
            'original_sources_angles_rolls_translations_unrestricted':True,'scales_covered':'lambda>=1',
            'closed_scale':1,'closed_translation':0,'closed_equality_forms':['Q=R^k','Q=M_n X R^k'],
            'entire_reference_chart_area':'3/800','body_and_normal_reversal_images_covered':True,
            'entire_old_triangle_and_1_40_caps_retained_separately':True,'unqualified_prior_criterion_dominance_asserted':False,
            'whole_north_triangle':geometry,'balanced_normalized_torque_hull':hull,'directional_source':directional,
            'complete_full_source_phase':phase,'explicit_new_union_scope_ray':ray,
            'signed_original_width_comparisons':pc,'signed_height_excess_comparisons':ec,'signed_width_envelope_sha256':envelope_sha,
            'retained_absolute_width_comparisons':pc0,'retained_absolute_width_excess':ec0,
            'retained_even_support_comparisons':sc0,'retained_even_support_excess':se0,'unique_even_minimum_comparisons':even,
            'exact_Rodrigues_audits':rodrigues,'pinned_dependency_files':len(source_pins),
            'new_sign_records':len(audit),'distinct_independent_rational_sign_audits_including_kernel_controls':len(values)+9,
            'malformed_controls_with_self_test':tests,'canonical_fixture_sha256':hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    data=json.loads((ROOT/'certificates.json').read_text())
    print(json.dumps(check(data,args.self_test),indent=2,sort_keys=True))
