"""Serial greedy proposals with one capped matching fallback per missing case.

Only complete mandatory-cohort actual-term checking proves the packing claim.
UNKNOWN, incomplete output, unsupported caps and unchecked UNSAT stop the run.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
PILOT = [0, 1, 2, 3, 4, 10, 157, 313, 314, 315, 469, 624]
CONSTRUCTION = ['pack_reflection622_cases.py', 'check_reflection622_packings.py',
                'build_reflection622_matching.py', 'solve_reflection622_matching.py']
CONTROLS = ['missing_case', 'duplicate_case', 'zero_polynomial', 'wrong_quadratic_class',
            'root_term', 'bichromatic_AP', 'within_pair_overlap', 'between_pair_overlap',
            'wrong_reflection', 'missing_pair', 'missing_reflection_member', 'boolean_index',
            'boolean_start', 'zero_start', 'zero_step', 'step311', 'outside_interval',
            'extra_root_hypothesis', 'unsupported_bound', 'wrong_modulus', 'wrong_constant', 'reversed_coefficients']
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')


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
    parser.add_argument('--scope', choices=['pilot', 'all'], required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--seed-cases', type=Path)
    parser.add_argument('--pilot-record', type=Path)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    began = time.monotonic()
    indexes = PILOT if args.scope == 'pilot' else list(range(625))
    construction = {n: sha(ROOT / n) for n in CONSTRUCTION}
    source_names = CONSTRUCTION + ['check_reflection622_subset.py', Path(__file__).name]
    sources = {n: sha(ROOT / n) for n in source_names}
    cached, cache_pin = {}, None
    if args.scope == 'all':
        require(args.pilot_record is not None and args.seed_cases is None, 'Complete pilot gate required')
        pilot = json.loads(args.pilot_record.read_text())
        require(pilot['status'] == 'HYBRID_REFLECTION_PILOT_BOTH_MODES_44_CONTROLS_VERIFIED', 'Pilot incomplete')
        require(pilot['pin']['sources'] == sources and pilot['indexes'] == PILOT, 'Pilot sources/scope differ')
        cert_path = Path(pilot['certificate'])
        require(sha(cert_path) == pilot['certificate_sha256'], 'Pilot certificate changed')
        cached = {c['index']: c for c in json.loads(cert_path.read_text())['cases']}
        cache_pin = {'pilot_record': str(args.pilot_record.resolve()), 'sha256': sha(args.pilot_record),
                     'certificate_sha256': sha(cert_path)}
    elif args.seed_cases:
        seed = json.loads(args.seed_cases.read_text())
        require(seed['construction_sources'] == construction, 'Seed construction sources changed')
        for item in seed['input_pins']:
            require(sha(Path(item['path'])) == item['sha256'], 'Seed input changed')
        cached = {c['index']: c for c in seed['cases']}
        cache_pin = {'seed_cases': str(args.seed_cases.resolve()), 'sha256': sha(args.seed_cases)}
    directory = args.output_dir.resolve()
    if directory.exists():
        require(args.resume, 'Existing output needs explicit resume')
    else:
        require(not args.resume, 'Absent output cannot resume')
        directory.mkdir(parents=True)
    pin = {'sources': sources, 'construction_sources': construction, 'scope': args.scope, 'indexes': indexes,
           'cache': cache_pin, 'case_cap': 200000, 'hard_child_seconds': 30, 'threads': 1,
           'simultaneous_CPU_jobs': 1, 'matching_queries_per_case_at_most': 1, 'matching_conflict_cap': 10000}
    pin_path, journal_path = directory / 'pin.json', directory / 'journal.json'
    if pin_path.exists():
        require(json.loads(pin_path.read_text()) == pin, 'Resume pins changed')
        journal = json.loads(journal_path.read_text())
        require(all(j['status'] == 'COMPLETED' for j in journal['jobs'].values()), 'Failed/interrupted jobs cannot resume')
    else:
        save(pin_path, pin)
        journal = {'agent': 'six-vdw-1', 'role': 'researcher', 'status': 'PARTIAL_NO_EXCLUSION', 'jobs': {}}
    records, cases, methods = [], [], {}

    def child(name, command, output):
        old = journal['jobs'].get(name)
        if old is not None:
            require(old['status'] == 'COMPLETED' and output.exists() and sha(output) == old['sha256'], 'Saved job changed')
            records.append(old)
            return json.loads(output.read_text())
        require(not output.exists(), 'Unjournaled output cannot be overwritten')
        journal['jobs'][name] = {'status': 'STARTED', 'output': str(output), 'command': command}
        save(journal_path, journal)
        try:
            run = subprocess.run(command, env=ENV, capture_output=True, text=True, timeout=30)
        except (subprocess.TimeoutExpired, KeyboardInterrupt):
            journal.update(status='STOPPED_OPERATIONAL_LIMIT_OR_INTERRUPTION_NO_EXCLUSION')
            journal['jobs'][name]['status'] = 'INCOMPLETE'
            save(journal_path, journal)
            raise
        if run.returncode:
            journal.update(status='STOPPED_CHILD_FAILURE_NO_EXCLUSION')
            journal['jobs'][name].update(status='FAILED', stderr=run.stderr[-3000:], returncode=run.returncode)
            save(journal_path, journal)
            raise RuntimeError('Child failed: ' + name)
        data = json.loads(output.read_text())
        seconds = data.get('seconds', data.get('seconds_total', 0))
        count = data.get('conservative_combined_cases', data.get('conservative_preflight_cases', 0))
        limited = 'OVER_CAP' in data['status']
        require(seconds < 30 and (count <= 200000 or limited), 'Child resource guard')
        entry = {'status': 'COMPLETED', 'output': str(output), 'sha256': sha(output), 'seconds': seconds,
                 'cases': count, 'maxrss_kib': data.get('maxrss_kib', 0), 'mathematical_status': data['status']}
        journal['jobs'][name] = entry
        save(journal_path, journal)
        records.append(entry)
        return data

    def stop(reason, index):
        summary = {'agent': 'six-vdw-1', 'role': 'researcher', 'status': reason, 'pin': pin,
                   'stopped_index': index, 'indexes_completed': [c['index'] for c in cases],
                   'jobs': records, 'mathematical_exclusion': False, 'new_W_bound': None}
        save(directory / 'result.json', summary)
        journal['status'] = reason
        save(journal_path, journal)
        print(json.dumps({'status': reason, 'stopped_index': index, 'cases_completed': len(cases)}), flush=True)

    for index in indexes:
        if index in cached:
            case = cached[index]
            methods[str(index)] = 'CACHED_COMPLETED_PROPOSAL_CHECKED_AT_COHORT_END'
        else:
            output = directory / f'proposal-{index:03d}.json'
            proposed = child(f'proposal-{index:03d}', [sys.executable, str(ROOT / CONSTRUCTION[0]),
                              '--indexes', str(index), '--output', str(output)], output)
            require(proposed['indexes'] == [index] and proposed['source_sha256'] == construction[CONSTRUCTION[0]],
                    'Wrong proposal source/index')
            proposal = proposed['cases'][0]
            if proposal['pairs_found'] == 12:
                case = {k: proposal[k] for k in ['index', 'coefficients', 'pairs']}
                methods[str(index)] = 'GREEDY'
            else:
                model_dir = directory / f'matching-{index:03d}'
                metadata = child(f'build-{index:03d}', [sys.executable, str(ROOT / CONSTRUCTION[2]),
                                 '--index', str(index), '--output-dir', str(model_dir)], model_dir / 'metadata.json')
                if metadata['status'] != 'MATCHING_CNF_READY_PENDING_SOLVER_AND_DEFINITION_CHECK':
                    stop(metadata['status'], index)
                    return
                result = child(f'solve-{index:03d}', [sys.executable, str(ROOT / CONSTRUCTION[3]),
                               '--model-dir', str(model_dir)], model_dir / 'solver.json')
                if result['status'] != 'SAT_MATCHING_PENDING_ACTUAL_TERM_CHECK':
                    stop(result['status'], index)
                    return
                witness = Path(result['witness'])
                require(sha(witness) == result['witness_sha256'], 'Changed matching witness')
                checked = model_dir / 'definition-checked.json'
                checked_data = child(f'definition-{index:03d}', [sys.executable, str(ROOT / 'check_reflection622_subset.py'),
                                     '--certificate', str(witness), '--indexes', str(index), '--output', str(checked)], checked)
                require(checked_data['indexes'] == [index] and checked_data['APs_checked'] == 24, 'Wrong witness check scope')
                case = json.loads(witness.read_text())['cases'][0]
                methods[str(index)] = 'CAPPED_SAT_MATCHING_AND_SEPARATE_ACTUAL_TERM_CHECK'
        require(case['index'] == index and len(case['pairs']) == 12, 'Wrong selected case')
        cases.append(case)
        if len(cases) % 25 == 0 or len(cases) == len(indexes):
            print(json.dumps({'scope': args.scope, 'cases_collected': len(cases),
                              'new_matching_witnesses': sum(v.startswith('CAPPED') for v in methods.values())}), flush=True)
    certificate = {'modulus': 311, 'pairs_per_case': 12, 'cases': cases}
    cert_path = directory / 'packings.json'
    compact = json.dumps(certificate, separators=(',', ':')) + '\n'
    if cert_path.exists():
        require(cert_path.read_text() == compact, 'Resumed compact certificate differs')
    else:
        cert_path.write_text(compact)
    positives = []
    checker = ROOT / CONSTRUCTION[1]
    for mode in [0, 1]:
        executable = [sys.executable] + (['-O'] if mode else [])
        output = directory / f'positive-mode{mode}.json'
        data = child(f'positive-mode{mode}', executable + [str(checker), '--certificate', str(cert_path),
                     '--scope', args.scope, '--output', str(output)], output)
        require(data['interpreter_optimization'] == mode and data['cases'] == len(indexes) and
                data['certificate_sha256'] == sha(cert_path) and data['checker_sha256'] == construction[checker.name],
                'Wrong mandatory-cohort check')
        positives.append(data)
        for control in CONTROLS:
            output = directory / (control + f'-mode{mode}.json')
            rejected = child(control + f'-mode{mode}', executable + [str(checker), '--certificate', str(cert_path),
                             '--scope', args.scope, '--control', control, '--output', str(output)], output)
            require(rejected['status'] == 'MATHEMATICAL_CORRUPTION_REJECTED' and
                    rejected['control'] == control and rejected['interpreter_optimization'] == mode, 'Wrong mathematical rejection')
    summary = {'agent': 'six-vdw-1', 'role': 'researcher', 'completed_at': datetime.now(timezone.utc).isoformat(),
               'status': 'HYBRID_REFLECTION_PILOT_BOTH_MODES_44_CONTROLS_VERIFIED' if args.scope == 'pilot' else
                         'ALL625_HYBRID_REFLECTION_PACKINGS_BOTH_MODES_44_CONTROLS_VERIFIED',
               'pin': pin, 'indexes': indexes, 'certificate': str(cert_path), 'certificate_sha256': sha(cert_path),
               'certificate_bytes': cert_path.stat().st_size, 'methods': methods,
               'exact_check': {k: positives[0][k] for k in ['cases', 'pairs_per_case', 'APs_per_case', 'APs_checked',
                              'actual_term_colors_checked', 'field_residues_per_case', 'largest_canonical_position']},
               'successful_jobs': len(records), 'jobs': records, 'corruptions_per_mode': 22,
               'seconds_total': time.monotonic() - began, 'longest_child_seconds': max(j['seconds'] for j in records),
               'max_child_rss_kib': max(j['maxrss_kib'] for j in records), 'maximum_child_cases': max(j['cases'] for j in records),
               'threads': 1, 'simultaneous_CPU_jobs': 1, 'hard_child_seconds': 30,
               'all625_claim': args.scope == 'all', 'new_W_bound': None, 'external_independent_review': False}
    save(directory / 'result.json', summary)
    journal['status'] = summary['status']
    save(journal_path, journal)
    print(json.dumps({k: summary[k] for k in ['status', 'successful_jobs', 'certificate_sha256', 'seconds_total',
                                           'longest_child_seconds', 'max_child_rss_kib', 'maximum_child_cases']}, indent=2), flush=True)


if __name__ == '__main__':
    main()
