#!/usr/bin/env python3
"""Exact finite hypotheses for quantitative all-source RID arc-tube control.

PROOF.md supplies the continuum perturbation, proper-branch and angle
arguments. The checker replays the complete arc chain and the published
uniform local certificate, identifies their actual named vertex models,
and checks every new exact margin, scalar bound and branch sanity case.
Python 3.11+, standard library only; no floating-point proof decisions.
"""
from fractions import Fraction as Q
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
DSTAR = Q(1, 10**6)
TUBE = Q(1, 10**38)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pinned(record, expected_names):
    directory = (HERE/record['directory']).resolve()
    require(set(record['sha256']) == set(expected_names), 'dependency file list differs')
    for name, sha in record['sha256'].items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest() == sha,
                'published prerequisite changed: '+name)
    return directory


def local_replay(record):
    names = ['LOCAL_PROOF.md', 'CELL_PROOF.md', 'TORQUE_PROOF.md', 'PROOF.md',
             'local_certificate.py', 'local_expected.json', 'verify.py',
             'cell_certificate.py', 'torque_certificate.py', 'cell_probes.json', 'limit_silhouette.json']
    directory = pinned(record, names)
    # The old kernel lives only in this sequential child. It cannot collide
    # with the arc chain's independently hash-pinned field module.
    program = '''from pathlib import Path
import hashlib,json,sys
p=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(p))
import local_certificate as c
import verify as v
if Path(v.__file__).resolve()!=p/'verify.py':raise ValueError('old arithmetic import differs')
c.self_test()
x=c.check()
actual=(json.dumps(x,indent=2,sort_keys=True)+'\\n').encode()
if actual!=(p/'local_expected.json').read_bytes():raise ValueError('complete local expected record differs')
print(json.dumps({'expected_bytes':len(actual),'expected_sha256':hashlib.sha256(actual).hexdigest(),
 'uniform_angle_radians':str(c.THETA0),'vertex_model':[[q.encode() for q in a] for a in v.vertices()],
 'selected_support_comparisons':x['critical_certificate']['selected_edge_corner_support_comparisons'],
 'radial_comparisons':x['critical_certificate']['radial_support_comparisons'],
 'rational_error_audits':x['critical_certificate']['rational_error_audits'],
 'inherited_cell_record_sha256':x['inherited_cell_output_sha256']}))
'''
    env = dict(os.environ)
    for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS']:
        env[name] = '1'
    cmd = [sys.executable] + (['-O'] if sys.flags.optimize else []) + ['-B', '-c', program, str(directory)]
    child = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=15)
    require(child.returncode == 0, 'uniform local replay failed: '+child.stderr[:1000])
    result = json.loads(child.stdout)
    require(Q(result['uniform_angle_radians']) == Q(1, 10**16), 'uniform local angle differs')
    return result


def arc_replay(record):
    directory = pinned(record, ['check.py', 'expected.json', 'PROOF.md', 'DEPENDENCIES.json'])
    require('field' not in sys.modules, 'unverified arithmetic already imported')
    spec = spec_from_file_location('tube_arc_dependency', directory/'check.py')
    arc = module_from_spec(spec)
    spec.loader.exec_module(arc)
    replay = arc.verify()
    output = json.dumps(replay, indent=2, sort_keys=True)+'\n'
    require(output == (directory/'expected.json').read_text(), 'complete arc expected record differs')
    base_path = directory
    # Arc -> width -> fivefold -> brightness, all hashes checked by that replay.
    for _ in range(3):
        parent = json.loads((base_path/'DEPENDENCIES.json').read_text())
        base_path = (base_path/parent['directory']).resolve()
    require(Path(sys.modules['field'].__file__).resolve() == base_path/'field.py',
            'shared arithmetic is not the replayed brightness source')
    require(hashlib.sha256((base_path/'verify.py').read_bytes()).hexdigest()
            == parent['sha256']['verify.py'], 'brightness source changed after replay')
    spec = spec_from_file_location('tube_brightness_geometry', base_path/'verify.py')
    base = module_from_spec(spec)
    spec.loader.exec_module(base)
    return base, replay


def model_alignment(b, encoded):
    require(len(encoded) == 60, 'local vertex inventory count differs')
    old = {tuple(b.F(*q) for q in v) for v in encoded}
    V = b.vertices()
    require(len(old) == 60 and old == set(V), 'two prerequisite named models differ')
    peak = b.PHI**3
    require(peak > b.ONE and all((b.F(sx), b.F(sy), sz*peak) in V
            for sx, sy, sz in product((-1, 1), repeat=3)),
            'actual box enclosing the unit ball absent')
    return dict(both_prerequisite_vertex_models_identical=True, compared_actual_vertices=60,
                common_model_sha256=b.digest([b.encode(v) for v in V]),
                actual_unit_ball_box_vertices=8, edge_two_body_inradius_lower='1')


def scalar_gates(b, arcs, dstar=DSTAR, tube=TUBE, gamma2_lower=Q(6), completion=Q(3)):
    F, phi, zero = b.F, b.PHI, b.ZERO
    require(0 < dstar < 1 and 0 < tube <= dstar, 'radius outside positive domain')
    require(7+8*phi < F(20) and F(Q(22, 5)**2) < 7+8*phi < F(Q(9, 2)**2)
            and phi**3 < F(Q(9, 2)), 'circumradius or row-support bounds differ')
    width_limit = 4*phi**6*(1-Q(10, 729)*Q(1, 4)**2)
    endpoint_margins = []
    for arc in arcs:
        area2 = F(*arc['physical_endpoint_area_squared'])
        width2 = F(*arc['endpoint_directional_width_squared'])
        require(zero < area2 < F((Q(1171, 20)-Q(1, 1000))**2)
                and 940+1520*phi > F(Q(583, 10)**2), 'arc uniform area margin not above1/1000')
        require(zero < width2 < F(81) and width_limit-width2 > F(Q(1, 1000)),
                'arc uniform squared-width margin not above1/1000')
        endpoint_margins.append(dict(axis=arc['axis'], area_squared_gate_margin=
            (F((Q(1171, 20)-Q(1, 1000))**2)-area2).encode(),
            width_squared_margin=(width_limit-width2).encode()))
    require(31*7 < 250 and 250*dstar < Q(1, 1000), 'perturbed area loses filter budget')
    require(180*dstar+100*dstar*dstar < Q(1, 1000), 'perturbed width loses filter budget')
    require(Q(144, 145) > Q(99, 100)**2 and Q(99, 100)-dstar > Q(24, 25),
            'receiving equatorial determinant loses its positive bound')
    require(Q(45, 116) > Q(3, 5)**2 and (Q(3, 5)-5*dstar)**2 > Q(1, 3) > Q(36, 125),
            'actual-original radial separation is lost')
    require(Q(1473, 5632)+Q(25, 22)*dstar < Q(4, 15), 'full roll no longer lies in row-lock cap')
    require(1-Q(4, 15)**2/2 > Q(9, 10) and Q(9, 2)*Q(4, 15)/Q(19, 10) == Q(12, 19),
            'positive row or support contraction fails')
    require(5/(1-Q(12, 19)) == Q(95, 7) < 14 and Q(11, 10)**2 > Q(20, 19)
            and Q(11, 10)*14 < 16, 'row correction factor16 fails')
    require(Q(3, 25)+16*dstar < Q(1, 7) and Q(1, 8)+16*dstar < Q(1, 4)
            and Q(4, 15)+16*dstar < Q(1, 3), 'row-fixed source loses mirror-plane domain')
    require((2-phi)/4 > F(Q(1, 16)) and 1-Q(1, 7)**2 > Q(24, 25)**2,
            'row-fixed signs or positive normal fail')
    require(phi**4 > F(gamma2_lower) and 2+phi > phi**2 and 680/gamma2_lower < 11**2,
            'squared radial error no longer gives11sqrt(delta)')
    require(14-58*Q(1, 7)/Q(24, 25) > 5 and Q(4250, 5) == 850 and 850**2*dstar < 1,
            'area tilt error not at mostsqrt(delta)')
    require((2*Q(1, 7)/(2*Q(24, 25)))**2+1 < 4,
            'unit normal is not2-Lipschitz in locked tilt')
    require(16+1+22 < 40 and 5*40 == 200, 'full frame, translation or scale coefficient differs')
    require(1+2**2 < completion*completion, 'completed proper frame coefficient fails')
    angle_coefficient = 2*completion*40
    require(angle_coefficient*angle_coefficient*tube < Q(1, 10**16)**2,
            'closed tube does not meet the published full relative-angle bound')
    return dict(closed_fit_receiving_chord_domain=str(dstar), strict_exclusion_closed_tube_chord=str(tube),
                global_area_lipschitz_upper='250', reference_arc_area_margin_lower='1/1000',
                reference_arc_squared_width_margin_lower='1/1000', actual_receiver_nonequatorial_height_lower='3/5-5delta',
                actual_receiver_nonequatorial_squared_height_lower='1/3', preserved_source_chord_upper='1/8',
                preserved_source_transverse_norm_upper='3/25', all_source_frame_before_row_correction_upper='4/15',
                fixed_row_chord_error_upper='16delta', fixed_source_transverse_norm_upper='1/7',
                radial_squared_error_upper='680delta', absolute_source_tilt_error_upper='11sqrt(delta)',
                area_excess_after_row_correction_upper='4250delta', mirror_area_derivative_lower='5',
                frame_error_upper='40sqrt(delta)', edge_two_translation_error_upper='200sqrt(delta)',
                scale_excess_upper='200sqrt(delta)', completed_relative_rotation_operator_error_upper='120sqrt(delta)',
                symmetry_corrected_relative_angle_radians_upper='240sqrt(delta)',
                dependency_uniform_angle_radians='1/10000000000000000', endpoint_uniform_margin_gates=endpoint_margins)


def halfturn_gates(b, diagonal=-1):
    field = sys.modules['field']
    I = tuple(tuple(b.ONE if i == j else b.ZERO for j in range(3)) for i in range(3))
    rays = [(b.ZERO, b.ZERO, b.ONE), (b.ONE, b.ZERO, b.F(12)),
            (b.ZERO, b.ONE, b.F(12)), (b.ONE, b.PHI, 1+3*b.PHI)]
    for r in rays:
        r2 = b.dot(r, r)
        J = tuple(tuple(2*r[i]*r[j]/r2+diagonal*I[i][j] for j in range(3)) for i in range(3))
        require(field.matmul(J, J) == I and field.matmul(tuple(zip(*J)), J) == I
                and field.determinant(J) == b.ONE and b.act(J, r) == r,
                'moving halfturn is not the stated proper involution')
        u = b.cross(r, (b.ONE, b.ZERO, b.ZERO))
        v = b.cross(r, u)
        require(u != (b.ZERO, b.ZERO, b.ZERO) and
                field.matmul((u, v), J) == (b.neg(u), b.neg(v)),
                'moving halfturn does not negate the actual row plane')
    return dict(exact_proper_moving_halfturn_cases=len(rays),
                halfturn_formula='J_n=2*n*n^t-I', negative_branch_transform='Qtilde=J_n*Q*g^-1',
                source_shadow_preserved_by_centrality=True, arbitrary_actual_scale_translation_preserved=True)


def negative_controls(b, arcs, encoded):
    cases = [lambda:scalar_gates(b, arcs, dstar=Q(1, 1000)),
             lambda:scalar_gates(b, arcs, tube=Q(1, 10**32)),
             lambda:scalar_gates(b, arcs, gamma2_lower=Q(1)),
             lambda:scalar_gates(b, arcs, completion=Q(2)),
             lambda:halfturn_gates(b, diagonal=1),
             lambda:model_alignment(b, encoded[:-1])]
    for case in cases:
        try:
            case()
        except ValueError:
            continue
        raise ValueError('damaged new perturbation/branch control accepted')
    return len(cases)


def verify():
    deps = json.loads((HERE/'DEPENDENCIES.json').read_text())
    require(set(deps) == {'arcs', 'uniform_local'}, 'prerequisite records differ')
    old = local_replay(deps['uniform_local'])
    b, arc = arc_replay(deps['arcs'])
    alignment = model_alignment(b, old['vertex_model'])
    V = b.vertices()
    planes, _ = b.complete_facets(V)
    C, _, _ = b.area_generators(V, planes)
    norm2 = max(b.dot(c, c) for c in C)
    require(len(C) == 31 and norm2 < b.F(49), 'global physical area Lipschitz premise differs')
    arcs = arc['receiver_arc_families']
    gates = scalar_gates(b, arcs)
    branches = halfturn_gates(b)
    return dict(agent='six-rupert-3', role='researcher', arithmetic='exact ordered Q(phi) and rational scalars',
                proof_status='written quantitative closed-fit proximity and strict receiving-tube exclusion',
                global_RID_Rupert_status='unresolved', arc_source_commit=deps['arcs']['source_commit'],
                uniform_local_source_commit=deps['uniform_local']['source_commit'],
                prerequisite_replay='four complete arc-chain expected records plus complete uniform-local expected record and its embedded cell hash',
                complete_uniform_local_expected_bytes=old['expected_bytes'],
                complete_uniform_local_expected_sha256=old['expected_sha256'],
                old_local_support_comparisons=old['selected_support_comparisons'],
                old_local_radial_comparisons=old['radial_comparisons'], old_local_error_audits=old['rational_error_audits'],
                inherited_old_cell_expected_sha256=old['inherited_cell_record_sha256'],
                physical_area_generators=31, maximum_squared_area_generator_norm=norm2.encode(),
                initial_motion_scope='arbitrary source frame, proper roll, physical translation and lambda>=1',
                receiving_reference_set='complete proper body orbit of both mirror arcs0<=s<=1/12, including endpoints',
                malformed_controls_rejected=negative_controls(b, arcs, old['vertex_model']),
                **alignment, **gates, **branches)


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
