"""Original augmented subset incidence and an exact free-coordinate basis.

No seed eigenvalue or expected record is used here. All arithmetic is int/Fraction.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parameters(b, layers):
    require(type(b) is int and 3 <= b <= 14, 'Control block size must be an integer in 3..14')
    require(type(layers) in (list, tuple) and layers, 'Nonempty literal layer list')
    require(all(type(a) is int and 2 <= a < b for a in layers), 'Proper layer integers in 2..b-1')
    require(list(layers) == sorted(set(layers)), 'Unique increasing layers')


def vertices(b, layers):
    parameters(b, layers)
    return [mask for a in layers for mask in sorted(sum(1 << i for i in c)
                for c in combinations(range(b), a))]


def row(mask, b):
    return [1] + [int(bool(mask & (1 << i))) for i in range(b)]


def gram_formula(b, layers):
    parameters(b, layers)
    m = sum(comb(b, a) for a in layers)
    t1 = sum(comb(b - 1, a - 1) for a in layers)
    t2 = sum(comb(b - 2, a - 2) for a in layers)
    return [[m if i == j == 0 else t1 if i == 0 or j == 0 or i == j else t2
             for j in range(b + 1)] for i in range(b + 1)]


def literal_gram(masks, b):
    g = [[0] * (b + 1) for _ in range(b + 1)]
    for mask in masks:
        w = row(mask, b)
        nonzero = [i for i, value in enumerate(w) if value]
        for i in nonzero:
            for j in nonzero:
                g[i][j] += 1
    return g


def rref_incidence(masks, b):
    """RREF on the literal augmented transpose, without a presumed rank."""
    m = len(masks)
    work = [[F(row(mask, b)[i]) for mask in masks] for i in range(b + 1)]
    pivots = []
    r = 0
    for j in range(m):
        p = next((i for i in range(r, b + 1) if work[i][j]), None)
        if p is None:
            continue
        work[r], work[p] = work[p], work[r]
        c = work[r][j]
        work[r] = [x / c for x in work[r]]
        for i in range(b + 1):
            if i != r and work[i][j]:
                q = work[i][j]
                work[i] = [x - q * y if y else x for x, y in zip(work[i], work[r])]
        pivots.append(j)
        r += 1
        if r == b + 1:
            break
    require(all(not x for w in work[r:] for x in w), 'Unaccounted nonzero RREF row')
    for i, p in enumerate(pivots):
        require(all(work[j][p] == int(i == j) for j in range(b + 1)), 'RREF pivot identity')
    free = [j for j in range(m) if j not in set(pivots)]
    columns = []
    for f in free:
        c = {f: F(1)}
        c.update({p: -work[i][f] for i, p in enumerate(pivots) if work[i][f]})
        columns.append(c)
    return dict(pivots=pivots, free=free, columns=columns, rref=work)


def check_basis(masks, b, basis):
    """Check every free original coordinate and every individual star equation."""
    m = len(masks)
    pivots, free, columns = basis['pivots'], basis['free'], basis['columns']
    require(type(pivots) is list and type(free) is list and type(columns) is list, 'Basis lists')
    require(all(type(j) is int and 0 <= j < m for j in pivots + free), 'Original coordinate indices')
    require(len(set(pivots + free)) == m and sorted(pivots + free) == list(range(m)), 'Pivot/free partition')
    require(len(columns) == len(free), 'Every free basis column retained')
    free_set = set(free)
    star_equations = 0
    norm = F(0)
    for f, c in zip(free, columns):
        require(type(c) is dict and c and all(type(j) is int and 0 <= j < m for j in c), 'Sparse original columns')
        require(all(type(value) in (int, F) and value for value in c.values()), 'Exact nonzero basis values')
        require(c.get(f) == 1 and {j for j in c if j in free_set} == {f}, 'Entire free-coordinate identity')
        actions = [F(0)] * (b + 1)
        for j, value in c.items():
            w = row(masks[j], b)
            for p in range(b + 1):
                if w[p]:
                    actions[p] += value
            norm += value * value
        require(all(not value for value in actions), 'Every original constant and point-star action')
        star_equations += len(actions)
    return dict(free_identity_columns=len(columns), star_equations=star_equations, norm_squared=norm,
                nonzero_basis_entries=sum(len(c) for c in columns))


def generate_block(b, layers):
    masks = vertices(b, layers)
    formula, literal = gram_formula(b, layers), literal_gram(masks, b)
    require(literal == formula, 'Every literal/formula Gram entry')
    basis = rref_incidence(masks, b)
    wanted = b if len(layers) == 1 else b + 1
    require(len(basis['pivots']) == wanted, 'Computed rank agrees with ordinary layer-rank proof')
    checked = check_basis(masks, b, basis)
    return dict(b=b, layers=list(layers), masks=masks, gram=literal, basis=basis, checks=checked)
