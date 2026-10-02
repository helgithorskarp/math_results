"""Fresh sequential model/proof reconstruction with fixed per-child guards."""
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


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--solver', type=Path, required=True)
    p.add_argument('--converter', type=Path, required=True)
    p.add_argument('--barrier-root', type=Path)
    a = p.parse_args()
    work = a.work.resolve()
    require(not work.exists(), 'fresh private work directory')
    pins = json.loads((HERE / 'SOURCE_PINS.json').read_text())
    require(set(pins) == {f.name for f in HERE.iterdir() if f.is_file() and f.name != 'SOURCE_PINS.json'},
            'complete compact-source inventory')
    for name, expected in pins.items():
        require(digest(HERE / name) == expected, 'pinned source changed: ' + name)
    expected = json.loads((HERE / 'EXPECTED.json').read_text())
    env = dict(os.environ)
    for k in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        env[k] = '1'
    records = []
    results = {}
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
        r = {'stage': name, 'seconds': time.monotonic() - began, 'returncode': child.returncode,
             'timeout': timeout, 'outer_seconds_guard': 35,
             'peak_child_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
        records.append(r)
        (work / 'progress.json').write_text(json.dumps(records, indent=2) + '\n')
        print(json.dumps(r, sort_keys=True), flush=True)
        require(not timeout and child.returncode == 0, 'incomplete stage; no exclusion: ' + name)
        if json_output:
            value = json.loads(stdout)
            (work / (name + '.json')).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
            results[name] = value
            return value

    def py(name, filename, *args, optimized=False):
        return stage(name, [sys.executable] + (['-O'] if optimized else []) +
                     ['-B', str(HERE / filename)] + [str(x) for x in args])

    model = work / 'regular-model.json'
    cnf = model.with_suffix('.cnf')
    census = work / 'field-columns.json'
    require(py('model', 'model.py', model) == expected['model'], 'whole generator result')
    require(digest(model) == expected['model_sha256'], 'canonical model bytes')
    require(py('field-census', 'field_columns.py', census) == expected['field_census'], 'whole field census')
    require(digest(census) == expected['field_census_sha256'], 'whole census bytes')
    for optimized, suffix in [(False, 'normal'), (True, 'optimized')]:
        require(py('definition-' + suffix, 'check_model.py', model, optimized=optimized) == expected['definition'],
                'whole independent definition audit')
        require(py('physical-controls-' + suffix, 'controls.py', model, census, optimized=optimized) == expected['physical_controls'],
                'whole physical controls')
        require(py('normalization-' + suffix, 'normalization.py', model, optimized=optimized) == expected['normalization'],
                'whole CRT transfer audit')
    (work / 'AUDITED_INPUTS.json').write_text(json.dumps({
        'status': 'FROZEN_H3_FULL_DEFINITION_CONTROLS_AND_NORMALIZATION_BEFORE_NATIVE',
        'source_pins_sha256': digest(HERE / 'SOURCE_PINS.json'), 'model_sha256': digest(model),
        'cnf_sha256': digest(cnf), 'field_census_sha256': digest(census)}, indent=2, sort_keys=True) + '\n')
    proposal = work / 'proposal.json'
    native = py('native', 'candidate.py', model, proposal, '--solver', a.solver.resolve())
    require(native['status'] == 'UNVERIFIED_UNSAT_PROPOSAL' and native['statistics']['conflicts'] <= 49900,
            'bounded UNSAT candidate required; UNKNOWN/SAT/incomplete proves no exclusion')
    require(native['cnf_sha256'] == expected['strict_proof']['cnf_sha256'], 'canonical CNF bytes')
    require(native['native_ascii_sha256'] == expected['native_ascii_sha256'], 'canonical native trace bytes')
    lrat = work / 'proof.lrat'
    stage('convert', [str(a.converter.resolve()), str(cnf), str(proposal.with_suffix('.drup')),
                      '-t', '20', '-L', str(lrat)], json_output=False)
    for optimized, suffix in [(False, 'normal'), (True, 'optimized')]:
        proof = py('proof-' + suffix, 'strict_rup.py', cnf, lrat, optimized=optimized)
        proof.pop('seconds')
        require(proof == expected['strict_proof'], 'whole exact positive-only proof result')
        require(py('proof-controls-' + suffix, 'proof_controls.py', cnf, lrat,
                   work / ('proof-controls-' + suffix), optimized=optimized) == expected['proof_controls'],
                'whole strict proof controls')
    for name, pinned in pins.items():
        require(digest(HERE / name) == pinned, 'source changed during replay')
    result = {'author': 'six-vdw-1', 'role': 'researcher',
              'status': 'COMPLETE_H3_ANY_COSET_ORBIT16_EXCLUSION_REPRODUCED',
              'source_pins_sha256': digest(HERE / 'SOURCE_PINS.json'),
              'model_sha256': digest(model), 'cnf_sha256': digest(cnf), 'proof_sha256': digest(lrat),
              'normal_optimized_whole_results_agree': True, 'forbidden_local_row_masks': 160,
              'remaining_local_row_masks': 420, 'cosets_covered': 10,
              'seconds': time.monotonic() - started, 'records': records,
              'scope': 'Chosen H3-invariant regular cyclic period620 family only; no W bound or interval witness.'}
    (work / 'REPRODUCTION.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
