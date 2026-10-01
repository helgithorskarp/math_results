"""Replay every count bound and the complete two-level phase split."""
import hashlib
import json
from math import gcd
from pathlib import Path

from envelope import LABELS, MASKS, FIXED, N, bound, require, strict

HERE = Path(__file__).resolve().parent
PREVIOUS_SHA256 = '99c433aad2c1f5a6d7246fb619efef9b387de021ddeccac8fe4d4bd59d96cbf2'
PREVIOUS_COMMIT = 'c87f46d672552ca570cd7bc0293969a4e3688c17'
PREVIOUS_REF = 'bafkreibhwbabvc6mqjab3riotqp33y52r73wffazskkh7rcpbhwadaz76m'
REPS = [[0, 2], [0, 4], [3, 1], [3, 2], [3, 4], [3, 5]]
PARENTS = [[0, 2, 4], [0, 2, 10], [0, 2, 11], [0, 4, 2], [0, 4, 7], [0, 4, 8]]


def schema(c):
    previous_path = HERE.parent / 'stage720-six-orbit-reduction' / 'certificate.json'
    previous_bytes = previous_path.read_bytes()
    require(hashlib.sha256(previous_bytes).hexdigest() == PREVIOUS_SHA256,
            'imported twelve-shape source pin differs')
    previous = json.loads(previous_bytes)
    require(c['schema'] == 'stage720-consumed12-16-v1' and c['period'] == N and
            c['original_labels'] == list(LABELS) and c['fixed'] == [[8, 5], [9, 6]] and
            c['target_divisors'] == [18, 6] and c['low_count'] == 12,
            'wrong mathematical domain')
    require(c['dependency'] == {'source_commit': PREVIOUS_COMMIT,
                               'graph_reference': PREVIOUS_REF,
                               'certificate_sha256': PREVIOUS_SHA256},
            'wrong credited dependency')
    require(previous['period'] == N and previous['original_labels'] == list(LABELS) and
            c['remaining_targets'] == previous['remaining_shapes'] and
            c['representatives'] == REPS and c['affine_map'] == [17, 48],
            'wrong imported target inventory or affine map')
    require(c['free_after12'] == [m for m in LABELS if m not in (8, 9, 12)] and
            c['free_after12_16'] == [m for m in LABELS if m not in (8, 9, 12, 16)],
            'consumed original resource retained, omitted or repeated')
    require(c['second_parent_prefixes'] == PARENTS, 'wrong child-parent inventory')
    require(len(c['first_rows']) == 72 and [r[:3] for r in c['first_rows']] ==
            [[a, d, b] for a, d in REPS for b in range(12)],
            'incomplete or repeated original twelve phase split')
    require(len(c['second_rows']) == 96 and [r[:4] for r in c['second_rows']] ==
            [[a, d, b, f] for a, d, b in PARENTS for f in range(16)],
            'incomplete or repeated original sixteen phase split')


def compute(c):
    schema(c)
    first, second, combinations = [], [], 0
    for a, d in REPS:
        for b in range(12):
            values, count = bound(a, d, {12: b})
            first.append([a, d, b, *values])
            combinations += count
    parents = [r[:3] for r in first if not strict(r)]
    require(parents == PARENTS, 'actual nonstrict parents differ')
    for a, d, b in parents:
        for f in range(16):
            values, count = bound(a, d, {12: b, 16: f})
            second.append([a, d, b, f, *values])
            combinations += count
    return first, second, combinations


def validate(c, first, second):
    schema(c)
    require(c['first_rows'] == first and c['second_rows'] == second,
            'literal count-envelope table differs')
    require([r[:3] for r in first if not strict(r)] == PARENTS and
            sum(strict(r) for r in first) == 66 and all(strict(r) for r in second),
            'phase split contains an open leaf')


def affine_controls(c):
    u, t = c['affine_map']
    require(gcd(u, N) == 1 and (5 * u + t) % 8 == 5 and (6 * u + t) % 9 == 6,
            'affine map does not preserve normalized classes')
    target_images = set()
    for a, d in REPS:
        image = ((u * a + t) % 18, (u * d + t) % 6)
        original = {x for x in range(N) if x % 18 == a or x % 6 == d}
        actual = {(u * x + t) % N for x in original}
        desired = {x for x in range(N) if x % 18 == image[0] or x % 6 == image[1]}
        require(actual == desired, 'literal target image differs')
        target_images.update(((a, d), image))
    require(target_images == {tuple(x) for x in c['remaining_targets']},
            'six representatives do not span twelve imported targets')
    family_checks = 0
    for m in LABELS:
        for a in range(m):
            image = sum(1 << ((u * x + t) % N) for x in range(a, N, m))
            require(image == MASKS[m][(u * a + t) % m], 'original phase-family image')
            family_checks += 1
    normalize_checks = 0
    for a in range(8):
        for b in range(9):
            shifts = [s for s in range(72) if (a + s) % 8 == 5 and (b + s) % 9 == 6]
            require(len(shifts) == 1, 'coprime-anchor translation not unique')
            s = shifts[0]
            before = {x for x in range(N) if x % 8 == a or x % 9 == b}
            after = sum(1 << ((x + s) % N) for x in before)
            require(after == FIXED, 'literal normalized fixed-set image')
            normalize_checks += 1
    return family_checks, normalize_checks


def summary(first, second, combinations, family_checks, normalize_checks):
    leaves = [r for r in first if strict(r)] + second
    return {'computed_prefixes': len(first) + len(second),
            'first_cases': len(first), 'first_strict': sum(strict(r) for r in first),
            'second_cases': len(second), 'second_strict': sum(strict(r) for r in second),
            'strict_leaves': len(leaves),
            'minimum_integer_gap': min(r[-2] - r[-1] for r in leaves if r[-1] is not None),
            'unreachable_count_thresholds': sum(r[-1] is None for r in first + second),
            'complete_original_pair_phase_combinations': combinations,
            'affine_original_phase_checks': family_checks,
            'anchor_translation_checks': normalize_checks,
            'remaining_target_shapes': 0, 'global_numerical_bound_changed': False}


def main():
    c = json.loads((HERE / 'certificate.json').read_text())
    first, second, combinations = compute(c)
    validate(c, first, second)
    families, translations = affine_controls(c)
    result = summary(first, second, combinations, families, translations)
    require(result == json.loads((HERE / 'expected.json').read_text()),
            'frozen complete summary differs')
    print(json.dumps({'agent': 'six-covering-1', 'role': 'researcher',
                      'status': 'CHECKED', **result}, sort_keys=True))


if __name__ == '__main__':
    main()
