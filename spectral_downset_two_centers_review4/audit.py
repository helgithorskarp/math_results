#!/usr/bin/env python3
"""Independent integer-matrix audit. No researcher code or solver imported."""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys


def need(condition, message):
    if not condition:
        raise ValueError(message)


def psd_rank(matrix):
    """Symmetric fraction-free Schur elimination, with positive pivots only.

    Every trailing matrix is a positive multiple of a Schur complement.
    A zero diagonal in a PSD matrix has a zero row. Division by the preceding
    positive pivot is exact (Bareiss identity); failure rejects the input.
    """
    a = [list(row) for row in matrix]
    n = len(a)
    need(all(len(row) == n for row in a), 'non-square')
    need(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)), 'asymmetric')
    previous = 1
    for k in range(n):
        need(all(a[i][i] >= 0 for i in range(k, n)), 'negative diagonal')
        for i in range(k, n):
            if a[i][i] == 0:
                need(all(a[i][j] == 0 for j in range(k, n)), 'nonzero zero-diagonal row')
        pivot_row = next((i for i in range(k, n) if a[i][i] > 0), None)
        if pivot_row is None:
            return k
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            for row in a:
                row[k], row[pivot_row] = row[pivot_row], row[k]
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(i, n):
                numerator = pivot * a[i][j] - a[i][k] * a[k][j]
                value, remainder = divmod(numerator, previous)
                need(remainder == 0, 'nonexact Bareiss division')
                a[i][j] = a[j][i] = value
        for i in range(k + 1, n):
            a[i][k] = a[k][i] = 0
        previous = pivot
    return n


def build(t, improved):
    need(isinstance(t, int) and not isinstance(t, bool) and t >= 1, 'bad leaf count')
    leaves = [1 << (i + 2) for i in range(t)]
    members = [0, 1, 2, 3] + leaves + [c | a for c in leaves for a in (1, 2)]
    denominator = 2 * t * (t + 1)
    matrix = []
    for a in members:
        row = []
        for b in members:
            if a == b == 0:
                value = -2 * t if improved else -t * (t + 1)
            elif a == 0 or b == 0:
                other = a or b
                value = 1 if improved and other in leaves else t
            elif a & b:
                value = 0
            elif a.bit_count() == b.bit_count() == 1:
                count = int(a in (1, 2)) + int(b in (1, 2))
                value = 0 if count == 2 else t - 1 if count == 1 else 0 if improved else -1
            elif a.bit_count() == b.bit_count() == 2:
                value = t + 2
            else:
                single, edge = (a, b) if a.bit_count() == 1 else (b, a)
                value = t + 2 if single in (1, 2) else 2 * t + 1 if edge == 3 else t
            row.append(value)
        matrix.append(row)
    return members, denominator, matrix


def check(members, denominator, matrix, s):
    n = len(members)
    need(len(set(members)) == n and members[0] == 0, 'duplicate/empty order')
    need(all(sum(row) == denominator for row in matrix), 'row sum')
    need(all(matrix[i][j] == 0 for i, a in enumerate(members)
             for j, b in enumerate(members) if a & b), 'support')
    star_sizes = [sum(bool(a & (1 << i)) for a in members)
                  for i in range(max(members).bit_length())]
    need(max(star_sizes) == s, 'star size')
    lower = [[(n - s) * matrix[i][j] + (s * denominator if i == j else 0)
              for j in range(n)] for i in range(n)]
    upper = [[(denominator if i == j else 0) - matrix[i][j]
              for j in range(n)] for i in range(n)]
    return psd_rank(lower), psd_rank(upper)


def original_source_hash(t, members, denominator, matrix):
    """Relabel to source's leaf-low/center-high masks, sorted source order."""
    def transport(a):
        return ((bool(a & 1) << t) | (bool(a & 2) << (t + 1)) |
                sum(1 << i for i in range(t) if a & (1 << (i + 2))))
    order = sorted(range(len(members)), key=lambda i: transport(members[i]))
    raw = json.dumps([[str(Fraction(matrix[i][j], denominator)) for j in order]
                      for i in order], separators=(',', ':')).encode()
    return sha256(raw).hexdigest()


def independent_base_families(t, members):
    """Lexicographic include/exclude search; no maximal-clique pivot routine."""
    nonempty = members[1:]
    adjacency = [sum(1 << j for j, b in enumerate(nonempty) if i != j and a & b)
                 for i, a in enumerate(nonempty)]
    best, answers, nodes = 0, set(), 0

    def visit(chosen, available):
        nonlocal best, answers, nodes
        nodes += 1
        size = chosen.bit_count()
        if size + available.bit_count() < best:
            return
        if not available:
            if size > best:
                best, answers = size, set()
            if size == best:
                answers.add(chosen)
            return
        bit = available & -available
        i = bit.bit_length() - 1
        rest = available ^ bit
        visit(chosen | bit, rest & adjacency[i])
        visit(chosen, rest)

    visit(0, (1 << len(nonempty)) - 1)
    expected = {sum(1 << i for i, a in enumerate(nonempty) if a & center) for center in (1, 2)}
    if t == 1:
        expected.add(sum(1 << i for i, a in enumerate(nonempty) if a & 4))
        expected.add(sum(1 << i for i, a in enumerate(nonempty) if a.bit_count() == 2))
    need(best == t + 2 and answers == expected, 'base extremizers')
    return len(answers), nodes


def base_case(t):
    members, d, old = build(t, False)
    _, _, new = build(t, True)
    n, s = len(members), t + 2
    old_ranks, new_ranks = check(members, d, old, s), check(members, d, new, s)
    nullity = 4 if t == 1 else 3
    need(old_ranks == (n - nullity, n - 1), 'original endpoint ranks')
    need(new_ranks == (n - (4 if t == 1 else 2), n - 1), 'improved endpoint ranks')
    old_core = [[old[i][j] + (t * s if i == j else 0) - t
                 for j in range(1, n)] for i in range(1, n)]  # t*C
    new_core = [[new[i][j] + (t * s if i == j else 0) - t
                 for j in range(1, n)] for i in range(1, n)]
    leaves = set(1 << (i + 2) for i in range(t))
    for i, a in enumerate(members[1:]):
        need(sum(old_core[i]) == 0, 'old centering')
        need(sum(new_core[i]) == (t - 1 if a in leaves else 0), 'new core row sum')
        for j, b in enumerate(members[1:]):
            need(new_core[i][j] - old_core[i][j] == int(a != b and a in leaves and b in leaves),
                 'leaf perturbation')
    need(psd_rank(new_core) == n - 1 - (4 if t == 1 else 2), 'new core rank')
    # Independently rebuild the full empty lift from core row sums.
    rows = list(map(sum, new_core))
    q = [[sum(rows)] + [-r for r in rows]] + [[-rows[i]] + row for i, row in enumerate(new_core)]
    lift = [[q[i][j] + t - (t * s if i == j else 0) for j in range(n)] for i in range(n)]
    need(lift == new, 'full empty lift')
    need(all(new[i][j] >= 0 for i in range(n) for j in range(n) if i != j), 'negative off-diagonal')
    # Written cap strengthening: Uplus >= I/t. Check its full core matrix exactly.
    uplus_minus = [[t * n * int(i == j) - t - new_core[i][j] - int(i == j)
                    for j in range(n - 1)] for i in range(n - 1)]
    psd_rank(uplus_minus)
    families, nodes = independent_base_families(t, members)
    return {'t': t, 'N': n, 's': s, 'original_L_rank': old_ranks[0],
            'improved_L_rank': new_ranks[0], 'upper_rank': new_ranks[1],
            'maximum_families': families, 'enumeration_nodes': nodes,
            'original_source_matrix_sha256': original_source_hash(t, members, d, old),
            'improved_integer_matrix_sha256': sha256(json.dumps(new, separators=(',', ':')).encode()).hexdigest()}


def product_case(ts):
    factors = [build(t, True) for t in ts]
    coordinate_members = list(product(*(f[0] for f in factors)))
    shifts = [sum(t + 2 for t in ts[:i]) for i in range(len(ts))]
    members = [sum(a << shift for a, shift in zip(row, shifts)) for row in coordinate_members]
    index_tuples = list(product(*(range(len(f[0])) for f in factors)))
    denominator = 1
    for _, d, _ in factors:
        denominator *= d
    matrix = []
    for aa in index_tuples:
        row = []
        for bb in index_tuples:
            value = 1
            for f, a, b in zip(factors, aa, bb):
                value *= f[2][a][b]
            row.append(value)
        matrix.append(row)
    n, smallest = len(members), min(ts)
    s = n * (smallest + 2) // (3 * smallest + 4)
    eligible = sum(t == smallest for t in ts)
    nullity = eligible * (4 if smallest == 1 else 2)
    ranks = check(members, denominator, matrix, s)
    need(ranks == (n - nullity, n - 1), 'tensor rank')
    return {'t': list(ts), 'N': n, 's': s, 'L_rank': ranks[0], 'upper_rank': ranks[1],
            'maximal_rank_among_all_H': n - nullity}


def controls():
    malformed = [[[0, 1], [1, 2]], [[1, 2], [2, 1]], [[1, 0], [1, 1]], [[-1]]]
    for matrix in malformed:
        try:
            psd_rank(matrix)
        except ValueError:
            pass
        else:
            raise ValueError('malformed matrix accepted')
    need(psd_rank([[1, 1], [1, 1]]) == 1 and psd_rank([[0, 0], [0, 0]]) == 0,
         'singular controls')
    # This perturbation is NOT positive semidefinite by itself.
    try:
        psd_rank([[0, 1], [1, 0]])
    except ValueError:
        pass
    else:
        raise ValueError('false PSD shortcut accepted')
    return len(malformed) + 1


def run():
    cases = [base_case(t) for t in list(range(1, 13)) + [19, 20, 21]]
    return {'agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'method': 'definition-level integer matrices; fraction-free positive-pivot Schur elimination',
            'base_cases': cases, 'products': [product_case(ts) for ts in [(1, 2), (2, 2), (2, 3)]],
            'rejected_controls': controls(),
            'scope': 'Finite exact checks support the independent uniform proof in REVIEW.md; no imported code, classification, solver or floating arithmetic.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--source-expected', type=Path, help='Optional original expected.json comparison, not a proof input')
    args = parser.parse_args()
    result = run()
    if args.source_expected:
        source = json.loads(args.source_expected.read_text())
        observed = {c['t']: c['original_source_matrix_sha256'] for c in result['base_cases']}
        need(observed == {c['t']: c['matrix_sha256'] for c in source['cases']}, 'source matrix hashes')
    if args.check:
        need(result == json.loads(Path(__file__).with_name('expected.json').read_text()), 'expected output')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
