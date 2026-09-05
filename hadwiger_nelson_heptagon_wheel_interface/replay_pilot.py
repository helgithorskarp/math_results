"""Optional reproduction of the three bounded native calls; no proof claim."""
import argparse
import json
from pathlib import Path
import resource
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('--inputs', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
parser.add_argument('--kissat', type=Path, required=True)
args = parser.parse_args()
args.out.mkdir(parents=True, exist_ok=False)


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4*1024**3,)*2)
    resource.setrlimit(resource.RLIMIT_FSIZE, (256*1024**2,)*2)


records = []
for i in range(3):
    command = [str(args.kissat), '--conflicts=200000', '--time=60',
               str(args.inputs/f'q{i}.cnf'), str(args.out/f'q{i}.drat')]
    started = time.perf_counter()
    with (args.out/f'q{i}.log').open('w') as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                preexec_fn=limits)
    status_lines = [line for line in (args.out/f'q{i}.log').read_text().splitlines()
                    if line.startswith('s ')]
    record = {'query': i, 'exit_code': result.returncode,
              'status_lines': status_lines, 'seconds': time.perf_counter()-started,
              'certificate_checked': False}
    records.append(record)
    (args.out/'replay.json').write_text(json.dumps(records, indent=2)+'\n')
    print(json.dumps(record), flush=True)
