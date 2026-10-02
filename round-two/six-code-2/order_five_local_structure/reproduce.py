"""Serial exact reproduction; runtime metadata stays outside the exact record."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import sys
import time


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    args = p.parse_args()
    if args.work.exists():
        raise ValueError('require a new reproduction directory')
    args.work.mkdir(parents=True)
    begin = time.monotonic()
    root = Path(__file__).resolve().parent
    prefix = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else [])
    commands = [prefix + [str(root / 'audit_types.py'), '--output', str(args.work / 'TYPES.json')],
                prefix + [str(root / 'audit_three.py'), '--classification', str(root / 'CLASSIFICATION.json'),
                          '--producer-summary', str(root / 'THREE_CERTIFICATE.json'), '--output', str(args.work / 'REPAIRS.json')]]
    for command in commands:
        remaining = 60 - (time.monotonic() - begin)
        if remaining <= 0:
            raise ValueError('INCOMPLETE initial 60-second whole reproduction guard')
        result = subprocess.run(command, capture_output=True, text=True, timeout=remaining)
        if result.returncode:
            raise ValueError(result.stderr + result.stdout)
    exact = {}
    for name in ('TYPES', 'REPAIRS'):
        record = json.loads((args.work / (name + '.json')).read_bytes())
        exact[name.lower()] = {k: v for k, v in record.items() if k not in ('seconds', 'peak_RSS_kib')}
    raw = (json.dumps(exact, sort_keys=True, separators=(',', ':')) + '\n').encode()
    expected = root / 'EXPECTED.json'
    if expected.exists() and json.loads(expected.read_bytes()) != exact:
        raise ValueError('complete exact record differs from expected result')
    (args.work / 'EXACT_RESULT.json').write_bytes(raw)
    execution = {'status': 'ALL_EXACT_CHECKS_PASSED', 'agent': 'six-code-2', 'role': 'researcher',
                 'python': sys.version, 'optimized': bool(sys.flags.optimize),
                 'seconds': time.monotonic() - begin, 'initial_whole_guard_seconds': 60,
                 'peak_child_RSS_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                 'exact_result_bytes': len(raw), 'exact_result_sha256': hashlib.sha256(raw).hexdigest()}
    (args.work / 'EXECUTION.json').write_text(json.dumps(execution, sort_keys=True, indent=2) + '\n')
    print(json.dumps(execution, sort_keys=True))


if __name__ == '__main__':
    main()
