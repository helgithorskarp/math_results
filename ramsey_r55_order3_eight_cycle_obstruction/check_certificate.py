#!/usr/bin/env python3
"""Elementary addition-only RUP replay and complete core-membership audit.

Every proof clause must follow by literal unit propagation after negating
its literals. Valid clauses are retained; neither RAT nor deletions are
needed. No generator, C++ checker, or solver implementation is imported.
"""
from pathlib import Path
import argparse
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parse_clause(tokens):
    values = tuple(map(int, tokens))
    require(values and values[-1] == 0 and 0 not in values[:-1], "clause syntax")
    require(len(set(values[:-1])) == len(values)-1, "duplicate literal")
    return values[:-1]


def read_core(path):
    rows = path.read_text().splitlines()
    header = rows[0].split()
    require(len(header) == 4 and header[:2] == ['p', 'cnf'], "core header")
    variables, count = map(int, header[2:])
    clauses = [parse_clause(line.split()) for line in rows[1:]]
    require(len(clauses) == count, "core clause count")
    require(all(1 <= abs(x) <= variables for c in clauses for x in c), "core variable range")
    return variables, clauses


def audit_membership(full_path, core):
    missing = {tuple(sorted(c)) for c in core}
    with full_path.open() as stream:
        header = next(stream).split()
        require(header[:2] == ['p', 'cnf'], "full header")
        count = 0
        for line in stream:
            count += 1
            missing.discard(tuple(sorted(parse_clause(line.split()))))
    require(count == int(header[3]), "full clause count")
    require(not missing, "core clause absent from full formula")


def unit_conflict(formula, assumptions):
    values = {}
    for lit in assumptions:
        variable, value = abs(lit), lit > 0
        if variable in values and values[variable] != value:
            return True
        values[variable] = value
    while True:
        changed = False
        for clause in formula:
            pending = []
            for lit in clause:
                if abs(lit) not in values:
                    pending.append(lit)
                elif values[abs(lit)] == (lit > 0):
                    break
            else:
                if not pending:
                    return True
                if len(pending) == 1:
                    lit = pending[0]
                    values[abs(lit)] = lit > 0
                    changed = True
        if not changed:
            return False


def replay(core, proof_lines, variables):
    require(proof_lines and proof_lines[-1] == '0', 'proof must end in the empty clause')
    formula = list(core)
    for index, line in enumerate(proof_lines, 1):
        clause = parse_clause(line.split())
        require(all(1 <= abs(x) <= variables for x in clause), 'proof variable range')
        require(unit_conflict(formula, [-x for x in clause]), f'non-RUP addition {index}')
        formula.append(clause)
    return dict(additions=len(proof_lines), verified=True)


def self_test():
    require(unit_conflict([(1, 2), (-1, 2)], (-2,)), "RUP fixture")
    for formula, proof in [([(-1, 2), (-2,)], ['1 0', '0']),
                           ([(1, 2)], ['0']), ([(1, 2)], ['3 0', '0']),
                           ([(1, 2)], ['1 0'])]:
        try:
            replay(formula, proof, 2)
        except ValueError:
            pass
        else:
            raise ValueError("invalid proof accepted")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', type=Path, required=True)
    parser.add_argument('--core', type=Path, required=True)
    parser.add_argument('--proof', type=Path, required=True)
    args = parser.parse_args()
    self_test()
    variables, core = read_core(args.core)
    audit_membership(args.full, core)
    proof = args.proof.read_text().splitlines()
    result = replay(core, proof, variables)
    require(proof[-1] == '0', "canonical final proof line")
    try:
        replay(core, proof[:-1], variables)
    except ValueError:
        pass
    else:
        raise ValueError("missing-empty mutation accepted")
    result.update(core_clauses=len(core), input_variables=variables, verified=True)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
