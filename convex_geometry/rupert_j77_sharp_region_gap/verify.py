#!/usr/bin/env python3
"""Exact J77 regional height spectrum, sharp gap and whole receiver triangle."""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,importlib.util,itertools,json

ROOT=Path(__file__).resolve().parent
def require(condition,message):
    if not condition:raise ValueError(message)
manifest=json.loads((ROOT/'dependencies.json').read_text())
require(manifest['source_directory']=='convex_geometry/rupert_j77_directional_receiver_domains'
        and manifest['source_commit']=='f7cfae81911e86c562b226a04f7966989812f94d','Incorrect source dependency')
require(set(manifest['sha256'])=={'.gitignore','README.md','PROOF.md','verify.py','certificates.json','dependencies.json','expected.json'},
        'Incomplete source pin set')
PRIOR=ROOT.parent.parent/manifest['source_directory']
for name,digest in manifest['sha256'].items():
    require(hashlib.sha256((PRIOR/name).read_bytes()).hexdigest()==digest,'Changed dependency: '+name)
spec=importlib.util.spec_from_file_location('j77_sharp_directional_parent',PRIOR/'verify.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
Q,V,D,N=old.Q,old.V,old.D,old.N
dot,sub,scale=old.dot,old.sub,old.scale
caps,local,ROLL=old.caps,old.local,old.ROLL
add,cross=caps.local.add,caps.cross
decode,encode,absq,root=old.decode,old.encode,old.absq,old.root
SHARP=Q(F(1,12))

def balance(active,y):
    for i,v in enumerate(active):
        if v==y:return (i,),(Q(1),)
    for i,j in itertools.combinations(range(len(active)),2):
        e=sub(active[i],active[j]);weight=dot(sub(y,active[j]),e)/dot(e,e)
        if 0<=weight<=1 and add(scale(weight,active[i]),scale(1-weight,active[j]))==y:
            return (i,j),(weight,1-weight)
    for i,j,k in itertools.combinations(range(len(active)),3):
        e,f=sub(active[j],active[i]),sub(active[k],active[i]);z=sub(y,active[i])
        ee,ef,ff=dot(e,e),dot(e,f),dot(f,f);det=ee*ff-ef*ef
        if det==0:continue
        ez,fz=dot(e,z),dot(f,z);u=(ez*ff-fz*ef)/det;v=(fz*ee-ez*ef)/det
        weights=(1-u-v,u,v)
        if all(w>=0 for w in weights) and add(active[i],add(scale(u,e),scale(v,f)))==y:
            return (i,j,k),weights
    return None

def generic_regions(points,audit):
    require(all(dot(v,v)>0 for v in points),'Zero core representative')
    for a,b in itertools.combinations(points,2):
        require(dot(cross(a,b),cross(a,b))>0,'Coincident great circles')
    determinants=[dot(a,cross(b,c)) for a,b,c in itertools.combinations(points,3)]
    require(all(d!=0 for d in determinants),'Nongeneric great-circle arrangement')
    audit.extend(determinants)
    return 1+len(points)*(len(points)-1)//2,len(determinants)

def stationary_records(points):
    rays={};occurrences=0
    for d,label in caps.candidates(points):
        occurrences+=1;require(dot(d,d)>0,'Zero candidate ray')
        rays.setdefault(caps.ray(d),label)
    records=[];boundary=nonstationary=0;score_digest=hashlib.sha256()
    for d,label in rays.items():
        heights=[dot(v,d) for v in points];h=min(absq(x) for x in heights)
        score_digest.update(json.dumps([label,[encode(x) for x in d],encode(h)],separators=(',',':')).encode()+b'\n')
        if h==0:boundary+=1;continue
        norm=dot(d,d);y=scale(h/norm,d);signs=tuple(x.sign() for x in heights)
        active_ids=[i for i,x in enumerate(heights) if absq(x)==h]
        active=[scale(signs[i],points[i]) for i in active_ids]
        selected=balance(active,y)
        if selected is None:nonstationary+=1;continue
        indices,weights=selected
        records.append({'ray':d,'nearest_point':y,'height_squared':h*h/norm,
                        'active_core_indices':active_ids,'balance_core_indices':[active_ids[i] for i in indices],
                        'balance_weights':weights,'candidate_label':label})
    return records,{'candidate_occurrences':occurrences,'unique_projective_candidates':len(rays),
                    'candidate_axial_scores':len(rays)*len(points),'boundary_candidates':boundary,
                    'nonstationary_candidates':nonstationary,'candidate_score_stream_sha256':score_digest.hexdigest()}

def certify_record(record,points,audit):
    d,y,c2=record['ray'],record['nearest_point'],record['height_squared']
    require(len(d)==len(y)==3 and dot(d,d)>0,'Invalid regional direction')
    values=[dot(v,d) for v in points]
    require(all(x!=0 for x in values),'Regional optimizer is on an axial wall')
    signs=[x.sign() for x in values];h=min(absq(x) for x in values)
    require(y==scale(h/dot(d,d),d) and c2==h*h/dot(d,d)==dot(y,y)>0,'Wrong nearest point or regional maximum')
    indices,weights=record['balance_core_indices'],record['balance_weights']
    require(1<=len(indices)==len(weights)<=3 and len(set(indices))==len(indices)
            and all(type(i) is int and 0<=i<len(points) for i in indices),'Malformed active balance')
    require(sum(weights,Q())==1 and all(w>=0 for w in weights),'Negative or unnormalized active weights')
    combined=tuple(sum((w*signs[i]*points[i][k] for i,w in zip(indices,weights)),Q()) for k in range(3))
    require(combined==y,'Full three-coordinate nearest-point balance fails')
    gaps=[dot(scale(s,v),y)-c2 for s,v in zip(signs,points)]
    require(all(g>=0 for g in gaps) and all(gaps[i]==0 for i in indices),'Nearest-point supporting plane fails')
    require(record['active_core_indices']==[i for i,g in enumerate(gaps) if g==0],'Incomplete active set')
    audit.extend(values);audit.extend(gaps);audit.extend(weights);audit.append(c2)
    mask=sum(1<<i for i,s in enumerate(signs) if s>0)
    return min(mask,((1<<len(points))-1)^mask)

def certify_table(records,points,region_count,audit):
    require(len(records)==region_count,'Incomplete regional optimizer table')
    indexed={}
    for record in records:
        pattern=certify_record(record,points,audit)
        require(pattern not in indexed,'Duplicate projective signed region')
        indexed[pattern]=record
    return indexed

def rotate(v):
    axis=(Q(),Q(1,1)/2,Q(1));c=Q(-1,1)/4;t=Q(1)/2
    return add(add(scale(c,v),scale((1-c)*dot(axis,v)/dot(axis,axis),axis)),scale(t,cross(axis,v)))
def body_orbit(v):
    rays=set()
    for mirror in [False,True]:
        w=(-v[0],v[1],v[2]) if mirror else v
        for k in range(5):rays.add(caps.ray(w));w=rotate(w)
    return rays

def spectrum(records,sharp,audit):
    require(0<sharp<caps.B,'Invalid regional-gap threshold')
    byray={r['ray']:r for r in records};require(len(byray)==len(records),'Duplicate regional axis')
    winning=body_orbit(D);require(len(winning)==5 and winning<=set(byray),'Missing winning regions')
    outside=[r for r in records if r['ray'] not in winning]
    require(all(byray[d]['height_squared']==caps.B for d in winning),'Winning height changed')
    require(max(r['height_squared'] for r in outside)==sharp,'Nonwinning regional gap is not sharp')
    audit.extend(sharp-r['height_squared'] for r in outside)
    second={r['ray'] for r in outside if r['height_squared']==sharp}
    second_rep=(Q(1),Q(-3,-1)/2,Q())
    require(second==body_orbit(second_rep) and len(second)==5,'Sharp second-maximum orbit is incomplete')
    levels=[]
    for value in sorted({r['height_squared'] for r in records},reverse=True):
        levels.append({'maximum_height_squared':encode(value),'projective_region_count':sum(r['height_squared']==value for r in records)})
    classes=[];seen=set()
    for ray in sorted(byray,key=lambda v:tuple((x.a,x.b) for x in v)):
        if ray in seen:continue
        orbit=body_orbit(ray);require(orbit<=set(byray),'Region table fails body-symmetry closure')
        value=byray[ray]['height_squared']
        require(all(byray[d]['height_squared']==value for d in orbit),'Regional orbit heights differ')
        seen.update(orbit)
        classes.append({'representative_ray':[encode(x) for x in ray],'projective_region_count':len(orbit),
                        'maximum_height_squared':encode(value)})
    require(len(levels)==14 and len(classes)==37 and seen==set(byray),'Incomplete regional spectrum or orbit list')
    return levels,classes

def criterion(flower,delta,heights,width_data,pi_data,pi_gap,rhi,c0hi,rholo,nlo,normals,sharp,audit):
    require(flower>0 and delta>=0,'Invalid receiver parameters')
    a=Q(F(101,100))*(Q(c0hi)-flower)/rholo
    theta=Q(F(1,25))+Q(F(101,100))*(a+delta)
    require(a>=0,'Negative source alignment bound')
    margins={'sharp_regional_gap':flower*flower-sharp,'receiver_height_gap_domain':Q(F(1,20))-delta,
             'source_chord_domain':Q(F(1,10))-a,'receiver_chord_domain':Q(F(1,10))-delta}
    roll=[]
    for cover in ROLL['covers']:
        for piece in cover['pieces']:
            p=width_data[piece['probe']];i,j=piece['source_pair'];h=absq(heights[i]-heights[j])/nlo
            gamma=caps.quadratic_piece(cover['sign'],piece,normals,
                   Q(F(ROLL['root_N_enclosure'][0])),Q(F(ROLL['root_N_enclosure'][1])),
                   Q(F(ROLL['gap_numerator_lower_bound'])),audit)
            error=p['norm_upper']*(h*a+p['kappa_upper']*delta+Q(rhi)*(a*a+delta*delta))
            b=F(piece['interval'][1]);margin=gamma-Q(1+b*b)*error
            require(margin>0,'Closed remote-roll piece is not excluded');roll.append(margin);audit.append(margin)
    error=sum((p['weight']*p['norm_upper']*(p['source_height_upper']*a+p['kappa_upper']*delta
              +Q(rhi)*(a*a+delta*delta)/2+Q(rhi)/25) for p in pi_data),Q())
    margins['half_turn']=pi_gap-error
    torque=Q(local.C*local.M)*(delta+theta/2);margins['translated_torque']=1-3*torque*torque
    require(all(m>0 for m in margins.values()),'Sharp directional receiver criterion fails')
    audit.extend(margins.values())
    return {'F_lower':encode(flower),'receiver_chord_upper':encode(delta),'source_chord_upper':encode(a),
            'full_angle_upper':encode(theta),'positive_margins':{k:encode(v) for k,v in margins.items()},
            'minimum_remote_roll_margin':encode(min(roll))}

def table_controls():
    basis=[tuple(Q(int(i==j)) for i in range(3)) for j in range(3)]
    for count in [1,2,3]:
        points=basis[:count];regions,_=generic_regions(points,[]);records,_=stationary_records(points)
        certify_table(records,points,regions,[])
        require(regions==2**(count-1) and all(r['height_squared']==Q(F(1,count)) for r in records),'Orthogonal regional control fails')
    return 3

def malformed_controls(data,records,points,region_count,constants):
    def changed(record):return {**record,'balance_weights':tuple(record['balance_weights'])}
    bad_point=changed(records[0]);bad_point['nearest_point']=add(bad_point['nearest_point'],(Q(F(1,100)),Q(),Q()))
    bad_weight=changed(records[0]);bad_weight['balance_weights']=(-Q(1),)+bad_weight['balance_weights'][1:]
    def wider_triangle():
        corners=[D,(Q(),Q(F(-7,6)),D[2]),(Q(F(1,40)),Q(F(-25,24)),D[2])]
        core=[v for v in V if scale(-1,v) in V]
        parameters=[old.corner_parameters(u,core,[]) for u in corners]
        heights,width,pi,gap,rhi,c0hi,rholo,nlo,normals=constants
        criterion(min(p[0] for p in parameters),max(p[1] for p in parameters),
                  heights,width,pi,gap,rhi,c0hi,rholo,nlo,normals,SHARP,[])
    bad_chart=json.loads(json.dumps(data));bad_chart['triangle'][1][2]=['4','0']
    invalid=[lambda:certify_table(records[:-1],points,region_count,[]),
             lambda:certify_table(records[1:]+[records[1]],points,region_count,[]),
             lambda:certify_record(bad_point,points,[]),lambda:certify_record(bad_weight,points,[]),
             lambda:spectrum(records,Q(F(1,13)),[]),lambda:generic_regions([points[0],points[0],points[1]],[]),
             wider_triangle,lambda:old.geometry_fixture(bad_chart)]
    for test in invalid:
        try:test()
        except ValueError:pass
        else:raise ValueError('Malformed regional evidence accepted')
    return len(invalid)

def check(data,self_test=False):
    inherited=old.check(json.loads((PRIOR/'certificates.json').read_text()),self_test)
    require(inherited==json.loads((PRIOR/'expected.json').read_text()),'Full parent output differs')
    sharp=decode(data['sharp_nonwinning_height_squared']);require(sharp==SHARP,'Unsupported sharp regional threshold')
    audit=[];core_ids=[i for i,v in enumerate(V) if scale(-1,v) in V and i<V.index(scale(-1,v))]
    points=[V[i] for i in core_ids];require(len(points)==25,'Wrong antipodal representative count')
    regions,det_count=generic_regions(points,audit);require(regions==301 and det_count==2300,'Wrong arrangement count')
    records,counts=stationary_records(points)
    indexed=certify_table(records,points,regions,audit);levels,classes=spectrum(records,sharp,audit)
    require(counts['candidate_occurrences']==9825 and counts['unique_projective_candidates']==3306,'Incomplete candidate generator')
    stream=[]
    for mask,record in sorted(indexed.items()):
        stream.append([mask,[encode(x) for x in record['ray']],[encode(x) for x in record['nearest_point']],
                       encode(record['height_squared']),record['active_core_indices'],record['balance_core_indices'],
                       [encode(w) for w in record['balance_weights']]])
    record_digest=hashlib.sha256(json.dumps(stream,separators=(',',':')).encode()).hexdigest()
    beta=decode(ROLL['beta']);w=caps.witness(points,ROLL['beta_witness']);values=[dot(v,w) for v in points]
    require(all(x!=0 for x in values),'Old beta witness lies on a wall')
    h=min(absq(x) for x in values);mask=sum(1<<i for i,x in enumerate(values) if x>0)
    mask=min(mask,((1<<25)-1)^mask);winning_record=indexed[mask]
    require(h*h/dot(w,w)==beta and winning_record['height_squared']==caps.B
            and caps.ray(w)!=winning_record['ray'],'Old cutoff witness was not nonstationary inside a winning region')
    audit.append(beta-sharp)
    corners,critical,area=old.geometry_fixture(data)
    _,rhi=root(caps.R2,audit);_,c0hi=root(caps.B,audit);rholo,_=root(Q(233,-10)/596,audit);nlo,_=root(N,audit)
    normals=caps.reference_geometry(audit)[0]
    heights,width,pi,gap,pair_count,excess,single,single_excess=old.transport_data(normals,Q(F(1,20)),nlo,audit)
    core=[v for v in V if scale(-1,v) in V];common=0
    for v in core:
        axial=[dot(v,u) for u in corners]
        require(all(x>0 for x in axial) or all(x<0 for x in axial),'Whole-triangle core signs vary')
        common+=1;audit.extend(axial)
    parameters=[old.corner_parameters(u,core,audit) for u in corners]
    result=criterion(min(p[0] for p in parameters),max(p[1] for p in parameters),
                     heights,width,pi,gap,rhi,c0hi,rholo,nlo,normals,sharp,audit)
    sc,dc,replays,smin,dmin=old.whole_triangle(corners,critical,local.make_probes(),audit)
    l= corners[1];lh=min(absq(dot(v,l)) for v in core);l_f2=lh*lh/dot(l,l)
    require(sharp<l_f2<beta,'New triangle does not cross the former regional cutoff')
    audit.extend([l_f2-sharp,beta-l_f2])
    denlo,_=root(dot(l,l)*N,audit);beyond=2-2*dot(D,l)/denlo-Q(F(1,35))*Q(F(1,35))
    require(beyond>0,'Far corner does not exceed chord1/35');audit.append(beyond)
    old_data=json.loads((PRIOR/'certificates.json').read_text());old_corners,_,old_area=old.geometry_fixture(old_data)
    weights=[(Q(1),Q(),Q()),(Q(F(5,12)),Q(F(7,12)),Q()),(Q(F(17,40)),Q(F(7,40)),Q(F(2,5)))]
    for target,coefficients in zip(old_corners,weights):
        require(sum(coefficients,Q())==1 and all(t>=0 for t in coefficients),'Invalid triangle containment weights')
        require(tuple(sum((t*u[k] for t,u in zip(coefficients,corners)),Q()) for k in range(3))==target,
                'Previous closed triangle is not contained')
    require(area==Q(F(1,560)) and area/old_area==Q(F(30,7)),'Incorrect fixed-z chart-area ratio')
    controls=table_controls()
    constants=(heights,width,pi,gap,rhi,c0hi,rholo,nlo,normals)
    malformed=malformed_controls(data,records,points,regions,constants) if self_test else 8
    unique=sorted(set(audit),key=lambda x:(x.a,x.b));local.independent_sign_audit(unique)
    return {'agent':'six-rupert-2','role':'researcher','claim_status':'J77_sharp_regional_gap_and_continuous_receiver_extension',
      'global_Rupert_resolved':False,'projective_signed_regions':regions,'directed_signed_regions':2*regions,
      'generic_nonzero_triple_determinants':det_count,'nearest_point_certificate_count':len(records),
      'nearest_point_support_comparisons':len(records)*len(points),'height_spectrum':levels,'C5v_region_orbits':classes,
      'sharp_nonwinning_region_maximum_squared':encode(sharp),'sharp_second_maximum_orbit_axes':5,
      'winning_region_orbit_axes':5,'winning_height_squared':encode(caps.B),
      'old_beta_is_nonstationary_inside_winning_region':True,'old_beta_region_optimizer_ray':[encode(x) for x in winning_record['ray']],
      'regional_nearest_point_certificate_sha256':record_digest,**counts,
      'all_source_orientations_rolls_translations':True,'scales_covered':'lambda >= 1',
      'closed_equality_forms':['Q=R^k','Q=M_n X R^k'],'closed_scale':1,'closed_translation':0,
      'whole_triangle_fixed_z_chart_area':encode(area),'previous_triangle_area_ratio':encode(area/old_area),
      'previous_whole_triangle_contained':True,'far_corner_chord_strict_lower_bound':'1/35',
      'far_corner_actual_height_squared':encode(l_f2),'far_corner_squared_chord_extension_margin':encode(beyond),
      'sharp_directional_receiver_criterion':result,'whole_triangle_common_core_signs':common,
      'whole_triangle_support_Bernstein_coefficients':sc,'whole_triangle_diameter_Bernstein_coefficients':dc,
      'whole_triangle_minimum_support_coefficient':encode(smin),'whole_triangle_minimum_diameter_coefficient':encode(dmin),
      'independent_actual_plane_barycenter_replays':replays,'difference_support_pair_checks':pair_count,
      'difference_excess_height_checks':excess,'half_turn_support_vertex_checks':single,'half_turn_excess_height_checks':single_excess,
      'orthogonal_regional_controls':controls,'malformed_controls_with_self_test':malformed+20,
      'new_sign_records':len(audit),'new_independent_rational_sign_audits':len(unique)+9,
      'inherited_canonical_certificate_sha256':inherited['canonical_certificate_sha256'],
      'canonical_certificate_sha256':hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    print(json.dumps(check(json.loads((ROOT/'certificates.json').read_text()),args.self_test),indent=2,sort_keys=True))
