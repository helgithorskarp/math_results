"""Fresh actual full case partition for the new branch; no external negatives."""
import json
from pathlib import Path

from run_preparations import digest, need, pair

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'


def current_cases(first,last):
    front = json.loads((WORK/f'fronts03-{first:05}-{last:05}.json').read_text())
    witness = json.loads((WORK/f'witness-phase-complete-{first:05}-{last:05}.json').read_text())
    need(digest(witness['finite']) == witness['finite_sha256'] and
         witness['finite']['front_producer_finite_sha256'] == front['finite_sha256'],
         'Fresh whole original case partition binding differs')
    cases = []
    for row in witness['finite']['slices']:
        a,b = row['case_slice']
        name = f'constant03-{first:05}-{last:05}-{a:05}-{b:05}'
        proposed = json.loads((WORK/(name+'.json')).read_text())
        need(digest(proposed['finite']) == proposed['finite_sha256'] == row['producer_finite_sha256'] and
             digest(proposed['cases']) == proposed['finite']['cases_sha256'] and
             proposed['finite']['producer_front_sha256'] == front['finite_sha256'] and
             [r['front_index'] for r in proposed['cases']] == list(range(a,b)),
             'Fresh actual original case interval differs')
        scalar = pair(f'constant-check03-{first:05}-{last:05}-{a:05}-{b:05}')
        need(scalar['finite_sha256'] == row['scalar_finite_sha256'] and
             scalar['finite']['complete_case_certificate_sha256'] == proposed['finite']['cases_sha256'],
             'Actual case originals not independently checked normally/O')
        cases.extend(proposed['cases'])
    need([r['front_index'] for r in cases] == list(range(len(front['survivors']))),
         'Fresh whole actual case cover is incomplete')
    misses = [r['front_index'] for r in cases if not r['constant16_exceeds44']]
    need(misses == witness['finite']['remaining_open_front_indices'], 'Genuine preserved miss cover differs')
    return {'cases':cases,'cases_sha256':digest(cases)},front,witness
