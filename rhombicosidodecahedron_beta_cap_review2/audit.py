#!/usr/bin/env python3
"""six-reviewer-2: independent exact RID beta-cap review and refinement.

Only pinned earlier reviewer modules are imported. No researcher Python,
researcher witness fixtures, sampled-angle premise or numerical solver.
Continuous reduction and conclusions are stated in REVIEW.md.
"""
import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

PINS = {
    'winning_audit': '1ce270a559c9b86582ff7bae580763490a10468d6cd5367a70927c7f269ac456',
    'winning_expected': 'f1ff37922401ce54d6c5ef965acda3bb81d8f0142e1be014abd527a14db4e791',
    'threshold_audit': 'f12b78980722260e5a6b8d777ec008d1de7e5c8c4ceae6a18a652ec42e541763',
    'threshold_expected': '1103fb6cca5f13c047b275f9e535cc7b65d9a18367c22e9b48aeb96627d4645c',
    'contact_audit': 'b34c68fe16041e379d5d24ac52953fd8af8cfa23b65f8f77cba6c063c1ad4a05',
}

def require(condition, message='independent beta-cap audit failed'):
    if not condition:
        raise ValueError(message)

def pin(path, key):
    require(hashlib.sha256(path.read_bytes()).hexdigest() == PINS[key], key + ' hash differs')

def load(winning, threshold, contact):
    for directory, key in [(winning, 'winning'), (threshold, 'threshold'), (contact, 'contact')]:
        pin(directory / 'audit.py', key + '_audit')
    for directory, key in [(winning, 'winning'), (threshold, 'threshold')]:
        pin(directory / 'expected.json', key + '_expected')
    spec = importlib.util.spec_from_file_location('reviewer2_contact_dependency', contact / 'audit.py')
    c = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c)
    g, k, previous = c.load_geometry(threshold, winning)
    return c, g, k, previous, json.loads((threshold / 'expected.json').read_text())

def arcs(cut, grid=64):
    require(0 < cut < 1 and grid == 64, 'invalid remote-domain policy')
    result = []
    for q in range(4):
        a, z = (cut, F(1)) if q % 2 == 0 else (F(0), (1-cut)/(1+cut))
        result.extend((q, j, a+(z-a)*F(j, grid), a+(z-a)*F(j+1, grid)) for j in range(grid))
    return result

def validate_domain(domain, cut):
    require(domain == arcs(cut), 'closed quarter, endpoint or interval omitted')

def validate_runs(runs, count=128):
    cells = set()
    for q, start, end, witness in runs:
        require(q in range(4) and 0 <= start < end <= 64 and witness in range(count), 'invalid witness run')
        for j in range(start, end):
            require((q, j) not in cells, 'duplicate witness interval')
            cells.add((q, j))
    require(cells == {(q, j) for q in range(4) for j in range(64)}, 'incomplete witness cover')

def formal_identity(l, h):
    # Compare all polynomial coefficients in s, separately for A, D, b+gamma.
    for p0, p1, p2 in [(1, 0, -1), (0, 2, 0), (-1, 0, -1)]:
        b0 = p0+p1*l+p2*l*l
        b1 = p0+p1*(l+h)/2+p2*l*h
        b2 = p0+p1*h+p2*h*h
        require((b0, 2*(b1-b0), b0-2*b1+b2) ==
                (p0+p1*l+p2*l*l, (h-l)*(p1+2*p2*l), p2*(h-l)**2),
                'Bernstein coefficient identity fails')

def circle_terms(g, target):
    n = target['normal']
    e = g.cross(n, (g.ONE, g.ZERO, g.ZERO))
    N = g.sqrt_field(g.dot(n, n))
    points = sorted(target['circle'])
    require(len(points) == 8, 'incomplete actual circle')
    coords = [(g.enclose(p[0]), g.idi(g.enclose(g.dot(p, e)), N)) for p in points]
    terms = []
    for m, p in zip(target['facets'], target['hull']):
        L = g.sqrt_field(g.dot(m, m))
        mx = g.idi(g.enclose(m[0]), L)
        my = g.idi(g.idi(g.enclose(g.dot(m, e)), N), L)
        b = g.idi(g.enclose(g.dot(m, p)), L)
        require(b[0] > 0, 'nonpositive physical support')
        for x, y in coords:
            terms.append((g.ia(g.im(mx, x), g.im(my, y)),
                          g.isu(g.im(my, x), g.im(mx, y)), b))
    require(len(terms) == 128, 'not all actual facet/circle pairs')
    return terms

def rotate(g, terms, q):
    result = []
    for A, D, b in terms:
        for _ in range(q):
            A, D = D, g.ins(A)
        result.append((A, D, b))
    return result

def verify_cover(g, terms, domain, cut, gap, runs):
    validate_domain(domain, cut)
    validate_runs(runs)
    require(len(terms) == 128 and gap > 0, 'invalid support coefficients or gap')
    cc = [rotate(g, terms, q) for q in range(4)]
    for q, start, end, witness in runs:
        for j in range(start, end):
            qq, jj, l, h = domain[q*64+j]
            require((qq, jj) == (q, j), 'wrong interval lookup')
            require(min(g.bernstein_lower(*cc[q][witness], l, h, gap)) > 0,
                    'selected witness does not exclude entire closed arc')

def cover(g, target, cut, gap):
    terms = circle_terms(g, target)
    domain = arcs(cut)
    validate_domain(domain, cut)
    cc = [rotate(g, terms, q) for q in range(4)]
    rows, runs = [], []
    minimum = None
    for q, j, l, h in domain:
        formal_identity(l, h)
        lows = [g.bernstein_lower(*term, l, h, gap) for term in cc[q]]
        value, witness = max((min(vals), i) for i, vals in enumerate(lows))
        require(value > 0, 'no exact remote witness on a closed arc')
        minimum = value if minimum is None else min(minimum, value)
        rows.append([q, j, witness, [str(x) for x in lows[witness]]])
        if runs and runs[-1][0] == q and runs[-1][2] == j and runs[-1][3] == witness:
            runs[-1][2] = j+1
        else:
            runs.append([q, j, j+1, witness])
    verify_cover(g, terms, domain, cut, gap, runs)
    return {
        'rational_cut': str(cut), 'reference_physical_support_gap': str(gap),
        'closed_arcs': 256, 'actual_facet_circle_candidates': 32768,
        'minimum_selected_Bernstein_coefficient_lower': str(minimum),
        'full_generated_record_sha256': hashlib.sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest(),
        'compact_closed_witness_runs': runs, 'all_selected_witnesses_replayed': True,
        'all_polynomial_coefficients_compared_for_formal_identity': True,
    }, (terms, domain, runs)

def bounds(g, beta, delta, cut, gamma, winning_gap, band):
    require(delta > 0 and 0 < cut < 1 and gamma > 0 and winning_gap > 0 and band > 0,
            'nonpositive theorem parameter')
    a = F(15, 4)*delta
    source = F(23, 50)*a + F(9, 4)*a*a
    target = F(9, 2)*delta + F(9, 4)*delta*delta
    lower = F(57, 125) - F(9, 2)*delta
    aw = F(101, 300)*(F(289, 500)-lower)
    winning = F(289, 500)*aw + F(9, 4)*aw*aw
    theta = 2*cut + F(101, 100)*(a+delta)
    checks = {
        'radius_upper': g.sign(g.sub((F(81, 4), 0), (11, 4))) > 0,
        'beta_above_height_cut': g.sign(g.sub(beta, (F(57, 125)**2, 0))) > 0,
        'source_lower_squared_above_other_regions': lower > 0 and lower*lower > F(1, 7),
        'beta_below_circle_axial_height_upper': g.sign(g.sub((F(23, 50)**2, 0), beta)) > 0,
        'sqrt2_upper': F(3, 2)**2 > 2,
        'source_chord_multiplier': F(3, 2)*F(9, 2)/F(9, 5) == F(15, 4),
        'receiving_cap_inside_persistent_support_cap': delta < F(1, 300),
        'all_chords_inside_small_angle_domain': 0 < delta < a < F(1, 10) and 0 < aw < F(1, 10),
        'small_chord_to_angle_derivative_bound': F(101, 100)**2*F(399, 400) > 1,
        'full_relative_near_angle_below_lower_contact_bound': theta < F(1, 16),
        'strict_remote_margin': gamma-source-target > 0,
        'winning_height_upper': F(289, 500)**2 > F(1, 3),
        'winning_sine_below_one_twentieth': 0 < (F(289, 500)-lower)/3 < F(1, 20),
        'winning_cosine_above199over200': F(399, 400) > F(199, 200)**2,
        'winning_chord_sine_multiplier': F(101, 100)**2*F(399, 400) > 1,
        'strict_winning_margin': winning_gap-winning-target > 0,
        'band_above_lower_region_maximum': g.sign(g.sub(g.sub(beta, (band, 0)), (F(1, 7), 0))) > 0,
        'band_root_above9over20': g.sign(g.sub(g.sub(beta, (band, 0)), (F(9, 20)**2, 0))) > 0,
        'band_chord_strictly_inside_cap': F(25, 27)*band < delta,
    }
    for name, result in checks.items():
        require(result, name)
    return {
        'closed_unit_normal_chord_cap': str(delta), 'nonwinning_squared_height_slack': str(band),
        'nonwinning_squared_diameter_slack': str(4*band), 'remote_parameter_cut': str(cut),
        'threshold_source_chord_upper': str(a), 'receiving_axial_height_lower': str(lower),
        'threshold_source_transport_upper': str(source), 'whole_receiver_transport_upper': str(target),
        'full_relative_near_principal_angle_upper': str(theta),
        'remote_reference_gap': str(gamma), 'remote_margin_lower': str(gamma-source-target),
        'winning_reference_gap': str(winning_gap), 'winning_source_chord_upper': str(aw),
        'winning_source_transport_upper': str(winning), 'winning_margin_lower': str(winning_gap-winning-target),
        'nonwinning_band_chord_upper': str(F(25, 27)*band), 'all_exact_scalar_guards': checks,
    }

def controls(g, saved, beta):
    terms, domain, runs = saved
    bad = [
        lambda: validate_domain(domain[:-1], F(1, 64)),
        lambda: validate_domain(list(reversed(domain)), F(1, 64)),
        lambda: validate_domain(domain+[domain[0]], F(1, 64)),
        lambda: arcs(F(0)),
        lambda: validate_runs(runs[:-1]),
        lambda: validate_runs(runs+[runs[0]]),
        lambda: validate_runs([[q, a, b, 128] for q, a, b, w in runs]),
        lambda: verify_cover(g, terms[:-1], domain, F(1, 64), F(1, 100), runs),
        lambda: verify_cover(g, terms, domain, F(1, 64), F(1, 4), runs),
        lambda: g.idi((F(1), F(2)), (F(0), F(1))),
        lambda: g.sqrt_field((-1, 0)),
        lambda: bounds(g, beta, F(1, 625), F(1, 64), F(1, 100), F(51, 1280), F(1, 600)),
        lambda: bounds(g, beta, F(1, 480), F(1, 48), F(1, 75), F(1, 16), F(1, 400)),
        lambda: bounds(g, beta, F(1, 480), F(1, 24), F(1, 75), F(1, 16), F(1, 450)),
    ]
    for f in bad:
        try:
            f()
        except ValueError:
            pass
        else:
            raise ValueError('malformed certificate or theorem parameter accepted')
    return len(bad)

def main():
    root = Path(__file__).resolve().parent.parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--winning-review', type=Path, default=root/'rhombicosidodecahedron_winning_receiver_review2')
    p.add_argument('--threshold-review', type=Path, default=root/'rhombicosidodecahedron_threshold_receiver_review2')
    p.add_argument('--contact-review', type=Path, default=root/'rhombicosidodecahedron_contact_collar_review2')
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    c, g, k, previous, prior_threshold = load(args.winning_review, args.threshold_review, args.contact_review)
    V = [g.vc(v, F(1, 2)) for v in k.original_vertices()]
    require(len(set(V)) == 60 and all(g.dot(v, v) == (11, 4) and g.vc(v, -1) in V for v in V),
            'original edge-two body or central symmetry differs')
    G = g.body_group(V)
    R, C = g.alignments(G)
    refs = ((g.ZERO, g.ONE, g.sc(g.add(g.ONE, g.PH), -3)),
            (g.ZERO, g.ONE, g.div(g.sub(g.sc(g.PH, 3), g.ONE), (11, 0))))
    beta = g.div(g.sub((19, 0), g.sc(g.PH, 8)), (29, 0))
    expected_disk = g.div(g.add((39, 0), g.sc(g.PH, 37)), (29, 0))
    require(g.sign(g.sub(expected_disk, (F(9, 5)**2, 0))) > 0, 'threshold tangent radius too small')
    orbit_data = g.orbit_audit(V, G, refs, beta)
    require(all(g.active_tangents(V, n, beta)[0] == expected_disk for n in refs), 'sharp threshold disks differ')
    global_data = previous['global']
    spectrum = [(tuple(map(F, v)), count) for v, count in global_data['regional_maximum_squared_spectrum_sqrt5_basis']]
    require(sum(count for v, count in spectrum) == 436 and
            sum(count for v, count in spectrum if v == (F(1, 3), F(0))) == 10 and
            sum(count for v, count in spectrum if v == beta) == 60 and
            g.minimum([g.sub((F(1, 7), 0), v) for v, count in spectrum if v not in [(F(1, 3), F(0)), beta]]) == g.ZERO,
            'inherited complete sign-region spectrum differs')
    H = [g.shadow(V, n, 16) for n in refs]
    nearest = lambda n: g.scaled(n, g.div(g.minimum([g.dot(v, n) for v in V if g.sign(g.dot(v, n)) > 0]), g.dot(n, n)))
    require(g.act(R, nearest(refs[0])) == nearest(refs[1]) and
            g.act(R, nearest(refs[1])) == nearest(refs[0]), 'positive directed proper alignment differs')
    alignments = []
    for si in range(2):
        for ti in range(2):
            D = g.identity() if si == ti else R
            source = {v for v in V if g.project(v, refs[si]) in H[si]['circle']}
            target = {v for v in V if g.project(v, refs[ti]) in H[ti]['circle']}
            require(len(source) == len(target) == 8 and {g.act(D, v) for v in source} == target and
                    {g.act(D, v) for v in H[si]['circle']} == H[ti]['circle'], 'actual circle alignment differs')
            alignments.append([si, ti, 8])
    low = (g.ZERO, g.sc(g.sub((2, 0), g.PH), F(1, 3)), (-1, 0))
    contacts = []
    contact_physical_data = {}
    for label, n, D, rho, theta in [('lower-I', low, g.identity(), F(7, 20), F(1, 16)),
                                  ('lower-C', low, C, F(7, 20), F(1, 16)),
                                  ('higher-I', refs[1], g.identity(), F(9, 20), F(1, 12)),
                                  ('higher-C', refs[1], C, F(9, 20), F(1, 12))]:
        record, gap, distance = c.actual_contacts(g, V, n, D)
        gate = c.local_bound(n, gap, distance, rho, F(1, 300), theta)
        physical = {key: value for key, value in record.items() if key not in
                    ['proper_branch_shared_original_vertices', 'generated_original_contacts_and_hull_sha256']}
        family = label.split('-')[0]
        require(contact_physical_data.get(family, physical) == physical, 'shared contacts have different physical support or torque data')
        contact_physical_data[family] = physical
        contacts.append({'branch': label, 'actual_contacts_and_torque_hull': record, 'persistent_local_gate': gate})
    hexagon, _ = k.boundary_geometry([g.vc(v, 2) for v in V])
    require(g.sign(g.sub(g.add((F(8, 3), 0), g.sc(g.PH, 4)), (9, 0))) > 0, 'winning tangent disk does not exceed3')
    B = k.chart()[1]
    source = g.shadow(V, B, 12)
    require(len(source['circle']) == 12, 'winning original corner count differs')
    for corner in source['hull']:
        preimages = [v for v in V if g.project(v, B) == corner]
        require(len(preimages) == 1 and g.sc(g.mul(g.dot(preimages[0], B), g.dot(preimages[0], B)), 3) == g.dot(B, B),
                'actual winning corner axial height differs')
    # Fresh entire-circle proof of the earlier reviewer's stronger raw gap.
    winning_covers = [g.closed_arc_cover(source, h) for h in H]
    require(winning_covers == prior_threshold['closed_arc_winning_source_separation'], 'fresh full-circle reference covers differ')
    original_covers, improved_covers, saved = [], [], []
    for h in H:
        result, control_input = cover(g, h, F(1, 64), F(1, 100))
        original_covers.append(result)
        saved.append(control_input)
        result, _ = cover(g, h, F(1, 48), F(1, 75))
        improved_covers.append(result)
    original = bounds(g, beta, F(1, 640), F(1, 64), F(1, 100), F(51, 1280), F(1, 600))
    improved = bounds(g, beta, F(1, 480), F(1, 48), F(1, 75), F(1, 16), F(1, 450))
    require(F(original['remote_margin_lower']) > F(1, 10000) and F(original['winning_margin_lower']) > F(1, 300), 'original margins differ')
    require(F(improved['remote_margin_lower']) > F(1, 5000) and F(improved['winning_margin_lower']) > F(1, 50), 'refined margins insufficient')
    result = {
        'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer',
        'researcher_modules_or_fixtures_used': False,
        'arithmetic': 'Q(sqrt5) Fraction pairs; independently verified80-bit dyadic positive roots; rational outward intervals',
        'pinned_previous_reviewer_dependencies': PINS,
        'inherited_complete_global_classification_rerun': False, 'complete_inherited_projective_regions': 436,
        'winning_regions': 10, 'threshold_regions': 60, 'remaining_regions': 366, 'remaining_maximum_squared': '1/7',
        'full_proper_body_group_reconstructed': 60, 'full_threshold_orbits_and_disks': orbit_data,
        'all_ordered_original_circle_alignments': alignments, 'fresh_actual_contacts_and_full_torque_hulls': contacts,
        'fresh_complete_winning_tangent_hexagon': hexagon,
        'fresh_entire_winning_reference_circle_covers': winning_covers,
        'confirmed_original_remote_covers': original_covers, 'proved_refined_remote_covers': improved_covers,
        'confirmed_original_transport_and_band': original, 'proved_refined_transport_and_band': improved,
        'positive_dyadic_roots_verified': len(g.ROOTS), 'malformed_controls_rejected': controls(g, saved[0], beta),
        'global_non_rupert_proved': False, 'numerical_global_epsilon_proved': False,
        'winning_receiving_region_below_beta_quantified': False,
        'continuous_bridges': 'Written in REVIEW.md; not proof-assistant formalized.',
    }
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')

if __name__ == '__main__':
    main()
