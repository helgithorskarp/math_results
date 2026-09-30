"""Forward reverse-unit-propagation checker with persistent watched literals.

Implementation reused verbatim from six-sorting-1, researcher, source
5ad75ecb80164da04c921f1898cf62334668a027 / graph7452.
https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_nullary_minimum_exclusion/watched_rup.py No solver is imported.
The reference occurrence-index implementation is cited from the endpoint
certificate; this implementation updates only clauses with a falsified watch.
Deleting proof clauses is ignored, keeping a stronger monotone database.
"""
from collections import defaultdict
import itertools


class WatchedRUP:
    def __init__(self, n, initial=()):
        self.n = n
        self.formula = []
        self.watch = defaultdict(list)
        self.units = []
        self.has_empty = False
        for clause in initial:
            self.add(clause)

    def add(self, clause):
        clause = list(dict.fromkeys(clause))
        assert all(0 < abs(v) <= self.n for v in clause)
        index = len(self.formula)
        self.formula.append(clause)
        if not clause:
            self.has_empty = True
        elif len(clause) == 1:
            self.units.append(clause[0])
        else:
            self.watch[clause[0]].append(index)
            self.watch[clause[1]].append(index)

    def entails_by_rup(self, clause):
        if self.has_empty:
            return True
        assigned = [0] * (self.n + 1)
        pending = [-lit for lit in clause] + self.units
        cursor = 0
        while cursor < len(pending):
            lit = pending[cursor]; cursor += 1
            variable = abs(lit)
            sign = 1 if lit > 0 else -1
            if assigned[variable] == -sign:
                return True
            if assigned[variable] == sign:
                continue
            assigned[variable] = sign
            false = -lit
            watched = self.watch[false]
            j = 0
            while j < len(watched):
                row = self.formula[watched[j]]
                if row[0] == false:
                    row[0], row[1] = row[1], row[0]
                assert row[1] == false
                other = row[0]
                other_value = assigned[abs(other)] * (1 if other > 0 else -1)
                if other_value == 1:
                    j += 1
                    continue
                replacement = None
                for k in range(2, len(row)):
                    v = row[k]
                    if assigned[abs(v)] * (1 if v > 0 else -1) != -1:
                        replacement = k
                        break
                if replacement is not None:
                    row[1], row[replacement] = row[replacement], row[1]
                    self.watch[row[1]].append(watched[j])
                    watched[j] = watched[-1]
                    watched.pop()
                    continue
                if other_value == -1:
                    return True
                pending.append(other)
                j += 1
        return False


def self_check(reference=None):
    possible = [tuple((i + 1) * sign for i, sign in enumerate(code) if sign)
                for code in itertools.product((-1, 0, 1), repeat=2)]
    checked = 0
    for chosen in range(1 << len(possible)):
        formula = [c for i, c in enumerate(possible) if chosen >> i & 1]
        checker = WatchedRUP(2, formula)
        other = reference(2, formula) if reference else None
        for candidate in possible:
            extended = formula + [(-lit,) for lit in candidate]
            sat = any(all(any(bool(mask >> (abs(lit) - 1) & 1) == (lit > 0)
                             for lit in c) for c in extended) for mask in range(4))
            answer = checker.entails_by_rup(candidate)
            assert not answer or not sat
            if candidate:
                assert answer == (not sat)
            if other:
                assert answer == other.entails_by_rup(candidate)
            checked += 1
    return checked


def replay(n, initial, proof_path):
    checker = WatchedRUP(n, initial)
    assert not checker.has_empty
    additions = deletions = 0
    for line in proof_path.open():
        if not line.strip() or line.startswith('c '):
            continue
        if line.startswith('d '):
            deletions += 1
            continue
        row = list(map(int, line.split()))
        assert row and row[-1] == 0
        row = row[:-1]
        assert checker.entails_by_rup(row), f'Non-RUP step{additions + 1}'
        checker.add(row)
        additions += 1
    assert checker.has_empty and additions > 0
    return additions, deletions


if __name__ == '__main__':
    print(self_check())
