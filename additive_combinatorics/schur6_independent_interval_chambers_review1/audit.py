"""Separate dense-vector audit of the 132 interval-chamber certificates."""

from collections import Counter
from fractions import Fraction
from itertools import groupby
import json
from math import gcd
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "schur6_independent_interval_chambers"


def basis(d, j):
    return tuple(int(i == j) for i in range(d + 1))


def constant(d, c):
    return tuple([0] * d + [c])


def add(*vectors):
    return tuple(map(sum, zip(*vectors)))


def mul(k, vector):
    return tuple(k * x for x in vector)


def sub(x, y):
    return add(x, mul(-1, y))


def evaluate(form, lengths):
    return sum(x * y for x, y in zip(form, [*lengths, 1]))


def valid_word(word, a):
    n = 5 * a
    assert len(word) == n - 1 and a % 2 == 1
    assert set(word) == set(range(6))
    assert all(word[x - 1] == word[n - x - 1] for x in range(1, n))
    for q in range(a):
        assert word[5 * q] in (0, 2, 3, 4, 5)
        assert word[5 * q + 1] in (1, 2, 3, 4, 5)
    modular = ordinary = doubling = 0
    for x in range(1, n):
        for y in range(x, n):
            z = (x + y) % n
            if z:
                modular += 1
                assert word[x - 1] != word[y - 1] or word[x - 1] != word[z - 1]
            if x + y < n:
                ordinary += 1
                doubling += x == y
                assert word[x - 1] != word[y - 1] or word[x - 1] != word[x + y - 1]
    return modular, ordinary, doubling


def image(word, u):
    n = len(word) + 1
    assert gcd(u, n) == 1
    result = [None] * (n - 1)
    for x, colour in enumerate(word, 1):
        changed = 1 - colour if u % 5 in (2, 3) and colour < 2 else colour
        result[(u * x) % n - 1] = changed
    assert all(c is not None for c in result)
    return result


def patterns(word):
    a = (len(word) + 1) // 5
    axis = [word[5 * q - 1] for q in range(1, (a + 1) // 2)]
    first = [word[5 * q] if word[5 * q] >= 2 else 0 for q in range(a)]
    second = [word[5 * q + 1] if word[5 * q + 1] >= 2 else 0 for q in range(a)]
    return [[(colour, len(list(g))) for colour, g in groupby(values)]
            for values in (axis, first, second)]


def shape(word):
    runs = patterns(word)
    lengths = [length for part in runs for _, length in part]
    counts = [len(part) for part in runs]
    d = len(lengths)
    one, zero = constant(d, 1), constant(d, 0)
    axis = add(one, *(mul(2, basis(d, j)) for j in range(counts[0])))
    groups = []
    endings = []
    offset = 0
    for part, start in zip(runs, (one, zero, zero)):
        cursor = start
        table = {c: [] for c in range(6)}
        for colour, _ in part:
            after = add(cursor, basis(d, offset))
            table[colour].append((cursor, sub(after, one)))
            cursor = after
            offset += 1
        groups.append(table)
        endings.append(cursor)
    assert offset == d
    positive, A, B = groups
    E = {c: positive[c] + [(sub(axis, hi), sub(axis, lo))
                          for lo, hi in positive[c]] for c in range(6)}
    eq = (sub(endings[1], axis), sub(endings[2], axis))
    assert evaluate(axis, lengths) == (len(word) + 1) // 5
    assert all(evaluate(form, lengths) == 0 for form in eq)
    return dict(dim=d, counts=counts, lengths=lengths, axis=axis,
                E=E, A=A, B=B, eq=eq, one=one)


def interval_sum(*parts):
    return add(*(p[0] for p in parts)), add(*(p[1] for p in parts))


def shift(part, delta):
    return add(part[0], delta), add(part[1], delta)


def term(m, reason, cuts):
    kind = reason[0]
    one, axis = m['one'], m['axis']
    E, A, B = m['E'], m['A'], m['B']
    if kind == 'integer_rounding':
        assert len(reason) == 2 and 0 <= reason[1] < len(cuts)
        return cuts[reason[1]]
    if kind == 'positive_run_length':
        assert len(reason) == 2 and 0 <= reason[1] < m['dim']
        raw = sub(one, basis(m['dim'], reason[1]))
    else:
        side = reason[-1]
        assert side in ('left_before_right', 'right_before_left')
        if kind == 'axis_sum':
            _, c, i, j, z, t, _ = reason
            assert c in range(6) and i <= j and t in (0, 1)
            left = interval_sum(E[c][i], E[c][j])
            right = shift(E[c][z], mul(t, axis))
        elif kind == 'A_A_B':
            _, c, i, j, z, t, _ = reason
            assert c in (2, 3, 4, 5) and i <= j and t in (0, 1)
            left = interval_sum(A[c][i], A[c][j])
            right = shift(B[c][z], mul(t, axis))
        elif kind == 'A_B_B_minus_one':
            _, c, i, j, k, t, _ = reason
            assert c in (2, 3, 4, 5) and j <= k and t in (1, 2)
            left = interval_sum(A[c][i], B[c][j], B[c][k])
            point = sub(mul(t, axis), one)
            right = point, point
        else:
            assert kind == 'difference_axis'
            _, name, state, i, j, z, t, _ = reason
            assert name in ('A', 'B') and state in (0, 2, 3, 4, 5) and t in (-1, 0)
            P = A if name == 'A' else B
            colour = state if state else (0 if name == 'A' else 1)
            X, Y = P[state][i], P[state][j]
            left = sub(X[0], Y[1]), sub(X[1], Y[0])
            right = shift(E[colour][z], mul(t, axis))
        lo, hi = left
        other_lo, other_hi = right
        if side == 'left_before_right':
            assert evaluate(hi, m['lengths']) < evaluate(other_lo, m['lengths'])
            raw = add(sub(hi, other_lo), one)
        else:
            assert evaluate(other_hi, m['lengths']) < evaluate(lo, m['lengths'])
            raw = add(sub(other_hi, lo), one)
    divisor = gcd(*raw)
    assert divisor > 0 and evaluate(raw, m['lengths']) <= 0
    return tuple(x // divisor for x in raw)


def certificate_sum(m, proof, cuts, types):
    d = m['dim']
    total = [Fraction(0)] * (d + 1)
    for entry in proof['terms']:
        weight = Fraction(entry['weight'])
        assert weight > 0
        row = term(m, entry['reason'], cuts)
        for j, value in enumerate(row):
            total[j] += weight * value
        types[entry['reason'][0]] += 1
    assert len(proof['equality_weights']) == 2
    for weight, row in zip(proof['equality_weights'], m['eq']):
        factor = Fraction(weight)
        for j, value in enumerate(row):
            total[j] += factor * value
    return tuple(total)


def check_chamber(cert, seed, types):
    m = shape(image(seed, cert['multiplier']))
    assert cert['run_counts'] == m['counts']
    assert cert['dimension'] == m['dim']
    cuts = []
    for cut in cert.get('rounding_cuts', []):
        upper = Fraction(cut['upper'])
        index = cut['coordinate']
        assert 0 <= index < m['dim']
        target = sub(basis(m['dim'], index), constant(m['dim'], upper))
        assert certificate_sum(m, cut, cuts, types) == target
        floor = upper.numerator // upper.denominator
        cuts.append(sub(basis(m['dim'], index), constant(m['dim'], floor)))
    upper = Fraction(cert['upper_bound_axis_factor'])
    assert certificate_sum(m, cert, cuts, types) == sub(
        m['axis'], constant(m['dim'], upper))
    assert upper >= 67
    return upper, m['dim']


def numeric_shape(word):
    a = (len(word) + 1) // 5
    groups = []
    colours = []
    lengths = []
    for part, start in zip(patterns(word), (1, 0, 0)):
        table = {c: [] for c in range(6)}
        cursor = start
        colours.append([c for c, _ in part])
        for c, length in part:
            table[c].append((cursor, cursor + length - 1))
            cursor += length
            lengths.append(length)
        groups.append(table)
    positive, A, B = groups
    E = {c: positive[c] + [(a - hi, a - lo) for lo, hi in positive[c]]
         for c in range(6)}
    return a, colours, lengths, E, A, B


def witness_membership(seed, witness):
    old, new = numeric_shape(seed), numeric_shape(witness)
    assert old[1] == new[1]
    count = 0
    def check(left_old, right_old, left_new, right_new):
        nonlocal count
        if left_old[1] < right_old[0]:
            assert left_new[1] < right_new[0]
        else:
            assert right_old[1] < left_old[0]
            assert right_new[1] < left_new[0]
        count += 1
    def sums(*parts):
        return sum(p[0] for p in parts), sum(p[1] for p in parts)
    for c in range(6):
        for i in range(len(old[3][c])):
            for j in range(len(old[3][c])):
                for z in range(len(old[3][c])):
                    for t in (0, 1):
                        X, Y = old[3][c][i], old[3][c][j]
                        x, y = new[3][c][i], new[3][c][j]
                        O, o = old[3][c][z], new[3][c][z]
                        check(sums(X, Y), (O[0] + t * old[0], O[1] + t * old[0]),
                              sums(x, y), (o[0] + t * new[0], o[1] + t * new[0]))
    for c in (2, 3, 4, 5):
        for i in range(len(old[4][c])):
            for j in range(len(old[4][c])):
                for z in range(len(old[5][c])):
                    for t in (0, 1):
                        X, Y = old[4][c][i], old[4][c][j]
                        x, y = new[4][c][i], new[4][c][j]
                        O, o = old[5][c][z], new[5][c][z]
                        check(sums(X, Y), (O[0] + t * old[0], O[1] + t * old[0]),
                              sums(x, y), (o[0] + t * new[0], o[1] + t * new[0]))
        for i in range(len(old[4][c])):
            for j in range(len(old[5][c])):
                for k in range(len(old[5][c])):
                    for t in (1, 2):
                        check(sums(old[4][c][i], old[5][c][j], old[5][c][k]),
                              (t * old[0] - 1,) * 2,
                              sums(new[4][c][i], new[5][c][j], new[5][c][k]),
                              (t * new[0] - 1,) * 2)
    for part, special in ((4, 0), (5, 1)):
        for state in (0, 2, 3, 4, 5):
            c = state or special
            for i in range(len(old[part][state])):
                for j in range(len(old[part][state])):
                    for z in range(len(old[3][c])):
                        for t in (-1, 0):
                            X, Y = old[part][state][i], old[part][state][j]
                            x, y = new[part][state][i], new[part][state][j]
                            O, o = old[3][c][z], new[3][c][z]
                            check((X[0] - Y[1], X[1] - Y[0]),
                                  (O[0] + t * old[0], O[1] + t * old[0]),
                                  (x[0] - y[1], x[1] - y[0]),
                                  (o[0] + t * new[0], o[1] + t * new[0]))
    return count, new[2]


def main():
    data = json.loads((SOURCE / 'certificate.json').read_text())
    seed = data['seed_word']
    assert data['seed_axis_factor'] == 67
    valid_word(seed, 67)
    seed_runs = patterns(seed)
    assert [sum(length for colour, length in part if colour == 0)
            for part in seed_runs[1:]] == [21, 20]
    n = len(seed) + 1
    units = [u for u in range(1, n // 2 + 1) if gcd(u, n) == 1]
    assert len(units) == 132
    assert [c['multiplier'] for c in data['chambers']] == units
    assert all(image(seed, u) == image(seed, n - u) for u in units)
    assert all(valid_word(image(seed, u), 67) for u in units)
    counts = Counter()
    dimensions = []
    bounds = {}
    for cert in data['chambers']:
        upper, dim = check_chamber(cert, seed, counts)
        bounds[cert['multiplier']] = upper
        dimensions.append(dim)
    assert (min(dimensions), max(dimensions)) == (86, 160)
    assert sum(counts.values()) == 5511
    assert counts == Counter({'A_B_B_minus_one': 306, 'difference_axis': 2257,
                              'axis_sum': 1331, 'positive_run_length': 1265,
                              'A_A_B': 326, 'integer_rounding': 26})
    assert {u: b for u, b in bounds.items() if b != 67} == {
        3: 70, 64: 68, 131: 69, 137: 71}
    def allowed(upper):
        a = upper.numerator // upper.denominator
        while a % 2 == 0 or a % 3 == 0:
            a -= 1
        return a
    assert max(map(allowed, bounds.values())) == 71
    witness = json.loads((SOURCE / 'witness.json').read_text())
    assert witness['multiplier'] == 137 and witness['axis_factor'] == 71
    word = witness['word']
    assert valid_word(word, 71) == (62658, 31329, 177)
    assert [word.count(c) for c in range(6)] == [46, 50, 110, 56, 48, 44]
    witness_runs = patterns(word)
    assert [sum(length for colour, length in part if colour == 0)
            for part in witness_runs[1:]] == [22, 24]
    comparisons, lengths = witness_membership(image(seed, 137), word)
    assert comparisons == 113048 and lengths == witness['run_lengths']
    print('PASS units=132 certificate_terms=5511 rounding_steps=15 '
          'axis_cap=71 endpoint=354 witness_modular=62658 '
          'membership_comparisons=113048')


if __name__ == '__main__':
    main()
