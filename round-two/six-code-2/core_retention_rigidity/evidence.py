"""Freeze preceding complete normal evidence and compare fresh optimized runs."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys


FILES = [('RESULT.json', 'core-retention-{mode}'),
         ('CERTIFICATE.json', 'core-retention-{mode}'),
         ('ORACLE.json', 'core-retention-{mode}'),
         ('STATES.json', 'core-retention-{mode}'),
         ('DOMAINS.json', 'core-retention-{mode}'),
         ('TAIL_MAXIMA.json', 'core-retention-{mode}'),
         ('AUDIT.json', 'core-retention-audit-{mode}'),
         ('DOMAIN_AUDIT.json', 'core-retention-audit-{mode}')]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def stable(value):
    if isinstance(value, dict):
        return {k: stable(v) for k, v in value.items() if k not in {'seconds', 'peak_RSS_kib'}}
    if isinstance(value, list):
        return [stable(v) for v in value]
    return value


def sources():
    directory = Path(__file__).parent
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(directory.iterdir()) if p.suffix == '.py' or p.name == 'INSTANCE.json'}


def read_data(scratch, mode):
    records, cores = {}, {}
    for name, pattern in FILES:
        path = scratch / pattern.format(mode=mode) / name
        raw = path.read_bytes()
        value = json.loads(raw)
        cores[name] = stable(value)
        records[name] = {'path': str(path), 'bytes': len(raw), 'raw_sha256': hashlib.sha256(raw).hexdigest(),
                         'stable_sha256': hashlib.sha256(encoded(cores[name])).hexdigest(),
                         'seconds': value.get('seconds') if isinstance(value, dict) else None,
                         'peak_RSS_kib': value.get('peak_RSS_kib') if isinstance(value, dict) else None}
    need(cores['RESULT.json']['status'] == 'COMPLETE_CORE_RETENTION55_UPPER69_AND_EXACT84_MAXIMA' and
         cores['AUDIT.json']['status'] == 'COMPLETE_INDEPENDENT_CORE_RETENTION55_MAXIMUM_SIZE_COUNT_AND_INVENTORY_AUDIT',
         'frontier incomplete')
    need(len(cores['DOMAINS.json']) == len(cores['DOMAIN_AUDIT.json']) == 1596, 'missing puncture domain')
    need(len(cores['AUDIT.json']['damage_controls']) == 11 and
         all(r['rejected'] for r in cores['AUDIT.json']['damage_controls']), 'missing damage rejection')
    return records, cores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['freeze', 'compare'])
    parser.add_argument('--scratch', type=Path, default=Path('scratch'))
    parser.add_argument('--expected', type=Path, default=Path(__file__).parent / 'EXPECTED.json')
    parser.add_argument('--output', type=Path, default=Path('scratch/core-retention-validation.json'))
    args = parser.parse_args()
    normal, normal_cores = read_data(args.scratch, 'normal')
    if args.action == 'freeze':
        need(not args.expected.exists(), 'refuse to replace preceding frozen expectation')
        value = {'agent': 'six-code-2', 'role': 'researcher',
                 'status': 'FROZEN_PRECEDING_COMPLETE_NORMAL_CORE_RETENTION55_EVIDENCE',
                 'frozen_at': datetime.now(timezone.utc).isoformat(), 'python_version': sys.version.split()[0],
                 'source_sha256': sources(),
                 'stable_evidence_sha256': {name: r['stable_sha256'] for name, r in normal.items()},
                 'exact_frontier': {'core_words': 57, 'retained_core_words': 55,
                                    'physical_words': 8568, 'punctures': 1596,
                                    'upper_bound': 69, 'maximum_codes': 84,
                                    'all_maximum_codes_restore_entire_core': True,
                                    'maximum_completion_polynomial': [1, 12, 38, 28, 5]}}
        args.expected.write_bytes(encoded(value))
        print(json.dumps(value['exact_frontier'], sort_keys=True), flush=True)
        return
    raw = args.expected.read_bytes()
    expected = json.loads(raw)
    need(expected['status'] == 'FROZEN_PRECEDING_COMPLETE_NORMAL_CORE_RETENTION55_EVIDENCE', 'wrong frozen expectation')
    need(expected['python_version'] == sys.version.split()[0] and expected['source_sha256'] == sources(),
         'interpreter, source or instance changed after freeze')
    optimized, optimized_cores = read_data(args.scratch, 'optimized')
    for name in normal:
        need(normal_cores[name] == optimized_cores[name], 'entrywise normal/O evidence differs: ' + name)
        need(normal[name]['stable_sha256'] == optimized[name]['stable_sha256'] ==
             expected['stable_evidence_sha256'][name], 'frozen evidence differs: ' + name)
    byte_equal = [name for name in normal if name not in {'RESULT.json', 'AUDIT.json'}]
    for name in byte_equal:
        need(Path(normal[name]['path']).read_bytes() == Path(optimized[name]['path']).read_bytes(),
             'literal evidence bytes differ: ' + name)
    value = {'agent': 'six-code-2', 'role': 'researcher',
             'status': 'AUTHOR_COMPLETE_CORE_RETENTION55_EXACT_UPPER69_AND84_MAXIMUM_CODES',
             'expected_sha256': hashlib.sha256(raw).hexdigest(), 'exact_frontier': expected['exact_frontier'],
             'all_stable_evidence_equal_normal_optimized_and_frozen': True,
             'raw_byte_equal_evidence': byte_equal, 'normal': normal, 'optimized': optimized,
             'max_peak_RSS_kib': max(r['peak_RSS_kib'] or 0 for mode in [normal, optimized] for r in mode.values()),
             'python_version': sys.version.split()[0], 'source_commit': None, 'graph_ref': None,
             'proof_status': 'Exact complete finite computations, ordinary unformalized conflict/partition/maximum-count/retention/component bridges, different same-author audits; independently unreviewed, priority unassessed.',
             'resource_policy': 'Existing1CPU2GiB, serial, threads1; initial60s whole-frontier guards never hit or increased.'}
    args.output.write_bytes(encoded(value))
    print(json.dumps({k: v for k, v in value.items() if k not in {'normal', 'optimized'}}, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
