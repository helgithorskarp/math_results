#!/usr/bin/env python3
"""Check every text-proof addition by reverse unit propagation (RUP).

Deletions are ignored: retaining already justified clauses is sound for RUP.
No solver, SAT library, or floating-point computation is used.
"""
import argparse
import hashlib
import json
from collections import deque
from pathlib import Path


class Formula:
    def __init__(self, variables):
        self.variables = variables
        self.clauses = []
        self.lengths = []
        self.occurrences = [[] for _ in range(2 * variables + 1)]
        self.units = []
        self.has_empty = False

    def add(self, clause):
        index = len(self.clauses)
        self.clauses.append(clause)
        self.lengths.append(len(clause))
        for literal in clause:
            self.occurrences[literal + self.variables].append(index)
        if len(clause) == 1:
            self.units.append(clause[0])
        if not clause:
            self.has_empty = True

    def rup(self, clause):
        if self.has_empty:
            return True
        values = [0] * (self.variables + 1)
        remaining = self.lengths.copy()
        satisfied = bytearray(len(self.clauses))
        queue = deque(self.units)
        queue.extend(-v for v in clause)
        while queue:
            literal = queue.popleft()
            variable, value = abs(literal), 1 if literal > 0 else -1
            if values[variable]:
                if values[variable] != value:
                    return True
                continue
            values[variable] = value
            for index in self.occurrences[literal + self.variables]:
                satisfied[index] = 1
            for index in self.occurrences[-literal + self.variables]:
                if satisfied[index]:
                    continue
                remaining[index] -= 1
                if remaining[index] == 0:
                    return True
                if remaining[index] == 1:
                    unknown = [v for v in self.clauses[index] if values[abs(v)] == 0]
                    if len(unknown) != 1:
                        raise ValueError("Propagation bookkeeping failure")
                    queue.append(unknown[0])
        return False


def parse_clause(tokens, variables):
    integers = list(map(int, tokens))
    if not integers or integers[-1] != 0 or 0 in integers[:-1]:
        raise ValueError("Malformed clause")
    clause = integers[:-1]
    if any(abs(v) > variables for v in clause) or len(set(clause)) != len(clause):
        raise ValueError("Invalid or duplicate literal")
    if any(-v in clause for v in clause):
        raise ValueError("Tautological clause outside this certificate format")
    return clause


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("proof", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    lines = args.cnf.read_text().splitlines()
    header = lines.pop(0).split()
    if len(header) != 4 or header[:2] != ["p", "cnf"]:
        raise ValueError("Invalid DIMACS header")
    variables, count = map(int, header[2:])
    if variables < 0 or count != len(lines):
        raise ValueError("Invalid DIMACS size")
    formula = Formula(variables)
    for line in lines:
        formula.add(parse_clause(line.split(), variables))
    additions = deletions = 0
    derived_empty = False
    for number, line in enumerate(args.proof.read_text().splitlines(), 1):
        tokens = line.split()
        if not tokens:
            raise ValueError("Blank proof line")
        deleting = tokens[0] == "d"
        clause = parse_clause(tokens[1:] if deleting else tokens, variables)
        if deleting:
            deletions += 1
            continue
        if not formula.rup(clause):
            raise ValueError(f"Addition on line {number} is not RUP")
        formula.add(clause)
        additions += 1
        derived_empty |= not clause
    if not derived_empty:
        raise ValueError("Proof never derives an empty clause")
    result = {"verified": True, "method": "all additions RUP; deletions ignored",
              "variables": variables, "input_clauses": count,
              "additions": additions, "deletions": deletions,
              "cnf_sha256": hashlib.sha256(args.cnf.read_bytes()).hexdigest(),
              "proof_sha256": hashlib.sha256(args.proof.read_bytes()).hexdigest()}
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
