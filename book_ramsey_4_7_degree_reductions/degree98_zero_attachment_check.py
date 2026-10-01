"""Exact conditional exclusion of the remaining (3,18,1) zero-attachment case.
Actual author six-books-1, researcher. Python 3.11+, standard library only.
Full generated matrices are optional private output; no external catalogue.
"""
from itertools import combinations, combinations_with_replacement
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json

def need(ok, msg):
    if not ok:
        raise RuntimeError(msg)

def six_graphs(degree):
    rows = [0] * 6
    remaining = list(degree)

    def visit(i):
        if i == 6:
            need(not any(remaining), 'unfinished six graph')
            yield tuple(rows)
            return
        allowed = [j for j in range(i + 1, 6) if remaining[j]]
        d = remaining[i]
        if d < 0 or d > len(allowed):
            return
        for chosen in combinations(allowed, d):
            remaining[i] = 0
            for j in chosen:
                remaining[j] -= 1
                rows[i] |= 1 << j
                rows[j] |= 1 << i
            if all(0 <= remaining[j] <= sum(remaining[k] > 0 for k in range(i + 1, 6) if k != j)
                   for j in range(i + 1, 6)):
                yield from visit(i + 1)
            for j in chosen:
                remaining[j] += 1
                rows[i] ^= 1 << j
                rows[j] ^= 1 << i
            remaining[i] = d

    yield from visit(0)

def full_graph(mask, cols, tail):
    j = [[0] * 10 for _ in range(10)]

    def edge(a, b):
        j[a][b] = j[b][a] = 1

    for a in range(1, 4):
        edge(0, a)
    for k, (a, b) in enumerate(combinations(range(1, 4), 2)):
        if mask >> k & 1:
            edge(a, b)
    for k, c in enumerate(cols):
        for a in range(3):
            if c >> a & 1:
                edge(a + 1, k + 4)
    for a, b in combinations(range(6), 2):
        if tail[a] >> b & 1:
            edge(a + 4, b + 4)
    need(all(sum(r) == 3 for r in j), 'full cubic')
    return j

def gram(j):
    return [[5 * (a == b) + 3 - j[a][b] - sum(j[a][k] * j[k][b] for k in range(10))
             for b in range(10)] for a in range(10)]

def isomorphism(a, b):
    # Exhaustive individual bijections with literal edge compatibility.
    signatures = lambda g: [tuple(sorted(sum(g[i][k] * g[k][j] for k in range(10))
                                      for j in range(10) if i != j)) for i in range(10)]
    sa, sb = signatures(a), signatures(b)
    mapping = [-1] * 10
    used = set()

    def visit():
        if len(used) == 10:
            return tuple(mapping)
        i = max((i for i in range(10) if mapping[i] < 0),
                key=lambda i: (sum(a[i][j] for j in range(10) if mapping[j] >= 0), -i))
        for t in range(10):
            if t in used or sa[i] != sb[t]:
                continue
            if any(a[i][j] != b[t][mapping[j]] for j in range(10) if mapping[j] >= 0):
                continue
            mapping[i] = t
            used.add(t)
            result = visit()
            if result is not None:
                return result
            used.remove(t)
            mapping[i] = -1
        return None

    return visit()

def inverse(a):
    n = len(a)
    aug = [[Q(x) for x in row] + [Q(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        p = next((i for i in range(j, n) if aug[i][j]), None)
        need(p is not None, 'singular template Gram')
        aug[j], aug[p] = aug[p], aug[j]
        value = aug[j][j]
        aug[j] = [x / value for x in aug[j]]
        for i in range(n):
            if i != j:
                value = aug[i][j]
                aug[i] = [x - value * y for x, y in zip(aug[i], aug[j])]
    inv = [row[n:] for row in aug]
    need(all(sum(a[i][k] * inv[k][j] for k in range(n)) == (i == j)
             for i in range(n) for j in range(n)), 'literal inverse identity')
    return inv

def cliques(adjacency, size):
    def visit(chosen, allowed):
        if len(chosen) == size:
            yield tuple(chosen)
            return
        if len(chosen) + len(allowed) < size:
            return
        for pos, v in enumerate(allowed):
            yield from visit(chosen + [v], [w for w in allowed[pos + 1:] if w in adjacency[v]])
    yield from visit([], list(range(len(adjacency))))

def core(step):
    j = [set() for _ in range(10)]
    for i in range(5):
        for a, b in ((i, (i + 1) % 5), (i + 5, (i + step) % 5 + 5), (i, i + 5)):
            j[a].add(b)
            j[b].add(a)
    return j

def outside(g):
    w = [set() for _ in range(11)]
    for i in range(11):
        for step in (1, 2):
            k = (i + step) % 11
            w[i].add(k)
            w[k].add(i)

    def add(a, b):
        need(a != b and b not in w[a], 'new outside edge')
        w[a].add(b)
        w[b].add(a)

    def remove(a, b):
        w[a].remove(b)
        w[b].remove(a)

    ends = [i for i in range(11) if g[i]]
    if len(ends) == 1:
        v = ends[0]
        u, x = next((u, x) for u, x in combinations(range(3, 11), 2)
                    if x in w[u] and u != v and x != v and u not in w[v] and x not in w[v])
        remove(u, x)
        add(v, u)
        add(v, x)
    elif len(ends) == 2:
        a, b = ends
        if b not in w[a]:
            add(a, b)
        else:
            # Avoid removing any edge of the prescribed A triangle.
            u, x = next((u, x) for u, x in combinations(range(3, 11), 2)
                        if x in w[u] and u not in (a, b) and x not in (a, b)
                        and u not in w[a] and x not in w[b])
            remove(u, x)
            add(a, u)
            add(b, x)
    need([len(r) for r in w] == [4 + v for v in g], 'outside degree sequence')
    need(all(b in w[a] for a, b in combinations(range(3), 2)), 'A triangle')
    return w

def incidence(row_degrees, col_degrees):
    m = [[0] * 10 for _ in range(11)]
    remaining = list(col_degrees)
    for v in sorted(range(11), key=lambda v: (-row_degrees[v], v)):
        selected = sorted(range(10), key=lambda x: (-remaining[x], x))[:row_degrees[v]]
        need(all(remaining[x] > 0 for x in selected), 'bipartite degrees')
        for x in selected:
            m[v][x] = 1
            remaining[x] -= 1
    need(not any(remaining), 'bipartite completion')
    return m

def switched(m):
    out = [row[:] for row in m]
    for a, b in combinations(range(11), 2):
        found = next(((x, y) for x in range(10) for y in range(10)
                      if out[a][x] == out[b][y] == 1 and out[a][y] == out[b][x] == 0), None)
        if found:
            x, y = found
            for v, q in ((a, x), (a, y), (b, x), (b, y)):
                out[v][q] ^= 1
            break
    need(out != m, 'different literal incidence')
    return out

def audit(j, w, m, t, g):
    # Independent set-neighborhood representation, labels z=0,N=1..10,V=11..21.
    r = [set() for _ in range(22)]

    def add(a, b):
        r[a].add(b)
        r[b].add(a)

    for x in range(10):
        add(0, x + 1)
    for a, b in combinations(range(10), 2):
        if b in j[a]:
            add(a + 1, b + 1)
    for a, b in combinations(range(11), 2):
        if b in w[a]:
            add(a + 11, b + 11)
    for v in range(11):
        for x in range(10):
            if m[v][x]:
                add(v + 11, x + 1)
    degrees = [len(row) for row in r]
    need(degrees == [10] + [9] * 10 + [8] * 3 + [9] * 8, 'literal 98 histogram')
    b = [set(range(22)) - {i} - r[i] for i in range(22)]
    f = [[0] * 22 for _ in range(22)]
    red_f, blue_f = [], []
    for i in range(22):
        for q in range(22):
            if q != i:
                f[i][q] = ((3 - len(r[i] & r[q])) if q in r[i]
                           else (6 - len(b[i] & b[q])))
        fr = sum(f[i][q] for q in r[i])
        fb = sum(f[i][q] for q in b[i])
        tr = sum(y in r[x] for x, y in combinations(r[i], 2))
        tb = sum(y in b[x] for x, y in combinations(b[i], 2))
        need(fr == 3 * degrees[i] - 2 * tr, 'red parity literal')
        need(fb == 6 * (21 - degrees[i]) - 2 * tb, 'blue parity literal')
        red_f.append(fr)
        blue_f.append(fb)
        sa = len(r[i] & {11, 12, 13})
        eps = int(0 in r[i])
        need(sum(f[i]) == 2 - (degrees[i] - 10) ** 2 + 2 * (sa - eps), 'incident literal')
    need([f[0][x + 1] for x in range(10)] == t, 'z red defects')
    need([f[0][v + 11] for v in range(11)] == g, 'z blue defects')
    need([sum(f[v]) for v in (0, 11, 12, 13)] == [2] * 4, 'even-root row two')
    e = [[f[x + 1][y + 1] for y in range(10)] for x in range(10)]
    s_a = [sum(m[a][x] for a in range(3)) for x in range(10)]
    for x in range(10):
        for y in range(10):
            j2 = len(j[x] & j[y])
            s0 = 5 * (x == y) + 3 - (y in j[x]) - j2
            actual = sum(m[v][x] * m[v][y] for v in range(11))
            need(actual == s0 - e[x][y], 'full Gram entry')
        right = s_a[x] - 2 - t[x] + sum(t[y] for y in j[x]) + sum(m[v][x] * g[v] for v in range(11))
        need(sum(e[x]) == right, 'NEW z row bridge')
    for v in range(11):
        a = int(v < 3)
        sa = len(w[v] & {0, 1, 2})
        mt = sum(m[v][x] * t[x] for x in range(10))
        wg = sum(g[u] for u in w[v])
        cross = sa - 2 * a - (1 + a) * g[v] + mt + wg
        within = 1 + sa - a + a * g[v] - mt - wg
        need(sum(f[v + 11][x + 1] for x in range(10)) == cross, 'generalized exterior cross')
        need(sum(f[v + 11][u + 11] for u in range(11)) == within, 'generalized exterior inside')
    need(any(f[i][q] < 0 for i, q in combinations(range(22), 2)), 'signed control, never host')
    return {'red_degree_square_sum': sum(d * d for d in degrees),
            'f_total': sum(map(sum, f)), 'parity_rows': 22, 'incident_rows': 22,
            'Gram_entries': 100, 'z_bridge_rows': 10, 'exterior_rows': 22,
            'minimum_signed_defect': min(f[i][q] for i, q in combinations(range(22), 2))}

def literal_controls():
    cases = []
    for name, step in (('Petersen', 2), ('prism', 1)):
        for branch in ('red_weight_two', 'red_adjacent_units', 'red_nonadjacent_units',
                       'blue_A_weight_two', 'blue_B_weight_two', 'blue_AA_units',
                       'blue_AB_units', 'blue_BB_units'):
            j = core(step)
            t, g = [0] * 10, [0] * 11
            def remove(a, b):
                j[a].remove(b)
                j[b].remove(a)
            def add(a, b):
                need(b not in j[a], 'new core edge')
                j[a].add(b)
                j[b].add(a)
            if branch == 'red_weight_two':
                t[0] = 2
                remove(0, 1)
                remove(0, 4)
                add(1, 4)
            elif branch == 'red_adjacent_units':
                t[0] = t[1] = 1
                remove(0, 1)
                # These are nonadjacent after deletion. For the adjacent
                # case retain 01 and instead use the removed spoke pair.
                add(0, 1)
                remove(0, 5)
                remove(1, 6)
                if 6 in j[5]:
                    # Prism's spokes use an existing inner edge; select
                    # different external endpoints for a valid switch.
                    add(0, 5)
                    add(1, 6)
                    remove(0, 4)
                    remove(1, 6)
                    add(4, 6)
                else:
                    add(5, 6)
            elif branch == 'red_nonadjacent_units':
                t[0] = t[2] = 1
                remove(0, 1)
                remove(2, 7)
                add(1, 7)
            elif branch == 'blue_A_weight_two':
                g[0] = 2
            elif branch == 'blue_B_weight_two':
                g[3] = 2
            elif branch == 'blue_AA_units':
                g[0] = g[1] = 1
            elif branch == 'blue_AB_units':
                g[0] = g[3] = 1
            elif branch == 'blue_BB_units':
                g[3] = g[4] = 1
            need([len(row) for row in j] == [3 - x for x in t], 'local core degrees')
            w = outside(g)
            m = incidence([5 - int(v < 3) - g[v] for v in range(11)], [5 + x for x in t])
            for version, mm in (('greedy', m), ('switched', switched(m))):
                checks = audit(j, w, mm, t, g)
                cases.append({'template': name, 'branch': branch, 'incidence': version, 'checks': checks})
    out = {'agent': 'six-books-1', 'role': 'researcher', 'private': True,
           'status': 'Literal signed controls validate identities; not a host classification or witness',
           'controls': cases, 'count': len(cases),
           'totals': {k: sum(v['checks'][k] for v in cases) for k in
                      ('parity_rows', 'incident_rows', 'Gram_entries', 'z_bridge_rows', 'exterior_rows')}}
    return {k: v for k, v in out.items() if k not in ('controls', 'private')}


def mask_graph(rows):
    need(type(rows) is list and len(rows) == 10, 'ten adjacency words')
    need(all(type(x) is int and 0 <= x < 1024 for x in rows), 'adjacency word type')
    j = [[int(rows[a] >> b & 1) for b in range(10)] for a in range(10)]
    need(all(j[a][a] == 0 and sum(j[a]) == 3 for a in range(10)), 'cubic representative')
    need(all(j[a][b] == j[b][a] for a in range(10) for b in range(10)), 'symmetric representative')
    return j


def bits_tuple(word):
    return tuple(x for x in range(10) if word >> x & 1)


def validate_input(certificate):
    need(type(certificate) is dict and certificate.get('schema') == 1, 'certificate schema')
    pool = certificate['negative_vectors']
    need(type(pool) is list and pool, 'nonempty negative pool')
    need(all(type(v) is list and len(v) == 10 and any(v)
             and all(type(x) is int for x in v) for v in pool), 'negative-vector type/dimension')
    reps = [mask_graph(rows) for rows in certificate['cubic_representatives']]
    need(len(reps) == 4, 'four declared representatives')
    return pool, reps


def negative_form(j, vector):
    jv = [sum(j[i][k] * vector[k] for k in range(10)) for i in range(10)]
    return (5 * sum(x * x for x in vector) + 3 * sum(vector) ** 2
            - sum(vector[i] * jv[i] for i in range(10)) - sum(x * x for x in jv))


def cubic_domain(pool, reps):
    profiles, full = [], []
    graph_hash, matrix_hash = hashlib.sha256(), hashlib.sha256()
    counts = [0] * len(reps)
    rejected = 0
    for mask in range(8):
        target = [2] * 3
        for k, (a, b) in enumerate(combinations(range(3), 2)):
            if mask >> k & 1:
                target[a] -= 1
                target[b] -= 1
        for cols in combinations_with_replacement(range(8), 6):
            if [sum(c >> a & 1 for c in cols) for a in range(3)] != target:
                continue
            tails = sorted(six_graphs([3 - c.bit_count() for c in cols]))
            need(len(tails) == len(set(tails)), 'duplicate tail graph')
            profiles.append({'mask': mask, 'columns': list(cols), 'count': len(tails)})
            for tail in tails:
                j = full_graph(mask, cols, tail)
                s = gram(j)
                word = ''.join(str(j[a][b]) for a, b in combinations(range(10), 2))
                graph_hash.update((word + '\n').encode())
                matrix_hash.update((json.dumps(s, separators=(',', ':')) + '\n').encode())
                neg = next((i for i, q in enumerate(pool) if negative_form(j, q) < 0), None)
                cid, mapping = None, None
                if neg is not None:
                    need(sum(pool[neg][a] * s[a][b] * pool[neg][b]
                             for a in range(10) for b in range(10)) < 0, 'literal negative certificate')
                    rejected += 1
                else:
                    matches = [(i, isomorphism(j, r)) for i, r in enumerate(reps)]
                    good = [(i, p) for i, p in matches if p is not None]
                    need(len(good) == 1, 'remaining cubic must map uniquely to one representative')
                    cid, mapping = good[0]
                    need(all(j[a][b] == reps[cid][mapping[a]][mapping[b]]
                             for a in range(10) for b in range(10)), 'literal cubic map')
                    counts[cid] += 1
                full.append({'profile': len(profiles) - 1, 'tail': tail,
                             'J': j, 'S0': s, 'negative_index': neg, 'class': cid, 'map': mapping})
    return {'profiles': profiles, 'graphs': len(full), 'negative_forms': rejected,
            'class_copies': counts, 'graph_sha256': graph_hash.hexdigest(),
            'matrix_sha256': matrix_hash.hexdigest()}, full


def a_stars(j, rows, exceptional):
    aset = set(range(5)) - set(exceptional)
    domains = []
    for v in sorted(aset):
        fixed = aset - {v}
        others = sorted(set(range(11)) - aset)
        allowed = []
        for pair in combinations(others, 2):
            neighbors = fixed | set(pair)
            if all(sum(j[x][y] for y in bits_tuple(rows[v]))
                   + sum(int(rows[u] >> x & 1) for u in neighbors) <= 3 for x in range(10)):
                allowed.append(sum(1 << u for u in neighbors))
        domains.append({'vertex': v, 'stars': sorted(allowed)})
    need(any(not d['stars'] for d in domains), 'at least one A vertex has no exterior star')
    return domains


def row_domain(j):
    s = gram(j)
    inv = inverse(s)
    need(all(sum(row) == Q(1, 23) for row in inv), 'inverse row sum')
    words4 = [w for w in range(1024) if w.bit_count() == 4]
    words5 = [w for w in range(1024) if w.bit_count() == 5]
    def inner(a, b):
        return sum(inv[x][y] for x in bits_tuple(a) for y in bits_tuple(b))
    four = [w for w in words4 if inner(w, w) == Q(20, 23)]
    adjacency = [set() for _ in four]
    disjoint = []
    for a, b in combinations(range(len(four)), 2):
        if inner(four[a], four[b]) == Q(-3, 23):
            adjacency[a].add(b)
            adjacency[b].add(a)
            if four[a] & four[b] == 0:
                disjoint.append((a, b))
    all_h = list(cliques(adjacency, 5)) if disjoint else None
    hsets = ([] if all_h is None else
             [h for h in all_h if any(a in h and b in h for a, b in disjoint)
              and all(sum(four[a] >> x & 1 for a in h) == 2 for x in range(10))])
    five = [w for w in words5 if inner(w, w) == Q(65, 69)]
    completions, star_records = [], []
    for h in hsets:
        hrows = tuple(four[a] for a in h)
        candidates = [w for w in five if all(inner(w, r) == Q(2, 23) for r in hrows)]
        fa = [set() for _ in candidates]
        for a, b in combinations(range(len(candidates)), 2):
            if inner(candidates[a], candidates[b]) == Q(-4, 69):
                fa[a].add(b)
                fa[b].add(a)
        solutions = []
        for indices in cliques(fa, 6):
            rows = hrows + tuple(candidates[a] for a in indices)
            need(all(sum(w >> x & 1 for w in rows) == 5 for x in range(10)), 'Gram column total')
            need([[sum((w >> x & 1) * (w >> y & 1) for w in rows) for y in range(10)]
                  for x in range(10)] == s, 'literal binary Gram')
            solutions.append(list(rows))
            for pair in combinations(range(5), 2):
                if rows[pair[0]] & rows[pair[1]] == 0:
                    star_records.append({'rows': list(rows), 'exceptional': list(pair),
                                         'A_star_domains': a_stars(j, rows, pair)})
        completions.append({'H': list(hrows), 'five_candidates': candidates,
                            'solutions': sorted(solutions)})
    return {'S0': s, 'inverse': [[[x.numerator, x.denominator] for x in row] for row in inv],
            'four_candidates': four, 'four_compatible_pairs': sum(map(len, adjacency)) // 2,
            'compatible_disjoint_pairs': [list(pair) for pair in disjoint],
            'H_cliques': None if all_h is None else len(all_h), 'eligible_H': len(hsets),
            'five_candidates': five, 'completions': completions, 'stars': star_records}


def compute(certificate):
    pool, reps = validate_input(certificate)
    census, full = cubic_domain(pool, reps)
    rows = [row_domain(j) for j in reps]
    results = {'cubic_census': census, 'row_domains': rows,
               'summary': {'profiles': len(census['profiles']), 'graphs': census['graphs'],
                           'negative_forms': census['negative_forms'],
                           'cubic_classes': len(reps),
                           'binary_Gram_matrices': sum(len(c['solutions']) for r in rows for c in r['completions']),
                           'exceptional_pair_placements': sum(len(r['stars']) for r in rows),
                           'A_star_survivors': 0},
               'signed_controls': literal_controls()}
    return results, full


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--matrices', type=Path)
    args = parser.parse_args()
    expected = json.loads(Path(__file__).with_name('degree98_zero_attachment_expected.json').read_text())
    results, full = compute(expected)
    need(results == expected['results'], 'compact certificate differs from complete replay')
    if args.matrices:
        args.matrices.write_text(json.dumps({'cubic_matrices': full, 'row_domains': results['row_domains']},
                                           separators=(',', ':')) + '\n')
    print(json.dumps({'agent': 'six-books-1', 'role': 'researcher', 'complete': True,
                      **results['summary'], 'excluded': 'histogram(3,18,1), A=K3, e(z,A)=0',
                      'matrices_written': args.matrices is not None}, sort_keys=True))


if __name__ == '__main__':
    main()
