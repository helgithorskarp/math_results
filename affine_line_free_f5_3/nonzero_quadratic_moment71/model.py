"""Exact polynomial evaluation over F_5; no external algebra package."""
from itertools import product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def projective_points(dimension):
    return tuple(v for v in product(range(5), repeat=dimension)
                 if any(v) and next(x for x in v if x) == 1)


POINTS = projective_points(3)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b)) % 5


def determinant(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0])) % 5


def monomials(degree):
    return tuple((a, b, degree-a-b) for a in range(degree+1)
                 for b in range(degree+1-a))


def evaluation(degree):
    return tuple(tuple(pow(x, a, 5)*pow(y, b, 5)*pow(z, c, 5) % 5
                       for a, b, c in monomials(degree)) for x, y, z in POINTS)


def inverse(matrix):
    n = len(matrix)
    require(all(len(row) == n for row in matrix), 'square matrix required')
    augmented = [list(row)+[int(i == j) for j in range(n)]
                 for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next((k for k in range(j, n) if augmented[k][j] % 5), None)
        require(pivot is not None, 'singular evaluation minor')
        augmented[j], augmented[pivot] = augmented[pivot], augmented[j]
        scale = pow(augmented[j][j], -1, 5)
        augmented[j] = [scale*x % 5 for x in augmented[j]]
        for k in range(n):
            if k != j:
                scale = augmented[k][j]
                augmented[k] = [(x-scale*y) % 5
                                for x, y in zip(augmented[k], augmented[j])]
    result = tuple(tuple(row[n:]) for row in augmented)
    require(all(sum(matrix[i][k]*result[k][j] for k in range(n)) % 5 == int(i == j)
                for i in range(n) for j in range(n)), 'inverse product check')
    return result


def information_set():
    matrix = evaluation(4)
    basis, pivots, chosen = [], [], []
    for i, original in enumerate(matrix):
        row = list(original)
        for pivot, earlier in zip(pivots, basis):
            scale = row[pivot]
            row = [(x-scale*y) % 5 for x, y in zip(row, earlier)]
        if not any(row):
            continue
        pivot = next(j for j, x in enumerate(row) if x)
        scale = pow(row[pivot], -1, 5)
        basis.append([scale*x % 5 for x in row])
        pivots.append(pivot)
        chosen.append(i)
        if len(chosen) == 15:
            break
    require(len(chosen) == 15, 'quartic evaluation rank')
    inv = inverse([matrix[i] for i in chosen])
    generator = tuple(tuple(sum(row[k]*inv[k][j] for k in range(15)) % 5
                            for j in range(15)) for row in matrix)
    require(all(generator[i] == tuple(int(j == k) for k in range(15))
                for j, i in enumerate(chosen)), 'information coordinates')
    return tuple(chosen), inv, generator


def structural_families():
    """Return full labeled evaluation sets, without an orbit quotient."""
    quadratic = evaluation(2)
    squares = {
        ''.join(str(sum(a*b for a, b in zip(coefficients, row))**2 % 5)
                for row in quadratic)
        for coefficients in product(range(5), repeat=6)
    }
    line = projective_points(2)
    binary_patterns = tuple(word for word in product((0, 1, 4), repeat=6)
                            if sum(word) % 5 == 0)
    cones = set()
    for vertex in POINTS:
        annihilators = [v for v in POINTS if dot(v, vertex) == 0]
        a, b = annihilators[:2]
        image = []
        for v in POINTS:
            x, y = dot(a, v), dot(b, v)
            image.append(None if x == y == 0 else line.index(
                (1, y*pow(x, -1, 5) % 5) if x else (0, 1)))
        require(image.count(None) == 1 and all(image.count(j) == 5 for j in range(6)),
                'binary quotient fiber sizes')
        for word in binary_patterns:
            cones.add(''.join('0' if j is None else str(word[j]) for j in image))
    return squares, cones, binary_patterns
