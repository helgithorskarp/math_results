"""Deterministic rational core proposals; positivity requires exact checking."""
from decimal import Decimal as D, localcontext, ROUND_HALF_EVEN
from fractions import Fraction as F
from itertools import combinations
from math import lcm
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cubic_seven_census import move, require


def setup(case):
    members = sorted([1 << i for i in range(7)] +
                     [sum(1 << i for i in t) for t in combinations(range(7), 2)] +
                     case['triple_masks'])
    star_sizes = [sum(a >> i & 1 for a in members) for i in range(7)]
    require(len(set(star_sizes)) == 1, 'unequal input stars')
    s = star_sizes[0]
    pairs = {(a, b) for a, b in combinations(members, 2) if not a & b}
    orbits, reps = [], []
    while pairs:
        a, b = min(pairs)
        orbit = {tuple(sorted((move(a, p), move(b, p)))) for p in case['point_group']}
        require(orbit <= pairs, 'pair orbit leaves available domain')
        pairs -= orbit
        orbits.append(orbit)
        reps.append((a, b))
    addresses = {(a, i): {} for a in members for i in range(7) if not a >> i & 1}
    for k, orbit in enumerate(orbits):
        for a, b in orbit:
            for i in range(7):
                if b >> i & 1:
                    row = addresses[a, i]
                    row[k] = row.get(k, 0)+1
                if a >> i & 1:
                    row = addresses[b, i]
                    row[k] = row.get(k, 0)+1
    rows = [dict(row) for row in sorted({tuple(sorted(row.items())) for row in addresses.values()})]
    return members, s, reps, orbits, rows


def fractionfree_echelon(original, variables, rhs):
    """Exact sparse Bareiss elimination of all affine equations."""
    rows = [dict(row) for row in original]
    for row in rows:
        if rhs:
            row[variables] = rhs
    origins = list(range(len(rows)))
    rank, previous, pivots, chosen = 0, 1, [], []
    for column in range(variables):
        k = next((k for k in range(rank, len(rows)) if rows[k].get(column)), None)
        if k is None:
            continue
        rows[k], rows[rank] = rows[rank], rows[k]
        origins[k], origins[rank] = origins[rank], origins[k]
        chosen.append(origins[rank])
        pivot_row = rows[rank]
        pivot = pivot_row[column]
        for i in range(rank+1, len(rows)):
            row = rows[i]
            left = row.get(column, 0)
            keys = row.keys() | pivot_row.keys() if left else row.keys()
            updated = {}
            for j in keys:
                if j <= column:
                    continue
                numerator = pivot*row.get(j, 0)-left*pivot_row.get(j, 0)
                value, remainder = divmod(numerator, previous)
                require(remainder == 0, 'nonexact affine Bareiss division')
                if value:
                    updated[j] = value
            rows[i] = updated
        pivots.append(column)
        previous = pivot
        rank += 1
    require(all(not row for row in rows[rank:]), 'inconsistent affine system')
    return rows[:rank], pivots, [original[i] for i in chosen]


def decimal_proposal(basis, weights, rhs, target):
    """70-digit LDL solve proposes entries; no approximate PSD claim follows."""
    rank, variables = len(basis), len(weights)
    omega = lcm(*weights)
    columns = [[] for _ in weights]
    for i, row in enumerate(basis):
        for j, value in row.items():
            columns[j].append((i, value))
    gram = [[0]*rank for _ in range(rank)]
    for j, incidences in enumerate(columns):
        multiplier = omega//weights[j]
        for i, left in incidences:
            for k, right in incidences:
                gram[i][k] += multiplier*left*right
    with localcontext() as context:
        context.prec = 70
        context.rounding = ROUND_HALF_EVEN
        diagonal, lower = [], [[D(int(i == j)) for j in range(rank)] for i in range(rank)]
        for i in range(rank):
            pivot = D(gram[i][i])-sum((lower[i][k]**2*diagonal[k] for k in range(i)), D(0))
            require(pivot > 0, 'proposal LDL pivot failed; not mathematical infeasibility')
            diagonal.append(pivot)
            for j in range(i+1, rank):
                lower[j][i] = (D(gram[j][i])-sum(
                    (lower[j][k]*lower[i][k]*diagonal[k] for k in range(i)), D(0)))/pivot
        y = []
        for i, row in enumerate(basis):
            b = D(omega*(rhs-(1+target)*sum(row.values())))
            y.append(b-sum((lower[i][k]*y[k] for k in range(i)), D(0)))
        multipliers = [D(0)]*rank
        for i in range(rank-1, -1, -1):
            multipliers[i] = y[i]/diagonal[i]-sum(
                (lower[j][i]*multipliers[j] for j in range(i+1, rank)), D(0))
        proposal = [D(1+target)+sum((D(value)*multipliers[i] for i, value in columns[j]), D(0))/D(weights[j])
                    for j in range(variables)]
        return proposal


def prepare(case, target=-3):
    members, s, reps, orbits, original = setup(case)
    variables = len(orbits)
    echelon, pivots, basis = fractionfree_echelon(original, variables, s)
    proposal = decimal_proposal(basis, [len(o) for o in orbits], s, target)
    return members, s, orbits, original, echelon, pivots, proposal, target


def candidate(prepared, grid=20):
    members, s, orbits, original, echelon, pivots, proposal, target = prepared
    variables = len(orbits)
    free = sorted(set(range(variables))-set(pivots))
    values = [None]*variables
    with localcontext() as context:
        context.prec = 70
        context.rounding = ROUND_HALF_EVEN
        for j in free:
            numerator = int((proposal[j]*grid).to_integral_value(rounding=ROUND_HALF_EVEN))
            values[j] = F(numerator, grid)
    for row, pivot in reversed(list(zip(echelon, pivots))):
        residual = F(row.get(variables, 0))
        for j, value in row.items():
            if j not in (pivot, variables):
                require(values[j] is not None, 'affine echelon is not triangular')
                residual -= value*values[j]
        values[pivot] = residual/row[pivot]
    require(all(sum((value*values[j] for j, value in row.items()), F(0)) == s for row in original),
            'complete exact affine equations fail')
    entries = {pair: values[j] for j, orbit in enumerate(orbits) for pair in orbit}
    c = [[F(s-1) if a == b else F(-1) if a & b else
          entries[min(a, b), max(a, b)]-1 for b in members] for a in members]
    return members, s, c, {'pair_orbits': variables, 'affine_rank': len(pivots),
                          'free_variables': len(free), 'target': target, 'grid': grid,
                          'decimal_precision': 70}


def construct(case, target=-3, grid=20):
    return candidate(prepare(case, target), grid)
