#!/usr/bin/env python3
"""Exact finite hypotheses for uniform RID local exclusion; see LOCAL_PROOF.md.

Python 3.11+ standard library, Q(phi) and Fraction only. This checks the
inherited whole-chamber certificate as well as the new critical-direction
identities and rational error bounds. No floating-point search is used.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from verify import PHI, QPhi, ZERO, act, check as check_mirror, dot, matmul, require, vertices
from torque_certificate import cross, determinant, subtract
from cell_certificate import check as check_cells, decode, encode, geometry

C = 3_000_000
THETA0 = Fraction(1, 10**16)


def scale(q, v):
    return tuple(q*x for x in v)


def add(v, w):
    return tuple(x+y for x,y in zip(v,w))


def cayley(w):
    """A rational proper rotation with parameter w, over Q(phi)."""
    return tuple(
        tuple(((1-dot(w,w))*QPhi(int(i==j))
               + 2*cross(w,tuple(QPhi(int(k==j)) for k in range(3)))[i]
               + 2*w[i]*w[j])/(1+dot(w,w)) for j in range(3)) for i in range(3))


def check_critical(loop_input=None, axis=None, radial_input=None, hidden=None, theta0=THETA0):
    V = vertices()
    require(theta0 == THETA0, 'only the stated rational exclusion angle is certified')
    u = (QPhi(1), PHI, 1+3*PHI)
    a = (QPhi(1), PHI, 1-PHI)
    b = (-PHI, QPhi(1), ZERO)
    if axis is not None:
        a = axis
    N, B = dot(u,u), dot(b,b)
    require(N == 12+16*PHI and B == 2+PHI, 'basis squared norms')
    require(dot(a,a) == QPhi(4) and dot(a,b) == dot(a,u) == dot(b,u) == ZERO,
            'orthogonal critical basis')
    require(cross(u,a) == scale(4*PHI,b), 'normal variation has the required sign')
    require(30 < N < 49 and 3 < B < 4 and 1+3*PHI < 6, 'basis brackets')
    cells, _, A, D = geometry()
    E = cells[2][2]
    require(scale(1+3*PHI,D) == u, 'critical chamber normalization')
    if loop_input is None:
        loop_input = json.loads(Path(__file__).with_name('limit_silhouette.json').read_text())
    L = list(map(decode,loop_input))
    require(len(L) == 16 and len(set(L)) == 16 and all(v in V for v in L),
            'sixteen silhouette vertices required')
    edges = [subtract(L[(j+1)%16],v) for j,v in enumerate(L)]
    corner_count = 0
    for j in range(6):
        require(dot(edges[j],edges[j]) == QPhi(4), 'length-two selected edge')
        for U in (A,D,E):
            m = cross(edges[j],U)
            for w in V:
                require(dot(m,subtract(L[j],w)) >= 0, 'selected edge fails support')
                corner_count += 1
    M = [cross(d,u) for d in edges]
    T = lambda j,v: cross(v,M[j])
    t0,t1,tm,tp,tn = T(1,L[1]),T(2,L[3]),T(3,L[4]),T(4,L[4]),T(0,L[1])
    require(add(scale(PHI,t0),t1) == (ZERO,ZERO,ZERO), 'opposite face contact torques')
    require(tm == scale(-2,u) and tp == scale(2,u), 'opposite radial contact torques')
    require(dot(a,t0) == ZERO and dot(b,t0) == QPhi(-4), 'face contact independence')
    require(dot(u,t0) == 16+24*PHI and 16+24*PHI < 56, 'face contact component')
    require(dot(a,tn) == QPhi(-4), 'negative contact selects positive a axis')
    require(all(dot(a,t) == ZERO for t in (t0,t1,tm,tp)), 'zero contact set')
    require(all(dot(m,m) < 196 for m in M[:6]), 'critical probes have norm less than 14')

    vplus = scale(PHI,add(a,b))
    vminus = scale(PHI,subtract(a,b))
    radial = [vplus,vminus,scale(-1,vplus),scale(-1,vminus)] if radial_input is None else radial_input
    require(len(radial) == 4 and set(radial) == {vplus,vminus,scale(-1,vplus),scale(-1,vminus)},
            'four specified equatorial vertices required')
    radial_count = 0
    radial_gap = None
    for v in radial:
        require(v in V and dot(u,v) == ZERO, 'equatorial vertex absent')
        for w in V-{v}:
            gap = dot(v,subtract(v,w))
            require(gap >= 2, 'equatorial radial gap is less than two')
            radial_gap = gap if radial_gap is None else min(radial_gap,gap)
            radial_count += 1
    require(radial_gap == QPhi(2), 'exact minimum radial gap two')

    hidden = (-2*PHI,PHI**2,-PHI) if hidden is None else hidden
    require(hidden in V and dot(M[5],subtract(hidden,L[5])) == ZERO,
            'specified hidden vertex must tie at D')
    hidden_linear = tuple(dot(cross(edges[5],r),subtract(hidden,L[5])) for r in (a,b,u))
    hidden_constant = 2*dot(a,T(5,hidden))
    require(hidden_linear == (ZERO,2*B,ZERO) and hidden_constant == 16+24*PHI,
            'hidden support derivative')
    upper = hidden_constant/(2*B)
    require(upper == N/5 and upper-4*PHI == (12-4*PHI)/5 > Fraction(4,5),
            'incompatible limiting bounds have a positive exact gap')
    shift = scale(8*PHI,b)
    factor = 32*PHI**3*B**2
    linear = tuple(2*sum((dot(v,r)*dot(v,shift) for v in (vplus,vminus)),ZERO)
                   for r in (a,b,u))
    constant = sum((dot(v,shift)**2 for v in (vplus,vminus)),ZERO)
    require(linear == (ZERO,factor,ZERO) and constant == 4*PHI*factor,
            'summed quadratic radial identity')
    require(PHI**3 > 4 and factor > 1000, 'quadratic factor lower bound')

    eps0 = theta0  # tan(theta/2)/2 <= theta for 0 <= theta <= 1.
    E0 = 21*C*eps0
    eta0 = 3*C*eps0
    scalar_checks = {
        'whole_chamber_or_mirror_case': theta0 < Fraction(1,200) and 200000*theta0 < Fraction(1,200),
        'bounded_rescaled_normal': 6*400000 < C,
        'probe_contact_error': 20*C+640 < 21*C,
        'small_contact_error': E0 < Fraction(1,1000),
        'axis_coordinate_bound': Fraction(1,4)*(1+Fraction(56,60)) < Fraction(1,2),
        'axis_sign': Fraction(18,5)-140*E0 > E0,
        'axis_distance_bound': 2*E0+2*E0**2 < 3*E0,
        'frame_alignment': 2*C+4 < 3*C,
        'radial_support_stability': 100*eta0+50*eta0**2 < 2,
        'normal_expansion_error': 882*C+4*C+64+112*eps0 < 1000*C,
        'base_radial_norm': 5*(C+32) < 6*C,
        'squared_radial_error': 50000000*eps0 < 1000,
        'hidden_support_error': 8820*C+40*C+1280+80*C*eps0 < 10000*C,
        'hidden_Y_error': Fraction(10000,6) < 2000,
        'final_incompatible_bounds': (200*C*C+2000*C)*eps0 < Fraction(4,5),
    }
    for label,passed in scalar_checks.items():
        require(passed, 'rational error audit failed: '+label)
    return {
        'normal':encode(u),'tangent_axis':encode(a),'other_tangent':encode(b),
        'normal_squared_norm':N.encode(),'selected_edge_corner_support_comparisons':corner_count,
        'radial_support_comparisons':radial_count,'minimum_radial_support_gap':radial_gap.encode(),
        'equatorial_vertices':list(map(encode,(vplus,vminus))),
        'polar_contacts':{'face_zero_pair':list(map(encode,(t0,t1))),
                          'radial_zero_pair':list(map(encode,(tm,tp))),
                          'negative_contact':encode(tn),'face_pair_first_weight':PHI.encode()},
        'hidden_outer_vertex':encode(L[5]),'hidden_source_vertex':encode(hidden),
        'hidden_edge':encode(edges[5]),'hidden_linear_X_Y_Z':encode(hidden_linear),
        'hidden_constant':hidden_constant.encode(),'limiting_upper_Y_magnitude':upper.encode(),
        'limiting_lower_Y_magnitude':(4*PHI).encode(),'strict_limiting_gap':(upper-4*PHI).encode(),
        'quadratic_factor':factor.encode(),'rescaled_normal_bound_C':C,
        'uniform_rotation_angle_radians':str(theta0),'contact_error_upper_bound':str(E0),
        'radial_frame_radius_upper_bound':str(eta0),
        'combined_Y_error_upper_bound':str((200*C*C+2000*C)*eps0),
        'rational_error_audits':len(scalar_checks),
    }


def self_test():
    V=vertices()
    a=(QPhi(1),PHI,1-PHI)
    L=json.loads(Path(__file__).with_name('limit_silhouette.json').read_text())
    good=check_critical()
    invalid=[{'axis':scale(-1,a)}, {'loop_input':L[::-1]},
             {'hidden':(-2*PHI,PHI**2,PHI)},
             {'radial_input':[decode(v) for v in good['equatorial_vertices']]},
             {'theta0':Fraction(1,1000)}]
    for changes in invalid:
        try:
            check_critical(**changes)
        except ValueError:
            pass
        else:
            raise ValueError('malformed critical certificate accepted')
    I=tuple(tuple(QPhi(int(i==j)) for j in range(3)) for i in range(3))
    for w in [(ZERO,ZERO,ZERO),scale(Fraction(1,17),a),
              (QPhi(Fraction(1,19)),PHI/23,QPhi(-1)/29)]:
        Q=cayley(w)
        require(matmul(tuple(zip(*Q)),Q)==I and determinant(*Q)==QPhi(1),
                'Cayley orthogonality/determinant identity')
        v=next(iter(V));outer=decode(good['hidden_outer_vertex']);m=decode(good['hidden_edge'])
        lhs=(1+dot(w,w))*dot(m,subtract(act(Q,v),outer))
        rhs=(1+dot(w,w))*dot(m,subtract(v,outer))+2*dot(w,cross(v,m))
        rhs+=2*(dot(w,v)*dot(w,m)-dot(w,w)*dot(v,m))
        require(lhs==rhs,'exact support numerator identity')


def check():
    cells=check_cells()
    mirror=check_mirror(vertices(),Fraction(1,100))
    cell_bytes=(json.dumps(cells,indent=2,sort_keys=True)+'\n').encode()
    return {'agent':'six-rupert-3','role':'researcher',
            'claim_status':'uniform_local_exclusion_with_exact_finite_hypotheses',
            'global_non_rupert_proved':False,
            'arithmetic':'Q(phi) and Fraction; no floating-point proof input',
            'inherited_cell_output_sha256':hashlib.sha256(cell_bytes).hexdigest(),
            'inherited_mirror_radial_comparisons':mirror['radial_gap_comparisons'],
            'critical_certificate':check_critical()}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    if args.self_test:
        self_test()
    print(json.dumps(check(),indent=2,sort_keys=True))
