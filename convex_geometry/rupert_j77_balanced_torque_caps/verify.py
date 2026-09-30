#!/usr/bin/env python3
"""Exact translated normalized torque and source-directional J77 cap proof."""
import argparse,hashlib,importlib.util,itertools,json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent.parent
def require(ok,message):
    if not ok:raise ValueError(message)
manifest=json.loads((ROOT/'dependencies.json').read_text())
require(len(manifest['sources'])==1,'Missing direct parent')
parent=manifest['sources'][0]
require(parent['source_directory']=='convex_geometry/rupert_j77_zero_height_supports'
        and parent['source_commit']=='afef1a458b006eb92866fb3d24c6bf99eee1590b','Wrong parent')
require(set(parent['sha256'])=={'.gitignore','README.md','PROOF.md','verify.py','certificates.json','dependencies.json','expected.json'},'Incomplete parent pins')
for name,digest in parent['sha256'].items():
    require(hashlib.sha256((REPO/parent['source_directory']/name).read_bytes()).hexdigest()==digest,'Changed direct parent')
spec=importlib.util.spec_from_file_location('j77_balanced_zero_parent',REPO/parent['source_directory']/'verify.py')
z=importlib.util.module_from_spec(spec);spec.loader.exec_module(z)
m=z.m;Q=z.Q;V=z.V;D=z.D;N=z.N
dot,cross,sub,scale,add=z.dot,z.cross,z.sub,z.scale,z.add
encode,decode,root,absq=m.encode,m.decode,m.root,m.absq
def digest(value):return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()
def pins():
    result=z.dependency_pins()
    for name,d in parent['sha256'].items():result[parent['source_directory']+'/'+name]=d
    require(len(result)==50,'Incomplete50file dependency boundary')
    return result
def solve(columns,target):
    n=len(target);require(len(columns)==n and all(len(c)==n for c in columns),'Wrong exact square dimensions')
    a=[[columns[j][i] for j in range(n)]+[Q(target[i])] for i in range(n)]
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]!=0),None)
        require(k is not None,'Singular witness basis')
        a[j],a[k]=a[k],a[j];div=a[j][j];a[j]=[x/div for x in a[j]]
        for k in range(n):
            if k!=j:
                factor=a[k][j];a[k]=[x-factor*y for x,y in zip(a[k],a[j])]
    weights=[row[-1] for row in a]
    require(all(sum((weights[j]*columns[j][i] for j in range(n)),Q())==Q(target[i]) for i in range(n)),'Independent linear identity replay fails')
    return weights
def balanced_point(indices,probes,costs,audit,override=None):
    require(len(indices)==3 and len(set(indices))==3 and all(type(i) is int and 0<=i<34 for i in indices),'Invalid original probe triple')
    columns=[(probes[i][1][0]/costs[i],probes[i][1][1]/costs[i],Q(1)) for i in indices]
    weights=solve(columns,(Q(),Q(),Q(1))) if override is None else override
    require(len(weights)==3 and all(w>=0 for w in weights) and sum(weights,Q())==1,'Not a positive normalized stress')
    require(all(sum((w*probes[i][1][k]/costs[i] for i,w in zip(indices,weights)),Q())==0 for k in range(3)),'Physical translation normal balance fails')
    point=tuple(sum((w*cross(V[probes[i][0]],probes[i][1])[k]/costs[i] for i,w in zip(indices,weights)),Q()) for k in range(3))
    audit.extend(weights)
    return point,weights
def center_hull(triples,probes,audit):
    costs=[]
    for i,p in probes:
        lo,hi=root(m.caps.R2*dot(p,p),audit);require(hi>0,'Invalid positive contact cost')
        costs.append(Q(hi))
    points=[];stresses=[]
    for ids in triples:
        point,weights=balanced_point(ids,probes,costs,audit)
        points.append(point);stresses.append([ids,[encode(w) for w in weights],[encode(x) for x in point]])
    require(len(points)==20 and len(set(points))==20,'Incomplete selected balanced hull')
    rank=False
    for b,c,d in itertools.combinations(points[1:],3):
        if dot(sub(b,points[0]),cross(sub(c,points[0]),sub(d,points[0])))!=0:rank=True;break
    require(rank,'Balanced hull is not full dimensional')
    facets={};comparisons=degenerate=0
    for ids in itertools.combinations(range(20),3):
        a,b,c=[points[i] for i in ids];normal=cross(sub(b,a),sub(c,a));height=dot(normal,a)
        if normal==(Q(),Q(),Q()):degenerate+=1;continue
        gaps=[height-dot(normal,p) for p in points];comparisons+=20;audit.extend(gaps)
        if all(g>=0 for g in gaps) or all(g<=0 for g in gaps):
            if all(g<=0 for g in gaps):normal=scale(-1,normal);height=-height
            require(height>0,'Origin violates an actual outward facet')
            plane=scale(1/height,normal);key=tuple(tuple(encode(x)) for x in plane)
            facets.setdefault(key,plane)
    require(len(facets)==36,'Complete selected hull facet count differs')
    margins=[1-dot(plane,plane)/49 for plane in facets.values()]
    require(all(g>0 for g in margins),'Actual hull does not contain centered1/7ball')
    audit.extend(margins)
    records=sorted([[[str(x.a),str(x.b)] for x in plane] for plane in facets.values()])
    return costs,{'selected_points':20,'all_selected_triples':1140,'degenerate_triples':degenerate,
                  'side_comparisons':comparisons,'actual_facets':36,'minimum_squared_ball_margin':encode(min(margins)),
                  'normalized_stress_sha256':digest(stresses),'complete_facet_sha256':digest(records)}
def tangent_gauges(points,claimed,audit):
    core=[v for v in V if scale(-1,v) in V];h=min(absq(dot(D,v)) for v in core)
    ids=[i for i,v in enumerate(V) if v in core and dot(D,v)==h]
    require(ids==[8,12,30,32] and h==Q(5,1)/4 and h*h/N==m.caps.B,'Wrong winning active contacts')
    negative=[scale(-1,sub(V[i],scale(h/N,D))) for i in ids]
    facets=[]
    for i,j in itertools.combinations(range(4),2):
        normal=cross(sub(negative[j],negative[i]),D);height=dot(normal,negative[i])
        gaps=[height-dot(normal,t) for t in negative];audit.extend(gaps)
        if all(g>=0 for g in gaps) or all(g<=0 for g in gaps):
            if all(g<=0 for g in gaps):normal=scale(-1,normal);height=-height
            require(height>0,'Origin not inside active tangent polygon')
            facets.append((normal,height))
    require(len(facets)==4,'Complete tangent quadrilateral missing')
    gauges={};records=[]
    for index,point in enumerate(points):
        L=max(absq(dot(normal,point))/height for normal,height in facets)
        require(L==claimed[0 if index<2 else 1] and L>0,'Wrong directional source gauge')
        gauges[point]=L
        for sign in [-1,1]:
            target=scale(Q(sign)/L,point);found=None
            for triple in itertools.combinations(range(4),3):
                w=solve([(negative[i][0],negative[i][1],Q(1)) for i in triple],(target[0],target[1],Q(1)))
                if all(x>=0 for x in w):found=triple,w;break
            require(found is not None,'Directional point has no positive active-contact construction')
            triple,w=found
            require(sum(w,Q())==1 and all(sum((a*negative[i][k] for i,a in zip(triple,w)),Q())==target[k] for k in range(3)),'Directional physical convex identity fails')
            audit.extend(w);records.append([index,sign,list(triple),[encode(x) for x in w]])
    require(Q(F(101,100))*Q(F(101,100))*Q(F(399,400))>1,'Source chord/radical factor invalid')
    return gauges,{'active_contact_indices':ids,'complete_tangent_edges':4,'signed_convex_constructions':8,
                    'first_source_gauge':encode(claimed[0]),'late_source_gauge':encode(claimed[1]),
                    'directional_convex_sha256':digest(records)}
def receiving_cap(probes,delta,nlo,nhi,audit):
    supports=[];diameters=[]
    for vertex,p in probes:
        _,eta=root(dot(p,p),audit);eta=Q(eta)
        for j,v in enumerate(V):
            if vertex==j:continue
            diff=sub(V[vertex],v);_,length=root(dot(diff,diff),audit)
            height=absq(dot(D,diff))/nlo
            margin=dot(p,diff)-eta*delta*(height+Q(length)*delta)
            require(margin>0,'Actual original support does not persist on entire cap')
            supports.append(margin)
    d0=4*(m.caps.R2-m.caps.B)
    for i in range(55):
        for j in range(i):
            if V[i]==scale(-1,V[j]):continue
            diff=sub(V[i],V[j]);square=dot(diff,diff);_,length=root(square,audit)
            height=max(Q(),absq(dot(D,diff))/nhi-Q(length)*delta)
            margin=d0-square+height*height
            require(margin>0,'Full-body diameter identity not certified on cap')
            diameters.append(margin)
    require(len(supports)==1836 and len(diameters)==1460,'Incomplete original cap comparisons')
    audit.extend(supports+diameters)
    return {'support_comparisons':len(supports),'nonantipodal_diameter_comparisons':len(diameters),
            'minimum_support_margin':encode(min(supports)),'minimum_diameter_margin':encode(min(diameters)),
            'whole_cap_comparison_sha256':digest([[encode(x) for x in supports],[encode(x) for x in diameters]])}
def selected_error(piece,a,delta,width,nlo,rhi,deficit,gauges):
    rec=width[piece['probe']];point=piece['point'];h=absq(dot(D,point))/nlo
    source=Q(rhi)*a*a
    if point in gauges:
        require(h==0,'Directional quadratic used at nonzero height')
        source=min(source,Q(F(101,200))*a*gauges[point]*deficit)
    return rec['norm_upper']*(h*a+rec['kappa_upper']*delta+source+Q(rhi)*delta*delta)
def complete_phase(flower,delta,constants,structure,gauges,audit):
    width,pi,gap,rhi,c0hi,rholo,nlo=constants;first,remote=structure
    deficit=Q(c0hi)-flower;a=Q(F(101,100))*deficit/rholo
    require(deficit>=0 and 0<=a<Q(F(1,10)) and 0<=delta<Q(F(1,20)),'Source/chord hypothesis outside proved range')
    margins={'sharp_source_gap':flower*flower-Q(F(1,12))};epsilon_bounds=[];brackets=[]
    for sign,p,K,T in first:
        E=selected_error(p,a,delta,width,nlo,rhi,deficit,gauges)
        epsilon,bracket=m.residual_inverse(K,T,E,audit);epsilon_bounds.append(epsilon);brackets.append(bracket)
    epsilon=max(epsilon_bounds);remote_margins=[];bernstein=[]
    for sign,p,c in remote:
        E=selected_error(p,a,delta,width,nlo,rhi,deficit,gauges);coeff=(c[0]-E,c[1],c[2]-E)
        lo,hi=[Q(F(x)) for x in p['interval']];value=lambda x:coeff[0]+x*(coeff[1]+x*coeff[2])
        beta=(value(lo),value(lo)+(hi-lo)*(coeff[1]+2*coeff[2]*lo)/2,value(hi))
        reconstructed=(beta[0],2*(beta[1]-beta[0]),beta[0]-2*beta[1]+beta[2])
        substituted=(value(lo),(hi-lo)*(coeff[1]+2*coeff[2]*lo),(hi-lo)*(hi-lo)*coeff[2])
        require(reconstructed==substituted and coeff[2]<=0,'Coupled closed interval polynomial invalid')
        margin=min(beta[0],beta[2]);require(margin>0 and beta[1]>=margin,'Incomplete signed remote-roll exclusion')
        remote_margins.append(margin);bernstein.extend(beta);audit.extend(list(beta)+[beta[1]-margin])
    transport=sum((p['weight']*p['norm_upper']*(p['source_height_upper']*a+p['kappa_upper']*delta
                   +Q(rhi)*(a*a+delta*delta)/2) for p in pi),Q())
    margins['even_full_shadow_half_turn']=gap-transport-m.G*epsilon*epsilon/2
    _,chord=root((a+delta)*(a+delta)+epsilon*epsilon,audit)
    theta=min(epsilon+Q(F(101,100))*(a+delta),Q(F(101,100))*chord)
    require(epsilon<Q(F(1,10)),'Composition roll outside proved range')
    margins['normalized_translated_torque']=Q(F(1,7))-delta-theta/2
    require(all(g>0 for g in margins.values()),'Source/even/normalized-torque gate fails')
    audit.extend(margins.values())
    # Fixed unrefined source-error barrier is recorded honestly as a failure
    # of that sufficient witness on this cap, not geometric nonexistence.
    oldlast=[]
    for sign,p,c in remote:
        if p['interval']==['13/20','1']:
            oldlast.append(sum(c,Q())-2*z.error(p,a,delta,width,nlo,rhi))
    require(len(oldlast)==2 and all(x<0 for x in oldlast),'Advertised source-coupling barrier is not present')
    audit.extend(oldlast)
    return {'receiver_F_lower':encode(flower),'source_chord_upper':encode(a),'residual_angle_upper':encode(epsilon),
            'full_gauged_angle_upper':encode(theta),'minimum_remote_margin':encode(min(remote_margins)),
            'minimum_inverse_bracket':encode(min(brackets)),
            'margins':{k:encode(v) for k,v in margins.items()},'signed_remote_intervals':len(remote),
            'remote_Bernstein_coefficients':len(bernstein),'old_uncoupled_late_endpoint_margins':[encode(x) for x in oldlast]}
def scope_witness(delta,audit):
    u=(Q(),Q(F(-9,10)),D[2]);square=dot(u,u)
    inside=dot(u,D)*dot(u,D)-(1-delta*delta/2)*(1-delta*delta/2)*square*N
    require(dot(u,D)>0 and inside>0,'Scope ray outside new cap');audit.append(inside)
    old_delta=Q(F(1,200));outside=[];cone_records=[]
    corners=[D,(Q(),Q(F(-13,11)),D[2]),(Q(F(1,10)),Q(F(-25,24)),D[2])]
    center=D
    for k in range(5):
        gap=(1-old_delta*old_delta/2)*(1-old_delta*old_delta/2)*square*N-dot(u,center)*dot(u,center)
        require(gap>0,'Scope ray in an old1/200axis cap');outside.append(gap)
        for reflected in [False,True]:
            cols=[(-v[0],v[1],v[2]) if reflected else v for v in corners]
            weights=solve(cols,u)
            require(any(w<0 for w in weights) and any(w>0 for w in weights),'Scope ray inside an old projective triangle image')
            cone_records.append([k,reflected,[encode(x) for x in weights]]);audit.extend(weights)
        center=m.sharp.rotate(center);corners=[m.sharp.rotate(v) for v in corners]
    audit.extend(outside)
    return {'ray':[encode(x) for x in u],'old_projective_triangle_images_excluded':10,
            'old_axis_caps_excluded':5,'strict_new_cap_margin':encode(inside),
            'minimum_old_cap_exclusion_margin':encode(min(outside)),'old_triangle_cone_sha256':digest(cone_records)}
def cap_geometry(delta,audit):
    centers=[D]
    for k in range(4):centers.append(m.sharp.rotate(centers[-1]))
    require(len(set(centers))==5 and m.sharp.rotate(centers[-1])==D
            and all(dot(c,c)==N for c in centers),'Wrong actual body-axis orbit')
    margins=[2-2*absq(dot(a,b))/N-4*delta*delta for a,b in itertools.combinations(centers,2)]
    require(all(g>0 for g in margins) and 2>2*delta,'Directed closed caps overlap')
    audit.extend(margins)
    # A chord-radius delta unit-sphere cap has area pi*delta^2.
    return {'distinct_unoriented_axes':5,'distinct_directed_centers':10,
            'projective_axis_separation_checks':len(margins),
            'minimum_disjointness_margin':encode(min(margins)),
            'unit_sphere_area_divided_by_pi':str(10*F(1,40)**2),
            'fraction_of_unit_sphere_area':str(F(10,4)*F(1,40)**2),
            'spherical_cap_area_ratio_to_previous_1_200_caps':25}
def controls(data,probes,costs,points,gauges,nlo,nhi,constants,structure):
    bad=list(data['balanced_probe_triples']);bad[-1]=bad[0]
    tests=[lambda:balanced_point([0,0,1],probes,costs,[]),
           lambda:balanced_point([0,1,34],probes,costs,[]),
           lambda:balanced_point(data['balanced_probe_triples'][0],probes,costs,[],[Q(-1),Q(1),Q(1)]),
           lambda:balanced_point(data['balanced_probe_triples'][0],probes,costs,[],[Q(F(1,3))]*3),
           lambda:center_hull(bad,probes,[]),
           lambda:tangent_gauges(points,[Q(1),Q(1)],[]),
           lambda:receiving_cap(probes,Q(F(1,5)),nlo,nhi,[]),
           lambda:complete_phase(Q(F(1,4)),Q(F(1,40)),constants,structure,gauges,[]),
           lambda:z.cover_shape(structure[1][:-1]),
           lambda:m.old.root_check(Q(2),F(1),F(1),[])]
    for test in tests:
        try:test()
        except ValueError:pass
        else:raise ValueError('Malformed balanced/source/cap evidence accepted')
    return len(tests)
def check(data,self_test=False):
    source_pins=pins();audit=[]
    require(data['receiver_chord_radius']=='1/40' and data['normalized_center_ball_radius']=='1/7'
            and data['local_full_angle']=='23/100' and data['root_grid_denominator']==10**12,'Wrong fixed proof parameters')
    require(len(V)==55 and len(set(V))==55 and all(dot(v,v)==m.caps.R2 for v in V),'Wrong actual original vertex body')
    nlo,nhi=root(N,audit);_,rhi=root(m.caps.R2,audit);c0lo,c0hi=root(m.caps.B,audit)
    rholo,_=root(Q(233,-10)/596,audit)
    signed_contact_margin=Q(c0lo)-Q(rhi)/10
    require(signed_contact_margin>0,'Winning active-contact signs not fixed on source cap');audit.append(signed_contact_margin)
    probes=m.local.make_probes();costs,hull=center_hull(data['balanced_probe_triples'],probes,audit)
    delta=Q(F(data['receiver_chord_radius']));cap=receiving_cap(probes,delta,nlo,nhi,audit)
    normals=m.caps.reference_geometry(audit)[0]
    prior=json.loads((REPO/parent['source_directory']/'certificates.json').read_text())
    first,remote,points=z.structures(prior,normals,nlo,nhi,audit)
    gauges,directional=tangent_gauges(points,[decode(data['first_directional_gauge']),decode(data['late_directional_gauge'])],audit)
    signed,pc,ec,envelope_sha=z.signed_envelopes(normals,nlo,audit)
    width={i:max((signed[i,s] for s in [-1,1]),key=lambda rec:rec['kappa_upper']) for i in [11,12,13]}
    heights,oldwidth,pi,gap,pc0,ec0,sc0,se0=m.old.transport_data(normals,z.RANGE,nlo,audit)
    even=m.even_stress(normals,pi,m.G,audit)
    require(Q(c0lo)-Q(rhi)*delta>0,'No positive uniform receiving height')
    phase=complete_phase(Q(c0lo)-Q(rhi)*delta,delta,(width,pi,gap,rhi,c0hi,rholo,nlo),(first,remote),gauges,audit)
    localmargin=Q(F(1,7))-delta-Q(F(23,100))/2
    require(localmargin==Q(F(1,350)) and localmargin>0,'Explicit full-angle local margin fails');audit.append(localmargin)
    witness=scope_witness(delta,audit)
    geometry=cap_geometry(delta,audit)
    tests=controls(data,probes,costs,points,gauges,nlo,nhi,(width,pi,gap,rhi,c0hi,rholo,nlo),(first,remote)) if self_test else 0
    values=sorted(set(audit),key=lambda q:(q.a,q.b));m.local.independent_sign_audit(values)
    fixture_sha=hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'agent':'six-rupert-2','role':'researcher',
            'claim_status':'translated_normalized_torque_and_directional_source_coupling_entire_closed_J77_caps',
            'global_Rupert_resolved':False,'independent_review_asserted':False,'original_sources_rolls_translations_unrestricted':True,
            'scales_covered':'lambda>=1','closed_equality_forms':['Q=R^k','Q=M_n X R^k'],'closed_scale':1,'closed_translation':0,
            'directed_body_axis_cap_centers':10,'unoriented_cap_axes':5,'entire_closed_receiver_chord_radius':'1/40',
            'normalized_balanced_center_ball_radius':'1/7','explicit_local_full_angle':'23/100','local_normalized_torque_margin':encode(localmargin),
            'balanced_hull':hull,'directional_source':directional,'whole_cap':cap,'complete_full_source_phase':phase,
            'cap_geometry':geometry,'active_source_contact_sign_margin':encode(signed_contact_margin),
            'entire_previous_triangle_retained_separately':True,'entire_prior_analytic_criterion_dominance_asserted':False,
            'new_explicit_union_scope_witness':witness,'signed_receiving_original_pair_checks':pc,'signed_receiving_excess_checks':ec,
            'signed_receiving_envelope_sha256':envelope_sha,'retained_absolute_width_comparisons':pc0,
            'retained_absolute_width_excess_checks':ec0,'retained_even_single_support_comparisons':sc0,
            'retained_even_single_support_excess_checks':se0,'unique_even_minimum_comparisons':even,
            'pinned_dependency_files':len(source_pins),'full_parent_outputs_replayed':False,
            'new_sign_records':len(audit),'new_distinct_rational_sign_audits':len(values)+9,
            'malformed_controls_with_self_test':tests,'canonical_certificate_sha256':fixture_sha}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    data=json.loads((ROOT/'certificates.json').read_text())
    print(json.dumps(check(data,args.self_test),indent=2,sort_keys=True))
