"""Size-preserving tail constraints. Published baseline remains unchanged.

Interval constraints are only complete for a nonredundant global sorter;
the size-44 lower bound supplies that hypothesis in the twenty-gate frontier.
Pure-side constraints and fixed edge bits need no nonredundancy hypothesis.
"""
import itertools
from pysat.card import CardEnc, EncType
from sat_encoding import Encoding as BaseEncoding


def canonicalize(gates):
    """Swap reversed adjacent disjoint pairs until locally lexicographic."""
    result = [tuple(p) for p in gates]
    swaps = 0
    changed = True
    while changed:
        changed = False
        for t in range(len(result) - 1):
            p, q = result[t:t + 2]
            if p > q and not set(p).intersection(q):
                result[t:t + 2] = q, p
                changed = True
                swaps += 1
    return result, swaps


class Encoding(BaseEncoding):
    def __init__(self, n, budget, solver_name='m22', body_file=None,
                 constants=True, intervals=True, pure_sides=True,
                 disjoint_lex=True):
        self.true = None
        self.constants = constants
        self.intervals = intervals
        self.pure_sides = pure_sides
        self.disjoint_lex = disjoint_lex
        self.skipped_tautologies = 0
        self.attempted_clauses = 0
        self.state_variables = 0
        self.mixed_bounds = 0
        self.route_branch_kind = None
        self.phase_gate_bans = False
        self.branch_shortcut_pairs = []
        self.permanent_redundancies = []
        super().__init__(n, budget, solver_name, body_file)
        if constants:
            fixed = self.new()
            self.add([fixed])
            self.true = fixed
        self.future = None
        before = self.clauses
        if intervals or pure_sides:
            self.add_future()
        self.future_clause_count = self.clauses - before
        before = self.clauses
        if disjoint_lex:
            for t in range(budget - 1):
                for q, upper in enumerate(self.pairs):
                    for p, lower in enumerate(self.pairs[:q]):
                        if not set(upper).intersection(lower):
                            self.add([-self.choice[t][q], -self.choice[t + 1][p]])
        self.lex_clause_count = self.clauses - before

    def add(self, clause):
        self.attempted_clauses += 1
        simplified = []
        seen = set()
        for lit in clause:
            if self.true is not None:
                if lit == self.true:
                    self.skipped_tautologies += 1
                    return
                if lit == -self.true:
                    continue
            if -lit in seen:
                self.skipped_tautologies += 1
                return
            if lit not in seen:
                simplified.append(lit)
                seen.add(lit)
        super().add(simplified)

    def add_future(self):
        n, m = self.n, self.budget
        e = [[self.new() for i in range(n - 1)] for t in range(m)]
        if self.true is None:
            e.append([self.new() for i in range(n - 1)])
            for lit in e[-1]:
                self.add([-lit])
        else:
            e.append([-self.true] * (n - 1))
        self.future = e
        for t in range(m):
            for i in range(n - 1):
                crosses = [self.choice[t][k] for k, (a, b) in enumerate(self.pairs)
                           if a <= i < b]
                # e[t,i] iff e[t+1,i] OR a selected gate crossing i|i+1.
                self.add([-e[t + 1][i], e[t][i]])
                for c in crosses:
                    self.add([-c, e[t][i]])
                self.add([-e[t][i], e[t + 1][i]] + crosses)
            if self.intervals:
                for k, (a, b) in enumerate(self.pairs):
                    for i, j in itertools.combinations(range(a, b), 2):
                        self.add([-self.choice[t][k], e[t + 1][i], e[t + 1][j]])

    def add_row(self, x, final_sorted=True):
        if x in self.rows:
            return
        n, m = self.n, self.budget
        assert 0 <= x < 2 ** n
        first_one = (x & -x).bit_length() - 1 if x else n
        zeros = ((1 << n) - 1) ^ x
        last_zero = zeros.bit_length() - 1

        def state(i):
            if self.constants and i < first_one:
                return -self.true
            if self.constants and i > last_zero:
                return self.true
            self.state_variables += 1
            return self.new()

        v = [[state(i) for i in range(n)] for t in range(m + 1)]
        self.rows[x] = v
        for i in range(n):
            self.add([v[0][i] if x >> i & 1 else -v[0][i]])
            if final_sorted:
                self.add([v[-1][i] if i >= n - x.bit_count() else -v[-1][i]])
        for t in range(m):
            vin, out = v[t], v[t + 1]
            for i in range(n):
                u = self.used[t][i]
                self.add([u, -out[i], vin[i]])
                self.add([u, out[i], -vin[i]])
            for k, (a, b) in enumerate(self.pairs):
                c = self.choice[t][k]
                self.add([-c, -out[a], vin[a]])
                self.add([-c, -out[a], vin[b]])
                self.add([-c, out[a], -vin[a], -vin[b]])
                self.add([-c, out[b], -vin[a]])
                self.add([-c, out[b], -vin[b]])
                self.add([-c, -out[b], vin[a], vin[b]])
        if self.pure_sides and final_sorted:
            for t in range(m + 1):
                for i in range(n - 1):
                    if i < n - x.bit_count():
                        for j in range(i + 1):
                            self.add([self.future[t][i], -v[t][j]])
                    if i >= n - x.bit_count() - 1:
                        for j in range(i + 1, n):
                            self.add([self.future[t][i], v[t][j]])

    def describe(self):
        return {**super().describe(),
                'filters': {'fixed_edge_constants': self.constants,
                            'future_intervals': self.intervals,
                            'pure_sides': self.pure_sides,
                            'adjacent_disjoint_lex': self.disjoint_lex},
                'state_variables': self.state_variables,
                'mixed_bounds': self.mixed_bounds,
                'route_branch': self.route_branch_kind,
                'phase_gate_bans': self.phase_gate_bans,
                'branch_shortcut_pairs': self.branch_shortcut_pairs,
                'permanent_redundancies': self.permanent_redundancies,
                'future_clause_count': self.future_clause_count,
                'lex_clause_count': self.lex_clause_count,
                'attempted_clauses': self.attempted_clauses,
                'skipped_tautologies': self.skipped_tautologies}

    def mixed_touch_bound(self, x, y, bound):
        """Bound touching a tracked high value OR tracked low value.

        x is the high-threshold row and y the nonlow-threshold row, x<=y.
        Threshold projections commute with compare-exchange, so the pair
        encodes a common three-color path, independently of middle ranks.
        """
        assert x & ~y == 0
        if bound >= self.budget:
            return
        self.mixed_bounds += 1
        if bound < 0:
            self.add([])
            return
        self.add_row(x)
        self.add_row(y)
        vx, vy = self.rows[x], self.rows[y]
        hits = [self.new() for t in range(self.budget)]
        for t in range(self.budget):
            for k, (a, b) in enumerate(self.pairs):
                c = self.choice[t][k]
                outside = [vx[t][a], vx[t][b], -vy[t][a], -vy[t][b]]
                for lit in outside:
                    self.add([-c, -lit, hits[t]])
                self.add([-c, -hits[t]] + outside)
        cnf = CardEnc.atmost(lits=hits, bound=bound, top_id=self.top,
                            encoding=EncType.seqcounter)
        self.top = max(self.top, cnf.nv)
        for clause in cnf.clauses:
            self.add(clause)

    def forbid_permanent_pair(self, pair):
        self.permanent_redundancies.append(list(pair))
        k = self.pairs.index(tuple(pair))
        for t in range(self.budget):
            self.add([-self.choice[t][k]])

    def route_branch(self, kind):
        """Two complete branches per frontier, conditional on a twenty-gate tail."""
        assert self.n == 11 and kind in ('max_once', 'min_once')
        self.route_branch_kind = kind
        if kind == 'max_once':
            self.card([u[10] for u in self.used], 1)
            for t in range(self.budget):
                for k, pair in enumerate(self.pairs):
                    if 10 in pair and pair != (9, 10):
                        self.add([-self.choice[t][k]])
        else:
            k = self.pairs.index((0, 1))
            pivots = [c[k] for c in self.choice]
            self.card(pivots, 1)
            for t, pivot in enumerate(pivots):
                for s in range(t):
                    self.add([-pivot, -self.used[s][1]])
                for s in range(t + 1, self.budget):
                    self.add([-pivot, -self.used[s][0]])
            self.touch_bound(2045, 1, 0)

    def phase_redundancies(self):
        """Valid when every input has bit1<=bit10 and the sorter is nonredundant.

        Before the first (0,1), wire1 cannot increase and wire10 cannot
        decrease, so (1,10) is redundant. That pivot makes wire0<=wire10;
        afterward wire0 cannot increase, making (0,10) redundant.
        """
        assert self.n == 11
        self.phase_gate_bans = True
        alive = [self.new() for t in range(self.budget + 1)]
        self.add([alive[0]])
        self.add([-alive[-1]])
        pivot_index = self.pairs.index((0, 1))
        upper_index = self.pairs.index((1, 10))
        outer_index = self.pairs.index((0, 10))
        for t in range(self.budget):
            pivot = self.choice[t][pivot_index]
            self.add([-alive[t + 1], alive[t]])
            self.add([-alive[t + 1], -pivot])
            self.add([-alive[t], pivot, alive[t + 1]])
            self.add([-alive[t], -self.choice[t][upper_index]])
            self.add([alive[t], -self.choice[t][outer_index]])

    def branch_shortcut(self):
        """Redundant propagation clause, from the branch and route cap three."""
        assert self.route_branch_kind in ('max_once', 'min_once')
        pairs = ([(6, 8), (6, 9), (7, 9)] if self.route_branch_kind == 'max_once'
                 else [(0, 3), (0, 4), (0, 5), (2, 5)])
        self.branch_shortcut_pairs = [list(p) for p in pairs]
        indices = [self.pairs.index(p) for p in pairs]
        self.add([row[k] for row in self.choice for k in indices])
