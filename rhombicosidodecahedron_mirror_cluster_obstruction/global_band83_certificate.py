#!/usr/bin/env python3
"""Exact finite hypotheses of GLOBAL_BAND_83_PROOF.md, Python3.11+ stdlib.

Fresh same-class phases, complete original candidate pools, and three fixed
signed-axis covers at q=83/200.  The continuous geometric bridges and the
inherited two mixed branches are identified in the companion written proof.
No adaptive public search, floating point, solver, or private input is used.
"""
import argparse, copy, hashlib, itertools, json
from fractions import Fraction as F
from math import comb, isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent

def demand(ok, message):
    if not ok:
        raise ValueError(message)

def validate_pins(rows):
    demand(len(rows) == 59 and len({r['file'] for r in rows}) == 59,
        'all59 distinct previously published mathematical inputs')
    for row in rows:
        demand(set(row) == {'file', 'bytes', 'sha256'}, 'exact input-pin schema')
        name = row['file']
        demand(Path(name).name == name and name.endswith(('.py', '.json')),
            'ordinary local mathematical input')
        raw = (HERE / name).read_bytes()
        demand(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
            'published input mismatch: ' + name)

INPUT_BYTES = (HERE / 'global_band83_inputs.json').read_bytes()
INPUTS = json.loads(INPUT_BYTES)
validate_pins(INPUTS['files'])

from verify import PHI, QPhi as Q, ZERO, act, dot, vertices, symmetry_group
from cell_certificate import encode
from torque_certificate import cross, subtract
from linear_roll_certificate import project
from contact_collar_certificate import LOW, complete_contacts
from threshold_receiver_certificate import REFS, I
from adaptive_receiver_certificate import rational_strings, check_roll_branch
from expanded_global_slack_certificate import actual_supports
from winning_cayley_certificate import padd, pmul, pscale
import axial_majorization_certificate as axial
import actual_torque_hull_certificate as hull
import balanced_receiver_certificate as balanced
import orthogonal_receiver_certificate as orthogonal
import winning_receiver_certificate as winning
import wider_winning_band_certificate as wider
import weighted_global_band_certificate as weighted
import coupled_nonwinning_certificate as coupled
import winning_cayley_certificate as wc
import threshold_cayley_certificate as tc

Q0 = F(83, 200)
WIN_THETA, WIN_RADIUS, WIN_DEPTH = F(1, 8), F(1, 15), 3
THRESHOLD_THETA, THRESHOLD_RADIUS, THRESHOLD_DEPTH = F(9, 100), F(1, 22), 4
CANDIDATE, MATCH_MAX = F(2, 5), F(9, 20)

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def winning_phase(q=Q0, radius=WIN_RADIUS):
    cL, cU = axial.exact_root('winning83_height', Q(F(1, 3)))
    rhoL, rhoU = axial.exact_root('winning83_disk', Q(F(8, 3)) + 4*PHI)
    s = (cU-q)/rhoL
    demand(0 < s < 1, 'positive fresh winning tangent bound')
    zL, zU = axial.exact_root('winning83_cosine', Q(1-s*s))
    d = F(1001, 1000)*s
    E = (F(13, 15)*d + F(41, 16)*d*d)/(1-d*d/4)
    X2, P = (2*d)**2+E*E, (1-d*d/4)**2*(1-E*E/4)
    gates = dict(
        complete_region_spectrum_above_remaining366=Q(q*q) > Q(F(1, 7)),
        reference_height_and_disk_positive=cL > q and rhoL > 0,
        original_body_radius=7+8*PHI < Q(F(9, 2)**2),
        actual_normal_chord_conversion=F(1001, 1000)**2*(1+zL) > 2,
        both_normal_chords_in_conditional_C3_domain=0 < d < F(1, 10),
        complete_C3_remote_roll_gate=E < F(77, 1000),
        principal_quaternion_branch=P > F(99, 100)**2 and F(99, 100)-d*d/4 > 0,
        composition_chord_domain=X2 < F(1, 9),
        whole_inverse_sine_derivative=F(101, 100)**2*(1-X2/4) > 1,
        full_actual_spatial_angle=F(101, 100)**2*X2 < WIN_THETA**2,
        full_angle_to_fresh_Cayley_radius=radius*(1-WIN_THETA**2/8)-WIN_THETA/2 > 0,
        rational_GLOBAL_one28_is_weaker=axial.BETA-Q(F(1, 28)) > Q(q*q))
    demand(all(gates.values()), 'unsupported fresh winning83 phase')
    return dict(q=str(q), both_original_normal_chords_upper=str(d),
        original_C3_roll_chord_upper=str(E), full_composition_chord_squared_upper=str(X2),
        quaternion_cosine_product_squared_lower=str(P), full_spatial_angle_upper=str(WIN_THETA),
        actual_Cayley_radius_upper=str(radius), all12_fresh_exact_scalar_gates=gates,
        source_winning_derived_using_committed_mixed8270=True,
        old_four_height_majorization_or_all_source_height_above_beta_used=False), d

def threshold_phase(q=Q0, radius=THRESHOLD_RADIUS):
    cL, cU = axial.exact_root('threshold83_height', axial.BETA)
    rhoL, rhoU = axial.exact_root('threshold83_disk', (39+37*PHI)/29)
    s = (cU-q)/rhoL
    demand(0 < s < 1, 'positive fresh threshold tangent bound')
    zL, zU = axial.exact_root('threshold83_cosine', Q(1-s*s))
    d = F(1001, 1000)*s
    eta = cU*d+F(9, 4)*d*d
    height2 = axial.BETA+Q(9*eta)
    hL, hU = axial.exact_root('threshold83_actual_candidate_height', height2)
    lx, lt = (49+45*PHI)/29, (135+195*PHI)/29
    chord, full = F(19, 5)*d, F(101, 100)*F(19, 5)*d
    gates = dict(
        actual_regional_chord_conversion=F(1001, 1000)**2*(1+zL) > 2,
        both_normal_spectra_above_other366=Q(q*q) > Q(F(1, 7)),
        fresh_original_candidate_distance=axial.BETA-Q(q*q)+Q(9*eta) < Q(CANDIDATE**2),
        all_actual_original_candidates_distinct=F(3, 2)-2*eta > 2*CANDIDATE,
        proper_circle_arcs_disjoint=2*MATCH_MAX < F(3, 2),
        complete_six_other_shift_gaps=5 > 2*MATCH_MAX,
        full_weighted_original_chord_coefficient=Q(F(19, 5)**2)*(axial.BETA+lx) > 4*lt,
        full_actual_spatial_chord_small=chord < F(1, 10),
        whole_inverse_sine_derivative=F(101, 100)**2*(1-F(1, 400)) > 1,
        full_actual_spatial_angle=full < THRESHOLD_THETA,
        full_angle_to_fresh_Cayley_radius=radius*(1-THRESHOLD_THETA**2/8)-THRESHOLD_THETA/2 > 0,
        rational_GLOBAL_one28_is_weaker=axial.BETA-Q(F(1, 28)) > Q(q*q))
    demand(all(gates.values()), 'unsupported fresh threshold83 phase')
    return dict(q=str(q), both_original_normal_chords_upper=str(d),
        original_source_circle_transport_upper=str(eta), actual_original_candidate_distance_upper=str(CANDIDATE),
        actual_radial_candidate_squared_height_upper=height2.encode(), actual_candidate_height_upper=str(hU),
        full_weighted_chord_upper=str(chord), full_spatial_angle_upper=str(full),
        chosen_full_angle_upper=str(THRESHOLD_THETA), actual_Cayley_radius_upper=str(radius),
        all12_fresh_exact_scalar_gates=gates,
        original_candidate_matching_and_positive_moment_premise_proved_in_written_bridge=True,
        old_four_height_majorization_interface_used=False), d, eta, hU

# Fresh pool constants and explicit radius/depth arguments; no old globals are changed.

def neg(p):return tuple(-q for q in p)

def canonical(p):
    first=next(q for q in p if q!=ZERO)
    return p if first>ZERO else neg(p)

def pool_filter(j,m,V,circle,originals,cap,eta,heightU,pool_override=None,patterns_override=None,eligible_height_squared_override=None):
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
    if eligible_height_squared_override is not None:
        demand(eligible_height_squared_override>=max2,'actual complete eligible maximum height cannot be understated')
        max2=eligible_height_squared_override
    hL,hU=axial.exact_root('eligible_pool_height'+str(j),max2)
    receive_eta=hU*cap+F(9,4)*cap*cap
    flat=CANDIDATE+eta+receive_eta
    demand(flat<MATCH_MAX,'flat error uses actual maximum eligible NONCIRCLE height')
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

def coefficients(L,B,bounds,ell,radius):
    A,C=transformed(L,B,bounds)
    first=[A[0]+i*A[1]+j*A[2] for i in (0,1) for j in (0,1)]
    P=tuple(ell*(A[k] if k<3 else ZERO)+radius*C[k] for k in range(6))
    bern=[P[0]+F(i,2)*P[1]+F(j,2)*P[2]+(P[3] if i==2 else ZERO)
        +F(i*j,4)*P[4]+(P[5] if j==2 else ZERO) for i in range(3) for j in range(3)]
    demand(all(c>ZERO for c in first),'strict positive complete affine corner coefficients')
    demand(all(c>ZERO for c in bern),'strict positive complete tensor Bernstein coefficients')
    return first,bern

def validate_cover(record,contact_count,max_depth):
    demand(set(record)=={'axis','sign','leaves'},'exact closed cube-face record schema')
    demand(type(record['axis']) is int and record['axis'] in range(3) and type(record['sign']) is int and record['sign'] in (-1,1),'cube face axis/sign')
    leaves=record['leaves'];demand(leaves,'nonempty complete face cover')
    for row in leaves:
        demand(isinstance(row,list) and len(row)==3,'fixed leaf schema')
        path,j,ell=row
        demand(isinstance(path,str) and len(path)<=max_depth and set(path)<=set('0123'),'bounded dyadic path')
        demand(type(j) is int and j in range(contact_count),'actual original threshold contact index')
        demand(F(ell)==norm_lower(box(path)),'saved positive outward norm lower bound')
    paths=[row[0] for row in leaves];wanted=set(paths)
    demand(len(wanted)==len(paths),'distinct fixed leaves')
    seen=[];nodes=0
    def visit(path):
        nonlocal nodes
        nodes+=1
        if path in wanted:seen.append(path);return
        demand(len(path)<max_depth and any(p.startswith(path) for p in wanted),'no uncovered dyadic square')
        for k in range(4):visit(path+str(k))
    visit('')
    demand(set(seen)==wanted and sum((F(1,4)**len(p) for p in paths),F(0))==1,
        'all four children, prefix-free whole closed square')
    return nodes

def validate_covers(records,contact_count,max_depth):
    demand(len(records)==6 and [(r['axis'],r['sign']) for r in records]==
        list(itertools.product(range(3),(-1,1))),'all six distinct closed signed cube faces')
    return [validate_cover(r,contact_count,max_depth) for r in records]

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

def direct_audits(row,axis,sign,L,B,bounds,ell,first,bern,radius):
    T,v,mu,h=row;A,C=transformed(L,B,bounds);x0,y0,dx,dy=bounds
    a,b=[k for k in range(3) if k!=axis]
    for s,t in ((F(0),F(0)),(F(1),F(1)),(F(1,3),F(2,5))):
        x=x0+dx*s;y=y0+dy*t;z=[F(0)]*3;z[axis]=F(sign);z[a]=x;z[b]=y
        actualL=dot(T,z);actualB=dot(v,z)*dot(mu,z)-h*dot(z,z)
        demand(A[0]+A[1]*s+A[2]*t==actualL,'direct affine original-vector audit')
        demand(C[0]+C[1]*s+C[2]*t+C[3]*s*s+C[4]*s*t+C[5]*t*t==actualB,'direct signed quadratic vector audit')
        bs=[F(comb(2,i))*s**i*(1-s)**(2-i) for i in range(3)]
        bt=[F(comb(2,j))*t**j*(1-t)**(2-j) for j in range(3)]
        demand(sum((bern[3*i+j]*bs[i]*bt[j] for i in range(3) for j in range(3)),ZERO)==ell*actualL+radius*actualB,
            'direct transformed Bernstein audit')
    return 9

def replay(contacts,record,radius,max_depth):
    nodes=validate_cover(record,len(contacts),max_depth);axis,sign=record['axis'],record['sign']
    data=[[face_coeff(row,axis,sign) for row in rows] for rows in contacts]
    values=[];audits=0
    for path,j,saved_ell in record['leaves']:
        bounds=box(path);ell=norm_lower(bounds);demand(F(saved_ell)==ell,'outward norm replay')
        for row,(L,B) in zip(contacts[j],data[j]):
            first,bern=coefficients(L,B,bounds,ell,radius)
            values.append([c.encode() for c in first+bern])
            audits+=direct_audits(row,axis,sign,L,B,bounds,ell,first,bern,radius)
    return dict(axis=axis,sign=sign,complete_quadtree_nodes=nodes,closed_leaves=len(record['leaves']),
        max_depth=max(len(row[0]) for row in record['leaves']),strict_positive_coefficients=13*len(values),
        full_exact_selected_coefficient_sha256=digest(values),direct_vector_and_Bernstein_audits=audits)

def threshold_case(j, V, cap, eta, heightU):
    m = (LOW, REFS[1])[j]
    circle, ordered, originals, full_hull = coupled.circle_geometry(m, V)
    pool = pool_filter(j, m, V, ordered, originals, cap, eta, heightU)
    moment, M, weights = weighted.moment_certificate(m, V)
    audit = weighted.moment_trace_audit(m, M)
    contact, probes, T, unused = complete_contacts(m, V, I)
    z = 1-cap*cap/2
    alpha, gamma = F(17, 16)*cap/z, cap/z
    demand(z > 0 and dot(m, m) < Q(F(17, 16)**2), 'raw whole-cap rectangle normalization')
    tangent, xaxis = (ZERO, -m[2], m[1]), (Q(1), ZERO, ZERO)
    U = [tuple(m[k]+sx*alpha*xaxis[k]+sy*gamma*tangent[k] for k in range(3))
        for sx, sy in ((-1, -1), (-1, 1), (1, -1), (1, 1))]
    contacts, contact_record = tc.original_contacts(V, U, probes)
    record = dict(case=j, raw_reference=encode(m), complete_original_circle_geometry_sha256=digest(circle),
        original_circle_counts=dict(original_projections=circle['full_original_projections'],
            full_receiving_hull_corners=circle['full_receiving_hull_corners'], original_circle_preimages=8,
            noncircle_original_heights=52, complete_reference_circle_pairs=28),
        original_circle_order=[encode(v) for v in originals],
        minimum_original_circle_pair_squared_distance=circle['minimum_reference_circle_pair_squared_distance'],
        all_six_other_cyclic_shift_obstructions=circle['complete_six_cyclic_shift_obstructions'],
        native_complete_candidate_pool=pool, original_weighted_moment=moment, full_moment_trace_audit=audit,
        complete_reference_contact_sha256=digest(contact), original_receiver_corner_contacts=contact_record,
        whole_cap_raw_four_corner_box=[encode(u) for u in U], raw_box_alpha_gamma=[str(alpha), str(gamma)],
        positive_whole_cap_chart_denominator_lower=str(z))
    return record, dict(m=m, ordered=ordered, originals=originals, probes=probes, U=U,
        contacts=contacts, M=M, weights=weights)

def winning_case(V, G, d):
    geo, B = axial.winning_geometry(V)
    orbits = axial.orbit_certificate(V, B)
    chamber = wider.wider_chamber(G, d=d)
    U, cut = winning.cut_triangle(Q0)
    outer = weighted.fresh_winning_outer(U, H=F(33, 500), L=F(27, 25))
    adaptive = hull.fixture('adaptive_receiver_expected.json', hull.ADAPTIVE_SHA)
    probes, pool, facets = hull.selected_probes(adaptive)
    supports = actual_supports(probes, U)
    contacts, contact_record = wc.contact_geometry(V, U, probes)
    moments = balanced.balanced_hypotheses()
    compact = {k:v for k,v in moments.items() if k not in ('records', 'complete_polygon')}
    compact['complete_reference_polygon_support_checks'] = moments['complete_polygon']['all_original_vertex_support_checks']
    compact = rational_strings(compact)
    parent = json.loads((HERE / 'balanced_receiver_expected.json').read_text())
    demand(compact == parent['balanced_hypotheses'], 'every native C3 original moment/gauge/height interface entry')
    roll = check_roll_branch()
    demand(roll == parent['complete_concavity_roll_branch'], 'entire native conditional concavity roll branch')
    composition = orthogonal.polynomial_identity()
    equality = wider.body_halfturns(G, V)
    record = dict(raw_reference=encode(B), fresh_original_tangent_geometry_sha256=digest(geo),
        directed_original_proper_gauge_checks=orbits, whole_band_original_proper_chamber=chamber,
        fresh_whole_band_cut_triangle=rational_strings(cut), fresh_whole_triangle_outer_bounds=outer,
        all1800_original_support_comparisons=supports, original_Cayley_contacts=contact_record,
        native24_C3_moment_gauge_triples=compact, native_complete_concavity_roll_gate=roll,
        native_perpendicular_axis_composition_polynomial=composition,
        all15_original_body_halfturn_axis_facts_sha256=digest(equality),
        every_body_halfturn_has_original_zero_height=True, exact_disjoint_LEFT_coset_count=120)
    return record, dict(m=B, U=U, probes=probes, contacts=contacts)

def enlargement_witnesses(V, saved):
    rays = [(Q(F(1, 25)), 2-PHI, Q(1)), (Q(F(3, 200)), LOW[1], LOW[2])]
    refs = [saved[0]['m'], saved[1]['m']]
    records = []
    for label, u, m in zip(('winning', 'threshold_low'), rays, refs):
        demand(all(dot(v, u)*dot(v, m) > ZERO for v in V), 'all60 strict original region signs of new height witness')
        f2 = min(dot(v, u)**2/dot(u, u) for v in V)
        demand(Q(Q0*Q0) <= f2 < Q(F(21, 50)**2), 'actual new receiving height between83over200 and21over50')
        records.append(dict(class_label=label, original_raw_receiver=encode(u), actual_minimum_squared_original_height=f2.encode(),
            all60_original_signs_and_heights_checked=True, below_old_GLOBAL21over50_cutoff=True,
            outside_all_previous_geometric_exclusion_unions_claimed=False))
    return records

def reject(name, action, rejected):
    try:
        action()
    except (ValueError, AssertionError):
        rejected.append(name)
        return
    raise ValueError('malformed evidence accepted: ' + name)

def validate_threshold_cases(records):
    demand(len(records) == 2 and [r['case'] for r in records] == [0, 1], 'both distinct ordered threshold receiver classes')
    for record in records:
        demand(set(record) == {'case', 'closed_axis_faces'}, 'exact threshold-cover case schema')
        validate_covers(record['closed_axis_faces'], 16, THRESHOLD_DEPTH)

def controls(wcovers, tcovers, saved, V, cap, eta, heightU):
    rejected = []
    def mutate(records, action):
        rows = copy.deepcopy(records)
        action(rows)
        return rows
    reject('missing_published_input', lambda:validate_pins(INPUTS['files'][:-1]), rejected)
    reject('duplicate_published_input', lambda:validate_pins(INPUTS['files'][:-1]+INPUTS['files'][:1]), rejected)
    for label, cover, count, depth in (('winning', wcovers, 10, WIN_DEPTH),
            ('threshold', tcovers[0]['closed_axis_faces'], 16, THRESHOLD_DEPTH)):
        validate = lambda rows:validate_covers(rows, count, depth)
        reject(label+'_missing_signed_face', lambda:validate(cover[:-1]), rejected)
        reject(label+'_duplicate_signed_face', lambda:validate(mutate(cover, lambda r:r.__setitem__(1, copy.deepcopy(r[0])))), rejected)
        reject(label+'_missing_closed_leaf', lambda:validate(mutate(cover, lambda r:r[0]['leaves'].pop())), rejected)
        reject(label+'_duplicate_closed_leaf', lambda:validate(mutate(cover, lambda r:r[0]['leaves'].append(copy.deepcopy(r[0]['leaves'][0])))), rejected)
        reject(label+'_overlapping_ancestor', lambda:validate(mutate(cover, lambda r:r[0]['leaves'].append(['', 0, '1']))), rejected)
        reject(label+'_invalid_dyadic_digit', lambda:validate(mutate(cover, lambda r:r[0]['leaves'][0].__setitem__(0, '4'))), rejected)
        reject(label+'_unsupported_depth', lambda:validate(mutate(cover, lambda r:r[0]['leaves'][0].__setitem__(0, '0'*(depth+1)))), rejected)
        reject(label+'_unknown_original_contact', lambda:validate(mutate(cover, lambda r:r[0]['leaves'][0].__setitem__(1, count))), rejected)
        reject(label+'_false_axis_norm_lower', lambda:validate(mutate(cover, lambda r:r[0]['leaves'][0].__setitem__(2, '2'))), rejected)
    reject('missing_threshold_class', lambda:validate_threshold_cases(tcovers[:-1]), rejected)
    reject('duplicate_threshold_class', lambda:validate_threshold_cases([tcovers[0], tcovers[0]]), rejected)
    reject('wrong_tensor_mixed_coefficient', lambda:bernstein_identities(F(1, 2)), rejected)
    reject('missing_original_body_vertex', lambda:axial.validate_body(V-{min(V)}), rejected)
    high = saved[2]
    eligible = [v for v in sorted(V) if dot(v, high['m'])**2/dot(high['m'], high['m']) <= Q((heightU+F(9, 2)*cap)**2)]
    reject('missing_eligible_original_antipode', lambda:pool_filter(1, high['m'], V, high['ordered'], high['originals'], cap, eta, heightU,
        pool_override=eligible[:-1]), rejected)
    reject('incomplete_signed_candidate_assignments', lambda:pool_filter(1, high['m'], V, high['ordered'], high['originals'], cap, eta, heightU,
        patterns_override=list(itertools.product((-1, 1), repeat=4))[:-1]), rejected)
    reject('circle_height_substituted_for_non_circle_maximum', lambda:pool_filter(1, high['m'], V, high['ordered'], high['originals'], cap, eta, heightU,
        eligible_height_squared_override=axial.BETA), rejected)
    reject('zero_weight_original_moment', lambda:weighted.moment_certificate(high['m'], V, supplied_weights=[ZERO]*4), rejected)
    v, e = saved[1]['probes'][0]
    mu = cross(tuple(-x for x in e), saved[1]['U'][0])
    reject('reversed_original_support', lambda:demand(dot(mu, v) > ZERO, 'positive original support'), rejected)
    reject('nonstrict_Cayley_affine_coefficients', lambda:coefficients((ZERO, ZERO, ZERO), (ZERO,)*6, box(''), F(1), WIN_RADIUS), rejected)
    T, v, mu, h = saved[1]['contacts'][0][0]
    w = (F(1, 10), F(2, 25), F(-1, 20))
    reject('discarded_signed_Cayley_quadratic', lambda:demand(dot(w, v)*dot(w, mu)-h*dot(w, w) == ZERO, 'false discarded quadratic'), rejected)
    reject('old_winning_raw_drift_reused', lambda:weighted.fresh_winning_outer(saved[0]['U'], H=F(13, 200), L=F(27, 25)), rejected)
    reject('unsafe_winning_Cayley_radius', lambda:winning_phase(radius=F(1, 100)), rejected)
    reject('unsafe_threshold_Cayley_radius', lambda:threshold_phase(radius=F(1, 100)), rejected)
    reject('unsupported_winning_lower_height', lambda:winning_phase(q=F(1, 3)), rejected)
    reject('unsupported_threshold_lower_height', lambda:threshold_phase(q=F(1, 3)), rejected)
    demand(len(rejected) == 36, 'all36 malformed-evidence controls reject')
    return rejected

def check():
    demand(INPUTS['q'] == str(Q0), 'exact fixed new receiving cutoff')
    axial.ROOT_RECORDS.clear()
    V = vertices()
    axial.validate_body(V)
    win_phase, dw = winning_phase()
    t_phase, dt, eta, heightU = threshold_phase()
    scalar_roots = dict(axial.ROOT_RECORDS)
    G = symmetry_group(V, return_matrices=True)
    wrecord, wdata = winning_case(V, G, dw)
    records, saved = [], [wdata]
    for j in range(2):
        record, data = threshold_case(j, V, dt, eta, heightU)
        records.append(record)
        saved.append(data)
    alignments = tc.proper_alignments(V, G, saved[1:])
    wcovers, tcovers = INPUTS['winning_closed_axis_covers'], INPUTS['both_threshold_closed_axis_covers']
    validate_covers(wcovers, 10, WIN_DEPTH)
    validate_threshold_cases(tcovers)
    basis = bernstein_identities()
    wfaces = [replay(wdata['contacts'], row, WIN_RADIUS, WIN_DEPTH) for row in wcovers]
    demand([r['closed_leaves'] for r in wfaces] == [4, 13, 4, 7, 1, 1], 'fresh fixed winning83 face counts')
    wrecord['all_six_complete_closed_axis_faces'] = wfaces
    for j, record in enumerate(records):
        faces = [replay(saved[j+1]['contacts'], row, THRESHOLD_RADIUS, THRESHOLD_DEPTH) for row in tcovers[j]['closed_axis_faces']]
        demand([r['closed_leaves'] for r in faces] == ([16, 4, 28, 28, 1, 1] if j == 0 else [22, 16, 4, 4, 22, 22]),
            'fresh fixed threshold83 face counts')
        record['all_six_complete_closed_axis_faces'] = faces
    all_faces = wfaces+[face for record in records for face in record['all_six_complete_closed_axis_faces']]
    leaves = sum(r['closed_leaves'] for r in all_faces)
    coefficients_count = sum(r['strict_positive_coefficients'] for r in all_faces)
    demand(leaves == 198 and coefficients_count == 9906, 'complete fresh198leaf/9906strict-coefficient certificate')
    witnesses = enlargement_witnesses(V, saved)
    root_hash, root_count = digest(axial.ROOT_RECORDS), len(axial.ROOT_RECORDS)
    rejected = controls(wcovers, tcovers, saved, V, dt, eta, heightU)
    return dict(agent='six-rupert-3', role='researcher',
        proof_status='complete_written_unformalized_author_checked_GLOBAL_necessary_receiving_gap',
        independently_reviewed=False, historical_priority_asserted=False, global_RID_status='OPEN',
        GLOBAL_strict_passage_receiving_height_upper=str(Q0), GLOBAL_squared_height_upper=str(Q0*Q0),
        exact_GLOBAL_squared_height_gap=(axial.BETA-Q(Q0*Q0)).encode(), rational_GLOBAL_squared_height_gap='1/28',
        prior_GLOBAL_receiving_height='21/50', prior_GLOBAL_squared_height_gap='1/31',
        exact_GLOBAL_strict_projected_diameter_squared_lower=(4*(7+8*PHI-Q(Q0*Q0))).encode(),
        all_original_source_rotations_translations_scales_and_cutoff_boundary_included=True,
        initial_small_spatial_angle_or_roll_assumed=False,
        fresh_winning_closed_classification='lambda=1,t=0,Q in G union J_n G;120proper LEFTcoset motions',
        threshold_closed_containment_coset_classification_claimed=False,
        all59_published_mathematical_inputs_unchanged=True, input_manifest_sha256=hashlib.sha256(INPUT_BYTES).hexdigest(),
        fresh_winning_same_class_phase=win_phase, fresh_threshold_all4_same_class_phase=t_phase,
        scalar_positive_outward_root_records=scalar_roots, all_outward_roots_regenerated=root_count,
        entire_outward_root_record_sha256=root_hash, winning_original_case=wrecord, both_threshold_original_cases=records,
        all_four_actual_original_proper_threshold_alignments=alignments,
        six_power_to_tensor_Bernstein_polynomial_identities=basis, complete_closed_axis_leaves=leaves,
        strict_positive_exact_coefficients=coefficients_count,
        all_original_receiving_corner_supports=9480, all_original_contact_displacement_polynomial_identities=158,
        all_complete_signed_antipodal_candidate_assignments=6144,
        native_original_weighted_moment_trace_audits=96,
        direct_vector_and_Bernstein_audits=sum(r['direct_vector_and_Bernstein_audits'] for r in all_faces),
        fixed_complete_cover_sha256=digest([wcovers, tcovers]), actual_new_receiving_height_band_witnesses=witnesses,
        malformed_evidence_controls_rejected=rejected, inherited436_region_spectrum_reenumerated=False,
        inherited_mixed8270_and8138_branches_rerun=False,
        old_same_class_guards_or_globals_widened=False,
        continuous_proof='GLOBAL_BAND_83_PROOF.md')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    result = check()
    raw = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode()
    if args.emit:
        print(raw.decode(), end='')
    else:
        demand(raw == (HERE / 'global_band83_expected.json').read_bytes(), 'every expected mathematical certificate byte matches')
        print(json.dumps(dict(status='verified_every_expected_byte', bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
            closed_axis_leaves=198, strict_coefficients=9906, original_supports=9480,
            original_displacement_identities=158, complete_pool_assignments=6144,
            proper_threshold_class_pairings=4, malformed_controls_rejected=36,
            GLOBAL_receiving_height=str(Q0), GLOBAL_squared_height_gap='1/28', global_RID='OPEN'), sort_keys=True))

if __name__ == '__main__':
    main()
