"""One capped physical decision, with fail-closed result and certificate handling."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import resource
import subprocess
import time
import verify


def identity(path):
    path = Path(path); digest = hashlib.sha256()
    with path.open('rb') as f:
        while chunk := f.read(1024*1024):
            digest.update(chunk)
    return {'bytes': path.stat().st_size, 'sha256': digest.hexdigest()}


def classify(exit_code, stdout, witness):
    """CaDiCaL -w redirects result records to the witness file; UNKNOWN is a comment."""
    lines = [line for line in stdout.splitlines() if line.startswith('s ')]
    witness_lines = [line for line in witness.splitlines() if line.startswith('s ')]
    combined = set(lines + witness_lines)
    if exit_code == 0 and not combined and witness == 'c UNKNOWN\n':
        return 'UNKNOWN'
    if exit_code == 10 and combined == {'s SATISFIABLE'} and witness_lines == ['s SATISFIABLE']:
        return 'SATISFIABLE'
    if exit_code == 20 and combined == {'s UNSATISFIABLE'} and witness_lines == ['s UNSATISFIABLE']:
        return 'UNSATISFIABLE'
    return 'UNEXPECTED_SOLVER_RESULT'


def run(solver, cnf, output, checker=None):
    output = Path(output).resolve(); output.mkdir(exist_ok=False)
    solver = Path(solver).resolve(); cnf = Path(cnf).resolve()
    receipt = {'seconds_limit': 300, 'solver': identity(solver), 'cnf': identity(cnf),
               'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'target_found': False, 'family_excluded': False}
    if receipt['cnf']['sha256'] != '91bf5f741a7e8d08ad1da1e347825cf572060db601bb40f2e185da2c6f734dce':
        raise ValueError('audited formula identity')
    if receipt['solver']['sha256'] != '823b3c94050654fda13dab0c8c34386d9777a1e6de31bd6bc20555979e7c5e0b':
        raise ValueError('frozen CaDiCaL executable identity')
    command = [str(solver), '-t', '300', '-w', 'witness.txt', str(cnf), 'trace.drat']
    receipt['command'] = command
    (output/'FROZEN.json').write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    start = time.monotonic()
    with (output/'stdout.txt').open('wb') as out, (output/'stderr.txt').open('wb') as err:
        result = subprocess.run(command, cwd=output, stdout=out, stderr=err)
    receipt.update({'exit_code': result.returncode, 'elapsed_seconds': time.monotonic()-start,
                    'max_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
    for name in ('stdout.txt', 'stderr.txt', 'witness.txt', 'trace.drat'):
        if (output/name).exists():
            receipt[name] = identity(output/name)
    status = [line for line in (output/'stdout.txt').read_text().splitlines() if line.startswith('s ')]
    receipt['solver_status_lines'] = status
    outcome = classify(result.returncode, (output/'stdout.txt').read_text(), (output/'witness.txt').read_text())
    receipt['witness_status'] = (output/'witness.txt').read_text().splitlines()[0]
    receipt['status'] = 'UNEXPECTED_SOLVER_RESULT'
    if outcome == 'UNKNOWN':
        receipt['status'] = 'UNKNOWN'; receipt['proof_status'] = 'PARTIAL_STREAM_NOT_A_CERTIFICATE'
    elif outcome == 'SATISFIABLE':
        graph, checked = verify.decode(verify.parse_model(output/'witness.txt'))
        (output/'GOOD43.json').write_text(json.dumps(graph, sort_keys=True)+'\n')
        from itertools import combinations
        bits = int(graph['red_hex'], 16)
        (output/'GOOD43.edges').write_text('43\n'+''.join(f'{u} {v}\n' for k, (u, v) in enumerate(combinations(range(43), 2)) if bits >> k & 1))
        receipt.update({'status': 'VERIFIED_GOOD43', 'target_found': True, 'physical_check': checked})
    elif outcome == 'UNSATISFIABLE':
        receipt['status'] = 'UNSAT_CERTIFICATE_PENDING'
        (output/'RESULT.json').write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
        if checker is None:
            raise ValueError('UNSAT requires an independent DRAT checker')
        with (output/'checker.txt').open('wb') as f:
            checked = subprocess.run([str(Path(checker).resolve()), str(cnf), str(output/'trace.drat')], stdout=f, stderr=subprocess.STDOUT)
        log = (output/'checker.txt').read_text()
        if checked.returncode != 0 or 's VERIFIED' not in log:
            raise ValueError('DRAT verification failed')
        receipt.update({'status': 'CERTIFIED_UNSAT', 'family_excluded': True,
                        'proof_status': 'INDEPENDENTLY_VERIFIED_DRAT', 'checker': identity(checker)})
    (output/'RESULT.json').write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    if receipt['status'] == 'UNEXPECTED_SOLVER_RESULT':
        raise ValueError('unexpected solver result; inspect preserved receipt')
    return receipt


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--solver', type=Path, required=True)
    p.add_argument('--cnf', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    p.add_argument('--checker', type=Path); a = p.parse_args()
    print(json.dumps(run(a.solver, a.cnf, a.output, a.checker), sort_keys=True))
