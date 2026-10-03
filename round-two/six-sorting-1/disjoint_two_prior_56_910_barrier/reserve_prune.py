"""Sufficient ORIGINAL HIGH reserve obstructions for the freshly checked prep functions.

Check one already verified shortest FULL64-row representative per function.
Any whole-original unmarked identity adds R>=1 to C+reserved D=9 and forces45.
Full-function/threshold replacement preserves every suffix at no greater size;
therefore a negative shortest representative excludes that whole function.
No selected negative is trusted before separate scalar set/word checking.
"""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import time

from controls import operations_allow

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT
PILOT = ROOT
WORK = ROOT/'work'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def main():
    operations_allow()
    started = time.monotonic()
    deadline = started+45
    source = PUBLIC/'prior'
    pin = next(r['sha256'] for r in json.loads((source/'source-manifest.json').read_text())['files']
               if r['path'] == 'profile.py')
    need(hashlib.sha256((source/'profile.py').read_bytes()).hexdigest() == pin, 'Packed source changed')
    spec = importlib.util.spec_from_file_location('original_high_reserve_packed', source/'profile.py')
    profile = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(profile)
    seed = json.loads((WORK/'reserve-seed.json').read_text())
    n = json.loads((WORK/'reserve-seed-checked.json').read_text())
    o = json.loads((WORK/'reserve-seed-checked-O.json').read_text())
    need(n['finite'] == o['finite'] and digest(n['finite']) == n['finite_sha256'] ==
         o['finite_sha256'] and n['finite']['all78_actual_seed_cost_plus_reserve_equal9'],
         'Complete original class reserves not checked in both modes')
    dead = [2, 3, 4, 5, 8, 9]
    checked = {r['original_HIGH_mask']: r for r in n['activity_domains']}
    domains = []
    for high, actual in checked.items():
        original = iter(profile.truth_columns(11))
        values = [profile.HIGH if high >> p & 1 else next(original) for p in range(13)]
        for a, b in seed['literal_prefix']:
            profile.transition(values, a, b)
        need(all(isinstance(values[p], int) for p in dead), 'Marked dead preparation port')
        image = {sum(((values[p] >> row) & 1) << j for j, p in enumerate(dead))
                 for row in range(2048)}
        mask = sum(1 << value for value in image)
        need(mask == actual['dead_projected_image_mask'], 'Packed ORIGINAL activity image differs from scalar')
        domains.append([high, mask])
    p = json.loads((PILOT/'work/branch03.json').read_text())
    cuts = json.loads((PILOT/'work/cuts03.json').read_text())
    phase = json.loads((WORK/'preparation-phase-complete.json').read_text())
    need(digest(phase['finite']) == phase['finite_sha256'] and
         p['full_functions_sha256'] == phase['finite']['preparation_full_function_list_sha256'] and
         len(cuts['retained_function_ids']) == phase['finite']['retained_functions'],
         'Wrong freshly checked preparation inventory')
    rows, census = [], Counter()
    indices = {q: i for i, q in enumerate(dead)}
    for offset, fid in enumerate(cuts['retained_function_ids']):
        if offset % 128 == 0:
            operations_allow()
            need(time.monotonic() < deadline, 'Incomplete45s reserve obstruction selection')
        f = p['functions'][fid]
        current = list(profile.truth_columns(6))
        witness = None
        for index, (a, b) in enumerate(f['shortest_word']):
            ia, ib = indices[a], indices[b]
            active = current[ia] & ~current[ib]
            high = next((original for original, image in domains if not active & image), None)
            if high is not None:
                record = checked[high]['original_record']
                E = next(r['current_class_maximum_E'] for r in seed['reserve_rows']
                         if r['original_HIGH_mask'] == high)
                witness = {'original_HIGH_mask': high, 'original_seed_record': record,
                           'current_HIGH_class_maximum_E': E, 'reserved_marked_touches': 9-E,
                           'first_reported_preparation_identity_index': index,
                           'identity_comparator': [a, b], 'original_activity_image_mask': checked[high]['dead_projected_image_mask'],
                           'certified_total_cost_lower_bound': record[4]+record[5]+1+9-E+35}
                need(witness['certified_total_cost_lower_bound'] == 45, 'Future identity cost not exactly45')
                break
            current[ia], current[ib] = current[ia] & current[ib], current[ia] | current[ib]
        status = 'ORIGINAL_HIGH_RESERVED_IDENTITY_PROPOSAL' if witness else 'NO_RESERVED_IDENTITY_FOUND_PRESERVED_OPEN'
        census[status] += 1
        rows.append({'retained_offset': offset, 'function_id': fid,
                     'preparation_word_sha256': digest(f['shortest_word']),
                     'full_function_sha256': digest(f['full_six_variable_columns']),
                     'status': status, 'witness': witness})
    finite = {'branch_index': 3, 'HIGH_word': [[5, 6], [9, 10]],
              'all_retained_preparation_functions': len(cuts['retained_function_ids']),
              'preparation_function_list_sha256': p['full_functions_sha256'],
              'preparation_cut_classification_sha256': cuts['classification_sha256'],
              'scalar_seed_reserve_finite_sha256': n['finite_sha256'],
              'original_activity_interfaces_sha256': digest(domains),
              'classification_sha256': digest(rows), 'census': dict(census),
              'remaining_retained_offsets': [r['retained_offset'] for r in rows if r['witness'] is None],
              'remaining_function_ids': [r['function_id'] for r in rows if r['witness'] is None],
              'future_original_floor': 35, 'whole_route_exclusion_claimed': False}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'FRESH_COMPLETE_ORIGINAL_RESERVED_ACTIVITY_PROPOSALS_NEED_SCALAR_REPLAY',
              'finite': finite, 'finite_sha256': digest(finite), 'classifications': rows,
              'seconds': time.monotonic()-started,
              'external_person_review_claimed': False,
              'context': '8539 ordinary pruning/event mechanism and peer2655 reserve idea; source9590 full-function replacement.',
              'scope': 'Sufficient whole ORIGINAL HIGH identity obstructions only; every miss stays open.'}
    (WORK/'reserve-preparation-classifications.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'finite_sha256': result['finite_sha256'],
                      'census': finite['census'], 'seconds': result['seconds']}), flush=True)


if __name__ == '__main__':
    main()
