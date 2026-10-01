#!/usr/bin/env python3
"""Exact finite inputs and rational gates for explicit J74 minimum caps.

Python standard library only. No hull finder, solver or floating point.
The continuum implications are the written argument in PROOF.md.
"""
import copy
from fractions import Fraction
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REQUIRED = {
    'q5.py', 'model.py', 'shadow.py', 'PROOF.md', 'expected.json',
    'RECEIVING_CAPS.md', 'boundary_prototypes/PROOF.md',
    'boundary_prototypes/certificate.json', 'boundary_prototypes/expected.json',
    'tangent_contacts/PROOF.md', 'tangent_contacts/certificate.json',
    'tangent_contacts/expected.json', 'local_mirror_rigidity/PROOF.md',
    'local_mirror_rigidity/DEPENDENCIES.json', 'local_mirror_rigidity/check.py',
    'local_mirror_rigidity/certificate.json', 'local_mirror_rigidity/expected.json'
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load():
    manifest = json.loads((HERE/'DEPENDENCIES.json').read_text())
    require(set(manifest['sha256']) == REQUIRED, 'complete pinned input set')
    parent = (HERE/manifest['directory']).resolve()
    for name, digest in manifest['sha256'].items():
        require(hashlib.sha256((parent/name).read_bytes()).hexdigest() == digest,
                'changed pinned input: '+name)
    sys.path.insert(0, str(parent))
    import q5
    import model
    from local_mirror_rigidity import check as local
    local_result = local.verify()
    require(local_result == json.loads((parent/'local_mirror_rigidity/expected.json').read_text()),
            'complete parent finite hypotheses, not just aggregate counts')
    return parent, manifest, model, q5, local, local_result


def full_axes(q5):
    Q, scale = q5.Q, q5.scale
    phi = Q(1, 1)/2
    return [(Q(1), Q(), Q()), (Q(), Q(1), Q())]+[
        scale(1/(2*phi), (Q(1), e*phi, d*(1+phi)))
        for e, d in ((-1, -1), (-1, 1), (1, -1), (1, 1))]


def moments_and_singletons(parent, model, q5, local):
    Q, dot, cross, sub, scale = q5.Q, q5.dot, q5.cross, q5.sub, q5.scale
    V = model.VERTICES
    axes = full_axes(q5)
    boundary = json.loads((parent/'boundary_prototypes/expected.json').read_text())
    contacts = json.loads((parent/'tangent_contacts/certificate.json').read_text())
    stresses = json.loads((parent/'tangent_contacts/expected.json').read_text())['verified_stresses']
    require(len(contacts['records']) == len(stresses) == len(axes) == 6,
            'all six actual equatorial moment inputs')
    profiles = []
    qsets = []
    for axis, (m, record, stress) in enumerate(zip(axes, contacts['records'], stresses)):
        require(dot(m, m) == 1 and record['axis'] == stress['axis'] == axis,
                'matching physical moment axis')
        qix = [i for i, v in enumerate(V) if dot(m, v) == 0]
        require(len(qix) == 4, 'all and only four original equatorial vertices')
        qsets.append(qix)
        weighted_ix = stress['equatorial_original_indices']
        require(len(weighted_ix) == len(set(weighted_ix)) == 4 and set(weighted_ix) == set(qix),
                'weights attached to exactly the actual equatorial originals')
        require(len(record['equatorial_weights']) == 4, 'one positive weight per original')
        weights = [Q(Fraction(a), Fraction(b)) for a, b in record['equatorial_weights']]
        require(min(weights) > 0 and sum(weights, Q()) == 1,
                'positive normalized actual moment weights')
        require(all(sum((w*V[i][j] for w, i in zip(weights, weighted_ix)), Q()) == 0
                    for j in range(3)), 'actual singleton zero barycenter')
        M = [[sum((w*V[i][j]*V[i][k] for w, i in zip(weights, weighted_ix)), Q())
              for k in range(3)] for j in range(3)]
        D = [[M[j][k]-(Q(j == k)-m[j]*m[k])/2 for k in range(3)] for j in range(3)]
        require(all(D[j][k] == D[k][j] for j in range(3) for k in range(3)) and
                all(sum((D[j][k]*m[k] for k in range(3)), Q()) == 0 for j in range(3)),
                'symmetric physical planar moment excess')
        trace = sum((D[j][j] for j in range(3)), Q())
        det = (trace*trace-sum((D[j][k]*D[k][j] for j in range(3) for k in range(3)), Q()))/2
        require(trace > 0 and det > 0, 'M strictly exceeds one half of the planar identity')
        W = boundary['profiles'][axis]['boundary_original_indices']
        require(set(qix).issubset(W), 'singletons belong to actual boundary prototype')
        height2 = min(dot(m, V[i])*dot(m, V[i]) for i in W if i not in qix)
        separation2 = min(dot(sub(V[a], V[b]), sub(V[a], V[b])) for a, b in combinations(qix, 2))
        require(height2 >= Q(1)/4 and separation2 >= 1, 'radial defect and injection gaps')
        basis = max(combinations(qix, 2),
                    key=lambda pair: dot(cross(V[pair[0]], V[pair[1]]), cross(V[pair[0]], V[pair[1]])))
        area2 = dot(cross(V[basis[0]], V[basis[1]]), cross(V[basis[0]], V[basis[1]]))
        require(area2 > Q(81)/4 and dot(V[basis[0]], V[basis[0]])+dot(V[basis[1]], V[basis[1]]) < 10,
                'well-conditioned physical singleton basis')
        profiles.append({'axis': axis, 'equatorial_original_indices': qix,
                         'basis_original_indices': list(basis), 'basis_Gram_determinant': str(area2),
                         'minimum_nonequatorial_boundary_height_squared': str(height2),
                         'minimum_equatorial_separation_squared': str(separation2),
                         'moment_excess_planar_trace': str(trace),
                         'moment_excess_planar_determinant': str(det)})
    return axes, qsets, profiles


def gram_catalogue(parent, model, q5, local, axes, qsets, profiles):
    Q, add, dot, cross, scale = q5.Q, q5.add, q5.dot, q5.cross, q5.scale
    V = model.VERTICES
    catalogue = json.loads((parent/'expected.json').read_text())['minimum_receiver_proper_motions']
    known = [tuple(tuple(local.scalar(x, Q) for x in col) for col in c['proper_matrix_columns'])
             for c in catalogue]
    require(len(catalogue) == 22 and all(len(cols) == 3 and all(len(col) == 3 for col in cols)
                                        for cols in known), 'complete proper catalogue columns')
    def apply(cols, v):
        return tuple(sum((cols[k][j]*v[k] for k in range(3)), Q()) for j in range(3))
    def proper(cols):
        return (all(dot(cols[i], cols[j]) == (i == j) for i in range(3) for j in range(3))
                and dot(cols[0], cross(cols[1], cols[2])) == 1)
    require(all(proper(cols) for cols in known), 'every pinned catalogue motion is proper')
    checked = 0
    mismatches = []
    isometries = []
    found = []
    counts = [[0]*6 for _ in range(6)]
    for source in range(6):
        m = axes[source]
        qix = qsets[source]
        ia, ib = profiles[source]['basis_original_indices']
        a, b = V[ia], V[ib]
        aa, ab, bb = dot(a, a), dot(a, b), dot(b, b)
        det = aa*bb-ab*ab
        sigma = dot(m, cross(a, b))
        require(det == sigma*sigma and sigma != 0, 'oriented exact source singleton basis')
        for receiver in range(6):
            for perm in permutations(qsets[receiver]):
                checked += 1
                gaps = []
                for i, j in combinations(range(4), 2):
                    gap = dot(V[qix[i]], V[qix[j]])-dot(V[perm[i]], V[perm[j]])
                    gaps.append(gap if gap >= 0 else -gap)
                if any(g > 0 for g in gaps):
                    mismatches.append(max(gaps))
                    continue
                match = dict(zip(qix, perm))
                c, d = V[match[ia]], V[match[ib]]
                def motion(v):
                    alpha = (bb*dot(a, v)-ab*dot(b, v))/det
                    beta = (aa*dot(b, v)-ab*dot(a, v))/det
                    return add(add(scale(alpha, c), scale(beta, d)),
                               scale(dot(m, v)/sigma, cross(c, d)))
                cols = tuple(motion(v) for v in ((Q(1), Q(), Q()), (Q(), Q(1), Q()), (Q(), Q(), Q(1))))
                require(proper(cols) and all(apply(cols, V[i]) == V[j] for i, j in match.items()),
                        'unique exact proper extension of the equatorial isometry')
                hits = [i for i, entry in enumerate(catalogue)
                        if entry['source_axis'] == source and entry['receiver_axis'] == receiver
                        and known[i] == cols]
                require(len(hits) == 1, 'one actual catalogue motion per isometry')
                found += hits
                counts[source][receiver] += 1
                isometries.append({'source_axis': source, 'receiver_axis': receiver,
                                   'target_original_ordering': list(perm), 'catalogue_index': hits[0]})
    require(checked == 6*6*24 == 864 and len(mismatches) == 842 and len(isometries) == 22,
            'complete bounded bijection enumeration')
    require(sorted(found) == list(range(22)), 'entrywise bijection to the entire original catalogue')
    gap = min(mismatches)
    require(gap == Q(0, Fraction(3, 10)) and gap > Q(1)/2,
            'positive exact Gram mismatch margin')
    return {'bijections_examined': checked, 'nonisometric_bijections': len(mismatches),
            'minimum_maximum_Gram_mismatch': str(gap), 'proper_isometric_bijections': len(isometries),
            'isometry_count_matrix': counts, 'isometries': isometries}


def contact_constants(parent, model, q5, local, local_result, parameters):
    Q, add, sub, scale, dot, cross = q5.Q, q5.add, q5.sub, q5.scale, q5.dot, q5.cross
    V = model.VERTICES
    cert = json.loads((parent/'local_mirror_rigidity/certificate.json').read_text())
    radius2 = Q(11, 4)/4
    axes = local.unit_axes(q5)
    cases = []
    recoveries, normals2, inverse_heights, B2s, Kabs, wall2, facet_inverse = [], [], [], [], [], [], []
    for record, profile, m in zip(cert['records'], local_result['profiles'], axes):
        require(record['axis'] == profile['axis'], 'same verified closed contact axis')
        def project(v):
            return sub(v, scale(dot(m, v), m))
        e1 = project((Q(), Q(1), Q()))
        if dot(e1, e1) == 0:
            e1 = project((Q(), Q(), Q(1)))
        e2 = cross(m, e1)
        require(0 < dot(e1, e1) <= 1 and 0 < dot(e2, e2) <= 1 and dot(e1, e2) == 0,
                'physical orthogonal recovery basis with norms at most one')
        def vector(xs):
            return tuple(local.scalar(x, Q) for x in xs)
        rays = [vector(v) for v in record['receiver_wall_rays']]
        wall2 += [dot(m, cross(a, b))*dot(m, cross(a, b)) for a, b in zip(rays, rays[1:]+rays[:1])]
        beta = [Q(Fraction(a), Fraction(b)) for a, b in record['equatorial_weights']]
        for fan, verified in zip(record['fans'], profile['fans']):
            rows = []
            for a, b in fan['original_edges']:
                delta = sub(V[b], V[a])
                height = dot(cross(delta, m), V[a])
                m0 = scale(1/height, cross(delta, m))
                inverse_heights.append(1/height)
                normals2.append(dot(m0, m0))
                for source in (a, b):
                    rows.append({'source': source, 'm0': m0, 'g0': cross(V[source], m0),
                                 'k': dot(delta, m)/height})
            common = []
            for source, weight in zip(record['equatorial_original_indices'], beta):
                pair = [row for row in rows if row['source'] == source]
                require(len(pair) == 2, 'both singleton contact rows retained')
                left, right = [row['m0'] for row in pair]
                difference = sub(left, right)
                theta = dot(sub(scale(1/radius2, V[source]), right), difference)/dot(difference, difference)
                common += [(pair[0], weight*theta), (pair[1], weight*(1-theta))]
            omega = [weight for _, weight in common]
            require(min(omega) > 0 and sum(omega, Q()) == 1, 'positive normalized recovery balance')
            linear = [[dot(row['g0'], m), dot(row['m0'], e1), dot(row['m0'], e2)]
                      for row, _ in common]
            require(all(sum((weight*row[j] for weight, row in zip(omega, linear)), Q()) == 0
                        for j in range(3)), 'exact linear common balance')
            ix = verified['common_rank_indices']
            matrix = [linear[i] for i in ix]
            det = local.determinant(matrix)
            require(det != 0, 'invertible selected physical common system')
            inv = []
            for i in range(3):
                invrow = []
                for j in range(3):
                    minor = [[matrix[r][c] for c in range(3) if c != i] for r in range(3) if r != j]
                    invrow.append(Q((-1)**(i+j))*(minor[0][0]*minor[1][1]-minor[0][1]*minor[1][0])/det)
                inv.append(invrow)
            for first, second in ((matrix, inv), (inv, matrix)):
                require(all(sum((first[i][k]*second[k][j] for k in range(3)), Q()) == (i == j)
                            for i in range(3) for j in range(3)), 'both exact matrix inverse identities')
            coordinate_bounds = []
            for coefficients in inv:
                alpha = [Q()]*8
                for i, coefficient in zip(ix, coefficients):
                    alpha[i] = coefficient
                ratios = [coefficient/weight for coefficient, weight in zip(alpha, omega)]
                total = sum(alpha, Q())
                positive, negative = total-min(ratios), max(ratios)-total
                require(positive >= 0 and negative >= 0, 'nonnegative balanced coordinate representations')
                coordinate_bounds.append(max(positive, negative))
            recovery = sum(coordinate_bounds, Q())
            require(recovery <= parameters['positive_span_recovery_bound'], 'uniform positive-span recovery bound')
            recoveries.append(recovery)
            B = tuple(sum((weight*row['k']*V[row['source']][j] for row, weight in common), Q())
                      for j in range(3))
            Kc = sum((weight*row['k'] for row, weight in common), Q())
            B2s.append(dot(B, B))
            Kabs.append(Kc if Kc >= 0 else -Kc)
            arays = [vector(v) for v in fan['critical_tilt_rays']]
            reciprocals = [1/(-dot(rows[facet]['g0'], arays[k]))
                           for k, facet in enumerate(verified['critical_facet_contact_indices'])]
            require(min(reciprocals) > 0 and max(reciprocals) <= parameters['facet_reciprocal_bound'],
                    'uniform actual critical facet reciprocal bound')
            facet_inverse += reciprocals
            cases.append({'axis': record['axis'], 'fan': verified['fan'],
                          'recovery_coordinate_bounds': [str(x) for x in coordinate_bounds],
                          'positive_span_recovery_bound': str(recovery),
                          'facet_reciprocals': [str(x) for x in reciprocals],
                          'B_squared': str(dot(B, B)), 'Kc_absolute': str(Kabs[-1])})
    require(len(cases) == 46, 'quantitative coverage of every parent closed fan')
    wall_lower = Fraction(parameters['wall_cross_lower_bound'])
    require(max(normals2) <= 1 and max(inverse_heights) <= 2 and max(B2s) <= 1 and max(Kabs) <= 1,
            'physical normal, edge-height and weighted error caps')
    require(min(wall2) > Q(wall_lower*wall_lower), 'uniform physical support-triangle coordinate bound')
    return {'closed_fans': len(cases), 'maximum_support_normal_squared': str(max(normals2)),
            'maximum_inverse_edge_height': str(max(inverse_heights)), 'maximum_B_squared': str(max(B2s)),
            'maximum_Kc_absolute': str(max(Kabs)), 'minimum_wall_cross_squared': str(min(wall2)),
            'maximum_positive_span_recovery': str(max(recoveries)),
            'maximum_facet_reciprocal': str(max(facet_inverse)), 'cases': cases}


def rational_gates(parameters):
    require(parameters['agent'] == 'six-rupert-2' and parameters['role'] == 'researcher', 'actual name and role')
    require(parameters['positive_span_recovery_bound'] == 60 and parameters['facet_reciprocal_bound'] == 80
            and Fraction(parameters['wall_cross_lower_bound']) == Fraction(1, 100),
            'constants match the written estimates')
    d = Fraction(parameters['pose_receiver_radius'])
    k = Fraction(parameters['cayley_threshold'])
    radius = Fraction(parameters['receiver_radius'])
    require(0 < d <= Fraction(1, 1000000) and 0 < k and 0 < radius,
            'positive radius parameters in proved pose domain')
    a, b, h = 1200, 961600, 2402
    cone_lead = (1-(a+b)*k)**2/20-2*b*k*(1+b*k)
    remainder = (2+8*h)*k+(2*h+2*h*h)*k*k
    gates = {
        'global_area_localizer': 15*d <= Fraction(1, 80),
        'source_moment_domain': 5*d <= Fraction(1, 100),
        'quadratic_translation_constant': Fraction(45, 4)/(1-Fraction(1, 10000)) < 12,
        'nonequatorial_projected_height': Fraction(1, 2)-Fraction(9, 4)*d >= Fraction(1, 4),
        'nonequatorial_convex_mass': 16*59*(5*d)**2 < Fraction(1, 2),
        'equatorial_projected_separation_squared': 1-20*d*d >= Fraction(1, 2),
        'physical_vertex_error': 225000*d+Fraction(27, 2) < 20,
        'singleton_injection': 40*d < 1,
        'Gram_gap_domain': 90*d < Fraction(1, 2),
        'proper_motion_Cayley_domain': 40*d <= 1,
        'receiver_tangent_chart': 1/(1-d*d/2) <= 2,
        'prototype_receiver_and_source_domain': 41*d < Fraction(1, 15),
        'companion_denominator': 80*d*d < 1,
        'companion_Cayley_bound': 42+80*d < 43*(1-80*d*d),
        'effective_receiving_radius': radius <= d and 50*radius <= k,
        'local_quadratic_error_domain': k <= Fraction(1, 100),
        'translation_absorption': 120*k <= Fraction(1, 2),
        'rho_bound_for_receiver_relation': a*k*k <= Fraction(1, 4),
        'critical_positive_part_domain': (a+b)*k <= Fraction(1, 100),
        'bilinear_leading_bound': cone_lead >= Fraction(1, 40),
        'bilinear_denominator_lower_bound': 1-k*k >= Fraction(99, 100),
        'weighted_remainder_absorption': remainder < Fraction(1, 100),
        'strict_bilinear_contradiction': Fraction(99, 4000) > remainder,
        'closed_support_triangle_domain': 200*k <= Fraction(1, 100),
        'global_receiving_area_gap_domain': 3*radius <= Fraction(1, 80)
    }
    require(all(gates.values()), 'unsafe quantitative gate: '+', '.join(name for name, ok in gates.items() if not ok))
    return {'a': a, 'b': b, 'h': h, 'cone_bilinear_lower_coefficient_at_threshold': str(cone_lead),
            'weighted_remainder_coefficient_at_threshold': str(remainder), 'gates': gates}


def verify():
    parameters = json.loads((HERE/'parameters.json').read_text())
    require(set(parameters) == {'agent', 'role', 'pose_receiver_radius', 'receiver_radius', 'cayley_threshold',
                                'positive_span_recovery_bound', 'facet_reciprocal_bound', 'wall_cross_lower_bound'},
            'complete literal quantitative parameter schema')
    gates = rational_gates(parameters)
    parent, manifest, model, q5, local, local_result = load()
    axes, qsets, profiles = moments_and_singletons(parent, model, q5, local)
    catalogue = gram_catalogue(parent, model, q5, local, axes, qsets, profiles)
    constants = contact_constants(parent, model, q5, local, local_result, parameters)
    rejected = 0
    damaged = copy.deepcopy(parameters)
    damaged['cayley_threshold'] = '1/100'
    damaged2 = copy.deepcopy(parameters)
    damaged2['receiver_radius'] = '1/1000000'
    for bad in (damaged, damaged2):
        try:
            rational_gates(bad)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('unsafe quantitative parameters accepted')
    return {'agent': 'six-rupert-2', 'role': 'researcher', 'pinned_source_commit': manifest['source_commit'],
            'pinned_inputs': len(REQUIRED),
            'parameters_sha256': hashlib.sha256((HERE/'parameters.json').read_bytes()).hexdigest(),
            'receiver_radius': parameters['receiver_radius'], 'pose_receiver_radius': parameters['pose_receiver_radius'],
            'cayley_threshold': parameters['cayley_threshold'],
            'parent_all_original_support_checks': local_result['total_all_original_support_checks'],
            'parent_bilinear_corner_checks': local_result['total_bilinear_corner_checks'],
            'parent_negative_controls': local_result['negative_geometric_controls'],
            'rejected_unsafe_parameter_controls': rejected,
            'singleton_profiles': profiles, 'Gram_catalogue': catalogue,
            'local_constants': constants, 'rational_gates': gates}


if __name__ == '__main__':
    result = verify()
    if '--emit' in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        require(result == json.loads((HERE/'expected.json').read_text()), 'complete exact quantitative record')
        print(json.dumps({k: v for k, v in result.items()
                          if k not in ('singleton_profiles', 'Gram_catalogue', 'local_constants', 'rational_gates')}, indent=2))
        print('864 bijections;22 catalogue matches;46 closed fans;25 rational gates: verified')
