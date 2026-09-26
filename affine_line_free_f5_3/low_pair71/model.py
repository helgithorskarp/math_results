"""Exact necessary incidence and centered-moment equations at |S|=71.

No optimization package is used here. Column types are plane spectra (s),
ordered parallel profiles (p), and six-plane line pencils (l).
"""
from itertools import combinations_with_replacement, permutations, product

N = 71
FORMS = {
    "zero": ((0, 0, 0), (31, 0, 0)),
    "rank1_square": ((1, 0, 0), (6, 25, 0)),
    "rank1_nonsquare": ((2, 0, 0), (6, 0, 25)),
    "rank2_split": ((1, 4, 0), (11, 10, 10)),
    "rank2_anisotropic": ((1, 2, 0), (1, 15, 15)),
    "rank3_square": ((1, 1, 1), (6, 15, 10)),
    "rank3_nonsquare": ((1, 1, 2), (6, 10, 15)),
}
LOW_PROFILES = (
    (7, 16, 16, 16, 16),
    (8, 15, 16, 16, 16),
    (9, 14, 16, 16, 16),
    (9, 15, 15, 16, 16),
    (9, 15, 16, 16, 15),
)


def character(value):
    value %= 5
    return 0 if value == 0 else 1 if value in (1, 4) else -1


def projective_points(dimension):
    return tuple(v for v in product(range(5), repeat=dimension)
                 if any(v) and next(x for x in v if x) == 1)


def parallel_profiles():
    """Scaling a normal permits q=0,1,2; both signs of a profile remain."""
    profiles = []
    for sizes in combinations_with_replacement(range(7, 17), 5):
        if sum(sizes) != N:
            continue
        for p in sorted(set(permutations(sizes))):
            if sum(t * p[t] for t in range(5)) % 5:
                continue
            q = sum(t * t * p[t] for t in range(5)) % 5
            if q in (0, 1, 2):
                profiles.append((p, q))
    return tuple(profiles)


def incidence_system(spectra):
    pencils = tuple((k, p) for k in range(5)
                    for p in combinations_with_replacement(
                        range(max(7, 5*k-9), 17), 6)
                    if sum(p) == N + 5*k)
    columns = tuple([('s', s) for s in spectra]
                    + [('p', p) for p in parallel_profiles()]
                    + [('l', p) for p in pencils])
    names, matrix, base = [], [], []

    def row(name, function, rhs):
        names.append(name)
        matrix.append(tuple(function(kind, data) for kind, data in columns))
        base.append(rhs)

    row('planes', lambda k, p: int(k == 's'), 155)
    row('plane_points', lambda k, p: p[0] if k == 's' else 0, 31*N)
    row('plane_pairs', lambda k, p: p[0]*(p[0]-1)//2 if k == 's' else 0,
        6*N*(N-1)//2)
    row('parallel_classes', lambda k, p: int(k == 'p'), 31)
    for m in range(7, 17):
        row(f'parallel_{m}',
            lambda k, p: int(p[0] == m) if k == 's'
            else -p[0].count(m) if k == 'p' else 0, 0)
    for c in range(5):
        for m in range(7, 17):
            row(f'pencil_{c}_{m}',
                lambda k, p: (p[c+1] if p[0] == m else 0) if k == 's'
                else -p[1].count(m) if k == 'l' and p[0] == c else 0, 0)
    row('lines', lambda k, p: int(k == 'l'), 775)
    row('line_points', lambda k, p: p[0] if k == 'l' else 0, 31*N)
    row('line_pairs', lambda k, p: p[0]*(p[0]-1)//2 if k == 'l' else 0,
        N*(N-1)//2)
    # These four right-hand sides are supplied by case_rhs.
    row('barycenter_star', lambda k, p: p[0][0] if k == 'p' else 0, 0)
    for q in (0, 1, 2):
        row(f'quadratic_{q}', lambda k, p: int(k == 'p' and p[1] == q), 0)
    objective = tuple(int(k == 's' and p[0] <= 9) for k, p in columns)
    return columns, tuple(names), tuple(matrix), tuple(base), objective


def case_rhs(base, form, mu_in_set):
    if mu_in_set not in (0, 1):
        raise ValueError('mu_in_set must be a bit')
    return base[:-4] + (6*N + 25*mu_in_set,) + FORMS[form][1]
