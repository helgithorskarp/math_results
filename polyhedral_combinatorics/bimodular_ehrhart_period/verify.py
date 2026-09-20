#!/usr/bin/env python3
"""Exact finite corroboration, not a formal proof of local Euler--Maclaurin.

Basic rational linear algebra and interpolation adapted from the preceding
type_b_local_period checker. Integer-image and direction-lattice checks are
new. No prior package is imported; no third-party library is required.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, factorial, gcd, lcm
from pathlib import Path
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
    require(all(type(x) is int for a in rows for x in a), 'noninteger coefficient')
    require(all(any(a) for a in rows), 'zero normal')
    require(all(type(b) is int for b in rhs), 'noninteger offset')

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


def determinant(a):
    if not a:
        return 1
    a = [[Q(x) for x in row] for row in a]
    n, out = len(a), Q(1)
    require(all(len(row) == n for row in a), 'nonsquare determinant')
    for j in range(n):
        k = next((i for i in range(j, n) if a[i][j]), None)
        if k is None:
            return 0
        if k != j:
            a[k], a[j] = a[j], a[k]
            out = -out
        pivot = a[j][j]
        out *= pivot
        for i in range(j+1, n):
            factor = a[i][j]/pivot
            for h in range(j+1, n):
                a[i][h] -= factor*a[j][h]
    require(out.denominator == 1, 'nonintegral determinant')
    return int(out)


def image_index(rows):
    if not rows:
        return 1
    q, d = len(rows), len(rows[0])
    require(q <= d and rank(rows) == q, 'dependent image rows')
    out = 0
    for cols in combinations(range(d), q):
        out = gcd(out, abs(determinant([[row[j] for j in cols] for row in rows])))
    require(out > 0, 'infinite image index')
    return out


def independent_system(rows, rhs):
    selected, values = [], []
    for row, b in zip(rows, rhs):
        if rank(selected+[row]) > len(selected):
            selected.append(row); values.append(b)
    return selected, values


def affine_has_integer_point(rows, rhs):
    try:
        rref(rows, rhs)
    except ValueError:
        return False
    rows, rhs = independent_system(rows, rhs)
    if not rows:
        return True
    return image_index(rows) == image_index([list(a)+[b] for a, b in zip(rows, rhs)])


def normalized_volume(vertices, dim):
    if dim == 0:
        return Q(1)
    require(dim == 1, 'fixture volume dimension unsupported')
    vertices = sorted(vertices)
    diff = [b-a for a, b in zip(vertices[0], vertices[-1])]
    scale = lcm(*(x.denominator for x in diff))
    g = gcd(*(int(x*scale) for x in diff))
    require(g > 0, 'degenerate segment')
    return Q(g, scale)


def max_full_minor(rows):
    d = len(rows[0])
    return max(abs(determinant([rows[i] for i in js]))
               for js in combinations(range(len(rows)), d))

def geometry(rows, rhs):
    validate(rows, rhs)
    vertices = vertices_of(rows, rhs)
    d = len(rows[0])
    require(affine_dimension(vertices) == d, 'fixture not full dimensional')
    # Boundedness is explicit in the displayed fixture constructions.
    facet_data = {}
    for a, b in zip(rows, rhs):
        indices = frozenset(i for i, v in enumerate(vertices) if dot(a, v) == b)
        if affine_dimension([vertices[i] for i in indices]) == d-1:
            facet_data[indices] = (a, b)
    facet_sets = list(facet_data)
    face_rows = [facet_data[s][0] for s in facet_sets]
    face_rhs = [facet_data[s][1] for s in facet_sets]
    faces = {frozenset(range(len(vertices)))}
    for facet in facet_sets:
        faces |= {face & facet for face in list(faces) if face & facet}
    bad = []
    for face in faces:
        active = [j for j, f in enumerate(facet_sets) if face <= f]
        a, b = [face_rows[j] for j in active], [face_rhs[j] for j in active]
        if not affine_has_integer_point(a, b):
            vs = [vertices[i] for i in sorted(face)]
            basis, _ = independent_system(a, b)
            bad.append((affine_dimension(vs), len(active), image_index(basis), vs))
    simple = all(sum(i in f for f in facet_sets) == d for i in range(len(vertices)))
    half = all(x.denominator in (1, 2) for v in vertices for x in v)
    if not bad:
        g, local, image_ok, volume, leading = None, True, True, Q(0), []
    else:
        k = max(t[0] for t in bad)
        leading = [t for t in bad if t[0] == k]
        g = d-k
        local = all(t[1] == g for t in leading)
        image_ok = local and all(t[2] == 2 for t in leading)
        volume = (sum((normalized_volume(t[3], k) for t in leading), Q(0))
                  if image_ok else None)
    return {'vertices': vertices, 'facets': len(facet_sets), 'faces': len(faces),
            'simple': simple, 'half_integral': half, 'g': g,
            'local_simple': local, 'index_two': image_ok, 'volume_sum': volume,
            'leading_indices': sorted(t[2] for t in leading),
            'leading_facet_counts': sorted(t[1] for t in leading),
            'max_full_minor': max_full_minor(face_rows)}

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
                if a[i] > 0:
                    upper = min(upper, remaining//a[i])
                else:
                    lower = max(lower, -((-remaining)//a[i]))
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


def one_case(name, rows, rhs, expected_condition=True):
    geom = geometry(rows, rhs)
    d = len(rows[0])
    require(geom['half_integral'], 'fixture not half integral')
    counts = counts_direct(rows, rhs, geom['vertices'], 2*d+5)
    for n in range(3):
        intervals = []
        for i in range(d):
            lo = min(n*v[i] for v in geom['vertices'])
            hi = max(n*v[i] for v in geom['vertices'])
            intervals.append(range(-((-lo).numerator//(-lo).denominator),
                                   hi.numerator//hi.denominator+1))
        literal = sum(all(dot(a, x) <= n*b for a, b in zip(rows, rhs))
                      for x in product(*intervals))
        require(literal == counts[n], 'unpruned enumeration disagreement: '+name)
    b, order, residual = ehrhart_check(d, counts)
    condition = geom['local_simple'] and geom['index_two']
    require(condition == expected_condition, 'incorrect hypothesis: '+name)
    if geom['g'] is None:
        require(b == [0], 'integral polytope has parity')
    elif condition:
        g, v = geom['g'], geom['volume_sum']
        require(len(b)-1 == d-g and b[-1] == v/2**(g+1), 'leading coefficient: '+name)
        require(order == g and residual == 2**(d-g)*factorial(d-g)*v, 'pole formula')
    else:
        require(b == [0], 'known negative control did not collapse')
        require(counts == [comb(n+d, d) for n in range(len(counts))], 'known collapse formula')
    if geom['simple'] and geom['max_full_minor'] <= 2:
        require(condition, 'bimodular bridge failed')
    out = {k: v for k, v in geom.items() if k != 'vertices'}
    out.update(name=name, dimension=d, vertex_count=len(geom['vertices']),
               max_entry=max(abs(x) for row in rows for x in row),
               B=[str(x) for x in b], root_order=order, residual=str(residual))
    out['volume_sum'] = str(out['volume_sum'])
    return out


def weighted_simplex(weights, capacity=1):
    d = len(weights)
    rows = [tuple(-int(i == j) for i in range(d)) for j in range(d)]
    return rows+[tuple(weights)], [0]*d+[capacity]


def fixtures():
    cases = []
    for weights, cap in [((2,), 1), ((1,), 1), ((1, 2), 1), ((1, 2), 2),
                          ((1, 1, 2), 1), ((1, 2, 2), 1), ((1, 1, 2, 2), 1)]:
        a, b = weighted_simplex(weights, cap)
        cases.append(one_case('simplex_'+str(weights)+'_cap'+str(cap), a, b))
    a, b = box(3)
    a += [(1, -1, 0), (1, 1, 0)]; b += [0, 1]
    cases.append(one_case('digon_prism', a, b))
    inv = [(1, -3, 2), (0, 1, -1), (0, 0, 1)]
    shift = (-2, 1, -1)
    changed = [tuple(sum(row[k]*inv[k][j] for k in range(3)) for j in range(3)) for row in a]
    changed_b = [v+dot(row, shift) for row, v in zip(changed, b)]
    cases.append(one_case('dense_sheared_prism', changed, changed_b))
    require(cases[-1]['max_entry'] > 2 and cases[-1]['max_full_minor'] == 2,
            'full-minor-only fixture missing')
    require(cases[-1]['B'] == cases[-2]['B'], 'unimodular invariance')
    a = [(-1, 0), (0, -1), (2, 0), (0, 2)]
    cases.append(one_case('half_square_index_four_globally', a, [0, 0, 1, 1]))
    require(cases[-1]['max_full_minor'] == 4, 'local criterion broader than global')
    a = [(-1,0,0),(0,-1,0),(0,0,-1),(1,1,0),(0,1,1),(1,0,1)]
    cases.append(one_case('locally_simple_graph_triangle', a, [0,0,0,1,1,1]))
    require(not cases[-1]['simple'] and cases[-1]['index_two'], 'local/global distinction')
    a = [(-1,0,0),(1,-1,0),(1,1,0),(1,0,-1),(1,0,1)]
    cases.append(one_case('Stanley_nonsimple_control', a, [0,0,1,0,1], False))
    require(cases[-1]['max_full_minor'] == 2 and not cases[-1]['local_simple'], 'Stanley boundary')
    a = [(0,-1),(-1,2),(1,2)]
    cases.append(one_case('McAllister_Woods_index_four_control', a, [0,0,2], False))
    require(cases[-1]['simple'] and cases[-1]['leading_indices'] == [4], 'index-four boundary')
    return cases


def image_audit():
    matrices, rhs_checks, proper_checks = 0, 0, 0
    for q in range(1, 5):
        c = [[int(i == j) if i < q-1 else (-1 if j < q-1 else 2)
              for j in range(q)] for i in range(q)]
        # Full-support and partial-support characters; dense integral entries.
        for variant in range(1 if q == 1 else 4):
            a = [row[:] for row in c]
            if q > 1:
                amount = variant
                a[0] = [x+amount*y for x, y in zip(a[0], a[-1])]
            for i in range(q):
                a[i].append(sum((j+1)*a[i][j] for j in range(q)))
            require(image_index(a) == 2, 'constructed image index')
            eps = [e for e in product(range(2), repeat=q) if any(e) and
                   all(sum(e[i]*a[i][j] for i in range(q)) % 2 == 0 for j in range(q+1))]
            require(len(eps) == 1, 'not one parity annihilator')
            e = eps[0]
            full = all(e)
            matrices += 1
            residue_image = {tuple(sum(a[i][j]*x[j] for j in range(q+1)) % 2 for i in range(q))
                             for x in product(range(2), repeat=q+1)}
            for b in product((-1, 0, 1), repeat=q):
                # Independent residue-image enumeration supplies the character test.
                expected = tuple(v % 2 for v in b) in residue_image
                require(affine_has_integer_point(a, b) == expected, 'augmented-minor membership')
                require(expected == (sum(x*y for x,y in zip(e,b)) % 2 == 0), 'character membership')
                rhs_checks += 1
            for mask in range((1 << q)-1):
                js = [j for j in range(q) if mask & (1 << j)]
                delta = image_index([a[j] for j in js])
                if full:
                    require(delta == 1, 'full character not surjective on proper subset')
                proper_checks += 1
            if not full:
                support = [i for i, bit in enumerate(e) if bit]
                require(len(support) < q and image_index([a[i] for i in support]) == 2,
                        'missing smaller affine obstruction')
    return {'rectangular_matrices': matrices, 'rhs_checks': rhs_checks,
            'proper_subsystems': proper_checks}


def main():
    cases = fixtures()
    require(not affine_has_integer_point([[2], [4]], [1, 3]),
            'inconsistent dependent equations accepted')
    invalid = 0
    for rows, rhs in [([], []), ([(1,0)], [Q(1,2)]), ([(0,0)], [1]),
                      ([(1,0),(1,)], [1,1]), ([(1.0,0)], [1])]:
        try:
            validate(rows, rhs)
        except ValueError:
            invalid += 1
        else:
            raise ValueError('malformed input accepted')
    result = {'status':'PASS', 'fixtures': cases, 'image_audit':image_audit(),
              'interpolation_holdouts':4*len(cases), 'literal_comparisons':3*len(cases),
              'malformed_inputs_rejected': invalid,
              'scope':'Finite exact corroboration; universal proof imports Berline-Vergne'}
    expected = Path(__file__).with_name('expected.json')
    if expected.exists():
        require(result == json.loads(expected.read_text()), 'expected record mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
