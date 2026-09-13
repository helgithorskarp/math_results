"""Small solver-independent helpers for the sealed-pool certificate."""
from __future__ import annotations

import base64
import hashlib
from pathlib import Path


def pack_colours(word: str) -> str:
    raw = bytearray((len(word) + 3) // 4)
    for i, ch in enumerate(word):
        c = ord(ch) - ord("0")
        if c not in range(4):
            raise ValueError("colour outside 0,...,3")
        raw[i // 4] |= c << (2 * (i % 4))
    return base64.b64encode(raw).decode()


def unpack_colours(data: str, length: int) -> str:
    raw = base64.b64decode(data, validate=True)
    if len(raw) != (length + 3) // 4:
        raise ValueError("wrong packed-colour length")
    word = "".join(str((raw[i // 4] >> (2 * (i % 4))) & 3)
                   for i in range(length))
    if length % 4 and raw[-1] >> (2 * (length % 4)):
        raise ValueError("nonzero packed-colour padding")
    return word


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CNF:
    """A deterministic Tseitin CNF with selector variables allocated first."""

    def __init__(self, selectors: int):
        self.nvars = selectors
        self.clauses: list[list[int]] = []

    def new(self) -> int:
        self.nvars += 1
        return self.nvars

    def xor(self, z: int, a: int, b: int) -> None:
        # z <-> a xor b; a and b may themselves be negative literals.
        self.clauses += [[a, b, -z], [a, -b, z],
                         [-a, b, z], [-a, -b, -z]]

    def land(self, z: int, a: int, b: int) -> None:
        # z <-> a and b.
        self.clauses += [[-z, a], [-z, b], [z, -a, -b]]

    def count_exact(self, literals: list[int], target: int) -> None:
        """Ripple-add literals to a binary counter and pin its final value."""
        if not 0 <= target <= len(literals):
            self.clauses.append([])
            return
        width = (len(literals) + 1).bit_length()
        previous = [self.new() for _ in range(width)]
        self.clauses += [[-v] for v in previous]
        for literal in literals:
            carry = literal
            current = []
            for bit in previous:
                value = self.new()
                next_carry = self.new()
                self.xor(value, bit, carry)
                self.land(next_carry, bit, carry)
                current.append(value)
                carry = next_carry
            self.clauses.append([-carry])
            previous = current
        for j, bit in enumerate(previous):
            self.clauses.append([bit if (target >> j) & 1 else -bit])

    def at_most(self, literals: list[int], bound: int) -> None:
        """Sinz sequential counter for sum(literals) <= bound."""
        n = len(literals)
        if bound < 0:
            self.clauses.append([])
            return
        if bound >= n:
            return
        if bound == 0:
            self.clauses += [[-x] for x in literals]
            return
        s = [[self.new() for _ in range(bound)] for _ in range(n - 1)]
        self.clauses.append([-literals[0], s[0][0]])
        self.clauses += [[-s[0][j]] for j in range(1, bound)]
        for i in range(1, n - 1):
            self.clauses += [[-literals[i], s[i][0]],
                             [-s[i - 1][0], s[i][0]]]
            for j in range(1, bound):
                self.clauses += [
                    [-literals[i], -s[i - 1][j - 1], s[i][j]],
                    [-s[i - 1][j], s[i][j]],
                ]
        for i in range(1, n):
            self.clauses.append([-literals[i], -s[i - 1][bound - 1]])

    def dimacs(self) -> bytes:
        lines = [f"p cnf {self.nvars} {len(self.clauses)}\n"]
        lines.extend(" ".join(map(str, clause)) + " 0\n"
                     for clause in self.clauses)
        return "".join(lines).encode()


def selector_cnf(pool: list[int], q5: list[int], killing_sets: list[list[int]],
                 order: int = 134, q5_bound: int = 6) -> CNF:
    index = {v: i + 1 for i, v in enumerate(pool)}
    if len(index) != len(pool):
        raise ValueError("repeated pool label")
    cnf = CNF(len(pool))
    cnf.count_exact([index[v] for v in pool], order)
    cnf.at_most([index[v] for v in q5], q5_bound)
    for killing in killing_sets:
        cnf.clauses.append([index[v] for v in killing])
    return cnf


def selector_exact_q_cnf(pool: list[int], q5: list[int],
                         killing_sets: list[list[int]], q_count: int,
                         order: int = 134) -> CNF:
    index = {v: i + 1 for i, v in enumerate(pool)}
    if len(index) != len(pool):
        raise ValueError("repeated pool label")
    cnf = CNF(len(pool))
    cnf.count_exact([index[v] for v in pool], order)
    cnf.count_exact([index[v] for v in q5], q_count)
    for killing in killing_sets:
        cnf.clauses.append([index[v] for v in killing])
    return cnf
