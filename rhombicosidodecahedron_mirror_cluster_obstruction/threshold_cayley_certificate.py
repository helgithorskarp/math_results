#!/usr/bin/env python3
"""Exact finite hypotheses of THRESHOLD_CAYLEY_PROOF.md, Python3.11+ stdlib.

Complete original candidate-pool injections and fixed signed-axis covers.
No floating point, solver, adaptive public search or private input is used.
The universal geometric bridges are proved in the companion written proof.
"""
import argparse,copy,hashlib,itertools,json
from fractions import Fraction as F
from math import comb,isqrt
from pathlib import Path

HERE=Path(__file__).resolve().parent

def demand(ok,message):
    if not ok:raise ValueError(message)

def validate_pins(rows):
    demand(len(rows)==53 and len({r['file'] for r in rows})==53,
        'all53 distinct previously published mathematical inputs')
    for row in rows:
        name=row['file']
        demand(Path(name).name==name and name.endswith(('.py','.json')),
            'ordinary local mathematical input')
        raw=(HERE/name).read_bytes()
        demand(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],
            'published input mismatch: '+name)

INPUT_BYTES=(HERE/'threshold_cayley_inputs.json').read_bytes()
INPUTS=json.loads(INPUT_BYTES)
validate_pins(INPUTS['files'])

from verify import PHI,QPhi as Q,ZERO,act,dot,vertices,symmetry_group
from cell_certificate import encode,decode
from torque_certificate import cross,subtract
from linear_roll_certificate import project
from threshold_receiver_certificate import REFS,I,active_balance,exact_rotations,validate_proper
from contact_collar_certificate import LOW,complete_contacts
from winning_cayley_certificate import cayley_matrix,pdot,pvec,padd,pmul,pscale,psum
import axial_majorization_certificate as axial
import coupled_nonwinning_certificate as coupled
import weighted_global_band_certificate as weighted

Q0=F(21,50);R=F(1,25);MAX_DEPTH=3

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def phase(q=Q0,radius=R):
    inherited=axial.scalar_certificate(q=q)
    cap=F(inherited['threshold_normal_chord_bound'])
    cU=F(axial.ROOT_RECORDS['threshold_height']['upper'])
    eta=cU*cap+F(9,4)*cap*cap
    height2=axial.BETA+Q(9*eta)
    hL,hU=axial.exact_root('radial_candidate_height',height2)
    theta=F(101,100)*F(19,5)*cap
    lx,lt=(49+45*PHI)/29,(135+195*PHI)/29
    gates=dict(
        original_candidate_distance_below_three8=axial.BETA-Q(q*q)+Q(9*eta)<Q(F(3,8)**2),
        eight_actual_source_candidates_distinct=F(3,2)-2*eta>F(3,4),
        proper_circle_matching_arcs_disjoint=F(4,5)<F(3,2),
        six_forbidden_shift_length_gaps_exceed_two_matching_errors=5>F(4,5),
        weighted_full_chord_coefficient_below19over5=Q(F(19,5)**2)*(axial.BETA+lx)>4*lt,
        conditional_full_chord_below_one10=F(19,5)*cap<F(1,10),
        inverse_sine_derivative_below101over100=F(101,100)**2*(1-F(1,400))>1,
        conditional_principal_full_angle_below_two25=theta<F(2,25),
        conditional_full_angle_to_Cayley_one25=radius*(1-theta*theta/8)-theta/2>0,
        rational_GLOBAL_gap_one31_is_strictly_weaker=axial.BETA-Q(F(1,31))>Q(q*q),
        source_and_receiver_root_radius_bound=7+8*PHI<Q(F(9,2)**2))
    demand(all(gates.values()),'unsupported enlarged threshold phase gates')
    return dict(q=str(q),threshold_coercivity_scalar_interface=inherited,
        both_threshold_normal_chord_upper=str(cap),circle_original_transport_upper=str(eta),
        actual_radial_candidate_squared_height_upper=height2.encode(),
        actual_radial_candidate_height_upper=str(hU),actual_candidate_distance_upper='3/8',
        full_weighted_chord_upper=str(F(19,5)*cap),full_principal_angle_upper=str(theta),
        conditional_Cayley_radius_upper=str(radius),all11_fresh_scalar_gates=gates),cap,eta,hU

def neg(p):return tuple(-q for q in p)

def canonical(p):
    first=next(q for q in p if q!=ZERO)
    return p if first>ZERO else neg(p)

def pool_filter(j,m,V,circle,originals,cap,eta,heightU,pool_override=None,patterns_override=None):
    eligible=sorted(v for v in V if dot(v,m)**2/dot(m,m)<=Q((heightU+F(9,2)*cap)**2))
    demand(set(originals)<=set(eligible),'all original circle candidates retained')
    if pool_override is not None:eligible=pool_override
    pool=sorted({project(v,m) for v in eligible})
    demand(len(pool)==len(eligible) and all(neg(p) in pool for p in pool),
        'distinct complete antipodal eligible original projections')
    reps=sorted({canonical(p) for p in circle})
    dest=sorted({canonical(p) for p in pool})
    demand(len(reps)==4 and len(circle)==8 and len(dest)*2==len(pool),
        'four source pairs and complete destination antipodal axes')
    max2=max(dot(v,m)**2/dot(m,m) for v in eligible)
    hL,hU=axial.exact_root('eligible_pool_height'+str(j),max2)
    receive_eta=hU*cap+F(9,4)*cap*cap
    flat=F(3,8)+eta+receive_eta
    demand(flat<F(2,5),'flat error uses actual maximum eligible NONCIRCLE height')
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

def original_contacts(V,U,probes):
    demand(len(probes)==len(set(probes))==16,'complete16 original threshold contacts')
    X,sq,den,N=cayley_matrix();contacts=[];identities=[];support_checks=0
    for j,(v,e) in enumerate(probes):
        plus=tuple(v[k]+e[k] for k in range(3));minus=subtract(v,e)
        demand(v in V and dot(e,e)==Q(4) and (plus in V or minus in V),
            'original endpoint and length-two edge')
        rows=[]
        for u in U:
            mu=cross(e,u);h=dot(mu,v);T=cross(v,mu)
            demand(dot(mu,u)==ZERO and dot(mu,mu)>ZERO and h>ZERO,'positive original support')
            for other in V:
                demand(dot(mu,subtract(v,other))>=ZERO,'every original vertex on whole receiver outer-box support')
                support_checks+=1
            linear=pdot(pvec(T),X)
            second=padd(pmul(pdot(pvec(v),X),pdot(pvec(mu),X)),pscale(sq,-h))
            signed=padd(linear,second)
            difference=[padd(psum([pscale(N[i][k],v[k]) for k in range(3)]),pscale(den,-v[i])) for i in range(3)]
            demand(pdot(pvec(mu),difference)==pscale(signed,2),'exact original signed Cayley displacement identity')
            identities.append([j,encode(u),encode(mu),h.encode(),encode(T)]);rows.append((T,v,mu,h))
        contacts.append(rows)
    return contacts,dict(original16_contact_edges=[dict(original_vertex=encode(v),original_edge=encode(e)) for v,e in probes],
        whole_original_receiver_corner_supports=support_checks,original_displacement_polynomial_identities=len(identities),
        Cayley_matrix_Gram_polynomial_identities=9,Cayley_determinant_polynomial_identities=1,
        original_corner_contact_record_sha256=digest(identities))

def case_geometry(j,V,cap,eta,heightU):
    m=(LOW,REFS[1])[j]
    circle,ordered,originals,H=coupled.circle_geometry(m,V)
    pool=pool_filter(j,m,V,ordered,originals,cap,eta,heightU)
    moment,M,weights=weighted.moment_certificate(m,V)
    moment_audit=weighted.moment_trace_audit(m,M)
    contact,probes,T,_=complete_contacts(m,V,I)
    z=1-cap*cap/2;a=F(17,16)*cap/z;b=cap/z
    demand(z>0 and dot(m,m)<Q(F(17,16)**2),'raw normalization bound for whole actual cap')
    tangent=(ZERO,-m[2],m[1]);xaxis=(Q(1),ZERO,ZERO)
    U=[tuple(m[k]+sx*a*xaxis[k]+sy*b*tangent[k] for k in range(3))
        for sx,sy in ((-1,-1),(-1,1),(1,-1),(1,1))]
    contacts,contact_record=original_contacts(V,U,probes)
    record=dict(case=j,raw_reference=encode(m),native_complete_original_circle_geometry=circle,
        native_complete_candidate_pool=pool,weighted_original_moment=moment,exact_full_angle_moment_audit=moment_audit,
        original_reference_contacts=contact,complete_closed_receiving_cap_raw_outer_box=[encode(u) for u in U],
        raw_box_alpha_and_beta_bounds=[str(a),str(b)],outer_box_z_positive_lower=str(z),
        exact_whole_box_original_contacts=contact_record)
    # The full16 reference rows are regenerated; the compact fixture pins their hash.
    record['original_reference_contacts']={k:v for k,v in contact.items() if k!='actual_contact_records'}
    record['original_reference_contacts']['all16_preimage_records_sha256']=digest(contact['actual_contact_records'])
    return record,dict(m=m,ordered=ordered,originals=originals,probes=probes,U=U,contacts=contacts,M=M,weights=weights)

def proper_alignments(V,G,saved):
    axes={'body_projective_orbits':[dict(representative_balance=active_balance(n,V)) for n in REFS]}
    Dcross,C,rotation_record=exact_rotations(G,axes);records=[]
    for si,ti in itertools.product(range(2),repeat=2):
        D=I if si==ti else Dcross;validate_proper(D)
        source,receiver=saved[si],saved[ti]
        transported=act(D,source['m']);ratio=dot(transported,receiver['m'])/dot(receiver['m'],receiver['m'])
        demand(ratio>ZERO and transported==tuple(ratio*q for q in receiver['m']),
            'positive DIRECTED proper reference-normal alignment')
        demand({act(D,v) for v in source['originals']}==set(receiver['originals']),
            'all8 actual source originals map exactly to receiving circle originals')
        contact,probes,T,_=complete_contacts(receiver['m'],V,D)
        demand(probes==receiver['probes'],'all16 selected contacts have actual ORIGINAL source preimages')
        demand((D in G)==(si==ti),'cross-class alignment must not be treated as a body symmetry')
        records.append(dict(source_class=si,receiving_class=ti,proper_alignment_matrix=[encode(row) for row in D],
            positive_raw_normal_proportionality=ratio.encode(),original_shared_vertices=contact['original_shared_vertices'],
            original_circle_preimages=8,original_local_contact_preimages=16,
            full16_original_source_contact_record_sha256=digest(contact['actual_contact_records']),
            source_class_to_receiver_directed_plane_orientation='proper',proper_alignment_is_body_symmetry=si==ti,
            relative_zero_rotation_has_an_original_touching_contact=True))
    return dict(actual_nonbody_cross_alignment=rotation_record,all4_ordered_original_proper_pairings=records)

def face_coeff(row,axis,sign):
    T,v,mu,h=row;a,b=[k for k in range(3) if k!=axis]
    return (sign*T[axis],T[a],T[b]),(v[axis]*mu[axis]-h,
        sign*(v[axis]*mu[a]+v[a]*mu[axis]),sign*(v[axis]*mu[b]+v[b]*mu[axis]),
        v[a]*mu[a]-h,v[a]*mu[b]+v[b]*mu[a],v[b]*mu[b]-h)

def box(path):
    x=y=F(-1);dx=dy=F(2)
    for digit in path:
        demand(digit in '0123','dyadic square digit')
        j=int(digit);dx/=2;dy/=2
        if j in (1,3):x+=dx
        if j in (2,3):y+=dy
    return x,y,dx,dy

def norm_lower(bounds):
    x,y,dx,dy=bounds
    def least(a,b):return min(a*a,b*b) if a*b>0 else F(0)
    n2=1+least(x,x+dx)+least(y,y+dy);grid=10**6
    ell=F(isqrt(n2.numerator*grid*grid//n2.denominator),grid)
    demand(ell>=1 and ell*ell<=n2 and (ell+F(1,grid))**2>n2,'positive outward cube-face norm enclosure')
    return ell

def transformed(L,B,bounds):
    x,y,dx,dy=bounds;l0,lx,ly=L;b0,bx,by,bxx,bxy,byy=B
    return (l0+lx*x+ly*y,lx*dx,ly*dy),(b0+bx*x+by*y+bxx*x*x+bxy*x*y+byy*y*y,
        dx*(bx+2*bxx*x+bxy*y),dy*(by+bxy*x+2*byy*y),bxx*dx*dx,bxy*dx*dy,byy*dy*dy)

def coefficients(L,B,bounds,ell):
    A,C=transformed(L,B,bounds)
    first=[A[0]+i*A[1]+j*A[2] for i in (0,1) for j in (0,1)]
    P=tuple(ell*(A[k] if k<3 else ZERO)+R*C[k] for k in range(6))
    bern=[P[0]+F(i,2)*P[1]+F(j,2)*P[2]+(P[3] if i==2 else ZERO)
        +F(i*j,4)*P[4]+(P[5] if j==2 else ZERO) for i in range(3) for j in range(3)]
    demand(all(c>ZERO for c in first),'strict positive complete affine corner coefficients')
    demand(all(c>ZERO for c in bern),'strict positive complete tensor Bernstein coefficients')
    return first,bern

def validate_cover(record):
    demand(set(record)=={'axis','sign','leaves'},'exact closed cube-face record schema')
    demand(type(record['axis']) is int and record['axis'] in range(3) and record['sign'] in (-1,1),'cube face axis/sign')
    leaves=record['leaves'];demand(leaves,'nonempty complete face cover')
    for row in leaves:
        demand(isinstance(row,list) and len(row)==3,'fixed leaf schema')
        path,j,ell=row
        demand(isinstance(path,str) and len(path)<=MAX_DEPTH and set(path)<=set('0123'),'bounded dyadic path')
        demand(type(j) is int and j in range(16),'actual original threshold contact index')
        demand(F(ell)==norm_lower(box(path)),'saved positive outward norm lower bound')
    paths=[row[0] for row in leaves];wanted=set(paths)
    demand(len(wanted)==len(paths),'distinct fixed leaves')
    seen=[];nodes=0
    def visit(path):
        nonlocal nodes
        nodes+=1
        if path in wanted:seen.append(path);return
        demand(len(path)<MAX_DEPTH and any(p.startswith(path) for p in wanted),'no uncovered dyadic square')
        for k in range(4):visit(path+str(k))
    visit('')
    demand(set(seen)==wanted and sum((F(1,4)**len(p) for p in paths),F(0))==1,
        'all four children, prefix-free whole closed square')
    return nodes

def validate_covers(records):
    demand(len(records)==6 and [(r['axis'],r['sign']) for r in records]==
        list(itertools.product(range(3),(-1,1))),'all six distinct closed signed cube faces')
    return [validate_cover(r) for r in records]

def bernstein_identities(mixed=F(1,4)):
    one={(0,0):Q(1)};sx={(1,0):Q(1)};sy={(0,1):Q(1)}
    def power(p,n):
        out=one
        for _ in range(n):out=pmul(out,p)
        return out
    def basis(p):return [pscale(pmul(power(p,i),power(padd(one,pscale(p,-1)),2-i)),comb(2,i)) for i in range(3)]
    bx,by=basis(sx),basis(sy)
    exponents=[(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)]
    for k,exponent in enumerate(exponents):
        P=[Q(int(k==j)) for j in range(6)];rebuilt={}
        for i in range(3):
            for j in range(3):
                c=P[0]+F(i,2)*P[1]+F(j,2)*P[2]+(P[3] if i==2 else ZERO)+mixed*i*j*P[4]+(P[5] if j==2 else ZERO)
                rebuilt=padd(rebuilt,pscale(pmul(bx[i],by[j]),c))
        demand(rebuilt=={exponent:Q(1)},'complete power-to-tensor-Bernstein polynomial identity')
    return len(exponents)

def direct_audits(row,axis,sign,L,B,bounds,ell,first,bern):
    T,v,mu,h=row;A,C=transformed(L,B,bounds);x0,y0,dx,dy=bounds
    a,b=[k for k in range(3) if k!=axis]
    for s,t in ((F(0),F(0)),(F(1),F(1)),(F(1,3),F(2,5))):
        x=x0+dx*s;y=y0+dy*t;z=[F(0)]*3;z[axis]=F(sign);z[a]=x;z[b]=y
        actualL=dot(T,z);actualB=dot(v,z)*dot(mu,z)-h*dot(z,z)
        demand(A[0]+A[1]*s+A[2]*t==actualL,'direct affine original-vector audit')
        demand(C[0]+C[1]*s+C[2]*t+C[3]*s*s+C[4]*s*t+C[5]*t*t==actualB,'direct signed quadratic vector audit')
        bs=[F(comb(2,i))*s**i*(1-s)**(2-i) for i in range(3)]
        bt=[F(comb(2,j))*t**j*(1-t)**(2-j) for j in range(3)]
        demand(sum((bern[3*i+j]*bs[i]*bt[j] for i in range(3) for j in range(3)),ZERO)==ell*actualL+R*actualB,
            'direct transformed Bernstein audit')
    return 9

def replay(contacts,record):
    nodes=validate_cover(record);axis,sign=record['axis'],record['sign']
    data=[[face_coeff(row,axis,sign) for row in rows] for rows in contacts]
    values=[];audits=0
    for path,j,saved_ell in record['leaves']:
        bounds=box(path);ell=norm_lower(bounds);demand(F(saved_ell)==ell,'outward norm replay')
        for row,(L,B) in zip(contacts[j],data[j]):
            first,bern=coefficients(L,B,bounds,ell)
            values.append([c.encode() for c in first+bern])
            audits+=direct_audits(row,axis,sign,L,B,bounds,ell,first,bern)
    return dict(axis=axis,sign=sign,complete_quadtree_nodes=nodes,closed_leaves=len(record['leaves']),
        max_depth=max(len(row[0]) for row in record['leaves']),strict_positive_coefficients=13*len(values),
        full_exact_selected_coefficient_sha256=digest(values),direct_vector_and_Bernstein_audits=audits)


def validate_all_cases(records):
    demand(len(records)==2 and [r['case'] for r in records]==[0,1],'both distinct threshold proper receiver classes')
    for r in records:
        demand(set(r)=={'case','closed_axis_faces'},'exact threshold case-cover schema')
        validate_covers(r['closed_axis_faces'])

def new_threshold_witness(V,m):
    u=(Q(F(1,100)),m[1],m[2]);f2=min(dot(v,u)**2/dot(u,u) for v in V)
    demand(all(dot(v,u)*dot(v,m)>ZERO for v in V),'actual new strict threshold-region signs')
    demand(Q(Q0*Q0)<=f2<axial.BETA-Q(F(1,100)),
        'actual threshold receiver between newq band and oldGLOBAL1over100 band')
    return dict(raw_original_receiver=encode(u),actual_minimum_original_squared_height=f2.encode(),
        all60_original_signs_and_heights_checked=True,new_threshold_height_band=True,
        below_old_GLOBAL_one100_height_cutoff=True,outside_every_old_geometric_union_claimed=False)

def reject(name,action,rejected):
    try:action()
    except (ValueError,AssertionError):rejected.append(name);return
    raise ValueError('malformed certificate accepted: '+name)

def controls(records,saved,V,cap,eta,heightU):
    rejected=[]
    def mutated(action):
        copy_rows=copy.deepcopy(records);action(copy_rows);return copy_rows
    reject('missing_published_input',lambda:validate_pins(INPUTS['files'][:-1]),rejected)
    reject('missing_threshold_class',lambda:validate_all_cases(records[:-1]),rejected)
    reject('duplicate_threshold_class',lambda:validate_all_cases([records[0],records[0]]),rejected)
    reject('missing_signed_axis_face',lambda:validate_covers(records[0]['closed_axis_faces'][:-1]),rejected)
    reject('duplicate_signed_axis_face',lambda:validate_all_cases(mutated(lambda r:r[0]['closed_axis_faces'].__setitem__(1,copy.deepcopy(r[0]['closed_axis_faces'][0])))),rejected)
    reject('missing_closed_axis_leaf',lambda:validate_all_cases(mutated(lambda r:r[0]['closed_axis_faces'][0]['leaves'].pop())),rejected)
    reject('duplicate_axis_leaf',lambda:validate_all_cases(mutated(lambda r:r[0]['closed_axis_faces'][0]['leaves'].append(copy.deepcopy(r[0]['closed_axis_faces'][0]['leaves'][0])))),rejected)
    reject('overlapping_axis_ancestor',lambda:validate_all_cases(mutated(lambda r:r[0]['closed_axis_faces'][0]['leaves'].append(['',0,'1']))),rejected)
    reject('invalid_axis_digit',lambda:validate_all_cases(mutated(lambda r:r[0]['closed_axis_faces'][0]['leaves'][0].__setitem__(0,'4'))),rejected)
    reject('unsupported_cover_depth',lambda:validate_all_cases(mutated(lambda r:r[0]['closed_axis_faces'][0]['leaves'][0].__setitem__(0,'0000'))),rejected)
    reject('unknown_original_contact',lambda:validate_all_cases(mutated(lambda r:r[0]['closed_axis_faces'][0]['leaves'][0].__setitem__(1,16))),rejected)
    reject('false_positive_axis_norm_lower',lambda:validate_all_cases(mutated(lambda r:r[0]['closed_axis_faces'][0]['leaves'][0].__setitem__(2,'2'))),rejected)
    reject('wrong_tensor_mixed_coefficient',lambda:bernstein_identities(F(1,2)),rejected)
    reject('missing_original_body_vertex',lambda:axial.validate_body(V-{min(V)}),rejected)
    row=saved[1];pool=[v for v in sorted(V) if dot(v,row['m'])**2/dot(row['m'],row['m'])<=Q((heightU+F(9,2)*cap)**2)]
    reject('missing_eligible_antipode',lambda:pool_filter(1,row['m'],V,row['ordered'],row['originals'],cap,eta,heightU,pool_override=pool[:-1]),rejected)
    reject('incomplete_signed_candidate_assignments',lambda:pool_filter(1,row['m'],V,row['ordered'],row['originals'],cap,eta,heightU,patterns_override=list(itertools.product((-1,1),repeat=4))[:-1]),rejected)
    reject('zero_weight_original_moment',lambda:weighted.moment_certificate(row['m'],V,supplied_weights=[ZERO]*4),rejected)
    v,e=saved[0]['probes'][0];mu=cross(tuple(-x for x in e),saved[0]['U'][0])
    reject('reversed_original_support',lambda:demand(dot(mu,v)>ZERO,'positive original support'),rejected)
    reject('nonstrict_Cayley_affine_coefficients',lambda:coefficients((ZERO,ZERO,ZERO),(ZERO,)*6,box(''),F(1)),rejected)
    T,v,mu,h=saved[0]['contacts'][0][0];w=(F(1,10),F(2,25),F(-1,20))
    reject('discarded_signed_Cayley_quadratic',lambda:demand(dot(w,v)*dot(w,mu)-h*dot(w,w)==ZERO,'false discarded quadratic'),rejected)
    reject('unsafe_angle_to_Cayley_radius',lambda:phase(radius=F(1,100)),rejected)
    reject('unsupported_lower_height',lambda:phase(q=F(1,3)),rejected)
    demand(len(rejected)==22,'all22 malformed controls rejected')
    return rejected

def check(self_test=False):
    axial.ROOT_RECORDS.clear();V=vertices();axial.validate_body(V)
    scalar,cap,eta,heightU=phase();scalar_roots=dict(axial.ROOT_RECORDS)
    G=symmetry_group(V,return_matrices=True);cases=[];saved=[]
    for j in range(2):
        record,data=case_geometry(j,V,cap,eta,heightU);cases.append(record);saved.append(data)
    alignments=proper_alignments(V,G,saved)
    records=INPUTS['both_threshold_closed_axis_covers'];validate_all_cases(records)
    basis=bernstein_identities();total_leaves=total_coefficients=0
    for j,(record,data) in enumerate(zip(cases,saved)):
        faces=[replay(data['contacts'],r) for r in records[j]['closed_axis_faces']]
        counts=[r['closed_leaves'] for r in faces]
        demand(counts==([4,4,16,16,1,1] if j==0 else [16,16,4,4,13,13]),'fresh complete threshold face-leaf counts')
        record['all_six_closed_axis_faces']=faces
        total_leaves+=sum(counts);total_coefficients+=sum(r['strict_positive_coefficients'] for r in faces)
    demand(total_leaves==108 and total_coefficients==5616,'complete108leaf/5616strict coefficient obstruction')
    witness=new_threshold_witness(V,saved[0]['m'])
    all_roots_hash=digest(axial.ROOT_RECORDS);all_roots_count=len(axial.ROOT_RECORDS)
    rejected=controls(records,saved,V,cap,eta,heightU) if self_test else []
    return dict(agent='six-rupert-3',role='researcher',
        proof_status='complete_written_unformalized_author_checked_GLOBAL_necessary_receiving_gap',
        independently_reviewed=False,global_RID_status='OPEN',GLOBAL_strict_passage_receiving_height_upper='21/50',
        GLOBAL_strict_passage_receiving_squared_height_upper='441/2500',
        exact_GLOBAL_squared_height_gap=(axial.BETA-Q(Q0*Q0)).encode(),
        rational_GLOBAL_squared_height_gap='1/31',prior_GLOBAL_gap='1/100',
        branch='both threshold sources into both threshold receivers atf>=21/50; all4 ordered proper pairings',
        threshold_closed_containment_coset_classification_claimed=False,receiving_cutoff_boundary_included=True,
        initial_small_angle_assumed=False,source_matched_original_premise_proved_by_written_pool_bridge=True,
        all53_published_mathematical_inputs_unchanged=True,input_manifest_sha256=hashlib.sha256(INPUT_BYTES).hexdigest(),
        fresh_all_source_threshold_phase=scalar,scalar_positive_outward_root_enclosures=scalar_roots,
        both_fresh_original_threshold_cases=cases,all_original_proper_class_alignments=alignments,
        six_tensor_Bernstein_power_basis_polynomial_identities=basis,complete_closed_axis_leaves=total_leaves,
        selected_strict_positive_exact_coefficients=total_coefficients,whole_original_receiving_corner_supports=7680,
        complete_signed_antipodal_pool_assignments=sum(c['native_complete_candidate_pool']['signed_injective_antipodal_assignments'] for c in cases),
        original_contact_displacement_polynomial_identities=128,
        positive_outward_roots_regenerated=all_roots_count,complete_outward_root_record_sha256=all_roots_hash,
        fixed_complete_cover_sha256=digest(records),new_actual_threshold_height_band_witness=witness,
        malformed_controls_rejected=rejected,zero_relative_Cayley_motion_excludes_STRICT_passage_by_original_contact=True,
        inherited436_region_spectrum_reenumerated=False,inherited_winning_q21over50_classifier_rerun=False,
        inherited_winning_to_threshold_full_roll_branch_rerun=False,
        continuous_proof='THRESHOLD_CAYLEY_PROOF.md')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true');parser.add_argument('--emit',action='store_true')
    args=parser.parse_args();result=check(args.self_test)
    raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
    if args.emit:print(raw.decode(),end='')
    else:
        demand(args.self_test,'published replay includes all malformed controls')
        demand(raw==(HERE/'threshold_cayley_expected.json').read_bytes(),'every expected mathematical certificate byte matches')
        print(json.dumps(dict(status='verified_every_expected_byte',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
            closed_axis_leaves=108,strict_coefficients=5616,original_supports=7680,complete_pool_assignments=6144,
            proper_class_pairings=4,malformed_controls_rejected=22,global_RID='OPEN',GLOBAL_gap='1/31',
            stronger_exact_receiving_height='21/50'),sort_keys=True))

if __name__=='__main__':main()
