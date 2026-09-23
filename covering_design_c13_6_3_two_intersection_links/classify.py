#!/usr/bin/env python3
"""Exhaust the cycle normal form using Python integers only.

Bit j of a mask denotes point j, 0 <= j < 12. Row order is forgotten only
after a complete matrix has been built. See PROOF.md for completeness.
"""
from itertools import combinations, permutations, product
from math import isqrt


def require(condition, message):
    if not condition:
        raise ValueError(message)


def partitions(n, least=3):
    if n == 0:
        yield ()
    for m in range(least, n + 1):
        for tail in partitions(n - m, m):
            yield (m,) + tail


def multiply(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def cycle_polynomial(n):
    # Coefficients in ascending order of det(x I - adjacency(C_n)).
    previous, current = [2], [0, 1]
    for _ in range(2, n + 1):
        following = [0] + current
        for i, x in enumerate(previous):
            following[i] -= x
        previous, current = current, following
    current[0] -= 2
    return current


def spectral_frontier():
    records = []
    polynomials = set()
    for parts in partitions(12):
        polynomial = [1]
        for n in parts:
            polynomial = multiply(polynomial, cycle_polynomial(n))
        require(tuple(polynomial) not in polynomials, 'cospectral partitions')
        polynomials.add(tuple(polynomial))
        determinant = sum(c * 3 ** i for i, c in enumerate(polynomial))
        records.append(dict(parts=parts, determinant=determinant,
                            square=isqrt(determinant) ** 2 == determinant,
                            polynomial=polynomial))
    return records


def quotient_matrices(parts):
    """All integral component row sums, with their forced Gram equations."""
    possibilities = []
    for m in parts:
        rows = []
        for a in product(*(range(min(5, n) + 1) for n in parts)):
            if sum(a) != 5 or any(m * x % n for x, n in zip(a, parts)):
                continue
            if sum(x * (m * x // n) for x, n in zip(a, parts)) == 2 * m + 1:
                rows.append(a)
        possibilities.append(rows)
    answers = []
    for matrix in product(*possibilities):
        if any(sum(m * matrix[i][j] // n for i, m in enumerate(parts)) != 5
               for j, n in enumerate(parts)):
            continue
        if any(sum(matrix[i][j] * (parts[k] * matrix[k][j] // parts[j])
                   for j in range(len(parts))) != 2 * parts[k]
               for i in range(len(parts)) for k in range(i)):
            continue
        answers.append(matrix)
    return answers


QUOTIENTS = {
    (3, 3, 3, 3): ((2, 1, 1, 1), (1, 2, 1, 1),
                   (1, 1, 2, 1), (1, 1, 1, 2)),
    (3, 9): ((2, 3), (1, 4)),
    (4, 8): ((1, 4), (2, 3)),
    (6, 6): ((2, 3), (3, 2)),
}


def column_permutations(parts, exchange_components=False):
    offsets, options = [], []
    offset = 0
    for n in parts:
        offsets.append(offset)
        options.append([tuple((a + sign * i) % n for i in range(n))
                        for a in range(n) for sign in (1, -1)])
        offset += n
    component_orders = (permutations(range(len(parts))) if exchange_components
                        else [tuple(range(len(parts)))])
    for order in component_orders:
        if any(parts[i] != parts[order[i]] for i in range(len(parts))):
            continue
        for actions in product(*options):
            yield tuple(offsets[order[i]] + j
                        for i, action in enumerate(actions) for j in action)


def move(rows, permutation, sort_rows=False):
    result = tuple(sum(1 << permutation[j] for j in range(12) if row >> j & 1)
                   for row in rows)
    return tuple(sorted(result)) if sort_rows else result


def cycle_neighbors(parts):
    neighbors = []
    offset = 0
    for n in parts:
        neighbors += [(offset + (j - 1) % n, offset + (j + 1) % n)
                      for j in range(n)]
        offset += n
    return neighbors


def cycle_blocks(parts, length, counts):
    choices, offset = [], 0
    for n, count in zip(parts, counts):
        choices.append(list(combinations(range(offset, offset + n), count)))
        offset += n
    masks = [sum(1 << j for group in pick for j in group)
             for pick in product(*choices)]
    vectors = {mask: tuple(mask >> j & 1 for j in range(12)) for mask in masks}
    neighbors = cycle_neighbors(parts)
    answers = []
    for first in masks:
        for second in masks:
            if (first & second).bit_count() != 1:
                continue
            rows = [vectors[first], vectors[second]]
            for _ in range(2, length + 2):
                row = tuple(rows[-1][a] + rows[-1][b] - rows[-2][j]
                            for j, (a, b) in enumerate(neighbors))
                if any(x not in (0, 1) for x in row):
                    break
                rows.append(row)
            if len(rows) != length + 2 or rows[-2:] != rows[:2]:
                continue
            block = tuple(sum(x << j for j, x in enumerate(row))
                          for row in rows[:length])
            if any((block[i] & block[j]).bit_count() !=
                   (1 if (i - j) % length in (1, length - 1) else 2)
                   for i in range(length) for j in range(i)):
                continue
            answers.append(block)
    require(len(answers) == len(set(answers)), 'duplicate cycle blocks')
    return answers


def compatible(a, b):
    return all((x & y).bit_count() == 2 for x in a for y in b)


def enumerate_family(parts):
    matrices = quotient_matrices(parts)
    if not matrices:
        return dict(quotients=0, blocks=[], first_orbits=0, ordered=0), set()
    target = QUOTIENTS[parts]
    for matrix in matrices:
        require(any(tuple(tuple(row[j] for j in order) for row in matrix) == target
                    for order in permutations(range(len(parts)))
                    if all(parts[i] == parts[order[i]] for i in range(len(parts)))),
                'unaccounted quotient')
    blocks = [cycle_blocks(parts, n, a) for n, a in zip(parts, target)]
    if not blocks[0]:
        return dict(quotients=len(matrices), blocks=list(map(len, blocks)),
                    first_orbits=0, ordered=0), set()
    remaining = set(blocks[0])
    firsts = []
    while remaining:
        first = min(remaining)
        firsts.append(first)
        orbit = {move(first, p) for p in column_permutations(parts)}
        require(orbit <= set(blocks[0]), 'column action left candidate set')
        remaining -= orbit
    solutions = set()
    ordered = 0

    def visit(chosen, lists):
        nonlocal ordered
        if not lists:
            rows = tuple(sorted(sum(chosen, ())))
            require(len(set(rows)) == 12, 'repeated row')
            require(all(sum(row >> j & 1 for row in rows) == 5
                        for j in range(12)), 'column sum')
            ordered += 1
            solutions.add(rows)
            return
        for block in lists[0]:
            following = [[b for b in candidates if compatible(block, b)]
                         for candidates in lists[1:]]
            if all(following):
                visit(chosen + [block], following)

    for first in firsts:
        following = [[b for b in candidates if compatible(first, b)]
                     for candidates in blocks[1:]]
        if all(following):
            visit([first], following)
    return dict(quotients=len(matrices), blocks=list(map(len, blocks)),
                first_orbits=len(firsts), ordered=ordered), solutions


def enumerate_all():
    report, all_solutions = [], {}
    for spectral in spectral_frontier():
        parts = spectral['parts']
        record = dict(spectral)
        if spectral['square']:
            statistics, solutions = enumerate_family(parts)
            record.update(statistics)
            record['row_sets'] = len(solutions)
            all_solutions[parts] = solutions
        report.append(record)
    return report, all_solutions


if __name__ == '__main__':
    import json
    report, _ = enumerate_all()
    print(json.dumps(report, indent=2))
