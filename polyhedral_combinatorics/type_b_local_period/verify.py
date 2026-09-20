#!/usr/bin/env python3
"""Exact finite corroboration, not a formal proof of local Euler--Maclaurin.

No previous research package or third-party library is imported.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, factorial
from pathlib import Path
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def rref(a, b=None):
    if not a:
        return [], []
    cols = len(a[0])
    rows = [[Q(x) for x in row]+([] if b is None else [Q(b[i])])
            for i, row in enumerate(a)]
    pivots = []
    for col in range(cols):
        pivot = next((i for i in range(len(pivots), len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        j = len(pivots)
        rows[j], rows[pivot] = rows[pivot], rows[j]
        factor = rows[j][col]
        rows[j] = [x/factor for x in rows[j]]
        for i in range(len(rows)):
            if i != j:
                factor = rows[i][col]
                rows[i] = [x-factor*y for x, y in zip(rows[i], rows[j])]
        pivots.append(col)
    if b is not None:
        require(all(not row[-1] for row in rows[len(pivots):]), 'inconsistent equations')
    return rows[:len(pivots)], pivots


def rank(a):
    return len(rref(a)[1])


def solve_square(a, b):
    rows, pivots = rref(a, b)
    require(len(pivots) == len(a), 'singular matrix')
    return tuple(row[-1] for row in rows)


def affine_dimension(vertices):
    if not vertices:
        return -1
    v = vertices[0]
    return rank([[x-y for x, y in zip(w, v)] for w in vertices[1:]])


def validate(rows, rhs):
    require(bool(rows) and len(rows) == len(rhs), 'empty or mismatched system')
    d = len(rows[0])
    require(d >= 1 and all(len(a) == d for a in rows), 'invalid dimensions')
    require(all(type(x) is int and x in (-1, 0, 1) for a in rows for x in a),
            'non-root coefficient')
    require(all(sum(x != 0 for x in a) in (1, 2) for a in rows), 'non-root support')
    require(all(type(b) is int for b in rhs), 'nonintegral offset')


def vertices_of(rows, rhs):
    d = len(rows[0])
    vertices = set()
    for indices in combinations(range(len(rows)), d):
        a = [rows[i] for i in indices]
        if rank(a) != d:
            continue
        v = solve_square(a, [rhs[i] for i in indices])
        if all(dot(a, v) <= b for a, b in zip(rows, rhs)):
            vertices.add(v)
    return sorted(vertices)


def affine_has_integer_point(rows, rhs):
    if not rows:
        return True
    reduced, pivots = rref(rows, rhs)
    free = [i for i in range(len(rows[0])) if i not in pivots]
    # Root systems have integral coefficients of the free variables in RREF.
    # Thus any integral solution differs from the free-zero solution by an
    # integral vector, and that particular solution decides affine integrality.
    require(all(row[j].denominator == 1 for row in reduced for j in free),
            'unexpected nonintegral nullspace basis')
    return all(row[-1].denominator == 1 for row in reduced)


def hull_area(points):
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    points = sorted(set(points))
    lower, upper = [], []
    for stack, seq in [(lower, points), (upper, reversed(points))]:
        for p in seq:
            while len(stack) >= 2 and cross(stack[-2], stack[-1], p) <= 0:
                stack.pop()
            stack.append(p)
    hull = lower[:-1]+upper[:-1]
    return abs(sum(a[0]*b[1]-a[1]*b[0] for a, b in
                   zip(hull, hull[1:]+hull[:1])))/2


def coordinate_volume(vertices, dim):
    if dim == 0:
        return Q(1)
    free = [i for i in range(len(vertices[0]))
            if len({v[i] for v in vertices}) > 1]
    require(len(free) == dim, 'leading face is not a coordinate face')
    require(dim <= 2, 'fixture volume dimension unsupported')
    if dim == 1:
        values = [v[free[0]] for v in vertices]
        return max(values)-min(values)
    return hull_area([tuple(v[i] for i in free) for v in vertices])


def geometry(rows, rhs):
    validate(rows, rhs)
    vertices = vertices_of(rows, rhs)
    d = len(rows[0])
    if affine_dimension(vertices) != d:
        return None
    # Fixture systems are bounded by explicit boxes or the displayed
    # nonnegative weighted triangle / pyramid descriptions.
    facet_data = {}
    for a, b in zip(rows, rhs):
        indices = frozenset(i for i, v in enumerate(vertices) if dot(a, v) == b)
        if affine_dimension([vertices[i] for i in indices]) == d-1:
            facet_data[indices] = (a, b)
    facet_sets = list(facet_data)
    facet_rows = [facet_data[s][0] for s in facet_sets]
    facet_rhs = [facet_data[s][1] for s in facet_sets]
    faces = {frozenset(range(len(vertices)))}
    for facet in facet_sets:
        faces |= {face & facet for face in list(faces) if face & facet}
    nonintegral = []
    for face in faces:
        active = [j for j, f in enumerate(facet_sets) if face <= f]
        if not affine_has_integer_point([facet_rows[j] for j in active],
                                       [facet_rhs[j] for j in active]):
            vs = [vertices[i] for i in sorted(face)]
            dim = affine_dimension(vs)
            nonintegral.append((dim, len(active), vs))
    simple = all(sum(i in f for f in facet_sets) == d for i in range(len(vertices)))
    require(all(x.denominator <= 2 for v in vertices for x in v), 'not half integral')
    if not nonintegral:
        g, local, volume_sum = None, True, Q(0)
        leading_faces = 0
    else:
        k = max(t[0] for t in nonintegral)
        leading = [t for t in nonintegral if t[0] == k]
        g, local = d-k, all(t[1] == d-k for t in leading)
        volume_sum = (sum((coordinate_volume(t[2], k) for t in leading), Q(0))
                      if local else None)
        leading_faces = len(leading)
    return {'vertices': vertices, 'facets': len(facet_sets), 'faces': len(faces),
            'simple': simple, 'g': g, 'local_condition': local,
            'volume_sum': volume_sum, 'leading_faces': leading_faces}


def counts_direct(rows, rhs, vertices, max_n):
    d = len(rows[0])
    lo = [min(v[i] for v in vertices) for i in range(d)]
    hi = [max(v[i] for v in vertices) for i in range(d)]
    by_last = [[] for _ in range(d)]
    for a, b in zip(rows, rhs):
        support = [i for i, x in enumerate(a) if x]
        by_last[support[-1]].append((a, b, support))
    output = []
    for n in range(max_n+1):
        values = [0]*d
        def visit(i):
            if i == d:
                return 1
            lower = -((-n*lo[i]).numerator//(-n*lo[i]).denominator)
            upper = (n*hi[i]).numerator//(n*hi[i]).denominator
            for a, b, support in by_last[i]:
                remaining = n*b-sum(a[j]*values[j] for j in support if j < i)
                if a[i] == 1:
                    upper = min(upper, remaining)
                else:
                    lower = max(lower, -remaining)
            total = 0
            for x in range(lower, upper+1):
                values[i] = x
                total += visit(i+1)
            return total
        output.append(visit(0))
    return output


def poly_mul(a, b):
    out = [Q(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def poly_eval(p, x):
    out = Q(0)
    for a in reversed(p):
        out = out*x+a
    return out


def interpolate(nodes, values):
    out = [Q(0)]*len(nodes)
    for x, y in zip(nodes, values):
        p, denominator = [Q(1)], Q(1)
        for z in nodes:
            if z != x:
                p = poly_mul(p, [-z, 1])
                denominator *= x-z
        out = [a+y*b/denominator for a, b in zip(out, p)]
    return out


def trim(p):
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def ehrhart_check(d, counts):
    residues = []
    for r in (0, 1):
        nodes = list(range(r, 2*d+2, 2))
        residues.append(interpolate(nodes, [counts[n] for n in nodes]))
    for n in range(2*d+2, len(counts)):
        require(poly_eval(residues[n % 2], n) == counts[n], 'residue holdout')
    b = trim([(a-c)/2 for a, c in zip(*residues)])
    h = [sum((-1)**j*comb(d+1, j)*counts[n-2*j]
             for j in range(min(d+1, n//2)+1)) for n in range(len(counts))]
    require(h[-2:] == [0, 0], 'numerator tail')
    h, order = trim(h), 0
    while len(h) > 1 and poly_eval(h, -1) == 0:
        q = [h[0]]
        for a in h[1:-1]:
            q.append(a-q[-1])
        require(q[-1] == h[-1], 'division remainder')
        h, order = trim(q), order+1
    return b, order, poly_eval(h, -1)


def box(d, low=0, high=1):
    rows, rhs = [], []
    for i in range(d):
        for sign, b in [(1, high), (-1, -low)]:
            a = [0]*d
            a[i] = sign
            rows.append(tuple(a)); rhs.append(b)
    return rows, rhs


def one_case(name, rows, rhs, expect_local=True):
    geom = geometry(rows, rhs)
    if geom is None:
        return None
    d = len(rows[0])
    counts = counts_direct(rows, rhs, geom['vertices'], 2*d+5)
    # Literal Cartesian-product enumeration audits the recursive pruning,
    # including translated fixtures with negative coordinate bounds.
    for n in range(3):
        intervals = []
        for i in range(d):
            lower = min(n*v[i] for v in geom['vertices'])
            upper = max(n*v[i] for v in geom['vertices'])
            intervals.append(range(-((-lower).numerator//(-lower).denominator),
                                   upper.numerator//upper.denominator+1))
        literal = sum(all(dot(a, x) <= n*b for a, b in zip(rows, rhs))
                      for x in product(*intervals))
        require(literal == counts[n], 'literal enumeration disagrees: '+name)
    b, order, residual = ehrhart_check(d, counts)
    g = geom['g']
    require(geom['local_condition'] == expect_local, 'unexpected local condition: '+name)
    if g is None:
        require(b == [0], 'integral polytope has parity')
    elif expect_local:
        v = geom['volume_sum']
        require(len(b)-1 == d-g and b[-1] == v/2**(g+1), 'leading theorem: '+name)
        require(order == g and residual == 2**(d-g)*factorial(d-g)*v, 'pole theorem')
    else:
        require(b == [0], 'Stanley control did not collapse')
        require(counts == [comb(n+3, 3) for n in range(2*d+6)], 'Stanley formula')
    return {'name': name, 'dimension': d, 'vertices': len(geom['vertices']),
            'facets': geom['facets'], 'simple': geom['simple'],
            'g': g, 'local_condition': geom['local_condition'],
            'leading_faces': geom['leading_faces'], 'volume_sum': str(geom['volume_sum']),
            'B': [str(x) for x in b], 'root_order': order, 'residual': str(residual)}


def audit_polytopes():
    records, rejected_dim = [], 0
    for b in product(range(3), repeat=4):
        rows, rhs = box(2, -1, 1)
        rows += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        rhs += list(b)
        rec = one_case('planar_'+''.join(map(str, b)), rows, rhs)
        if rec is None:
            rejected_dim += 1
        else:
            records.append(rec)
    named = []
    for capacities in [(1, 1, 1), (2, 3, 4)]:
        rows = [(-1, 0, 0), (0, -1, 0), (0, 0, -1),
                (1, 1, 0), (0, 1, 1), (1, 0, 1)]
        rhs = [0, 0, 0]+list(capacities)
        named.append(one_case('triangle_'+str(capacities), rows, rhs))
    # Signed even-cycle example: four active facets with a half-integral vertex.
    rows, rhs = box(4, -1, 1)
    rows += [(1, 1, 0, 0), (0, 1, 1, 0), (0, 0, 1, 1), (-1, 0, 0, 1)]
    rhs += [1, 1, 1, 0]
    named.append(one_case('signed_even_cycle', rows, rhs))
    # A digon face with two free coordinate directions, globally simple.
    rows, rhs = box(4)
    rows += [(1, -1, 0, 0), (1, 1, 0, 0)]
    rhs += [0, 1]
    named.append(one_case('digon_times_square', rows, rhs))
    # Integral translation and a sign reflection retain the lattice and counts.
    shift, signs = (2, -1, 1, -2), (-1, 1, -1, 1)
    transformed = [tuple(a*s for a, s in zip(row, signs)) for row in rows]
    transformed_rhs = [b+dot(a, shift) for a, b in zip(transformed, rhs)]
    named.append(one_case('translated_reflected_digon', transformed, transformed_rhs))
    require(named[-1]['B'] == named[-2]['B'], 'translation/reflection changed counts')
    # Simple type-B alcove, distinct from the graph-polytope models.
    rows = [(0, 0, -1), (0, -1, 1), (-1, 1, 0), (1, 1, 0)]
    named.append(one_case('B3_alcove', rows, [0, 0, 0, 1]))
    rows = [(-1, 0, 0), (1, -1, 0), (1, 1, 0), (1, 0, -1), (1, 0, 1)]
    named.append(one_case('Stanley_nonsimple_control', rows, [0, 0, 1, 0, 1], False))
    require(not named[0]['simple'] and named[0]['local_condition'], 'local weaker than global')
    require(named[1]['simple'], 'weighted triangle not simple')
    digest = hashlib.sha256(json.dumps(records, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return {'planar_systems': 81, 'full_dimensional_planar': len(records),
            'lower_dimensional_rejected': rejected_dim,
            'nonintegral_planar': sum(r['g'] is not None for r in records),
            'planar_digest': digest, 'named_cases': named,
            'holdout_values': 4*(len(records)+len(named)),
            'literal_enumeration_comparisons': 3*(len(records)+len(named))}


def audit_signed_cones():
    matrices = cases = forests = 0
    for size in range(2, 6):
        for edge_signs in product((-1, 1), repeat=size):
            rows = []
            for i, s in enumerate(edge_signs):
                row = [0]*size
                row[i], row[(i+1) % size] = 1, s
                rows.append(row)
            if rank(rows) != size:
                continue
            matrices += 1
            inverse_columns = [solve_square(rows, [int(i == j) for i in range(size)])
                               for j in range(size)]
            require(all(2*x in (-1, 1) for v in inverse_columns for x in v), 'cycle inverse')
            for rhs in product(range(2), repeat=size):
                v = tuple(sum(inverse_columns[j][i]*rhs[j] for j in range(size))
                          for i in range(size))
                require(all(x.denominator == 1 for x in v) == (sum(rhs) % 2 == 0),
                        'signed RHS parity')
                for slack in product(range(2), repeat=size):
                    y = [v[i]-sum(inverse_columns[j][i]*slack[j] for j in range(size))
                         for i in range(size)]
                    require(all(x.denominator == 1 for x in y)
                            == (sum(rhs) % 2 == sum(slack) % 2), 'slack character')
                    cases += 1
                if sum(rhs) % 2:
                    for mask in range((1 << size)-1):
                        indices = [i for i in range(size) if mask & (1 << i)]
                        require(affine_has_integer_point([rows[i] for i in indices],
                                                        [rhs[i] for i in indices]),
                                'proper-face translation')
                        forests += 1
    invalid = 0
    for rows, rhs in [([], []), ([(2, 0)], [1]), ([(1, 1, 1)], [1]),
                      ([(1, 0)], [Q(1, 2)]), ([(0, 0)], [1])]:
        try:
            validate(rows, rhs)
        except ValueError:
            invalid += 1
        else:
            raise ValueError('malformed system accepted')
    return {'invertible_cycle_matrices': matrices, 'slack_cases': cases,
            'proper_face_affine_checks': forests, 'malformed_systems_rejected': invalid}


def main():
    result = {'status': 'PASS', 'polytopes': audit_polytopes(),
              'signed_cones': audit_signed_cones(),
              'scope': 'Exact finite corroboration; universal proof imports Berline-Vergne'}
    expected = Path(__file__).with_name('expected.json')
    if expected.exists():
        require(result == json.loads(expected.read_text()), 'expected record mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
