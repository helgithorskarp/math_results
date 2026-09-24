"""Explicit Tseitin, saturated-counter, and lexicographic CNF primitives.

Adapted without changing clause order from the public orbit-51 generator.
No third-party cardinality encoder is used.
"""

import itertools


class Cnf:
    def __init__(self) -> None:
        self.nvars = 0
        self.clauses: list[list[int]] = []

    def var(self) -> int:
        self.nvars += 1
        return self.nvars

    def and_var(self, lits: list[int]) -> int:
        out = self.var()
        self.clauses.extend([[-out, lit] for lit in lits])
        self.clauses.append([out] + [-lit for lit in lits])
        return out

    def count_states(self, lits: list[int], cap: int, initial: int = 0) -> list[int]:
        """Return exact saturated-count states after all literals.

        State j means the count equals j for j < cap; state cap means the
        count is at least cap.  Each row is one-hot and transitions are exact.
        """
        if not 0 <= initial <= cap:
            raise ValueError("invalid initial counter state")
        states = [[self.var() for _ in range(cap + 1)]
                  for _ in range(len(lits) + 1)]
        for row in states:
            self.clauses.append(row)
            for a, b in itertools.combinations(row, 2):
                self.clauses.append([-a, -b])
        self.clauses.append([states[0][initial]])
        for i, lit in enumerate(lits):
            for j in range(cap + 1):
                self.clauses.append([-states[i][j], lit, states[i + 1][j]])
                nxt = min(j + 1, cap)
                self.clauses.append([-states[i][j], -lit, states[i + 1][nxt]])
        return states[-1]

    def exactly(self, lits: list[int], value: int) -> None:
        final = self.count_states(lits, value + 1)
        self.clauses.append([final[value]])

    def lex_le(self, left: list[int], right: list[int], strict: bool = False) -> None:
        """Enforce Boolean lex order left <= right with 0 < 1."""
        if len(left) != len(right):
            raise ValueError("unequal lexicographic word lengths")
        prefix = self.var()
        self.clauses.append([prefix])
        for a, b in zip(left, right):
            self.clauses.append([-prefix, -a, b])
            following = self.var()
            self.clauses.append([-following, prefix])
            self.clauses.append([-following, -a, b])
            self.clauses.append([-following, a, -b])
            self.clauses.append([-prefix, -a, -b, following])
            self.clauses.append([-prefix, a, b, following])
            prefix = following
        if strict:
            self.clauses.append([-prefix])
