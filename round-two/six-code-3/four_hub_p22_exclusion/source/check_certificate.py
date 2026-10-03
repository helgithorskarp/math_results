"""Compare all compact certificate entries with the whole independently audited image."""
import hashlib
import json
from pathlib import Path

R = Path('round-two/six-code-3')
S = R / 'scratch'

def need(c, m):
    if not c:
        raise ValueError(m)

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()

def main():
    output = S / 'pass24-certificate-check.json'
    need(not output.exists(), 'fresh compact certificate check')
    path = S / 'CERTIFICATE.json'
    cert = json.loads(path.read_text())
    cap = json.loads((S / 'pass23-T0-capacity-independent.json').read_text())
    row = json.loads((S / 'pass23-T0-row-base-independent.json').read_text())
    need(cap['all_actual_capacity_records_match'] and row['all_entire_records_match'],
         'both whole independent images required')
    need(cap['candidate_cases'] == 969 and cap['excluded'] == 592 and
         row['checked_cases'] == row['excluded_cases'] == 377 and row['surviving_cases'] == 0,
         'every original coupled choice excluded')
    by_id = {r['live_case_ordinal']: r for r in row['records']}
    rebuilt = []
    for i, r in enumerate(cap['records']):
        need(r['live_case_ordinal'] == i, 'all ordered original choices')
        if r['excluded_by_weighted_capacity']:
            why = ['capacity', r['type18_multiplicity'], r['weighted_positive_entry_capacity']]
            need(why[1] > why[2], 'actual excluding integer capacity')
        else:
            q = by_id[i]
            need(all(q[k] == r[k] for k in ['survivor_ordinal', 'carrier_index', 'N4', 'population', 'carrier']),
                 'same actual original choice across independent images')
            fail = q['first_failure']
            if fail['reason'] == 'no_common_admissible_physical_row':
                why = ['empty_row_domain', fail['type_id']]
                need(any(t['type_id'] == fail['type_id'] and t['multiplicity'] > 0 and
                         not t['actual_catalogue_indices'] for t in q['admissible_original_rows']),
                     'actual empty physical row domain')
            else:
                need(fail['reason'] == 'ordinary_same_row_sum_bound', 'known ordinary bound')
                b = q['bounds'][fail['bound_index']]
                need(b['minimum'] > b['target'] or (not b['upper_only'] and b['maximum'] < b['target']),
                     'actual excluding integer row interval')
                why = ['row_sum', b['family'], b['subset_mask'], b['target'], b['minimum'], b['maximum']]
        rebuilt.append([r['survivor_ordinal'], r['carrier_index'], r['N4'], why])
    need(cert['case_count'] == len(rebuilt) == 969 and cert['cases'] == rebuilt,
         'entire compact certificate agrees with original audited mathematical image')
    result = dict(agent='six-code-3', role='researcher', status='ALL969_COMPACT_CERTIFICATE_ENTRIES_CHECKED',
                  cases=969, capacity_excluded=592, shared_row_excluded=377,
                  certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  no_population_or_frequency_caps_added=True, independent_person_review=False)
    output.write_bytes(canonical(result) + b'\n')
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
