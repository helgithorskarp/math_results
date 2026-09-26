"""Exact congruence reduction of all symmetric 3-by-3 matrices over F_5."""
from collections import Counter
from itertools import product
from field import determinant, require

IDENTITY = ((1,0,0), (0,1,0), (0,0,1))
FORMS = {
    'zero': (0,0,0),
    'rank1_square': (1,0,0),
    'rank1_nonsquare': (2,0,0),
    'rank2_split': (1,4,0),
    'rank2_anisotropic': (1,2,0),
    'rank3_square': (1,1,1),
    'rank3_nonsquare': (1,1,2),
}


def multiply(a, b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(3)) % 5
                       for j in range(3)) for i in range(3))


def congruence(matrix, change):
    transpose = tuple(zip(*change))
    return multiply(multiply(transpose, matrix), change)


def normalize(matrix):
    """Return a named representative and an actual invertible basis change."""
    current, basis = matrix, IDENTITY

    def apply(change):
        nonlocal current, basis
        current = congruence(current, change)
        basis = multiply(basis, change)

    def scale_column(j, scalar):
        change = [list(row) for row in IDENTITY]
        change[j][j] = scalar
        apply(change)

    rank = 0
    for i in range(3):
        pivot = next((j for j in range(i,3) if current[j][j]), None)
        if pivot is None:
            pair = next(((j,k) for j in range(i,3) for k in range(j+1,3)
                         if current[j][k]), None)
            if pair is None:
                break
            j, k = pair
            change = [list(row) for row in IDENTITY]
            change[k][j] = 1  # new column j is e_j+e_k
            apply(change)
            pivot = j
        if pivot != i:
            change = [list(row) for row in IDENTITY]
            for row in change:
                row[i], row[pivot] = row[pivot], row[i]
            apply(change)
        for j in range(i+1,3):
            change = [list(row) for row in IDENTITY]
            change[i][j] = -current[i][j]*pow(current[i][i],-1,5) % 5
            apply(change)
        target = 1 if current[i][i] in (1,4) else 2
        scalar = next(s for s in range(1,5) if current[i][i]*s*s % 5 == target)
        scale_column(i, scalar)
        rank += 1

    # A pair of nonsquare diagonal entries (2,2) is congruent to (1,1).
    twos = [j for j in range(rank) if current[j][j] == 2]
    while len(twos) >= 2:
        j, k = twos[:2]
        change = [list(row) for row in IDENTITY]
        change[j][j], change[j][k] = 2, 2
        change[k][j], change[k][k] = 2, 3
        apply(change)
        twos = twos[2:]
    if twos and twos[0] != rank-1:
        j, k = twos[0], rank-1
        change = [list(row) for row in IDENTITY]
        for row in change:
            row[j], row[k] = row[k], row[j]
        apply(change)
    if rank == 2 and current[1][1] == 1:
        scale_column(1, 2)  # use the split representative (1,4,0)
    diagonal = tuple(current[i][i] for i in range(3))
    name = next((name for name, d in FORMS.items() if d == diagonal), None)
    require(name is not None, 'quadratic representative')
    require(all(current[i][j] == (diagonal[i] if i == j else 0)
                for i in range(3) for j in range(3)), 'diagonal reduction')
    require(determinant(*basis) != 0 and congruence(matrix,basis) == current,
            'exact congruence witness')
    return name, basis


def audit():
    counts = Counter()
    for a,b,c,d,e,f in product(range(5), repeat=6):
        matrix = ((a,d,e),(d,b,f),(e,f,c))
        name, _ = normalize(matrix)
        counts[name] += 1
    require(sum(counts.values()) == 15625 and set(counts) == set(FORMS),
            'complete symmetric-matrix classification')
    return dict(sorted(counts.items()))
