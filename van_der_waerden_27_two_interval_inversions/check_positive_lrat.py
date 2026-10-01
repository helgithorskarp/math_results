"""Strict positive-hint RUP certificate checking with Python integers and dictionaries.

The bounded case domain comprises input clauses, added proof obligations and
deleted clause identifiers. Hint-clause reads and literal inspections are also
reported separately; they are the work within each proof obligation.
No SAT solver, CNF constructor, or upstream proof checker is imported.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import sys
import time


class InvalidProof(ValueError):
    pass


def require(ok, reason):
    if not ok:
        raise InvalidProof(reason)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify(cnf, lrat):
    formula = {}
    cases = hints_checked = literals_checked = assumptions = 0
    with cnf.open() as stream:
        header = next(stream).split()
        require(len(header) == 4 and header[:2] == ['p', 'cnf'], 'DIMACS header')
        variables, count = map(int, header[2:])
        require(variables > 0 and 0 < count <= 200000, 'Positive bounded CNF dimensions')
        for index, line in enumerate(stream, 1):
            row = list(map(int, line.split()))
            require(row and row[-1] == 0 and all(0 < abs(lit) <= variables for lit in row[:-1]), 'DIMACS clause')
            clause = tuple(row[:-1])
            require(len(set(clause)) == len(clause) and not set(clause).intersection(-lit for lit in clause), 'Non-tautological unique literals')
            formula[index] = clause
            cases += 1
            literals_checked += len(clause)
        require(len(formula) == count, 'Complete CNF row count')
    last, added, deleted, lines, empty = count, 0, 0, 0, False
    with lrat.open() as stream:
        for line in stream:
            require(not empty, 'Proof content follows terminal empty clause')
            fields = line.split()
            require(len(fields) >= 3, 'LRAT line')
            label = int(fields[0])
            lines += 1
            if fields[1] == 'd':
                ids = list(map(int, fields[2:]))
                require(ids and ids[-1] == 0 and all(i > 0 for i in ids[:-1]), 'Deletion identifiers')
                require(0 < label <= last and len(set(ids[:-1])) == len(ids) - 1, 'Deletion label/unique ids')
                for ident in ids[:-1]:
                    require(ident in formula, 'Deleting unavailable clause')
                    del formula[ident]
                deleted += len(ids) - 1
                cases += len(ids) - 1
            else:
                require(label > last, 'Fresh increasing proof clause identifiers')
                integers = list(map(int, fields[1:]))
                require(integers.count(0) == 2 and integers[-1] == 0, 'Clause and hint terminators')
                split = integers.index(0)
                clause, hints = integers[:split], integers[split + 1:-1]
                require(all(0 < abs(lit) <= variables for lit in clause), 'Actual variable domain')
                require(len(set(clause)) == len(clause) and not set(clause).intersection(-lit for lit in clause), 'Non-tautological proof clause')
                require(hints and all(hint > 0 for hint in hints), 'Mandatory positive RUP hints; RAT unsupported')
                require(all(hint in formula for hint in hints), 'Unavailable proof hint')
                # Negate every proposed literal. Only actual unit clauses may
                # extend this temporary assignment, and an actual all-false
                # clause must terminate the hint chain.
                truth = {abs(lit): lit < 0 for lit in clause}
                assumptions += len(clause)
                conflict = False
                for position, hint in enumerate(hints):
                    hinted = formula[hint]
                    unassigned, satisfied = [], False
                    hints_checked += 1
                    for lit in hinted:
                        literals_checked += 1
                        value = truth.get(abs(lit))
                        if value is None:
                            unassigned.append(lit)
                        elif value == (lit > 0):
                            satisfied = True
                    require(not satisfied, 'Satisfied hint cannot justify RUP propagation')
                    require(len(unassigned) <= 1, 'Hint is not an actual unit or false clause')
                    if not unassigned:
                        require(position == len(hints) - 1, 'Hints extend beyond actual conflict')
                        conflict = True
                        break
                    lit = unassigned[0]
                    truth[abs(lit)] = lit > 0
                require(conflict, 'RUP hint chain has no actual contradiction')
                formula[label] = tuple(clause)
                last, added, empty = label, added + 1, not clause
                cases += 1
            require(cases <= 200000, 'Unchanged200000 proof-obligation/deletion case cap')
    require(empty, 'No verified terminal empty clause')
    return {'status': 'ALL_POSITIVE_RUP_HINTS_VERIFIED_AND_EMPTY_CLAUSE_DERIVED',
            'CNF_variables': variables, 'CNF_clauses': count, 'proof_lines': lines,
            'added_RUP_clauses': added, 'deleted_identifiers': deleted, 'last_clause_id': last,
            'proof_obligation_cases': cases, 'hint_clause_reads': hints_checked,
            'literal_inspections': literals_checked, 'negated_clause_literals': assumptions,
            'RAT_supported_or_trusted': False, 'solver_or_encoder_imported': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--CNF', type=Path, required=True)
    parser.add_argument('--LRAT', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'Existing proof evidence')
    began = time.monotonic()
    result = verify(args.CNF, args.LRAT)
    result.update(agent='six-vdw-1', role='researcher', checked_at=datetime.now(timezone.utc).isoformat(),
                  CNF_sha256=sha(args.CNF), LRAT_sha256=sha(args.LRAT), checker_sha256=sha(__file__),
                  interpreter_optimization=sys.flags.optimize, seconds=time.monotonic() - began,
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, threads=1, new_W_bound=None)
    require(result['seconds'] < 30, 'Unchanged30-second proof child limit')
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
