"""Reproduce the single-interval exclusion using only this source directory."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
           NUMEXPR_NUM_THREADS='1', PYTHONOPTIMIZE='0')
SOURCE_NAMES = ['verify_interval_cover.py', 'export_interval_cover_bitset.py', 'check_residual_interval_points.py',
                'check_interval_word_chunk.py', 'propose_residual_interval_aps.py', 'audit_base_formula.py',
                Path(__file__).name]
INPUT_NAMES = ['base3704.bits', 'AP-cover.json', 'residual-cuts.json', 'point-obstructions.json', 'expected.json']
COVER_CONTROLS = ['empty_APs', 'over_cap_APs', 'boolean_start', 'zero_step', 'negative_start', 'outside_word',
                  'duplicate_AP', 'wrong_length', 'wrong_digest', 'unsupported_terms', 'extra_hypothesis',
                  'drop_to_seed_false_cover']
POINT_CONTROLS = ['empty_points', 'missing_point', 'duplicate_cut', 'wrong_cut', 'boolean_coordinate', 'zero_step',
                  'outside_word', 'bichromatic_AP', 'wrong_length', 'unsupported_terms', 'wrong_word_digest',
                  'wrong_cover_digest', 'wrong_residual_digest', 'extra_hypothesis']


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + '.new')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    directory = args.output_dir.resolve()
    require(args.resume == directory.exists(), 'Existing output requires resume; new output must be absent')
    directory.mkdir(parents=True, exist_ok=True)
    expected = json.loads((ROOT / 'expected.json').read_text())
    for name, digest in expected['input_sha256'].items():
        require(sha(ROOT / name) == digest, 'Wrong compact proof input: ' + name)
    pin = {'sources': {n: sha(ROOT / n) for n in SOURCE_NAMES}, 'inputs': {n: sha(ROOT / n) for n in INPUT_NAMES},
           'python': sys.version, 'case_cap': 200000, 'child_seconds': 30, 'threads': 1, 'simultaneous_CPU_jobs': 1,
           'source_only': True, 'private_proof_inputs': False}
    if (directory / 'pin.json').exists():
        require(json.loads((directory / 'pin.json').read_text()) == pin, 'Resume source/input pins changed')
        journal = json.loads((directory / 'journal.json').read_text())
        require(all(j['status'] == 'COMPLETED' for j in journal['jobs'].values()), 'Failed/incomplete stages cannot resume')
    else:
        save(directory / 'pin.json', pin)
        journal = {'status': 'PARTIAL_NO_FAMILY_CONCLUSION', 'jobs': {}}
    jobs = []

    def child(name, source, arguments, mode=0):
        output = directory / (name + '.json')
        command = [sys.executable] + (['-O'] if mode else []) + [str(ROOT / source)] + arguments + ['--output', str(output)]
        old = journal['jobs'].get(name)
        if old:
            require(sha(output) == old['sha256'], 'Completed output changed')
        else:
            require(not output.exists(), 'Unjournaled output cannot be overwritten')
            journal['jobs'][name] = {'status': 'STARTED', 'command': command}
            save(directory / 'journal.json', journal)
            process = None
            try:
                process = subprocess.Popen(command, env=ENV, text=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, start_new_session=True)
                stdout, stderr = process.communicate(timeout=30)
                require(process.returncode == 0, stderr[-2500:])
            except BaseException as error:
                if process is not None and process.poll() is None:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.communicate()
                journal['jobs'][name].update(status='FAILED_OR_INCOMPLETE', error=str(error))
                journal['status'] = 'STOPPED_OPERATIONAL_FAILURE_NO_EXCLUSION'
                save(directory / 'journal.json', journal)
                raise
        data = json.loads(output.read_text())
        source_digest = data.get('checker_sha256', data.get('source_sha256'))
        require(source_digest == pin['sources'][source], 'Wrong child source')
        cases = data.get('conservative_combined_cases', data.get('APs_checked', data.get('actual_AP_assignment_cases')))
        require(type(cases) is int and cases <= 200000 and data['seconds'] < 30, 'Unchanged operational guard')
        if 'interpreter_optimization' in data:
            require(data['interpreter_optimization'] == mode, 'Wrong optimization mode')
        entry = {'status': 'COMPLETED', 'output': str(output), 'sha256': sha(output), 'cases': cases,
                 'seconds': data['seconds'], 'maxrss_kib': data['maxrss_kib'], 'mathematical_status': data['status']}
        journal['jobs'][name] = entry
        save(directory / 'journal.json', journal)
        jobs.append(entry)
        return data

    word, cover, cuts, points = [ROOT / n for n in INPUT_NAMES[:4]]
    formula = child('base-formula', 'audit_base_formula.py', ['--word', str(word)])
    require(formula['status'] == 'EXPLICIT_QR617_FORMULA_MATCHES_ALL3704_BITS', 'Base formula audit failed')
    # The frozen baseline rank checker uses assertions. It is deliberately run
    # only in normal mode, with PYTHONOPTIMIZE=0 and no -O argument.
    controls = child('baseline-controls', 'check_interval_word_chunk.py', ['--controls'])
    require(controls['status'] == 'INTERVAL_RANK_DOMAIN_AND_MONOCHROME_CONTROLS_PASSED', 'Baseline definition controls')
    monochromes, checked = [], 0
    for start in range(0, 1141450, 190000):
        stop = min(1141450, start + 190000)
        witness = directory / f'baseline-{start:07d}.jsonl'
        data = child(f'baseline-{start:07d}', 'check_interval_word_chunk.py',
                     ['--word', str(word), '--start', str(start), '--stop', str(stop), '--monochromes', str(witness)])
        require(data['AP_start_inclusive'] == start and data['AP_stop_exclusive'] == stop
                and data['APs_checked'] == stop - start and data['word_file_sha256'] == pin['inputs']['base3704.bits']
                and data['monochromes_sha256'] == sha(witness), 'Baseline AP partition changed')
        checked += data['APs_checked']
        monochromes.extend(json.loads(line) for line in witness.read_text().splitlines())
    require(checked == 1141450 and len(monochromes) == 1
            and monochromes[0]['a_zero_based'] == 1 and monochromes[0]['d'] == 617, 'Exact baseline mismatch')
    print(json.dumps({'stage': 'baseline', 'all_APs': checked, 'bad_APs': len(monochromes)}), flush=True)

    supplied_cuts = json.loads(cuts.read_text())['cuts']
    mode_cuts = []
    for mode in [0, 1]:
        collected, domain = [], 0
        for start in range(0, 3704, 32):
            count = min(32, 3704 - start)
            arguments = ['--word', str(word), '--certificate', str(cover), '--row-start', str(start), '--row-count', str(count)]
            merge = child(f'merge-mode{mode}-row{start:04d}', 'verify_interval_cover.py', arguments, mode)
            bitset = child(f'bitset-mode{mode}-row{start:04d}', 'export_interval_cover_bitset.py', arguments, mode)
            for data in [merge, bitset]:
                require(data['certificate_sha256'] == pin['inputs']['AP-cover.json']
                        and data['word_file_sha256'] == pin['inputs']['base3704.bits']
                        and data['row_start'] == start and data['row_stop_exclusive'] == start + count,
                        'Coverage partition/input mismatch')
            require(merge['uncovered_intervals'] == bitset['uncovered_count']
                    and merge['cut_intervals_checked'] == bitset['cut_intervals_checked']
                    and [{k: r[k] for k in ['left', 'cut_intervals', 'uncovered']} for r in merge['rows']] == bitset['rows'],
                    'Independent coverage algorithms disagree')
            require(merge['selected_APs'] == bitset['selected_APs'] == 289
                    and merge['derived_rectangles'] == bitset['derived_rectangles'] == 525,
                    'Exact certificate scope differs')
            domain += bitset['cut_intervals_checked']
            collected.extend(bitset['cuts'])
        require(domain == 3704 * 3705 // 2 == 6861660 and collected == supplied_cuts and len(collected) == 2899,
                'Every mandatory residual cut must equal the full cover complement')
        mode_cuts.append(collected)
        for control in COVER_CONTROLS:
            data = child(f'cover-control-mode{mode}-{control}', 'verify_interval_cover.py',
                         ['--word', str(word), '--certificate', str(cover), '--row-start', '0', '--row-count', '32',
                          '--control', control], mode)
            require(data['status'] == 'MATHEMATICAL_CORRUPTION_REJECTED' and data['control'] == control,
                    'Cover mathematical corruption accepted')
        arguments = ['--word', str(word), '--cover', str(cover), '--cuts', str(cuts), '--certificate', str(points)]
        data = child(f'points-mode{mode}', 'check_residual_interval_points.py', arguments, mode)
        require(data['status'] == 'ALL2899_MANDATORY_RESIDUAL_CUTS_HAVE_DIRECTLY_CHECKED_MONO_APS'
                and data['certificate_sha256'] == pin['inputs']['point-obstructions.json']
                and data['cover_sha256'] == pin['inputs']['AP-cover.json']
                and data['residual_cuts_sha256'] == pin['inputs']['residual-cuts.json'], 'Direct point check incomplete')
        for control in POINT_CONTROLS:
            corrupted = child(f'point-control-mode{mode}-{control}', 'check_residual_interval_points.py',
                              arguments + ['--control', control], mode)
            require(corrupted['status'] == 'MATHEMATICAL_CORRUPTION_REJECTED' and corrupted['control'] == control,
                    'Point mathematical corruption accepted')
        print(json.dumps({'stage': 'complete proof check', 'mode': mode, 'all_cut_intervals': domain,
                          'cover_remaining': len(collected), 'residual_obstructions': data['APs_verified']}), flush=True)
    require(mode_cuts[0] == mode_cuts[1], 'Optimization changes exact family coverage')

    # Fresh positive generation is extra reproducibility evidence, not a proof
    # premise. Every provided AP has already passed direct definition checking.
    cursor, regenerated, unresolved, search_jobs = [0, 1, 1], [], [], 0
    for index in range(512):
        if cursor[0] == 2899:
            break
        data = child(f'fresh-positive-{index:03d}', 'propose_residual_interval_aps.py',
                     ['--word', str(word), '--cuts', str(cuts), '--point-index', str(cursor[0]),
                      '--next-d', str(cursor[1]), '--next-a', str(cursor[2])])
        require(data['initial_cursor'] == cursor and data['next_cursor'] > cursor
                and data['word_sha256'] == pin['inputs']['base3704.bits']
                and data['cuts_sha256'] == pin['inputs']['residual-cuts.json']
                and data['AP_tests'] <= 8000 and data['finished_points'] <= 32, 'Fresh positive cursor/input guard')
        cursor = data['next_cursor']
        regenerated.extend(data['positive_points'])
        unresolved.extend(data['prefix64_unresolved_cuts'])
        search_jobs += 1
    require(cursor == [2899, 1, 1] and not unresolved and regenerated == json.loads(points.read_text())['points'],
            'Fresh bounded positive regeneration incomplete or differs')
    result = {'agent': 'six-vdw-1', 'role': 'researcher', 'completed_at': datetime.now(timezone.utc).isoformat(),
              'status': 'ALL6861660_SINGLE_INTERVAL_INVERSIONS_EXCLUDED_EXACTLY_BOTH_MODES',
              'check': expected['check'], 'base_word_APs_checked': checked, 'base_word_bad_APs': len(monochromes),
              'cover_APs': len(json.loads(cover.read_text())['APs']), 'covered_cuts': 6861660 - 2899,
              'residual_cuts': 2899, 'residual_APs_per_mode': 2899, 'mathematical_corruptions': 52,
              'fresh_positive_jobs': search_jobs, 'successful_jobs': len(jobs), 'jobs': jobs, 'pin': pin,
              'private_proof_inputs': False, 'new_W_bound': None,
              'seconds_total': sum(j['seconds'] for j in jobs),
              'longest_child_seconds': max(j['seconds'] for j in jobs),
              'maximum_child_cases': max(j['cases'] for j in jobs), 'max_child_rss_kib': max(j['maxrss_kib'] for j in jobs)}
    require(result['status'] == expected['status'], 'Expected scope differs')
    save(directory / 'result.json', result)
    journal['status'] = result['status']
    save(directory / 'journal.json', journal)
    print(json.dumps({k: v for k, v in result.items() if k not in ['jobs', 'pin']}, indent=2), flush=True)


if __name__ == '__main__':
    main()
