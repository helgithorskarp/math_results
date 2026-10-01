"""Independent finite semantic controls and deliberate audit rejection cases.

Author/executing agent: six-sorting-2, researcher. No solver is imported.
"""
import argparse
from copy import deepcopy
import itertools
import json
from pathlib import Path
import resource
import time

from audit_encoding import Audit

PAIRS = tuple(itertools.combinations(range(9), 2))


def interval_components(word, n=9):
    for start in range(len(word) + 1):
        neighbors = [set() for _ in range(n)]
        for a, b in word[start:]:
            neighbors[a].add(b)
            neighbors[b].add(a)
        unseen = set(range(n))
        while unseen:
            component = {min(unseen)}
            todo = list(component)
            while todo:
                for v in neighbors[todo.pop()]:
                    if v not in component:
                        component.add(v)
                        todo.append(v)
            if max(component) - min(component) + 1 != len(component):
                return False
            unseen -= component
    return True


def boundary_test(word, n=9):
    closed = [False] * (n - 1)
    valid = True
    for a, b in reversed(word):
        valid &= sum(not closed[i] for i in range(a, b)) <= 1
        for i in range(a, b):
            closed[i] = True
    return valid


def semantics():
    xor = 0
    for used, swap, old, new in itertools.product((False, True), repeat=4):
        clauses = [(used, not old, new), (used, old, not new),
                   (swap, not old, new), (swap, old, not new),
                   (not used, not swap, old, new),
                   (not used, not swap, not old, not new)]
        assert all(any(c) for c in clauses) == (new == (old ^ (used and swap)))
        xor += 1
    swap_tests = 0
    for a, b, swap in itertools.product((False, True), repeat=3):
        clauses = [(not swap, a), (not swap, not b), (not a, b, swap)]
        assert all(any(c) for c in clauses) == (swap == (a and not b))
        swap_tests += 1
    touch = 0
    for used, marked, flag in itertools.product((False, True), repeat=3):
        accepted = any((not used, not marked, flag))
        assert accepted == (not (used and marked) or flag)
        touch += 1
    return dict(xor_truth_assignments=xor, swap_truth_assignments=swap_tests,
                one_sided_touch_truth_assignments=touch)


def structure():
    checks = 0
    for length in range(4):
        for word in itertools.product(PAIRS, repeat=length):
            assert boundary_test(word) == interval_components(word)
            checks += 1
    pairs4 = tuple(itertools.combinations(range(4), 2))
    full_sorters = 0
    for length in (5, 6):
        for word in itertools.product(pairs4, repeat=length):
            rows = [[row >> i & 1 for i in range(4)] for row in range(16)]
            nonredundant = True
            for a, b in word:
                active = False
                for bits in rows:
                    if bits[a] > bits[b]:
                        bits[a], bits[b] = bits[b], bits[a]
                        active = True
                if not active:
                    nonredundant = False
                    break
            if nonredundant and all(bits == sorted(bits) for bits in rows):
                assert interval_components(word, 4)
                full_sorters += 1
    assert full_sorters == 708
    assert not interval_components([(0, 2)], 3)
    return dict(nine_wire_words_up_to_length_three=checks,
                nonredundant_four_wire_full_sorters_length_five_six=full_sorters,
                partial_image_counterexample_rejected=True)


def rejections(meta, path):
    # Bypass hash checks deliberately: mutate a parsed semantic clause.
    audit = Audit(meta, path)
    index = meta['sections']['gate_choices'] + 18
    clause = list(audit.clauses[index])
    clause[-1] = -clause[-1]
    audit.clauses[index] = tuple(clause)
    try:
        audit.run()
    except AssertionError:
        clause_rejected = True
    else:
        raise AssertionError('Wrong Boolean clause accepted')
    changed = deepcopy(meta)
    key = next((r, p, c) for r, p, c in changed['caps'] if 0 < c < 11)
    for row in changed['caps']:
        if tuple(row) == key:
            row[2] += 1
    for row in changed['hit_flags']:
        if tuple(row[:3]) == key:
            row[2] += 1
    try:
        Audit(changed, path).run()
    except AssertionError:
        cap_rejected = True
    else:
        raise AssertionError('Altered cardinality meaning accepted')
    return dict(changed_Boolean_clause_rejected=clause_rejected,
                changed_cardinality_cap_rejected=cap_rejected)


def main():
    assert __debug__
    parser = argparse.ArgumentParser()
    parser.add_argument('cnf', type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    meta = json.loads(args.cnf.with_suffix('.metadata.json').read_text())
    result = dict(agent='six-sorting-2', role='researcher', status='FINITE_SEMANTIC_AND_REJECTION_CONTROLS_VERIFIED',
                  semantics=semantics(), structure=structure(), rejections=rejections(meta, args.cnf),
                  seconds=time.monotonic() - started,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    args.cnf.with_suffix('.controls.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
