#!/usr/bin/env python3
"""Exact finite hypotheses of GAMMA_BRANCH_PROOF.md, Python3.11+ stdlib.

Complete CLOSED roll covers certify Gamma7/100 at both threshold references.
All original support envelopes are checked at the actual q83/200 chords.
Only the winning-source/threshold-receiver branch is excluded here.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def demand(ok, message):
    if not ok:
        raise ValueError(message)


def validate_pin_rows(rows):
    demand(len(rows) == 47 and len({r['file'] for r in rows}) == 47,
           'complete distinct47published mathematical inputs')
    for row in rows:
        name = row['file']
        demand(Path(name).name == name and name.endswith(('.py', '.json')),
               'ordinary same-directory mathematical input')
        raw = (HERE/name).read_bytes()
        demand(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
               'published mathematical input mismatch: '+name)


INPUT_BYTES = (HERE/'gamma_branch_inputs.json').read_bytes()
INPUTS = json.loads(INPUT_BYTES)
validate_pin_rows(INPUTS['files'])
INPUT_SHA = hashlib.sha256(INPUT_BYTES).hexdigest()

from verify import PHI, QPhi, ZERO, dot, vertices
from cell_certificate import encode, geometry
from torque_certificate import cross, subtract
from linear_roll_certificate import exact_hull, project
from threshold_receiver_certificate import REFS, facet_coefficients, hull_data, source_coordinates
from contact_collar_certificate import LOW
import axial_majorization_certificate as axial
import coupled_nonwinning_certificate as coupled
import weighted_global_band_certificate as weighted

Q, GAMMA, HEIGHT = F(83, 200), F(7, 100), F(13, 10)


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def scalars(q=Q, gamma=GAMMA):
    demand(F(2,5)<q<F(9,20) and gamma>0, 'positive supported scalar domain')
    cL, cU = axial.exact_root('threshold_height',axial.BETA)
    c0L, c0U = axial.exact_root('winning_height',QPhi(F(1,3)))
    rtL, rtU = axial.exact_root('threshold_disk_radius',(39+37*PHI)/29)
    rwL, rwU = axial.exact_root('winning_disk_radius',QPhi(F(8,3))+4*PHI)
    sT, sW = (cU-q)/rtL, (c0U-q)/rwL
    demand(0<sT<1 and 0<sW<1, 'positive small whole-region tangent bounds')
    zTL, zTU = axial.exact_root('threshold_cosine_at_tangent_bound',QPhi(1-sT*sT))
    zWL, zWU = axial.exact_root('winning_cosine_at_tangent_bound',QPhi(1-sW*sW))
    aT, aW = F(1001,1000)*sT, F(1001,1000)*sW
    etaW, etaT = c0U*aW+F(9,4)*aW*aW, HEIGHT*aT+F(9,4)*aT*aT
    gap = gamma-etaW-etaT
    gates = dict(
        whole_region_height_squared_above_other_spectrum=QPhi(q*q)>QPhi(F(1,7)),
        threshold_reference_height_exceeds_q=cL>q,
        winning_reference_height_exceeds_q=c0L>q,
        exact_original_body_radius_below9over2=7+8*PHI<QPhi(F(9,2)**2),
        threshold_whole_region_chord_conversion=F(1001,1000)**2*(1+zTL)>2,
        winning_whole_region_chord_conversion=F(1001,1000)**2*(1+zWL)>2,
        threshold_chord_below23over1000=aT<F(23,1000),
        winning_chord_below54over1000=aW<F(54,1000),
        explicit_branch_one28_band_above_q_squared=axial.BETA-QPhi(F(1,28))>QPhi(q*q),
        actual_transported_support_gap_exceeds_one600=gap>F(1,600),
    )
    demand(all(gates.values()),'unsupported whole-region Gamma branch scalar gates')
    return dict(q=str(q),gamma=str(gamma),receiving_height_intercept=str(HEIGHT),
                all10_scalar_gates=gates,threshold_tangent_norm_bound=str(sT),
                winning_tangent_norm_bound=str(sW),threshold_normal_chord_bound=str(aT),
                winning_normal_chord_bound=str(aW),original_winning_corner_transport_bound=str(etaW),
                whole_original_receiving_support_transport_bound=str(etaT),
                exact_positive_transported_support_gap=str(gap),certified_gap_lower='1/600',
                old25epsilonover27_denominator_premise_used=False,
                initial_full_spatial_rotation_small_angle_assumed=False)


def source_geometry(V, selected=None):
    axial.validate_body(V)
    B = geometry()[0][0][1]
    N = dot(B,B)
    H = exact_hull({project(v,B) for v in V},B)
    demand(len(H)==12 and len(set(H))==12 and
           all(dot(p,p)==7+8*PHI-QPhi(F(1,3)) for p in H),
           'complete actual threefold source dodecagon')
    preimages=[]
    for p in H:
        actual=[v for v in V if project(v,B)==p]
        demand(len(actual)==1 and 3*dot(actual[0],B)**2==N,
               'unique ORIGINAL winning corner and height squared one third')
        preimages.append(actual[0])
    if selected is not None:
        demand(selected==preimages,'all twelve original source corner preimages')
    normals=[cross(subtract(q,p),B) for p,q in zip(H,H[1:]+H[:1])]
    comparisons=[]
    for j,(p,m) in enumerate(zip(H,normals)):
        demand(dot(m,m)>ZERO and dot(m,p)>ZERO,'positive actual source hull facet')
        for i,v in enumerate(sorted(V)):
            gap=dot(m,subtract(p,v))
            demand(gap>=ZERO,'all ORIGINAL source points satisfy the complete hull')
            comparisons.append([j,i,gap.encode()])
    demand(len(comparisons)==720,'all twelve source facets times sixty originals')
    return dict(raw_reference=encode(B),all12_original_corner_preimages=[encode(v) for v in preimages],
                complete12_corner_hull=[encode(p) for p in H],
                all720_original_hull_supports_checked=True,
                full_original_hull_support_record_sha256=digest(comparisons),
                all12_original_corner_absolute_height_squared=['1/3','0']),B,H,preimages


def coefficient_digest(coefficients):
    return digest([[[str(x.lo),str(x.hi)] for x in row] for row in coefficients])


def rejection(name, action, rows):
    try:
        action()
    except (ValueError,AssertionError):
        rows.append(name)
        return
    raise ValueError('malformed control unexpectedly accepted: '+name)


def check(self_test=False):
    axial.ROOT_RECORDS.clear()
    V=vertices()
    axial.validate_body(V)
    scalar=scalars()
    roots=dict(axial.ROOT_RECORDS)
    win_geometry,B=axial.winning_geometry(V)
    threshold_geometry=[axial.threshold_geometry(n,V) for n in REFS]
    orbits=axial.orbit_certificate(V,B)
    source,B,H0,preimages=source_geometry(V)
    coords=source_coordinates(H0,B)
    cases=[]
    saved=[]
    for j,n in enumerate((LOW,REFS[1])):
        S,H,normals,_,_,_=hull_data(n,V)
        demand(len(S)==60 and len(H)==len(normals)==16,'complete original receiving polygon')
        # Complete search only supplies witnesses. Every selected leaf, all
        # three exact coefficients, and both children at every split replay.
        cover,coefficients=coupled.whole_winning_cover(H,n,coords,gamma=GAMMA)
        envelope=weighted.receiving_envelope(n,V,H,normals,
                  cap=F(scalar['threshold_normal_chord_bound']),height_bound=HEIGHT)
        demand(envelope['whole_original_receiving_support_error_upper']==
               scalar['whole_original_receiving_support_transport_bound'],
               'enlarged-domain receiving envelope uses the actual scalar chord')
        cases.append(dict(case=j,raw_receiving_reference=encode(n),full_closed_roll_cover=cover,
                          all192_actual_facet_original_corner_coefficient_interval_sha256=
                              coefficient_digest(coefficients),
                          all960_enlarged_original_support_envelopes=envelope))
        saved.append((n,H,normals,coefficients,cover))
    demand(sum(c['full_closed_roll_cover']['whole_closed_leaves'] for c in cases)==84,
           'complete deterministic fresh84leaf Gamma7over100 cover')
    rejected=[]
    if self_test:
        n,H,normals,coeff,cover=saved[0]
        leaves=cover['all_compact_closed_leaf_witnesses']
        bad_index=[list(x) for x in leaves];bad_index[0][2]=192
        rejection('missing_published_input_pin',lambda:validate_pin_rows(INPUTS['files'][:-1]),rejected)
        rejection('missing_original_vertex',lambda:axial.validate_body(V-{min(V)}),rejected)
        rejection('missing_original_source_corner',lambda:source_geometry(V,preimages[:-1]),rejected)
        rejection('missing_whole_receiving_facet',lambda:weighted.receiving_envelope(n,V,H[:-1],normals[:-1]),rejected)
        rejection('missing_closed_circle_quarter',lambda:coupled.validate_closed_tree([x for x in leaves if x[0]!=3]),rejected)
        rejection('missing_closed_roll_leaf',lambda:coupled.validate_closed_tree(leaves[:-1]),rejected)
        rejection('duplicate_closed_roll_leaf',lambda:coupled.validate_closed_tree(leaves+[leaves[0]]),rejected)
        rejection('invalid_original_roll_witness',lambda:coupled.validate_closed_tree(bad_index),rejected)
        rejection('false_reference_Gamma',lambda:coupled.replay_winning_cover(leaves,coeff,F(100)),rejected)
        rejection('receiving_intercept_below_tied_original',lambda:weighted.receiving_envelope(n,V,H,normals,
                       cap=F(scalar['threshold_normal_chord_bound']),height_bound=F(1,2)),rejected)
        rejection('old_Gamma_insufficient_on_new_domain',lambda:scalars(gamma=F(1,16)),rejected)
        rejection('unsupported_lower_receiving_height',lambda:scalars(q=F(33,80)),rejected)
        demand(len(rejected)==12,'all twelve malformed certificate controls')
    return dict(agent='six-rupert-3',role='researcher',
                proof_status='complete_written_unformalized_author_checked_branch_exclusion',
                independently_reviewed=False,global_RID_status='OPEN',
                branch='all winning signed-region sources into threshold signed-region receivers f(n)>=83/200',
                closed_exclusion_all_original_proper_Q_planar_t_lambda_at_least_one=True,
                explicit_source_branch_squared_height_band='f(n)^2>=beta-1/28',
                global_receiving_squared_height_gap='1/100 unchanged',
                stronger_GLOBAL_gap_proved=False,initial_full_rotation_angle_premise=False,
                all60_original_vertices=[encode(v) for v in sorted(V)],
                original_source_geometry=source,whole_region_scalar_certificate=scalar,
                all_six_validated_outward_positive_root_enclosures=roots,
                regenerated_winning_tangent_geometry_sha256=digest(win_geometry),
                regenerated_both_threshold_tangent_geometries_sha256=digest(threshold_geometry),
                sharp_winning_tangent_disk_squared=(QPhi(F(8,3))+4*PHI).encode(),
                sharp_threshold_tangent_disk_squared=((39+37*PHI)/29).encode(),
                directed_proper_gauge_checks=orbits,both_receiving_reference_cases=cases,
                published47_input_pins_checked=True,input_manifest_sha256=INPUT_SHA,
                malformed_controls_rejected=rejected,
                previous436region_spectrum_reenumerated=False,
                previous_old_Gamma1over16_credited_to_review7576=True,
                new_independent_reviewer_verdict_requested=False,
                continuous_geometric_proof='GAMMA_BRANCH_PROOF.md')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--emit',action='store_true')
    args=parser.parse_args()
    result=check(args.self_test)
    raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
    if args.emit:
        print(raw.decode(),end='')
    else:
        demand(args.self_test,'published verification includes all malformed controls')
        demand(raw==(HERE/'gamma_branch_expected.json').read_bytes(),
               'every compact expected certificate byte must match')
        print(json.dumps(dict(status='verified_every_expected_byte',bytes=len(raw),
                              sha256=hashlib.sha256(raw).hexdigest(),closed_roll_leaves=84,
                              selected_exact_Bernstein_bounds=252,original_receiving_envelopes=1920,
                              scalar_gates=10,malformed_controls_rejected=12,
                              source_branch_only=True,global_receiving_gap='1/100'),sort_keys=True))


if __name__=='__main__':
    main()
