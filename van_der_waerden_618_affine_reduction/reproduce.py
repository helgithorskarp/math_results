"""Sequential bounded reproduction; generated proof corpora stay in build/."""
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

from check_rup_lrat import verify
from encode import controls as phase_controls, encoding
from rup_controls import controls as rup_controls

ROOT = Path(__file__).resolve().parent
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def run(args, seconds=35):
    result = subprocess.run(args, text=True, capture_output=True, env=ENV, timeout=seconds)
    require(result.returncode == 0, f'child failed: {args}: {result.stderr} {result.stdout}')
    return result.stdout


def solve(family, build, conflicts, stem):
    # Only discovery/trace production occurs in this child; it certifies nothing.
    from pysat.solvers import Solver
    seeds = json.loads((ROOT/'seeds.json').read_text())
    raw = (build/f'{family}.cnf').read_text().splitlines()
    clauses = [list(map(int, line.split()[:-1])) for line in raw[1:]]
    preferences = [(i+1)*(1 if bit == '1' else -1) for i, bit in enumerate(seeds[family])]
    with Solver(name='cadical195', bootstrap_with=clauses, with_proof=True) as solver:
        solver.set_phases(preferences)
        solver.conf_budget(conflicts)
        status = solver.solve_limited()
        statistics = solver.accum_stats()
        if status is False:
            libc = ctypes.CDLL(None)
            libc.fflush.argtypes = [ctypes.c_void_p]
            libc.fflush.restype = ctypes.c_int
            require(libc.fflush(None) == 0, 'C proof-buffer flush failed')
            proof = solver.get_proof()
        else:
            proof = None
    if proof is not None:
        (build/f'{stem}.drat').write_text('\n'.join(proof)+'\n')
    print(json.dumps({'status': 'UNSAT_PENDING_CHECK' if status is False else 'SAT' if status is True else 'UNKNOWN',
                      'statistics': statistics, 'conflict_budget': conflicts,
                      'mathematical_exclusion': False}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--builddir', type=Path, default=ROOT/'build')
    parser.add_argument('--converter-source', type=Path)
    parser.add_argument('--h17-source', type=Path, default=ROOT.parent/'van_der_waerden_618_phase_symmetry')
    parser.add_argument('--sanitizers', action='store_true')
    parser.add_argument('--solve', choices=['h2', 'h3', 'reflection'])
    parser.add_argument('--conflicts', type=int, default=100000)
    parser.add_argument('--stem')
    args = parser.parse_args()
    args.builddir = args.builddir.resolve()
    if args.solve:
        solve(args.solve, args.builddir, args.conflicts, args.stem or args.solve)
        return
    start = time.monotonic()
    build = args.builddir; build.mkdir(parents=True, exist_ok=True)
    expected = json.loads((ROOT/'expected.json').read_text())
    require(phase_controls() == expected['phase_controls'], 'phase controls disagree')
    require(rup_controls() == expected['rup_controls'], 'RUP controls disagree')
    flags = ['-O1', '-fsanitize=address,undefined', '-fno-omit-frame-pointer'] if args.sanitizers else ['-O2']
    run(['g++', '-std=c++17', '-Wall', '-Wextra', '-Wconversion', '-Wshadow', *flags,
         str(ROOT/'direct_encode.cpp'), '-o', str(build/'direct_encode')], 30)
    converter_meta = expected['drat_converter']['files']['drat-trim.c']
    converter_source = build/'drat-trim.c'
    if args.converter_source:
        converter_source.write_bytes(args.converter_source.read_bytes())
    elif not converter_source.exists():
        data = urllib.request.urlopen(converter_meta['url'], timeout=15).read()
        converter_source.write_bytes(data)
    require(hashlib.sha256(converter_source.read_bytes()).hexdigest() == converter_meta['sha256'], 'wrong pinned converter source')
    run(['gcc', '-O2', '-std=gnu99', str(converter_source), '-o', str(build/'drat-trim')], 30)
    summaries = {}
    for family in ['h3', 'h2', 'reflection']:
        raw, meta = encoding(family)
        want = expected['families'][family]
        require(meta['variables'] == want['variables'] and meta['clauses'] == want['initial_clauses'] and meta['cnf_sha256'] == want['cnf_sha256'], 'encoding changed')
        native = run([str(build/'direct_encode'), family], 30).encode()
        require(raw == native, 'complete independent CNF comparison failed')
        (build/f'{family}.cnf').write_bytes(raw)
        output = run([sys.executable, str(ROOT/'reproduce.py'), '--solve', family, '--builddir', str(build)])
        discovery = json.loads(output)
        require(discovery['status'] == 'UNSAT_PENDING_CHECK', 'no complete proof produced; no exclusion established')
        conversion = run([str(build/'drat-trim'), str(build/f'{family}.cnf'), str(build/f'{family}.drat'),
                          '-t', '30', '-L', str(build/f'{family}.lrat')])
        require('s VERIFIED' in conversion, 'proof conversion/check failed')
        checked = verify(build/f'{family}.cnf', build/f'{family}.lrat')
        checked['reference_proof_byte_match'] = checked['proof_sha256'] == want['proof_sha256']
        summaries[family] = checked
        print(json.dumps({'family': family, **checked}), flush=True)
    # A discovery budget cut is explicitly UNKNOWN and supplies no proof.
    partial = json.loads(run([sys.executable, str(ROOT/'reproduce.py'), '--solve', 'h3', '--builddir', str(build),
                              '--conflicts', '1', '--stem', 'h3-incomplete']))
    require(partial['status'] == 'UNKNOWN', 'unexpected budget-control result')
    require(not (build/'h3-incomplete.drat').exists(), 'incomplete solve yielded a proof')
    # Explicit previously published mathematical input; preserve its own checker.
    require((args.h17_source/'reproduce.py').is_file(), 'missing published H17 dependency; see README')
    h17 = json.loads(run([sys.executable, str(args.h17_source/'reproduce.py')]))
    require(h17['status'] == 'VERIFIED' and h17['certificate_sha256'] == expected['h17_dependency']['certificate_sha256'], 'H17 dependency did not reproduce')
    result = {'agent': 'six-vdw-1', 'role': 'researcher', 'status': 'VERIFIED_ALL_PUBLISHED_REDUCTIONS',
              'families': summaries, 'h17_dependency': h17['certificate_sha256'],
              'budget_control_UNKNOWN': True, 'phase_affine_stabilizer_order': 1,
              'color_affine_stabilizer_order_at_most': 2,
              'nontrivial_color_affine_symmetry_requires_separable_CRT': True,
              'length3704_witness': False, 'seconds': time.monotonic()-start,
              'peak_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (build/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'families'}))


if __name__ == '__main__':
    main()
