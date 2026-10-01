"""Regenerate the omitted proof locally, then check every positive RUP hint."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

SOURCE = Path(__file__).resolve().parent
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
           NUMEXPR_NUM_THREADS='1', PYTHONOPTIMIZE='0')


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    directory = args.output_dir.resolve()
    require(not directory.exists(), 'Existing reproduction directory')
    directory.mkdir(parents=True)
    began = time.monotonic()
    expected = json.loads((SOURCE / 'expected.json').read_text())
    require(importlib.metadata.version('python-sat') == expected['python_sat'], 'Pinned Python-SAT version required')
    names = ['build_instance.py', 'solve.py', 'verify_encoding.py', 'check_positive_lrat.py',
             'controls_positive_lrat.py', 'drat-trim.c', Path(__file__).name, 'expected.json',
             'base3704.bits', 'AP-pool.json', 'requirements.txt', 'UPSTREAM-LICENSE']
    pin = {'sources': {n: sha(SOURCE / n) for n in names}, 'source': str(SOURCE),
           'python': sys.version, 'python_sat': importlib.metadata.version('python-sat'),
           'max_child_seconds': 30, 'native_proof_seconds': 20, 'case_cap': 200000,
           'threads': 1, 'simultaneous_CPU_jobs': 1, 'private_proof_inputs': False,
           'proof_generated_locally_then_checked': True}
    save(directory / 'pin.json', pin)
    jobs, journal = [], {'status': 'PARTIAL_SOURCE_REPRODUCTION_NO_FAMILY_EXCLUSION', 'jobs': {}}

    def child(name, command, output=None, reject_reason=None):
        require(output is None or not output.exists(), 'Existing child result')
        journal['jobs'][name] = {'status': 'STARTED', 'command': command}
        save(directory / 'journal.json', journal)
        process, started = None, time.monotonic()
        try:
            process = subprocess.Popen(command, env=ENV, text=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, start_new_session=True)
            stdout, stderr = process.communicate(timeout=30)
            require((process.returncode != 0 and reject_reason in stderr) if reject_reason else process.returncode == 0,
                    'Unexpected child result: ' + stderr[-2000:] + stdout[-1000:])
        except BaseException as error:
            if process is not None and process.poll() is None:
                os.killpg(process.pid, signal.SIGKILL)
                process.communicate()
            journal['status'] = 'STOPPED_OPERATIONAL_FAILURE_OR_INVALID_PROOF_NO_EXCLUSION'
            journal['jobs'][name].update(status='FAILED_OR_INCOMPLETE', error=str(error))
            save(directory / 'journal.json', journal)
            raise
        elapsed = time.monotonic() - started
        data = json.loads(output.read_text()) if output is not None and not reject_reason else None
        if data is not None:
            cases = data.get('conservative_combined_cases', data.get('proof_obligation_cases', 17))
            require(cases <= 200000 and data['seconds'] < 30, 'Child case/time guard')
        else:
            cases = 0
        job = {'status': 'COMPLETED', 'name': name, 'command': command, 'wall_seconds': elapsed,
               'cases': cases, 'maxrss_kib': data.get('maxrss_kib') if data else None,
               'output': str(output) if output is not None else None,
               'sha256': sha(output) if output is not None and not reject_reason else None,
               'expected_corruption_rejection': reject_reason}
        journal['jobs'][name] = job
        save(directory / 'journal.json', journal)
        jobs.append(job)
        return data, stdout

    model = directory / 'model'
    metadata, _ = child('build', [sys.executable, str(SOURCE / 'build_instance.py'), '--output-dir', str(model)], model / 'metadata.json')
    require(metadata['CNF_sha256'] == expected['CNF_sha256'], 'Actual canonical CNF differs')
    for mode in [0, 1]:
        output = directory / f'encoding-mode{mode}.json'
        audit, _ = child(f'encoding-mode{mode}', [sys.executable] + (['-O'] if mode else []) +
                         [str(SOURCE / 'verify_encoding.py'), '--model-dir', str(model), '--output', str(output)], output)
        require(audit['clause_multiset_match'] and audit['base_formula_verified'] and audit['interpreter_optimization'] == mode,
                'Literal encoding audit incomplete')
    native, _ = child('untrusted-proof-proposal', [sys.executable, str(SOURCE / 'solve.py'), '--model-dir', str(model)], model / 'solver.json')
    require(native['status'] == 'UNSAT_UNCHECKED_PROOF_NO_FAMILY_EXCLUSION', 'No bounded proof proposal; no exclusion claimed')
    require(native['reported_conflict_budget_respected'], 'Conflict cap exceeded')
    require(metadata['clauses'] + native['proof_lines'] <= 200000, 'Input clause/proof-step cap')
    tool = directory / 'drat-trim'
    child('compile-proof-transformer', ['cc', '-O2', str(SOURCE / 'drat-trim.c'), '-o', str(tool)])
    lrat = directory / 'proof.lrat'
    _, stdout = child('convert-proof-to-positive-hints', [str(tool), str(model / 'instance.cnf'),
                       native['unchecked_proof'], '-L', str(lrat), '-t', '20'])
    require('s VERIFIED' in stdout and '0 RAT lemmas in core' in stdout, 'No positive-hint proof produced')
    proof_checks = []
    for mode in [0, 1]:
        output = directory / f'RUP-mode{mode}.json'
        check, _ = child(f'RUP-mode{mode}', [sys.executable] + (['-O'] if mode else []) +
                         [str(SOURCE / 'check_positive_lrat.py'), '--CNF', str(model / 'instance.cnf'), '--LRAT', str(lrat),
                          '--output', str(output)], output)
        require(check['status'] == 'ALL_POSITIVE_RUP_HINTS_VERIFIED_AND_EMPTY_CLAUSE_DERIVED'
                and check['CNF_sha256'] == expected['CNF_sha256'] and check['interpreter_optimization'] == mode,
                'Exact proof check incomplete')
        proof_checks.append(check)
        control_dir = directory / f'RUP-controls-mode{mode}'
        control, _ = child(f'RUP-controls-mode{mode}', [sys.executable] + (['-O'] if mode else []) +
                           [str(SOURCE / 'controls_positive_lrat.py'), '--output-dir', str(control_dir)], control_dir / 'result.json')
        require(control['status'] == 'TWO_POSITIVE_CERTIFICATES_AND_FIFTEEN_EXACT_RUP_CORRUPTIONS_VERIFIED', 'Proof controls incomplete')
    require(proof_checks[0]['hint_clause_reads'] == proof_checks[1]['hint_clause_reads'], 'Optimization changes proof coverage')
    # Alter actual clauses and an AP definition while updating file hashes, so
    # these fixtures test mathematics rather than merely a stale hash guard.
    for name, reason in [('wrong_start_clause', 'Literal clause multiset differs'),
                         ('extra_axiom', 'Exact independently derived header'),
                         ('boolean_AP', 'Positive actual APs')]:
        corrupt_dir = directory / ('encoding-control-' + name)
        corrupt_dir.mkdir()
        meta = dict(metadata)
        if name == 'boolean_AP':
            pool = json.loads((SOURCE / 'AP-pool.json').read_text())
            pool['APs'][0][0] = True
            pool_path = corrupt_dir / 'AP-pool.json'
            save(pool_path, pool)
            meta.update(AP_pool=str(pool_path), AP_pool_sha256=sha(pool_path))
        else:
            rows = (model / 'instance.cnf').read_text().splitlines()
            if name == 'wrong_start_clause':
                rows[1] = '-3705 -1 0'
            else:
                header = rows[0].split()
                header[3] = str(int(header[3]) + 1)
                rows[0] = ' '.join(header)
                rows.append('1 0')
            target = corrupt_dir / 'instance.cnf'
            target.write_text('\n'.join(rows) + '\n')
            meta.update(CNF=str(target), CNF_sha256=sha(target))
        save(corrupt_dir / 'metadata.json', meta)
        for mode in [0, 1]:
            output = corrupt_dir / f'rejected-mode{mode}.json'
            child(f'encoding-control-{name}-mode{mode}', [sys.executable] + (['-O'] if mode else []) +
                  [str(SOURCE / 'verify_encoding.py'), '--model-dir', str(corrupt_dir), '--output', str(output)], output, reason)
    result = {'agent': 'six-vdw-1', 'role': 'researcher', 'completed_at': datetime.now(timezone.utc).isoformat(),
              'status': expected['status'], 'pin': pin, 'jobs': jobs, 'successful_jobs': len(jobs),
              'private_proof_inputs': False, 'proof_generated_locally': True,
              'CNF_sha256': sha(model / 'instance.cnf'), 'DRAT_sha256': sha(native['unchecked_proof']), 'LRAT_sha256': sha(lrat),
              'reference_proof_hashes_match': sha(native['unchecked_proof']) == expected['reference_DRAT_sha256']
              and sha(lrat) == expected['reference_LRAT_sha256'], 'proof_checks': proof_checks,
              'two_run_masks': expected['two_run_masks'], 'atmost_two_run_masks': expected['atmost_two_run_masks'],
              'minimum_disagreement_runs_if_AP_free': 3, 'minimum_agreement_runs_if_AP_free': 3,
              'minimum_match_edit_transitions_if_AP_free': 5, 'new_W_bound': None,
              'seconds_total': time.monotonic() - began, 'longest_child_seconds': max(j['wall_seconds'] for j in jobs),
              'maximum_child_cases': max(j['cases'] for j in jobs),
              'max_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'mathematical_corruptions': 36, 'positive_small_proof_checks': 4,
              'trust_boundary': 'Written run/counter/AP reduction and strict Python integer positive-hint RUP checker. Native solver and transformer propose evidence.'}
    require(len(jobs) == 16, 'Required source checks omitted')
    save(directory / 'result.json', result)
    journal['status'] = result['status']
    save(directory / 'journal.json', journal)
    print(json.dumps({k: v for k, v in result.items() if k not in ['pin', 'jobs', 'proof_checks']}, indent=2), flush=True)


if __name__ == '__main__':
    main()
