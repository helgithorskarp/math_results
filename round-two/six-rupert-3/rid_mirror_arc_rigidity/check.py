#!/usr/bin/env python3
"""Exact finite hypotheses for all-source RID rigidity on two mirror arcs.

The continuum matching, orientation, row-locking and area arguments are in
PROOF.md. This checker replays three complete pinned prerequisite records,
then checks actual originals, affine supports throughout both intervals,
physical endpoint hulls, finite circle maps and every new scalar bound.
Python 3.11+, standard library only. No floating-point decisions.
"""
from fractions import Fraction as Q
from importlib.util import module_from_spec, spec_from_file_location
from itertools import permutations, product
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_dependency():
    record = json.loads((HERE/'DEPENDENCIES.json').read_text())
    directory = (HERE/record['directory']).resolve()
    require(set(record['sha256']) == {'check.py', 'expected.json', 'PROOF.md', 'DEPENDENCIES.json'},
            'dependency fingerprint list differs')
    for name, digest in record['sha256'].items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest() == digest,
                'width prerequisite source changed: '+name)
    require('field' not in sys.modules, 'unverified arithmetic was already imported')
    spec = spec_from_file_location('rid_width_dependency', directory/'check.py')
    width = module_from_spec(spec)
    spec.loader.exec_module(width)
    regenerated = json.dumps(width.verify(), indent=2, sort_keys=True)+'\n'
    require(regenerated == (directory/'expected.json').read_text(),
            'complete width prerequisite did not replay')
    cap_record = json.loads((directory/'DEPENDENCIES.json').read_text())
    cap_path = (directory/cap_record['directory']).resolve()
    base_record = json.loads((cap_path/'DEPENDENCIES.json').read_text())
    base_path = (cap_path/base_record['directory']).resolve()
    require(Path(sys.modules['field'].__file__).resolve() == base_path/'field.py',
            'arithmetic import is not the verified brightness source')
    # Both hashes were checked before the complete nested replay. Check again
    # before sharing its exact arithmetic and geometry in this certificate.
    for name in ('field.py', 'verify.py'):
        require(hashlib.sha256((base_path/name).read_bytes()).hexdigest()
                == base_record['sha256'][name], 'brightness source changed after replay')
    spec = spec_from_file_location('rid_arc_geometry', base_path/'verify.py')
    base = module_from_spec(spec)
    spec.loader.exec_module(base)
    return base, record


def original_geometry(b, V, equator):
    F, phi, zero = b.F, b.PHI, b.ZERO
    R2, a, c, peak = 7+8*phi, phi**2, 2+phi, phi**3
    actual = {v for v in V if v[2] == zero}
    require(len(V) == len(set(V)) == 60 and all(b.neg(v) in V for v in V),
            'original vertex set or central symmetry differs')
    require(len(equator) == len(set(equator)) == 4 and set(equator) == actual,
            'equatorial set is not four complete actual originals')
    require(actual == {(sx*a, sy*c, zero) for sx, sy in product((-1, 1), repeat=2)},
            'actual equatorial rectangle differs')
    require(all(b.dot(v, v) == R2 for v in V), 'original circumradii differ')
    require(all(abs(v[2]) >= b.ONE for v in V if v not in actual),
            'nonequatorial originals lack unit axial height')
    require(all(abs(v[i]) <= peak for v in V for i in range(3)),
            'original coordinate peak differs')
    locking = {}
    for j in (0, 1):
        points = []
        for signs in product((-1, 1), repeat=2):
            others = iter(signs)
            points.append(tuple(peak if i == j else F(next(others)) for i in range(3)))
        require(len(set(points)) == 4 and all(v in V for v in points),
                'four actual row-locking originals absent')
        locking['x' if j == 0 else 'y'] = [b.encode(v) for v in points]
    return dict(original_vertices=60, equatorial_originals=4, nonequatorial_originals=56,
                circumradius_squared=R2.encode(), equatorial_rectangle_halfwidth=a.encode(),
                equatorial_rectangle_halfheight=c.encode(), coordinate_support_peak=peak.encode(),
                minimum_nonequatorial_axial_height='1', row_locking_originals=locking,
                equatorial_originals_sha256=b.digest([b.encode(v) for v in equator]))


def matching_gates(b, epsilon=Q(11, 20), row_radius=Q(4, 15)):
    F, phi = b.F, b.PHI
    R2, a, c, peak = 7+8*phi, phi**2, 2+phi, phi**3
    require(F(Q(22, 5)**2) < R2 < F(20) < F(Q(9, 2)**2) and peak < F(Q(9, 2)),
            'positive circumradius or coordinate root bounds fail')
    require(1-Q(3, 25)**2 > Q(24, 25)**2 and Q(144, 145) > Q(24, 25)**2,
            'source or receiver positive normal height fails')
    require(Q(20)*Q(3, 25)**2 == Q(36, 125) and
            Q(5, 8)**2*Q(144, 145) == Q(45, 116) and
            Q(45, 116) > Q(36, 125) and Q(36, 125) < epsilon**2,
            'radial support separation or matching error bound fails')
    require(2*a*Q(24, 25) > F(2*epsilon), 'distinct circle match is not forced')
    require(2*c*Q(24, 25)-2*a > F(2*epsilon), 'long and short sides can be swapped')
    orientation_error = 2*epsilon*2*(a+c)+4*epsilon*epsilon
    require(orientation_error < 4*a*c*Q(24, 25), 'proper triangle orientation is not robust')
    source_drift, receiver_drift = Q(9, 256), Q(1, 64)
    require(Q(9, 2)*Q(1, 8)**2/2 == source_drift and
            Q(9, 2)*Q(1, 12)**2/2 == receiver_drift,
            'quadratic equatorial transport constants differ')
    roll = Q(5, 22)*(epsilon+source_drift+receiver_drift)
    full = Q(1, 8)+roll
    require(full < row_radius and 1-row_radius**2/2 > Q(9, 10),
            'full frame or positive row cap fails')
    lock = Q(9, 2)*row_radius/Q(19, 10)
    require(lock < 1, 'row-locking contradiction is not strict')
    require(Q(14)-Q(58)*Q(3, 25)/Q(24, 25) > 0,
            'locked source arc area is not increasing')
    return dict(source_twofold_tangent_upper='3/25', source_twofold_chord_upper='1/8',
                receiver_twofold_chord_upper='1/12', projected_equator_smallest_singular_value_lower='24/25',
                source_equatorial_squared_height_upper='36/125',
                receiver_nonequatorial_squared_height_lower='45/116', circle_matching_error_upper=str(epsilon),
                orientation_determinant_error_upper=orientation_error.encode(),
                orientation_determinant_magnitude_lower=(4*a*c*Q(24, 25)).encode(),
                source_equatorial_transport_error_upper=str(source_drift),
                receiver_equatorial_transport_error_upper=str(receiver_drift),
                residual_roll_operator_distance_upper=str(roll), full_frame_operator_distance_upper=str(full),
                row_distance_upper=str(row_radius), row_locking_scalar_upper=str(lock),
                locked_source_area_derivative_lower='27/4')


def triangle(b, a, c, d):
    return (c[0]-a[0])*(d[1]-a[1])-(c[1]-a[1])*(d[0]-a[0])


def circle_map(b, E, mapping):
    require(sorted(mapping) == list(range(4)), 'circle map is not bijective')
    anti = {i:E.index(b.neg(v)) for i, v in enumerate(E)}
    require(all(mapping[anti[i]] == anti[mapping[i]] for i in range(4)),
            'circle map is not antipodal')
    require(all(b.dot(b.sub(E[i], E[j]), b.sub(E[i], E[j])) ==
                b.dot(b.sub(E[mapping[i]], E[mapping[j]]), b.sub(E[mapping[i]], E[mapping[j]]))
                for i in range(4) for j in range(i)), 'circle map swaps rectangle side types')
    require(triangle(b, E[0], E[1], E[2])*
            triangle(b, E[mapping[0]], E[mapping[1]], E[mapping[2]]) > b.ZERO,
            'circle map reverses proper orientation')


def circle_maps(b, E):
    maps = []
    for mapping in permutations(range(4)):
        try:
            circle_map(b, E, mapping)
        except ValueError:
            continue
        maps.append(mapping)
    anti = tuple(E.index(b.neg(v)) for v in E)
    require(set(maps) == {tuple(range(4)), anti}, 'proper circle survivors differ')
    return dict(circle_permutations_checked=24, proper_circle_survivors=[list(x) for x in maps])


def area_geometry(b, V):
    planes, _ = b.complete_facets(V)
    C, _, _ = b.area_generators(V, planes)
    zero, one, phi = b.ZERO, b.ONE, b.PHI
    e = (zero, zero, one)
    D = [v for v in C if b.dot(v, e) == zero]
    nonzero = [v for v in C if b.dot(v, e) != zero]
    require(len(C) == 31 and len(D) == 6 and len(nonzero) == 25,
            'twofold area generator partition differs')
    signed = tuple(sum((b.dot(v, e).sign()*v[i] for v in nonzero), zero) for i in range(3))
    require(signed == (zero, zero, 12+28*phi), 'twofold signed area sum differs')
    stability = min(b.dot(v, e)**2/b.dot(v, v) for v in nonzero)
    require(stability == (2-phi)/4 and stability > b.F(Q(1, 8)**2),
            'nonzero area signs can change in the source cap')
    return D, dict(area_generators=31, zero_axial_area_generators=6,
                   nonzero_axial_area_generators=25, signed_nonzero_area_sum=b.encode(signed),
                   minimum_normalized_nonzero_axial_dot_squared=stability.encode())


def receiver_arc(b, V, D, axis, upper=Q(1, 12), support_sign=1):
    require(axis in (0, 1) and 0 < upper <= Q(1, 12), 'receiver arc outside declared domain')
    F, phi, zero, one = b.F, b.PHI, b.ZERO, b.ONE
    e = (zero, zero, one)
    tangent = (one, zero, zero) if axis == 0 else (zero, one, zero)
    A0, H = 12+28*phi, b.brightness_raw(D, tangent)
    require(H == (4+8*phi if axis == 0 else 8+4*phi) and H > F(14) and A0 < F(58),
            'mirror-plane area coefficients differ')
    require(H-A0*upper > zero, 'receiver area is not increasing on the whole interval')
    # A scaled endpoint normal; direct_shadow_raw includes its physical Jacobian.
    r = tuple(e[i]/upper+tangent[i] for i in range(3))
    raw, corners = b.direct_shadow_raw(V, r)
    require(raw == A0/upper+H, 'independent physical endpoint hull disagrees with area formula')
    area2 = raw*raw/b.dot(r, r)
    require(area2 < F(Q(1171, 20)**2) and 940+1520*phi > F(Q(583, 10)**2),
            'entire receiver area is not below A1+1/4')
    z0, z1 = (phi, one, zero), (zero, zero, -phi if axis == 0 else -one)
    require(b.dot(e, z0) == zero and b.dot(tangent, z0)+b.dot(e, z1) == zero and
            b.dot(tangent, z1) == zero, 'width direction is not perpendicular throughout')
    B, k, ell = 3*phi**2, support_sign*(phi**2 if axis == 0 else phi), phi**2 if axis == 0 else one
    witness = (2*phi, phi**2, -phi)
    require(witness in V and b.dot(witness, z0) == B and b.dot(witness, z1) == k,
            'actual width support witness coefficients differ')
    support_checks = 0
    for s in (Q(0), upper):
        z = tuple(z0[i]+s*z1[i] for i in range(3))
        for v in V:
            require(b.dot(v, z) <= B+k*s, 'affine support endpoint inequality fails')
            support_checks += 1
    S = phi+2
    require(b.dot(z0, z0) == S and b.dot(z0, z1) == zero and b.dot(z1, z1) == ell,
            'physical width denominator coefficients differ')
    require(B > zero and k > zero and k*S-ell*B*upper > zero,
            'receiver directional width is not increasing on the whole interval')
    width2 = 4*(B+k*upper)**2/(S+ell*upper*upper)
    width_limit = 4*phi**6*(1-Q(10, 729)*Q(1, 4)**2)
    require(width2 < width_limit and corners == 16, 'endpoint width budget or actual hull differs')
    return dict(axis='x' if axis == 0 else 'y', arc_parameter_interval=['0', str(upper)],
                tangent_area_slope=H.encode(), endpoint_receiving_raw=b.encode(r),
                physical_endpoint_area_squared=area2.encode(), endpoint_hull_corners=corners,
                directional_width_constant=B.encode(), directional_width_slope=k.encode(),
                directional_width_denominator_constant=S.encode(), directional_width_denominator_quadratic=ell.encode(),
                actual_width_support_witness=b.encode(witness), affine_support_endpoint_checks=support_checks,
                endpoint_directional_width_squared=width2.encode(), endpoint_width_squared_margin=(width_limit-width2).encode())


def negative_controls(b, V, E, D):
    cases = [lambda:original_geometry(b, V, E[:-1]),
             lambda:matching_gates(b, epsilon=Q(1, 4)),
             lambda:matching_gates(b, row_radius=Q(1, 2)),
             lambda:circle_map(b, E, (0, 2, 1, 3)),
             lambda:circle_map(b, E, (2, 3, 0, 1)),
             lambda:receiver_arc(b, V, D, 0, support_sign=-1)]
    for case in cases:
        try:
            case()
        except ValueError:
            continue
        raise ValueError('damaged mathematical control accepted')
    return len(cases)


def verify():
    b, dependency = load_dependency()
    V, G = b.vertices(), b.proper_group(b.vertices())
    E = sorted([v for v in V if v[2] == b.ZERO], key=b.key)
    require(len(G) == 60, 'proper body group order differs')
    Rz = ((-b.ONE, b.ZERO, b.ZERO), (b.ZERO, -b.ONE, b.ZERO), (b.ZERO, b.ZERO, b.ONE))
    require(Rz in G, 'negative-tilt proper spatial body lift absent')
    geometry = original_geometry(b, V, E)
    gates = matching_gates(b)
    maps = circle_maps(b, E)
    D, areas = area_geometry(b, V)
    arcs = [receiver_arc(b, V, D, axis) for axis in (0, 1)]
    return dict(agent='six-rupert-3', role='researcher', arithmetic='exact ordered Q(phi)',
                proof_status='written all-source closed-fit classification with exact finite hypotheses',
                global_RID_Rupert_status='unresolved', dependency_commit=dependency['source_commit'],
                dependency_graph=dependency['graph_ref'], prerequisite_replay='every byte of all three earlier expected records',
                proper_body_rotations=60, receiver_arc_families=arcs,
                receiving_set='proper body images of both n=(s,0,1)/sqrt(1+s^2),n=(0,s,1)/sqrt(1+s^2),0<=s<=1/12',
                closed_fit_classification='lambda=1,t=0,B1=sigma*B2*g; sigma in {+1,-1},g a proper body rotation',
                motion_scope='arbitrary source normal, proper planar roll and physical translation before reduction',
                strict_fit_status='excluded on the whole compact mirror-arc union; full RID remains open',
                malformed_controls_rejected=negative_controls(b, V, E, D), **geometry, **gates, **maps, **areas)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    output = json.dumps(verify(), indent=2, sort_keys=True)+'\n'
    if not args.emit:
        require(output == (HERE/'expected.json').read_text(), 'new expected record differs')
    print(output, end='')


if __name__ == '__main__':
    main()
