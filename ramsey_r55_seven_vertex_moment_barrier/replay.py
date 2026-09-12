"""Regenerate the exact relaxation and check its compact rational control."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work-dir', type=Path, required=True)
    parser.add_argument('--validate-counting', action='store_true')
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    target = args.work_dir.resolve()
    if target == source or target.exists():
        raise SystemExit('Use a fresh work directory outside the source package.')
    target.mkdir(parents=True)
    files = ['graph_types.py', 'generate_base.py', 'generate_integer.py',
             'generate_squares.py', 'verify.py', 'validate.py',
             'exact_density.json']
    for name in files:
        shutil.copy2(source / name, target / name)
    start = time.monotonic()
    for name in ['generate_base.py', 'generate_integer.py',
                 'generate_squares.py', 'verify.py']:
        subprocess.run([sys.executable, '-B', str(target / name)], check=True)
    actual = json.loads((target / 'verification.json').read_text())
    expected = json.loads((source / 'expected.json').read_text())
    actual.pop('seconds'); expected.pop('seconds')
    assert actual == expected, 'Exact verification differs from the stored result.'
    if args.validate_counting:
        subprocess.run([sys.executable, '-B', str(target / 'validate.py')], check=True)
        a = json.loads((target / 'counting_validation.json').read_text())
        e = json.loads((source / 'expected_counting_validation.json').read_text())
        a.pop('seconds'); e.pop('seconds')
        assert a == e, 'Direct-count validation differs from the stored result.'
    result = {
        'status': 'EXACT_REPLAY_MATCH',
        'certificate_sha256': hashlib.sha256((source / 'exact_density.json').read_bytes()).hexdigest(),
        'seconds': time.monotonic() - start,
        'terminal_physical_decisions': 0,
    }
    (target / 'replay.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))

if __name__ == '__main__':
    main()
