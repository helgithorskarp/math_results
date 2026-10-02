"""Private independent selected nested-certificate replay, one branch per stage.

Credited self-contained scalar verifier from actual9420 is imported, never the
packed producer. Complete front coverage is checked separately, not inferred
from selected witnesses. Known S7>=16 may be used directly; larger labels need
all original inner cubes and independent heap/forest anchor bounds. No assertion
is used for a mathematical check, so Python -O must give identical finite data.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--branch', type=int, required=True)
    args = parser.parse_args()
    need(0 <= args.branch < 10, 'Invalid branch')
    start = time.monotonic()
    manifest = json.loads((PUBLIC/'source-manifest.json').read_text())
    pin = next(r['sha256'] for r in manifest['files'] if r['path'] == 'numeric.py')
    need(hashlib.sha256((PUBLIC/'numeric.py').read_bytes()).hexdigest() == pin,
         'Credited scalar primitive source changed')
    spec = importlib.util.spec_from_file_location('one_prior_scalar_nested', PUBLIC/'numeric.py')
    numeric = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(numeric)
    intake = json.loads((ROOT/'work/partner4-one-prior-singleton-fronts.json').read_text())
    cover = json.loads((ROOT/'work/partner4-one-prior-fronts-independent-normal.json').read_text())
    cover_o = json.loads((ROOT/'work/partner4-one-prior-fronts-independent-optimized.json').read_text())
    finite = lambda r: {k:v for k,v in r.items() if k not in ('seconds', 'maximum_rss_kib')}
    need(finite(cover) == finite(cover_o), 'Independent cover differs under -O')
    need(cover['status'] == 'PRIVATE_COMPLETE_5613_FRONT_COVER_INDEPENDENTLY_VERIFIED',
         'Complete front cover was not independently checked')
    need(cover['producer_records_sha256'] == intake['finite_records_sha256'],
         'Complete cover links to a different intake')
    baseline = json.loads((ROOT/f'work/partner4-one-prior-constant-branch{args.branch}.json').read_text())
    full = json.loads((ROOT/f'work/partner4-one-prior-full-branch{args.branch}.json').read_text())
    need(baseline['branch_id'] == full['branch_id'] == args.branch, 'Certificate branch differs')
    need(baseline['intake_records_sha256'] == intake['finite_records_sha256'], 'Baseline intake differs')
    need(digest(baseline['cases']) == baseline['finite_cases_sha256'] and
         digest(full['cases']) == full['finite_cases_sha256'], 'Certificate body hash differs')
    need(not full['uncomputed_front_indices'] and not full['inconclusive_front_indices'],
         'A producer-only incomplete or open case cannot be an exclusion')
    expected = [i for i,r in enumerate(intake['survivors']) if r['branch_id'] == args.branch]
    need([r['front_index'] for r in baseline['cases']] == expected,
         'Constant screen duplicates or omits a complete branch front')
    residual = [r['front_index'] for r in baseline['cases'] if not r['constant16_exceeds44']]
    need(residual == baseline['inconclusive_front_indices'] == [r['front_index'] for r in full['cases']],
         'Inner refinement duplicates or omits a residual front')
    refined = {r['front_index']:r for r in full['cases']}
    replay, masses, counts = [], [], Counter()
    for constant in baseline['cases']:
        need(time.monotonic()-start < 45,
             'Operational45s guard: partial independent replay is not an exclusion')
        index = constant['front_index']
        front = intake['survivors'][index]
        case = constant if constant['constant16_exceeds44'] else refined[index]
        word = front['prefix']
        need(case['front_index'] == index and case['branch_id'] == args.branch and
             all(case[k] == front[k] for k in ('function_id', 'singleton', 'tail_id',
                                               'prefix_sha256', 'remaining_gate_budget', 'nine_core_sha256')),
             'Selected case differs from the independent complete cover')
        need(digest(word) == front['prefix_sha256'] and len(word) == front['front_prefix_length'] and
             44-len(word) == front['remaining_gate_budget'] and
             all(0 <= a < b < 13 for a,b in word), 'Literal standard word/budget differs')
        need(digest(front['nine_core_states']) == front['nine_core_sha256'], 'Complete image hash differs')
        seen, mass = set(), 0
        for witness in case['selected_witnesses']:
            low, high = witness['original_LOW_mask'], witness['original_HIGH_mask']
            need(low.bit_count() == high.bit_count() == 3 and not low&high and low|high < 8192,
                 'Invalid original3+3 domain')
            record = numeric.family(13, word, low, high, 'outer')
            need(record == witness['outer_record'], 'Whole original scalar record differs')
            pruned = numeric.pruning(13, word, record)
            q = tuple(tuple(g) for g in pruned['retained_prefix'])
            need(digest(q) == witness['retained_Q_sha256'], 'Oriented free-carrier word differs')
            B = witness['B7']
            need(isinstance(B, int) and B >= 16, 'Unjustified seven-input lower bound')
            if B == 16:
                inner_hashes, anchor_values = {}, {}
                counts['constant16_selected_occurrences'] += 1
            else:
                bound, data, anchors = numeric.inner_checked(q)
                need(bound == B, 'Independent whole-cube inner anchor bound differs')
                inner_hashes = {k:r['records_sha256'] for k,r in data.items()}
                anchor_values = {k:r['lower_bound'] for k,r in anchors.items()}
                counts['inner_anchor_selected_occurrences'] += 1
            credit = sum(record[4:6])
            need(credit+B == witness['label'], 'Selected nested label differs')
            current = tuple(record[2:4])
            need(current not in seen, 'Selected current outer classes overlap')
            seen.add(current)
            mass += 1 << (credit+B)
            replay.append({'front_index':index, 'record':record, 'Q_sha256':digest(q),
                           'pruning_sha256':digest(pruned), 'B7':B, 'label':credit+B,
                           'inner_record_hashes':inner_hashes, 'inner_anchor_bounds':anchor_values})
        need(mass == case['selected_mass'] and mass > 1 << 44,
             'Strict independent selected nested inequality fails')
        masses.append([index, mass])
        counts['verified_fronts'] += 1
        counts['constant16_closed_fronts' if constant['constant16_exceeds44']
               else 'inner_anchor_closed_fronts'] += 1
    result = {'agent':'six-sorting-1', 'role':'researcher', 'branch_id':args.branch,
              'status':'PRIVATE_COMPLETE_ONE_PRIOR_BRANCH_INDEPENDENTLY_NESTED_EXCLUDED',
              'census':dict(counts), 'selected_occurrences':len(replay),
              'distinct_inner_words':numeric.inner_checked.cache_info().currsize,
              'minimum_selected_mass':min(r[1] for r in masses), 'size44_ceiling':1 << 44,
              'selected_B7_counts':dict(Counter(r['B7'] for r in replay)),
              'replay_sha256':digest(replay), 'root_masses_sha256':digest(masses),
              'complete_cover_records_sha256':intake['finite_records_sha256'],
              'credited_numeric_source_sha256':pin, 'metrics':numeric.METRICS,
              'same_author_algorithmic_independence':True, 'external_person_review_claimed':False,
              'scope':'ExactlyONE priorHIGH equal merge before its first strict singleton after literalB23;L4. Arbitrary suffix, conditional standard-word scope, no global size44 exclusion.',
              'seconds':time.monotonic()-start,
              'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
