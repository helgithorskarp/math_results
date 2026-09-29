"""Small solver-free checker for a deletion-free reverse-unit-propagation proof.

A proof clause C is accepted only if unit propagation derives a contradiction
from the already accepted formula together with the negation of every literal
of C.  The last proof clause must be empty.  No RAT steps or deletions are accepted.
"""
from collections import defaultdict, deque
import argparse
import hashlib
import json
from pathlib import Path
import time


def read_dimacs(path):
    nv = declared = None
    clauses, current = [], []
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith("c"):
            continue
        if line.startswith("p"):
            words = line.split()
            if nv is not None or len(words) != 4 or words[:2] != ["p", "cnf"]:
                raise ValueError("malformed DIMACS header")
            nv, declared = map(int, words[2:])
            continue
        if nv is None:
            raise ValueError("clauses before header")
        for literal in map(int, line.split()):
            if literal:
                if abs(literal) > nv:
                    raise ValueError("out of range literal")
                current.append(literal)
            else:
                clauses.append(tuple(dict.fromkeys(current)))
                current = []
    if nv is None or current or len(clauses) != declared:
        raise ValueError("incomplete or incorrectly counted CNF")
    return nv, clauses


class Propagator:
    def __init__(self, nv, clauses):
        self.nv = nv
        self.clauses = []
        self.occurrences = defaultdict(list)
        self.units = []
        self.empty = False
        for clause in clauses:
            self.add(clause)

    def add(self, clause):
        clause = tuple(dict.fromkeys(clause))
        if any(-x in clause for x in clause):
            return  # tautologies do not affect propagation
        if not clause:
            self.empty = True
        if len(clause) == 1:
            self.units.append(clause[0])
        index = len(self.clauses)
        self.clauses.append(clause)
        for literal in clause:
            self.occurrences[literal].append(index)

    def conflict(self, assumptions):
        if self.empty:
            return True
        # Every check starts from scratch: no learned or solver state is trusted.
        values = [-1] * (self.nv + 1)
        remaining = [len(clause) for clause in self.clauses]
        satisfied = bytearray(len(self.clauses))
        queue = deque([*self.units, *assumptions])
        while queue:
            literal = queue.popleft()
            v, desired = abs(literal), int(literal > 0)
            if not 1 <= v <= self.nv:
                raise ValueError("out of range assumption")
            if values[v] != -1:
                if values[v] != desired:
                    return True
                continue
            values[v] = desired
            for index in self.occurrences[literal]:
                satisfied[index] = 1
            for index in self.occurrences[-literal]:
                if satisfied[index]:
                    continue
                remaining[index] -= 1
                if remaining[index] == 0:
                    return True
                if remaining[index] == 1:
                    candidates = [x for x in self.clauses[index] if values[abs(x)] == -1]
                    if len(candidates) != 1:
                        raise AssertionError("unit-propagation invariant failure")
                    queue.append(candidates[0])
        return False


def verify(cnf, proof):
    nv, clauses = read_dimacs(cnf)
    propagator = Propagator(nv, clauses)
    count = 0
    last = None
    for number, line in enumerate(proof.read_text().splitlines(), 1):
        if not line.strip() or line.startswith("c"):
            continue
        words = line.split()
        if words[0] in ("d", "a"):
            raise ValueError("only deletion-free RUP is supported")
        literals = list(map(int, words))
        if not literals or literals[-1] != 0 or 0 in literals[:-1]:
            raise ValueError("proof clause must end in a single zero")
        clause = tuple(dict.fromkeys(literals[:-1]))
        if any(abs(x) > nv for x in clause):
            raise ValueError("out of range proof variable")
        if not propagator.conflict(-x for x in clause):
            raise ValueError(f"non-RUP clause on line {number}")
        propagator.add(clause)
        count += 1
        last = clause
    if last != ():
        raise ValueError("proof does not end with a checked empty clause")
    return {"result": "VERIFIED UNSAT", "variables": nv, "input_clauses": len(clauses),
            "proof_clauses": count, "cnf_sha256": hashlib.sha256(cnf.read_bytes()).hexdigest(),
            "proof_sha256": hashlib.sha256(proof.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("proof", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    result = verify(args.cnf, args.proof)
    result["elapsed_seconds"] = round(time.monotonic() - start, 3)
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
