"""Numeric whole-original-cube replay of additional tight free-pivot cuts.

Checks only supplied sufficient cuts; retained cases are not feasibility claims.
Original full eleven-bit images are from independently reconstructed 2048 cubes.
"""
from collections import Counter
import hashlib
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


def gate(x, a, b):
    if x >> a & 1 and not (x >> b & 1):
        x ^= (1 << a) | (1 << b)
    return x


def operations_allow():
    from controls import operations_allow as authorize
    authorize()


def main():
    operations_allow()
    start = time.monotonic()
    deadline = start + 45
    first, last = map(int, sys.argv[1:3])
    need(0 <= first < last <= 25, 'Bounded branch range required')
    record = json.loads((ROOT/'work/two-prior-independent-original-cubes.json').read_text())
    cache = record['scalar_cache']
    need(digest(cache) == record['scalar_cache_sha256'] ==
         '105a51aade5e8409ba8c7487946c2fab80f819518d4e3758d2de503d6e90ae01', 'Original cube cache differs')
    domains = dict(cache['original_LOW_domains'])
    expected_core = {original: core for core, original, correct in cache['full_core_witnesses']}
    branches = []
    totals = Counter()
    for index in range(first, last):
        operations_allow()
        p = json.loads((OUT/f'branch{index:02}.json').read_text())
        checked = json.loads((OUT/f'checked{index:02}.json').read_text())
        need(checked['finite']['producer_function_list_sha256'] == p['full_functions_sha256'],
             'Preparation function cover not checked')
        screen = json.loads((OUT/f'cuts{index:02}.json').read_text())
        rows = screen['classified_preparations']
        need(screen['checked_preparation_functions_sha256'] == p['full_functions_sha256'] and
             digest(rows) == screen['classification_sha256'], 'Classification not bound to checked functions')
        need([r['function_id'] for r in rows] == list(range(len(p['functions']))), 'Classification cover incomplete')
        inherited = {r['full_function_sha256'] for r in p['minimum_lock_proposals']}
        counts = Counter()
        numeric = []
        retained = []
        for r in rows:
            need(time.monotonic() < deadline, 'Incomplete independent cut replay:45s guard')
            fid = r['function_id']
            f = p['functions'][fid]
            status = r['status']
            is_old_lock = digest(f['full_six_variable_columns']) in inherited
            if status == 'INHERITED_INDEPENDENTLY_CHECKED_MINIMUM_LOCK':
                need(is_old_lock, 'Unreported or false inherited lock')
            else:
                need(not is_old_lock, 'Inherited lock silently moved to another class')
                if status == 'NO_CUT_FOUND_RETAINED_WITHOUT_FEASIBILITY_ASSERTION':
                    retained.append(fid)
                else:
                    need(status == 'ADDITIONAL_TIGHT_FREE_PIVOT_CUT_EXCLUDES_STANDARD_SIZE44',
                         'Unrecognized cut status')
                    port = r['pivot_port']
                    lo = r['original_LOW_mask']
                    need(2 <= port <= 11 and lo in domains, 'Invalid free pivot or original LOW mask')
                    image = set(domains[lo])
                    for a, b in p['HIGH_word'] + f['shortest_word']:
                        need(a < b and 2 <= a < b <= 11 and any(
                            (x >> (a-2) & 1) > (x >> (b-2) & 1) for x in image),
                            'Original prefix witness changes D9/R0')
                        image = {gate(x, a-2, b-2) for x in image}
                    pivot = port - 2
                    need(all(all((x >> q & 1) <= (x >> pivot & 1) for q in range(pivot))
                             and all((x >> pivot & 1) <= (x >> q & 1) for q in range(pivot+1, 11))
                             for x in image), 'Whole original LOW free-cut inequality fails')
                    original = r['full_original_boolean_witness']
                    need(original in expected_core and expected_core[original] == r['wrong_original_core_state'],
                         'Original Boolean witness is not the scalar core witness')
                    row = [original >> q & 1 for q in range(13)]
                    for a, b in cache['prefix'] + p['HIGH_word'] + f['shortest_word']:
                        if row[a] > row[b]:
                            row[a], row[b] = row[b], row[a]
                    correct = int(original.bit_count() >= 13-port)
                    need(row[port] != correct, 'Claimed wrong full-input rank is correct')
                    numeric.append([fid, port, lo, original, len(image)])
                    counts[f'pivot_{port}'] += 1
            counts[status] += 1
        need(dict(counts) == screen['census'] and retained == screen['retained_function_ids'],
             'Complete cut census or retained cover differs')
        branch = {'branch_index': index, 'census': dict(counts), 'classification_sha256': digest(rows),
                  'numeric_original_cut_records_sha256': digest(numeric),
                  'retained_functions': len(retained)}
        branches.append(branch)
        totals.update(counts)
    finite = {'branches': branches, 'census': dict(totals),
              'original_scalar_cache_sha256': record['scalar_cache_sha256'],
              'generic_cut_ref': 'bafkreifwrtftchnstruhgs2j5kfrwmriqzrzoum3n5zvultkwnh7wj4n5a'}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'ALL_SUPPLIED_ORIGINAL_D9_R0_FREE_PIVOT_CUTS_AND_COMPLETE_RETAINED_COVER_VERIFIED',
              'finite': finite, 'finite_sha256': digest(finite),
              'seconds': time.monotonic()-start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Sufficient cuts on complete two-prior preparation cover only; no singleton/tail or whole sorting exclusion.',
              'same_author_algorithmic_independence': True, 'external_person_review_claimed': False}
    suffix = '-O' if not __debug__ else ''
    (ROOT/f'work/two-prior-free-cut-independent-{first:02}-{last:02}{suffix}.json').write_text(
        json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'finite'}, sort_keys=True))
    print(json.dumps({'census': dict(totals)}, sort_keys=True))


if __name__ == '__main__':
    main()
