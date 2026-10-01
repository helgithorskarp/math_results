"""Serial capped reproduction of the 26 run and three signed refutations."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import urllib.request

from audit import audit_cover
from sign_audit import audit_all as audit_signs
from check_rup_lrat import verify

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--resume', action='store_true')
    ap.add_argument('--drat-source', type=Path)
    args = ap.parse_args()
    began = time.monotonic()
    work = args.work.resolve()
    expected = json.loads((ROOT/'expected.json').read_text())
    stems = [f'run-{i}' for i in range(7, 33)]+['anti', 'one-opposed-pair', 'one-agreed-pair']
    require([c['stem'] for c in expected['proof_cases']] == stems, 'incomplete expected proof cover')
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
               MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    pins = {p.name: sha(p) for p in ROOT.iterdir()
            if p.is_file() and p.suffix in ('.py', '.json', '.txt')}
    require(pins['check_rup_lrat.py'] == expected['reused_checker']['sha256'], 'changed reused checker')
    if args.resume:
        require((work/'pins.json').is_file(), 'no input checkpoint')
        require(json.loads((work/'pins.json').read_text()) == pins, 'source pins changed')
    else:
        require(not work.exists() or not any(work.iterdir()), 'use a fresh work directory')
        work.mkdir(parents=True, exist_ok=True)
        (work/'pins.json').write_text(json.dumps(pins, sort_keys=True, indent=2)+'\n')
    timings = {}

    def run(label, command, limit=30):
        start = time.monotonic()
        try:
            result = subprocess.run(list(map(str, command)), env=env,
                                    capture_output=True, text=True, timeout=limit)
        except subprocess.TimeoutExpired as error:
            raise ValueError(f'{label}: timeout; no mathematical exclusion') from error
        timings[label] = time.monotonic()-start
        require(result.returncode == 0,
                f'{label}: failed; no mathematical exclusion: {result.stderr[-2000:]}')
        return result.stdout

    # Encode the full reduction, including open cases. Only L>=7 is refuted.
    for length in range(2, 33):
        run(f'encode_run_{length}', [sys.executable, ROOT/'encode.py',
            work/f'run-{length}.cnf', '--length', length])
    for case in ('anti', 'one-opposed-pair', 'one-agreed-pair'):
        run('encode_'+case, [sys.executable, ROOT/'sign_encode.py',
            work/(case+'.cnf'), '--case', case])
    audits = {'runs': json.loads(json.dumps(audit_cover(work))), 'signs': audit_signs(work)}
    optimized_audits = {
        'runs': json.loads(run('optimized_run_audit', [sys.executable, '-O', ROOT/'audit.py', work])),
        'signs': json.loads(run('optimized_sign_audit', [sys.executable, '-O', ROOT/'sign_audit.py', work]))}
    require(audits == optimized_audits, 'optimized mathematical audits differ')
    require(audits['runs'] == expected['run_audit'], 'run model or coverage changed')
    require(audits['signs'] == expected['signed_audit'], 'signed models or coverage changed')
    source = work/'drat-trim.c'
    if args.drat_source:
        source.write_bytes(args.drat_source.read_bytes())
    elif not source.exists():
        source.write_bytes(urllib.request.urlopen(expected['converter']['url'], timeout=20).read())
    require(sha(source) == expected['converter']['sha256'], 'unrecognized converter source')
    converter = work/'drat-trim'
    run('compile_converter', ['gcc', '-O2', '-std=gnu99', source, '-o', converter])
    checked = []
    for reference in expected['proof_cases']:
        stem = reference['stem']
        cnf = work/(stem+'.cnf')
        require(sha(cnf) == reference['cnf_sha256'], 'different exact proof instance')
        drat, lrat, solved = (work/(stem+s) for s in ('.drat', '.lrat', '.solve.json'))
        if args.resume and solved.exists():
            record = json.loads(solved.read_text())
            require(record['status'] == 'UNSAT_PENDING_CHECK' and record['cnf_sha256'] == sha(cnf),
                    'incomplete solver checkpoint')
            require(drat.exists() and record['drat_sha256'] == sha(drat), 'incomplete proof checkpoint')
        else:
            require(not drat.exists(), 'unmarked partial solver trace; use a fresh stem')
            record = json.loads(run('solve_'+stem, [sys.executable, ROOT/'solve.py', cnf]))
            require(record['status'] == 'UNSAT_PENDING_CHECK', 'no complete candidate proof')
        converted = work/(stem+'.conversion.complete.json')
        if args.resume and converted.exists():
            require(lrat.exists(), 'missing converted proof')
            require(json.loads(converted.read_text()) == {'drat_sha256': sha(drat), 'lrat_sha256': sha(lrat)},
                    'changed converted trace')
        else:
            require(not lrat.exists(), 'unmarked partial conversion; use a fresh stem')
            output = run('convert_'+stem, [converter, cnf, drat, '-t', 25, '-L', lrat])
            require('s VERIFIED' in output, 'conversion unsuccessful')
            converted.write_text(json.dumps({'drat_sha256': sha(drat), 'lrat_sha256': sha(lrat)}, indent=2)+'\n')
        exact = verify(cnf, lrat)
        optimized = json.loads(run('optimized_replay_'+stem,
                                   [sys.executable, '-O', ROOT/'check_rup_lrat.py', cnf, lrat]))
        require(all(exact[k] == optimized[k] for k in exact), 'optimized proof checker differs')
        checked.append({'stem': stem, 'solve': record, 'RUP': exact,
                        'reference_RUP_byte_match': exact['proof_sha256'] == reference['proof_sha256']})
        (work/'checked-cases.json').write_text(json.dumps(checked, sort_keys=True, indent=2)+'\n')
        print(json.dumps({'case': stem, 'status': 'EXACT_REFUTATION_REPLAYED',
                          'additions': exact['checked_additions']}), flush=True)
    require([c['stem'] for c in checked] == stems, 'incomplete required proof cover')
    command = [ROOT/'controls.py', work/'run-7.cnf', work/'run-7.lrat',
               '--signed-cnf', work/'anti.cnf']
    controls = json.loads(run('controls', [sys.executable]+command+['--work', work/'controls']))
    optimized_controls = json.loads(run('optimized_controls',
        [sys.executable, '-O']+command+['--work', work/'controls-O']))
    require(controls == optimized_controls, 'optimized corruption controls differ')
    incomplete = work/'one-conflict.cnf'
    if args.resume and incomplete.with_suffix('.solve.json').exists():
        limited = json.loads(incomplete.with_suffix('.solve.json').read_text())
        require(limited['cnf_sha256'] == sha(work/'run-7.cnf'), 'changed budget-control input')
    else:
        incomplete.write_bytes((work/'run-7.cnf').read_bytes())
        limited = json.loads(run('one_conflict_control',
            [sys.executable, ROOT/'solve.py', incomplete, '--conflicts', 1]))
    require(limited['status'] == 'UNKNOWN', 'one-conflict control did not stop')
    require(not incomplete.with_suffix('.drat').exists(), 'incomplete solver emitted exclusion trace')
    result = {'agent': 'six-vdw-2', 'role': 'researcher', 'status': expected['status'],
              'maximum_log_run': 6, 'non_QR_antipodal_phase_bounds': [2, 42],
              'unresolved_run_cases': [2, 3, 4, 5, 6], 'family_exclusion': False,
              'audits': audits, 'checked_cases': checked, 'controls': controls,
              'one_conflict_UNKNOWN': True, 'threads': 1, 'CPU_jobs_at_once': 1,
              'seconds': time.monotonic()-began, 'stage_seconds': timings,
              'maxrss_parent_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'maxrss_child_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'Python': sys.version, 'source_pins': pins}
    (work/'result.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items()
                     if k not in ('checked_cases', 'source_pins', 'stage_seconds', 'audits')}, sort_keys=True))


if __name__ == '__main__':
    main()
