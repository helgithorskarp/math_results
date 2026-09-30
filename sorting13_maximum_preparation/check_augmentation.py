"""Compare L16 exact-route clauses with independent frozen scalar predicates.

Auxiliary words are not claimed to sort L; the checked full L18 control does.
"""
import itertools
import json
from pathlib import Path

from search import augment
from sequential_sat import Writer
from pysat.solvers import Glucose4

HERE = Path(__file__).resolve().parent
PAIRS = list(itertools.combinations(range(9), 2))


class MemoryWriter(Writer):
    def __init__(self, solver):
        self.variables = self.clauses = 0
        self.solver = solver

    def add(self, *literals):
        if any(v is True for v in literals):
            return
        clause = list(dict.fromkeys(v for v in literals if v is not False))
        if any(-v in clause for v in clause):
            return
        self.solver.add_clause(clause)
        self.clauses += 1


def scalar_trace(mask, word):
    row = [(mask >> i) & 1 for i in range(9)]
    result = [list(row)]
    for a, b in word:
        if row[a] > row[b]:
            row[a], row[b] = row[b], row[a]
        result.append(list(row))
    return result


def records(pruning):
    rows = pruning['critical_single_bounds'] + pruning['selected_mixed_bounds'] + pruning['designated_bounds']
    return list({(r['x'], r['y']): r for r in rows}.values())


def predicate(word, pruning, traces, exact):
    gates = len(word)
    for r in records(pruning):
        count = sum(bool(traces[r['x']][t][a] or traces[r['x']][t][b]
                         or not traces[r['y']][t][a] or not traces[r['y']][t][b])
                    for t, (a, b) in enumerate(word))
        if count > r['cap'] + gates - 16:
            return False
    if gates != 16:
        return True
    touches = lambda state: [bool(traces[state][t][a] or traces[state][t][b])
                              for t, (a, b) in enumerate(word)]
    if [g for g, hit in zip(word, touches(32)) if hit] != [(5, 7), (7, 8)]:
        return False
    if [g for g, hit in zip(word, touches(256)) if hit] != [(7, 8)]:
        return False
    if [g for g in word if 0 in g] != [(0, 1)]:
        return False
    root = word.index((7, 8))
    post = [g for g in word[root+1:] if 7 in g]
    if len(post) != 1 or post[0] not in ((5, 7), (6, 7)):
        return False
    if post[0] == (5, 7) and (6, 7) not in word[:word.index((5, 7))]:
        return False
    if exact:
        separate = [touches(1 << i) for i in (3, 4, 5, 7, 8)]
        if [sum(row) for row in separate] != [4, 4, 2, 4, 1]:
            return False
        if sum(any(row[t] for row in separate) for t in range(16)) != 5:
            return False
    return True


def check(word, pruning, exact, max_preparations=None):
    word = list(map(tuple, word)); gates = len(word)
    needed = {r[k] for r in records(pruning) for k in ('x', 'y')} | {1 << i for i in (3, 4, 5, 7, 8)}
    traces = {state: scalar_trace(state, word) for state in needed}
    expected = predicate(word, pruning, traces, exact)
    if max_preparations is not None:
        expected = expected and word.index((7, 8)) < 5 + max_preparations
    bits = {state: [[bool(v) for v in row] for row in trace] for state, trace in traces.items()}
    with Glucose4() as solver:
        w = MemoryWriter(solver)
        choices = [[w.var() for _ in PAIRS] for _ in word]
        for t, row in enumerate(choices):
            w.exactly_one(row); w.add(row[PAIRS.index(word[t])])
        augment(w, choices, PAIRS, bits, pruning, gates, None, True, exact, max_preparations)
        actual = solver.solve()
    assert actual == expected, (word, exact, expected, actual)
    return actual


def main():
    if not __debug__:
        raise RuntimeError('Run without Python optimization')
    pruning = json.loads((HERE / 'fixture.json').read_text())
    frontier = dict(kernel_words=pruning['maximum_kernel_words'])
    simple = dict(critical_single_bounds=[r for r in pruning['critical_single_bounds'] if r['x']],
                  selected_mixed_bounds=[],
                  designated_bounds=[next(r for r in pruning['designated_bounds'] if (r['x'], r['y']) == (288, 510))])
    controls = []
    for kernel in frontier['kernel_words']:
        controls.append(kernel + [[0, 1], [5, 6], [6, 7]] + [[1, 2]] * 8)
        controls.append(kernel + [[0, 1], [5, 7]] + [[1, 2]] * 9)
    assert len(controls) == 42
    totals = dict(simple=dict(SAT=0, UNSAT=0), full=dict(SAT=0, UNSAT=0))
    words = {tuple(map(tuple, word)) for word in controls}
    for word in controls:
        for index, replacement in ((0, [0, 3]), (15, [1, 8]), (5, [0, 2]), (7, [4, 7])):
            changed = list(word); changed[index] = replacement
            words.add(tuple(map(tuple, changed)))
    for word in sorted(words):
        for label, data in (('simple', simple), ('full', pruning)):
            actual = check(word, data, True)
            totals[label]['SAT' if actual else 'UNSAT'] += 1
    assert totals['simple']['SAT'] == 27 and totals['simple']['UNSAT']
    # Three pure binary controls satisfy the prior necessary cut conditions,
    # but fail the exact-route lower counts added after their exclusion7436.
    pure = [[(4, 7), (3, 7), (5, 7), (7, 8)],
            [(3, 7), (4, 7), (5, 7), (7, 8)],
            [(3, 4), (4, 7), (5, 7), (7, 8)]]
    for kernel in pure:
        word = kernel + [(0, 1), (5, 6), (6, 7)] + [(1, 2)] * 9
        assert check(word, simple, False) and not check(word, simple, True)
    assert check(pruning['control18'], pruning, True)
    # Keep 16 slots while shifting the five-kernel root by zero, one or two
    # genuine nongates. This independently audits the added root-time clause.
    preparation_cases = 0
    for kernel in frontier['kernel_words']:
        for prep in (0, 1, 2):
            word = [[1, 2]] * prep + kernel + [[0, 1], [5, 6], [6, 7]] + [[1, 2]] * (8-prep)
            assert check(word, simple, True, 1) == (prep <= 1)
            preparation_cases += 1
    result = dict(agent='six-sorting-2', role='researcher', status='VERIFIED',
                  distinct_auxiliary_words=len(words), frozen_cases=2*len(words)+7+preparation_cases,
                  preparation_clause_cases=preparation_cases,
                  subset_positive_words=27, route_lower_count_negative_controls=3,
                  full_L18_control=True, counts=totals,
                  scope='Clause semantics and auxiliary conditions only; no L16 witness or exclusion')
    (HERE / 'scratch' / 'augmentation-checked.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
