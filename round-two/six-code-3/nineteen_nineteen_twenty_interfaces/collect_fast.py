"""Gap-free aggregation of all92 completed source-bound mixed orientations.

A missing/incomplete orientation is an error, never a zero case. Raw cores
remain local; the exported manifest is compact counts and canonical hashes.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

from bindings import PRIOR, v
from fast_run import digest, fingerprint


def load(work, executables, pairs=None):
    full = pairs is None
    if pairs is None:
        pairs = [(case, orientation) for case in range(46) for orientation in (0, 1)]
    v.check(len(pairs) == len(set(pairs)) and all(type(case) is int and 0 <= case < 46
            and type(orientation) is int and orientation in (0, 1) for case, orientation in pairs),
            'aggregation selected domain')
    current = fingerprint(executables)
    prior_path = PRIOR / 'expected.json'
    v.check(digest(prior_path) == '952b768db8778961eaa16e14d8b684d642058bb62b8837c445ae4521893f5d58',
            'published complete prior tail/prefix manifest changed')
    prior = json.loads(prior_path.read_text())['cases']
    v.check(len(prior) == 46 and [row['case'] for row in prior] == list(range(46)),
            'published prior complete case ordering')
    core_rows, cases = [], []
    for case, orientation in pairs:
        result_path = work / f'fast-case-{case}-{orientation}.json'
        seal_path = work / f'fast-sealed-{case}-{orientation}.json'
        v.check(result_path.exists() and seal_path.exists(), 'missing complete orientation; no exclusion')
        result, seal = json.loads(result_path.read_text()), json.loads(seal_path.read_text())
        v.check(seal['status'] == 'COMPLETE_LOCAL_DUAL_ENGINE_EXECUTION' and
                seal['result_sha256'] == digest(result_path), 'incomplete/changed local complete execution')
        v.compare(seal['binding'], current, 'aggregation local source/executable mismatch')
        v.compare(result['binding'], current, 'aggregation result source/executable mismatch')
        v.check(result['status'] == 'COMPLETE_SELECTED_DUAL_ENGINE_ORIENTATION' and
                type(result['case']) is int and result['case'] == case and
                type(result['orientation']) is int and result['orientation'] == orientation,
                'aggregation completed domain/status')
        v.check(type(result['covers']) is int and result['covers'] == prior[case]['covers'],
                'complete prior four-tail domain count mismatch')
        if orientation == 1:
            # Swapping15/16 transports original y20 prefixes to new z20 prefixes.
            v.check(result['z_eleven'] == prior[case]['counts']['y_eleven'],
                    'transported complete degree20 prefix mismatch')
        intervals = result['intervals']
        v.check(intervals[0]['start'] == 0 and intervals[-1]['finish'] == result['covers'] and
                all(a['finish'] == b['start'] for a, b in zip(intervals, intervals[1:])),
                'aggregation interval gap/overlap')
        v.check(sum(r['z_eleven'] for r in intervals) == result['z_eleven'] and
                sum(r['y_ten'] for r in intervals) == result['core_count'],
                'aggregation complete interval counts')
        cores = result['cores']
        v.check(type(result['core_count']) is int and result['core_count'] == len(cores),
                'aggregation complete core count')
        v.check(all(core['case'] == case and core['orientation'] == orientation and
                    0 <= core['cover'] < result['covers'] and
                    core['core_sha256'] == v.sha(core['blocks']) for core in cores),
                'aggregation literal core metadata/hash')
        core_rows.extend(cores)
        cases.append({'case': case, 'orientation': orientation, 'input_m': result['input_m'],
                      'input_model': result['input_model'], 'covers': result['covers'],
                      'z_eleven': result['z_eleven'], 'cores': len(cores),
                      'carrier_sha256': result['carrier_sha256'],
                      'core_records_sha256': v.sha(cores), 'universes_sha256': v.sha(result['universes']),
                      'core_y_m_census': dict(sorted(Counter(core['y_m'] for core in cores).items()))})
    hashes = [core['core_sha256'] for core in core_rows]
    v.check(len(hashes) == len(set(hashes)), 'duplicate labelled core across marked orientations')
    record = {'status': 'COMPLETE_ALL92_JOINT_CENSUS' if full else 'COMPLETE_EXPLICIT_SELECTED_JOINT_DOMAINS',
              'cases': cases, 'orientation_count': len(cases), 'core_count': len(core_rows),
              'covers': sum(row['covers'] for row in cases),
              'z_eleven': sum(row['z_eleven'] for row in cases),
              'sorted_core_hashes_sha256': v.sha(sorted(hashes)),
              'core_records_sha256': v.sha(core_rows), 'binding': current,
              'scope': 'Joint stars only; no residual numerical bound follows without its separate certificate.'}
    if full:
        v.check(record['orientation_count'] == 92 and record['covers'] == 3080796 and
                sum(row['z_eleven'] for row in cases if row['orientation'] == 1) == 18062,
                'full92 orientation/tail/transport coverage')
    return core_rows, record


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--include-executable', type=Path, required=True)
    parser.add_argument('--color-executable', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    cores, record = load(args.work, [args.include_executable, args.color_executable])
    args.output.write_bytes(v.encode(record))
    print(json.dumps({k: record[k] for k in ('status', 'orientation_count', 'core_count', 'covers', 'z_eleven', 'core_records_sha256')}))
