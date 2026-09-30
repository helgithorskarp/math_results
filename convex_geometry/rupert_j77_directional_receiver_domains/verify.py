#!/usr/bin/env python3
"""Exact directional J77 receiver domains; standard-library Python 3.11+."""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,importlib.util,itertools,json,sys

ROOT=Path(__file__).resolve().parent
def require(c,message):
    if not c:raise ValueError(message)
manifest=json.loads((ROOT/'dependencies.json').read_text())
require(manifest['source_directory']=='convex_geometry/rupert_j77_all_source_diameter_caps'
        and manifest['source_commit']=='97ce8ace4dd4398a9f397428ccc9758ed5e1b028','Wrong direct dependency')
require(set(manifest['sha256'])=={'.gitignore','README.md','PROOF.md','verify.py','certificates.json','dependencies.json','expected.json'},
        'Incomplete direct dependency manifest')
PRIOR=ROOT.parent.parent/manifest['source_directory']
for name,digest in manifest['sha256'].items():
    require(hashlib.sha256((PRIOR/name).read_bytes()).hexdigest()==digest,'Changed direct dependency: '+name)
spec=importlib.util.spec_from_file_location('j77_directional_caps_dependency',PRIOR/'verify.py')
caps=importlib.util.module_from_spec(spec);spec.loader.exec_module(caps)
Q,V,D,N=caps.Q,caps.VERTICES,caps.D,caps.N
dot,sub,scale=caps.dot,caps.sub,caps.scale
local=caps.local
ROLL=json.loads((PRIOR/'certificates.json').read_text())
GRID=10**12
def encode(x):return [str(x.a),str(x.b)]
def decode(x):return Q(*x)
def absq(x):return x if x>=0 else -x
def root_check(q,lo,hi,audit):
    lo,hi=F(lo),F(hi)
    require(0<=lo<=hi and Q(lo)*Q(lo)<=q<=Q(hi)*Q(hi),'Invalid outward square-root enclosure')
    audit.extend([q-Q(lo)*Q(lo),Q(hi)*Q(hi)-q])
def root(q,audit):
    require(0<=q<=1024,'Radicand outside fixed grid domain')
    lo=0;hi=32*GRID+1
    while hi-lo>1:
        mid=(lo+hi)//2;x=Q(F(mid,GRID))
        if x*x<=q:lo=mid
        else:hi=mid
    lower=F(lo,GRID);upper=lower if Q(lower)*Q(lower)==q else F(hi,GRID)
    root_check(q,lower,upper,audit)
    return lower,upper
def geometry_fixture(data):
    require(data['root_grid_denominator']==GRID,'Unsupported root grid')
    triangle=data['triangle'];require(len(triangle)==3,'Missing closed triangle corner')
    corners=[tuple(decode(x) for x in u) for u in triangle]
    require(all(len(u)==3 for u in corners) and corners[0]==D,'Wrong triangle dimensions or anchor')
    require(all(u[2]==D[2] for u in corners),'Triangle leaves the stated affine chart')
    area=(corners[1][0]-D[0])*(corners[2][1]-D[1])-(corners[1][1]-D[1])*(corners[2][0]-D[0])
    require(area>0,'Triangle is degenerate or reversed')
    index=data['diameter_core_vertex']
    require(type(index) is int and 0<=index<55 and scale(-1,V[index]) in V,'Invalid critical core antipodal pair')
    return corners,index,area/2
def corner_parameters(u,core,audit):
    u2=dot(u,u);positive_dot=dot(D,u)
    require(u2>0 and positive_dot>0,'Invalid directed receiver ray')
    _,norm_hi=root(u2,audit)
    _,den_hi=root(u2*N,audit)
    axial=min(absq(dot(v,u)) for v in core)
    flower=axial/norm_hi
    delta2=2-2*positive_dot/den_hi
    require(delta2>=0,'Inconsistent upper receiver chord')
    _,delta_hi=root(delta2,audit)
    return flower,Q(delta_hi)
def transport_data(normals,receiver_range,nlo,audit):
    heights=[dot(D,v) for v in V]
    roll_ids=sorted({p['probe'] for c in ROLL['covers'] for p in c['pieces']})
    width_data={};pair_checks=excess_checks=0
    for index in roll_ids:
        m=normals[index];values=[dot(m,v) for v in V];maximum,minimum=max(values),min(values)
        plus=[i for i,x in enumerate(values) if x==maximum];minus=[i for i,x in enumerate(values) if x==minimum]
        raw=max(absq(heights[i]-heights[j]) for i in plus for j in minus)
        _,mh=root(dot(m,m),audit);width=maximum-minimum
        for i,j in itertools.product(range(55),repeat=2):
            gap=width-values[i]+values[j];dh=absq(heights[i]-heights[j]);pair_checks+=1
            require(gap>=0,'Incorrect full reference difference support');audit.append(gap)
            if dh>raw:
                margin=gap-Q(mh)*receiver_range*(dh-raw)/nlo
                require(margin>0,'Difference support height-gap range fails')
                audit.append(margin);excess_checks+=1
        width_data[index]={'norm_upper':Q(mh),'kappa_upper':raw/nlo,'plus':plus,'minus':minus,
                           'tie_height_raw':raw}
    pi_data=[];single_checks=single_excess=0
    weights=[decode(w) for w in ROLL['half_turn_weights']]
    gap=Q()
    require(sum(weights,Q())==1 and all(w>0 for w in weights),'Invalid inherited half-turn weights')
    require(all(sum((w*normals[i][k] for w,i in zip(weights,ROLL['half_turn_indices'])),Q())==0 for k in range(3)),
            'Inherited half-turn stress fails full normal balance')
    for weight,index in zip(weights,ROLL['half_turn_indices']):
        m=normals[index];values=[dot(m,v) for v in V];maximum,minimum=max(values),min(values)
        require(maximum==1,'Reference half-turn receiver offset changed')
        plus=[i for i,x in enumerate(values) if x==maximum];minus=[i for i,x in enumerate(values) if x==minimum]
        raw=max(absq(heights[i]) for i in plus)
        source=min(minus,key=lambda i:(absq(heights[i]),i));_,mh=root(dot(m,m),audit)
        for i,value in enumerate(values):
            height=absq(heights[i]);support_gap=maximum-value;single_checks+=1
            require(support_gap>=0,'Incorrect half-turn receiver support');audit.append(support_gap)
            if height>raw:
                margin=support_gap-Q(mh)*receiver_range*(height-raw)/nlo
                require(margin>0,'Half-turn receiver height-gap range fails');audit.append(margin);single_excess+=1
        pi_data.append({'probe':index,'weight':weight,'norm_upper':Q(mh),'source_vertex':source,
                        'source_height_upper':absq(heights[source])/nlo,'kappa_upper':raw/nlo})
        gap+=weight*(-minimum-1)
    require(gap==Q(-151,74)/241,'Half-turn weighted gap changed')
    return heights,width_data,pi_data,gap,pair_checks,excess_checks,single_checks,single_excess
def criterion(flower,delta,receiver_range,heights,width_data,pi_data,pi_gap,rhi,c0hi,rholo,nlo,normals,audit):
    require(flower>0 and delta>=0,'Invalid normalized receiver parameters')
    a=Q(F(101,100))*(Q(c0hi)-flower)/rholo
    require(a>=0,'Negative source alignment bound')
    theta=Q(F(1,25))+Q(F(101,100))*(a+delta)
    margins={'winning_region':flower*flower-decode(ROLL['beta']),
             'receiver_height_gap_domain':receiver_range-delta,
             'source_chord_domain':Q(F(1,10))-a,'receiver_chord_domain':Q(F(1,10))-delta}
    roll_margins=[]
    for cover in ROLL['covers']:
        for piece in cover['pieces']:
            record=width_data[piece['probe']];i,j=piece['source_pair']
            h=absq(heights[i]-heights[j])/nlo
            gamma=caps.quadratic_piece(cover['sign'],piece,normals,
                                       Q(F(ROLL['root_N_enclosure'][0])),Q(F(ROLL['root_N_enclosure'][1])),
                                       Q(F(ROLL['gap_numerator_lower_bound'])),audit)
            error=record['norm_upper']*(h*a+record['kappa_upper']*delta+Q(rhi)*(a*a+delta*delta))
            upper_endpoint=F(piece['interval'][1]);margin=gamma-Q(1+upper_endpoint*upper_endpoint)*error
            require(margin>0,'Closed remote-roll piece is not excluded')
            roll_margins.append(margin);audit.append(margin)
    error=sum((p['weight']*p['norm_upper']*(p['source_height_upper']*a+p['kappa_upper']*delta
              +Q(rhi)*(a*a+delta*delta)/2+Q(rhi)/25) for p in pi_data),Q())
    margins['half_turn']=pi_gap-error
    torque_error=Q(local.C*local.M)*(delta+theta/2)
    margins['translated_torque']=1-3*torque_error*torque_error
    require(all(x>0 for x in margins.values()),'Directional receiver criterion fails')
    audit.extend(margins.values())
    return {'F_lower':encode(flower),'receiver_chord_upper':encode(delta),'source_chord_upper':encode(a),
            'full_angle_upper':encode(theta),'positive_margins':{k:encode(v) for k,v in margins.items()},
            'minimum_remote_roll_margin':encode(min(roll_margins))}
def whole_triangle(corners,critical,probes,audit):
    # Cache evaluations of linear forms, then build all six quadratic Bernstein coefficients.
    vertex_values=[[dot(v,u) for u in corners] for v in V]
    gram=[[dot(u,w) for w in corners] for u in corners]
    barycenter=tuple(sum((u[k] for u in corners),Q())/3 for k in range(3));barynorm=dot(barycenter,barycenter)
    supports=[];diameters=[];replays=0
    for i,m in probes:
        m_values=[dot(m,u) for u in corners]
        projected= sub(m,scale(dot(m,barycenter)/barynorm,barycenter))
        for j in range(55):
            if i==j:continue
            z=sub(V[i],V[j]);gap=dot(m,z);z_values=[vertex_values[i][k]-vertex_values[j][k] for k in range(3)]
            coefficients=[]
            for k,l in itertools.combinations_with_replacement(range(3),2):
                value=gap*gram[k][l]-(m_values[k]*z_values[l]+m_values[l]*z_values[k])/2
                require(value>0,'Actual receiver support is not valid on closed triangle')
                coefficients.append((k,l,value));audit.append(value)
            assembled=sum((value*(1 if k==l else 2) for k,l,value in coefficients),Q())/9
            direct=barynorm*dot(projected,z)
            require(assembled==direct,'Independent actual-plane support replay differs')
            replays+=1;supports.extend(v for k,l,v in coefficients)
    for i,j in itertools.combinations(range(55),2):
        if V[j]==scale(-1,V[i]):continue
        z=sub(V[i],V[j]);z2=dot(z,z);z_values=[vertex_values[i][k]-vertex_values[j][k] for k in range(3)]
        coefficients=[]
        for k,l in itertools.combinations_with_replacement(range(3),2):
            value=(4*caps.R2-z2)*gram[k][l]+z_values[k]*z_values[l]-4*vertex_values[critical][k]*vertex_values[critical][l]
            require(value>0,'Full-body diameter reduction fails on closed triangle')
            coefficients.append((k,l,value));audit.append(value)
        assembled=sum((value*(1 if k==l else 2) for k,l,value in coefficients),Q())/9
        pair_diameter=z2-dot(z,barycenter)*dot(z,barycenter)/barynorm
        core_diameter=4*caps.R2-4*dot(V[critical],barycenter)*dot(V[critical],barycenter)/barynorm
        require(assembled==barynorm*(core_diameter-pair_diameter),'Independent physical diameter replay differs')
        replays+=1;diameters.extend(v for k,l,v in coefficients)
    require(len(supports)==11016 and len(diameters)==8760 and replays==3296,'Incomplete quadratic patch checks')
    return len(supports),len(diameters),replays,min(supports),min(diameters)
def self_tests(data,core,normals,constants):
    def copy():return json.loads(json.dumps(data))
    missing=copy();missing['triangle'].pop()
    reversed_triangle=copy();reversed_triangle['triangle'][1],reversed_triangle['triangle'][2]=reversed_triangle['triangle'][2],reversed_triangle['triangle'][1]
    bad_grid=copy();bad_grid['root_grid_denominator']=0
    bad_pair=copy();bad_pair['diameter_core_vertex']=54
    wide=copy();wide['triangle'][2][0]=['1/50','0']
    bad_range=Q(F(1,2))
    heights,width,pi,gap,rhi,c0hi,rholo,nlo=constants
    def wide_test():
        corners,index,area=geometry_fixture(wide)
        parameters=[corner_parameters(u,core,[]) for u in corners]
        criterion(min(p[0] for p in parameters),max(p[1] for p in parameters),Q(F(1,20)),
                  heights,width,pi,gap,rhi,c0hi,rholo,nlo,normals,[])
    invalid=[lambda:geometry_fixture(missing),lambda:geometry_fixture(reversed_triangle),lambda:geometry_fixture(bad_grid),
             lambda:geometry_fixture(bad_pair),wide_test,lambda:transport_data(normals,bad_range,nlo,[]),
             lambda:root_check(Q(2),F(3,2),F(3,2),[]),lambda:root(Q(1025),[])]
    for test in invalid:
        try:test()
        except ValueError:pass
        else:raise ValueError('Malformed directional certificate accepted')
    for q,answer in ((Q(),F(0)),(Q(1),F(1)),(Q(4),F(2)),(Q(1024),F(32))):
        require(root(q,[])==(answer,answer),'Square-root endpoint control fails')
    return len(invalid)
def check(data,self_test=False):
    inherited=caps.check(ROLL,self_test)
    require(inherited==json.loads((PRIOR/'expected.json').read_text()),'Full inherited all-source replay differs')
    audit=[];corners,critical,area=geometry_fixture(data)
    receiver_range=Q(F(data['height_gap_unit_chord_range']))
    require(0<receiver_range<1,'Invalid receiver transport range')
    rlo,rhi=root(caps.R2,audit);c0lo,c0hi=root(caps.B,audit);rholo,rhohi=root(Q(233,-10)/596,audit)
    nlo,nhi=root(N,audit);llo,lhi=root(caps.R2-caps.B,audit)
    require(nlo>0 and rholo>0,'Zero radical denominator')
    normals=caps.reference_geometry(audit)[0]
    heights,width,pi,gap,pair_checks,excess,single_checks,single_excess=transport_data(normals,receiver_range,nlo,audit)
    _,core,_,_,_=caps.cupola_construction();core=[v for v in V if v in core]
    parameters=[corner_parameters(u,core,audit) for u in corners]
    common_signs=0
    for v in core:
        values=[dot(v,u) for u in corners]
        require(all(x>0 for x in values) or all(x<0 for x in values),'Axial signs do not persist on whole triangle')
        audit.extend(values);common_signs+=1
    triangle_criterion=criterion(min(p[0] for p in parameters),max(p[1] for p in parameters),receiver_range,
                               heights,width,pi,gap,rhi,c0hi,rholo,nlo,normals,audit)
    sc,dc,replays,smin,dmin=whole_triangle(corners,critical,local.make_probes(),audit)
    denlo,denhi=root(dot(corners[1],corners[1])*N,audit)
    beyond=2-2*dot(D,corners[1])/denlo-Q(F(1,60))*Q(F(1,60))
    require(beyond>0,'Triangle does not extend beyond the claimed chord');audit.append(beyond)
    cap=Q(F(data['cap_unit_chord']));require(0<cap<=Q(local.DELTA),'Unsupported complete-cap receiver support domain')
    lower=Q(c0lo)*(1-cap*cap/2)-Q(lhi)*cap
    cap_criterion=criterion(lower,cap,receiver_range,heights,width,pi,gap,rhi,c0hi,rholo,nlo,normals,audit)
    nonpaired=Q(901,-125)/1490
    cap_margins=[nonpaired-16*caps.R2*cap,Q(local.GAP)-2*Q(local.M)*cap,
                 Q(local.THETA)-decode(cap_criterion['full_angle_upper'])]
    require(all(x>0 for x in cap_margins),'Complete-cap diameter/support/angle condition fails');audit.extend(cap_margins)
    constants=(heights,width,pi,gap,rhi,c0hi,rholo,nlo)
    new_controls=self_tests(data,core,normals,constants) if self_test else 8
    signs=sorted(set(audit),key=lambda x:(x.a,x.b));local.independent_sign_audit(signs)
    return {'agent':'six-rupert-2','role':'researcher','claim_status':'J77_directional_all_source_closed_receiver_domains',
            'global_Rupert_resolved':False,'all_source_orientations_rolls_translations':True,'scales_covered':'lambda >= 1',
            'closed_equality_forms':['Q=R^k','Q=M_n X R^k'],'closed_scale':1,'closed_translation':0,
            'root_grid_denominator':GRID,'receiver_height_gap_unit_chord_range':str(receiver_range.a),
            'complete_cap_unit_chord':str(cap.a),'complete_cap_radius_factor_over_prior':10,
            'complete_cap_criterion':cap_criterion,'cap_support_diameter_angle_margins':[encode(v) for v in cap_margins],
            'whole_triangle_criterion':triangle_criterion,'whole_triangle_chart_area':encode(area),
            'whole_triangle_common_core_signs':common_signs,'triangle_corner_chord_strict_lower_bound':'1/60',
            'triangle_extension_squared_chord_margin':encode(beyond),
            'whole_triangle_support_Bernstein_coefficients':sc,'whole_triangle_diameter_Bernstein_coefficients':dc,
            'whole_triangle_minimum_support_coefficient':encode(smin),'whole_triangle_minimum_diameter_coefficient':encode(dmin),
            'independent_actual_plane_barycenter_replays':replays,'difference_support_pair_checks':pair_checks,
            'difference_excess_height_checks':excess,'half_turn_support_vertex_checks':single_checks,
            'half_turn_excess_height_checks':single_excess,'half_turn_source_vertices':[p['source_vertex'] for p in pi],
            'remote_roll_pieces_per_criterion':12,'remote_quadratic_Bernstein_coefficients_per_criterion':36,
            'new_sign_records':len(audit),'new_independent_rational_sign_audits':len(signs)+9,
            'malformed_controls_with_self_test':new_controls+12,'exact_root_endpoint_controls':4,
            'inherited_canonical_certificate_sha256':inherited['canonical_certificate_sha256'],
            'canonical_certificate_sha256':hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    print(json.dumps(check(json.loads((ROOT/'certificates.json').read_text()),args.self_test),indent=2,sort_keys=True))
