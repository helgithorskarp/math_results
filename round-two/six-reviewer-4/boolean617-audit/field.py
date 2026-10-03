"""Fresh reviewer arithmetic, frozen before target executable access."""
import itertools

P = 617
PROJECTIONS = (170, 204, 240)

def need(condition, message):
    if not condition:
        raise ValueError(message)

def gauss(p=P):
    need(p > 7 and all(p % d for d in range(2, int(p**0.5)+1)), 'prime domain')
    return [None] + [sum((a*j) % p > p//2 for j in range(1, p//2+1)) % 2
                     for a in range(1, p)]

def squares(p=P):
    residues = {a*a % p for a in range(1, p)}
    return [None] + [int(a not in residues) for a in range(1, p)]

def bit(word, values):
    need(all(v in (0, 1) for v in values), 'undefined character input')
    return (word >> sum(v << i for i, v in enumerate(values))) & 1

def colors(t, word, table, p=P):
    roots = (0, 1, t)
    return [None if x in roots else bit(word, [table[(x-r) % p] for r in roots])
            for x in range(p)]

def orbit(t, p=P):
    a = pow(t, -1, p)
    b = pow(1-t, -1, p)
    return sorted({t, (1-t) % p, a, (1-a) % p, b, (1-b) % p})

def cover(p=P):
    unseen = set(range(2, p))
    rows = []
    while unseen:
        t = min(unseen)
        row = orbit(t, p)
        need(set(row) <= unseen, 'geometry overlap')
        need(all(orbit(u, p) == row for u in row), 'geometry closure')
        rows.append(row)
        unseen.difference_update(row)
    need(sorted(u for row in rows for u in row) == list(range(2, p)), 'geometry coverage')
    return rows

def transport(t, word, table, p=P):
    """Find a root ordering; pull the entire truth table back, then gauge."""
    roots = (0, 1, t)
    representative = min(orbit(t, p))
    for order in itertools.permutations(range(3)):
        offset = roots[order[0]]
        scale = (roots[order[1]] - offset) % p
        normalized = (roots[order[2]] - offset) * pow(scale, -1, p) % p
        if normalized != representative:
            continue
        flip = table[scale]
        pulled = []
        for index in range(8):
            source_bits = [0, 0, 0]
            for k, original_index in enumerate(order):
                source_bits[original_index] = ((index >> k) & 1) ^ flip
            pulled.append(bit(word, source_bits))
        gauge = pulled[0]
        result = sum((value ^ gauge) << index for index, value in enumerate(pulled))
        need(result % 2 == 0, 'truth gauge')
        return representative, result, offset, scale, order, gauge
    raise ValueError('missing normalization')
