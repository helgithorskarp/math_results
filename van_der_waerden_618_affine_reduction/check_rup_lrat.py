"""Small exact checker for the RUP-only subset of text LRAT used here.

Clauses are Boolean disjunctions. Each addition must give a positive sequence
of unit-propagation clause IDs contradicting the negation of that addition.
RAT hints and malformed inputs are rejected. A checked empty clause is required.
The converter and SAT solver are not trusted by this checker.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_cnf(path):
    lines = path.read_text().splitlines()
    header = lines[0].split()
    require(len(header) == 4 and header[:2] == ['p', 'cnf'], 'invalid CNF header')
    n, m = map(int, header[2:])
    require(n > 0 and m >= 0 and len(lines) == m+1, 'CNF dimensions disagree')
    clauses = {}
    for cid, line in enumerate(lines[1:], 1):
        tokens = list(map(int, line.split()))
        require(tokens and tokens[-1] == 0 and 0 not in tokens[:-1], 'invalid CNF clause')
        clause = tokens[:-1]
        require(all(1 <= abs(lit) <= n for lit in clause), 'CNF literal outside domain')
        clauses[cid] = tuple(clause)
    return n, m, clauses


def check_addition(clause, hints, active):
    require(all(h > 0 for h in hints), 'RAT hints are unsupported')
    # Negate every literal in the proposed clause as a temporary assumption.
    values = {}
    for lit in clause:
        variable, false_value = abs(lit), int(lit < 0)
        if variable in values and values[variable] != false_value:
            return 0  # tautological proposed clause
        values[variable] = false_value
    steps = 0
    for hid in hints:
        require(hid in active, 'unknown or deleted hint clause')
        constraint = active[hid]
        unassigned = set()
        satisfied = False
        for lit in constraint:
            variable = abs(lit)
            if variable not in values:
                unassigned.add(lit)
            elif values[variable] == int(lit > 0):
                satisfied = True
                break
        if satisfied:
            continue  # this clause does not propagate anything
        steps += 1
        if not unassigned:
            return steps  # a contradiction under the temporary assumptions
        require(len(unassigned) == 1, 'hint is neither unit nor conflicting')
        lit = next(iter(unassigned))
        values[abs(lit)] = int(lit > 0)
    raise ValueError('addition has no checked propagation contradiction')


def verify(cnf, proof):
    n, original_count, active = read_cnf(cnf)
    maximum_id = original_count
    additions = deletions = hints_checked = 0
    empty_checked = False
    with proof.open() as stream:
        for line_number, line in enumerate(stream, 1):
            parts = line.split()
            require(parts and len(parts) >= 3, f'invalid proof line {line_number}')
            cid = int(parts[0])
            require(cid > 0, 'nonpositive clause ID')
            if parts[1] == 'd':
                tokens = list(map(int, parts[2:]))
                require(tokens and tokens[-1] == 0 and all(i > 0 for i in tokens[:-1]), 'invalid deletion')
                for hid in tokens[:-1]:
                    require(hid in active, 'deleting absent clause')
                    del active[hid]
                    deletions += 1
                continue
            tokens = list(map(int, parts[1:]))
            require(tokens.count(0) == 2 and tokens[-1] == 0, 'addition needs two terminators')
            split = tokens.index(0)
            clause, hints = tokens[:split], tokens[split+1:-1]
            require(cid > maximum_id and cid not in active, 'addition ID is not fresh and increasing')
            require(all(1 <= abs(lit) <= n for lit in clause), 'proof literal outside domain')
            hints_checked += check_addition(clause, hints, active)
            active[cid] = tuple(clause)
            maximum_id = cid
            additions += 1
            if not clause:
                empty_checked = True
    require(empty_checked, 'no checked empty clause')
    return {'status': 'EXACT_RUP_LRAT_VERIFIED', 'variables': n,
            'initial_clauses': original_count, 'checked_additions': additions,
            'deleted_clauses': deletions, 'propagation_hints_checked': hints_checked,
            'cnf_sha256': hashlib.sha256(cnf.read_bytes()).hexdigest(),
            'proof_sha256': hashlib.sha256(proof.read_bytes()).hexdigest(),
            'mathematical_exclusion': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cnf', type=Path)
    parser.add_argument('proof', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    try:
        result = verify(args.cnf, args.proof)
    except (ValueError, KeyError, IndexError) as error:
        print(json.dumps({'status': 'REJECTED', 'reason': str(error), 'mathematical_exclusion': False}))
        raise SystemExit(2)
    result['seconds'] = time.monotonic()-start
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
