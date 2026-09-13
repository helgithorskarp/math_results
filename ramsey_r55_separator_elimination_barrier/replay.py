"""Regenerate and independently check the complete incidence certificate."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work-dir', type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    work = args.work_dir.resolve()
    if work.exists():
        raise SystemExit('Use a fresh work directory outside the checkout.')
    work.mkdir(parents=True)
    for name in ['generate.py', 'verify.py']:
        shutil.copy2(source / name, work / name)
    start = time.monotonic()
    cert = work / 'hamilton43-matching.bin'
    subprocess.run([sys.executable, '-B', str(work / 'generate.py'),
                    '--n', '43', '--cycle', '--output', str(cert)], check=True)
    output = work / 'verified.json'
    subprocess.run([sys.executable, '-B', str(work / 'verify.py'),
                    str(cert), '--output', str(output)], check=True)
    result = json.loads(output.read_text())
    expected_path = source / 'EXPECTED.json'
    expected = json.loads(expected_path.read_text())
    for value in [result, expected]:
        value.pop('seconds', None)
    if result != expected:
        raise RuntimeError('Exact replay differs from expected certificate.')
    report = {'status': 'EXACT_INCIDENCE_REPLAY_MATCH',
              'certificate_sha256': hashlib.sha256(cert.read_bytes()).hexdigest(),
              'seconds': time.monotonic() - start,
              'physical_cases_closed': 0,
              'treewidth_primal': result['treewidth_primal'],
              'treewidth_incidence': result['treewidth_incidence_lower'],
              'free_edge_host_cutwidth': result['free_edge_host_cutwidth']}
    (work / 'replay.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
