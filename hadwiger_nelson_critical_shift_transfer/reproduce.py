"""Generate bulk evidence outside the repository, then validate both proof layers."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from check_rup import check
from controls import run as controls
from verify import verify

ROOT = Path(__file__).resolve().parent


def run_logged(command, log, expected_code):
    with log.open('w') as stream:
        result = subprocess.run([str(x) for x in command], stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode != expected_code:
        raise RuntimeError(f'command exited {result.returncode}; inspect {log}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--kissat', type=Path, required=True)
    parser.add_argument('--drat-trim', type=Path, required=True)
    args = parser.parse_args()
    work = args.work.resolve()
    repository = ROOT.parent
    if work == repository or repository in work.parents:
        raise ValueError('generated evidence must be outside the repository')
    work.mkdir(parents=True, exist_ok=True)
    expected = json.loads((ROOT/'expected.json').read_text())
    print('Producing necessary collision clauses.', flush=True)
    run_logged([sys.executable, ROOT/'produce.py', work], work/'produce.log', 0)
    premises = verify(work)
    if premises != expected['premises']:
        raise ValueError('generated instance differs from the pinned reference run')
    print('Every geometric premise verified. Generating an UNSAT proof.', flush=True)
    run_logged([args.kissat.resolve(), '--plain', work/'instance.cnf', work/'proof.drat'], work/'kissat.log', 20)
    run_logged([args.drat_trim.resolve(), work/'instance.cnf', work/'proof.drat', '-L', work/'proof.lrat'], work/'drat_trim.log', 0)
    if 's VERIFIED' not in (work/'drat_trim.log').read_text():
        raise ValueError('DRAT-trim did not report verification')
    print('Checking the RUP proof with the standalone Python checker.', flush=True)
    proof = check(work/'instance.cnf', work/'proof.lrat')
    control_result = controls()
    # JSON turns the integer keys of the positive-map dictionary into strings.
    if json.loads(json.dumps(control_result)) != expected['controls']:
        raise ValueError('control result differs')
    output = {'premises': premises, 'proof': proof, 'controls': control_result,
              'proof_sha256': {name: hashlib.sha256((work/name).read_bytes()).hexdigest()
                               for name in ('proof.drat', 'proof.lrat')}}
    (work/'verified.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, sort_keys=True))


if __name__ == '__main__':
    main()
