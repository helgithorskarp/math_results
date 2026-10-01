#!/usr/bin/env python3
"""Exact gates for a uniform all-source fivefold receiver cap.

This checks the finite premises of the complete geometric reduction in
PROOF.md. Python 3.11+ standard library; exact arithmetic only.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
NEIGHBOR = HERE.parent / 'pentagonal_fivefold_neighborhood'
NEIGHBOR_HASH = '859ed5887565853fb3850ffc06ce9a4a7aae35d3d1e83af9b71a0b8a286f14ae'
if hashlib.sha256((NEIGHBOR/'check.py').read_bytes()).hexdigest() != NEIGHBOR_HASH:
    raise ValueError('neighborhood arithmetic/model source changed')
sys.path.insert(0, str(NEIGHBOR))
import check as C
import verify as V

EPS = F(1, 100000)
KAPPA = F(999, 1000)
RADIUS = F(1, 1000000)
LOCAL_RADIUS = F(1, 10000)
LOCAL_ANGLE = F(1, 50)
BODY_RADIUS = F(11, 10)
TORQUE = F(1, 12)
NORMAL_DRIFT = F(7, 2)
WEIGHT_DRIFT = F(7)
PROBE_BOUND = F(6, 5)
DUALS_HASH = '5be0b452ec1e2f323c7af57bdf8ea24ad6c53538a6a89f4caf64f1e1de2f600e'


def projection(v):
    height = V.ldot(V.N, v)
    return tuple(V.ladd(x, V.lscale(-n/V.H, height))
                 for x, n in zip(v, V.N))


def source_budget(vs, mats):
    path = HERE.parent/'pentagonal_minimum_diameter/duals.json'
    V.require(hashlib.sha256(path.read_bytes()).hexdigest() == DUALS_HASH,
              'signed-cover data changed')
    D, E = V.orbit_rows(vs)
    margin = V.cover_check(mats, D, E, json.loads(path.read_text()))
    V.require(margin > F(1, 250), 'signed-cover relative margin too small')
    V.require(KAPPA*KAPPA > 1-F(1, 250), 'relaxed weighted RHS loses margin')
    h, r, a = V.qi(V.H), V.BOX[2], V.BOX[3]
    ico = h.square()-(h+r.square()*(h-1)+h*EPS/4)/a.square()
    V.require(ico.lo > V.B0*V.B0, 'relaxed ico threshold misses B0')
    diff = (1-KAPPA*KAPPA)*r.square()-h*EPS/4
    V.require(diff.lo > 0, 'relaxed difference threshold misses kappa*r')
    # The transverse regular pentagon has radius>1, hence inradius>phi/2.
    # Positive row signs and actual threshold b=sqrt(r^2-h*epsilon/4)
    # give cos(gamma)>=kappa and the displayed linear chord coefficient.
    chord_coefficient = h.sqrt()/(2*V.qi(V.PHI)*(1+KAPPA)*r
                                 *V.I.coerce((1+KAPPA)/2).sqrt())
    V.require(chord_coefficient.hi < 3, 'source chord coefficient too large')
    return {'signed_cover_duals': 238,
            'signed_cover_relative_margin_lower_bound': '1/250',
            'source_squared_diameter_budget': str(EPS),
            'source_chord_per_budget': '3',
            'relaxed_ico_threshold_above_B0': True,
            'relaxed_difference_threshold_above_kappa_r': True,
            'source_chord_coefficient_upper_bound': str(chord_coefficient.hi)}


def outer_points(vs):
    # alpha=phi*r-u: short projected edge half length*sqrt(h).
    # beta=phi*u+r: longitudinal edge component/contact transverse torque.
    # eta=phi*r+u: LONG projected edge half length*sqrt(h).
    eta = V.ladd(V.lscale(V.PHI, V.lf(2)), V.lf(1))
    circum = V.poly_add({(0, 0): V.ONE}, V.poly_square(eta), V.ONE/V.H)
    top, gaps = [], []
    for i, p in enumerate(vs):
        gap = V.poly_add(circum, C.projected_length_squared(p), -V.ONE)
        if not gap:
            top.append(i)
        else:
            b = V.poly_interval(gap, V.BOX)
            V.require(b.lo > F(1, 100), f'outer radial gap too small at{i}')
            gaps.append(b.lo)
    v = (V.lf(2, -V.ONE), V.lf(0), V.lf(1))
    w = (V.lf(2), V.lf(0), V.lf(1, -V.ONE))
    expected = set()
    projected = []
    for _ in range(5):
        expected.update((vs.index(v), vs.index(w)))
        projected.extend((projection(v), projection(w)))
        v, w = V.lmv(V.G, v), V.lmv(V.G, w)
    V.require(len(top) == 10 and set(top) == expected and len(gaps) == 82,
              'maximal shadow points are not the two long-edge endpoint orbits')
    h = V.qi(V.H)
    eta_i = V.linterval(eta, V.BOX)
    denom = h+eta_i.square()
    c = (h-3*eta_i.square())/denom
    d = eta_i*(3*h-eta_i.square())/(h*denom)
    # Q maps the base projected v=m-eta/h*U to w=m+eta/h*U,
    # where U=(phi,0,-1). Q^2 v has the following exact rational form.
    q2v = (d*V.qi(V.PHI), c, -d)
    radius2 = V.poly_interval(circum, V.BOX)
    V.require(radius2.lo > 1, 'outer radius must exceed one')
    branch = []
    for p in projected:
        pi = tuple(V.linterval(x, V.BOX) for x in p)
        distance = sum(((x-y).square() for x, y in zip(q2v, pi)), V.I(0, 0))
        V.require(distance.lo > radius2.hi/16, 'wrong roll branch too close')
        branch.append(distance.lo-radius2.hi/16)
    V.require(min(branch) > F(1, 100), 'wrong roll squared margin too small')
    return {'maximal_shadow_radius_points': 10,
            'strict_radial_comparisons': 82,
            'squared_radial_gap_lower_bound': '1/100',
            'wrong_roll_branch_comparisons': 10,
            'wrong_roll_branch_squared_margin_lower_bound': '1/100',
            'maximal_shadow_radius_squared': [str(radius2.lo), str(radius2.hi)]}


def contact_gates(vs):
    m = (V.Z, -V.ONE, V.Z)
    v = (V.lf(2, -V.ONE), V.lf(0, -V.ONE), V.lf(1, -V.ONE))
    w = (V.lf(2), V.lf(0, -V.ONE), V.lf(1))
    gaps = []
    for p in vs:
        d = V.ldot(m, C.sub(v, p))
        if p in (v, w):
            V.require(d == V.lf(0, V.Z), 'short-edge endpoint support changed')
        else:
            b = V.linterval(d, V.BOX)
            V.require(b.lo > F(1, 20), 'short-edge unit support gap too small')
            gaps.append(b.lo)
    alpha = V.ladd(V.lscale(V.PHI, V.lf(2)), V.lf(1, -V.ONE))
    beta = V.ladd(V.lscale(V.PHI, V.lf(1)), V.lf(2))
    alpha2, beta2 = V.poly_square(alpha), V.poly_square(beta)
    ai, bi = V.linterval(alpha, V.BOX), V.linterval(beta, V.BOX)
    h = V.qi(V.H)
    V.require(ai.lo > 0 and bi.lo > 0, 'contact signs changed')
    V.require((5*ai.square()/h).lo > TORQUE*TORQUE,
              'axial torque lower bound too small')
    V.require((bi.square()-2*ai.square()).lo > 0,
              'transverse torque lower bound too small')
    L2 = h*(V.BOX[1].square()+V.BOX[2].square())/ai.square()
    V.require(L2.hi < NORMAL_DRIFT*NORMAL_DRIFT, 'normal drift too large')
    c_min = 1-LOCAL_RADIUS*LOCAL_RADIUS/2
    W = 2*bi/(c_min*ai)
    V.require(W.hi < WEIGHT_DRIFT, 'positive edge-normal weights drift too much')
    V.require(1-WEIGHT_DRIFT*LOCAL_RADIUS > 0, 'weights may become negative')
    V.require(BODY_RADIUS*(1+NORMAL_DRIFT*LOCAL_RADIUS) < PROBE_BOUND,
              'probe displacement bound too small')
    V.require(F(1, 20)-2*BODY_RADIUS*NORMAL_DRIFT*LOCAL_RADIUS > 0,
              'actual edge no longer supporting')
    # Exact C5 moment identities for transported-edge weights and torque.
    edge = C.sub(w, v)
    torque = C.linear_cross(v, m)
    axial = V.ldot(V.N, edge)
    transverse = tuple(V.ladd(x, V.lscale(-n/V.H, axial))
                       for x, n in zip(edge, V.N))
    tmom = [[{} for _ in range(3)] for _ in range(3)]
    amom = [[{} for _ in range(3)] for _ in range(3)]
    tsum = [V.lf(0, V.Z)]*3
    for _ in range(5):
        tsum = [V.ladd(x, y) for x, y in zip(tsum, transverse)]
        for j in range(3):
            for k in range(3):
                tmom[j][k] = V.poly_add(tmom[j][k], C.multiply(transverse[j], transverse[k]))
                amom[j][k] = V.poly_add(amom[j][k], C.multiply(torque[j], torque[k]))
        transverse, torque = V.lmv(V.G, transverse), V.lmv(V.G, torque)
    V.require(tuple(tsum) == (V.lf(0, V.Z),)*3, 'edge transverse sum nonzero')
    for j in range(3):
        for k in range(3):
            Pjk = (V.ONE if j == k else V.Z)-V.N[j]*V.N[k]/V.H
            t_expected = {e: 10*Pjk*c/V.H for e, c in alpha2.items() if Pjk*c != V.Z}
            a_expected = V.poly_add(
                {e: 5*V.N[j]*V.N[k]*c/(V.H*V.H)
                 for e, c in alpha2.items() if V.N[j]*V.N[k]*c != V.Z},
                {e: 5*Pjk*c/(2*V.H) for e, c in beta2.items() if Pjk*c != V.Z})
            V.require(tmom[j][k] == t_expected, 'edge weight second moment mismatch')
            V.require(amom[j][k] == a_expected, 'rotational torque second moment mismatch')
    margin = ((1-WEIGHT_DRIFT*LOCAL_RADIUS)*TORQUE
              -5*BODY_RADIUS*NORMAL_DRIFT*LOCAL_RADIUS
              -5*PROBE_BOUND*LOCAL_ANGLE/2)
    V.require(margin > 0, 'finite local-rotation remainder defeats torque')
    return {'strict_base_short_edge_supports': len(gaps),
            'unit_short_edge_gap_lower_bound': '1/20',
            'moment_entry_identities': 18,
            'local_receiver_chord': str(LOCAL_RADIUS),
            'local_relative_rotation_angle': str(LOCAL_ANGLE),
            'unit_axis_torque_lower_bound': str(TORQUE),
            'normal_drift_upper_bound': str(NORMAL_DRIFT),
            'weight_drift_upper_bound': str(WEIGHT_DRIFT),
            'local_strict_rotation_margin': str(margin)}


def final_gates():
    V.require((V.qi(V.H)*V.BOX[3].square()).hi < BODY_RADIUS*BODY_RADIUS,
              'old radius audit does not give advertised body bound')
    V.require(8*BODY_RADIUS*BODY_RADIUS < 10, 'diameter Lipschitz constant')
    V.require(10*RADIUS <= EPS, 'receiver cap exceeds global source budget')
    V.require(RADIUS <= LOCAL_RADIUS, 'receiver cap exceeds local support range')
    tilt_chord = 31*RADIUS
    shadow_error = 37*RADIUS
    V.require(BODY_RADIUS*(2*RADIUS+tilt_chord) < shadow_error,
              'shadow comparison error too small')
    V.require(2*BODY_RADIUS*shadow_error < F(1, 100),
              'nonmaximal target points cannot be ruled out')
    roll_chord = F(9, 1000)
    V.require(2*shadow_error < roll_chord*roll_chord, 'roll point match too loose')
    V.require(2*roll_chord < F(1, 4), 'wrong roll branch may survive')
    V.require(2*(tilt_chord+roll_chord) < LOCAL_ANGLE,
              'all-source roll/tilt bound exceeds local rotation range')
    return {'all_source_receiver_chord': str(RADIUS),
            'strict_passage_receiving_squared_diameter_gap': str(RADIUS/3),
            'folded_source_tilt_chord_upper_bound': str(tilt_chord),
            'centered_shadow_comparison_error': str(shadow_error),
            'roll_operator_chord_upper_bound': str(roll_chord),
            'full_relative_rotation_angle_upper_bound': str(2*(tilt_chord+roll_chord))}


def main():
    mats = V.group()
    vs = V.vertices(mats)
    out = {'agent':'six-rupert-1','role':'researcher',
           'claim':'effective all-source fivefold receiver caps and source diameter budget',
           'full_rupert_problem':'OPEN', 'floating_point_proof_decisions':0,
           'dependency_neighborhood_checker_sha256':NEIGHBOR_HASH,
           'source_duals_sha256':DUALS_HASH}
    out.update(source_budget(vs, mats))
    out.update(outer_points(vs))
    out.update(contact_gates(vs))
    out.update(final_gates())
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
