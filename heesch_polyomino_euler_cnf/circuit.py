"""Exact Boolean gates and a balanced unsigned counting circuit.

All bit vectors are least significant bit first.  Variables are positive integers,
negative integers are negated literals, and variable 1 is fixed to true.
"""
from dataclasses import dataclass, field


@dataclass
class Circuit:
    clauses: list[list[int]] = field(default_factory=lambda: [[1]])
    nv: int = 1
    gates: list[tuple[int, str, tuple[int, ...]]] = field(default_factory=list)

    @property
    def true(self):
        return 1

    @property
    def false(self):
        return -1

    def new(self):
        self.nv += 1
        return self.nv

    def clause(self, literals):
        literals = set(literals)
        if 1 in literals or any(-x in literals for x in literals):
            return
        literals.discard(-1)
        self.clauses.append(sorted(literals, key=lambda x: (abs(x), x)))

    def and_(self, literals):
        xs = set(literals)
        if -1 in xs or any(-x in xs for x in xs):
            return -1
        xs.discard(1)
        if not xs:
            return 1
        if len(xs) == 1:
            return next(iter(xs))
        xs = tuple(sorted(xs, key=lambda x: (abs(x), x)))
        z = self.new()
        for x in xs:
            self.clause([-z, x])
        self.clause([z, *(-x for x in xs)])
        self.gates.append((z, "and", xs))
        return z

    def or_(self, literals):
        return -self.and_(-x for x in literals)

    def xor(self, a, b):
        if a == -1:
            return b
        if b == -1:
            return a
        if a == 1:
            return -b
        if b == 1:
            return -a
        if a == b:
            return -1
        if a == -b:
            return 1
        z = self.new()
        for row in [(a, b, -z), (a, -b, z), (-a, b, z), (-a, -b, -z)]:
            self.clause(row)
        self.gates.append((z, "xor", (a, b)))
        return z

    def majority(self, a, b, c):
        xs = (a, b, c)
        if 1 in xs:
            remaining = list(xs)
            remaining.remove(1)
            return self.or_(remaining)
        if -1 in xs:
            remaining = list(xs)
            remaining.remove(-1)
            return self.and_(remaining)
        for x in xs:
            if xs.count(x) >= 2:
                return x
            if -x in xs:
                return next(y for y in xs if y not in (x, -x))
        z = self.new()
        for x, y in [(a, b), (a, c), (b, c)]:
            self.clause([-x, -y, z])
            self.clause([x, y, -z])
        self.gates.append((z, "majority", xs))
        return z

    def add(self, a, b):
        carry = -1
        output = []
        for i in range(max(len(a), len(b))):
            x = a[i] if i < len(a) else -1
            y = b[i] if i < len(b) else -1
            output.append(self.xor(self.xor(x, y), carry))
            carry = self.majority(x, y, carry)
        output.append(carry)
        return output

    def count(self, literals):
        vectors = [[x] for x in literals]
        if not vectors:
            return [-1]
        while len(vectors) > 1:
            vectors = [self.add(vectors[i], vectors[i + 1])
                       if i + 1 < len(vectors) else vectors[i]
                       for i in range(0, len(vectors), 2)]
        return vectors[0]

    def equal_count(self, literals, target):
        xs = list(literals)
        target -= xs.count(1)
        xs = [x for x in xs if abs(x) != 1]
        if not 0 <= target <= len(xs):
            self.clause([])
            return
        total = self.count(xs)
        for i, x in enumerate(total):
            self.clause([x if (target >> i) & 1 else -x])

    def evaluate(self, inputs):
        """Definition-level deterministic evaluation, independent of a solver."""
        values = {1: True, **inputs}

        def literal(x):
            return values[abs(x)] if x > 0 else not values[abs(x)]

        for z, operation, xs in self.gates:
            bits = [literal(x) for x in xs]
            if operation == "and":
                values[z] = all(bits)
            elif operation == "xor":
                values[z] = bits[0] != bits[1]
            elif operation == "majority":
                values[z] = sum(bits) >= 2
            else:
                raise ValueError(operation)
        return all(any(literal(x) for x in clause) for clause in self.clauses)

    def write_dimacs(self, path):
        with open(path, "w") as out:
            out.write(f"p cnf {self.nv} {len(self.clauses)}\n")
            for clause in self.clauses:
                out.write(" ".join(map(str, clause)) + " 0\n")
