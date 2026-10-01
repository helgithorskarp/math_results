"""six-sorting-2 researcher: independent clause/coverage audit, without encoder or SAT-library imports.

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


class Audit:
    def __init__(self, meta, path):
        self.meta = meta
        self.clauses = []
        with path.open() as stream:
            for line in stream:
                if line.startswith('c') or not line.strip():
                    continue
                if line.startswith('p'):
                    _, _, nv, nc = line.split()
                    self.variables, self.count = int(nv), int(nc)
                else:
                    word = list(map(int, line.split()))
                    assert word[-1] == 0 and all(word[:-1])
                    self.clauses.append(tuple(word[:-1]))
        assert len(self.clauses) == self.count == meta['clauses']
        assert self.variables == meta['variables']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == meta['cnf_sha256']
        self.cursor = self.top = self.cards = 0
        self.base = set()
        for word in meta['choices'] + meta['used']:
            self.base.update(word)
        for histories in meta['rows'].values():
            for word in histories:
                self.base.update(word)
        for word in meta['swaps'].values():
            self.base.update(word)
        for row, mode, cap, flags in meta['hit_flags']:
            self.base.update(flags)
        for word in meta.get('boundary', []):
            self.base.update(word)

    def new(self, supplied):
        self.top += 1
        assert supplied == self.top, ('variable allocation', supplied, self.top)

    def expect(self, values):
        if any(v is True for v in values):
            return
        clause = tuple(v for v in values if v is not False)
        assert self.clauses[self.cursor] == clause, (self.cursor, self.clauses[self.cursor], clause)
        self.cursor += 1

    def card(self, flags, cap, exact=False):
        if cap < 0:
            self.expect([])
            return
        if not exact and cap >= len(flags):
            return
        start = self.cursor
        while self.cursor < len(self.clauses):
            word = self.clauses[self.cursor]
            if any(abs(v) in self.base and abs(v) not in flags for v in word):
                break
            self.cursor += 1
        group = self.clauses[start:self.cursor]
        assert group
        auxiliary = card_shape_check(group, flags, cap, exact)
        assert auxiliary == list(range(self.top + 1, self.top + len(auxiliary) + 1))
        self.top += len(auxiliary)
        self.cards += 1

    def section(self, name, start):
        assert self.cursor - start == self.meta['sections'][name], (name, self.cursor - start)

    def run(self):
        meta, budget = self.meta, self.meta['budget']
        choice, used = meta['choices'], meta['used']
        rows = {int(row): values for row, values in meta['rows'].items()}
        swaps = {int(row): values for row, values in meta['swaps'].items()}
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
            self.card(choice[t], 1, True)
            for i in range(9):
                selected = [choice[t][j] for j, gate in enumerate(PAIRS) if i in gate]
                for c in selected:
                    self.expect([-c, used[t][i]])
                self.expect([-used[t][i]] + selected)
        self.section('gate_choices', 0)
        begin = self.cursor
        for row in meta['record']['image9']:
            target = ((1 << row.bit_count()) - 1) << (9 - row.bit_count())
            if row == target:
                assert row not in rows and row not in swaps
                continue
            bits, swap = rows[row], swaps[row]
            assert len(bits) == budget + 1 and len(swap) == budget
            for word in bits:
                assert len(word) == 9
                for v in word:
                    self.new(v)
            for v in swap:
                self.new(v)
            for i in range(9):
                self.expect([bits[0][i] if row >> i & 1 else -bits[0][i]])
                self.expect([bits[-1][i] if target >> i & 1 else -bits[-1][i]])
            for t in range(budget):
                s = swap[t]
                for j, (a, b) in enumerate(PAIRS):
                    c, x, z = choice[t][j], bits[t][a], bits[t][b]
                    self.expect([-c, -s, x])
                    self.expect([-c, -s, -z])
                    self.expect([-c, -x, z, s])
                for i in range(9):
                    u, x, y = used[t][i], bits[t][i], bits[t + 1][i]
                    for clause in ([u, -x, y], [u, x, -y], [s, -x, y], [s, x, -y],
                                   [-u, -s, x, y], [-u, -s, -x, -y]):
                        self.expect(clause)
        self.section('Boolean_shared_swaps', begin)
        begin = self.cursor
        flags_by_cap = {(r, p, c): flags for r, p, c, flags in meta['hit_flags']}
        expected_keys = {(r, p, c) for r, p, c in meta['caps'] if c < budget}
        assert set(flags_by_cap) == expected_keys
        for row, mode, cap in meta['caps']:
            if cap >= budget:
                continue
            flags = flags_by_cap[row, mode, cap]
            assert len(flags) == budget
            for v in flags:
                self.new(v)
            for t in range(budget):
                for i in range(9):
                    mark = rows[row][t][i] if row in rows else bool(row >> i & 1)
                    if not mode:
                        mark = not mark if isinstance(mark, bool) else -mark
                    unmarked = not mark if isinstance(mark, bool) else -mark
                    self.expect([-used[t][i], unmarked, flags[t]])
            self.card(flags, cap)
        self.section('one_sided_pruning', begin)
        begin = self.cursor
        if meta['activity']:
            assert budget == 12 and len(meta['domains']) == 12
            for domain in meta['domains']:
                assert set(domain['image9']) <= set(meta['record']['image9'])
                for t in range(budget):
                    self.expect([swaps[row][t] for row in domain['image9'] if row in swaps])
        self.section('saturated_slice_activity', begin)
        begin = self.cursor
        for t in range(budget - 1):
            for j, a in enumerate(PAIRS):
                for k, b in enumerate(PAIRS[:j]):
                    if set(a).isdisjoint(b):
                        self.expect([-choice[t][j], -choice[t + 1][k]])
        self.section('adjacent_disjoint_normalization', begin)
        if 'boundary' in meta:
            begin = self.cursor
            boundary = meta['boundary']
            assert len(boundary) == budget + 1
            for word in boundary:
                assert len(word) == 8
                for v in word:
                    self.new(v)
            for flag in boundary[-1]:
                self.expect([-flag])
            for t in range(budget - 1, -1, -1):
                for i in range(8):
                    selected = [choice[t][j] for j, (a, b) in enumerate(PAIRS) if a <= i < b]
                    current, following = boundary[t][i], boundary[t + 1][i]
                    self.expect([-current, following] + selected)
                    self.expect([current, -following])
                    for c in selected:
                        self.expect([current, -c])
                for j, (a, b) in enumerate(PAIRS):
                    for i, k in itertools.combinations(range(a, b), 2):
                        self.expect([-choice[t][j], boundary[t + 1][i], boundary[t + 1][k]])
            self.section('attributed_suffix_interval_components', begin)
        assert self.cursor == self.count and self.top == self.variables
        return dict(status='EVERY_CLAUSE_AND_AUXILIARY_COVERAGE_INDEPENDENTLY_AUDITED',
                    clauses=self.count, variables=self.variables, cardinality_blocks=self.cards)


def main():
    assert __debug__
    parser = argparse.ArgumentParser()
    parser.add_argument('cnf', type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    meta = json.loads(args.cnf.with_suffix('.metadata.json').read_text())
    result = Audit(meta, args.cnf).run()
    result.update(cardinality_shapes=list(SHAPES.values()),
                  exhaustive_cardinality_assignments=sum(v['tests'] for v in SHAPES.values()),
                  seconds=time.monotonic() - started,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  trust='This is an encoding audit, not an UNSAT checker; input provenance and mathematical reductions are separate requirements')
    args.cnf.with_suffix('.coverage-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__ == '__main__':
    main()
