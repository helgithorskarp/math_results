"""Independent witness and domain audit of the 537-unit-orbit obstruction.

Run: python3 -B audit.py. This file imports no reviewed checker or generator.
"""

from itertools import combinations
from math import gcd
from pathlib import Path
import json
import lzma

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'schur_s6_multiplier_orbit_distance'
N = 537
FULL = (1 << 6) - 1


def bit(colour):
    return 1 << (colour - 1)


def triples(n):
    return ((a, b, a + b) for a in range(1, n + 1)
            for b in range(a, n + 1 - a))


def modular_baseline(base):
    assert len(base) == N and set(base[1:]) == set(range(1, 7))
    for a, b in combinations(range(1, N), 2):
        z = (a + b) % N
        if z:
            assert not (base[a] == base[b] == base[z])
    for a in range(1, N):
        z = 2 * a % N
        if z:
            assert base[a] != base[z]


def witness_groups(word, record):
    pair_counts = []
    groups = {}
    for c in range(1, 7):
        pairs = [(x, N - x) for x in range(1, (N + 1) // 2)
                 if word[x] == word[N - x] == c]
        pair_counts.append(len(pairs))
        if c not in (2, 4, 5, 6):
            continue
        chosen = record[str(c)]
        out = [set(p) for p in pairs]
        supports = []
        seen = set()
        for x, coordinates in chosen:
            p = (x, N - x)
            assert p in pairs and p not in seen
            seen.add(p)
            assert len(coordinates) == 20
            support = set()
            for endpoint_index, v in enumerate(p):
                other_colours = [d for d in range(1, 7) if d != c]
                for colour_index, d in enumerate(other_colours):
                    offset = 10 * endpoint_index + 2 * colour_index
                    a, b = coordinates[offset:offset + 2]
                    assert 1 <= a <= b and a + b <= 536
                    vertices = {a, b, a + b}
                    assert v in vertices
                    required = vertices - {v}
                    assert required and all(word[u] == d for u in required)
                    support.update(required)
            assert support
            supports.append(support)
        all_groups = out + supports
        seen_vertices = set()
        for group in all_groups:
            assert not (seen_vertices & group)
            seen_vertices.update(group)
        groups[c] = all_groups
    assert pair_counts == [64, 43, 55, 38, 32, 35]
    return groups, pair_counts


def domain_refutation(word, groups):
    """Enforce exact one edited vertex per group and all Schur constraints."""
    assert len(groups) == 49
    free = set().union(*groups)
    assert all(1 <= v <= 536 for v in free)
    extended = word + [5]
    domains = [0] + [FULL if v in free else bit(extended[v])
                     for v in range(1, N + 1)]
    all_triples = [(a, b, z, tuple(sorted({a, b, z})))
                   for a, b, z in triples(N)]
    reductions = 0

    def restrict(v, allowed):
        nonlocal reductions
        new = domains[v] & allowed
        if not new:
            raise ValueError(f'empty domain at {v}')
        changed = new != domains[v]
        domains[v] = new
        reductions += changed
        return changed

    rounds = 0
    try:
        while True:
            rounds += 1
            changed = False
            for group in groups:
                forced = [v for v in group if not (domains[v] & bit(word[v]))]
                possible = [v for v in group if domains[v] & ~bit(word[v])]
                if len(forced) > 1 or not possible:
                    raise ValueError('exact-one-edit group contradiction')
                if forced:
                    for v in group:
                        if v != forced[0]:
                            changed |= restrict(v, bit(word[v]))
                if len(possible) == 1:
                    v = possible[0]
                    changed |= restrict(v, FULL & ~bit(word[v]))

            for a, b, z, vertices in all_triples:
                fixed = [(v, domains[v]) for v in vertices
                         if domains[v].bit_count() == 1]
                if len(fixed) < len(vertices) - 1:
                    continue
                if len({d for _, d in fixed}) != 1:
                    continue
                colour_bit = fixed[0][1]
                remaining = [v for v in vertices if domains[v].bit_count() != 1]
                if not remaining:
                    raise ValueError(f'fixed monochromatic Schur triple {(a, b, z)}')
                changed |= restrict(remaining[0], FULL & ~colour_bit)
            if not changed:
                return False, rounds, len(free), reductions, None
    except ValueError as exc:
        return True, rounds, len(free), reductions, str(exc)


def main():
    base = [0] + [int(x) for x in (SOURCE / 'baseline.txt').read_text().strip()]
    modular_baseline(base)
    with lzma.open(SOURCE / 'certificates.json.xz', 'rt') as handle:
        cert = json.load(handle)
    units = [m for m in range(1, N) if gcd(m, N) == 1]
    assert len(units) == 356 and set(cert) == {str(m) for m in units}
    exceptions = []
    selected_min = {c: 999 for c in (2, 4, 5, 6)}
    for m in units:
        inverse = pow(m, -1, N)
        word = [0] + [base[inverse * x % N] for x in range(1, N)]
        record = cert[str(m)]
        assert set(record) == {'2', '4', '5', '6'}
        groups, pair_counts = witness_groups(word, record)
        lower = pair_counts[:]
        for c in (2, 4, 5, 6):
            lower[c - 1] = len(groups[c])
            selected_min[c] = min(selected_min[c], len(record[str(c)]))
        if min(lower) < 50:
            assert m in (83, 454) and lower[4] == 49 and min(lower) == 49
            yes, rounds, free_count, reductions, why = domain_refutation(word, groups[5])
            assert yes, f'no independent contradiction for multiplier {m}'
            exceptions.append((m, rounds, free_count, reductions, why))
        else:
            assert min(lower) >= 50
    assert {m for m, *_ in exceptions} == {83, 454}
    print(json.dumps({'units': len(units), 'selected_minima': selected_min,
                      'exceptions': exceptions, 'status': 'VERIFIED_ORBIT_DISTANCE_50'},
                     sort_keys=True))


if __name__ == '__main__':
    main()
