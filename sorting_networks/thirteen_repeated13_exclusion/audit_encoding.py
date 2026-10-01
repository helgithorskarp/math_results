"""six-sorting-1 researcher: complete clause audit, without encoder or SAT imports.

Horn auxiliary-existence routine adapted with credit from six-sorting-2,
source9d6ec9a6ba29103c9de43d716823e25b132d4b1c, graph8222.
The comparator and touch gadgets below are audited separately for this kernel.

Reconstructs every non-cardinality clause from metadata, validates canonical
variable allocation, and checks cardinality auxiliary existence by exhaustive
Horn closure of all relevant flag assignments. The native DRAT checker is a
separate required step. A successful audit alone does not prove UNSAT.
"""
from collections import Counter, deque
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

PAIRS = tuple(itertools.combinations(range(9), 2))
SHAPES = {}


def canon_card(clauses, flags):
    variables = set(abs(v) for clause in clauses for v in clause)
    auxiliaries = sorted(variables - set(flags))
    rename = {v: i + 1 for i, v in enumerate(list(flags) + auxiliaries)}
    canon = tuple(tuple(rename[abs(v)] if v > 0 else -rename[abs(v)] for v in clause) for clause in clauses)
    return canon, auxiliaries


def horn_model(clauses, flags_count, assignment):
    """Least Horn model after fixing flags, using exact Boolean propagation."""
    clauses_left = []
    heads = []
    mentions = {}
    queue = deque()
    facts = set()
    for clause in clauses:
        negative = []
        positive = []
        satisfied = False
        for lit in clause:
            v = abs(lit)
            if v <= flags_count:
                value = bool(assignment >> (v - 1) & 1)
                if value == (lit > 0):
                    satisfied = True
                    break
            elif lit > 0:
                positive.append(v)
            else:
                negative.append(v)
        if satisfied:
            continue
        assert len(positive) <= 1, ('not Horn after flags fixed', clause)
        index = len(heads)
        heads.append(positive[0] if positive else None)
        clauses_left.append(len(set(negative)))
        for v in set(negative):
            mentions.setdefault(v, []).append(index)
        if not negative:
            queue.append(index)
    while queue:
        index = queue.popleft()
        head = heads[index]
        if head is None:
            return False
        if head in facts:
            continue
        facts.add(head)
        for affected in mentions.get(head, ()):
            clauses_left[affected] -= 1
            if clauses_left[affected] == 0:
                queue.append(affected)
    return True


def card_shape_check(clauses, flags, cap, exact):
    canon, auxiliaries = canon_card(clauses, flags)
    shape = canon, len(flags), cap, exact
    if shape in SHAPES:
        return auxiliaries
    n = len(flags)
    tests = 0
    if exact:
        assert cap == 1
        assert tuple(range(1, n + 1)) in canon
        assert all(v <= 0 or v > n for clause in canon if clause != tuple(range(1, n + 1)) for v in clause)
        for i in range(n):
            assert horn_model(canon, n, 1 << i)
            tests += 1
        assert not horn_model(canon, n, 0)
        tests += 1
        for i, j in itertools.combinations(range(n), 2):
            assert not horn_model(canon, n, (1 << i) | (1 << j))
            tests += 1
        # Atmost clauses have only negative flags: rejection of every pair
        # also rejects every larger set of true flags, by monotonicity.
    else:
        assert n <= 12
        for assignment in range(1 << n):
            assert horn_model(canon, n, assignment) == (assignment.bit_count() <= cap)
            tests += 1
    SHAPES[shape] = dict(flags=n, cap=cap, exact=exact, tests=tests)
    return auxiliaries


def truth_controls():
    """Definition-level truth tables, independent of row propagation code."""
    def holds(clauses, values):
        return all(any(values[abs(lit)] == (lit > 0) for lit in clause) for clause in clauses)
    # Variables: selector=1, left=2, right=3, output-left=4, output-right=5.
    gates = [(-1, -4, 2), (-1, -4, 3), (-1, 4, -2, -3),
             (-1, 5, -2), (-1, 5, -3), (-1, -5, 2, 3)]
    checks = 0
    for assignment in itertools.product((False, True), repeat=5):
        v = dict(enumerate(assignment, 1))
        expected = not v[1] or (v[4] == min(v[2], v[3]) and v[5] == max(v[2], v[3]))
        assert holds(gates, v) == expected
        checks += 1
    for mode in (0, 1):
        a, b = (2, 3) if mode else (-2, -3)
        touched = [(-1, -a, 4), (-1, -b, 4), (-1, a, b, -4)]
        for assignment in itertools.product((False, True), repeat=4):
            v = dict(enumerate(assignment, 1))
            expected = not v[1] or v[4] == (v[2] == bool(mode) or v[3] == bool(mode))
            assert holds(touched, v) == expected
            checks += 1
    for assignment in itertools.product((False, True), repeat=3):
        v = dict(enumerate(assignment, 1))
        assert holds([(1, -2, 3), (1, 2, -3)], v) == (v[1] or v[2] == v[3])
        checks += 1
    return checks


class Audit:
    def __init__(self, meta, path, expected):
        self.meta = meta
        assert meta['n'] == 9 and meta['budget'] == expected['budget']
        assert meta['record']['parent_index'] == expected['parent_index']
        assert meta['record']['image'] == expected['image']
        assert meta['record']['rows9_sha256'] == expected['rows_sha256']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == meta['cnf_sha256'] == expected['cnf_sha256']
        self.clauses = []
        self.variables = self.count = None
        body_hash = hashlib.sha256()
        with path.open() as stream:
            for line in stream:
                if line.startswith('p '):
                    assert self.variables is None
                    _, kind, nv, nc = line.split()
                    assert kind == 'cnf'
                    self.variables, self.count = int(nv), int(nc)
                else:
                    word = list(map(int, line.split()))
                    assert word[-1] == 0 and all(0 < abs(v) <= self.variables for v in word[:-1])
                    self.clauses.append(tuple(word[:-1]))
                    body_hash.update(line.encode('ascii'))
        assert len(self.clauses) == self.count == meta['clauses'] == expected['clauses']
        assert self.variables == meta['variables'] == expected['variables']
        assert body_hash.hexdigest() == meta['clause_stream_sha256'] == expected['clause_stream_sha256']
        self.cursor = self.top = self.cards = 0
        self.base = set()
        for group in meta['choices'] + meta['used']:
            self.base.update(group)
        for histories in meta['rows'].values():
            for group in histories:
                self.base.update(group)
        for row, mode, cap, flags in meta['hit_flags']:
            self.base.update(flags)

    def new(self, supplied):
        self.top += 1
        assert supplied == self.top, ('allocation', supplied, self.top)

    def expect(self, clause):
        assert self.clauses[self.cursor] == tuple(clause), (self.cursor, self.clauses[self.cursor], clause)
        self.cursor += 1

    def card(self, flags, cap, exact=False):
        start = self.cursor
        while self.cursor < self.count:
            clause = self.clauses[self.cursor]
            if any(abs(v) in self.base and abs(v) not in flags for v in clause):
                break
            self.cursor += 1
        group = self.clauses[start:self.cursor]
        assert group
        auxiliary = card_shape_check(group, flags, cap, exact)
        assert auxiliary == list(range(self.top + 1, self.top + len(auxiliary) + 1))
        self.top += len(auxiliary)
        self.cards += 1

    def section(self, name, start):
        assert self.cursor - start == self.meta['sections'][name], name

    def run(self):
        meta, budget = self.meta, self.meta['budget']
        choice, used = meta['choices'], meta['used']
        rows = {int(row): values for row, values in meta['rows'].items()}
        assert list(rows) == meta['record']['rows9']
        assert len(choice) == len(used) == budget
        for word in choice:
            assert len(word) == 36
            for supplied in word:
                self.new(supplied)
        for word in used:
            assert len(word) == 9
            for supplied in word:
                self.new(supplied)
        for t in range(budget):
            self.card(choice[t], 1, exact=True)
            for i in range(9):
                incident = [choice[t][j] for j, gate in enumerate(PAIRS) if i in gate]
                for selector in incident:
                    self.expect([-selector, used[t][i]])
                self.expect([-used[t][i]] + incident)
        self.section('gate_choices', 0)
        begin = self.cursor
        for row in meta['record']['rows9']:
            bits = rows[row]
            assert len(bits) == budget + 1
            for word in bits:
                assert len(word) == 9
                for supplied in word:
                    self.new(supplied)
            for i in range(9):
                self.expect([bits[0][i] if row >> i & 1 else -bits[0][i]])
                self.expect([bits[-1][i] if i >= 9 - row.bit_count() else -bits[-1][i]])
            for t in range(budget):
                for i in range(9):
                    u, incoming, outgoing = used[t][i], bits[t][i], bits[t + 1][i]
                    self.expect([u, -outgoing, incoming])
                    self.expect([u, outgoing, -incoming])
                for selector, (a, b) in zip(choice[t], PAIRS):
                    x, y, low, high = bits[t][a], bits[t][b], bits[t + 1][a], bits[t + 1][b]
                    for clause in ([-selector, -low, x], [-selector, -low, y],
                                   [-selector, low, -x, -y], [-selector, high, -x],
                                   [-selector, high, -y], [-selector, -high, x, y]):
                        self.expect(clause)
        self.section('Boolean_comparators', begin)
        begin = self.cursor
        supplied_flags = meta['hit_flags']
        active = [(r, p, c) for r, p, c, *_ in meta['caps'] if c < budget]
        assert [(r, p, c) for r, p, c, flags in supplied_flags] == active
        for row, mode, cap, flags in supplied_flags:
            assert 0 <= cap < budget and len(flags) == budget
            for supplied in flags:
                self.new(supplied)
            for t in range(budget):
                for selector, (a, b) in zip(choice[t], PAIRS):
                    mark_a, mark_b = rows[row][t][a], rows[row][t][b]
                    if not mode:
                        mark_a, mark_b = -mark_a, -mark_b
                    self.expect([-selector, -mark_a, flags[t]])
                    self.expect([-selector, -mark_b, flags[t]])
                    self.expect([-selector, mark_a, mark_b, -flags[t]])
            self.card(flags, cap)
        self.section('one_sided_pruning', begin)
        assert self.cursor == self.count and self.top == self.variables
        return dict(status='EVERY_CLAUSE_AND_AUXILIARY_INDEPENDENTLY_AUDITED',
                    variables=self.variables, clauses=self.count, cardinality_blocks=self.cards)
