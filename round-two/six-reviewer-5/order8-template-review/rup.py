"""Independent signed-set positive-RUP replay, reused from reviewer evidence h8522.

Clauses are immutable signed-literal sets; true/false sets drive propagation.
No author checker is imported. Empty initial formulas are accepted as inputs,
so exhaustive truth-classification controls include the empty clause family.
"""
import hashlib
from pathlib import Path

class Invalid(ValueError):
    pass


def need(condition, explanation):
    if not condition:
        raise Invalid(explanation)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def clauses(path):
    with Path(path).open() as stream:
        fields = next(stream, '').split()
        need(len(fields) == 4 and fields[:2] == ['p', 'cnf'], 'CNF header')
        nv, nc = map(int, fields[2:])
        need(nv > 0 and nc >= 0, 'CNF dimensions')
        rows = []
        for line in stream:
            values = list(map(int, line.split()))
            need(values and values[-1] == 0 and 0 not in values[:-1], 'CNF termination')
            row = values[:-1]
            need(all(0 < abs(x) <= nv for x in row), 'CNF variable domain')
            need(len(set(row)) == len(row), 'Duplicate CNF literal')
            need(not any(-x in row for x in row), 'Tautological CNF clause')
            rows.append(tuple(row))
        need(len(rows) == nc, 'CNF row coverage')
    return nv, rows


def literal_set(row, nv):
    need(len(set(row)) == len(row), 'Duplicate proof literal')
    for x in row:
        need(0 < abs(x) <= nv, 'Proof variable domain')
    need(not any(-x in row for x in row), 'Tautological proof clause')
    return frozenset(row)


def verify(cnf, proof):
    nv, initial = clauses(cnf)
    db = {i: literal_set(row, nv) for i, row in enumerate(initial, 1)}
    count = len(initial)
    last = count
    additions = deletions = hint_reads = lines = 0
    finished = False
    with Path(proof).open() as stream:
        for line in stream:
            need(not finished, 'Content after empty clause')
            tokens = line.split()
            need(len(tokens) >= 3, 'Proof grammar')
            ident = int(tokens[0])
            lines += 1
            if tokens[1] == 'd':
                ids = list(map(int, tokens[2:]))
                need(ids and ids[-1] == 0 and all(x > 0 for x in ids[:-1]), 'Deletion grammar')
                need(0 < ident <= last and len(set(ids[:-1])) == len(ids) - 1, 'Deletion identifiers')
                for i in ids[:-1]:
                    need(i in db, 'Unavailable deletion')
                    del db[i]
                deletions += len(ids) - 1
                continue
            need(ident > last, 'Fresh proof identifier')
            nums = list(map(int, tokens[1:]))
            need(nums.count(0) == 2 and nums[-1] == 0, 'Proof terminators')
            split = nums.index(0)
            proposed = nums[:split]
            hints = nums[split + 1:-1]
            need(hints and all(h > 0 for h in hints), 'Positive RUP hints required')
            new_clause = literal_set(proposed, nv)
            # All literals of the proposed clause are initially false.
            false = set(new_clause)
            true = {-x for x in new_clause}
            conflict = False
            for offset, h in enumerate(hints):
                need(h in db, 'Unavailable proof hint')
                row = db[h]
                hint_reads += 1
                need(row.isdisjoint(true), 'Satisfied hint')
                pending = row.difference(false)
                need(len(pending) <= 1, 'Nonunit hint')
                if not pending:
                    need(offset == len(hints) - 1, 'Hints after conflict')
                    conflict = True
                else:
                    unit = next(iter(pending))
                    true.add(unit)
                    false.add(-unit)
            need(conflict, 'No RUP conflict')
            db[ident] = new_clause
            last = ident
            additions += 1
            finished = not proposed
    need(finished, 'No terminal empty clause')
    return {'status': 'SIGNED_SET_RUP_EMPTY_CLAUSE_VERIFIED',
            'variables': nv, 'input_clauses': count, 'proof_lines': lines,
            'RUP_additions': additions, 'deletions': deletions,
            'hint_reads': hint_reads, 'last_clause_id': last,
            'CNF_sha256': sha(cnf), 'LRAT_sha256': sha(proof)}
