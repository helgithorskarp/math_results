"""Small standard-library checker for the positive-hint (RUP) LRAT fragment.

It does not import the producer, a SAT library, or DRAT-trim. Deletions are
ignored: every retained derived clause has already been proved a consequence
of the original formula. Negative RAT hints are deliberately rejected.
"""
import argparse
import json
from pathlib import Path


def read_cnf(path):
    clauses = []
    declared = None
    for line in Path(path).read_text().splitlines():
        if not line or line.startswith('c'):
            continue
        if line.startswith('p '):
            if declared is not None:
                raise ValueError('duplicate header')
            parts = line.split()
            if len(parts) != 4 or parts[:2] != ['p', 'cnf']:
                raise ValueError('invalid header')
            declared = tuple(map(int, parts[2:]))
            continue
        values = list(map(int, line.split()))
        if not values or values[-1] != 0 or 0 in values[:-1]:
            raise ValueError('expected one terminated clause per line')
        clauses.append(tuple(values[:-1]))
    if declared is None or len(clauses) != declared[1]:
        raise ValueError('clause count mismatch')
    if any(abs(x) > declared[0] for c in clauses for x in c):
        raise ValueError('variable out of range')
    return declared[0], clauses


def check(cnf, proof):
    n, original = read_cnf(cnf)
    known = {i+1: c for i, c in enumerate(original)}
    last = len(original)
    additions = hints_used = deletions = 0
    for line in Path(proof).open():
        parts = line.split()
        if not parts or parts[0] == 'c':
            continue
        ident = int(parts[0])
        if len(parts) >= 2 and parts[1] == 'd':
            ids = list(map(int, parts[2:]))
            if not ids or ids[-1] != 0 or any(i <= 0 for i in ids[:-1]):
                raise ValueError('bad deletion syntax')
            deletions += len(ids)-1
            continue
        if ident <= last or ident in known:
            raise ValueError('nonfresh addition id')
        values = list(map(int, parts[1:]))
        zeros = [i for i, x in enumerate(values) if x == 0]
        if len(zeros) != 2 or zeros[-1] != len(values)-1:
            raise ValueError('bad addition syntax')
        clause = tuple(values[:zeros[0]])
        hints = values[zeros[0]+1:-1]
        if not hints or any(h <= 0 or h not in known for h in hints):
            raise ValueError('only existing positive RUP hints accepted')
        if any(abs(x) > n for x in clause):
            raise ValueError('new variable in RUP proof')
        if len(set(clause)) != len(clause) or any(-x in clause for x in clause):
            raise ValueError('noncanonical candidate clause')
        # Truth is represented by signed literals. Assume the candidate false.
        truth = {-x for x in clause}
        conflict = False
        for offset, h in enumerate(hints):
            parent = known[h]
            if any(x in truth for x in parent):
                raise ValueError('satisfied clause is not a propagation hint')
            remaining = set(x for x in parent if -x not in truth)
            hints_used += 1
            if not remaining:
                if offset != len(hints)-1:
                    raise ValueError('conflict must be final hint')
                conflict = True
                break
            if len(remaining) != 1:
                raise ValueError('hint is not unit')
            truth.update(remaining)
        if not conflict:
            raise ValueError('candidate not proved by unit contradiction')
        known[ident] = clause
        last = ident
        additions += 1
        if not clause:
            return {'status': 'VERIFIED', 'input_variables': n,
                    'input_clauses': len(original), 'rup_additions': additions,
                    'propagation_hints': hints_used, 'ignored_deletions': deletions}
    raise ValueError('proof did not derive the empty clause')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cnf', type=Path)
    parser.add_argument('lrat', type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.cnf, args.lrat), sort_keys=True))
