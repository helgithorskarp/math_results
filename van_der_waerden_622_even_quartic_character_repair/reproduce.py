"""Fresh source-only625-case proof reproduction, with strict serial caps."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
           MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', PYTHONOPTIMIZE='0')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    work = args.output_dir.resolve()
    require(work != ROOT.parent and ROOT.parent not in work.parents, 'output must be outside publication repository')
    require(sys.version_info >= (3, 11), 'Python3.11+ required')
    if work.exists():
        require(args.resume, 'existing output requires explicit--resume')
    else:
        require(not args.resume, 'resume requires an existing run')
        work.mkdir(parents=True)
    require(not (work / 'STOPPED.json').exists(), 'failed job preserved; no silent retry')
    inflight = work / 'inflight.json'
    if inflight.exists():
        require(Path(json.loads(inflight.read_text())['output']).exists(), 'interrupted job incomplete; no silent retry')
    started = time.monotonic()
    expected = json.loads((ROOT / 'expected.json').read_text())
    pin = {'sources': {p.name: sha(p) for p in [ROOT / 'pack_cases.py', ROOT / 'check_packings.py',
                                              ROOT / 'audit_reduction.py', ROOT / 'reproduce.py',
                                              ROOT / 'expected.json', ROOT / 'packings.json']},
           'hard_child_seconds': 30, 'case_cap': 200000, 'threads': 1}
    pin_path = work / 'pin.json'
    if pin_path.exists():
        require(json.loads(pin_path.read_text()) == pin, 'source pins differ')
    else:
        pin_path.write_text(json.dumps(pin, indent=2) + '\n')
    require(sha(ROOT / 'packings.json') == expected['certificate_sha256'], 'supplied certificate digest')
    records = []

    def job(command, output, source, status):
        if output.exists():
            data = json.loads(output.read_text())
        else:
            inflight.write_text(json.dumps({'command': command, 'output': str(output)}, indent=2) + '\n')
            try:
                result = subprocess.run(command, cwd=ROOT, env=ENV, capture_output=True, text=True, timeout=30)
                require(result.returncode == 0, result.stderr[-1500:])
                data = json.loads(output.read_text())
            except Exception as error:
                (work / 'STOPPED.json').write_text(json.dumps({'output': str(output), 'error': str(error),
                    'no_mathematical_exclusion': True}, indent=2) + '\n')
                raise
        source_field = 'checker_sha256' if source.name == 'check_packings.py' else 'source_sha256'
        require(data[source_field] == sha(source), 'completed source pin mismatch')
        require(data['status'] == status, 'job status mismatch')
        require(data['conservative_combined_cases'] <= 200000 and data['seconds'] < 30, 'unchanged resource guard')
        if inflight.exists():
            inflight.unlink()
        records.append({'output': str(output), 'sha256': sha(output), 'seconds': data['seconds'],
                        'cases': data['conservative_combined_cases'], 'maxrss_kib': data['maxrss_kib'],
                        'status': data['status']})
        return data

    generator = ROOT / 'pack_cases.py'
    cases = []
    for start in range(0, 625, 2):
        count = min(2, 625 - start)
        output = work / f'proposal-{start:03d}.json'
        data = job([sys.executable, str(generator), '--start', str(start), '--count', str(count),
                    '--output', str(output)], output, generator,
                   'GREEDY_ROOT_FREE_PACKINGS_PENDING_INDEPENDENT_CHECK')
        require(data['start'] == start and data['count'] == count, 'proposal case interval')
        require([c['index'] for c in data['cases']] == list(range(start, start + count)), 'proposal ordered coverage')
        require(all(c['packing_size'] == 20 for c in data['cases']), 'greedy did not find required packing; no exclusion')
        cases.extend({k: c[k] for k in ['index', 'coefficients', 'APs']} for c in data['cases'])
        if start % 100 == 0 or start + count == 625:
            print(json.dumps({'cases_regenerated': len(cases)}), flush=True)
    require([c['index'] for c in cases] == list(range(625)), 'complete proposal cohort')
    generated = work / 'packings.json'
    raw = (json.dumps({'modulus': 311, 'APs_per_case': 20, 'cases': cases}, separators=(',', ':')) + '\n').encode()
    require(hashlib.sha256(raw).hexdigest() == expected['certificate_sha256'], 'fresh canonical certificate digest')
    if generated.exists():
        require(generated.read_bytes() == raw, 'saved generated certificate differs')
    else:
        generated.write_bytes(raw)
    checker = ROOT / 'check_packings.py'
    for optimization in [0, 1]:
        flags = ['-O'] if optimization else []
        for label, certificate in [('supplied', ROOT / 'packings.json'), ('fresh', generated)]:
            output = work / f'{label}-check-mode{optimization}.json'
            data = job([sys.executable, *flags, str(checker), '--certificate', str(certificate), '--output', str(output)],
                       output, checker, expected['checker_status'])
            require(data['interpreter_optimization'] == optimization, 'actual interpreter optimization')
            require(data['certificate_sha256'] == expected['certificate_sha256'], 'checked input certificate')
            for key, value in expected['check'].items():
                require(data[key] == value, 'expected exact check field:' + key)
        for control in expected['controls']:
            output = work / f'control-{control}-mode{optimization}.json'
            data = job([sys.executable, *flags, str(checker), '--certificate', str(generated),
                        '--output', str(output), '--control', control], output, checker,
                       'MATHEMATICAL_CORRUPTION_REJECTED')
            require(data['control'] == control and data['interpreter_optimization'] == optimization, 'control coverage')
    require(len(expected['controls']) == len(set(expected['controls'])) == 18, 'complete control manifest')
    audit = ROOT / 'audit_reduction.py'
    for mode, status in [('field', 'QUARTIC_FIELD_POWER_CHARACTER_AND_CRT_AUDIT_PASSED'),
                         ('shift', 'ALL_QUARTIC_LEADING_AND_CUBIC_COEFFICIENT_SHIFT_PAIRS_PASSED')]:
        output = work / f'audit-{mode}.json'
        job([sys.executable, str(audit), '--mode', mode, '--output', str(output)], output, audit, status)
    cursor, pairs, indexes = 0, 0, set()
    for start in expected['parameter_A_chunks']:
        require(start == cursor, 'audit A-domain gap')
        count = min(64, 311 - start)
        output = work / f'audit-parameters-{start:03d}.json'
        data = job([sys.executable, str(audit), '--mode', 'parameters', '--start', str(start), '--count', str(count),
                    '--output', str(output)], output, audit,
                   'EXACT_EVEN_QUARTIC_TWO_PARAMETER_NORMALIZATION_SLICE_PASSED')
        require(data['A_start_inclusive'] == start and data['A_stop_exclusive'] == start + count, 'audit actual interval')
        cursor = start + count
        pairs += data['AB_parameter_pairs']
        indexes.update(data['canonical_indexes_reached'])
    require(cursor == 311 and pairs == 96721 and indexes == set(range(625)), 'complete normalization coverage')
    summary = {'agent': 'six-vdw-1', 'role': 'researcher', 'status': expected['status'],
               'completed_at': datetime.now(timezone.utc).isoformat(), 'python': platform.python_version(),
               'pin': pin, 'certificate_sha256': expected['certificate_sha256'],
               'exact_check': expected['check'], 'corruptions_per_mode': 18,
               'AB_parameter_pairs': pairs, 'fresh_case_count': 625,
               'successful_jobs': len(records), 'jobs': records,
               'seconds_total': time.monotonic() - started,
               'longest_child_seconds': max(r['seconds'] for r in records),
               'max_child_rss_kib': max(r['maxrss_kib'] for r in records),
               'maximum_child_cases': max(r['cases'] for r in records),
               'threads': 1, 'simultaneous_CPU_jobs': 1, 'hard_child_seconds': 30,
               'new_W_bound': None, 'external_independent_review': False}
    (work / 'result.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k not in ['jobs', 'pin']}, indent=2), flush=True)


if __name__ == '__main__':
    main()
