#!/usr/bin/env python3
"""Exact finite hypotheses of THRESHOLD_CLOSED_BAND_PROOF.md (Python3.11+).

The complete q83 parent is replayed before the new affine original-vertex
support checks.  The original all-Q gauge and the continuous geometric and
coset bridges are written in the companion proof.  This is an author checker,
not an independent implementation or formal proof.  No numerical search,
floating predicate, solver, external package, or private input is used.
"""
import argparse
import copy
import hashlib
import itertools
import json
import re
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT_PINS = {
    'global_band83_certificate.py': (33751, '0bb1cbd5c38477d5c6f7c90f357026429ac4c1a9a9a4050123347e9ca9214e8f'),
    'global_band83_inputs.json': (29329, 'd9604a38b9e7901c757c4cae708883aa8578ad004f598d2588049d5afa280491'),
    'global_band83_expected.json': (97277, 'e619a294e94e3c191049db309490b000833982e2cb6645890e69fa220afb6aa5'),
}


def demand(ok, message):
    if not ok:
        raise ValueError(message)


def validate_pins(rows):
    demand(isinstance(rows, list) and len(rows) == 62, 'all62 published input pins')
    names = []
    for row in rows:
        demand(isinstance(row, dict) and set(row) == {'file', 'bytes', 'sha256'}, 'exact pin schema')
        name = row['file']
        demand(isinstance(name, str) and Path(name).name == name and name.endswith(('.py', '.json')),
            'ordinary local mathematical file')
        demand(type(row['bytes']) is int and 0 < row['bytes'] < 1000000 and
            isinstance(row['sha256'], str) and re.fullmatch('[0-9a-f]{64}', row['sha256']), 'well-formed byte pin')
        names.append(name)
    demand(len(set(names)) == 62, 'all62 input pins distinct')
    for name, (size, sha) in PARENT_PINS.items():
        demand(dict(zip(names, rows)).get(name) == dict(file=name, bytes=size, sha256=sha),
            'fixed public q83 parent pin: ' + name)
    for row in rows:
        p = HERE / row['file']
        demand(p.is_file() and not p.is_symlink(), 'regular original input')
        raw = p.read_bytes()
        demand(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
            'published mathematical input mismatch: ' + row['file'])


def validate_scalar(q):
    demand(isinstance(q, list) and len(q) == 2, 'Q(phi) coefficient pair')
    for s in q:
        demand(isinstance(s, str) and len(s) <= 512 and str(F(s)) == s, 'canonical rational coefficient')


def validate_vector(v):
    demand(isinstance(v, list) and len(v) == 3, 'three original spatial coordinates')
    for q in v:
        validate_scalar(q)


def validate_input(data, check_files=True):
    demand(isinstance(data, dict) and set(data) == {'schema', 'receiving_cutoff', 'parent_expected_sha256',
        'files', 'actual_D', 'actual_raw_references', 'LOW', 'HIGH'}, 'exact closed-band input schema')
    demand(data['schema'] == 'rid-q83-closed-band-v1' and data['receiving_cutoff'] == '83/200',
        'fixed original closed receiving band')
    demand(data['parent_expected_sha256'] == PARENT_PINS['global_band83_expected.json'][1],
        'exact parent expected-byte commitment')
    if check_files:
        validate_pins(data['files'])
    demand(isinstance(data['actual_D'], list) and len(data['actual_D']) == 3, 'three spatial matrix rows')
    for row in data['actual_D']:
        validate_vector(row)
    demand(isinstance(data['actual_raw_references'], list) and len(data['actual_raw_references']) == 2,
        'both actual raw reference normalizations')
    for row in data['actual_raw_references']:
        validate_vector(row)
    demand(isinstance(data['LOW'], dict) and set(data['LOW']) == {'edge', 'source'}, 'exact LOW witness schema')
    for v in data['LOW'].values():
        validate_vector(v)
    high = data['HIGH']
    demand(isinstance(high, dict) and set(high) == {'signed_half_box_witnesses', 'inplane_receiving_polygon',
        'shared_support_contacts'}, 'exact HIGH witness schema')
    signed = high['signed_half_box_witnesses']
    demand(isinstance(signed, list) and len(signed) == 2 and [r.get('sign') for r in signed] == [-1, 1],
        'both ordered signed original half-box witnesses')
    for row in signed:
        demand(isinstance(row, dict) and set(row) == {'sign', 'receiving_edge', 'source'} and
            type(row['sign']) is int, 'exact signed witness schema')
        edge = row['receiving_edge']
        demand(isinstance(edge, list) and len(edge) == 2 and edge[0] != edge[1], 'distinct original edge endpoints')
        for v in edge:
            validate_vector(v)
        validate_vector(row['source'])
    polygon = high['inplane_receiving_polygon']
    demand(isinstance(polygon, list) and len(polygon) == 16 and len({json.dumps(v) for v in polygon}) == 16,
        'sixteen distinct ordered original receiving vertices')
    for v in polygon:
        validate_vector(v)
    contacts = high['shared_support_contacts']
    demand(isinstance(contacts, list) and len(contacts) == 2, 'both original shared support contacts')
    for row in contacts:
        demand(isinstance(row, dict) and set(row) == {'facet', 'source'} and
            type(row['facet']) is int and 0 <= row['facet'] < 16, 'exact original support-contact schema')
        validate_vector(row['source'])
    demand(contacts[0]['facet'] != contacts[1]['facet'], 'two different original support facets')


INPUT_BYTES = (HERE / 'threshold_closed_band_inputs.json').read_bytes()
INPUTS = json.loads(INPUT_BYTES)
validate_input(INPUTS)

# The fixed public parent and all its older exact kernels are checked before
# importing mathematical code.  The full parent check is called in check().
from verify import PHI, QPhi as Q, ZERO, act, dot, matmul, vertices, symmetry_group
from cell_certificate import encode, decode
from torque_certificate import cross, subtract
import global_band83_certificate as parent

I = ((Q(1), ZERO, ZERO), (ZERO, Q(1), ZERO), (ZERO, ZERO, Q(1)))
a = (2*PHI-1)/5
D = ((Q(-1), ZERO, ZERO), (ZERO, a, -2*a), (ZERO, -2*a, -a))
L = ((Q(1), ZERO, ZERO), (ZERO, Q(-1), ZERO), (ZERO, ZERO, Q(-1)))
REFS = ((ZERO, (2-PHI)/3, Q(-1)), (ZERO, Q(1), (3*PHI-1)/11))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def matrix_encode(matrix):
    return [encode(row) for row in matrix]


def determinant(matrix):
    return dot(matrix[0], cross(matrix[1], matrix[2]))


def validate_alignment(matrix, group):
    demand(matmul(matrix, tuple(zip(*matrix))) == I and determinant(matrix) == Q(1),
        'actual proper orthogonal source rotation')
    demand(matrix == D and matmul(matrix, matrix) == I and matrix not in group,
        'fixed involutory nonbody cross-class alignment')


def raw_geometry(result, data):
    records = result['both_threshold_original_cases']
    refs = tuple(decode(row['raw_reference']) for row in records)
    demand(refs == REFS == tuple(decode(row) for row in data['actual_raw_references']),
        'actual public raw reference normalization retained')
    boxes = [[decode(row) for row in r['whole_cap_raw_four_corner_box']] for r in records]
    d = F(result['fresh_threshold_all4_same_class_phase']['both_original_normal_chords_upper'])
    z = 1-d*d/2
    alpha, gamma = F(17, 16)*d/z, d/z
    for m, box in zip(refs, boxes):
        tangent = (ZERO, -m[2], m[1])
        exact = [tuple(m[k]+Q(sx*alpha)*(Q(1) if k == 0 else ZERO)+Q(sy*gamma)*tangent[k]
            for k in range(3)) for sx, sy in ((-1, -1), (-1, 1), (1, -1), (1, 1))]
        demand(box == exact and all(dot(u, m) == dot(m, m) for u in box), 'actual full closed raw box')
    alignments = result['all_four_actual_original_proper_threshold_alignments']['all4_ordered_original_proper_pairings']
    demand(len(alignments) == 4 and
        [tuple(decode(row) for row in r['proper_alignment_matrix']) for r in alignments] == [I, D, D, I],
        'all four actual ordered proper class alignments')
    endpoints = [tuple((x+y)/2 for x, y in zip(boxes[1][j], boxes[1][j+2])) for j in (0, 1)]
    demand(all(u[0] == ZERO for u in endpoints) and alpha > 0 and gamma > 0,
        'entire nondegenerate in-plane closed segment')
    return refs, boxes, endpoints, d, alpha, gamma


def low_separation(low, box, V):
    edge, source = decode(low['edge']), decode(low['source'])
    demand(edge == (Q(1), PHI, PHI-1) and source == (2+PHI, ZERO, -1-PHI) and source in V,
        'fixed LOW functional and ORIGINAL source')
    rows = [[dot(cross(edge, u), subtract(act(D, source), v)) for v in V] for u in box]
    demand(all(g > Q(F(1, 4)) for row in rows for g in row), 'uniform original LOW gap strictly above1/4')
    return dict(constant_cross_product_edge=encode(edge), original_source=encode(source),
        actual_D_source=encode(act(D, source)), all4_minimum_original_gaps=[min(row).encode() for row in rows],
        original_affine_comparisons=240, all240_original_gaps_sha256=digest([[g.encode() for g in row] for row in rows]),
        whole_closed_LOW_box_D_containment_impossible_by_written_affinity=True)


def signed_half_boxes(high, box, endpoints, V):
    records = []
    c = (12*PHI-16)/5
    demand(c > ZERO, 'strict fixed original protrusion coefficient')
    for item in high['signed_half_box_witnesses']:
        sign = item['sign']
        v, w = (decode(row) for row in item['receiving_edge'])
        p = decode(item['source'])
        demand(v in V and w in V and p in V, 'all signed witness endpoints and source ORIGINAL')
        edge = subtract(w, v)
        demand(dot(edge, edge) == Q(4), 'actual original edge length2')
        corners = endpoints+[u for u in box if Q(sign)*u[0] > ZERO]
        demand(len(corners) == 4, 'both complete closed signed half-boxes')
        gaps, heights, protrusions = [], [], []
        for u in corners:
            mu = cross(edge, u)
            row = [dot(mu, subtract(v, z)) for z in V]
            h = dot(mu, v)
            gap = dot(mu, subtract(act(D, p), v))
            demand(all(g >= ZERO for g in row) and h > ZERO, 'actual entire half-box receiving support')
            demand(gap == c*Q(sign)*u[0], 'retained exact signed original protrusion identity')
            gaps.append(row); heights.append(h); protrusions.append(gap)
        records.append(dict(sign=sign, original_receiving_edge=[encode(v), encode(w)],
            original_source=encode(p), actual_D_source=encode(act(D, p)),
            original_half_box_support_checks=240, corner_positive_support_values=[h.encode() for h in heights],
            coefficient_per_signed_raw_x=c.encode(), all4_exact_source_protrusions=[g.encode() for g in protrusions],
            original_receiving_support_sha256=digest([[g.encode() for g in row] for row in gaps]),
            entire_open_signed_half_box_excluded_by_written_affinity=True))
    return records


def distinct_segment_vertices(polygon, endpoints):
    records = []
    for i, j in itertools.combinations(range(16), 2):
        delta = subtract(polygon[j], polygon[i])
        if delta[0] != ZERO:
            records.append([i, j, 'constant_x', delta[0].encode()])
        else:
            values = [dot(cross(u, (Q(1), ZERO, ZERO)), delta) for u in endpoints]
            demand(all(value > ZERO for value in values) or all(value < ZERO for value in values),
                'all projected vertices remain distinct on the whole closed segment')
            records.append([i, j, 'same_x_affine_y', [value.encode() for value in values]])
    demand(len(records) == 120, 'all120 original polygon pairs checked')
    return dict(all_original_vertex_pairs=120, constant_x_separations=sum(row[2] == 'constant_x' for row in records),
        same_x_two_endpoint_separations=sum(row[2] == 'same_x_affine_y' for row in records),
        complete_projected_distinctness_sha256=digest(records))


def segment_supports(high, endpoints, V):
    polygon = [decode(row) for row in high['inplane_receiving_polygon']]
    demand(len(polygon) == 16 and len(set(polygon)) == 16 and all(v in V for v in polygon),
        'sixteen distinct ORIGINAL receiving polygon vertices')
    distinct = distinct_segment_vertices(polygon, endpoints)
    edges = [subtract(polygon[(i+1) % 16], v) for i, v in enumerate(polygon)]
    DV = [act(D, v) for v in V]
    records = []
    for i, (v, edge) in enumerate(zip(polygon, edges)):
        values, gap_rows = [], []
        demand(dot(edge, edge) > ZERO, 'nonzero original polygon edge')
        for u in endpoints:
            mu = cross(edge, u)
            receiving = [dot(mu, subtract(v, z)) for z in V]
            source = [dot(mu, subtract(v, z)) for z in DV]
            h, turn = dot(mu, v), dot(u, cross(edge, edges[(i+1) % 16]))
            demand(h > ZERO and turn > ZERO, 'positive support and strict original projected turn')
            demand(all(g >= ZERO for g in receiving), 'ALL60 original receiving points below actual support')
            demand(all(g >= ZERO for g in source), 'ALL60 original D source points below every actual support')
            values.append(dict(positive_support=h.encode(), strict_consecutive_turn=turn.encode(),
                minimum_receiving_gap=min(receiving).encode(), minimum_D_source_gap=min(source).encode()))
            gap_rows.append([*[g.encode() for g in receiving], *[g.encode() for g in source]])
        records.append(dict(facet=i, original_vertex=encode(v), original_edge=encode(edge),
            both_endpoint_supports=values, all240_endpoint_supports_sha256=digest(gap_rows)))
    contacts = []
    for item in high['shared_support_contacts']:
        i, p = item['facet'], decode(item['source'])
        demand(p in V, 'ORIGINAL shared support source')
        gaps = [dot(cross(edges[i], u), subtract(polygon[i], act(D, p))) for u in endpoints]
        demand(gaps == [ZERO, ZERO], 'two exact endpoint shared support contacts')
        contacts.append(dict(facet=i, original_source=encode(p), actual_D_source=encode(act(D, p)),
            both_exact_contact_gaps=[g.encode() for g in gaps]))
    first, second = [item['facet'] for item in high['shared_support_contacts']]
    determinants = [dot(u, cross(edges[first], edges[second])) for u in endpoints]
    demand(all(value > ZERO for value in determinants) or all(value < ZERO for value in determinants),
        'whole segment shared support independence')
    return dict(original_ordered_polygon=[encode(v) for v in polygon], full_projected_distinctness=distinct,
        all16_original_facets=records, all_original_receiving_support_checks=1920,
        all_original_D_source_support_checks=1920, positive_original_support_values=32,
        strict_original_consecutive_turns=32, whole_segment_shared_support_contacts=contacts,
        both_contact_independence_determinants=[value.encode() for value in determinants],
        entire_closed_inplane_D_containment_proved_by_written_affinity=True,
        original_scale1_translation0_forced_by_written_two_support_bridge=True)


def reverse_separation(low, high_box, V):
    edge, p = act(D, decode(low['edge'])), decode(low['source'])
    DV = [act(D, v) for v in V]
    rows = [[dot(cross(edge, u), subtract(p, z)) for z in DV] for u in high_box]
    demand(all(g > Q(F(1, 4)) for row in rows for g in row), 'whole HIGH reverse original gap strictly above1/4')
    c = (-3+9*PHI)/11
    bL, bH = [(ZERO, -m[2], m[1]) for m in REFS]
    demand(c > Q(1) and act(D, REFS[1]) == tuple(c*x for x in REFS[0]) and
        act(D, bH) == tuple(-c*x for x in bL), 'actual normalized high-to-low center and tangent map')
    return dict(constant_reverse_cross_product_edge=encode(edge), original_receiving_witness=encode(p),
        all4_minimum_reverse_original_gaps=[min(row).encode() for row in rows],
        original_reverse_affine_comparisons=240, complete_reverse_gap_sha256=digest([[g.encode() for g in row] for row in rows]),
        actual_HIGH_to_LOW_raw_scale=c.encode(), raw_tangent_direction_reversed=True,
        receiving_shadow_not_subset_of_D_shadow_on_whole_HIGH_box_by_written_affinity=True)


def original_height_signs(refs, boxes, V):
    records = []
    for j, (m, box) in enumerate(zip(refs, boxes)):
        ordinary = [dot(v, u)*dot(v, m) for u in box for v in V]
        transformed = [dot(v, act(D, u))*dot(v, act(D, m)) for u in box for v in V]
        demand(all(value > ZERO for value in ordinary+transformed), 'original receiving and D-normal signs on entire box')
        records.append(dict(case=j, ordinary_original_height_sign_checks=240,
            transformed_original_height_sign_checks=240, both_f_n_and_f_Dn_positive_on_whole_box_by_written_affinity=True,
            all480_strict_original_sign_values_sha256=digest([value.encode() for value in ordinary+transformed])))
    return records


def body_halfturns(G, V):
    records = []
    for g in G:
        if sum((g[i][i] for i in range(3)), ZERO) != Q(-1):
            continue
        demand(matmul(g, g) == I, 'proper trace-minus-one rotation is an actual half-turn')
        axis = next(tuple(g[i][j]+I[i][j] for i in range(3)) for j in range(3)
            if any(g[i][j]+I[i][j] != ZERO for i in range(3)))
        demand(dot(axis, axis) > ZERO and act(g, axis) == axis, 'nonzero original half-turn axis')
        witnesses = [v for v in V if dot(v, axis) == ZERO]
        demand(witnesses, 'each original body half-turn axis has an ORIGINAL zero-height vertex')
        records.append(dict(original_proper_body_matrix=matrix_encode(g), actual_axis=encode(axis),
            original_zero_height_vertex=encode(witnesses[0])))
    demand(len(records) == 15, 'all15 original proper body half-turns')
    return records


def halfturn(u):
    demand(dot(u, u) > ZERO, 'nonzero actual receiving normal')
    return tuple(tuple(2*u[i]*u[j]/dot(u, u)-I[i][j] for j in range(3)) for i in range(3))


def finite_coset_regressions(G):
    normals = [REFS[1], (ZERO, Q(1), REFS[1][2]+Q(F(1, 100))),
        (Q(F(3, 200)), Q(1), REFS[1][2])]
    records = []
    for u in normals:
        J = halfturn(u)
        bases = (I, J, D, matmul(J, D))
        cosets = [{matmul(base, g) for g in G} for base in bases]
        demand(all(len(coset) == 60 for coset in cosets) and len(set.union(*cosets)) == 240,
            'supplementary exact finite LEFT coset construction')
        records.append(dict(raw_receiving_normal=encode(u), left_coset_sizes=[len(coset) for coset in cosets],
            total_distinct_proper_motions=240, sorted_actual_motion_sha256=digest([matrix_encode(g) for g in sorted(set.union(*cosets))])))
    demand(L in G and matmul(L, D) == matmul(D, L) and
        all(act(L, m) == tuple(-q for q in m) for m in REFS), 'actual proper normal-reversal gauge')
    return dict(finite_examples=records, examples_not_used_as_continuous_disjointness_premise=True,
        actual_proper_normal_reversal_body_matrix=matrix_encode(L), normal_reversal_commutes_with_fixed_D=True,
        moving_halfturns_on_LEFT_original_source_body_factors_on_RIGHT=True)


def reject(label, action, rejected):
    try:
        action()
    except (ValueError, ZeroDivisionError):
        rejected.append(label)
        return
    raise ValueError('malformed evidence accepted: ' + label)


def controls(data, result, G, V, boxes, endpoints):
    rejected = []
    def mutation(change):
        item = copy.deepcopy(data)
        change(item)
        return item
    schema = lambda item:validate_input(item, check_files=False)
    reject('missing_published_input', lambda:validate_pins(data['files'][:-1]), rejected)
    reject('duplicate_published_input', lambda:validate_pins(data['files'][:-1]+data['files'][:1]), rejected)
    reject('changed_fixed_parent_hash', lambda:validate_pins(mutation(lambda item:item['files'][-1].__setitem__('sha256', '0'*64))['files']), rejected)
    reject('unsupported_receiving_cutoff', lambda:schema(mutation(lambda item:item.__setitem__('receiving_cutoff', '2/5'))), rejected)
    reject('noncanonical_rational', lambda:schema(mutation(lambda item:item['LOW']['edge'][0].__setitem__(0, '2/2'))), rejected)
    reject('missing_original_spatial_coordinate', lambda:schema(mutation(lambda item:item['LOW']['source'].pop())), rejected)
    improper = ((Q(-1), ZERO, ZERO), (ZERO, Q(1), ZERO), (ZERO, ZERO, Q(1)))
    reject('improper_source_alignment', lambda:validate_alignment(improper, G), rejected)
    reject('body_symmetry_substituted_for_cross_alignment', lambda:validate_alignment(I, G), rejected)
    wrong = mutation(lambda item:item['actual_raw_references'][0].__setitem__(1, ['1', '0']))
    reject('historical_LOW_raw_scaling_substituted', lambda:raw_geometry(result, wrong), rejected)
    reject('changed_LOW_constant_edge', lambda:low_separation(mutation(lambda item:item['LOW']['edge'][0].__setitem__(0, '-1'))['LOW'], boxes[0], V), rejected)
    reject('nonoriginal_LOW_source', lambda:low_separation(mutation(lambda item:item['LOW'].__setitem__('source', encode((ZERO, ZERO, ZERO))))['LOW'], boxes[0], V), rejected)
    reject('missing_signed_half_box', lambda:schema(mutation(lambda item:item['HIGH']['signed_half_box_witnesses'].pop())), rejected)
    reject('duplicate_signed_half_box', lambda:schema(mutation(lambda item:item['HIGH']['signed_half_box_witnesses'].__setitem__(1, copy.deepcopy(item['HIGH']['signed_half_box_witnesses'][0])))), rejected)
    wrong = mutation(lambda item:item['HIGH']['signed_half_box_witnesses'][0]['receiving_edge'].reverse())
    reject('reversed_original_half_box_support', lambda:signed_half_boxes(wrong['HIGH'], boxes[1], endpoints, V), rejected)
    wrong = mutation(lambda item:item['HIGH']['signed_half_box_witnesses'][0].__setitem__('source', encode((ZERO, ZERO, ZERO))))
    reject('nonoriginal_half_box_source', lambda:signed_half_boxes(wrong['HIGH'], boxes[1], endpoints, V), rejected)
    wrong = mutation(lambda item:item['HIGH']['signed_half_box_witnesses'][0].__setitem__('source', item['HIGH']['signed_half_box_witnesses'][1]['source']))
    reject('wrong_signed_original_protruding_source', lambda:signed_half_boxes(wrong['HIGH'], boxes[1], endpoints, V), rejected)
    reject('missing_original_polygon_vertex', lambda:schema(mutation(lambda item:item['HIGH']['inplane_receiving_polygon'].pop())), rejected)
    wrong = mutation(lambda item:item['HIGH']['inplane_receiving_polygon'].__setitem__(1, copy.deepcopy(item['HIGH']['inplane_receiving_polygon'][0])))
    reject('duplicate_original_polygon_vertex', lambda:schema(wrong), rejected)
    wrong = mutation(lambda item:item['HIGH']['inplane_receiving_polygon'].__setitem__(0, encode((ZERO, ZERO, ZERO))))
    reject('nonoriginal_polygon_vertex', lambda:segment_supports(wrong['HIGH'], endpoints, V), rejected)
    wrong = mutation(lambda item:item['HIGH']['inplane_receiving_polygon'].reverse())
    reject('reversed_original_segment_polygon', lambda:segment_supports(wrong['HIGH'], endpoints, V), rejected)
    reject('missing_shared_support_contact', lambda:schema(mutation(lambda item:item['HIGH']['shared_support_contacts'].pop())), rejected)
    wrong = mutation(lambda item:item['HIGH']['shared_support_contacts'].__setitem__(1, copy.deepcopy(item['HIGH']['shared_support_contacts'][0])))
    reject('duplicate_shared_support_facet', lambda:schema(wrong), rejected)
    wrong = mutation(lambda item:item['HIGH']['shared_support_contacts'][0].__setitem__('facet', 16))
    reject('unknown_original_shared_support_facet', lambda:schema(wrong), rejected)
    wrong = mutation(lambda item:item['HIGH']['shared_support_contacts'][0].__setitem__('source', item['LOW']['source']))
    reject('wrong_original_shared_support_source', lambda:segment_supports(wrong['HIGH'], endpoints, V), rejected)
    demand(len(rejected) == 24, 'all24 new malformed-evidence controls reject')
    return rejected


def check():
    result = parent.check()
    raw = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode()
    demand(raw == (HERE / 'global_band83_expected.json').read_bytes() and
        hashlib.sha256(raw).hexdigest() == INPUTS['parent_expected_sha256'], 'EVERY regenerated public parent byte matches')
    parent_rows = parent.INPUTS['files']+[
        dict(file=name, bytes=size, sha256=sha) for name, (size, sha) in PARENT_PINS.items()]
    demand(sorted(INPUTS['files'], key=lambda row:row['file']) == sorted(parent_rows, key=lambda row:row['file']),
        'exact complete old59-plus-parent3 mathematical input baseline')
    V = sorted(vertices())
    G = sorted(symmetry_group(set(V), return_matrices=True))
    matrix = tuple(decode(row) for row in INPUTS['actual_D'])
    validate_alignment(matrix, G)
    refs, boxes, endpoints, d, alpha, gamma = raw_geometry(result, INPUTS)
    low = low_separation(INPUTS['LOW'], boxes[0], V)
    signed = signed_half_boxes(INPUTS['HIGH'], boxes[1], endpoints, V)
    segment = segment_supports(INPUTS['HIGH'], endpoints, V)
    reverse = reverse_separation(INPUTS['LOW'], boxes[1], V)
    heights = original_height_signs(refs, boxes, V)
    halfturns = body_halfturns(G, V)
    regressions = finite_coset_regressions(G)
    rejected = controls(INPUTS, result, G, V, boxes, endpoints)
    return dict(agent='six-rupert-3', role='researcher',
        proof_status='complete_written_unformalized_author_checked_original_closed_q83_band_classification',
        independently_reviewed=False, historical_priority_asserted=False, global_RID_status='OPEN',
        original_receiving_height_cutoff='83/200', cutoff_boundary_included=True,
        every_original_proper_Q_physical_planar_t_and_scale_ge1_included=True,
        closed_containment_forces_original_scale1_translation0=True,
        winning_closed_motions='G union J_n G;120 equality orientations (inherited8330)',
        LOW_closed_motions='G union J_n G;120 equality orientations',
        HIGH_offplane_closed_motions='G union J_n G;120 equality orientations',
        HIGH_inplane_closed_motions='G union J_n G union D G union J_n D G;240 orientations,120 equality and120 unequal touching',
        exceptional_plane='actual canonical HIGH raw u_x=0',
        receiving_body_fold_U='extra LEFT cosets U D G and J_n U D G for physical receiver U n',
        global_strict_receiving_cutoff_and_gap_unchanged=['83/200', '1/28'],
        all62_previously_published_mathematical_inputs_unchanged=True,
        fixed_new_input_manifest_sha256=hashlib.sha256(INPUT_BYTES).hexdigest(),
        complete_parent_replay=dict(expected_bytes=len(raw), expected_sha256=hashlib.sha256(raw).hexdigest(),
            closed_axis_leaves=198, strict_coefficients=9906, original_corner_supports=9480,
            original_contact_displacement_identities=158, complete_antipodal_pool_assignments=6144,
            proper_ordered_threshold_pairings=4, malformed_evidence_controls_rejected=36,
            inherited436_region_spectrum_reenumerated=False, inherited_mixed8270_and8138_rerun=False),
        actual_nonbody_proper_involutory_D=matrix_encode(D), actual_raw_references=[encode(m) for m in refs],
        whole_closed_raw_boxes=[[encode(u) for u in box] for box in boxes],
        whole_closed_HIGH_inplane_segment_endpoints=[encode(u) for u in endpoints],
        inherited_derived_actual_normal_chord_upper=str(d), actual_raw_alpha_gamma=[str(alpha), str(gamma)],
        LOW_whole_box_separation=low, HIGH_both_signed_half_box_separations=signed,
        HIGH_entire_closed_inplane_original_containment=segment, HIGH_whole_box_unequal_shadow=reverse,
        whole_box_original_nonzero_height_hypotheses=heights,
        all15_original_body_halfturn_zero_height_witnesses=halfturns,
        exact_supplementary_coset_and_normal_reversal_regressions=regressions,
        new_original_affine_support_comparisons=4800, new_original_strict_height_sign_checks=960,
        continuous_four_LEFT_coset_disjointness_proved_by_written_group_and_shadow_bridge=True,
        all_Q_zero_local_motion_bridge_inherited_from_replayed_parent=True,
        new_malformed_evidence_controls_rejected=rejected, continuous_proof='THRESHOLD_CLOSED_BAND_PROOF.md')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    result = check()
    raw = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode()
    if args.emit:
        print(raw.decode(), end='')
    else:
        demand(raw == (HERE / 'threshold_closed_band_expected.json').read_bytes(), 'EVERY new expected certificate byte matches')
        print(json.dumps(dict(status='verified_every_expected_byte', bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
            original_closed_height_band='83/200', inherited_parent_leaves=198, inherited_parent_strict_coefficients=9906,
            new_original_support_comparisons=4800, new_strict_original_height_signs=960,
            original_halfturn_witnesses=15, continuous_HIGH_exceptional_plane=True,
            equality_orientations=120, HIGH_inplane_orientations=240,
            parent_malformed_controls_rejected=36, new_malformed_controls_rejected=24, global_RID='OPEN'), sort_keys=True))


if __name__ == '__main__':
    main()
