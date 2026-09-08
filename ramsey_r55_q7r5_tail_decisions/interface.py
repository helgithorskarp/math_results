"""Complete h3887 task filter. Retained physical formulas are unchanged."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
COUNTS = {7: 640, 8: 546356, 9: 362, 10: 4}

def parameters(name):
    try:
        prefix, q, r, c = name.split('-')
        q, r, c = int(q[1:]), int(r[1:]), int(c[1:])
    except (ValueError, TypeError):
        raise ValueError('Invalid h3887 task syntax') from None
    if not (prefix == 'bo1' and q in COUNTS and 5 <= r <= q and 0 <= c < COUNTS[q]
            and name == f'bo1-q{q}-r{r}-c{c:06d}'):
        raise ValueError('Noncanonical or out-of-range h3887 task')
    return q, r, c

def table():
    data = json.loads((HERE / 'TASKS.json').read_text())
    excluded, retained = data['excluded_core_indices'], data['retained_core_indices']
    if sorted(excluded + retained) != list(range(640)) or len(set(excluded + retained)) != 640:
        raise ValueError('Bad partition')
    return data

def status(name):
    q, r, c = parameters(name)
    data = table()
    closed = q == 7 and r == 5 and c in data['excluded_core_indices']
    return {'task': name, 'status': 'CERTIFIED_UNSAT' if closed else 'UNKNOWN',
            'reason': 'Complete induced tail is impossible' if closed else 'Physical43 completion remains undecided',
            'tail_witness_available': q == 7 and r == 5 and c in data['retained_core_indices'],
            'good43': False}

def registry():
    data = table()
    classes = []
    for q in range(7, 11):
        for r in range(5, q + 1):
            row = {'q': q, 'r': r, 'original_core_start': 0, 'original_core_stop': COUNTS[q]}
            if (q, r) == (7, 5):
                row['retained_core_indices'] = data['retained_core_indices']
                row['certified_unsat_core_indices'] = data['excluded_core_indices']
            else:
                row['retained_core_start'], row['retained_core_stop'] = 0, COUNTS[q]
            classes.append(row)
    return {'classes': classes, 'original_global_tasks': 2189178,
            'remaining_global_tasks': 2189178 - len(data['excluded_core_indices']),
            'q10_h3987_residual_children': 161, 'good43': False}

def validate_parent(parent):
    spec = json.loads((HERE / 'INPUTS.json').read_text())['parents'][0]
    if parent.name != spec['directory']:
        raise ValueError('Expected the h3887 source directory')
    raw = (parent / 'SHA256SUMS').read_bytes()
    if hashlib.sha256(raw).hexdigest() != spec['manifest_sha256'] or len(raw.splitlines()) != spec['manifest_entries']:
        raise ValueError('Parent source manifest')
    for line in raw.decode().splitlines():
        sha, name = line.split('  ', 1)
        if hashlib.sha256((parent / name).read_bytes()).hexdigest() != sha:
            raise ValueError('Parent source changed: ' + name)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--task')
    p.add_argument('--registry', action='store_true')
    p.add_argument('--emit', metavar='CATALOG_DIRECTORY')
    p.add_argument('--parent', default=str(HERE.parent / 'ramsey_r55_maximal_block_order'))
    p.add_argument('--output')
    p.add_argument('--triangles', action='store_true')
    a = p.parse_args()
    if a.registry:
        print(json.dumps(registry(), indent=2))
        return
    result = status(a.task)
    if a.emit and result['status'] == 'UNKNOWN':
        if not a.output:
            raise ValueError('New output filename required')
        parent = Path(a.parent).resolve()
        validate_parent(parent)
        command = [sys.executable, '-B', str(parent / 'ordered.py'), a.emit,
                   '--task', a.task, '--cnf', a.output]
        if a.triangles:
            command.append('--triangles')
        completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if completed.returncode:
            raise RuntimeError(completed.stderr)
        result['original_h3887_formula'] = json.loads(completed.stdout)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
