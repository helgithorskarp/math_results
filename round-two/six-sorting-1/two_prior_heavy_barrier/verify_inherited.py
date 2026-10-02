"""Independent sets and numeric core replay of inherited9590 obstructions.

Published9590 is an imported negative theorem. Here verify the exact physical
images and budget monotonicity, not rerun its established nested certificate.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'work'
BRANCHES = (0, 6, 11, 15, 16, 19, 21, 22, 23, 24)


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
    source = ROOT/'prior'
    old = json.loads((source/'work/partner4-one-prior-singleton-fronts.json').read_text())
    cert = json.loads((source/'certificate.json').read_text())
    bound = {'branches': old['branches'], 'survivors': old['survivors'],
             'rejections': old['rejected_heads_or_tail_prefixes']}
    need(digest(bound) == cert['front_records_sha256'] ==
         '8e18f17dbd27d7b0943a4c98170c039ea8521ad176c40031e80e5f9db96fb366' and
         len(old['survivors']) == cert['verified_nested_fronts'] == 5613,
         'Old front vectors differ from published9590 certificate')
    cache = json.loads((ROOT/'work/two-prior-independent-original-cubes.json').read_text())['scalar_cache']
    states = [core for core, original, correct in cache['full_core_witnesses']]
    prefix = cache['prefix']
    proposal = json.loads((ROOT/'work/two-prior-heavy-inherited-obstructions.json').read_text())
    rows = proposal['classifications']
    need(digest(rows) == proposal['classification_sha256'], 'Complete inclusion classification digest differs')
    targets = {}
    expected = set()
    for branch in BRANCHES:
        intake = json.loads((OUT/f'heavy-fronts{branch:02}.json').read_text())
        checked = json.loads((OUT/f'heavy-checked{branch:02}.json').read_text())
        need(checked['finite']['producer_front_sha256'] == intake['finite_sha256'], 'New front cover unchecked')
        targets[branch] = intake['survivors']
        expected.update((branch, i) for i in range(len(intake['survivors'])))
    seen = set()
    old_images = {}
    new_images = {}
    counts = Counter()
    per_branch = {}
    relation_records = []
    metrics = Counter()

    def replay(record, store, key):
        if key not in store:
            need(record['prefix'][:26] == prefix and record['remaining_gate_budget'] == 44-len(record['prefix']),
                 'Literal core prefix or remaining budget differs')
            values = list(states)
            for a, b in record['prefix'][26:]:
                need(2 <= a < b <= 11, 'Literal core gate is nonstandard or touches a held port')
                values = [gate(x, a-2, b-2) for x in values]
            need(all((x >> 9 & 1) == int(states[i].bit_count() >= 1) for i, x in enumerate(values)),
                 'Held second-largest control failed')
            image = sorted({x & 511 for x in values})
            need(image == record['nine_core_states'] and digest(image) == record['nine_core_sha256'] and
                 digest(record['prefix']) == record['prefix_sha256'], 'Entire scalar core image or prefix hash differs')
            store[key] = set(image)
            metrics['complete_scalar_core_inputs'] += 157
        return store[key]

    for row in rows:
        need(time.monotonic() < deadline, 'Incomplete independent inheritance check:45s guard')
        key = (row['branch_index'], row['front_index'])
        need(key in expected and key not in seen, 'Classification missing, duplicated or outside cover')
        seen.add(key)
        current = targets[key[0]][key[1]]
        need(row['prefix_sha256'] == current['prefix_sha256'] and
             row['nine_core_sha256'] == current['nine_core_sha256'] and
             row['remaining_gate_budget'] == current['remaining_gate_budget'], 'Classification refers to wrong new target')
        status = row['status']
        if status == 'PUBLISHED_ONE_PRIOR_KERNEL_INCLUSION_EXCLUDES_STANDARD_SIZE44':
            index = row['known_one_prior_front_index']
            need(0 <= index < len(old['survivors']), 'Known obstruction index invalid')
            witness = old['survivors'][index]
            need(row['known_one_prior_prefix_sha256'] == witness['prefix_sha256'] and
                 row['known_one_prior_image_sha256'] == witness['nine_core_sha256'] and
                 row['known_one_prior_gate_budget'] == witness['remaining_gate_budget'], 'Old witness metadata differs')
            a = replay(witness, old_images, index)
            b = replay(current, new_images, key)
            need(a <= b, 'Published impossible kernel is not a subset of new target')
            need(current['remaining_gate_budget'] <= witness['remaining_gate_budget'], 'Budget monotonicity is reversed')
            relation_records.append([key[0], key[1], index, len(a), len(b),
                                     current['remaining_gate_budget'], witness['remaining_gate_budget']])
        else:
            need(status == 'NO_PUBLISHED_KERNEL_INCLUSION_FOUND_TARGET_REMAINS_OPEN', 'Unknown status')
        counts[status] += 1
        per_branch.setdefault(key[0], Counter())[status] += 1
    need(seen == expected and dict(counts) == proposal['census'], 'Complete target classification or census differs')
    branches = [{'branch_index': branch, 'census': dict(per_branch[branch])} for branch in BRANCHES]
    need(branches == proposal['branches'], 'Complete branch census differs')
    finite = {'census': dict(counts), 'branches': branches, 'metrics': dict(metrics),
              'whole_classification_sha256': proposal['classification_sha256'],
              'scalar_set_inclusion_records_sha256': digest(relation_records),
              'distinct_old_images_replayed': len(old_images), 'new_images_replayed': len(new_images),
              'dependency': proposal['dependency'], 'old_front_records_sha256': cert['front_records_sha256']}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'COMPLETE_PUBLISHED9590_KERNEL_INCLUSION_AND_BUDGET_OBSTRUCTIONS_INDEPENDENTLY_VERIFIED',
              'finite': finite, 'finite_sha256': digest(finite),
              'seconds': time.monotonic()-start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Supplied sufficient inherited negatives only; retained targets open; no whole two-prior or global sorting exclusion.',
              'same_author_algorithmic_independence': True, 'external_person_review_claimed': False}
    suffix = '-O' if not __debug__ else ''
    (ROOT/f'work/two-prior-heavy-inheritance-independent{suffix}.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'finite'}, sort_keys=True))
    print(json.dumps({'census': dict(counts), 'metrics': dict(metrics),
                      'old_images_replayed': len(old_images)}, sort_keys=True))


if __name__ == '__main__':
    main()
