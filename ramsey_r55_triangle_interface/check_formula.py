"""Read a generated DIMACS file against the independent physical clause stream."""
from pathlib import Path
import argparse
import hashlib
import json
import audit


def check(name, cache, path):
    data = audit.physical(name, cache); plan = audit.independent_plan(data)
    variables = max(plan['variables'].values())
    clauses = 1+360*(data['q']-1)+plan['target_count']
    clauses += sum(len(x)+1 for x in plan['inputs'].values())
    for vertices in __import__('itertools').combinations(range(4*data['r'], 43), 4):
        if audit.forbid(data, vertices, 1) is not None:
            clauses += 1
    digest = hashlib.sha256(); size = 0; count = 0; path = Path(path)
    with path.open('rb') as stream:
        line = stream.readline(); digest.update(line); size += len(line)
        if line != f'p cnf {variables} {clauses}\n'.encode():
            raise ValueError('header mismatch')
        for section, expected in audit.independent_clauses(data, plan):
            line = stream.readline(); digest.update(line); size += len(line); count += 1
            if line != (' '.join(map(str, expected))+' 0\n').encode():
                raise ValueError(f'literal mismatch in {section} clause {count}')
        if stream.read(1):
            raise ValueError('trailing content')
    if count != clauses or size != path.stat().st_size:
        raise ValueError('file dimensions')
    return {'status': 'VERIFIED_REAL_DIMACS_FROM_INDEPENDENT_PHYSICAL_STREAM',
            'task': name, 'variables': variables, 'clauses': clauses,
            'bytes': size, 'sha256': digest.hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('cache', type=Path)
    parser.add_argument('--task', required=True); parser.add_argument('--cnf', type=Path, required=True)
    args = parser.parse_args(); print(json.dumps(check(args.task, args.cache, args.cnf), indent=2, sort_keys=True))
