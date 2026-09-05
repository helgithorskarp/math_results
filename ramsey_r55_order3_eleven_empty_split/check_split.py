#!/usr/bin/env python3
"""Literal pair-orbit binding audit and complete arithmetic split controls."""
from itertools import combinations, combinations_with_replacement, product


def require(ok, message):
    if not ok:
        raise ValueError(message)


def primary():
    def sigma(v):
        return 3*(v//3)+(v % 3+1) % 3 if v < 33 else v
    representatives = set()
    for a, b in combinations(range(43), 2):
        if b < 33 and a//3 == b//3:
            continue
        orbit, pair = set(), (a, b)
        while pair not in orbit:
            orbit.add(pair)
            pair = tuple(sorted((sigma(pair[0]), sigma(pair[1]))))
        representatives.add(min(orbit))
    cross = sorted(p for p in representatives if p[1] < 33)
    fixed = sorted(p for p in representatives if p[0] >= 33)
    links = sorted((p for p in representatives if p[0] < 33 <= p[1]), key=lambda p: (p[1], p[0]))
    require((len(cross), len(fixed), len(links)) == (165, 45, 110), 'orbit categories')
    return {p: i+1 for i, p in enumerate(cross+fixed+links)}


def equality_rows():
    rows = [(0, 0, 0)]
    for i in range(3):
        rows += [tuple(int(j == i) for j in range(3))]*2
    for pair in combinations(range(3), 2):
        rows.append(tuple(int(j in pair) for j in range(3)))
    return sorted(rows)


def expected(branch):
    ids = primary()
    if branch == 'many':
        return [-ids[3*i, 34] for i in range(3)]
    require(branch == 'one', 'unknown branch')
    return [ids[3*i, 33+row] if bit else -ids[3*i, 33+row]
            for row, bits in enumerate(equality_rows()) if row
            for i, bit in enumerate(bits)]


def audit(base, path, branch):
    tail = expected(branch)
    with base.open('rb') as a, path.open('rb') as b:
        header = a.readline().split()
        require(header[:2] == [b'p', b'cnf'], 'base header')
        nv, nc = map(int, header[2:])
        require(b.readline() == f'p cnf {nv} {nc+len(tail)}\n'.encode(), 'split header')
        for _ in range(nc):
            line = a.readline()
            require(bool(line) and b.readline() == line, 'complete base prefix')
        require(a.read() == b'', 'base EOF')
        for lit in tail:
            require(b.readline() == f'{lit} 0\n'.encode(), 'branch binding')
        require(b.read() == b'', 'split EOF')
    return dict(variables=nv, clauses=nc+len(tail), appended_units=len(tail), complete_prefix=True)


def controls(producer):
    ids = primary()
    masks = [sum(bit << i for i, bit in enumerate(row)) for row in equality_rows()]
    require(masks == list(producer.EQUALITY_MASKS), 'equality ordering')
    for branch in ('one', 'many'):
        require(producer.units(branch) == expected(branch), 'branch primary meanings')
    total = basic = stronger = one = many = 0
    for sequence in combinations_with_replacement(range(8), 10):
        total += 1
        counts = [sequence.count(mask) for mask in range(8)]
        if any(sum(bool(s & (1 << i)) for s in sequence) > 4 for i in range(3)):
            continue
        if any(counts[1 << i] > 2 for i in range(3)):
            continue
        basic += 1
        require(counts[0] >= 1, 'missing inherited empty signature')
        rows = sorted(tuple(int(bool(s & (1 << i))) for i in range(3)) for s in sequence)
        values = {ids[3*i, 33+r]: bit for r, row in enumerate(rows) for i, bit in enumerate(row)}
        truths = {branch: all(values[abs(lit)] == int(lit > 0) for lit in producer.units(branch))
                  for branch in ('one', 'many')}
        require(truths == dict(one=counts[0] == 1, many=counts[0] >= 2), 'arithmetic cover mismatch')
        if any(sum(bool(s & (1 << i)) and not bool(s & (1 << k)) for s in sequence) > 3
               for i in range(3) for k in range(3) if i != k):
            continue
        stronger += 1
        one += truths['one']
        many += truths['many']
    full = list(product((0, 1), repeat=11))
    require(all(full[i][:3] <= full[i+1][:3] for i in range(len(full)-1)), 'prefix ordering')
    require(total == 19448 and basic == 928 and (stronger, one, many) == (778, 1, 777), 'control census')
    wrong_masks = [0, 1, 1, 2, 2, 3, 4, 4, 5, 6]
    wrong_rows = [tuple(int(bool(s & (1 << i))) for i in range(3)) for s in wrong_masks]
    require(wrong_rows != sorted(wrong_rows), 'numeric-mask order should fail lex order')
    return dict(compositions=total, basic_profiles=basic, stronger_profiles=stronger,
                one_profiles=one, many_profiles=many, full_signatures=len(full),
                equality_masks=masks, numeric_mask_order_rejected=True,
                equality_units=producer.units('one'), many_units=producer.units('many'))
