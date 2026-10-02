"""Private exact kernel inclusion selector using published actual9590.

If A cannot be sorted by b_A standard gates, A subset B and b_B<=b_A
exclude B at budget b_B. Physical nine-core maps are identical (ports2..10).
No inclusion found is unresolved, not feasible. No new nested computations.
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


def operations_allow():
    from controls import operations_allow as authorize
    authorize()


def main():
    operations_allow()
    start = time.monotonic()
    deadline = start + 45
    source = ROOT/'prior'
    old = json.loads((source/'work/partner4-one-prior-singleton-fronts.json').read_text())
    certificate = json.loads((source/'certificate.json').read_text())
    old_records = {'branches': old['branches'], 'survivors': old['survivors'],
                   'rejections': old['rejected_heads_or_tail_prefixes']}
    need(digest(old_records) == old['finite_records_sha256'] == certificate['front_records_sha256'] ==
         '8e18f17dbd27d7b0943a4c98170c039ea8521ad176c40031e80e5f9db96fb366',
         'Prior full front data differs from published checked9590 certificate')
    need(len(old['survivors']) == certificate['verified_nested_fronts'] == 5613,
         'Published prior obstruction set incomplete')
    unique = {}
    for i, r in enumerate(old['survivors']):
        image = tuple(r['nine_core_states'])
        if image not in unique or unique[image][1] < r['remaining_gate_budget']:
            unique[image] = (i, r['remaining_gate_budget'])
    known = sorted((image, index, budget) for image, (index, budget) in unique.items())
    inverted = {}
    for i, (image, old_index, budget) in enumerate(known):
        for x in image:
            inverted[x] = inverted.get(x, 0) | (1 << i)
    ordered_states = sorted(inverted, key=lambda x: (-inverted[x].bit_count(), x))
    eligible = {b: sum(1 << i for i, (image, old_index, budget) in enumerate(known) if budget >= b)
                for b in range(13)}
    classifications = []
    census = Counter()
    branch_counts = []
    for branch in BRANCHES:
        operations_allow()
        intake = json.loads((OUT/f'heavy-fronts{branch:02}.json').read_text())
        checked = json.loads((OUT/f'heavy-checked{branch:02}.json').read_text())
        need(checked['finite']['producer_front_sha256'] == intake['finite_sha256'],
             'Heavy full front cover not independently checked')
        counts = Counter()
        for i, r in enumerate(intake['survivors']):
            need(time.monotonic() < deadline, 'Incomplete inclusion selector:45s guard')
            remaining = r['remaining_gate_budget']
            present = set(r['nine_core_states'])
            possible = eligible[remaining]
            for x in ordered_states:
                if x not in present:
                    possible &= ~inverted[x]
                    if not possible:
                        break
            result = {'branch_index': branch, 'front_index': i, 'prefix_sha256': r['prefix_sha256'],
                      'nine_core_sha256': r['nine_core_sha256'], 'remaining_gate_budget': remaining}
            if possible:
                chosen = (possible & -possible).bit_length()-1
                image, old_index, budget = known[chosen]
                need(set(image) <= present and remaining <= budget, 'Inverted-index inclusion selector failed')
                witness = old['survivors'][old_index]
                result.update({'status': 'PUBLISHED_ONE_PRIOR_KERNEL_INCLUSION_EXCLUDES_STANDARD_SIZE44',
                               'known_one_prior_front_index': old_index,
                               'known_one_prior_prefix_sha256': witness['prefix_sha256'],
                               'known_one_prior_image_sha256': witness['nine_core_sha256'],
                               'known_one_prior_gate_budget': budget})
            else:
                result['status'] = 'NO_PUBLISHED_KERNEL_INCLUSION_FOUND_TARGET_REMAINS_OPEN'
            classifications.append(result)
            counts[result['status']] += 1
        branch_counts.append({'branch_index': branch, 'census': dict(counts)})
        census.update(counts)
    finite = {'branches': branch_counts, 'census': dict(census),
              'prior_full_front_records_sha256': certificate['front_records_sha256'],
              'prior_distinct_images': len(known), 'prior_union_states': len(inverted),
              'classification_sha256': digest(classifications)}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'COMPLETE_PRIVATE_SUFFICIENT_PUBLISHED_KERNEL_INCLUSION_SCREEN_NEEDS_INDEPENDENT_REPLAY',
              **finite, 'classifications': classifications,
              'finite_sha256': digest(finite), 'seconds': time.monotonic()-start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'dependency': {'height': 9590,
                 'artifact_ref': 'bafkreicjuxisc2rj42fjg4lmb7xdldam6lhgju2k4zdb3lc75u463r4n3a',
                 'source_commit': 'f47e57677011488966488f68228562643bed2b3c'},
              'scope': 'Only TEN heavy-chain two-prior routes. No claim that every target is excluded; the FIFTEEN disjoint-pair intakes remain unprocessed.'}
    (ROOT/'work/two-prior-heavy-inherited-obstructions.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'classifications'}, sort_keys=True))


if __name__ == '__main__':
    main()
