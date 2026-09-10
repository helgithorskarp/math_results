"""Bounded SAT experiments with direct witnesses and checked UNSAT proofs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time
from encode import decode

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('cnf', type=Path)
parser.add_argument('--seconds', type=int, default=300)
parser.add_argument('--kissat', default='kissat')
parser.add_argument('--checker', default='drat-trim')
args = parser.parse_args()
if args.seconds < 1:
    parser.error('--seconds must be positive')
base = args.cnf.with_suffix('')
def artifact(suffix):
    return Path(str(base) + suffix)
proof, log = artifact('.drat'), artifact('.kissat.log')
start = time.monotonic()
with log.open('w') as stream:
    try:
        result = subprocess.run(
            [args.kissat, f'--time={args.seconds}', str(args.cnf), str(proof)],
            stdout=stream, stderr=subprocess.STDOUT, timeout=args.seconds+15)
        code = result.returncode
    except subprocess.TimeoutExpired:
        code = None
text = log.read_text()
lines = set(text.splitlines())
status = ('SAT' if 's SATISFIABLE' in lines else
          'UNSAT' if 's UNSATISFIABLE' in lines else 'UNKNOWN')
record = {'status': status, 'exit_code': code,
          'seconds': time.monotonic()-start, 'time_limit': args.seconds,
          'cnf_sha256': hashlib.sha256(args.cnf.read_bytes()).hexdigest(),
          'proof_bytes': proof.stat().st_size if proof.exists() else 0,
          'proof_verified': False}
if status == 'SAT':
    model = [int(x) for line in text.splitlines() if line.startswith('v ')
             for x in line.split()[1:] if x != '0']
    metadata = json.loads(artifact('.json').read_text())
    partition = decode(model, metadata)
    if metadata.get('anchor'):
        partition = [metadata['anchor']] + partition
    record['partition_zero_based'] = partition
elif status == 'UNSAT':
    with artifact('.check.log').open('w') as stream:
        check = subprocess.run(
            [args.checker, str(args.cnf), str(proof), '-t', '120'],
            stdout=stream, stderr=subprocess.STDOUT, timeout=135)
    record['checker_exit_code'] = check.returncode
    record['proof_verified'] = (check.returncode == 0 and
                                's VERIFIED' in artifact('.check.log').read_text())
    if not record['proof_verified']:
        raise RuntimeError('UNSAT proof verification failed; inspect checker log')
artifact('.run.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record))
