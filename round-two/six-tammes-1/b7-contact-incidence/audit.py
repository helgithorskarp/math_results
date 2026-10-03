"""One-author separate audit: polygon triangulations, sparse polynomials, Bareiss.

No producer, dense kernel, imported certificate or numerical data is a proof input.
The included certificate is compared only after the full reconstruction finishes.
"""
from fractions import Fraction
from itertools import combinations, permutations, product
from collections import Counter, defaultdict
from pathlib import Path
from hashlib import sha256
from math import comb
import argparse
import json

F = Fraction
A = ((0, 5, 11), (0, 6, 11), (0, 5, 7), (5, 9, 11))
B = ((1, 2, 4), (2, 4, 8), (1, 2, 10), (1, 10, 12))
NEW = (20, 21, 22)
B_CYCLE = (1, 4, 8, 2, 10, 12)
LO, HI = F(7, 10), F(3, 4)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def P(*coefficients):
    return {i: F(x) for i, x in enumerate(coefficients) if x}


def plus(*polynomials):
    out = defaultdict(F)
    for p in polynomials:
        for i, x in p.items():
            out[i] += x
    return {i: x for i, x in out.items() if x}


def scale(p, c):
    return {i: c*x for i, x in p.items() if c*x}


def times(p, q):
    out = defaultdict(F)
    for i, x in p.items():
        for j, y in q.items():
            out[i+j] += x*y
    return {i: x for i, x in out.items() if x}


def quotient(p, q):
    require(q, 'nonzero divisor')
    rem, answer = dict(p), {}
    degree = max(q)
    while rem and max(rem) >= degree:
        i = max(rem) - degree
        c = rem[max(rem)] / q[degree]
        answer[i] = answer.get(i, F(0)) + c
        rem = plus(rem, {j+i: -c*x for j, x in q.items()})
    answer = {i: x for i, x in answer.items() if x}
    require(plus(times(answer, q), rem) == p, 'entire division identity')
    return answer, rem


def common_divisor(p, q):
    # Every Euclidean step is verified as a polynomial identity. A common zero
    # persists to the final nonzero remainder; normalize its leading term.
    require(p or q, 'nontrivial common-divisor inputs')
    while q:
        _, rem = quotient(p, q)
        p, q = q, rem
    return scale(p, 1/p[max(p)])


def serial_poly(p):
    return [str(p.get(i, F(0))) for i in range(max(p, default=-1)+1)]


def serialize(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':')) + '\n'


def fingerprint(data):
    return sha256(serialize(data).encode()).hexdigest()


def bernstein_sign(p):
    # Horner affine substitution, then the identity x^j=sum_{i>=j}
    # C(i,j)/C(n,j) B_i^n(x). This differs from the dense power expansion.
    if not p:
        return 0
    degree = max(p)
    transformed = {}
    for i in range(degree, -1, -1):
        transformed = plus(times(transformed, P(LO, HI-LO)), P(p.get(i, 0)))
    bs = [sum(transformed.get(j, 0)*F(comb(i, j), comb(degree, j)) for j in range(i+1))
          for i in range(degree+1)]
    return 1 if all(x > 0 for x in bs) else -1 if all(x < 0 for x in bs) else 0


R, D, G = P(0, 1), P(2, -1), P(-2, 2, 2, -2, 0, 1)


def gram(v, w):
    diagonal = plus(*(times(x, y) for x, y in zip(v, w)))
    sv, sw = plus(*v), plus(*w)
    return plus(times(P(2, -2), diagonal), times(R, times(sv, sw)))


def reflect(x, y, z):
    return tuple(plus(times(R, plus(a, b)), scale(c, -1)) for a, b, c in zip(x, y, z))


def a_points():
    return {0: (P(1), P(), P()), 5: (P(), P(1), P()), 11: (P(), P(), P(1)),
            6: (R, P(-1), R), 7: (R, R, P(-1)), 9: (P(-1), R, R)}


def triangle_edges(ts):
    return Counter(tuple(sorted((t[i], t[j]))) for t in ts for i, j in ((0, 1), (0, 2), (1, 2)))


def outside_edges(ts):
    counts = triangle_edges(ts)
    require(set(counts.values()) <= {1, 2}, 'no three-face edge')
    return sorted(e for e, n in counts.items() if n == 1)


def canon(ts):
    names = sorted({v for t in ts for v in t} - set(B_CYCLE))
    variants = []
    for image in permutations(NEW[:len(names)]):
        rename = dict(zip(names, image))
        variants.append(tuple(sorted(tuple(sorted(rename.get(v, v) for v in t)) for t in ts)))
    return min(variants)


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for n in range(total+1):
        for rest in compositions(total-n, parts-1):
            yield (n,) + rest


def triangulations(polygon):
    if len(polygon) <= 2:
        yield ()
        return
    for middle in range(1, len(polygon)-1):
        t = tuple(sorted((polygon[0], polygon[middle], polygon[-1])))
        for left in triangulations(polygon[:middle+1]):
            for right in triangulations(polygon[middle:]):
                yield (t,) + left + right


def disk_shapes(number):
    # Each root boundary edge and its inserted corners bound an independent
    # polygon. All Catalan triangulations of those six polygons are retained.
    answers = set()
    for sizes in compositions(number, 6):
        cursor, polygons = 0, []
        for i, n in enumerate(sizes):
            polygon = (B_CYCLE[i],) + NEW[cursor:cursor+n] + (B_CYCLE[(i+1) % 6],)
            cursor += n
            polygons.append(tuple(triangulations(polygon)))
        for choices in product(*polygons):
            answers.add(canon(tuple(tuple(sorted(t)) for t in B) + sum(choices, ())))
    return sorted(answers)


def points(ts):
    # Start from the single basis triangle and propagate the entire face tree.
    root = (1, 2, 4)
    p = {1: (P(1), P(), P()), 2: (P(), P(1), P()), 4: (P(), P(), P(1))}
    done, remaining = {root}, set(ts) - {root}
    while remaining:
        advanced = False
        for t in sorted(remaining):
            parents = [u for u in done if len(set(t) & set(u)) == 2]
            if not parents:
                continue
            require(len(parents) == 1, 'entire selected face adjacency is a tree')
            parent = parents[0]
            e = sorted(set(t) & set(parent))
            old = next(v for v in parent if v not in e)
            new = next(v for v in t if v not in e)
            require(new not in p, 'fresh face-tree corner')
            p[new] = reflect(p[e[0]], p[e[1]], p[old])
            remaining.remove(t)
            done.add(t)
            advanced = True
            break
        require(advanced, 'full propagation completes')
    require(all(gram(v, v) == D for v in p.values()), 'all unit identities')
    return p


def freshness(prefixes):
    rows = []
    for shapes in prefixes:
        for ts in shapes:
            ps = points(ts)
            for e in outside_edges(ts):
                parent = next(t for t in ts if set(e) <= set(t))
                old = next(v for v in parent if v not in e)
                w = reflect(ps[e[0]], ps[e[1]], ps[old])
                for k in sorted(ps):
                    if k in e:
                        continue
                    p = plus(gram(w, ps[k]), scale(D, -1))
                    require(bernstein_sign(p) == -1, 'all first-reuse probes are strictly different')
                    rows.append([ts, e, k, serial_poly(p)])
    rows.sort(key=lambda row: (row[0], row[1], row[2]))
    require(len(rows) == 1530, 'all independently enumerated first-reuse probes')
    return rows


def multiplicity(ts):
    original = {tuple(sorted(t)) for t in B}
    new = set(ts) - original
    count = 0
    for order in permutations(sorted(new)):
        done = set(original)
        available = set(B_CYCLE)
        good = True
        for t in order:
            e = tuple(sorted(set(t) & available))
            if len(e) != 2 or e not in outside_edges(done):
                good = False
                break
            available.update(t)
            done.add(t)
        if good:
            count += 1
    return count


def packing(shapes):
    outcomes, valid = [], []
    for index, ts in enumerate(shapes):
        ps, es = points(ts), triangle_edges(ts)
        require(len(ps) == 9 and len(es) == 15 and len(outside_edges(ts)) == 9, 'B7 whole disk incidence')
        require(all(gram(ps[u], ps[v]) == R for u, v in es), 'all contact identities')
        signs = []
        for u, v in combinations(sorted(ps), 2):
            if (u, v) in es:
                continue
            s = bernstein_sign(plus(gram(ps[u], ps[v]), scale(R, -1)))
            require(s in (-1, 1), 'every full nonedge polynomial has a strict closed-band sign')
            signs.append([u, v, s])
        positive = [[u, v] for u, v, s in signs if s == 1]
        if not positive:
            valid.append(index)
            actual = {t for t in combinations(sorted(ps), 3) if all(e in es for e in combinations(t, 2))}
            require(actual == set(ts), 'all contact triples retained')
        outcomes.append({'shape': index, 'rejecting_pair': positive[0] if positive else None,
                         'whole_nonedge_sign_digest': fingerprint(signs)})
    require(len(valid) == 56, 'all fifty-six packing patterns')
    return outcomes, valid


def overlaps(shapes, valid):
    kept, rows, tested = [], [], []
    ap = a_points()
    for index in valid:
        ts, es = shapes[index], triangle_edges(shapes[index])
        if es[(10, 12)] != 1:
            continue
        kept.append(index)
        bp = points(ts)
        sectors = Counter(v for t in ts for v in t)
        for assignment in product((-1, 6, 7, 9), repeat=3):
            actual = [a for a in assignment if a != -1]
            if len(actual) != len(set(actual)):
                continue
            names = dict(zip(NEW, assignment))
            reason = None
            for v, a in names.items():
                if a == -1:
                    continue
                if sectors[v] > 2:
                    reason = 'more than two B triangle sectors'
                    break
                if a in (7, 9) and es[tuple(sorted((v, 12 if a == 7 else 10)))] != 1:
                    reason = 'prescribed cross contact is not a B boundary edge'
                    break
            if reason is None:
                for u, v in combinations(NEW, 2):
                    if names[u] == -1 or names[v] == -1:
                        continue
                    polynomial = plus(gram(bp[u], bp[v]), scale(gram(ap[names[u]], ap[names[v]]), -1))
                    if polynomial:
                        require(bernstein_sign(polynomial) != 0, 'every two-ear mismatch is strictly root-free')
                        reason = 'strict ear metric mismatch'
                        break
            tested.append([index, list(assignment), reason])
            if reason is None:
                rows.append([index, *assignment])
    require(len(kept) == 31 and len(tested) == 1054 and len(rows) == 137, 'entire overlap cover')
    require(Counter(sum(a != -1 for a in row[1:]) for row in rows) == {0: 31, 1: 106}, 'all larger overlaps excluded')
    return kept, rows, fingerprint(tested)


def grid_paths():
    grid = [(i, j) for i in range(5) for j in range(9) if (i, j) not in ((0, 0), (4, 8))]
    answers = []
    # Exhaust all four-element subsets of the 43 internal grid positions.
    for middle in combinations(grid, 4):
        path = ((0, 0),) + middle + ((4, 8),)
        steps = [(b[0]-a[0], b[1]-a[1]) for a, b in zip(path, path[1:])]
        if any(a < 0 or b < 0 for a, b in steps):
            continue
        if Counter(a+b for a, b in steps) == {2: 3, 3: 2}:
            answers.append(path)
    require(len(answers) == 530 and answers == sorted(answers), 'entire monotone grid-chain cover')
    return answers


def long_arc(ts):
    neighbors = defaultdict(set)
    for u, v in outside_edges(ts):
        if {u, v} != {10, 12}:
            neighbors[u].add(v)
            neighbors[v].add(u)
    arc = [12]
    while arc[-1] != 10:
        remaining = neighbors[arc[-1]] - set(arc)
        require(len(remaining) == 1, 'simple long boundary arc')
        arc.append(next(iter(remaining)))
    require(len(arc) == 9 and len(set(arc)) == 9, 'whole B boundary arc')
    return arc


def annuli(shapes, kept):
    a = [7, 0, 6, 11, 9]
    aa = {7: 1, 0: 3, 6: 1, 11: 3, 9: 1, 5: 3}
    paths, tested, rows = grid_paths(), [], []
    for index in kept:
        ts, b = shapes[index], long_arc(shapes[index])
        triangle_counts = {**aa, **Counter(v for t in ts for v in t)}
        for path in paths:
            cross = [(a[i], b[j]) for i, j in path]
            cross_counts = Counter(v for u in cross for v in u)
            degree = {v: n+1+cross_counts[v] for v, n in triangle_counts.items()}
            reason = None
            if min(degree.values()) < 3 or max(degree.values()) > 5:
                reason = 'complete degree'
            faces = []
            if reason is None:
                for start, stop in zip(path, path[1:]):
                    i, j = start
                    ii, jj = stop
                    face = a[i:ii+1] + b[j:jj+1][::-1]
                    require(len(face) in (4, 5) and len(set(face)) == len(face), 'simple disk candidate')
                    faces.append(face)
                    uncut = [v for v in face if not cross_counts[v]]
                    if any(triangle_counts[v] <= 2 for v in uncut):
                        reason = 'nonconvex sole nontriangle sector'
                        break
                    if len(face) == 4:
                        if any(triangle_counts[v] == 3 for v in uncut):
                            reason = 'quadrilateral after three triangles'
                            break
                        for i, v in enumerate(face):
                            if v in uncut and triangle_counts[v] == 4 and max(degree[face[(i-1) % 4]], degree[face[(i+1) % 4]]) == 5:
                                reason = 'four-triangle quad has degree-five neighbor'
                                break
                        if reason:
                            break
            tested.append([index, path, reason])
            if reason is None:
                counter = Counter()
                for face in list(A) + list(ts) + [(5, 7, 12, 10, 9)] + faces:
                    for i in range(len(face)):
                        counter[tuple(sorted((face[i], face[(i+1) % len(face)])))] += 1
                require(len(counter) == 30 and set(counter.values()) == {2}, 'all contacts with both complete incident faces')
                actual = {t for t in combinations(sorted(degree), 3) if all(e in counter for e in combinations(t, 2))}
                require(actual == {tuple(sorted(t)) for t in list(A)+list(ts)}, 'all eleven and only eleven triples')
                rows.append({'shape': index, 'cross': [list(e) for e in cross], 'faces': faces})
    require(len(tested) == 16430 and len(rows) == 80, 'entire annulus reduction')
    return rows, fingerprint(tested)


def bareiss(matrix):
    m = [[dict(x) for x in row] for row in matrix]
    previous, orientation = P(1), 1
    for k in range(len(m)-1):
        if not m[k][k]:
            candidate = next((i for i in range(k+1, len(m)) if m[i][k]), None)
            if candidate is None:
                return {}
            m[k], m[candidate] = m[candidate], m[k]
            orientation *= -1
        pivot = m[k][k]
        for i in range(k+1, len(m)):
            for j in range(k+1, len(m)):
                numerator = plus(times(pivot, m[i][j]), scale(times(m[i][k], m[k][j]), -1))
                m[i][j], remainder = quotient(numerator, previous)
                require(not remainder, 'every Bareiss division is exact')
            m[i][k] = {}
        previous = pivot
    return scale(m[-1][-1], orientation)


def equations(row, shapes):
    bp, ap = points(shapes[row['shape']]), a_points()
    fixed, conditions = [], []
    for face in row['faces']:
        corners = [i for i, v in enumerate(face) if v in ap]
        if len(face) != 4 or len(corners) != 1:
            continue
        i = corners[0]
        name = face[i]
        v, z, w = (bp[face[(i+j) % 4]] for j in (1, 2, 3))
        denominator = plus(D, gram(v, w))
        require(bernstein_sign(denominator) == 1, 'positive opposite-corner reflection denominator')
        numerator = tuple(plus(times(P(0, 2), plus(x, y)), scale(times(denominator, zz), -1))
                          for x, y, zz in zip(v, w, z))
        require(gram(numerator, numerator) == times(D, times(denominator, denominator)), 'unit reflection exact')
        fixed.append((name, numerator, denominator))
        for b in sorted(bp):
            if [name, b] in row['cross']:
                conditions.append(plus(gram(numerator, bp[b]), scale(times(R, denominator), -1)))
    for (a, n, l), (b, nn, ll) in combinations(fixed, 2):
        target = D if a == b else gram(ap[a], ap[b])
        conditions.append(plus(gram(n, nn), scale(times(target, times(l, ll)), -1)))
    for (a, n, l), (b, nn, ll) in combinations(fixed, 2):
        if a == b:
            continue
        for unknown, anchor in row['cross']:
            if unknown in (a, b):
                continue
            v = bp[anchor]
            x, y = times(gram(ap[a], ap[unknown]), l), times(gram(ap[b], ap[unknown]), ll)
            matrix = [[times(D, times(l, l)), gram(n, nn), x, gram(n, v)],
                      [gram(n, nn), times(D, times(ll, ll)), y, gram(nn, v)],
                      [x, y, D, R], [gram(n, v), gram(nn, v), R, D]]
            conditions.append(bareiss(matrix))
    return conditions


def algebra(rows, shapes):
    outcomes, full, strict, receipts = [], [], [], []
    for i, row in enumerate(rows):
        eqs = equations(row, shapes)
        nonzero = [(j, p) for j, p in enumerate(eqs) if p]
        status, witness = 'retained', None
        for j, p in nonzero:
            if bernstein_sign(p):
                status, witness = 'excluded-equation', [j, serial_poly(p)]
                break
        if status == 'retained' and len(nonzero) >= 2:
            h = nonzero[0][1]
            for _, p in nonzero[1:]:
                h = common_divisor(h, p)
            if bernstein_sign(h):
                status, witness = 'excluded-gcd', serial_poly(h)
        if status == 'retained':
            for j, p in nonzero:
                q, remainder = quotient(p, G)
                if not remainder and bernstein_sign(q):
                    status, witness = 'critical-only', [j, serial_poly(q)]
                    break
        if status in ('retained', 'critical-only'):
            full.append(i)
        if status == 'retained':
            strict.append(i)
        outcomes.append({'map': i, 'status': status, 'witness': witness})
        receipts.append([i, [serial_poly(p) for p in eqs]])
    require(Counter(row['status'] for row in outcomes) == {'excluded-equation': 23, 'excluded-gcd': 4, 'critical-only': 1, 'retained': 52}, 'all algebra outcomes')
    return outcomes, full, strict, fingerprint(receipts)


def build():
    derivative = {i-1: F(i)*x for i, x in G.items() if i}
    require(bernstein_sign(derivative) == 1, 'critical polynomial strictly monotone')
    require(sum(x*LO**i for i, x in G.items()) < 0 < sum(x*HI**i for i, x in G.items()), 'exact unique critical root')
    prefixes = [disk_shapes(n) for n in range(3)]
    require(list(map(len, prefixes)) == [1, 6, 27], 'all smaller disk triangulations')
    shapes = disk_shapes(3)
    require(len(shapes) == 110, 'all final disk triangulations')
    multiplicities = [multiplicity(ts) for ts in shapes]
    require(sum(multiplicities) == 336, 'whole independent history-order cover')
    collisions = freshness(prefixes)
    packing_rows, valid = packing(shapes)
    kept, overlap_rows, overlap_digest = overlaps(shapes, valid)
    maps, annulus_digest = annuli(shapes, kept)
    algebra_rows, full, strict, algebra_digest = algebra(maps, shapes)
    record = {'format': 'b7-contact-incidence-v1', 'actual_author': 'six-tammes-1', 'role': 'researcher',
              'cosine_closed_band': ['7/13', '3/5'], 'r_closed_band': [str(LO), str(HI)],
              'physical_interface': 'ALL9813 Corollary C; fullG20; A4/B7 actual complete TT components; ALL extra contacts retained',
              'A': A, 'B': B, 'new_B_labels': NEW, 'critical_r_polynomial': serial_poly(G),
              'all_shapes': shapes, 'history_multiplicities': multiplicities,
              'freshness': {'ordered_collision_tests': 2250, 'normalized_collision_tests': 1530,
                            'whole_normalized_polynomial_digest': fingerprint(collisions)},
              'packing': packing_rows, 'packing_compatible_shapes': valid, 'actual_P_shapes': kept,
              'overlap_rows': overlap_rows, 'whole_overlap_filter_digest': overlap_digest,
              'raw_increment_paths': 530, 'raw_annulus_rows': 16430,
              'whole_annulus_filter_digest': annulus_digest, 'geometric_maps': maps,
              'algebra': algebra_rows, 'whole_necessary_equations_digest': algebra_digest,
              'full_band_maps': full, 'strict_improvement_maps': strict}
    return json.loads(serialize(record))


def verify(record, expected=None):
    if expected is None:
        expected = build()
    require(serialize(record) == serialize(expected), 'entire independently regenerated certificate')


def summary(record):
    return {'status': 'complete', 'ordered_attachment_histories': sum(record['history_multiplicities']),
            'B7_shapes_before_packing': len(record['all_shapes']),
            'normalized_first_reuse_tests': record['freshness']['normalized_collision_tests'],
            'packing_compatible_B7_shapes': len(record['packing_compatible_shapes']),
            'actual_P_B7_shapes': len(record['actual_P_shapes']),
            'one_overlap_assignments': sum(sum(v != -1 for v in row[1:]) == 1 for row in record['overlap_rows']),
            'geometric_disjoint_maps': len(record['geometric_maps']),
            'full_band_disjoint_maps': len(record['full_band_maps']),
            'strict_improvement_disjoint_maps': len(record['strict_improvement_maps']),
            'certificate_SHA256': fingerprint(record)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', type=Path)
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('CERTIFICATE.json'))
    args = parser.parse_args()
    record = build()
    if args.emit:
        args.emit.write_text(serialize(record))
    else:
        verify(json.loads(args.certificate.read_text()), record)
    print(serialize(summary(record)), end='')


if __name__ == '__main__':
    main()
