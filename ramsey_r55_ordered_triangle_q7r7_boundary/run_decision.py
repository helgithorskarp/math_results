"""One frozen physical decision for the ordered shared-triangle task."""
from pathlib import Path
from itertools import combinations
import argparse
import datetime
import hashlib
import json
import resource
import subprocess
import sys
import time

FORMULA_SHA256 = '899f8492e9806bc87ed71296a9aca8d52b63f3cfaa4eaa0e1bf17b0ac945664a'
SOLVER_SHA256 = '823b3c94050654fda13dab0c8c34386d9777a1e6de31bd6bc20555979e7c5e0b'
CHECKER_SHA256 = '9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a'
TASK = 'bo1-q7-r7-c000000'
LIMIT = 1800


def identity(path):
    path = Path(path).resolve()
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return {'bytes': path.stat().st_size, 'sha256': digest.hexdigest()}


def classify(exit_code, stdout, witness):
    stdout_status = [line for line in stdout.splitlines() if line.startswith('s ')]
    witness_status = [line for line in witness.splitlines() if line.startswith('s ')]
    combined = set(stdout_status + witness_status)
    if exit_code == 0 and not combined and witness == 'c UNKNOWN\n':
        return 'UNKNOWN'
    if exit_code == 10 and combined == {'s SATISFIABLE'} and witness_status == ['s SATISFIABLE']:
        return 'SATISFIABLE'
    if exit_code == 20 and combined == {'s UNSATISFIABLE'} and witness_status == ['s UNSATISFIABLE']:
        return 'UNSATISFIABLE'
    return 'UNEXPECTED_SOLVER_RESULT'


def controls():
    cases = [
        (0, '', 'c UNKNOWN\n', 'UNKNOWN'),
        (10, 's SATISFIABLE\n', 's SATISFIABLE\nv 1 0\n', 'SATISFIABLE'),
        (20, 's UNSATISFIABLE\n', 's UNSATISFIABLE\n', 'UNSATISFIABLE'),
        (0, '', '', 'UNEXPECTED_SOLVER_RESULT'),
        (10, 's SATISFIABLE\n', 's SATISFIABLE\ns UNSATISFIABLE\n', 'UNEXPECTED_SOLVER_RESULT'),
        (20, 's UNSATISFIABLE\n', 'c UNKNOWN\n', 'UNEXPECTED_SOLVER_RESULT'),
    ]
    if any(classify(*case[:3]) != case[3] for case in cases):
        raise ValueError('classification controls')
    return {'status': 'VERIFIED_FAIL_CLOSED_RESULT_CLASSIFIER', 'cases': len(cases)}


def run(solver, checker, cnf, cache, source, output):
    controls()
    output = Path(output).resolve()
    output.mkdir(exist_ok=False)
    solver = Path(solver).resolve()
    checker = Path(checker).resolve()
    cnf = Path(cnf).resolve()
    cache = Path(cache).resolve()
    source = Path(source).resolve()
    receipt = {
        'task': TASK,
        'seconds_limit': LIMIT,
        'solver': identity(solver),
        'checker': identity(checker),
        'cnf': identity(cnf),
        'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'target_found': False,
        'family_excluded': False,
        'solver_calls': 1,
    }
    if receipt['cnf']['sha256'] != FORMULA_SHA256:
        raise ValueError('audited formula identity')
    if receipt['solver']['sha256'] != SOLVER_SHA256:
        raise ValueError('frozen solver identity')
    if receipt['checker']['sha256'] != CHECKER_SHA256:
        raise ValueError('frozen checker identity')
    command = [str(solver), '-t', str(LIMIT), '-w', 'witness.txt', str(cnf), 'trace.drat']
    receipt['command'] = command
    (output / 'FROZEN.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    start = time.monotonic()
    with (output / 'stdout.txt').open('wb') as stdout, (output / 'stderr.txt').open('wb') as stderr:
        result = subprocess.run(command, cwd=output, stdout=stdout, stderr=stderr)
    receipt.update({
        'exit_code': result.returncode,
        'elapsed_seconds': time.monotonic() - start,
        'solver_max_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
    })
    for name in ('stdout.txt', 'stderr.txt', 'witness.txt', 'trace.drat'):
        if (output / name).exists():
            receipt[name] = identity(output / name)
    stdout_text = (output / 'stdout.txt').read_text()
    witness_text = (output / 'witness.txt').read_text()
    outcome = classify(result.returncode, stdout_text, witness_text)
    receipt['solver_status_lines'] = [line for line in stdout_text.splitlines() if line.startswith('s ')]
    receipt['witness_status'] = witness_text.splitlines()[0] if witness_text.splitlines() else ''
    receipt['status'] = 'UNEXPECTED_SOLVER_RESULT'
    if outcome == 'UNKNOWN':
        receipt.update(status='UNKNOWN', proof_status='PARTIAL_STREAM_NOT_A_CERTIFICATE')
    elif outcome == 'SATISFIABLE':
        sys.path.insert(0, str(source / 'ramsey_r55_maximal_block_order'))
        import ordered
        checked = ordered.accept(TASK, cache, output / 'witness.txt', triangles=True)
        graph = checked['graph']
        (output / 'GOOD43.json').write_text(json.dumps(checked, indent=2, sort_keys=True) + '\n')
        bits = int(graph['red_hex'], 16)
        edges = ''.join(f'{u} {v}\n' for k, (u, v) in enumerate(combinations(range(43), 2)) if bits >> k & 1)
        (output / 'GOOD43.edges').write_text('43\n' + edges)
        receipt.update(status='VERIFIED_GOOD43', target_found=True,
                       physical_check=checked['certificate'], carrier_code=checked['carrier_code'])
    elif outcome == 'UNSATISFIABLE':
        receipt['status'] = 'UNSAT_CERTIFICATE_PENDING'
        (output / 'RESULT.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
        with (output / 'checker.txt').open('wb') as log:
            verified = subprocess.run([str(checker), str(cnf), str(output / 'trace.drat')],
                                      stdout=log, stderr=subprocess.STDOUT)
        checker_text = (output / 'checker.txt').read_text()
        receipt['checker.txt'] = identity(output / 'checker.txt')
        receipt['checker_exit_code'] = verified.returncode
        receipt['combined_max_rss_kib'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        if verified.returncode != 0 or 's VERIFIED' not in checker_text:
            (output / 'RESULT.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
            raise ValueError('DRAT verification failed')
        receipt.update(status='CERTIFIED_UNSAT', family_excluded=True,
                       proof_status='INDEPENDENTLY_VERIFIED_DRAT')
    (output / 'RESULT.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    if receipt['status'] == 'UNEXPECTED_SOLVER_RESULT':
        raise ValueError('unexpected solver result; inspect preserved receipt')
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--solver', type=Path)
    parser.add_argument('--checker', type=Path)
    parser.add_argument('--cnf', type=Path)
    parser.add_argument('--cache', type=Path)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    if args.controls:
        print(json.dumps(controls(), sort_keys=True))
    else:
        if any(value is None for value in (args.solver, args.checker, args.cnf, args.cache, args.source, args.output)):
            parser.error('decision paths are required')
        print(json.dumps(run(args.solver, args.checker, args.cnf, args.cache, args.source, args.output), sort_keys=True))
