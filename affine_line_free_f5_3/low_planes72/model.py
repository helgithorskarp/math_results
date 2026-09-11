"""Exact incidence system and finite projection cover; no optimizer needed."""
from itertools import combinations_with_replacement, product


def incidence_system(spectra):
    parallel = [p for p in combinations_with_replacement(range(8, 17), 5)
                if sum(p) == 72]
    pencils = [(k, p) for k in range(5)
               for p in combinations_with_replacement(
                   range(max(8, 5*k-8), 17), 6)
               if sum(p) == 72+5*k]
    columns = [('s', s) for s in spectra]
    columns += [('p', p) for p in parallel]
    columns += [('l', p) for p in pencils]
    names, matrix, rhs = [], [], []

    def row(name, coefficient, value):
        names.append(name)
        matrix.append([coefficient(kind, x) for kind, x in columns])
        rhs.append(value)

    row('planes', lambda t, x: int(t == 's'), 155)
    row('plane_points', lambda t, x: x[0] if t == 's' else 0, 2232)
    row('plane_pairs', lambda t, x: x[0]*(x[0]-1)//2 if t == 's' else 0, 15336)
    row('parallel_classes', lambda t, x: int(t == 'p'), 31)
    for m in range(8, 17):
        row(f'parallel_size_{m}', lambda t, x:
            int(x[0] == m) if t == 's' else (-x.count(m) if t == 'p' else 0), 0)
    for k in range(5):
        for m in range(8, 17):
            row(f'pencil_{k}_size_{m}', lambda t, x:
                (x[1+k] if x[0] == m else 0) if t == 's'
                else (-x[1].count(m) if t == 'l' and x[0] == k else 0), 0)
    row('lines', lambda t, x: int(t == 'l'), 775)
    row('line_points', lambda t, x: x[0] if t == 'l' else 0, 2232)
    row('line_pairs', lambda t, x: x[0]*(x[0]-1)//2 if t == 'l' else 0, 2556)
    return columns, names, matrix, rhs


def projection_system(offsets):
    """30 rows: x=b, then y=a*x+b; 25 columns: lexicographic (x,y)."""
    points = list(product(range(5), repeat=2))
    lines = [[int(x == b) for x, y in points] for b in range(5)]
    lines += [[int((y-a*x) % 5 == b) for x, y in points]
              for a in range(5) for b in range(5)]
    bounds = [16]*30
    for a, b in enumerate(offsets):
        bounds[5+5*a+b] = 9
    return lines, bounds


PROFILES = ((8, 16, 16, 16, 16), (9, 15, 16, 16, 16))
CASES = tuple(combinations_with_replacement(range(2), 3))
