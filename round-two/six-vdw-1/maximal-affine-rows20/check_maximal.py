"""Independent64-row construction, complete maximality witnesses and decoder."""
import argparse
import copy
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def span(vectors):
    values = {0}
    for v in vectors:
        values |= {x ^ v for x in tuple(values)}
    return values


def audit(d):
    require(d['author'] == 'six-vdw-1' and d['role'] == 'researcher', 'attribution')
    h = span([1023, 62, 124, 60])
    k = span([1023, 62, 124, 60, 153, 277])
    cube, rows = {72 ^ x for x in h}, {72 ^ x for x in k}
    require(len(h) == 16 and len(k) == 64 and h <= k, 'independent basis ranks')
    require(d['direction_space'] == sorted(h) and d['cube_rows'] == sorted(cube), 'base cube')
    require(type(d['entries']) is list and len(d['entries']) == 64, 'complete quotient input')
    covered, admitted = set(), set()
    bad_witnesses = 0
    for item in d['entries']:
        delta = item['representative']
        require(type(delta) is int and 0 <= delta < 1024, 'representative domain')
        coset = {delta ^ x for x in h}
        require(delta == min(coset) and not covered.intersection(coset), 'canonical disjoint quotient')
        covered.update(coset)
        if coset <= k:
            require(item['locally_complete'] is True and item['first_bad_row_AP'] is None,
                    'positive coset record')
            admitted.update(coset)
        else:
            require(not coset.intersection(k) and item['locally_complete'] is False, 'negative coset record')
            bad = item['first_bad_row_AP']
            require(type(bad) is dict, 'negative witness missing')
            mask, start, step, color = (bad[key] for key in ['mask', 'start', 'step', 'color'])
            require(all(type(v) is int for v in [mask, start, step, color]) and
                    mask in {x ^ delta for x in cube} and 0 <= start < 20 and
                    0 < step < 20 and color in [0, 1], 'actual negative witness domain')
            points = [(start + j * step) % 20 for j in range(7)]
            require(bad['points'] == points and
                    all(((mask // 2 ** (s % 10)) % 2 + s // 10) % 2 == color for s in points),
                    'entire actual monochromatic progression')
            bad_witnesses += 1
    require(covered == set(range(1024)) and admitted == k and bad_witnesses == 60,
            'all1024 differences covered, exactly64 admissible directions')
    row_pairs = point_identities = parity_inputs = 0
    for mask in sorted(rows):
        colors = [(mask // 2 ** s) % 2 for s in range(10)]
        colors += [1 - x for x in colors]
        for start in range(20):
            for step in range(1, 20):
                require(len({colors[(start + j * step) % 20] for j in range(7)}) > 1,
                        'bad64-family local progression')
                row_pairs += 1
    equations = [[0, 7, 8, 9], [2, 5, 8, 9], [3, 5, 7, 9], [4, 5, 7, 8]]
    for value in range(1024):
        f = [(value >> s) & 1 for s in range(10)]
        parity = all(sum(f[s] for s in equation) % 2 == 0 for equation in equations)
        require(parity == (value in k), 'all1024 row membership inputs')
        parity_inputs += 1
        if parity:
            alpha, beta, gamma = f[9], f[1] ^ f[9], f[6] ^ f[9]
            eta, epsilon, zeta = f[5] ^ alpha ^ beta ^ gamma, f[7] ^ alpha, f[8] ^ alpha
            original = ((1023 if alpha else 0) ^ (62 if beta else 0) ^
                        (124 if gamma else 0) ^ (60 if eta else 0) ^
                        (153 if epsilon else 0) ^ (277 if zeta else 0))
            require(original == value, 'unique original coefficient decoder')
            for s in range(20):
                actual = (((72 ^ original) // 2 ** (s % 10)) % 2 + s // 10) % 2
                decoded = ((72 // 2 ** (s % 10)) % 2 + s // 10 + f[s % 10]) % 2
                require(actual == decoded, 'all actual original row/color identities')
                point_identities += 1
    return {'author': 'six-vdw-1', 'role': 'researcher',
            'status': 'COMPLETE_UNIQUE_MAXIMAL_AFFINE64_ROW_CHECK',
            'base_mask': 72, 'original_cube_dimension': 4, 'maximal_containing_cube_dimension': 6,
            'row_count': 64, 'basis': [1023, 62, 124, 60, 153, 277],
            'raw_differences_covered': 1024, 'admissible_directions': 64,
            'rejected_directions': 960, 'bad_coset_actual_AP_witnesses': bad_witnesses,
            'actual_local_row_pairs': row_pairs, 'row_membership_truth_inputs': parity_inputs,
            'original_point_identities': point_identities,
            'phase_parity_equations_zero_based': equations,
            'field31_encoding': {'point_variables': 300, 'column_parity_equations': 120,
                                 'four_literal_membership_clauses': 960,
                                 'independent_coefficient_bits_after_global_palette': 179,
                                 'full_field_model_or_witness_computed': False},
            'scope': 'Unique maximal locally admissible affine extension CONTAINING this chosen16-row cube. Other affine families, nonaffine families and the full field/interval problem remain open.'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('catalogue', type=Path); a = p.parse_args()
    d = json.loads(a.catalogue.read_text()); result = audit(d)
    mutations = []
    x = copy.deepcopy(d); x['entries'].pop(); mutations.append(x)
    x = copy.deepcopy(d); x['entries'][1] = x['entries'][0]; mutations.append(x)
    j = next(i for i, item in enumerate(d['entries']) if item['first_bad_row_AP'] is not None)
    x = copy.deepcopy(d); x['entries'][j]['first_bad_row_AP']['color'] ^= 1; mutations.append(x)
    x = copy.deepcopy(d); x['entries'][j]['first_bad_row_AP']['step'] = 0; mutations.append(x)
    x = copy.deepcopy(d); x['entries'][j]['first_bad_row_AP']['mask'] = 72; mutations.append(x)
    x = copy.deepcopy(d); x['entries'][j]['locally_complete'] = True; mutations.append(x)
    x = copy.deepcopy(d); x['direction_space'][0] = 1; mutations.append(x)
    for x in mutations:
        try: audit(x)
        except (ValueError, KeyError, TypeError): pass
        else: raise ValueError('damaged maximality certificate accepted')
    result['damaged_maximality_certificate_rejections'] = len(mutations)
    print(json.dumps(result, sort_keys=True), flush=True)
