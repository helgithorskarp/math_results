"""Exact Boolean comparator encoding; clauses are streamed to a single SAT solver."""
import hashlib
import itertools
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

def scalar(n, gates, x):
    """Direct Boolean-list simulation, independent of the SAT recurrence."""
    bits = [(x >> i) & 1 for i in range(n)]
    for a, b in gates:
        if bits[a] > bits[b]:
            bits[a], bits[b] = bits[b], bits[a]
    return bits


def failures(n, gates, states):
    return [x for x in states if scalar(n, gates, x) !=
            [0] * (n - x.bit_count()) + [1] * x.bit_count()]


class Encoding:
    def __init__(self, n, budget, solver_name='m22', body_file=None):
        self.n, self.budget = n, budget
        self.pairs = list(itertools.combinations(range(n), 2))
        self.solver = Solver(name=solver_name)
        self.top = 0
        self.clauses = 0
        self.hash = hashlib.sha256()
        self.body_file = body_file
        self.choice = [[self.new() for p in self.pairs] for t in range(budget)]
        self.used = [[self.new() for i in range(n)] for t in range(budget)]
        self.rows = {}
        for t in range(budget):
            if not self.choice[t]:
                self.add([])
            else:
                self.card(self.choice[t], 1)
            for i in range(n):
                incident = [self.choice[t][k] for k, p in enumerate(self.pairs) if i in p]
                for c in incident:
                    self.add([-c, self.used[t][i]])
                self.add([-self.used[t][i]] + incident)

    def new(self):
        self.top += 1
        return self.top

    def add(self, clause):
        self.clauses += 1
        line = ' '.join(map(str, clause)) + ' 0\n'
        self.hash.update(line.encode('ascii'))
        if self.body_file is not None:
            self.body_file.write(line)
        self.solver.add_clause(clause)

    def card(self, literals, bound):
        cnf = CardEnc.equals(lits=literals, bound=bound,
                             top_id=self.top, encoding=EncType.seqcounter)
        self.top = max(self.top, cnf.nv)
        for c in cnf.clauses:
            self.add(c)

    def add_row(self, x, final_sorted=True):
        if x in self.rows:
            return
        n = self.n
        assert 0 <= x < 2 ** n
        v = [[self.new() for i in range(n)] for t in range(self.budget + 1)]
        self.rows[x] = v
        for i in range(n):
            self.add([v[0][i] if x >> i & 1 else -v[0][i]])
            if final_sorted:
                self.add([v[-1][i] if i >= n - x.bit_count() else -v[-1][i]])
        for t in range(self.budget):
            vin, out = v[t], v[t + 1]
            for i in range(n):
                u = self.used[t][i]
                self.add([u, -out[i], vin[i]])
                self.add([u, out[i], -vin[i]])
            for k, (a, b) in enumerate(self.pairs):
                c = self.choice[t][k]
                # c => out[a] = vin[a] AND vin[b].
                self.add([-c, -out[a], vin[a]])
                self.add([-c, -out[a], vin[b]])
                self.add([-c, out[a], -vin[a], -vin[b]])
                # c => out[b] = vin[a] OR vin[b].
                self.add([-c, out[b], -vin[a]])
                self.add([-c, out[b], -vin[b]])
                self.add([-c, -out[b], vin[a], vin[b]])

    def root_hits(self, x, count):
        assert x.bit_count() == 1
        self.add_row(x)
        v = self.rows[x]
        hits = [self.new() for t in range(self.budget)]
        for t in range(self.budget):
            for k, (a, b) in enumerate(self.pairs):
                c = self.choice[t][k]
                self.add([-c, -v[t][a], hits[t]])
                self.add([-c, -v[t][b], hits[t]])
                self.add([-c, v[t][a], v[t][b], -hits[t]])
        self.card(hits, count)

    def touch_bound(self, x, bound, polarity=1):
        """Bound gates touched by fixed maxima (1) or fixed minima (0)."""
        if bound >= self.budget:
            return
        if bound < 0:
            self.add([])
            return
        self.add_row(x)
        v = self.rows[x]
        hits = [self.new() for t in range(self.budget)]
        for t in range(self.budget):
            for k, (a, b) in enumerate(self.pairs):
                c = self.choice[t][k]
                va = v[t][a] if polarity else -v[t][a]
                vb = v[t][b] if polarity else -v[t][b]
                self.add([-c, -va, hits[t]])
                self.add([-c, -vb, hits[t]])
                self.add([-c, va, vb, -hits[t]])
        cnf = CardEnc.atmost(lits=hits, bound=bound, top_id=self.top,
                            encoding=EncType.seqcounter)
        self.top = max(self.top, cnf.nv)
        for clause in cnf.clauses:
            self.add(clause)

    def assume_gates(self, gates):
        assert len(gates) == self.budget
        return [self.choice[t][self.pairs.index(tuple(p))] for t, p in enumerate(gates)]

    def decode(self):
        model = set(self.solver.get_model())
        result = []
        for row in self.choice:
            picked = [p for c, p in zip(row, self.pairs) if c in model]
            assert len(picked) == 1, picked
            result.append(picked[0])
        return result

    def describe(self):
        return {'variables': self.top, 'clauses': self.clauses,
                'clause_stream_sha256': self.hash.hexdigest(),
                'rows': len(self.rows), 'solver_stats': self.solver.accum_stats()}
