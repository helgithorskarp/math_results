"""Regenerate all625 paired packings using only this package and PySAT.

Completed, pinned stages are resumable. Incomplete or failed native jobs are
preserved and never silently retried. Actual AP checking uses only stdlib.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
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


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + '.new')
    temporary.write_text(json.dumps(data, indent=2) + '\n')
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    started = time.monotonic()
    work = args.output_dir.resolve()
    repository = next((p for p in ROOT.parents if (p / '.git').exists()), ROOT.parent)
    require(work != repository and repository not in work.parents, 'Output must be outside the repository')
    require(sys.version_info >= (3, 11), 'Python3.11+ required')
    expected = json.loads((ROOT / 'expected.json').read_text())
    require(version('python-sat') == expected['python_sat'], 'Pinned PySAT version required')
    for name, digest in expected['source_sha256'].items():
        require(sha(ROOT / name) == digest, 'Frozen source differs:' + name)
    require(sha(ROOT / 'packings.json') == expected['certificate_sha256'], 'Supplied certificate digest')
    require((ROOT / 'packings.json').stat().st_size == expected['certificate_bytes'], 'Supplied certificate length')
    if work.exists():
        require(args.resume, 'Existing output requires explicit resume')
    else:
        require(not args.resume, 'Absent output cannot resume')
        work.mkdir(parents=True)
    names = list(expected['source_sha256']) + ['reproduce.py', 'requirements.txt', 'expected.json', 'packings.json']
    pin = {'sources': {n: sha(ROOT / n) for n in names}, 'python_sat': version('python-sat'),
           'hard_child_seconds': 30, 'case_cap': 200000, 'matching_conflict_cap': 10000,
           'threads': 1, 'simultaneous_CPU_jobs': 1, 'private_proof_inputs': False}
    pin_path, journal_path = work / 'pin.json', work / 'journal.json'
    if pin_path.exists():
        require(json.loads(pin_path.read_text()) == pin, 'Resume pins changed')
        journal = json.loads(journal_path.read_text())
        require(all(j['status'] == 'COMPLETED' for j in journal['jobs'].values()),
                'Interrupted or failed stages cannot resume')
    else:
        save(pin_path, pin)
        journal = {'status': 'PARTIAL_NO_EXCLUSION', 'jobs': {}}
        save(journal_path, journal)
    records = []

    def stage(name, command, output, cohort=False):
        old = journal['jobs'].get(name)
        if old:
            require(old['status'] == 'COMPLETED' and output.exists() and sha(output) == old['sha256'],
                    'Saved stage changed')
        else:
            require(not output.exists(), 'Unjournaled output cannot be overwritten')
            journal['jobs'][name] = {'status': 'STARTED', 'output': str(output), 'command': command}
            save(journal_path, journal)
            try:
                if cohort:
                    # The serial manager applies30s to each actual compute child.
                    # Its complete625-case sequence is not one30s child job.
                    with subprocess.Popen(command, env=ENV, stdout=subprocess.PIPE,
                                          stderr=subprocess.STDOUT, text=True) as run:
                        for line in run.stdout:
                            print(line.rstrip(), flush=True)
                        require(run.wait() == 0, 'Cohort stage failed')
                else:
                    run = subprocess.run(command, env=ENV, capture_output=True, text=True, timeout=30)
                    require(run.returncode == 0, run.stderr[-2000:])
                require(output.exists(), 'Stage produced no completed result')
            except BaseException as error:
                journal['status'] = 'STOPPED_NO_MATHEMATICAL_EXCLUSION'
                journal['jobs'][name].update(status='INCOMPLETE_OR_FAILED', error=str(error))
                save(journal_path, journal)
                raise
        data = json.loads(output.read_text())
        if cohort:
            leaves = data['jobs']
            require(data['pin']['sources'] == {n: pin['sources'][n] for n in data['pin']['sources']},
                    'Cohort source pins')
            require(len(leaves) == data['successful_jobs'], 'Cohort child count')
            for leaf in leaves:
                path = Path(leaf['output'])
                require(leaf['status'] == 'COMPLETED' and sha(path) == leaf['sha256'], 'Completed leaf changed')
                require(leaf['seconds'] < 30 and leaf['cases'] <= 200000, 'Cohort child cap')
            require(sha(Path(data['certificate'])) == data['certificate_sha256'], 'Cohort certificate changed')
            records.extend(leaves)
        else:
            source = ROOT / Path(command[2] if command[1] == '-O' else command[1]).name
            field = 'checker_sha256' if source.name == 'check_reflection622_packings.py' else 'source_sha256'
            require(data[field] == sha(source), 'Arithmetic/checker source pin')
            require(data['seconds'] < 30 and data['conservative_combined_cases'] <= 200000, 'Child cap')
            records.append({'status': 'COMPLETED', 'output': str(output), 'sha256': sha(output),
                            'seconds': data['seconds'], 'cases': data['conservative_combined_cases'],
                            'maxrss_kib': data['maxrss_kib'], 'mathematical_status': data['status']})
        journal['jobs'][name] = {'status': 'COMPLETED', 'output': str(output), 'sha256': sha(output)}
        save(journal_path, journal)
        return data

    manager = ROOT / 'run_reflection622_hybrid.py'
    pilot_result = work / 'pilot' / 'result.json'
    pilot = stage('pilot', [sys.executable, str(manager), '--scope', 'pilot', '--output-dir', str(work / 'pilot')],
                  pilot_result, cohort=True)
    require(pilot['status'] == 'HYBRID_REFLECTION_PILOT_BOTH_MODES_44_CONTROLS_VERIFIED' and
            pilot['indexes'] == expected['pilot_indexes'] and pilot['pin']['cache'] is None, 'Fresh mandatory pilot')
    full = stage('all625', [sys.executable, str(manager), '--scope', 'all', '--output-dir', str(work / 'all625'),
                           '--pilot-record', str(pilot_result)], work / 'all625' / 'result.json', cohort=True)
    require(full['status'] == 'ALL625_HYBRID_REFLECTION_PACKINGS_BOTH_MODES_44_CONTROLS_VERIFIED', 'Full cohort incomplete')
    require(full['certificate_sha256'] == expected['certificate_sha256'] and
            full['exact_check'] == expected['check'] and full['indexes'] == list(range(625)), 'Exact full certificate')
    require(Path(full['certificate']).read_bytes() == (ROOT / 'packings.json').read_bytes(), 'Fresh bytes differ')
    require(pilot['corruptions_per_mode'] == full['corruptions_per_mode'] == len(expected['controls']) == 22,
            'Corruption-control count')
    for result, directory in [(pilot, work / 'pilot'), (full, work / 'all625')]:
        for mode in [0, 1]:
            for control in expected['controls']:
                data = json.loads((directory / (control + f'-mode{mode}.json')).read_text())
                require(data['status'] == 'MATHEMATICAL_CORRUPTION_REJECTED' and data['control'] == control
                        and data['interpreter_optimization'] == mode, 'Exact corruption coverage')
    methods = Counter(pilot['methods'].values())
    methods.update(v for v in full['methods'].values() if v != 'CACHED_COMPLETED_PROPOSAL_CHECKED_AT_COHORT_END')
    require(dict(methods) == expected['fresh_methods'], 'Fresh construction-method coverage')
    checker = ROOT / 'check_reflection622_packings.py'
    for mode in [0, 1]:
        command = [sys.executable] + (['-O'] if mode else []) + [str(checker), '--certificate',
                   str(ROOT / 'packings.json'), '--scope', 'all', '--output', str(work / f'supplied-mode{mode}.json')]
        data = stage(f'supplied-mode{mode}', command, work / f'supplied-mode{mode}.json')
        require(data['status'] == expected['checker_status'] and data['interpreter_optimization'] == mode and
                data['certificate_sha256'] == expected['certificate_sha256'], 'Supplied positive check')
        require(all(data[k] == v for k, v in expected['check'].items()), 'Supplied exact check fields')
    audit = ROOT / 'audit_reduction.py'
    for mode, status in [('field', 'QUARTIC_FIELD_POWER_CHARACTER_AND_CRT_AUDIT_PASSED'),
                         ('shift', 'ALL_QUARTIC_LEADING_AND_CUBIC_COEFFICIENT_SHIFT_PAIRS_PASSED')]:
        output = work / f'audit-{mode}.json'
        data = stage('audit-' + mode, [sys.executable, str(audit), '--mode', mode, '--output', str(output)], output)
        require(data['status'] == status, 'Arithmetic audit failed')
    cursor, pairs, indexes = 0, 0, set()
    for start in expected['parameter_A_chunks']:
        require(start == cursor, 'A-domain coverage gap')
        count = min(64, 311 - start)
        output = work / f'audit-parameters-{start:03d}.json'
        data = stage(f'parameters-{start:03d}', [sys.executable, str(audit), '--mode', 'parameters',
                     '--start', str(start), '--count', str(count), '--output', str(output)], output)
        require(data['status'] == 'EXACT_EVEN_QUARTIC_TWO_PARAMETER_NORMALIZATION_SLICE_PASSED' and
                data['A_start_inclusive'] == start and data['A_stop_exclusive'] == start + count, 'Exact slice')
        cursor += count
        pairs += data['AB_parameter_pairs']
        indexes.update(data['canonical_indexes_reached'])
    require(cursor == 311 and pairs == expected['complete_parameters'] and indexes == set(range(625)),
            'Complete625-case normalization audit')
    require(len(records) == expected['expected_total_jobs'], 'Exact completed-job coverage')
    summary = {'agent': 'six-vdw-1', 'role': 'researcher', 'status': expected['status'],
               'completed_at': datetime.now(timezone.utc).isoformat(), 'python': platform.python_version(),
               'python_sat': version('python-sat'), 'pin': pin, 'private_proof_inputs': False,
               'certificate_sha256': expected['certificate_sha256'], 'certificate_bytes': expected['certificate_bytes'],
               'exact_check': expected['check'], 'fresh_methods': dict(methods),
               'pilot_jobs': pilot['successful_jobs'], 'all625_jobs': full['successful_jobs'],
               'corruptions_per_mode_per_cohort': 22, 'AB_parameter_pairs': pairs,
               'successful_jobs': len(records), 'jobs': records, 'seconds_total': time.monotonic() - started,
               'longest_child_seconds': max(r['seconds'] for r in records),
               'max_child_rss_kib': max(r['maxrss_kib'] for r in records),
               'maximum_child_cases': max(r['cases'] for r in records),
               'threads': 1, 'simultaneous_CPU_jobs': 1, 'hard_child_seconds': 30,
               'case_cap': 200000, 'matching_conflict_cap': 10000,
               'new_W_bound': None, 'external_independent_review': False}
    save(work / 'result.json', summary)
    journal['status'] = expected['status']
    save(journal_path, journal)
    print(json.dumps({k: v for k, v in summary.items() if k not in ['pin', 'jobs']}, indent=2), flush=True)


if __name__ == '__main__':
    main()
