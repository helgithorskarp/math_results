"""Independent mixed-radix CRT coordinates; no producer imports."""
from itertools import product
from math import gcd

PERIOD = 2520
PREFIX = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
ORDER = (15, 18, 24, 36, 20)
C15 = (0, 1, 2, 4, 6, 11)
C18 = (0, 1, 2, 3, 4, 5, 6, 9, 12, 15)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def coordinates(period=PERIOD, prefix=PREFIX):
    need(period == PERIOD, "literal period required")
    factors = (8, 9, 5, 7)
    terms = tuple((period // m) * pow(period // m, -1, m) for m in factors)
    # An actual bijection, not a symmetry quotient. Every physical point survives.
    physical = tuple(sum(r * t for r, t in zip(rs, terms)) % period
                     for rs in product(*(range(m) for m in factors)))
    need(len(physical) == period and set(physical) == set(range(period)),
         "CRT coordinate bijection")
    required = tuple(x for x in physical
                     if x % 8 != 4 and all(x % n != a for n, a in prefix))
    labels = tuple(n for n in range(8, period + 1)
                   if period % n == 0 and n not in {p[0] for p in prefix})
    masks = {}
    for n in labels:
        phases = [0] * n
        for i, x in enumerate(required):
            phases[x % n] |= 1 << i
        masks[n] = tuple(phases)
        need(sum(m.bit_count() for m in phases) == len(required),
             "each original label partitions the required set")
    return physical, required, labels, masks


def marginal_row(phases, labels, masks, full):
    chosen = ORDER[:len(phases)]
    covered = 0
    for n, a in zip(chosen, phases):
        need(0 <= a < n, "original phase domain")
        covered |= masks[n][a]
    residual = full ^ covered
    remaining = tuple(n for n in labels if n not in chosen)
    values = tuple(max((residual & m).bit_count() for m in masks[n])
                   for n in remaining)
    gain = covered.bit_count()
    return gain, values, gain + sum(values)


def affine_partition():
    # Solve the prefix equations directly, with no formula for translations.
    maps = tuple((u, v) for u in range(PERIOD) if gcd(u, PERIOD) == 1
                 for v in range(0, PERIOD, 72)
                 if all((u * a + v) % n == a for n, a in PREFIX))
    pairs = set(product(range(15), range(18)))
    orbits = []
    while pairs:
        seed = min(pairs)
        orbit = sorted({((u * seed[0] + v) % 15, (u * seed[1] + v) % 18)
                        for u, v in maps})
        need(set(orbit) <= pairs, "disjoint affine orbits")
        pairs.difference_update(orbit)
        orbits.append(orbit)
    need([o[0] for o in orbits] == list(product(C15, C18)),
         "complete simultaneous orbit representatives")
    return maps, orbits
