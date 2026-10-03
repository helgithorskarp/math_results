"""Forward attachment producer and exact dense-polynomial verifier; stdlib only."""
from fractions import Fraction as F
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
from pathlib import Path
from hashlib import sha256
import argparse
import json
from poly import add, neg, mul, divide, bezout, bernstein

A = ((0, 5, 11), (0, 6, 11), (0, 5, 7), (5, 9, 11))
B = ((1, 2, 4), (2, 4, 8), (1, 2, 10), (1, 10, 12))
NEW = (20, 21, 22)
R, D = [F(0), F(1)], [F(2), F(-1)]
LO, HI = F(7, 10), F(3, 4)
G = [F(x) for x in (-2, 2, 2, -2, 0, 1)]


def need(ok, why):
    if not ok:
        raise ValueError(why)


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':')) + '\n'


def digest(data):
    return sha256(canonical(data).encode()).hexdigest()


def encode(p):
    return [str(x) for x in p]


def sign(p):
    bs = bernstein(p, LO, HI)
    return 1 if all(x > 0 for x in bs) else -1 if all(x < 0 for x in bs) else 0


def inner(x, y):
    diagonal, all_terms = [], []
    for i in range(3):
        for j in range(3):
            term = mul(x[i], y[j])
            all_terms = add(all_terms, term)
            if i == j:
                diagonal = add(diagonal, term)
    return add(mul(D, diagonal), mul(R, add(all_terms, neg(diagonal))))


def flip(x, y, z):
    return [add(mul(R, add(a, b)), neg(c)) for a, b, c in zip(x, y, z)]


def gap(x, y):
    return add(inner(x, y), neg(R))


def core(which):
    labels = (0, 5, 11) if which == 'A' else (1, 2, 4)
    p = {labels[i]: [[F(1)] if i == j else [] for j in range(3)] for i in range(3)}
    if which == 'A':
        p[6] = flip(p[0], p[11], p[5])
        p[7] = flip(p[0], p[5], p[11])
        p[9] = flip(p[5], p[11], p[0])
    else:
        need(which == 'B', 'core selector')
        p[8] = flip(p[2], p[4], p[1])
        p[10] = flip(p[1], p[2], p[4])
        p[12] = flip(p[1], p[10], p[2])
    return p


def edges(triangles):
    return Counter(tuple(sorted(e)) for t in triangles for e in combinations(t, 2))


def boundary(triangles):
    count = edges(triangles)
    need(all(n in (1, 2) for n in count.values()), 'edge has at most two triangles')
    return sorted(e for e, n in count.items() if n == 1)


def normalize(triangles):
    fresh = sorted({v for t in triangles for v in t} - set(core('B')))
    forms = []
    for perm in permutations(NEW[:len(fresh)]):
        mapping = dict(zip(fresh, perm))
        code = tuple(sorted(tuple(sorted(mapping.get(v, v) for v in t)) for t in triangles))
        forms.append((code, tuple(sorted(mapping.items()))))
    return min(forms)


def reconstruct(triangles):
    points = core('B')
    done = {tuple(sorted(t)) for t in B}
    todo = set(triangles) - done
    while todo:
        possibilities = [t for t in sorted(todo) if len(set(t) & set(points)) == 2]
        need(possibilities, 'a fresh boundary attachment exists')
        t = possibilities[0]
        e = tuple(sorted(set(t) & set(points)))
        parents = [u for u in done if set(e) <= set(u)]
        need(len(parents) == 1, 'single old parent on boundary edge')
        old = next(v for v in parents[0] if v not in e)
        new = next(v for v in t if v not in e)
        points[new] = flip(points[e[0]], points[e[1]], points[old])
        done.add(t)
        todo.remove(t)
    need(len(points) == len(triangles) + 2, 'fresh disk support')
    return points


def enumerate_histories():
    shapes, histories, collisions = set(), Counter(), {}
    raw_collisions = 0

    def walk(ts, ps, depth):
        nonlocal raw_collisions
        if depth == 3:
            key, _ = normalize(ts)
            shapes.add(key)
            histories[key] += 1
            return
        prefix, renamed = normalize(ts)
        mapping = dict(renamed)
        for e in boundary(ts):
            parent = next(t for t in ts if set(e) <= set(t))
            old = next(v for v in parent if v not in e)
            new = flip(ps[e[0]], ps[e[1]], ps[old])
            for k in sorted(ps):
                if k in e:
                    continue
                polynomial = add(inner(new, ps[k]), neg(D))
                need(sign(polynomial) == -1, 'first old-B-corner reuse is impossible')
                raw_collisions += 1
                key = (prefix, tuple(sorted(mapping.get(v, v) for v in e)), mapping.get(k, k))
                value = encode(polynomial)
                need(key not in collisions or collisions[key] == value, 'normalized reuse polynomial agrees')
                collisions[key] = value
            label = NEW[depth]
            walk(ts + [tuple(e) + (label,)], {**ps, label: new}, depth + 1)

    walk(list(B), core('B'), 0)
    need(sum(histories.values()) == 336 and raw_collisions == 2250, 'whole ordered attachment cover')
    need(len(shapes) == 110 and len(collisions) == 1530, 'whole normalized finite cover')
    collision_rows = [[prefix, e, k, value] for (prefix, e, k), value in sorted(collisions.items())]
    return sorted(shapes), histories, collision_rows


def packing(shapes):
    outcomes, valid = [], []
    for index, ts in enumerate(shapes):
        ps = reconstruct(ts)
        es = edges(ts)
        need(len(ps) == 9 and len(es) == 15 and len(boundary(ts)) == 9, 'whole B7 disk')
        need(all(inner(p, p) == D for p in ps.values()), 'all nine unit identities')
        need(all(not gap(ps[u], ps[v]) for u, v in es), 'all fifteen contact identities')
        signs = []
        for u, v in combinations(sorted(ps), 2):
            if (u, v) not in es:
                s = sign(gap(ps[u], ps[v]))
                need(s in (-1, 1), 'every nonedge has a strict sign throughout the closed band')
                signs.append([u, v, s])
        violations = [[u, v] for u, v, s in signs if s == 1]
        if not violations:
            valid.append(index)
            triples = {t for t in combinations(sorted(ps), 3) if all(e in es for e in combinations(t, 2))}
            need(triples == set(ts), 'exactly seven contact triples')
        outcomes.append({'shape': index, 'rejecting_pair': violations[0] if violations else None,
                         'whole_nonedge_sign_digest': digest(signs)})
    need(len(valid) == 56, 'whole packing-compatible shape set')
    return outcomes, valid


def overlap_cases(shapes, valid):
    kept_shapes, rows, all_tests = [], [], []
    ap = core('A')
    for index in valid:
        ts = shapes[index]
        es = edges(ts)
        if es[(10, 12)] != 1:
            continue
        kept_shapes.append(index)
        ps = reconstruct(ts)
        counts = Counter(v for t in ts for v in t)
        for assignment in product((-1, 6, 7, 9), repeat=3):
            used = [x for x in assignment if x != -1]
            if len(used) != len(set(used)):
                continue
            labeling = dict(zip(NEW, assignment))
            reason = None
            for k, a in labeling.items():
                if a == -1:
                    continue
                if counts[k] > 2:
                    reason = 'more than two B triangle sectors'
                    break
                if a in (7, 9) and es[tuple(sorted((k, 12 if a == 7 else 10)))] != 1:
                    reason = 'prescribed cross contact is not a B boundary edge'
                    break
            if reason is None:
                for u, v in combinations(NEW, 2):
                    if labeling[u] == -1 or labeling[v] == -1:
                        continue
                    p = add(gap(ps[u], ps[v]), neg(gap(ap[labeling[u]], ap[labeling[v]])))
                    if p:
                        need(sign(p) != 0, 'whole two-ear metric test is root-free')
                        reason = 'strict ear metric mismatch'
                        break
            all_tests.append([index, list(assignment), reason])
            if reason is None:
                rows.append([index, *assignment])
    need(len(kept_shapes) == 31 and len(all_tests) == 1054 and len(rows) == 137, 'whole overlap cover')
    need(Counter(sum(a != -1 for a in row[1:]) for row in rows) == Counter({0: 31, 1: 106}), 'at most one shared ear')
    return kept_shapes, rows, digest(all_tests)


def b_long_arc(ts):
    adj = defaultdict(list)
    for u, v in boundary(ts):
        if (u, v) != (10, 12):
            adj[u].append(v)
            adj[v].append(u)
    arc, previous = [12], None
    while arc[-1] != 10:
        u = arc[-1]
        candidates = [v for v in sorted(adj[u]) if v != previous]
        need(len(candidates) == 1, 'unique complementary B boundary path')
        previous, v = u, candidates[0]
        need(v not in arc, 'simple B boundary')
        arc.append(v)
    need(len(arc) == 9 and set(arc) == {v for t in ts for v in t}, 'whole nine-point B boundary')
    return arc


def increment_paths():
    def walk(i, j, q, p, path):
        if len(path) == 6:
            if (i, j, q, p) == (4, 8, 3, 2):
                yield path
            return
        for length in (2, 3):
            if (length == 2 and q == 3) or (length == 3 and p == 2):
                continue
            for a in range(length + 1):
                b = length - a
                if i + a <= 4 and j + b <= 8:
                    yield from walk(i + a, j + b, q + (length == 2), p + (length == 3), path + ((i + a, j + b),))
    paths = sorted(walk(0, 0, 0, 0, ((0, 0),)))
    need(len(paths) == 530 and len(set(paths)) == 530, 'all five-cell increment paths')
    return paths


def annulus_cases(shapes, kept):
    a_arc = [7, 0, 6, 11, 9]
    a_counts = {7: 1, 0: 3, 6: 1, 11: 3, 9: 1, 5: 3}
    rows, tests = [], []
    paths = increment_paths()
    for index in kept:
        ts = shapes[index]
        b_arc = b_long_arc(ts)
        counts = {**a_counts, **Counter(v for t in ts for v in t)}
        for path in paths:
            cross = [(a_arc[i], b_arc[j]) for i, j in path]
            k = Counter(v for edge in cross for v in edge)
            degrees = {v: counts[v] + 1 + k[v] for v in counts}
            reason = None
            if any(d < 3 or d > 5 for d in degrees.values()):
                reason = 'complete degree'
            faces = []
            if reason is None:
                for (i, j), (ii, jj) in zip(path, path[1:]):
                    face = a_arc[i:ii+1] + list(reversed(b_arc[j:jj+1]))
                    need(len(face) in (4, 5) and len(face) == len(set(face)), 'simple nontriangle candidate')
                    faces.append(face)
                    internal = [v for v in face if k[v] == 0]
                    if any(counts[v] <= 2 for v in internal):
                        reason = 'nonconvex sole nontriangle sector'
                        break
                    if len(face) == 4:
                        if any(counts[v] == 3 for v in internal):
                            reason = 'quadrilateral after three triangles'
                            break
                        for pos, v in enumerate(face):
                            if k[v] == 0 and counts[v] == 4 and any(degrees[face[h % 4]] == 5 for h in (pos-1, pos+1)):
                                reason = 'four-triangle quad has degree-five neighbor'
                                break
                        if reason:
                            break
            tests.append([index, path, reason])
            if reason is None:
                full_faces = list(A) + list(ts) + [(5, 7, 12, 10, 9)] + faces
                incidence = Counter(tuple(sorted(e)) for face in full_faces for e in zip(face, face[1:] + face[:1]))
                need(len(incidence) == 30 and all(n == 2 for n in incidence.values()), 'all complete thirty edges and both incident faces retained')
                triples = {t for t in combinations(sorted(counts), 3) if all(e in incidence for e in combinations(t, 2))}
                need(triples == {tuple(sorted(t)) for t in list(A) + list(ts)}, 'exactly eleven contact triples')
                rows.append({'shape': index, 'cross': [list(e) for e in cross], 'faces': faces})
    need(len(tests) == 16430 and len(rows) == 80, 'whole disjoint-support annulus cover')
    return rows, digest(tests)


def determinant(m):
    total = []
    for perm in permutations(range(len(m))):
        inversions = sum(perm[i] > perm[j] for i in range(len(m)) for j in range(i+1, len(m)))
        term = [F(-1 if inversions % 2 else 1)]
        for i, j in enumerate(perm):
            term = mul(term, m[i][j])
        total = add(total, term)
    return total


def necessary_equations(row, shapes):
    ps, ap = reconstruct(shapes[row['shape']]), core('A')
    aset = set(ap)
    predictions, equations = [], []
    for face in row['faces']:
        if len(face) != 4 or sum(v in aset for v in face) != 1:
            continue
        pos = next(i for i, v in enumerate(face) if v in aset)
        a = face[pos]
        u, middle, v = (face[(pos + h) % 4] for h in (1, 2, 3))
        denominator = add(D, inner(ps[u], ps[v]))
        need(sign(denominator) == 1, 'positive rational rhombus reflection denominator')
        numerator = [add(mul([F(0), F(2)], add(x, y)), neg(mul(denominator, z)))
                     for x, y, z in zip(ps[u], ps[v], ps[middle])]
        need(inner(numerator, numerator) == mul(D, mul(denominator, denominator)), 'reflected unit identity')
        predictions.append((a, numerator, denominator))
        for b in sorted(ps):
            if [a, b] in row['cross']:
                equations.append(add(inner(numerator, ps[b]), neg(mul(R, denominator))))
    for (a, n, l), (aa, nn, ll) in combinations(predictions, 2):
        target = D if a == aa else inner(ap[a], ap[aa])
        equations.append(add(inner(n, nn), neg(mul(target, mul(l, ll)))))
    for (a, n, l), (aa, nn, ll) in combinations(predictions, 2):
        if a == aa:
            continue
        for ax, bj in row['cross']:
            if ax in (a, aa):
                continue
            v = ps[bj]
            x, y = mul(inner(ap[a], ap[ax]), l), mul(inner(ap[aa], ap[ax]), ll)
            m = [[mul(D, mul(l, l)), inner(n, nn), x, inner(n, v)],
                 [inner(n, nn), mul(D, mul(ll, ll)), y, inner(nn, v)],
                 [x, y, D, R], [inner(n, v), inner(nn, v), R, D]]
            equations.append(determinant(m))
    return equations


def algebra_cases(rows, shapes):
    outcomes, full, strict, receipts = [], [], [], []
    for index, row in enumerate(rows):
        equations = necessary_equations(row, shapes)
        nz = [(i, p) for i, p in enumerate(equations) if p]
        status, witness = 'retained', None
        for i, p in nz:
            if sign(p):
                status, witness = 'excluded-equation', [i, encode(p)]
                break
        if status == 'retained' and len(nz) >= 2:
            h = nz[0][1]
            for _, p in nz[1:]:
                h = bezout(h, p)[0]
            if sign(h):
                status, witness = 'excluded-gcd', encode(h)
        if status == 'retained':
            for i, p in nz:
                q, rem = divide(p, G)
                if not rem and sign(q):
                    status, witness = 'critical-only', [i, encode(q)]
                    break
        if status in ('retained', 'critical-only'):
            full.append(index)
        if status == 'retained':
            strict.append(index)
        receipts.append([index, [encode(p) for p in equations]])
        outcomes.append({'map': index, 'status': status, 'witness': witness})
    need(Counter(o['status'] for o in outcomes) == Counter({'excluded-equation': 23, 'excluded-gcd': 4, 'critical-only': 1, 'retained': 52}), 'whole exact algebra screen')
    need(len(full) == 53 and len(strict) == 52, 'closed and strict-improvement map lists')
    return outcomes, full, strict, digest(receipts)


def build():
    need(sign([F(i) * G[i] for i in range(1, len(G))]) == 1, 'critical polynomial strictly increases')
    need(sum(x * LO**i for i, x in enumerate(G)) < 0 < sum(x * HI**i for i, x in enumerate(G)), 'unique critical root in closed band')
    shapes, histories, collisions = enumerate_histories()
    packing_rows, valid = packing(shapes)
    kept, overlaps, overlap_digest = overlap_cases(shapes, valid)
    maps, annulus_digest = annulus_cases(shapes, kept)
    algebra, full, strict, algebra_digest = algebra_cases(maps, shapes)
    record = {'format': 'b7-contact-incidence-v1', 'actual_author': 'six-tammes-1', 'role': 'researcher',
              'cosine_closed_band': ['7/13', '3/5'], 'r_closed_band': [str(LO), str(HI)],
              'physical_interface': 'ALL9813 Corollary C; fullG20; A4/B7 actual complete TT components; ALL extra contacts retained',
              'A': A, 'B': B, 'new_B_labels': NEW, 'critical_r_polynomial': encode(G),
              'all_shapes': shapes, 'history_multiplicities': [histories[t] for t in shapes],
              'freshness': {'ordered_collision_tests': 2250, 'normalized_collision_tests': 1530,
                            'whole_normalized_polynomial_digest': digest(collisions)},
              'packing': packing_rows, 'packing_compatible_shapes': valid, 'actual_P_shapes': kept,
              'overlap_rows': overlaps, 'whole_overlap_filter_digest': overlap_digest,
              'raw_increment_paths': 530, 'raw_annulus_rows': 16430,
              'whole_annulus_filter_digest': annulus_digest, 'geometric_maps': maps,
              'algebra': algebra, 'whole_necessary_equations_digest': algebra_digest,
              'full_band_maps': full, 'strict_improvement_maps': strict}
    return json.loads(canonical(record))


def verify(record, expected=None):
    # Controls may supply the once-regenerated reference. Normal verification
    # always builds it here. Canonical JSON also rejects bool/float for integers.
    if expected is None:
        expected = build()
    need(canonical(record) == canonical(expected), 'entire regenerated mathematical certificate must agree')


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
            'certificate_SHA256': digest(record)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', type=Path)
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('CERTIFICATE.json'))
    args = parser.parse_args()
    record = build()
    if args.emit:
        args.emit.write_text(canonical(record))
    else:
        verify(json.loads(args.certificate.read_text()), record)
    print(canonical(summary(record)), end='')


if __name__ == '__main__':
    main()
