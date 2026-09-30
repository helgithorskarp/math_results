"""Classical S(3,5,17) and exact C5 orbit model, Python standard library."""
from collections import Counter
from itertools import combinations, product


def mul(a, b):
    """GF(16), integer bit basis, modulus x^4+x+1."""
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 16:
            a ^= 19
    return out


def power(a, exponent):
    out = 1
    while exponent:
        if exponent & 1:
            out = mul(out, a)
        a = mul(a, a)
        exponent >>= 1
    return out


def divide(a, b):
    if not b:
        raise ValueError('division by zero')
    return mul(a, power(b, 14))


def triples(mask):
    points = [i for i in range(18) if mask >> i & 1]
    return tuple(sum(1 << i for i in t) for t in combinations(points, 3))


def transform(mask, permutation):
    return sum(1 << permutation[i] for i in range(len(permutation)) if mask >> i & 1)


def orbit(mask, permutation):
    values = []
    while mask not in values:
        values.append(mask)
        mask = transform(mask, permutation)
    assert mask == values[0]
    return tuple(sorted(values))


def classical_design():
    """Labels 0..15 in GF(16), 16=infinity; new point 17 is unused."""
    assert all(mul(a, power(a, 14)) == 1 for a in range(1, 16))
    subfield = [a for a in range(16) if power(a, 4) == a]
    assert len(subfield) == 4
    line = subfield + [16]
    circles = set()
    matrices = 0
    for a, b, c, d in product(range(16), repeat=4):
        if not (mul(a, d) ^ mul(b, c)):
            continue
        if next(x for x in (a, b, c, d) if x) != 1:
            continue
        matrices += 1
        image = []
        for x in line:
            if x == 16:
                y = divide(a, c) if c else 16
            else:
                numerator = mul(a, x) ^ b
                denominator = mul(c, x) ^ d
                y = divide(numerator, denominator) if denominator else 16
            image.append(y)
        assert len(set(image)) == 5
        circles.add(sum(1 << p for p in image))
    assert matrices == 4080 and len(circles) == 68
    assert all((a & b).bit_count() <= 2 for a, b in combinations(circles, 2))
    incidence = Counter(t for c in circles for t in triples(c))
    universe = {sum(1 << p for p in t) for t in combinations(range(17), 3)}
    assert set(incidence) == universe and set(incidence.values()) == {1}
    return tuple(sorted(circles))


def orbit_summary(design):
    """Coverage reduction for cycle type 5^3 1^3; not an exclusion."""
    zeta = power(2, 3)
    assert power(zeta, 5) == 1 and zeta != 1
    permutation = [mul(zeta, x) for x in range(16)] + [16, 17]
    assert sorted(permutation) == list(range(18))
    assert {transform(c, permutation) for c in design} == set(design)
    blocks = [sum(1 << p for p in t) for t in combinations(range(18), 5)]
    block_orbits = sorted({orbit(b, permutation) for b in blocks})
    assert Counter(map(len, block_orbits)) == {1: 3, 5: 1713}
    all_triples = [sum(1 << p for p in t) for t in combinations(range(18), 3)]
    triple_orbits = {orbit(t, permutation) for t in all_triples}
    assert Counter(map(len, triple_orbits)) == {1: 1, 5: 163}
    row_of = {t: o for o in triple_orbits if len(o) == 5 for t in o}
    admissible = []
    seed_count = 0
    for words in block_orbits:
        if len(words) != 5:
            continue
        if any((a & b).bit_count() > 2 for a, b in combinations(words, 2)):
            continue
        covered = {t for b in words for t in triples(b)}
        assert len(covered) == 50 and all(t in row_of for t in covered)
        assert len({row_of[t] for t in covered}) == 10
        admissible.append(words)
        seed_count += set(words) <= set(design)
    assert len(admissible) == 1125 and seed_count == 13
    # Reproduce weights in h+u+2w<=13 for each excluded fixed point.
    weight_histograms = []
    for new_point in (0, 16, 17):
        swap = list(range(18))
        swap[17], swap[new_point] = swap[new_point], swap[17]
        other_design = {transform(c, swap) for c in design}
        weights = Counter()
        for words in admissible:
            values = []
            for b in words:
                if b >> new_point & 1:
                    q = b ^ (1 << new_point)
                    values.append(1 if any(q & c == q for c in other_design) else 2)
                else:
                    values.append(int(b in other_design))
            assert len(set(values)) == 1
            weights[values[0]] += 1
        weight_histograms.append({str(k): v for k, v in sorted(weights.items())})
    return {'permutation': permutation, 'admissible_full_block_orbits': len(admissible),
            'nonfixed_triple_orbits': 163, 'original_circle_full_orbits': seed_count,
            'target70_full_orbits': 14, 'extension_weight_histograms': weight_histograms}
