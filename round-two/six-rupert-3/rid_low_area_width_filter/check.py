#!/usr/bin/env python3
"""Exact finite hypotheses for the RID area/width source-domain filter.

The written proof supplies all continuum implications. This program replays
the hash-pinned geometry/cap certificate, then reconstructs original contact
edges, checks their robust convexity, tests physical projected-line identities
and verifies every rational/positive-root gate used in the new theorem.
"""
from fractions import Fraction as Q
from importlib.util import module_from_spec, spec_from_file_location
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
                'dependency source changed: '+name)
    spec = spec_from_file_location('fivefold_cap_dependency', directory/'check.py')
    cap = module_from_spec(spec)
    spec.loader.exec_module(cap)
    regenerated = json.dumps(cap.verify(), indent=2, sort_keys=True)+'\n'
    require(regenerated == (directory/'expected.json').read_text(),
            'complete fivefold prerequisite did not replay')
    parent = json.loads((directory/'DEPENDENCIES.json').read_text())
    basepath = (directory/parent['directory']).resolve()
    # The preceding full replay checked all four parent hashes before import.
    require(Path(sys.modules['field'].__file__).resolve() == basepath/'field.py',
            'arithmetic import is not the verified parent')
    require(hashlib.sha256((basepath/'verify.py').read_bytes()).hexdigest()
            == parent['sha256']['verify.py'], 'parent changed after replay')
    spec = spec_from_file_location('brightness_geometry', basepath/'verify.py')
    base = module_from_spec(spec)
    spec.loader.exec_module(base)
    return base, record


def contact_order(b, V, w):
    p2 = (7-4*b.PHI)/5
    s = b.dot(w, w)
    J = [v for v in V if b.dot(w, v)**2/s == p2]
    u = (-b.PHI, b.ZERO, b.ZERO)
    t = b.cross(w, u)
    by_point = {(b.dot(u, v), b.dot(t, v)):v for v in J}
    require(len(by_point) == len(J) == 10, 'original contact projection collision')
    points = sorted(by_point)
    def turn(a, c, d):
        return (c[0]-a[0])*(d[1]-a[1])-(c[1]-a[1])*(d[0]-a[0])
    def half(seq):
        result = []
        for q in seq:
            while len(result)>1 and turn(result[-2], result[-1], q)<=b.ZERO:
                result.pop()
            result.append(q)
        return result
    hull = half(points)[:-1]+half(reversed(points))[:-1]
    require(len(hull) == 10, 'reference contact polygon is not a decagon')
    return [by_point[q] for q in hull]


def edge_geometry(b, V, ring, w, radius=Q(1, 30)):
    F, phi, zero = b.F, b.PHI, b.ZERO
    sn = b.dot(w, w)
    p2 = (7-4*phi)/5
    require(len(ring) == len(set(ring)) == 10 and set(ring)
            == {v for v in V if b.dot(w, v)**2/sn == p2},
            'contact loop is not ten distinct complete actual originals')
    require(all(b.neg(v) in ring for v in ring), 'contact loop is not centrally symmetric')
    require(0 < radius <= Q(1, 30), 'contact proof radius outside declared domain')
    p_upper, tangent_upper = Q(1, 3), Q(7, 5)
    require(p2 < F(p_upper*p_upper) and (3+4*phi)/5 < F(tangent_upper*tangent_upper),
            'positive height/halfedge root bounds fail')
    require(2-(p_upper+tangent_upper*radius)**2 > Q(9, 5),
            'projected edge denominator not above9/5')
    cosines = []
    identities = 0
    samples = [w, (F(Q(1, 100)), phi, b.ONE),
               (b.ZERO, phi+F(Q(1, 100)), b.ONE),
               (F(Q(1, 100)), phi+F(Q(1, 100)), b.ONE+F(Q(1, 100)))]
    for i, vi in enumerate(ring):
        vj = ring[(i+1)%10]
        M = tuple((vi[k]+vj[k])/2 for k in range(3))
        T = tuple((vj[k]-vi[k])/2 for k in range(3))
        require(b.dot(M, w) == zero and b.dot(M, M) == phi**6,
                'opposite-height equatorial midpoint identity fails')
        require(b.dot(M, T) == zero and b.dot(T, T) == F(2),
                'orthogonal midpoint/halfedge identity fails')
        require(b.dot(T, w)**2/sn == p2 and b.dot(T, T)-p2 == (3+4*phi)/5,
                'halfedge height/tangent identity fails')
        for vk in ring:
            if vk in (vi, vj):
                continue
            L = b.cross(b.sub(vj, vi), b.sub(vk, vi))
            ref = b.dot(w, L)
            require(ref > zero, 'contact loop has nonpositive orientation')
            ratio = ref*ref/(sn*b.dot(L, L))
            require(ratio > F(radius*radius), 'contact order unstable on whole chord cap')
            cosines.append(ratio)
        for r in samples:
            r2 = b.dot(r, r)
            PM = tuple(M[k]-r[k]*b.dot(r, M)/r2 for k in range(3))
            PT = tuple(T[k]-r[k]*b.dot(r, T)/r2 for k in range(3))
            pt2 = b.dot(PT, PT)
            require(pt2 > zero, 'sample projected edge is degenerate')
            direct = (b.dot(PM, PM)*pt2-b.dot(PM, PT)**2)/pt2
            reduced = phi**6-2*b.dot(r, M)**2/(2*r2-b.dot(r, T)**2)
            require(direct == reduced, 'physical Gram/edge-distance identity differs')
            identities += 1
    require(len(cosines) == 80 and identities == 40, 'edge check counts differ')
    return dict(original_contact_edges=10, robust_convexity_comparisons=80,
                minimum_normalized_boundary_dot_squared=min(cosines).encode(),
                contact_order_chord=str(radius), original_antipodal_contacts=10,
                edge_midpoint_squared_radius=(phi**6).encode(),
                edge_halfdifference_squared_length='2',
                edge_tangent_squared_radius=((3+4*phi)/5).encode(),
                physical_edge_distance_identity_checks=identities,
                projected_edge_squared_length_lower='9/5',
                contact_width_squared_lower='(20+32phi)*(1-(10/9)*d^2)')


def scalar_gates(b, eta=Q(1, 4), rstar=Q(3, 25)):
    F, phi = b.F, b.PHI
    A0, A1sq, A2sq = 12+28*phi, 940+1520*phi, 960+1536*phi
    rho2 = (288+464*phi)/5
    require(0 < eta <= Q(1, 4), 'area budget outside declared domain')
    U = Q(175, 3)+eta
    require(F(58**2)<A1sq<F(Q(175, 3)**2) and F(U*U)<A2sq,
            'area budget does not separate third polar level')
    require(2*eta/58<Q(1, 10)**2, 'initial fivefold chord not below1/10')
    require(48+64*phi>F(12**2), 'fivefold inradius not above12')
    require(Q(399, 400)**2<1-Q(1, 10)**2/4 and
            12*Q(399, 400)-Q(59, 20)>9, 'fivefold coercivity not above9')
    require(eta/9<=Q(1, 36)<Q(1, 30), 'source outside contact-order chord cap')
    rmax2 = 1-A0*A0/(U*U)
    require(0<rstar*rstar<rmax2<rho2/(A0*A0+rho2),
            'twofold tangent function not increasing throughout possible interval')
    comparison = U*U-A0*A0*(1-rstar*rstar)-rho2*rstar*rstar
    margin = 4*A0*A0*rho2*rstar*rstar*(1-rstar*rstar)-comparison*comparison
    require(comparison>0 and margin>0, 'twofold positive-root upper-radius gate fails')
    require(rstar*rstar<Q(1, 8)**2*(1-Q(1, 8)**2/4), 'twofold chord1/8 fails')
    return dict(edge_two_area_excess_budget=str(eta),
                area_rational_upper=str(U), fivefold_initial_chord_upper='1/10',
                fivefold_coercivity_lower='9', fivefold_source_chord_upper=str(eta/9),
                source_fivefold_width_squared_lower=(4*phi**6*(1-Q(10, 729)*eta*eta)).encode(),
                surviving_twofold_tangent_upper=str(rstar), surviving_twofold_chord_upper='1/8',
                twofold_polar_tangent_squared_upper=rmax2.encode(),
                twofold_positive_root_comparison=comparison.encode(),
                twofold_positive_root_margin=margin.encode())


def receiver_example(b, V, G, width_sign=-1):
    F, phi, zero = b.F, b.PHI, b.ZERO
    r = (F(1), zero, F(12))
    r2 = b.dot(r, r)
    raw, corners = b.direct_shadow_raw(V, r)
    area2 = raw*raw/r2
    f2 = min(b.dot(r, v)**2/r2 for v in V)
    z = (12*phi, F(12), width_sign*phi)
    require(b.dot(r, z) == zero, 'receiver width direction not perpendicular')
    width2 = 4*max(b.dot(z, v) for v in V)**2/b.dot(z, z)
    limit = 4*phi**6*(1-Q(10, 729)*Q(1, 4)**2)
    require(F(Q(583, 10)**2)<940+1520*phi and area2<F(Q(1171, 20)**2),
            'receiver area not below A1+1/4')
    require(area2>940+1520*phi and area2<960+1536*phi and corners == 16,
            'receiver is not the specified sixteen-corner shadow in the second-level band')
    require(width2<limit, 'receiving width does not reject tilted fivefold sources')
    lower = f2/(2+phi)**2
    require(lower>F(Q(1, 17)**2), 'twofold source annulus lower bound fails')
    e2 = (zero, zero, b.ONE)
    w = (zero, phi, b.ONE)
    cos2_twofold = max(b.dot(r, b.act(g, e2)) for g in G)**2/r2
    cos2_fivefold = max(b.dot(r, b.act(g, w)) for g in G)**2/(r2*b.dot(w, w))
    require(cos2_twofold<(1-F(Q(1, 145800)))**2 and
            cos2_fivefold<(1-F(Q(1, 4500000)))**2 and f2<F(Q(6889, 40000)),
            'example is inside one of the specified prior receiving exclusions')
    require((1-F(Q(1, 128)))**2<cos2_twofold<(1-F(Q(1, 578)))**2,
            'known identity closed fit is outside the claimed source annulus')
    return dict(example_receiving_raw=b.encode(r), example_receiving_norm_squared=r2.encode(),
                example_receiving_area_squared=area2.encode(), example_shadow_corners=corners,
                example_minimum_height_squared=f2.encode(),
                example_actual_perpendicular_width_direction=b.encode(z),
                example_actual_width_squared=width2.encode(), example_width_squared_margin=(limit-width2).encode(),
                example_source_tangent_squared_lower=lower.encode(), example_source_chord_lower='1/17',
                example_identity_closed_fit_inside_annulus=True,
                example_outside_current_twofold_fivefold_caps_and_83_over_200_height_band=True,
                example_all_source_nonpassage_status='unresolved; remaining twofold annuli and roll')


def negative_controls(b, V, G, ring, w):
    cases = [lambda:edge_geometry(b, V, ring[:-1], w),
             lambda:edge_geometry(b, V, ring[:-1]+[ring[0]], w),
             lambda:edge_geometry(b, V, list(reversed(ring)), w),
             lambda:scalar_gates(b, Q(1, 3)),
             lambda:scalar_gates(b, rstar=Q(1, 10)),
             lambda:receiver_example(b, V, G, width_sign=1)]
    for case in cases:
        try:
            case()
        except ValueError:
            continue
        raise ValueError('malformed or out-of-budget control accepted')
    return len(cases)


def verify():
    b, dependency = load_dependency()
    V, w = b.vertices(), (b.ZERO, b.PHI, b.ONE)
    ring = contact_order(b, V, w)
    edges = edge_geometry(b, V, ring, w)
    G = b.proper_group(V)
    gates = scalar_gates(b)
    example = receiver_example(b, V, G)
    return dict(agent='six-rupert-3', role='researcher', arithmetic='exact ordered Q(phi)',
                proof_status='written source-domain reduction with exact finite hypotheses',
                global_RID_Rupert_status='unresolved', dependency_commit=dependency['source_commit'],
                dependency_graph=dependency['graph_ref'], dependency_replay='every byte of both earlier expected records',
                contact_loop_sha256=b.digest([b.encode(v) for v in ring]),
                main_filter='A(receiver)<=A1+eta and minwidth(receiver)^2<=(20+32phi)*(1-10eta^2/729)',
                conclusion='every closed fit at scale>=1 has source chord<1/8 from a twofold axis',
                proper_roll_translation_scope='arbitrary proper roll and physical translation; no source-nearness premise',
                malformed_controls_rejected=negative_controls(b, V, G, ring, w),
                **edges, **gates, **example)


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
