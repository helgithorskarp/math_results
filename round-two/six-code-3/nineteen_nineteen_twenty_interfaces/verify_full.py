"""Standalone literal check of all regenerated cores, colors and the witness.

Imports only the standard library and the two standalone literal checkers.
Complete negative search coverage still requires running both exact engines;
matching a manifest alone is not an absence certificate.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import time

from check_witness import check as check_witness
from verify_colors import check_record, require, sha


def check(census_work, color_work, expected, residual_expected, witness):
    begun = time.monotonic()
    require(expected['status'] == 'COMPLETE_ALL92_JOINT_CENSUS' and
            expected['orientation_count'] == 92 and expected['core_count'] == 4871 and
            expected['covers'] == 3080796, 'standalone complete census domain')
    pairs = [(r['case'], r['orientation']) for r in expected['cases']]
    require(pairs == [(c, o) for c in range(46) for o in (0, 1)],
            'standalone missing/repeated/reordered orientation')
    stored = json.loads((color_work / 'mathematical-census.json').read_text())
    require(stored == expected, 'standalone residual full-domain binding')
    cores = []
    for row in expected['cases']:
        case, orientation = row['case'], row['orientation']
        got = json.loads((census_work / f'fast-case-{case}-{orientation}.json').read_text())
        require(got['status'] == 'COMPLETE_SELECTED_DUAL_ENGINE_ORIENTATION' and
                got['case'] == case and got['orientation'] == orientation,
                'standalone complete orientation status')
        require(got['core_count'] == len(got['cores']) == row['cores'] and
                sha(got['cores']) == row['core_records_sha256'],
                'standalone complete orientation core inventory')
        for name in ('input_model', 'input_m', 'covers', 'z_eleven', 'carrier_sha256'):
            require(got[name] == row[name], 'standalone orientation manifest field')
        require(sha(got['universes']) == row['universes_sha256'],
                'standalone orientation universe checksum')
        intervals = got['intervals']
        require(intervals and intervals[0]['start'] == 0 and
                intervals[-1]['finish'] == got['covers'] and
                all(a['finish'] == b['start'] for a, b in zip(intervals, intervals[1:])) and
                sum(r['z_eleven'] for r in intervals) == got['z_eleven'] and
                sum(r['y_ten'] for r in intervals) == len(got['cores']),
                'standalone complete interval coverage')
        for core in got['cores']:
            require(core['case'] == case and core['orientation'] == orientation and
                    0 <= core['cover'] < got['covers'], 'standalone core provenance')
        cores.extend(got['cores'])
    hashes = [r['core_sha256'] for r in cores]
    require(len(cores) == 4871 and len(hashes) == len(set(hashes)) and
            sha(cores) == expected['core_records_sha256'] and
            sha(sorted(hashes)) == expected['sorted_core_hashes_sha256'],
            'standalone global core coverage/distinctness')
    require(sum(row['covers'] for row in expected['cases']) == 3080796 and
            sum(row['z_eleven'] for row in expected['cases']) == 39773 and
            sum(row['z_eleven'] for row in expected['cases'] if row['orientation'] == 1) == 18062,
            'standalone full tail/prefix counts')
    domain_hash = sha(expected)
    records, checks = [], []
    for index, core in enumerate(cores):
        record = json.loads((color_work / f'color-{index}.json').read_text())
        checks.append(check_record(core, record, index, domain_hash))
        records.append(record)
    certificate = {'status': 'COMPLETE_ALL_CORE_PROPER_COLOR_RECORDS',
                   'domain_sha256': domain_hash, 'core_count': 4871, 'records': records}
    require(sha(certificate) == residual_expected['certificate_sha256'] and
            domain_hash == residual_expected['domain_sha256'], 'standalone full certificate checksum')
    census = {str(k): v for k, v in sorted(Counter(r['capacity'] for r in checks).items())}
    require(census == residual_expected['capacity_census'] and
            max(r['capacity'] for r in checks) == residual_expected['maximum_capacity'] == 23,
            'standalone full proper-color capacity inventory')
    require(residual_expected['core_count'] == 4871 and residual_expected['orientation_count'] == 92 and
            residual_expected['certified_total_upper_bound'] == 67,
            'standalone residual aggregate declaration')
    witness_result = check_witness(witness)
    require(witness['core_sha256'] in set(hashes), 'standalone witness core in full census')
    matched = cores[hashes.index(witness['core_sha256'])]
    require(set(matched['blocks']) <= set(witness['blocks']), 'standalone witness/core inclusion')
    return {'status': 'PASS_ALL4871_LITERAL_COLORS_AND_LITERAL67',
            'core_count': 4871, 'candidate_range': [min(r['candidates'] for r in checks),
                                                  max(r['candidates'] for r in checks)],
            'capacity_census': census, 'maximum_capacity': 23, 'certified_total_upper_bound': 67,
            'certificate_sha256': sha(certificate), 'per_core_checks_sha256': sha(checks),
            'witness_sha256': sha(witness), 'witness_words': witness_result['words'],
            'witness_core_index': hashes.index(witness['core_sha256']),
            'seconds': time.monotonic() - begun}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--census-work', type=Path, required=True)
    parser.add_argument('--color-work', type=Path, required=True)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--residual-expected', type=Path,
                        default=Path(__file__).with_name('RESIDUAL_SUMMARY.json'))
    parser.add_argument('--witness', type=Path, default=Path(__file__).with_name('witness67.json'))
    args = parser.parse_args()
    result = check(args.census_work, args.color_work, json.loads(args.expected.read_text()),
                   json.loads(args.residual_expected.read_text()), json.loads(args.witness.read_text()))
    print(json.dumps(result, sort_keys=True))
