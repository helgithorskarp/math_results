"""Regenerate two exact103-bit exclusions and replay positive-RUP certificates.

All jobs are sequential, one thread, and bounded30seconds per child. Generated
CNFs, proof corpora and binaries stay in the ignored build directory.
"""
import argparse
import ctypes
import hashlib
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
DEPENDENCY = ROOT.parent/EXPECTED['dependency']['directory']
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
           MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


require(__debug__, 'Run without Python -O: exact assertion checks are required')
for name, info in EXPECTED['dependency']['files'].items():
    require(sha((DEPENDENCY/name).read_bytes()) == info['sha256'], 'Dependency bytes changed: '+name)
sys.path.insert(0, str(DEPENDENCY))
from check_coloring import cyclic_report, interval_report
from check_rup_lrat import verify
from encode import candidate, encoding, local_table, static_cost
from rup_controls import controls as rup_controls
from normalize import controls as normalization_controls, normalize_phase


def run(args, stdin=None, seconds=30):
    result = subprocess.run(list(map(str, args)), input=stdin, text=True,
                            capture_output=True, env=ENV, timeout=seconds)
    require(result.returncode == 0, 'Child failed: '+result.stderr)
    return result.stdout


def solve(case, build, conflicts):
    from pysat.solvers import Solver
    require(conflicts in [1, 50000], 'Unsupported bounded conflict budget')
    cases = json.loads((ROOT/'cases.json').read_text())
    u = list(map(int, cases['orientation_seed']))
    raw = (build/(case+'.cnf')).read_bytes()
    require(sha(raw) == EXPECTED['models'][case]['cnf_sha256'], 'Solver input hash mismatch')
    clauses = [list(map(int, line.split()[:-1])) for line in raw.decode().splitlines()[1:]]
    with Solver(name='cadical195', bootstrap_with=clauses, with_proof=True) as solver:
        solver.set_phases([(i+1)*(1 if bit else -1) for i, bit in enumerate(u)])
        solver.conf_budget(conflicts)
        status = solver.solve_limited()
        stats = solver.accum_stats()
        if status is False:
            libc = ctypes.CDLL(None)
            libc.fflush.argtypes = [ctypes.c_void_p]
            libc.fflush.restype = ctypes.c_int
            require(libc.fflush(None) == 0, 'Proof stream flush failed')
            trace = ('\n'.join(solver.get_proof())+'\n').encode()
        else:
            trace = None
    if conflicts == 1:
        require(status is None and trace is None, 'One-conflict control must remain UNKNOWN')
    else:
        require(status is False and trace is not None, 'No completed exclusion; UNKNOWN/SAT cannot replace checked proof')
        (build/(case+'.drat')).write_bytes(trace)
    print(json.dumps({'status': 'UNSAT_PENDING_PROOF' if status is False else 'UNKNOWN',
                      'conflict_budget': conflicts, 'stats': stats,
                      'mathematical_exclusion': False}))


def rejection_controls(build, case):
    cnf, original = build/(case+'.cnf'), build/(case+'.lrat')
    lines = original.read_text().splitlines()
    corruptions = []
    changed = lines.copy()
    for i, line in enumerate(changed):
        tokens = line.split()
        if tokens[1] != 'd' and tokens[1] != '0':
            tokens[1] = '104'
            changed[i] = ' '.join(tokens)
            break
    else:
        raise RuntimeError('No nonempty addition for corruption control')
    corruptions.append('\n'.join(changed)+'\n')
    corruptions.append('\n'.join(line for line in lines if line.split()[1] != '0')+'\n')
    path = build/(case+'-corrupt.lrat')
    for text in corruptions:
        path.write_text(text)
        try:
            verify(cnf, path)
        except (ValueError, KeyError, IndexError):
            pass
        else:
            raise RuntimeError('Corrupted production certificate accepted')
    path.unlink()
    return len(corruptions)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', type=Path, default=ROOT/'build')
    parser.add_argument('--drat-source', type=Path)
    parser.add_argument('--sanitize', action='store_true')
    parser.add_argument('--solve', choices=['same', 'mixed'])
    parser.add_argument('--conflicts', type=int, default=50000)
    args = parser.parse_args()
    build = args.build.resolve()
    build.mkdir(parents=True, exist_ok=True)
    if args.solve:
        solve(args.solve, build, args.conflicts)
        return
    start = time.monotonic()
    cases = json.loads((ROOT/'cases.json').read_text())
    norm = normalization_controls()
    require(norm['same_label_skeletons'] == norm['mixed_label_skeletons'] == 31518, 'Orbit cover changed')
    malformed = [[0]*102, [0]*103, [1]+[0]*102, [1, 1, 1]+[0]*100, [6, 1]+[0]*101, [0.5, 1]+[0]*101]
    for phi in malformed:
        try:
            normalize_phase(phi)
        except AssertionError:
            pass
        else:
            raise RuntimeError('Malformed/two-exception-domain input accepted')
    flags = ['-std=c++17', '-Wall', '-Wextra', '-Wconversion', '-Wshadow']
    flags += ['-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer'] if args.sanitize else ['-O2']
    run(['g++', *flags, DEPENDENCY/'direct_encode.cpp', '-o', build/'direct_encode'])
    converter_info = EXPECTED['drat_converter']['files']['drat-trim.c']
    converter_source = build/'drat-trim.c'
    data = args.drat_source.read_bytes() if args.drat_source else urllib.request.urlopen(converter_info['url'], timeout=15).read()
    require(sha(data) == converter_info['sha256'], 'Pinned converter source mismatch')
    converter_source.write_bytes(data)
    run(['gcc', '-O2', '-std=gnu99', converter_source, '-o', build/'drat-trim'])
    table, table_metadata = local_table()
    require(sha(table) == '70d4e42aec4b2426139f19f4b3cc999a0c2654db3b5f27ba72563cfe741fea67', 'Published local table changed')
    proof_results, model_results = {}, {}
    bad_proofs = 0
    for name, case in cases['fiber_cases'].items():
        tau = case['exception_labels']+[0]*101
        cnf, weighted, meta = encoding(tau)
        require(sha(cnf) == EXPECTED['models'][name]['cnf_sha256'], 'CNF reference hash mismatch')
        require(sha(weighted) == EXPECTED['models'][name]['weighted_sha256'], 'Weight reference hash mismatch')
        require(meta['nae_edges'] == EXPECTED['models'][name]['edges'], 'Exact sparse count mismatch')
        stdin = '103\n'+' '.join(map(str, tau))+'\n'
        for kind, expected_data in [('cnf', cnf), ('weighted', weighted)]:
            direct = run([build/'direct_encode', kind], stdin)
            require(direct.encode() == expected_data, 'Full cyclic/field complete encoding mismatch')
        (build/(name+'.cnf')).write_bytes(cnf)
        (build/(name+'.weighted')).write_bytes(weighted)
        solver_result = json.loads(run([sys.executable, Path(__file__).resolve(), '--build', build, '--solve', name]))
        require(solver_result['status'] == 'UNSAT_PENDING_PROOF', 'Solver result is not a completed trace')
        output = run([build/'drat-trim', build/(name+'.cnf'), build/(name+'.drat'), '-t', '30', '-L', build/(name+'.lrat')])
        require('VERIFIED' in output, 'Untrusted trace conversion did not complete')
        proof = verify(build/(name+'.cnf'), build/(name+'.lrat'))
        for k, value in EXPECTED['proofs'][name].items():
            require(proof[k] == value, 'Checked certificate/reference mismatch: '+k)
        proof['reference_proof_byte_match'] = True
        proof_results[name] = proof
        model_results[name] = {**meta, 'cnf_sha256': sha(cnf), 'weighted_sha256': sha(weighted)}
        bad_proofs += rejection_controls(build, name)
    unknown = json.loads(run([sys.executable, Path(__file__).resolve(), '--build', build, '--solve', 'same', '--conflicts', '1']))
    require(unknown['status'] == 'UNKNOWN', 'Budget control changed')
    generic_controls = rup_controls()
    phi = list(map(int, cases['construction_candidate']['phases']))
    tau, u = [v % 3 for v in phi], [v // 3 for v in phi]
    _, weighted, _ = encoding(tau)
    _, cost = static_cost(weighted, u)
    colors = candidate(tau, u)
    cyc = cyclic_report(colors)
    integer = interval_report([colors[i % 618] for i in range(3704)])
    require(cost == 594 and cyc['monochromatic_cyclic_pairs'] == 4*cost == 2376, 'Construction candidate objective mismatch')
    require(integer['monochromatic_interval_progressions'] == 7117 and not integer['verified'], 'Invalid candidate mismatch')
    summary = {'agent': 'six-vdw-1', 'role': 'researcher',
               'status': 'VERIFIED_ALL_TWO_EXCEPTION_CUTS', 'normalization': norm,
               'models': model_results, 'proofs': proof_results,
               'local_table_sha256': sha(table), 'malformed_normalization_rejections': len(malformed),
               'production_proof_rejections': bad_proofs, 'RUP_controls': generic_controls,
               'budget_control_UNKNOWN': True, 'construction_candidate':
               {'status': 'INVALID', 'static_cost': cost, 'cyclic_check': cyc, 'integer_check': integer},
               'product_excluded': False, 'one_exception_excluded': False,
               'length3704_witness': False, 'sanitizers': args.sanitize,
               'seconds': time.monotonic()-start,
               'peak_parent_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               'peak_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (build/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps({k: v for k, v in summary.items() if k not in ['normalization', 'models', 'proofs', 'construction_candidate']}, indent=2))


if __name__ == '__main__':
    main()
