"""Small independent checker for the positive-hint (RUP) subset of LRAT.

No solver, DRAT trimmer, or producer is imported. Every added clause must follow
by the listed unit propagations after its negation. RAT hints are rejected.
"""
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(clauses, variables, path):
    database = {i: tuple(c) for i, c in enumerate(clauses, 1)}
    last = len(clauses)
    additions = deletions = steps = 0
    empty = False
    for line_number, line in enumerate(Path(path).open(), 1):
        tokens = line.split()
        require(bool(tokens), 'empty proof line')
        ident = int(tokens[0])
        if len(tokens) > 1 and tokens[1] == 'd':
            values = list(map(int, tokens[2:]))
            require(values and values[-1] == 0 and 0 not in values[:-1], 'deletion format')
            for cid in values[:-1]:
                require(cid in database, 'deleting absent clause')
                del database[cid]
                deletions += 1
            continue
        require(not empty and ident > last, 'non-increasing ID or data after refutation')
        values = list(map(int, tokens[1:]))
        require(0 in values, 'missing clause terminator')
        split = values.index(0)
        clause, hints = values[:split], values[split+1:]
        require(hints and hints[-1] == 0 and all(h > 0 for h in hints[:-1]), 'non-RUP hints')
        require(all(0 < abs(v) <= variables for v in clause), 'literal out of range')
        require(len(set(clause)) == len(clause), 'duplicate literal')
        assignment = {}
        for lit in clause:
            var, val = abs(lit), lit < 0
            require(var not in assignment, 'tautological clause unsupported')
            assignment[var] = val
        conflict = False
        for offset, hint in enumerate(hints[:-1]):
            require(hint in database and not conflict, 'missing or trailing hint')
            unresolved = []
            for lit in database[hint]:
                value = assignment.get(abs(lit))
                require(value is None or value != (lit > 0), 'hint clause is satisfied')
                if value is None:
                    unresolved.append(lit)
            require(len(unresolved) <= 1, 'hint is not unit or conflicting')
            if not unresolved:
                conflict = True
            else:
                lit = unresolved[0]
                assignment[abs(lit)] = lit > 0
            steps += 1
        require(conflict, f'no RUP conflict at line {line_number}')
        database[ident] = tuple(clause)
        last = ident
        additions += 1
        empty = not clause
    require(empty, 'proof does not end in the empty clause')
    return {'additions': additions, 'deletions': deletions, 'hint_steps': steps, 'empty_clause': True}
