"""The prior incidence system, augmented by exact plane-pair identities."""
import importlib.util
from itertools import combinations_with_replacement
from pathlib import Path


def choose2(n):
    return n * (n - 1) // 2


def system(spectra):
    path = Path(__file__).resolve().parent.parent / 'low_planes72' / 'model.py'
    spec = importlib.util.spec_from_file_location('prior_incidence_model', path)
    prior = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prior)
    columns, names, rows, rhs = prior.incidence_system(spectra)
    sizes = [[int(kind == 's' and data[0] == m) for kind, data in columns]
             for m in range(8, 17)]
    pairs = list(combinations_with_replacement(range(8, 17), 2))
    pair_rows = []
    for m, n in pairs:
        row = []
        for kind, data in columns:
            block = data if kind == 'p' else data[1] if kind == 'l' else ()
            i, j = block.count(m), block.count(n)
            row.append(choose2(i) if m == n else i * j)
        pair_rows.append(row)
    extended = [row[:] for row in rows] + [sizes[0], sizes[1]]
    labels = names + ['a8_zero', 'a9_eleven']
    target = rhs + [0, 11]
    for (m, n), row in zip(pairs, pair_rows):
        if m == n == 9:
            extended.append(row)
            labels.append('pair_9_9')
            target.append(55)
        elif m == 9 or n == 9:
            other = n if m == 9 else m
            extended.append([x - 11*y for x, y in zip(row, sizes[other-8])])
            labels.append(f'pair_9_{other}')
            target.append(0)
    return columns, names, rows, rhs, sizes, pairs, pair_rows, labels, extended, target
