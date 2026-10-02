"""Standalone exact checks of the supplemental63 upper116 and positive99 fixture."""
import hashlib
import json
from math import lcm
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent


def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def read(name):
    return json.loads((ROOT / name).read_text())


def native(name, *args):
    run = subprocess.run([str(ROOT / 'build' / name), *map(str, args)],
                         capture_output=True, text=True, timeout=17)
    need(run.returncode == 0, 'native computation failed: ' + run.stderr)
    return json.loads(run.stdout)


def validate_certificate(certificate):
    scope = {'schema': 1, 'target_remainder4': 3, 'omitted_remainder9': 6,
        'original_cofactors': [d for d in range(2, 721) if 720 % d == 0],
        'whole_copy_cofactors': [2, 4], 'selected_cofactors': [8, 3, 6, 12, 5, 10, 20],
        'real_finer_nine_cofactors': [9, 18, 36], 'virtual_original_modulus': 63,
        'fine_binary_cofactor': 16, 'virtual_nine_resources': 1, 'claimed_upper': 116,
        'global_L_min_8_improved': False,
        'equality_histogram': [8, 36, 36, 6, 29, 36, 9, 0, 0, 0, 0],
        'equality_mandatory_points': 116, 'equality_optional_points': 36}
    for key, value in scope.items():
        need(certificate.get(key) == value, 'certificate scope differs: ' + key)
    actual = native('audit')
    need({k: actual[k] for k in certificate['expected_census']} == certificate['expected_census'],
         'different complete literal census differs')
    need(actual['original_phase_checks'] == 16919 and actual['original_progression_points'] == 146160
         and actual['productive_original_phase_checks'] == 4907, 'raw original phase domain differs')
    need(actual['equality_full9_controls'] == 216000 and actual['equality_seven_states'] == 40
         and actual['implied_K_upper'] == 116, 'different four-resource equality audit incomplete')
    return actual


def literal_positive(data):
    tail = [tuple(row) for row in data['tail_classes']]
    top = [tuple(row) for row in data['TOP_classes']]
    extra = tuple(data['supplemental63_class'])
    need(len(tail) == 29 and {m for a, m in tail} == {7*d for d in range(2, 721) if 720 % d == 0},
         'original29 resource inventory')
    need(len(top) == 20 and {m for a, m in top} == {27*d for d in range(1, 561) if 560 % d == 0},
         'original20 TOP inventory')
    need(extra == (9, 63) and data['marked18'] == data['marked126'] == 9, 'positive marked resource scope')
    need(all(type(a) is int and type(m) is int and 0 <= a < m for a, m in tail + top + [extra]),
         'canonical positive phases')
    S = [x for x in range(720) if x % 4 == 3 and x % 9 != 6]
    pieces = [{t for t in range(180) if t % m == a}
              for a, m in data['projected_support_disjoint_classes']]
    need(len(pieces) == 6 and [len(p) for p in pieces] == [60, 20, 12, 4, 2, 1], 'six-piece support sizes')
    need(not any(pieces[i] & pieces[j] for i in range(6) for j in range(i)), 'six-piece support overlaps')
    symbolic_K = sorted(4*t+3 for t in set.union(*pieces))
    need(symbolic_K == data['K'] and len(symbolic_K) == data['support_size'] == 99, 'symbolic positive K differs')
    need(set(symbolic_K) <= set(S), 'positive K outside S')
    small = bytearray(5040)
    for a, m in tail + [extra]:
        for y in range(a, 5040, m):
            small[y] = 1
    maximum = [x for x in S if all(small[y] for y in range(x, 5040, 720))]
    need(maximum == symbolic_K, 'literal supplemental63 support differs')
    rows = tail + top
    need(len(rows) == len({m for a, m in rows}) == 49, '49 original distinct moduli')
    need(lcm(*(m for a, m in rows)) == 15120 and min(m for a, m in rows) == 14, 'tail-only LCM/minimum')
    large, relief = bytearray(15120), bytearray(15120)
    for a, m in rows:
        for y in range(a, 15120, m):
            large[y] = 1
    for a, m in top:
        for y in range(a, 15120, m):
            relief[y] = 1
    large_K = [x for x in S if all(large[y] for y in range(x, 15120, 720))]
    need(large_K == symbolic_K, 'literal49-class21-lift support differs')
    copy_counts = [0] * 7
    for x in S:
        for s in range(7):
            y = next(y for y in range(x, 5040, 720) if y % 7 == s)
            top_complete = all(relief[y+5040*k] for k in range(3))
            need(top_complete == (s == 2 and x % 18 == 9), 'all-three-lift TOP equivalence differs')
            if all(large[y+5040*k] for k in range(3)):
                copy_counts[s] += 1
    need(copy_counts == [160, 160, 99, 144, 101, 120, 104] and sum(large) == 5705,
         'literal support profile differs')
    need(not data['first_stage_found'] and not data['full_cover_found'], 'positive tail-only scope')
    return {'support_size': 99, 'disjoint_piece_sizes': [len(p) for p in pieces],
            'supplemental63_original_resources': 30, 'distinct_TOP_original_resources': 49,
            'seven_copy_lift_points_checked': 1120, 'twenty_one_lift_points_checked': 3360,
            'all3_TOP_lift_points_checked': 3360, 'copy_support_counts': copy_counts,
            '49_class_period_union': 5705, '49_class_LCM': 15120, '49_class_minimum': 14,
            'full_cover_found': False, 'first_stage_found': False}


def main():
    certificate = read('certificate.json')
    producer = native('producer', 117)
    audit = validate_certificate(certificate)
    keys = list(certificate['expected_census'])
    need({k: producer[k] for k in keys} == {k: audit[k] for k in keys}, 'different complete algorithms disagree')
    need(producer['best_histogram'] == certificate['equality_histogram'], 'producer equality shape differs')
    certificate_damages = []
    for label in ['capacity', 'copy_census', 'equality_overlap', 'virtual_resource']:
        damaged = json.loads(json.dumps(certificate))
        if label == 'capacity':
            damaged['expected_census']['other_resource_capacity'] += 1
        elif label == 'copy_census':
            damaged['expected_census']['canonical_cases'] -= 1
        elif label == 'equality_overlap':
            damaged['expected_census']['equality_max_extra_union'] += 1
        else:
            damaged['virtual_original_modulus'] = 126
        try:
            validate_certificate(damaged)
        except RuntimeError as error:
            certificate_damages.append({'damage': label, 'reason': str(error)})
        else:
            raise RuntimeError('damaged upper certificate accepted')
    positive = read('positive.json')
    positive_result = literal_positive(positive)
    positive_damages = []
    for label in ['unsupported_target', 'missing_original_label', 'broken_anchor']:
        damaged = json.loads(json.dumps(positive))
        if label == 'unsupported_target':
            x = next(x for x in range(720) if x % 4 == 3 and x % 9 != 6 and x not in damaged['K'])
            damaged['K'] = sorted(damaged['K'][1:] + [x])
        elif label == 'missing_original_label':
            damaged['tail_classes'] = damaged['tail_classes'][1:]
        else:
            for row in damaged['tail_classes']:
                if row[1] == 14:
                    row[0] = 1
        try:
            literal_positive(damaged)
        except RuntimeError as error:
            positive_damages.append({'damage': label, 'reason': str(error)})
        else:
            raise RuntimeError('damaged positive fixture accepted')
    result = {'agent': 'six-covering-1', 'role': 'researcher',
        'status': 'SUPPLEMENTAL63_TAIL_SUPPORT_99_TO_116_VERIFIED',
        'M_bounds': [99, 116], 'coarse_cases': audit['canonical_cases'],
        'equality_profiles': audit['at_or_above_threshold'],
        'equality_fine9_domains': audit['equality_full9_controls'],
        'ordered_four_resource_controls': audit['ordered_four_resource_controls'],
        'minimum_equality_overlap_loss': audit['equality_min_overlap_loss'],
        'raw_original_phase_checks': audit['original_phase_checks'],
        'raw_original_progression_points': audit['original_progression_points'],
        'positive': positive_result, 'certificate_damages_rejected': certificate_damages,
        'positive_damages_rejected': positive_damages,
        'independent_verdict': False, 'ordinary_bridge_formalized': False,
        'global_L_min_8_improved': False,
        'input_sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                         for name in ['certificate.json', 'positive.json', 'producer.cpp', 'audit.cpp']}}
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
