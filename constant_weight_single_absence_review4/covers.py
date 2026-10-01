"""Independent exact covers grouped by the omitted tail class."""
from itertools import combinations, product
import time


def need(value, text):
    if not value:
        raise ValueError(text)


def pairs(block):
    return frozenset(combinations(sorted(block), 2))


def group_covers(options, universe, state_limit=200000, seconds=10, started=None):
    start = time.monotonic() if started is None else started
    states = 0
    found = []

    def visit(remaining, used, chosen):
        nonlocal states
        states += 1
        if states > state_limit or time.monotonic()-start > seconds:
            raise RuntimeError('INCOMPLETE: omission-class cover guard')
        if not remaining:
            if used == universe:
                found.append(tuple(sorted(chosen)))
            return
        pivot = min(remaining, key=lambda g: (len(remaining[g]), g))
        for blocks, occupied in remaining[pivot]:
            need(used.isdisjoint(occupied) and occupied <= universe, 'remaining alternatives obey pair capacity')
            next_classes = {g: [(bs, ps) for bs, ps in choices if ps.isdisjoint(occupied)]
                            for g, choices in remaining.items() if g != pivot}
            if all(next_classes.values()):
                visit(next_classes, used | occupied, chosen+blocks)

    visit(dict(enumerate(options)), frozenset(), ())
    need(len(set(found)) == len(found), 'unique complete grouped covers')
    return sorted(found), states


def census(Q, x, y, a, state_limit=200000, seconds=10):
    start = time.monotonic()
    fixed = [frozenset(q) | {y} for q in Q]
    tails = sorted(tuple(sorted(w-{a, y})) for w in fixed if a in w)
    need(len(tails) == 5 and all(len(g) == 3 for g in tails), 'five tail triples')
    T = set(range(18))-{a, x, y}
    need(set().union(*map(set, tails)) == T and sum(map(len, tails)) == 15, 'tail partition')
    U = frozenset((i, j) for i, j in combinations(sorted(T), 2)
                  if not any(i in g and j in g for g in tails))
    need(len(U) == 90, 'cross-tail pair universe')
    classes = []
    all_columns = []
    for omitted in range(5):
        blocks = []
        for choice in product(*(tails[g] for g in range(5) if g != omitted)):
            q = tuple(sorted(choice))
            if all(len((set(q) | {a}) & w) <= 2 for w in fixed):
                blocks.append(q)
                all_columns.append(q)
        classes.append(sorted(blocks))
    all_columns.sort()
    # Definition-level second carrier: every eighteen-point five-word.
    literal = []
    for word in combinations(range(18), 5):
        w = frozenset(word)
        if a in w and x not in w and y not in w and all(len(w & f) <= 2 for f in fixed):
            q = tuple(sorted(w-{a}))
            if pairs(q) <= U:
                literal.append(q)
    need(sorted(literal) == all_columns, 'entire independent legal a-word carrier')
    triple_classes = []
    tested_triples = 0
    for group in classes:
        options = []
        pair_sets = {b: pairs(b) for b in group}
        for triple in combinations(group, 3):
            tested_triples += 1
            ps = [pair_sets[b] for b in triple]
            if ps[0].isdisjoint(ps[1]) and ps[0].isdisjoint(ps[2]) and ps[1].isdisjoint(ps[2]):
                options.append((triple, ps[0] | ps[1] | ps[2]))
        triple_classes.append(options)
    found, states = group_covers(triple_classes, U, state_limit, seconds, start)
    for full in found:
        need(len(full) == 15 and all(sum(v in b for b in full) == 4 for v in T), 'literal full cover demands')
    return sorted(found), {'legal_columns': all_columns, 'class_sizes': list(map(len, classes)),
                           'triple_class_sizes': list(map(len, triple_classes)),
                           'tested_triples': tested_triples, 'states': states, 'pair_count': len(U)}
