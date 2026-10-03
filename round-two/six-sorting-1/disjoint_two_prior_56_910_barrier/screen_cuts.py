"""Private sufficient tight free-pivot screening of checked preparation cover.

Generic cut proof credited to six-sorting-2 actual9616, extending9525.
No failure to find a cut establishes feasibility. All generated data private.
"""
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'work'


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def operations_allow():
    from controls import operations_allow as authorize
    authorize()


def main():
    operations_allow()
    start = time.monotonic()
    first, last = map(int, sys.argv[1:3])
    need(0 <= first < last <= 25, 'Bounded branch range required')
    source = ROOT/'prior/work'
    base = json.loads((source/'low26-partner4-construction-pilot.json').read_text())['core_states']
    domains = json.loads((source/'low26-partner4-activity-pilot.json').read_text())['all39_original_domains']
    cache = json.loads((ROOT/'work/two-prior-independent-original-cubes.json').read_text())['scalar_cache']
    witnesses = {core: original for core, original, correct in cache['full_core_witnesses']}
    need(len(base) == 157 and len(domains) == 39 and set(base) == set(witnesses), 'Full original inputs differ')
    target = [sum(int(x.bit_count() >= 10-j) << i for i, x in enumerate(base)) for j in range(10)]
    original_columns = [sum((x >> j & 1) << i for i, x in enumerate(base)) for j in range(10)]
    masks = [(r['original_LOW_mask'], r['core_image_index_mask']) for r in domains]
    for branch in range(first, last):
        began = time.monotonic()
        deadline = began + 45
        proposal = json.loads((OUT/f'branch{branch:02}.json').read_text())
        checked = json.loads((OUT/f'checked{branch:02}.json').read_text())
        need(checked['finite']['producer_function_list_sha256'] == proposal['full_functions_sha256'],
             'Function producer not independently checked')
        columns = list(original_columns)
        for a, b in proposal['HIGH_word']:
            columns[a-2], columns[b-2] = columns[a-2] & columns[b-2], columns[a-2] | columns[b-2]
        dead = proposal['dead_preparation_ports']
        patterns = [sum((columns[p-2] >> i & 1) << j for j, p in enumerate(dead)) for i in range(157)]
        bins = [sum(1 << i for i, x in enumerate(patterns) if x == k) for k in range(64)]
        inherited = {r['full_function_sha256'] for r in proposal['minimum_lock_proposals']}
        rows = []
        census = Counter()
        for fid, f in enumerate(proposal['functions']):
            need(time.monotonic() < deadline, 'Incomplete cut screen: operational45s guard')
            if fid % 1024 == 0:
                operations_allow()
            row = {'function_id': fid}
            if digest(f['full_six_variable_columns']) in inherited:
                row['status'] = 'INHERITED_INDEPENDENTLY_CHECKED_MINIMUM_LOCK'
            else:
                current = list(columns)
                for p, c in zip(dead, f['full_six_variable_columns']):
                    current[p-2] = sum(bins[k] for k in range(64) if c >> k & 1)
                cut = None
                for j in range(10):
                    wrong = current[j] ^ target[j]
                    if not wrong:
                        continue
                    invalid = 0
                    for q in range(j):
                        invalid |= current[q] & ~current[j]
                    for q in range(j+1, 10):
                        invalid |= current[j] & ~current[q]
                    # Physical12 is the held global maximum, so F_p<=F_12
                    # holds on every original LOW cube; checker retains12.
                    lo = next((lo for lo, mask in masks if not invalid & mask), None)
                    if lo is not None:
                        index = (wrong & -wrong).bit_length() - 1
                        cut = {'pivot_port': j+2, 'original_LOW_mask': lo,
                               'full_original_boolean_witness': witnesses[base[index]],
                               'wrong_original_core_state': base[index]}
                        break
                if cut is not None:
                    row.update(cut)
                    row['status'] = 'ADDITIONAL_TIGHT_FREE_PIVOT_CUT_EXCLUDES_STANDARD_SIZE44'
                    census[f'pivot_{cut["pivot_port"]}'] += 1
                else:
                    row['status'] = 'NO_CUT_FOUND_RETAINED_WITHOUT_FEASIBILITY_ASSERTION'
            rows.append(row)
            census[row['status']] += 1
        finite = {'branch_index': branch, 'HIGH_word': proposal['HIGH_word'],
                  'checked_preparation_functions_sha256': proposal['full_functions_sha256'],
                  'classification_sha256': digest(rows), 'census': dict(census)}
        result = {'agent': 'six-sorting-1', 'role': 'researcher',
                  'status': 'COMPLETE_PRIVATE_SUFFICIENT_FREE_CUT_SCREEN_NEEDS_INDEPENDENT_REPLAY',
                  **finite, 'classified_preparations': rows,
                  'retained_function_ids': [r['function_id'] for r in rows if r['status'].startswith('NO_CUT')],
                  'finite_sha256': digest(finite), 'seconds': time.monotonic()-began,
                  'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  'generic_cut_dependency': {'height': 9616,
                     'artifact_ref': 'bafkreifwrtftchnstruhgs2j5kfrwmriqzrzoum3n5zvultkwnh7wj4n5a',
                     'source_commit': '3467d5cb5699e0cf55a74c74dbabacc3dac9262f'},
                  'scope': 'Sufficient whole-original LOW C9/R0 pivot cuts only, before singleton. No new full branch or global sorting exclusion.'}
        (OUT/f'cuts{branch:02}.json').write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps({k: v for k, v in result.items() if k not in
                         ('classified_preparations', 'retained_function_ids')}, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
