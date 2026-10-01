#!/usr/bin/env python3
"""Exact finite hypotheses of WINNING_CAYLEY_PROOF.md, Python3.11+ stdlib.

Replays a fixed complete signed-axis cover for the fresh q21/50 triangle.
The continuous all-source phase and equality proof are written separately.
No adaptive search, floating point, solver or private input is required.
"""
import argparse,copy,hashlib,itertools,json
from fractions import Fraction as F
from math import comb,isqrt
from pathlib import Path

HERE=Path(__file__).resolve().parent

def demand(ok,message):
    if not ok:raise ValueError(message)

def validate_pins(rows):
    demand(len(rows)==50 and len({r['file'] for r in rows})==50,
           'all fifty distinct previously published mathematical inputs')
    for row in rows:
        name=row['file']
        demand(Path(name).name==name and name.endswith(('.py','.json')),'ordinary local mathematical input')
        raw=(HERE/name).read_bytes()
        demand(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],
               'published input mismatch: '+name)

INPUT_BYTES=(HERE/'winning_cayley_inputs.json').read_bytes()
INPUTS=json.loads(INPUT_BYTES)
validate_pins(INPUTS['files'])

from verify import PHI,QPhi as Q,ZERO,dot,vertices,symmetry_group
from cell_certificate import encode,geometry
from torque_certificate import cross,subtract
from adaptive_receiver_certificate import rational_strings,check_roll_branch
from expanded_global_slack_certificate import actual_supports
import axial_majorization_certificate as axial
import actual_torque_hull_certificate as hull
import balanced_receiver_certificate as balanced
import orthogonal_receiver_certificate as orthogonal
import winning_receiver_certificate as winning
import wider_winning_band_certificate as wider
import weighted_global_band_certificate as weighted

Q0=F(21,50);R=F(1,16);THETA=F(3,25);MAX_DEPTH=3

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def phase(q=Q0,radius=R):
    cL,cU=axial.exact_root('winning_height',Q(F(1,3)))
    rhoL,rhoU=axial.exact_root('winning_disk_radius',Q(F(8,3))+4*PHI)
    s=(cU-q)/rhoL
    demand(0<s<1,'positive honest winning tangent bound')
    zL,zU=axial.exact_root('winning_cosine_at_tangent_bound',Q(1-s*s))
    d=F(1001,1000)*s
    E=(F(13,15)*d+F(41,16)*d*d)/(1-d*d/4)
    X2=(2*d)**2+E*E;P=(1-d*d/4)**2*(1-E*E/4)
    gates=dict(
        height_above_remaining366_region_spectrum=Q(q*q)>Q(F(1,7)),
        receiving_height_below_winning_reference=cL>q,
        exact_body_radius_below9over2=7+8*PHI<Q(F(9,2)**2),
        sharp_disk_positive_original_bound=rhoL>0,
        honest_whole_region_chord_conversion=F(1001,1000)**2*(1+zL)>2,
        actual_both_normal_chords_in_conditional_C3_domain=0<d<F(1,10),
        whole_remote_roll_gate=E<F(77,1000),
        positive_principal_quaternion_branch=P>F(99,100)**2 and F(99,100)-d*d/4>0,
        composition_chord_domain=X2<F(1,9),
        inverse_sine_derivative_gate=F(101,100)**2*(1-X2/4)>1,
        full_original_spatial_angle_below_three25=F(101,100)**2*X2<THETA*THETA,
        full_angle_to_Cayley_radius=radius*(1-THETA*THETA/8)-THETA/2>0)
    demand(all(gates.values()),'unsupported all-source winning phase bounds')
    return dict(q=str(q),winning_tangent_norm_upper=str(s),honest_both_normal_chord_upper=str(d),
        balanced_C3_roll_chord_upper=str(E),composition_chord_squared_upper=str(X2),
        quaternion_cosine_product_squared_lower=str(P),full_principal_angle_upper=str(THETA),
        Cayley_radius_upper=str(radius),all12_exact_scalar_gates=gates,
        actual_source_winning_from_spectrum_and_axial_majorization=True,
        old_all_source_F_squared_above_beta_criterion_used=False,
        initial_full_original_rotation_small_angle_assumed=False),d

# Sparse exact polynomial arithmetic. Keys have either two or three variables.
def padd(a,b):
    c=dict(a)
    for k,v in b.items():
        c[k]=c.get(k,ZERO)+v
        if c[k]==ZERO:del c[k]
    return c

def pscale(a,v):return {k:v*t for k,t in a.items() if v*t!=ZERO}
def pmul(a,b):
    c={}
    for k,v in a.items():
        for l,w in b.items():
            m=tuple(x+y for x,y in zip(k,l));c[m]=c.get(m,ZERO)+v*w
    return {k:v for k,v in c.items() if v!=ZERO}
def psum(rows):
    c={}
    for row in rows:c=padd(c,row)
    return c
def pdot(a,b):return psum([pmul(x,y) for x,y in zip(a,b)])
def pcross(a,b):return [padd(pmul(a[(i+1)%3],b[(i+2)%3]),pscale(pmul(a[(i+2)%3],b[(i+1)%3]),-1)) for i in range(3)]
def const(q):return {(0,0,0):Q.coerce(q)} if Q.coerce(q)!=ZERO else {}
def pvec(v):return [const(q) for q in v]

def cayley_matrix():
    one=const(1)
    X=[{tuple(int(i==k) for i in range(3)):Q(1)} for k in range(3)]
    sq=pdot(X,X);den=padd(one,sq);minus=padd(one,pscale(sq,-1))
    skew=list(map(list,zip(*[pcross(X,pvec(tuple(Q(int(i==k)) for i in range(3)))) for k in range(3)])))
    N=[[psum([minus if i==j else {},pscale(pmul(X[i],X[j]),2),pscale(skew[i][j],2)]) for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            gram=psum([pmul(N[k][i],N[k][j]) for k in range(3)])
            demand(gram==(pmul(den,den) if i==j else {}),'proper Cayley orthogonality polynomial identity')
    demand(pdot(N[0],pcross(N[1],N[2]))==pmul(pmul(den,den),den),'proper Cayley determinant polynomial identity')
    return X,sq,den,N

def contact_geometry(V,U,probes):
    hull.validate_probes(probes)
    X,sq,den,N=cayley_matrix();contacts=[];identities=[]
    for j,(v,e) in enumerate(probes):
        plus=tuple(v[k]+e[k] for k in range(3));minus=subtract(v,e)
        demand(v in V and dot(e,e)==Q(4) and (plus in V or minus in V),'original endpoint/length-two oriented edge')
        rows=[]
        for u in U:
            mu=cross(e,u);h=dot(mu,v);T=cross(v,mu)
            demand(dot(mu,u)==ZERO and dot(mu,mu)>ZERO and h>ZERO,'strict original support offset and receiver orthogonality')
            demand(all(dot(mu,subtract(v,w))>=ZERO for w in V),'whole original receiving support at every raw corner')
            linear=pdot(pvec(T),X)
            second=padd(pmul(pdot(pvec(v),X),pdot(pvec(mu),X)),pscale(sq,-h))
            signed=padd(linear,second)
            difference=[padd(psum([pscale(N[i][k],v[k]) for k in range(3)]),pscale(den,-v[i])) for i in range(3)]
            demand(pdot(pvec(mu),difference)==pscale(signed,2),'original Cayley displacement polynomial identity')
            identities.append([[j],encode(u),encode(mu),h.encode(),encode(T)])
            rows.append((T,v,mu,h))
        contacts.append(rows)
    return contacts,dict(all10_original_endpoint_contacts=[dict(contact=j,original_vertex=encode(v),
        original_oriented_edge=encode(e),original_second_endpoint=encode(tuple(v[k]+e[k] for k in range(3))
            if tuple(v[k]+e[k] for k in range(3)) in V else subtract(v,e))) for j,(v,e) in enumerate(probes)],
        whole_original_receiver_corner_supports=1800,strict_offset_and_orthogonality_checks=30,
        Cayley_matrix_orthogonality_polynomial_identities=9,Cayley_determinant_polynomial_identities=1,
        original_contact_displacement_polynomial_identities=len(identities),
        original_corner_contact_record_sha256=digest(identities))

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
        demand(type(j) is int and j in range(10),'actual original contact index')
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

def witness(V,B):
    u=(ZERO,Q(F(171,500)),Q(1))
    demand(all(dot(v,u)*dot(v,B)>ZERO for v in V),'actual new receiver strict winning signs')
    f2=min(dot(v,u)**2/dot(u,u) for v in V)
    demand(Q(Q0*Q0)<=f2<axial.BETA-Q(F(1,100)),'new receiving height outside old global1over100 band')
    return dict(raw_original_receiver=encode(u),actual_minimum_original_squared_height=f2.encode(),
        all60_original_signs_and_heights_checked=True,new_winning_q21over50_band=True,
        below_old_GLOBAL_one100_height_cutoff=True,outside_every_old_geometric_union_claimed=False)

def reject(name,action,rejected):
    try:action()
    except (ValueError,AssertionError):rejected.append(name);return
    raise ValueError('malformed certificate accepted: '+name)

def controls(records,contacts,probes,U,V):
    rejected=[]
    def changed(action):
        rows=copy.deepcopy(records);action(rows);return rows
    reject('missing_published_input',lambda:validate_pins(INPUTS['files'][:-1]),rejected)
    reject('missing_closed_axis_face',lambda:validate_covers(records[:-1]),rejected)
    reject('duplicate_closed_axis_face',lambda:validate_covers(changed(lambda r:r.__setitem__(1,copy.deepcopy(r[0])))),rejected)
    reject('missing_signed_axis',lambda:validate_covers(changed(lambda r:r[0].__setitem__('sign',1))),rejected)
    reject('missing_closed_axis_leaf',lambda:validate_covers(changed(lambda r:r[0]['leaves'].pop())),rejected)
    reject('duplicate_axis_leaf',lambda:validate_covers(changed(lambda r:r[0]['leaves'].append(copy.deepcopy(r[0]['leaves'][0])))),rejected)
    reject('overlapping_ancestor_leaf',lambda:validate_covers(changed(lambda r:r[0]['leaves'].append(['',0,'1']))),rejected)
    reject('invalid_subdivision_digit',lambda:validate_covers(changed(lambda r:r[0]['leaves'][0].__setitem__(0,'4'))),rejected)
    reject('excess_fixed_cover_depth',lambda:validate_covers(changed(lambda r:r[0]['leaves'][0].__setitem__(0,'0000'))),rejected)
    reject('unknown_original_contact',lambda:validate_covers(changed(lambda r:r[0]['leaves'][0].__setitem__(1,10))),rejected)
    reject('false_axis_norm_lower',lambda:validate_covers(changed(lambda r:r[0]['leaves'][0].__setitem__(2,'2'))),rejected)
    reject('wrong_tensor_mixed_coefficient',lambda:bernstein_identities(F(1,2)),rejected)
    reject('missing_original_vertex',lambda:axial.validate_body(V-{min(V)}),rejected)
    v,e=probes[0];mu=cross(tuple(-x for x in e),U[0])
    reject('reversed_original_support',lambda:demand(dot(mu,v)>ZERO,'strict original support'),rejected)
    reject('nonstrict_linear_coefficient',lambda:coefficients((ZERO,ZERO,ZERO),(ZERO,)*6,box(''),F(1)),rejected)
    T,v,mu,h=contacts[0][0];w=(F(1,10),F(2,25),F(-1,20))
    signed=dot(w,v)*dot(w,mu)-h*dot(w,w)
    reject('discarded_signed_Cayley_quadratic',lambda:demand(signed==ZERO,'false discarded quadratic'),rejected)
    reject('unsafe_small_Cayley_radius',lambda:phase(radius=F(1,100)),rejected)
    reject('unsupported_lower_height_domain',lambda:phase(q=F(401,1000)),rejected)
    demand(len(rejected)==18,'all eighteen malformed controls rejected')
    return rejected

def check(self_test=False):
    axial.ROOT_RECORDS.clear();V=vertices();axial.validate_body(V)
    scalar,d=phase();roots=dict(axial.ROOT_RECORDS)
    win_geometry,B=axial.winning_geometry(V)
    G=symmetry_group(V,return_matrices=True)
    orbits=axial.orbit_certificate(V,B)
    chamber=wider.wider_chamber(G,d=d)
    U,cut=winning.cut_triangle(Q0)
    outer=weighted.fresh_winning_outer(U,H=F(13,200),L=F(27,25))
    adaptive=hull.fixture('adaptive_receiver_expected.json',hull.ADAPTIVE_SHA)
    probes,pool,facets=hull.selected_probes(adaptive)
    supports=actual_supports(probes,U)
    contacts,contact_data=contact_geometry(V,U,probes)
    moments=balanced.balanced_hypotheses()
    compact={k:v for k,v in moments.items() if k not in ('records','complete_polygon')}
    compact['complete_reference_polygon_support_checks']=moments['complete_polygon']['all_original_vertex_support_checks']
    compact=rational_strings(compact)
    parent=json.loads((HERE/'balanced_receiver_expected.json').read_text())
    demand(compact==parent['balanced_hypotheses'],'all native C3 moments/heights/gauges match the pinned interface')
    roll=check_roll_branch()
    demand(roll==parent['complete_concavity_roll_branch'],'whole roll-domain gate matches the pinned interface')
    composition=orthogonal.polynomial_identity()
    records=INPUTS['closed_axis_covers'];validate_covers(records)
    basis=bernstein_identities();faces=[replay(contacts,r) for r in records]
    demand([r['closed_leaves'] for r in faces]==[4,13,4,7,1,1] and sum(r['strict_positive_coefficients'] for r in faces)==1170,
        'fresh complete30leaf cover and all1170strict coefficients')
    equality=wider.body_halfturns(G,V)
    actual_witness=witness(V,B)
    rejected=controls(records,contacts,probes,U,V) if self_test else []
    return dict(agent='six-rupert-3',role='researcher',
        proof_status='complete_written_unformalized_author_checked_winning_receiver_rigidity',
        independently_reviewed=False,global_RID_status='OPEN',global_receiving_squared_height_gap='1/100 unchanged',
        stronger_GLOBAL_gap_proved=False,
        branch='all original source orientations into any winning strict signed-region receiver f(n)>=21/50',
        closed_containment_classification='lambda=1,t=0,Q in G union J_n G; J_n=2nn^t-I',
        exact_disjoint_LEFT_coset_orientation_count=120,receiving_cutoff_boundary_included=True,
        all50_published_mathematical_inputs_unchanged=True,input_manifest_sha256=hashlib.sha256(INPUT_BYTES).hexdigest(),
        fresh_all_source_phase=scalar,all_three_positive_outward_root_enclosures=roots,
        fresh_winning_tangent_geometry_sha256=digest(win_geometry),directed_actual_proper_gauge_checks=orbits,
        fresh_proper_chamber=chamber,fresh_original_q21over50_cut_triangle=rational_strings(cut),
        fresh_whole_triangle_outer_bounds=outer,all1800_original_support_comparisons=supports,
        fresh_original_Cayley_contacts=contact_data,native24_C3_moment_gauge_triples=compact,
        native_complete_concavity_roll_gate=roll,native_orthogonal_composition_polynomial=composition,
        six_tensor_Bernstein_power_basis_polynomial_identities=basis,all_six_closed_axis_faces=faces,
        complete_closed_axis_leaves=30,selected_strict_positive_exact_coefficients=1170,
        fixed_complete_cover_sha256=digest(records),all15_original_body_halfturn_axis_facts=equality,
        actual_new_receiving_height_band_witness=actual_witness,malformed_controls_rejected=rejected,
        inherited436_region_spectrum_reenumerated=False,inherited_axial_majorization_branch_rerun=False,
        old_unsigned_torque_half_ball_remainder_at_new_angle=str(F(1,2)-F(9,2)*F(27,25)*THETA),
        zero_Cayley_vector_treated_as_identity_equality=True,continuous_proof='WINNING_CAYLEY_PROOF.md')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true');parser.add_argument('--emit',action='store_true')
    args=parser.parse_args();result=check(args.self_test)
    raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
    if args.emit:print(raw.decode(),end='')
    else:
        demand(args.self_test,'published replay includes all malformed controls')
        demand(raw==(HERE/'winning_cayley_expected.json').read_bytes(),'every expected mathematical certificate byte matches')
        print(json.dumps(dict(status='verified_every_expected_byte',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
            closed_axis_leaves=30,strict_coefficients=1170,original_supports=1800,native_C3_triples=24,
            scalar_gates=12,malformed_controls_rejected=18,global_RID='OPEN',global_receiving_gap='1/100 unchanged'),sort_keys=True))

if __name__=='__main__':main()
