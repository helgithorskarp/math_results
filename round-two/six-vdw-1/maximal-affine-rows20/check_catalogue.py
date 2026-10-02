"""Local extension coverage and actual AP witnesses; no proposer import."""
import argparse
from collections import Counter
import copy
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def facts():
    cube = set()
    for state in range(16):
        f = [(state // 2 ** j) % 2 for j in range(4)]
        mask = 0
        for s in range(10):
            a, b = (62 // 2 ** s) % 2, (124 // 2 ** s) % 2
            color = (72 // 2 ** s) % 2 ^ f[2 * a + b]
            mask += color * 2 ** s
        cube.add(mask)
    direction = {mask ^ 72 for mask in cube}
    require(len(cube) == len(direction) == 16 and 0 in direction and
            all(x ^ y in direction for x in direction for y in direction), 'independent cube/group reconstruction')
    valid = set()
    for mask in range(1024):
        row = [(mask // 2 ** s) % 2 for s in range(10)]
        row += [1 - v for v in row]
        ok = True
        for first in range(20):
            for second in range(20):
                if first == second:
                    continue
                points = [(first + j * (second - first)) % 20 for j in range(7)]
                if len({row[x] for x in points}) == 1:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            valid.add(mask)
    return frozenset(cube), frozenset(direction), frozenset(valid)


def audit(d, context):
    cube, direction, valid = context
    require(d['author'] == 'six-vdw-1' and d['role'] == 'researcher' and
            d['status'] == 'PROPOSED_COMPLETE_LOCAL_AFFINE_EXTENSIONS', 'attribution/status')
    require(d['base_mask'] == 72 and d['cube_rows'] == sorted(cube) and
            d['direction_space'] == sorted(direction), 'cube/direction domain')
    require(d['all_admissible_antiperiodic_rows'] == len(valid), 'complete actual row count')
    require(d['raw_differences_covered'] == 1024 and d['cosets'] == 64 and
            d['proper_extension_candidates'] == 63, 'coverage dimensions')
    require(d['scope'] == 'Every one-bit affine extension of this chosen16-row cube in the10-bit lower-row space; no field/interval existence or exclusion.', 'scope')
    entries = d['entries']
    require(type(entries) is list and len(entries) == 64, 'entry cover size')
    covered, representatives, successes, histogram = set(), [], [], Counter()
    witness_count = positive_rows = 0
    for item in entries:
        delta = item['representative']
        require(type(delta) is int and 0 <= delta < 1024, 'difference domain')
        coset = {delta ^ h for h in direction}
        require(delta == min(coset) and not covered.intersection(coset), 'canonical disjoint coset')
        covered.update(coset); representatives.append(delta)
        shifted = {mask ^ delta for mask in cube}
        count = len(shifted.intersection(valid))
        histogram[count] += 1
        require(type(item['shifted_coset_valid_rows']) is int and item['shifted_coset_valid_rows'] == count,
                'entire actual valid-row count in coset')
        complete = count == 16
        require(type(item['locally_complete']) is bool and item['locally_complete'] == complete, 'local candidate status')
        if complete:
            require(item['first_bad_row_AP'] is None, 'spurious failure in positive coset')
            positive_rows += len(cube | shifted)
            if delta:
                successes.append(delta)
        else:
            bad = item['first_bad_row_AP']
            require(type(bad) is dict, 'missing actual bad-row witness')
            mask, start, step, color = (bad[k] for k in ['mask', 'start', 'step', 'color'])
            require(all(type(v) is int for v in [mask, start, step, color]) and mask in shifted - valid and
                    0 <= start < 20 and 0 < step < 20 and color in [0, 1], 'bad-row witness domain')
            points = [(start + j * step) % 20 for j in range(7)]
            require(bad['points'] == points, 'entire actual AP positions')
            require(all(((mask // 2 ** (s % 10)) % 2 + s // 10) % 2 == color for s in points), 'actual monochromatic AP')
            witness_count += 1
    require(covered == set(range(1024)) and representatives == sorted(set(representatives)), 'complete ordered cover')
    require(d['proper_locally_admissible_extensions'] == successes, 'complete larger family list')
    require({int(k): v for k, v in d['valid_rows_per_coset_histogram'].items()} == dict(histogram), 'full coset histogram')
    return {'author': 'six-vdw-1', 'role': 'researcher',
            'status': 'COMPLETE_LOCAL_AFFINE_EXTENSION_CATALOGUE_CHECK',
            'raw_differences_covered': len(covered), 'cosets': len(entries),
            'proper_extension_candidates': 63, 'admissible_antiperiodic_rows': len(valid),
            'proper_locally_admissible_extensions': successes, 'bad_coset_actual_AP_witnesses': witness_count,
            'positive_rows_checked_in_complete_extensions': positive_rows,
            'valid_rows_per_coset_histogram': dict(sorted(histogram.items())),
            'scope': 'Local extension classification only; no global field/interval consequence asserted.'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('catalogue', type=Path); a = p.parse_args()
    d = json.loads(a.catalogue.read_text()); context = facts(); result = audit(d, context)
    mutations = []
    for key, value in [('raw_differences_covered', 1023), ('cosets', 63),
                       ('all_admissible_antiperiodic_rows', 581),
                       ('scope', 'all affine row spaces excluded')]:
        x = copy.deepcopy(d); x[key] = value; mutations.append(x)
    x = copy.deepcopy(d); x['entries'].pop(); mutations.append(x)
    x = copy.deepcopy(d); x['entries'][1] = x['entries'][0]; mutations.append(x)
    j = next(i for i, item in enumerate(d['entries']) if item['first_bad_row_AP'] is not None)
    x = copy.deepcopy(d); x['entries'][j]['first_bad_row_AP']['color'] ^= 1; mutations.append(x)
    x = copy.deepcopy(d); x['entries'][j]['first_bad_row_AP']['step'] = 0; mutations.append(x)
    x = copy.deepcopy(d); x['entries'][j]['locally_complete'] = True; mutations.append(x)
    for x in mutations:
        try: audit(x, context)
        except (ValueError, KeyError, TypeError): pass
        else: raise ValueError('damaged local extension catalogue accepted')
    result['damaged_catalogue_rejections'] = len(mutations)
    print(json.dumps(result, sort_keys=True), flush=True)
