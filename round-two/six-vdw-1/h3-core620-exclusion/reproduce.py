"""Fresh full six-case reconstruction; each serial child retains the 35s guard."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPS = [8, 10, 12, 20, 34, 72]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', required=True, type=Path)
    p.add_argument('--solver', required=True, type=Path)
    p.add_argument('--converter', required=True, type=Path)
    p.add_argument('--barrier-root', type=Path)
    a = p.parse_args()
    work = a.work.resolve()
    require(not work.exists(), 'fresh private work directory')
    pins = json.loads((HERE / 'SOURCE_PINS.json').read_text())
    require(set(pins) == {f.name for f in HERE.iterdir() if f.is_file() and f.name != 'SOURCE_PINS.json'},
            'complete compact-source inventory')
    for name, value in pins.items():
        require(digest(HERE / name) == value, 'changed source: ' + name)
    expected = json.loads((HERE / 'EXPECTED.json').read_text())
    env = dict(os.environ)
    for k in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        env[k] = '1'
    records = []
    started = time.monotonic()

    def barrier():
        if a.barrier_root:
            require(not any((a.barrier_root / n).exists() for n in
                            ['PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json', 'STOP', 'STOP.json']),
                    'operations barrier')
        require(not (work / 'STOP').exists(), 'local stop barrier')

    barrier()
    work.mkdir(parents=True)

    def stage(name, command, json_output=True):
        barrier()
        began = time.monotonic()
        child = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 text=True, start_new_session=True, env=env)
        timeout = False
        try:
            stdout, stderr = child.communicate(timeout=35)
        except subprocess.TimeoutExpired:
            timeout = True
            os.killpg(child.pid, signal.SIGKILL)
            stdout, stderr = child.communicate()
        (work / (name + '.stdout')).write_text(stdout)
        (work / (name + '.stderr')).write_text(stderr)
        r = {'stage': name, 'seconds': time.monotonic() - began,
             'returncode': child.returncode, 'timeout': timeout, 'outer_seconds_guard': 35,
             'peak_child_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
        records.append(r)
        (work / 'progress.json').write_text(json.dumps(records, indent=2) + '\n')
        print(json.dumps(r, sort_keys=True), flush=True)
        require(not timeout and child.returncode == 0, 'incomplete stage; no exclusion: ' + name)
        if json_output:
            value = json.loads(stdout)
            destination=work/(name+'.json')
            require(not destination.exists(),'preserve an existing child artifact: '+name)
            destination.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')
            return value

    def py(name, filename, *args, optimized=False):
        return stage(name, [sys.executable] + (['-O'] if optimized else []) +
                     ['-B', str(HERE / filename)] + [str(x) for x in args])

    models = work / 'models'
    require(py('models', 'model.py', models) == expected['generator'], 'whole six-case generator result')
    for rep in REPS:
        require(digest(models / ('row' + str(rep) + '.json')) == expected['cases'][str(rep)]['model_sha256'],
                'canonical actual model bytes')
        require(digest(models / ('row' + str(rep) + '.cnf')) == expected['cases'][str(rep)]['strict_proof']['cnf_sha256'],
                'canonical whole DIMACS bytes')
    for optimized, suffix in [(False, 'normal'), (True, 'optimized')]:
        for rep in REPS:
            require(py('definition' + str(rep) + '-' + suffix, 'audit.py',
                       models / ('row' + str(rep) + '.json'), rep, optimized=optimized) ==
                    expected['cases'][str(rep)]['definition'], 'whole independent physical definition')
        for part in ['tiny', 'damages-first', 'damages-second']:
            require(py('controls-' + part + '-' + suffix, 'controls.py', models / 'row34.json',
                       part, optimized=optimized) == expected['physical_controls'][part],
                    'whole positive/damaged definition controls')
        cover = work / ('normalization-cover-' + suffix + '.json')
        require(py('cover-' + suffix, 'cover.py', models / 'row34.json', cover,
                   optimized=optimized) == expected['cover'], 'whole preserving six-case cover result')
        require(digest(cover) == expected['cover_sha256'], 'whole physical normalization cover bytes')
    frozen = {'status': 'FROZEN_ALL_SIX_H3_REMAINING_CASES_AND_COMPLETE_COVER_BEFORE_NATIVE',
              'source_pins_sha256': digest(HERE / 'SOURCE_PINS.json'),
              'model_sha256': {str(r): digest(models / ('row' + str(r) + '.json')) for r in REPS},
              'cnf_sha256': {str(r): digest(models / ('row' + str(r) + '.cnf')) for r in REPS}}
    (work / 'AUDITED_INPUTS.json').write_text(json.dumps(frozen, sort_keys=True, indent=2) + '\n')
    for rep in REPS:
        for name, value in pins.items():
            require(digest(HERE / name) == value, 'source changed before native proposal')
        model = models / ('row' + str(rep) + '.json')
        cnf = model.with_suffix('.cnf')
        e = expected['cases'][str(rep)]
        proposal = work / ('proposal' + str(rep) + '.json')
        native = py('native' + str(rep), 'candidate.py', model, proposal,
                    '--solver', a.solver.resolve(), '--first-row', rep)
        require(native['status'] == 'UNVERIFIED_UNSAT_PROPOSAL' and native['statistics']['conflicts'] <= 49900,
                'bounded complete proposal required; incomplete result proves no exclusion')
        require(native['native_ascii_sha256'] == e['native_ascii_sha256'], 'canonical native trace')
        lrat = work / ('proof' + str(rep) + '.lrat')
        stage('convert' + str(rep), [str(a.converter.resolve()), str(cnf),
                                   str(proposal.with_suffix('.drup')), '-t', '20', '-L', str(lrat)],
              json_output=False)
        for optimized, suffix in [(False, 'normal'), (True, 'optimized')]:
            proof = py('proof' + str(rep) + '-' + suffix, 'strict_rup.py', cnf, lrat, optimized=optimized)
            proof.pop('seconds')
            require(proof == e['strict_proof'], 'whole exact positive-only RUP result')
            require(py('proof-controls' + str(rep) + '-' + suffix, 'proof_controls.py', cnf, lrat,
                       work / ('proof-controls' + str(rep) + '-' + suffix), optimized=optimized) ==
                    expected['proof_controls'], 'whole strict proof damage controls')
    for name, value in pins.items():
        require(digest(HERE / name) == value, 'source changed during reconstruction')
    result = {'author': 'six-vdw-1', 'role': 'researcher',
              'status': 'COMPLETE_H3_REGULAR620_NONEXISTENCE_REPRODUCED',
              'premise': expected['premise'], 'remaining_case_representatives': REPS,
              'source_pins_sha256': digest(HERE / 'SOURCE_PINS.json'),
              'normal_optimized_whole_results_agree': True,
              'seconds': time.monotonic() - started, 'records': records,
              'scope': 'No AP7-free H3={1,5,25}-invariant antipodal regular cyclic620 core exists; '
                       'conditional on previously proved orbit16 lemma. No arbitrary-core or W bound.'}
    (work / 'REPRODUCTION.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
