"""Independent exact evaluation/interpolation and de Casteljau margin audit.

No author or prerequisite Python module is imported. Original cover/graph
witnesses are explicitly exported by replay_parent.py, a separate trusted
dependency replay. All new polynomial coefficients and relaxation margins
are reconstructed here from the written Gram/chart definitions.
"""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path
import resource
import sys
import time

OLD_DELTA = Q(1, 156250)
NEW_EPSILON = Q(3, 40000000)
NEW_GROWTH = Q(2837, 32)
NEW_DELTA = NEW_EPSILON * NEW_GROWTH
DEGREES = (6, 2, 2)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def inverse(matrix):
    n = len(matrix)
    rows = [list(row) + [Q(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if rows[i][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [x / scale for x in rows[col]]
        for i in range(n):
            if i != col:
                scale = rows[i][col]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[col])]
    return [row[n:] for row in rows]


def bernstein_inverse(degree):
    nodes = [Q(i, degree) for i in range(degree + 1)]
    matrix = [[Q(comb(degree, j)) * x ** j * (1 - x) ** (degree - j)
               for j in range(degree + 1)] for x in nodes]
    return inverse(matrix)


def metric(u, v, t):
    return (1 - t * t) * (u * u + v * v) + 2 * t * (1 - t) * u * v


def core(t):
    r = 2 * t / (1 + t)
    return {
        0: (r*r-1, -r, r+r*r), 1: (r, -1, r), 2: (1, 0, 0),
        3: (r, r, -1), 4: (r*r*r+r*r-r, r*r*r+2*r*r-1, -r-r*r),
        5: (r*r-1, r+r*r, -r), 6: (0, 1, 0), 7: (0, 0, 1)}


def actual_polynomial(label, t, u, v):
    """A_label^T H Y - t D R, evaluated exactly from the geometry."""
    denominator = (1 + t) ** 3
    radius = 1 + metric(u, v, t)
    y = (radius - 2 - 2 * t * (u + v), 2 * u, 2 * v)
    h_y = [(1 - t) * y[j] + t * sum(y) for j in range(3)]
    a = [denominator * z for z in core(t)[label]]
    return sum(a[j] * h_y[j] for j in range(3)) - t * denominator * radius


def contract(values, axis, matrix):
    output = {}
    others = [i for i in range(3) if i != axis]
    for rest in product(*(range(DEGREES[i] + 1) for i in others)):
        base = [0, 0, 0]
        for i, value in zip(others, rest):
            base[i] = value
        for destination in range(DEGREES[axis] + 1):
            total = Q(0)
            for source in range(DEGREES[axis] + 1):
                base[axis] = source
                total += matrix[destination][source] * values[tuple(base)]
            base[axis] = destination
            output[tuple(base)] = total
    return output


def interpolate(label, lo, hi):
    values = {}
    for i, j, k in product(range(7), range(3), range(3)):
        t, u, v = lo + (hi - lo) * Q(i, 6), -4 + 4 * j, -4 + 4 * k
        values[i, j, k] = actual_polynomial(label, t, Q(u), Q(v))
    for axis, degree in enumerate(DEGREES):
        values = contract(values, axis, bernstein_inverse(degree))
    return values


def split(row, x):
    levels = [list(row)]
    while len(levels[-1]) > 1:
        previous = levels[-1]
        levels.append([(1-x)*a + x*b for a, b in zip(previous, previous[1:])])
    return [level[0] for level in levels], [level[-1] for level in reversed(levels)]


def restricted(row, a, b):
    need(0 <= a < b <= 1, 'Closed nonempty subinterval')
    _, right = split(row, a)
    left, _ = split(right, (b-a)/(1-a))
    return left


def cell_coefficients(values, cell):
    need(len(cell) == 3 and all(type(z) is int for z in cell), 'Integer dyadic cell')
    d, i, j = cell
    need(0 <= d <= 12 and 0 <= i < 2**d and 0 <= j < 2**d, 'Dyadic cell bounds')
    output = dict(values)
    for axis, index in [(1, i), (2, j)]:
        left, right = Q(index, 2**d), Q(index+1, 2**d)
        others = [z for z in range(3) if z != axis]
        changed = {}
        for rest in product(*(range(DEGREES[z]+1) for z in others)):
            base = [0, 0, 0]
            for z, value in zip(others, rest):
                base[z] = value
            row = []
            for k in range(3):
                base[axis] = k
                row.append(output[tuple(base)])
            for k, value in enumerate(restricted(row, left, right)):
                base[axis] = k
                changed[tuple(base)] = value
        output = changed
    return output


def factor(cell, lo, hi):
    d, i, j = cell
    side = Q(8, 2**d)
    us = [-4 + side*i, -4 + side*(i+1)]
    vs = [-4 + side*j, -4 + side*(j+1)]
    return (1+hi)**3 * max(1+metric(u, v, lo) for u, v in product(us, vs))


def evaluate_bernstein(values, coordinates):
    weights = [[Q(comb(n, j))*x**j*(1-x)**(n-j) for j in range(n+1)]
               for n, x in zip(DEGREES, coordinates)]
    return sum(c*weights[0][i]*weights[1][j]*weights[2][k]
               for (i, j, k), c in values.items())


def stability():
    lo, hi, pilot = Q(14,25), Q(593,1000), Q(1,10000)
    need(2*hi/(1+hi) < Q(3,4), 'Reflection factor below three quarters')
    need(0 < lo-pilot and hi < Q(3,5), 'Positive nondegenerate anchor interval')
    need(2+2*(lo-pilot) >= Q(8,5)**2 and 2-2*hi >= Q(4,5)**2, 'Reflection denominators')
    need(1-Q(3,4)**2-4*pilot**2 > Q(1,2)**2, 'Reflection normal branch gap')
    need(3+16*pilot <= 4 and 10*pilot < Q(4,5) and 2*(1-hi)>Q(4,5)**2,
         'Normal-coordinate stability and wrong-branch exclusion')
    need(1-Q(3,5)**2 >= Q(4,5)**2 and Q(3,5)**2 <= 1-Q(3,5)**2,
         'Anchor square-root bounds')
    need(Q(3,5)**2 <= 4*(1-Q(3,5)**2)**3 and Q(5,16)+7*pilot<Q(1,2),
         'Inverse-square-root and anchor transverse bounds')
    need(1-Q(3,5)**2-Q(1,2)**2>Q(1,2)**2, 'Anchor normal gap')
    error = {2: Q(0), 6: Q(2), 7: Q(17)}
    for new, a, b, old in [(1,2,7,6),(3,2,6,7),(0,1,7,2),(5,3,6,2),(4,3,5,6)]:
        error[new] = 20 + Q(3,4)*(error[a]+error[b]) + error[old]
    need(max(error.values()) == NEW_GROWTH, 'Exact sharpened growth')
    need(NEW_EPSILON <= pilot and NEW_DELTA == Q(8511,1280000000), 'Improved tolerance bridge')
    need(hi+NEW_DELTA<1 and 16*(1-hi)*(1-hi-NEW_DELTA)**2>1,
         'Complete unchanged square chart at improved relaxation')
    return {'growth': str(NEW_GROWTH), 'epsilon': str(NEW_EPSILON),
            'delta': str(NEW_DELTA), 'errors': {str(k):str(error[k]) for k in sorted(error)}}


def audit(exported, expected):
    kind = exported['strip']
    lo, hi = [Q(*z) for z in exported['interval']]
    need((lo,hi) == ((Q(14,25),Q(29,50)) if kind=='lower' else (Q(29,50),Q(593,1000))), 'Exact strip')
    polys = [interpolate(label, lo, hi) for label in range(8)]
    # Degree bounds prove recovery. Additional exact off-grid evaluations test
    # indexing, axes and the de Casteljau implementation independently.
    checks = 0
    for label in range(8):
        for x,y,z in [(Q(1,7),Q(2,7),Q(3,7)),(Q(5,11),Q(7,11),Q(3,11))]:
            need(evaluate_bernstein(polys[label], (x,y,z)) ==
                 actual_polynomial(label, lo+(hi-lo)*x, -4+8*y, -4+8*z), 'Off-grid identity')
            checks += 1
    old_rows, new_rows, limits = [], [], []
    for cell, method, label in exported['discarded']:
        if method != 'bernstein':
            continue
        need(type(label) is int and 0 <= label < 8, 'Actual core label')
        values = cell_coefficients(polys[label], cell)
        margin, bound = min(values.values()), factor(cell, lo, hi)
        need(margin-OLD_DELTA*bound>0, 'Original transferred margin')
        need(margin-NEW_DELTA*bound>0, 'Improved transferred margin')
        old_rows.append([cell,label,str(margin),str(bound),str(margin-OLD_DELTA*bound)])
        new_rows.append([cell,label,str(margin),str(bound),str(margin-NEW_DELTA*bound)])
        limits.append(margin/bound)
    old_duals, new_duals = [], []
    for tag, certificates in [('single',exported['single_cells']),('pair',exported['conditioned_pairs'])]:
        for cert in certificates:
            cells = [cert['cell']] if tag=='single' else cert['cells']
            bounds = [factor(cell,lo,hi) for cell in cells]
            support, weights = cert['support'], [Q(x) for x in cert['weights']]
            need(len(support)==len(set(support))==len(weights) and all(type(i) is int for i in support),
                 'Unique exact dual support')
            need(all(x>=0 for x in weights) and sum(weights)==1, 'Normalized nonnegative dual weights')
            original = Q(cert['negative_rhs'])
            need(original<0, 'Inherited exact negative RHS')
            weight = sum((w*bounds[index//8] for index,w in zip(support,weights)
                          if 0<=index<8*len(cells)), Q(0))
            need(original+OLD_DELTA*weight<0, 'Original dual transfer')
            need(original+NEW_DELTA*weight<0, 'Improved dual transfer')
            old_duals.append([tag,cells,str(original),str(weight),str(original+OLD_DELTA*weight)])
            new_duals.append([tag,cells,str(original),str(weight),str(original+NEW_DELTA*weight)])
            if weight:
                limits.append(-original/weight)
    need(len(old_rows)==expected['bernstein_discards_transferred'] and
         digest(old_rows)==expected['bernstein_transfer_sha256'] and
         len(old_duals)==expected['duals_transferred'] and
         digest(old_duals)==expected['dual_transfer_sha256'], 'Entrywise original transfer hashes')
    limit = min(limits)
    need(limit==Q('853/20845400' if kind=='lower' else '868844/128783337075'), 'Complete relaxation limit')
    return {'strip':kind,'status':'INTERPOLATION_AND_DE_CASTELJAU_TRANSFERS_VERIFIED',
            'bernstein_records':len(new_rows),'dual_records':len(new_duals),
            'old_bernstein_hash':digest(old_rows),'old_dual_hash':digest(old_duals),
            'new_bernstein_hash':digest(new_rows),'new_dual_hash':digest(new_duals),
            'minimum_new_Bernstein_margin':str(min(Q(z[-1]) for z in new_rows)),
            'maximum_new_dual_rhs':str(max(Q(z[-1]) for z in new_duals)) if new_duals else None,
            'relaxation_limit':str(limit),'off_grid_checks':checks,
            'inherited_cover_cells':exported['receipt']['cover_cells'],
            'inherited_clique_search_states':exported['receipt']['clique_search_states'],
            'stability':stability()}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--export',type=Path,required=True)
    p.add_argument('--author-expected',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();began=time.monotonic()
    exported=json.loads(a.export.read_text())
    rows=json.loads(a.author_expected.read_text())['strips']
    expected=next(z for z in rows if z['strip']==exported['strip'])
    result=audit(exported,expected)
    result.update(agent='six-reviewer-5',role='independent reviewer',python=sys.version.split()[0],
                  optimization=sys.flags.optimize,seconds=time.monotonic()-began,
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  trust_boundary='Original cover/capacity/graph and old affine cancellation proofs are pinned dependencies; all changed margins are independently reconstructed.')
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
