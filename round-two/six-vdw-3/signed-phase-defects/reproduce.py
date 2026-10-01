#!/usr/bin/env python3
"""Regenerate the compact one-exception proof; independently audit and replay.

All computations are sequential and one-thread. Generated proof corpora and
pinned external source stay in the chosen work directory, outside publication.
"""
import argparse
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import urllib.request


ROOT = Path(__file__).resolve().parent
EXPECTED = json.loads((ROOT/'expected.json').read_text())
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
           MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, seconds=45):
    result = subprocess.run(list(map(str, argv)), text=True, capture_output=True,
                            env=ENV, timeout=seconds)
    require(result.returncode == 0, 'Child failed: '+result.stderr+result.stdout)
    return result.stdout


def pinned_source(info, output):
    if output.exists():
        data = output.read_bytes()
    else:
        data = urllib.request.urlopen(info['url'], timeout=20).read()
    require(hashlib.sha256(data).hexdigest() == info['sha256'], 'Pinned source differs: '+info['url'])
    output.write_bytes(data)


def solve(work, conflicts):
    import pysat
    from pysat.solvers import Solver
    require(pysat.__version__ == EXPECTED['solver']['python_sat_version'], 'Unpinned solver package')
    cnf = work/'model.cnf'
    require(sha(cnf) == EXPECTED['model']['model_sha256'], 'Solver model hash differs')
    clauses = [list(map(int, row.split()[:-1])) for row in cnf.read_text().splitlines()[1:]]
    start = time.monotonic()
    with Solver(name='cadical195', bootstrap_with=clauses, with_proof=True) as solver:
        solver.conf_budget(conflicts)
        status = solver.solve_limited()
        stats = solver.accum_stats()
        if status is False:
            libc = ctypes.CDLL(None)
            libc.fflush.argtypes = [ctypes.c_void_p]
            libc.fflush.restype = ctypes.c_int
            require(libc.fflush(None) == 0, 'Proof stream flush failed')
            (work/'trace.drat').write_text('\n'.join(solver.get_proof())+'\n')
    if conflicts == 1:
        require(status is None, 'One-conflict control must remain UNKNOWN')
    else:
        require(status is False, 'No finished refutation: SAT/UNKNOWN cannot support this exclusion')
    print(json.dumps({'status': 'UNKNOWN' if status is None else 'UNSAT_PENDING_CHECK',
                      'conflict_budget': conflicts, 'stats': stats,
                      'seconds': time.monotonic()-start, 'mathematical_exclusion': False}))


def checker_module(path):
    spec = importlib.util.spec_from_file_location('published_positive_RUP_checker', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def checker_controls(module, work):
    cnf, proof = work/'tiny.cnf', work/'tiny.lrat'
    cnf.write_text('p cnf 2 3\n1 2 0\n-1 0\n-2 0\n')
    proof.write_text('4 0 2 3 1 0\n')
    require(module.verify(cnf, proof)['mathematical_exclusion'], 'Valid tiny refutation rejected')
    invalid = ['4 1 0 3 1 0\n',  # valid nonempty addition, missing empty clause
               '4 0 -1 2 0\n', '4 3 0 1 0\n', '4 0 99 0\n',
               '4 0 2 3 1\n', '4 0 1 0\n',
               '4 d 2 0\n5 0 2 3 1 0\n', '3 0 2 3 1 0\n']
    for text in invalid:
        proof.write_text(text)
        try:
            module.verify(cnf, proof)
        except (ValueError, KeyError, IndexError):
            pass
        else:
            raise ValueError('Invalid tiny refutation accepted')
    cnf.unlink()
    proof.unlink()
    return len(invalid)


def production_controls(module, work):
    lines = (work/'trace.lrat').read_text().splitlines()
    damaged = lines.copy()
    for i, row in enumerate(damaged):
        tokens = row.split()
        if tokens[1] not in ('d', '0'):
            tokens[1] = str(EXPECTED['model']['variables']+1)
            damaged[i] = ' '.join(tokens)
            break
    else:
        raise ValueError('Production proof has no nonempty addition')
    cases = ['\n'.join(damaged)+'\n',
             '\n'.join(row for row in lines if row.split()[1] != '0')+'\n']
    target = work/'corrupted.lrat'
    for text in cases:
        target.write_text(text)
        try:
            module.verify(work/'model.cnf', target)
        except (ValueError, KeyError, IndexError):
            pass
        else:
            raise ValueError('Corrupted production proof accepted')
    target.unlink()
    return len(cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workdir', type=Path, default=ROOT/'build')
    parser.add_argument('--solve', action='store_true')
    parser.add_argument('--conflicts', type=int, choices=(1, 200000), default=200000)
    args = parser.parse_args()
    work = args.workdir.resolve()
    work.mkdir(exist_ok=True, parents=True)
    if args.solve:
        solve(work, args.conflicts)
        return
    start = time.monotonic()
    sources = EXPECTED['sources']
    base, checker, converter = work/'published-cut-generate.py', work/'published-rup-checker.py', work/'drat-trim.c'
    for key, target in [('cut_generator', base), ('RUP_checker', checker), ('drat_converter', converter)]:
        pinned_source(sources[key], target)
    metadata = json.loads(run([sys.executable, ROOT/'generate.py', '--base-source', base,
                               '--output', work/'model.cnf']))
    require(metadata['sha256'] == EXPECTED['model']['model_sha256'], 'Generator model differs')
    audit_results = []
    for flags in ([], ['-O']):
        audit = json.loads(run([sys.executable, *flags, ROOT/'check.py', work/'model.cnf',
                                '--controls', '--output', work/('audit'+('O' if flags else '')+'.json')]))
        require(audit == EXPECTED['audit'], 'Independent full audit differs')
        audit_results.append(audit['status'])
    print('COMPLETE_NORMAL_AND_OPTIMIZED_MODEL_AUDITS', flush=True)
    run(['gcc', '-O2', '-std=gnu99', converter, '-o', work/'drat-trim'])
    solver = json.loads(run([sys.executable, Path(__file__).resolve(), '--workdir', work, '--solve']))
    require(solver['status'] == 'UNSAT_PENDING_CHECK', 'Incomplete solver result')
    print('SOLVER_TRACE_PENDING_REPLAY', flush=True)
    conversion = run([work/'drat-trim', work/'model.cnf', work/'trace.drat', '-t', '35',
                      '-L', work/'trace.lrat'])
    (work/'conversion.log').write_text(conversion)
    require('VERIFIED' in conversion, 'Untrusted conversion did not finish')
    proof_results = []
    for flags in ([], ['-O']):
        proof = json.loads(run([sys.executable, *flags, checker, work/'model.cnf', work/'trace.lrat']))
        proof.pop('seconds', None)
        require(proof == EXPECTED['proof'], 'Exact checked proof/reference differs')
        proof_results.append(proof)
    print('EXACT_NORMAL_AND_OPTIMIZED_RUP_REPLAYS', flush=True)
    module = checker_module(checker)
    tiny = checker_controls(module, work)
    damaged = production_controls(module, work)
    unknown = json.loads(run([sys.executable, Path(__file__).resolve(), '--workdir', work,
                              '--solve', '--conflicts', '1']))
    require(unknown['status'] == 'UNKNOWN', 'Incomplete-search control changed')
    summary = {'agent': 'six-vdw-3', 'role': 'researcher',
               'status': 'VERIFIED_ONE_EXCEPTION_EXCLUSION_AND_SIGNED_DEFECT_REDUCTION',
               'model': EXPECTED['model'], 'audit_statuses': audit_results,
               'proof': proof_results[0], 'optimized_proof_replay': True,
               'generic_proof_corruptions_rejected': tiny,
               'production_proof_corruptions_rejected': damaged,
               'one_conflict_control_UNKNOWN': True, 'solver_discovery': solver,
               'seconds': time.monotonic()-start,
               'parent_peak_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               'child_peak_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'separable_103_family_excluded': False, 'new_W_bound': False}
    (work/'summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True)+'\n')
    print(json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    main()
