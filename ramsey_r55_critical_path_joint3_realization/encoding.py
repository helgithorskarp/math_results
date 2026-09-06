"""Copied threshold/lex primitives; provenance in README; not trusted for graph theorem."""
class CounterEncoder:
    """s[i,j] iff at least j of the first i literals are true."""
    def __init__(self, variables, clauses):
        self.variables = variables
        self.clauses = list(clauses)

    @staticmethod
    def neg(literal):
        return not literal if type(literal) is bool else -literal

    def add(self, *literals):
        if any(lit is True for lit in literals):
            return
        self.clauses.append(tuple(lit for lit in literals if lit is not False))

    def interval(self, literals, lower, upper):
        n = len(literals)
        lower, upper = max(lower, 0), min(upper, n)
        if lower > upper:
            self.add()
            return
        previous = [True]+[False]*(upper+1)
        for i, literal in enumerate(literals, 1):
            current = [True]
            for j in range(1, upper+2):
                if j > i:
                    current.append(False)
                    continue
                self.variables += 1
                s, a, b = self.variables, previous[j], previous[j-1]
                # s <=> a OR (literal AND b).
                self.add(self.neg(a), s)
                self.add(self.neg(literal), self.neg(b), s)
                self.add(-s, a, literal)
                self.add(-s, a, b)
                current.append(s)
            previous = current
        if lower:
            self.add(previous[lower])
        self.add(self.neg(previous[upper+1]))


def add_lex(enc, left, right):
    same = True
    for a, b in zip(left, right):
        enc.add(enc.neg(same), -a, b)
        enc.variables += 1
        nxt = enc.variables
        enc.add(-nxt, same)
        enc.add(-nxt, -a, b)
        enc.add(-nxt, a, -b)
        enc.add(enc.neg(same), a, b, nxt)
        enc.add(enc.neg(same), -a, -b, nxt)
        same = nxt
