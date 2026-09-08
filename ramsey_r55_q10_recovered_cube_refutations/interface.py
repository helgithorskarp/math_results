"""Emit the 161 residual physical tasks; the other 99 have checked refutations."""
from pathlib import Path
import argparse
import hashlib
import json
import verify

ROOT = Path(__file__).resolve().parent


def patch_clauses(branch):
    return [c['clause'] for c in json.loads((ROOT/'INPUTS.json').read_text())['certificates']
            if c['branch'] == branch]


def write_cnf(source, output, suffix):
    source, output = Path(source), Path(output)
    h = hashlib.sha256()
    with source.open('rb') as stream, output.open('xb') as target:
        header = stream.readline().decode().split()
        verify.need(header[:3] == ['p', 'cnf', '40351'] and
                    int(header[3]) == 1931146, 'source header')
        line = f'p cnf 40351 {1931146 + len(suffix)}\n'.encode()
        target.write(line); h.update(line)
        while block := stream.read(1024 * 1024):
            target.write(block); h.update(block)
        for clause in suffix:
            line = (' '.join(map(str, clause)) + ' 0\n').encode()
            target.write(line); h.update(line)
    return {'bytes': output.stat().st_size, 'sha256': h.hexdigest(),
            'variables': 40351, 'clauses': 1931146 + len(suffix)}


def emit(task_id, branches, output):
    rows = verify.tasks()
    found = [r for r in rows if r['id'] == task_id]
    verify.need(len(found) == 1, 'unknown task id')
    row = found[0]
    if row['status'] == 'CERTIFIED_UNSAT':
        return {'task': task_id, 'status': 'CERTIFIED_UNSAT',
                'certificate': row['certificate'], 'file_written': False}
    inputs = json.loads((ROOT/'INPUTS.json').read_text())
    spec = next(b for b in inputs['branches'] if b['branch'] == row['branch'])
    source = Path(branches)/(row['branch'] + '.cnf')
    verify.need(verify.sha(source) == spec['sha256'], 'frozen source hash')
    suffix = patch_clauses(row['branch']) + [[x] for x in row['cube']]
    if row['forced_residual_literal'] is not None:
        suffix.append([row['forced_residual_literal']])
    result = write_cnf(source, output, suffix)
    return {'task': task_id, 'status': 'UNKNOWN', 'file_written': True,
            'cube': row['cube'], 'forced_residual_literal': row['forced_residual_literal'],
            **result}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task')
    parser.add_argument('--branches', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.task:
        verify.need(args.branches is not None and args.output is not None,
                    '--branches and --output required')
        result = emit(args.task, args.branches, args.output)
    else:
        result = {'summary': verify.task_summary(verify.tasks()), 'tasks': verify.tasks()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
