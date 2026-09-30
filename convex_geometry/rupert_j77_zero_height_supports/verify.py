#!/usr/bin/env python3
"""Exact zero-height source witnesses and one-sided J77 receiving widths."""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,importlib.util,itertools,json

ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent.parent
def require(ok,message):
    if not ok:raise ValueError(message)
manifest=json.loads((ROOT/'dependencies.json').read_text())
require(len(manifest['sources'])==1,'Incomplete direct dependency')
parent=manifest['sources'][0]
require(parent['source_directory']=='convex_geometry/rupert_j77_adaptive_roll_domains'
        and parent['source_commit']=='94e3ef96d8cdaff6fd6e0c6f0f7397b14c2f0a6b','Wrong adaptive parent')
require(set(parent['sha256'])=={'.gitignore','README.md','PROOF.md','verify.py','certificates.json','dependencies.json','expected.json'},
        'Incomplete direct source pins')
for name,digest in parent['sha256'].items():
    require(hashlib.sha256((REPO/parent['source_directory']/name).read_bytes()).hexdigest()==digest,'Changed direct dependency: '+name)
spec=importlib.util.spec_from_file_location('j77_zero_height_adaptive_parent',REPO/parent['source_directory']/'verify.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
Q,V,D,N=m.Q,m.V,m.D,m.N
dot,sub,add,scale,cross=m.dot,m.sub,m.add,m.scale,m.cross
encode,decode,absq,root=m.encode,m.decode,m.absq,m.root
B=m.B;RANGE=Q(F(1,20))

def dependency_pins():
    pins=m.all_dependency_pins()
    for name,digest in parent['sha256'].items():
        path=parent['source_directory']+'/'+name
        require(path not in pins or pins[path]==digest,'Conflicting source pin')
        pins[path]=digest
    require(len(pins)==43,'Incomplete direct/transitive dependency boundary')
    return pins

def signed_envelopes(normals,nlo,audit,wrong_raw=False):
    heights=[dot(D,v) for v in V];records={};pairs=excess=0;stream=[]
    for index in [11,12,13]:
        normal=normals[index];values=[dot(normal,v) for v in V]
        H=max(values)-min(values);plus=[i for i,x in enumerate(values) if x==max(values)]
        minus=[i for i,x in enumerate(values) if x==min(values)]
        _,eta=root(dot(normal,normal),audit);eta=Q(eta)
        for sign in [-1,1]:
            raw=max(Q(),max(sign*(heights[i]-heights[j]) for i,j in itertools.product(plus,minus)))
            if wrong_raw and index==11 and sign==1:raw=Q()
            margins=[]
            for i,j in itertools.product(range(55),repeat=2):
                gap=H-values[i]+values[j];h=sign*(heights[i]-heights[j]);pairs+=1
                require(gap>=0,'Incorrect full original receiver width');audit.append(gap)
                if h>raw:
                    margin=gap-eta*RANGE*(h-raw)/nlo
                    require(margin>0,'One-sided receiving height-gap envelope fails')
                    margins.append(margin);audit.append(margin);excess+=1
            require(margins,'Missing signed excess comparisons')
            record={'norm_upper':eta,'kappa_upper':raw/nlo,'raw_height':raw,
                    'minimum_excess_margin':min(margins),'excess_count':len(margins)}
            records[index,sign]=record
            stream.append([index,sign,encode(raw),encode(eta),encode(min(margins)),len(margins)])
    require(records[12,1]['raw_height']==0,'Late receiving width has a first-order height cost')
    require(records[11,1]['raw_height']==records[13,1]['raw_height']==Q(F(1,2),F(-1,10)),
            'Wrong signed first-support height')
    return records,pairs,excess,hashlib.sha256(json.dumps(stream,separators=(',',':')).encode()).hexdigest()

def convex_difference(pairs,weight,audit):
    require(len(pairs)==2 and 0<weight<1,'Invalid positive convex difference')
    require(all(len(p)==2 and all(type(i) is int and 0<=i<55 for i in p) for p in pairs),
            'Invalid original difference indices')
    left=sub(V[pairs[0][0]],V[pairs[0][1]]);right=sub(V[pairs[1][0]],V[pairs[1][1]])
    point=add(scale(weight,left),scale(1-weight,right))
    require(dot(D,point)==0,'Constructed difference has nonzero axial height')
    margin=4*m.caps.R2-dot(point,point)
    require(margin>0,'Constructed difference exceeds the body diameter bound')
    audit.extend([weight,1-weight,margin])
    return point

def polynomial(sign,piece,normals,nlo,nhi,audit):
    normal=scale(piece['orientation'],normals[piece['probe']]);point=piece['point']
    values=[dot(normal,v) for v in V];H=max(values)-min(values)
    d=dot(normal,point);S=sign*dot(normal,cross(D,point))
    require(H>=absq(d),'Source difference leaves the supporting strip')
    k=S/Q(nhi if S>=0 else nlo)
    audit.extend([H-d,H+d]);return d-H,2*k,-d-H

def cover_shape(remote):
    require(len(remote)==10 and {s for s,p,c in remote}=={-1,1},'Incomplete signed remote cover')
    for sign in [-1,1]:
        intervals=sorted((F(p['interval'][0]),F(p['interval'][1])) for s,p,c in remote if s==sign)
        require(len(intervals)==5 and intervals[0][0]==B and intervals[-1][1]==1,
                'Wrong remote interval endpoints')
        require(all(a<b for a,b in intervals) and all(a[1]==b[0] for a,b in zip(intervals,intervals[1:])),
                'Signed closed cover has a gap or overlap')

def structures(data,normals,nlo,nhi,audit):
    nu=decode(data['first_convex_weight']);tau=decode(data['late_convex_weight'])
    require(nu==Q(F(1,2),F(1,5)) and tau==Q(7,-1)/22,'Wrong exact convex weights')
    require(data['late_split']=='13/20','Wrong closed remote split')
    first=[];late=[];points=[]
    for sign,index,pairs in [(1,11,[[29,54],[16,24]]),(-1,13,[[31,51],[19,24]])]:
        point=convex_difference(pairs,nu,audit);points.append(point)
        p={'probe':index,'orientation':1,'point':point,'pairs':pairs,'weight':nu}
        coeff=polynomial(sign,p,normals,nlo,nhi,audit)
        require(coeff[0]==0 and coeff[1]>0 and coeff[2]<0,'Invalid zero-height first inverse polynomial')
        first.append((sign,p,coeff[1],-coeff[2]));audit.extend(coeff)
    for sign,pairs in [(1,[[8,15],[8,14]]),(-1,[[12,11],[12,10]])]:
        point=convex_difference(pairs,tau,audit);points.append(point)
        p={'probe':12,'orientation':1,'point':point,'pairs':pairs,'weight':tau,'interval':['13/20','1']}
        late.append((sign,p,polynomial(sign,p,normals,nlo,nhi,audit)))
    expected=[(Q(F(5,4),F(7,20)),Q(F(3,2),1),Q(F(1,4),F(1,4))),
              (Q(F(-5,4),F(-7,20)),Q(F(3,2),1),Q(F(1,4),F(1,4))),
              (Q(2,1),Q(1),tau),(Q(-2,-1),Q(1),tau)]
    require(points==expected,'Explicit coordinate construction identities fail')
    require(first[0][2:]==first[1][2:] and late[0][2]==late[1][2],'Reflected signed support polynomials differ')
    remote=[]
    for cover in m.ROLL['covers']:
        for original in cover['pieces'][1:]:
            if original['interval']==['151/200','1']:continue
            p=dict(original);i,j=p['source_pair'];p['point']=sub(V[i],V[j])
            if p['interval']==['51/100','151/200']:p['interval']=['51/100','13/20']
            remote.append((cover['sign'],p,polynomial(cover['sign'],p,normals,nlo,nhi,audit)))
    remote.extend(late);cover_shape(remote)
    return first,remote,points

def error(piece,a,delta,width,nlo,rhi):
    record=width[piece['probe']];h=absq(dot(D,piece['point']))/nlo
    return record['norm_upper']*(h*a+record['kappa_upper']*delta+Q(rhi)*(a*a+delta*delta))

def phase(flower,delta,constants,structure,audit):
    width,pi,gap,rhi,c0hi,rholo,nlo=constants;first,remote=structure
    a=Q(F(101,100))*(Q(c0hi)-flower)/rholo
    require(a>=0 and delta>=0,'Invalid source or receiving chord bound')
    margins={'sharp_regional_gap':flower*flower-Q(F(1,12)),
             'signed_receiver_range':RANGE-delta,'source_chord_domain':Q(F(1,10))-a,
             'receiver_chord_domain':Q(F(1,10))-delta}
    epsilons=[];brackets=[]
    for sign,p,K,T in first:
        epsilon,bracket=m.residual_inverse(K,T,error(p,a,delta,width,nlo,rhi),audit)
        epsilons.append(epsilon);brackets.append(bracket)
    epsilon=max(epsilons);remote_margins=[]
    for sign,p,c in remote:
        E=error(p,a,delta,width,nlo,rhi);coeff=(c[0]-E,c[1],c[2]-E)
        lo,hi=[Q(F(x)) for x in p['interval']];value=lambda x:coeff[0]+x*(coeff[1]+x*coeff[2])
        beta=(value(lo),value(lo)+(hi-lo)*(coeff[1]+2*coeff[2]*lo)/2,value(hi))
        reconstructed=(beta[0],2*(beta[1]-beta[0]),beta[0]-2*beta[1]+beta[2])
        substituted=(value(lo),(hi-lo)*(coeff[1]+2*coeff[2]*lo),(hi-lo)*(hi-lo)*coeff[2])
        require(reconstructed==substituted and coeff[2]<=0,'Coupled quadratic identity/concavity fails')
        margin=min(beta[0],beta[2])
        require(margin>0 and beta[1]>=margin,'Closed signed remote interval is not excluded')
        remote_margins.append(margin);audit.extend(list(beta)+[beta[1]-margin])
    transport=sum((p['weight']*p['norm_upper']*(p['source_height_upper']*a+p['kappa_upper']*delta
                   +Q(rhi)*(a*a+delta*delta)/2) for p in pi),Q())
    margins['even_full_shadow_half_turn']=gap-transport-m.G*epsilon*epsilon/2
    _,composition_upper=root((a+delta)*(a+delta)+epsilon*epsilon,audit)
    theta=min(epsilon+Q(F(101,100))*(a+delta),Q(F(101,100))*composition_upper)
    margins['roll_chord_domain']=Q(F(1,10))-epsilon
    torque=Q(m.local.C*m.local.M)*(delta+theta/2)
    margins['translated_torque']=1-3*torque*torque
    require(all(x>0 for x in margins.values()),'Zero-height receiving criterion fails')
    audit.extend(margins.values())
    return {'F_lower':flower,'source_chord_upper':a,'receiver_chord_upper':delta,
            'residual_angle_upper':epsilon,'full_angle_upper':theta,
            'minimum_remote_margin':min(remote_margins),'minimum_inverse_bracket_margin':min(brackets),
            'positive_margins':margins}

def receiving_cone(corners,normals,audit):
    count=0
    for index in [11,12,13]:
        for u in corners:
            value=-dot(normals[index],u)
            require(value>=0,'Receiving triangle leaves the one-sided cone');audit.append(value);count+=1
    return count

def rodrigues_controls():
    # Exact definition-level checks; the general continuous identity is proved in PROOF.md.
    def rd(a,b):return sum((x*y for x,y in zip(a,b)),F())
    def rc(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
    n0=(F(),F(),F(1));mu=(F(2),F(1),F());w=(F(3),F(-2),F(5));w0=w[:2]+(F(),)
    count=0
    for axis,t in itertools.product([(F(1),F(),F()),(F(3,5),F(4,5),F())],[F(),F(1,20),F(-1,20)]):
        c=(1-t*t)/(1+t*t);s=2*t/(1+t*t);delta2=2-2*c;e=rc(axis,n0)
        def rotate(v):
            av=rd(axis,v);cv=rc(axis,v)
            return tuple(c*v[i]+(1-c)*av*axis[i]+s*cv[i] for i in range(3))
        n=rotate(n0);actual=rd(rotate(mu),w)
        signed=rd(mu,w)-rd(w,n0)*rd(mu,n)-delta2*rd(mu,e)*rd(w,e)/2
        require(actual==signed,'Signed receiving Rodrigues identity fails')
        inv_axis=tuple(-x for x in axis);av=rd(inv_axis,w0);cv=rc(inv_axis,w0)
        transported=tuple(c*w0[i]+(1-c)*av*inv_axis[i]+s*cv[i] for i in range(3))
        projection_difference=tuple(transported[i]-w0[i] if i<2 else F() for i in range(3))
        expected=tuple(-delta2*rd(w0,e)*e[i]/2 for i in range(3))
        require(projection_difference==expected,'Zero-height source Rodrigues identity fails')
        require(rd(expected,expected)<=delta2*delta2*rd(w0,w0)/4,'Zero-height quadratic remainder fails')
        count+=1
    return count

def controls(data,normals,nlo,nhi,corners,remote):
    missing=remote[:-1];wrong_weight=json.loads(json.dumps(data));wrong_weight['late_convex_weight']=['1','0']
    bad_split=json.loads(json.dumps(data));bad_split['late_split']='3/5'
    bad_cone=[D,(Q(),Q(F(-9,10)),D[2]),corners[2]]
    tests=[lambda:convex_difference([[8,15],[8,14]],Q(-1),[]),
           lambda:convex_difference([[8,15],[8,14]],Q(F(1,2)),[]),
           lambda:convex_difference([[8,55],[8,14]],Q(7,-1)/22,[]),
           lambda:structures(wrong_weight,normals,nlo,nhi,[]),
           lambda:structures(bad_split,normals,nlo,nhi,[]),lambda:cover_shape(missing),
           lambda:signed_envelopes(normals,nlo,[],True),lambda:receiving_cone(bad_cone,normals,[]),
           lambda:m.residual_inverse(Q(1),Q(1),Q(1),[]),
           lambda:m.old.root_check(Q(F(1,2)),F(1),F(1),[])]
    for test in tests:
        try:test()
        except ValueError:pass
        else:raise ValueError('Malformed zero-height evidence accepted')
    return len(tests)

def check(data,self_test=False):
    pins=dependency_pins();audit=[]
    require(data['height_gap_unit_chord_range']=='1/20' and data['subdivision_depth']==2,
            'Wrong signed receiving range or cover depth')
    corners,critical,area=m.old.geometry_fixture(data)
    require(corners==[D,(Q(),Q(F(-13,11)),D[2]),(Q(F(1,10)),Q(F(-25,24)),D[2])]
            and critical==11,'Wrong receiving macrotriangle')
    require(len(V)==55 and all(dot(v,v)==m.caps.R2 for v in V),'Wrong actual body sphere')
    require({(-v[0],v[1],v[2]) for v in V}==set(V) and {m.sharp.rotate(v) for v in V}==set(V),
            'Actual required body symmetries fail')
    normals=m.caps.reference_geometry(audit)[0];cone_checks=receiving_cone(corners,normals,audit)
    nlo,nhi=root(N,audit);_,rhi=root(m.caps.R2,audit);_,c0hi=root(m.caps.B,audit)
    rholo,_=root(Q(233,-10)/596,audit)
    signed,pair_checks,excess,envelope_digest=signed_envelopes(normals,nlo,audit)
    width={index:signed[index,1] for index in [11,12,13]}
    heights,old_width,pi,gap,pc,ec,sc,se=m.old.transport_data(normals,RANGE,nlo,audit)
    even_comparisons=m.even_stress(normals,pi,m.G,audit)
    first,remote,points=structures(data,normals,nlo,nhi,audit)
    constants=(width,pi,gap,rhi,c0hi,rholo,nlo)
    core=[v for v in V if scale(-1,v) in V];require(len(core)==50,'Wrong antipodal core')
    for v in core:
        values=[dot(v,u) for u in corners]
        require(all(x>0 for x in values) or all(x<0 for x in values),'Common axial signs fail')
        audit.extend(values)
    triangles,parents=m.closed_partition(corners,2)
    vertices=sorted({u for t in triangles for u in t},key=lambda u:tuple((x.a,x.b) for x in u))
    parameters={u:m.old.corner_parameters(u,core,audit) for u in vertices}
    phases=[]
    for t in triangles:
        ps=[parameters[u] for u in t]
        phases.append(phase(min(p[0] for p in ps),max(p[1] for p in ps),constants,(first,remote),audit))
    probes=m.local.make_probes();torque_digest=m.actual_torque_balances(probes,audit)
    supports,diameters,replays,smin,dmin=m.old.whole_triangle(corners,critical,probes,audit)
    prior_corners,_,prior_area=m.old.geometry_fixture(json.loads((REPO/parent['source_directory']/'certificates.json').read_text()))
    prior_weights=[(Q(1),Q(),Q()),(Q(),Q(1),Q()),(Q(F(37,108)),Q(F(11,108)),Q(F(5,9)))]
    for u,ws in zip(prior_corners,prior_weights):
        require(sum(ws,Q())==1 and all(w>=0 for w in ws),'Invalid old triangle convex inclusion')
        require(tuple(sum((w*v[k] for w,v in zip(ws,corners)),Q()) for k in range(3))==u,
                'Earlier whole triangle is not contained')
    require(area==Q(F(1,110)) and area/prior_area==Q(F(9,5)),'Wrong fixed-chart area extension')
    stream=[[[[encode(x) for x in u] for u in t],m.encoded_phase(r)] for t,r in zip(triangles,phases)]
    digest=hashlib.sha256(json.dumps(stream,separators=(',',':')).encode()).hexdigest()
    bounds=[min(p['F_lower'] for p in phases)-Q(F(83,250)),
            Q(F(17,200))-max(p['source_chord_upper'] for p in phases),
            Q(F(187,5000))-max(p['receiver_chord_upper'] for p in phases),
            Q(F(9,500))-max(p['residual_angle_upper'] for p in phases),
            Q(F(111,1000))-max(p['full_angle_upper'] for p in phases),
            min(p['minimum_remote_margin'] for p in phases)-Q(F(3,125))]
    require(all(x>0 for x in bounds),'Advertised exact rational cover bounds fail');audit.extend(bounds)
    identity_terms=m.composition_identity();frames=m.frame_audits();rodrigues=rodrigues_controls()
    rejected=controls(data,normals,nlo,nhi,corners,remote) if self_test else 10
    unique=sorted(set(audit),key=lambda x:(x.a,x.b));m.local.independent_sign_audit(unique)
    return {'agent':'six-rupert-2','role':'researcher','claim_status':'zero_height_supports_one_sided_widths_entire_closed_J77_triangle',
            'global_Rupert_resolved':False,'independent_review_asserted':False,
            'all_source_orientations_rolls_translations':True,'scales_covered':'lambda >= 1',
            'closed_equality_forms':['Q=R^k','Q=M_n X R^k'],'closed_scale':1,'closed_translation':0,
            'whole_triangle_fixed_z_chart_area':encode(area),'previous_triangle_area_ratio':encode(area/prior_area),
            'previous_whole_triangle_contained':True,'zero_height_source_differences':[[encode(x) for x in w] for w in points],
            'signed_receiver_branch_records':6,'signed_receiver_original_pair_checks':pair_checks,
            'signed_receiver_excess_checks':excess,'signed_receiver_envelope_sha256':envelope_digest,
            'whole_triangle_receiving_cone_checks':cone_checks,'whole_triangle_common_core_signs':len(core),
            'complete_closed_pieces':len(triangles),'split_parent_triangles':parents,'unique_cover_vertex_rays':len(vertices),
            'residual_inverse_branch_checks':2*len(phases),'remote_closed_interval_checks':10*len(phases),
            'remote_Bernstein_coefficients':30*len(phases),'advertised_rational_cover_bounds':len(bounds),
            'piece_parameter_extrema':{k:{'minimum':encode(min(p[k] for p in phases)),
                                         'maximum':encode(max(p[k] for p in phases))}
                                       for k in ['F_lower','source_chord_upper','receiver_chord_upper','residual_angle_upper','full_angle_upper']},
            'minimum_remote_margin':encode(min(p['minimum_remote_margin'] for p in phases)),
            'minimum_inverse_bracket_margin':encode(min(p['minimum_inverse_bracket_margin'] for p in phases)),
            'minimum_piece_positive_margins':{k:encode(min(p['positive_margins'][k] for p in phases)) for k in phases[0]['positive_margins']},
            'whole_triangle_support_Bernstein_coefficients':supports,'whole_triangle_diameter_Bernstein_coefficients':diameters,
            'whole_triangle_minimum_support_coefficient':encode(smin),'whole_triangle_minimum_diameter_coefficient':encode(dmin),
            'independent_actual_plane_barycenter_replays':replays,
            'retained_full_width_support_comparisons':pc,'retained_absolute_width_excess_checks':ec,
            'retained_half_turn_support_comparisons':sc,'retained_half_turn_excess_checks':se,
            'even_half_turn_original_minimum_comparisons':even_comparisons,
            'positive_torque_combination_sha256':torque_digest,'signed_translated_torque_balances':6,
            'perpendicular_composition_identity_terms':identity_terms,'exact_proper_frame_gauge_audits':frames,
            'exact_definition_level_Rodrigues_audits':rodrigues,'malformed_controls_with_self_test':rejected,
            'new_sign_records':len(audit),'new_independent_rational_sign_audits':len(unique)+9,
            'pinned_dependency_files':len(pins),'full_regional_parent_replayed_in_this_run':False,
            'full_adaptive_parent_replayed_in_this_run':False,
            'complete_cover_bounds_sha256':digest,
            'canonical_certificate_sha256':hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    print(json.dumps(check(json.loads((ROOT/'certificates.json').read_text()),args.self_test),indent=2,sort_keys=True))
