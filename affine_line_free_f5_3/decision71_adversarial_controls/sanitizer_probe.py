"""Inventory sanitizer outcomes for the eight valid and eight wrong-input checks."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess

from replay import OFFICIAL_SOURCE_SHA256
from verify import digest, dimacs, formula, load_fixtures, require


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus', type=Path, required=True, help='Fresh replay.py output')
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--checker', type=Path, required=True)
    parser.add_argument('--checker-source', type=Path, required=True)
    parser.add_argument('--warnings-off', action='store_true',
                        help='Diagnostic isolation using official -w, after the pinned binary framing guard')
    args = parser.parse_args()
    require(digest(args.checker_source.read_bytes()) == OFFICIAL_SOURCE_SHA256, 'wrong checker source')
    symbols = subprocess.check_output(['nm', '-D', str(args.checker)], text=True)
    require('__asan_init' in symbols and '__ubsan_handle_shift_out_of_bounds' in symbols,
            'checker lacks the required sanitizer instrumentation')
    summary = json.loads((args.corpus/'summary.json').read_text())
    require(summary['status'] == 'FOUR_MINIMAL_TWO_CLAUSE_WEAKENINGS_VERIFIED',
            'missing successful ordinary replay')
    require(not args.out.exists(), 'output must be new')
    args.out.mkdir(parents=True)
    env = dict(os.environ, ASAN_OPTIONS='detect_leaks=0:halt_on_error=1',
               UBSAN_OPTIONS='halt_on_error=1:print_stacktrace=1')
    fixtures, _ = load_fixtures()
    cases = []
    framing = []
    guard = None
    if args.warnings_off:
        guard_path = Path(__file__).resolve().parent.parent/'decision71_independent_proofs/binary_drat_framing.py'
        require(digest(guard_path.read_bytes()) ==
                '8ce3d45465a1b21ea4f028b27b9a9fb86d9bf0139730d6a26aa06c4b5f22cf08',
                'framing guard source changed')
        spec = importlib.util.spec_from_file_location('reviewer_framing', guard_path)
        guard = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guard)
    for r in fixtures:
        original = formula(r['weights'])
        removed = r['removed_clause_indices']
        for omission in removed:
            prefix = args.corpus/f"case_{r['index']}_omit_{omission}"
            proof = prefix.with_suffix('.drat')
            recorded = next(q for q in summary['records']
                            if (q['index'], q['omitted_clause']) == (r['index'], omission))
            require(digest(proof.read_bytes()) == recorded['proof_sha256'], 'proof identity changed')
            if guard:
                framed = guard.inspect(proof)
                require(framed['sha256'] == recorded['proof_sha256']
                        and framed['status'] == 'BINARY_DRAT_FRAMING_VALID', 'binary framing failed')
                framing.append({'index': r['index'], 'omitted_clause': omission, **framed})
            for mode in ('valid', 'wrong_input'):
                discard = [omission] if mode == 'valid' else removed
                cnf = (prefix.with_suffix('.cnf') if mode == 'valid'
                       else args.corpus/f"case_{r['index']}_omit_both.cnf")
                expected = dimacs([c for i, c in enumerate(original) if i not in discard])
                require(cnf.read_bytes() == expected, 'incorrect probe formula')
                command = [str(args.checker.resolve()), str(cnf), str(proof)]
                if args.warnings_off:
                    command.append('-w')
                result = subprocess.run(command,
                                        env=env, capture_output=True, text=True, timeout=60)
                output = result.stdout+result.stderr
                log = args.out/f"{r['index']}_{omission}_{mode}.log"
                log.write_text(output)
                findings = []
                for line in output.splitlines():
                    if 'runtime error:' in line:
                        findings.append(line[line.index('drat-trim.c:'):] if 'drat-trim.c:' in line
                                        else line[line.index('runtime error:'):])
                    elif 'ERROR: AddressSanitizer:' in line:
                        findings.append(line[line.index('ERROR: AddressSanitizer:'):].split(' on address ')[0])
                cases.append({'index': r['index'], 'omitted_clause': omission, 'mode': mode,
                              'cnf_sha256': digest(expected), 'proof_sha256': recorded['proof_sha256'],
                              'returncode': result.returncode, 'diagnostics': findings,
                              'verified': result.returncode == 0 and 's VERIFIED' in result.stdout.splitlines(),
                              'normal_rejection': 's NOT VERIFIED' in result.stdout.splitlines()
                                                  and result.returncode >= 0 and not findings})
                print(json.dumps(cases[-1]), flush=True)
    valid = [r for r in cases if r['mode'] == 'valid']
    invalid = [r for r in cases if r['mode'] == 'wrong_input']
    result = {'status': 'SANITIZER_PROBE_COMPLETE_WITH_FINDINGS' if any(r['diagnostics'] for r in cases)
                        else 'SANITIZER_PROBE_COMPLETE_NO_FINDINGS',
              'valid_inputs_cleanly_verified': sum(r['verified'] and not r['diagnostics'] for r in valid),
              'wrong_inputs_normally_rejected': sum(r['normal_rejection'] for r in invalid),
              'wrong_inputs_with_diagnostics': sum(bool(r['diagnostics']) for r in invalid),
              'checker_sha256': digest(args.checker.read_bytes()),
              'checker_source_sha256': OFFICIAL_SOURCE_SHA256,
              'environment': {k: env[k] for k in ('ASAN_OPTIONS', 'UBSAN_OPTIONS')},
              'warnings_off': args.warnings_off, 'binary_framing_checks': framing,
              'framing_guard_sha256': digest(guard_path.read_bytes()) if guard else None,
              'cases': cases, 'global_exact_proof_accepted': False}
    (args.out/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}, indent=2))


if __name__ == '__main__':
    main()
