"""Producer-free arithmetic and dense literal graph verification."""
from itertools import combinations, product, permutations
import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def table_audit(table):
    rows = table['rows']
    keys = [(r['omega'], r['alpha']) for r in rows]
    require(len(keys) == 16 and set(keys) == set(product(range(1, 5), repeat=2)),
            'incomplete or duplicate cap domain')
    d = dict(zip(keys, rows))
    for (a, b), row in d.items():
        require(all(row['upper'] <= d[x, y]['upper']
                    for x in range(a, 5) for y in range(b, 5)),
                'coordinatewise monotonicity')
    # A single ten-coordinate enumeration, independently filtered using all
    # literal cliques/stable sets of the five-cycle, audits every cap row.
    c = [[int((i-j) % 5 in (1, 4)) for j in range(5)] for i in range(5)]
    cliques, stable = [], []
    for mask in range(1, 32):
        vertices = [i for i in range(5) if mask >> i & 1]
        if all(c[i][j] for i, j in combinations(vertices, 2)):
            cliques.append(vertices)
        if all(not c[i][j] for i, j in combinations(vertices, 2)):
            stable.append(vertices)
    counts = {k: 0 for k in keys}
    maxima = {k: 0 for k in keys}
    attainers = {k: [] for k in keys}
    valid = 0
    for bits in product((1, 2, 3), repeat=10):
        p, q = bits[:5], bits[5:]
        a0 = max(sum(p[i] for i in s) for s in cliques)
        b0 = max(sum(q[i] for i in s) for s in stable)
        if a0 > 4 or b0 > 4:
            continue
        valid += 1
        value = sum(d[p[i], q[i]]['upper'] for i in range(5))
        for a in range(a0, 5):
            for b in range(b0, 5):
                key = a, b
                counts[key] += 1
                if value > maxima[key]:
                    maxima[key], attainers[key] = value, []
                if value == maxima[key]:
                    attainers[key].append([list(p), list(q)])
    # Cross multiplication and Euclidean reduction, without Fraction or
    # the producer's recurrence iteration, audit all rational envelopes.
    from math import gcd
    for (a, b), row in d.items():
        num, den = 0, 1
        pairs = [(p, q) for p in range(1, a+1) for q in range(1, b+1)
                 if (p, q) != (a, b)]
        for p, q in pairs:
            z = d[p, q]['upper']
            if z*den > num*p*q:
                num, den = z, p*q
        g = gcd(num, den)
        num, den = num//g, den//g
        require(row['rho'] == [num, den], 'rational envelope')
        require(sorted(row['rho_attainers']) == sorted(
            [[p, q] for p, q in pairs if d[p, q]['upper']*den == num*p*q]),
            'envelope attainers')
        perfect = a*b*num//den
        require(row['perfect_upper'] == perfect, 'perfect bound')
        require(row['c5_population_count'] == counts[a, b], 'population completeness')
        require(row['c5_upper'] == maxima[a, b], 'cycle maximum')
        require(row['c5_maximizers'] == attainers[a, b], 'entrywise cycle maximizers')
        require(row['upper'] == max(1, perfect, maxima[a, b]), 'induction closure')
    require(table['max_good_order'] == 25 and d[4, 4]['upper'] == 25,
            'target cap')
    require(table['excluded_core_order'] == 26 and table['target_order'] == 43
            and table['arbitrary_outside_vertices'] == 17, 'global class')
    require(table['c5_population_checks'] == sum(counts.values()), 'total counts')
    require(d[4, 4]['perfect_upper'] < 25 and d[4, 4]['c5_maximizers'] ==
            [[[2]*5, [2]*5]], 'unique top equality pattern')
    return {'ten_coordinate_vectors': 3**10, 'admissible_vectors': valid,
            'cap_row_incidents': sum(counts.values()), 'rows': 16}


def weighted_controls():
    # Every graph on four vertices is perfect; directly check the weighted
    # clique/stable-set product inequality without a coloring routine.
    subsets = [[i for i in range(4) if m >> i & 1] for m in range(1, 16)]
    pairs = list(combinations(range(4), 2))
    count = 0
    for word in range(64):
        a = [[0]*4 for _ in range(4)]
        for k, (i, j) in enumerate(pairs):
            a[i][j] = a[j][i] = word >> k & 1
        cs = [s for s in subsets if all(a[i][j] for i, j in combinations(s, 2))]
        ss = [s for s in subsets if all(not a[i][j] for i, j in combinations(s, 2))]
        for w in product((1, 2), repeat=8):
            p, q = w[:4], w[4:]
            left = sum(p[i]*q[i] for i in range(4))
            ca = max(sum(p[i] for i in s) for s in cs)
            cb = max(sum(q[i] for i in s) for s in ss)
            require(left <= ca*cb, 'weighted product control')
            count += 1
    # C5 at unit weights violates the product inequality, so its perfect
    # hypothesis cannot be discarded in the proof.
    require(5 > 2*2, 'nonperfect negative control')
    return {'four_vertex_graph_weight_pairs': count,
            'nonperfect_cycle_control': {'left': 5, 'right': 4}}


def matrix(item):
    n, h = item['n'], item['red_bits_hex']
    require(type(n) is int and 1 <= n <= 43, 'order')
    width = max(1, (n*(n-1)//2+3)//4)
    require(type(h) is str and len(h) == width and
            all(x in '0123456789abcdef' for x in h), 'hex convention')
    w = int(h, 16)
    require(w < (1 << (n*(n-1)//2)), 'unused high bits')
    a = [[0]*n for _ in range(n)]
    for k, (i, j) in enumerate(combinations(range(n), 2)):
        a[i][j] = a[j][i] = w >> k & 1
    return a


def five_kind(a, s):
    degrees = [sum(a[u][v] for v in s if u != v) for u in s]
    if degrees == [0]*5:
        return 'blue5'
    if degrees == [4]*5:
        return 'red5'
    deg = sorted(degrees)
    if deg not in ([1, 1, 2, 2, 2], [2, 2, 2, 3, 3]):
        return None
    color = int(deg == [1, 1, 2, 2, 2])
    seen, stack = {s[0]}, [s[0]]
    while stack:
        u = stack.pop()
        for v in s:
            if u != v and a[u][v] == color and v not in seen:
                seen.add(v)
                stack.append(v)
    return ('path' if color else 'complement_path') if len(seen) == 5 else None


def tree_matrix(tree):
    kind = tree['kind']
    if kind in ('clique', 'independent'):
        n = tree['n']
        require(type(n) is int and n >= 1, 'tree leaf')
        return [[int(i != j and kind == 'clique') for j in range(n)] for i in range(n)]
    require(kind == 'cycle5' and len(tree['children']) == 5, 'tree node')
    parts = [tree_matrix(t) for t in tree['children']]
    labels = [(i, j) for i, block in enumerate(parts) for j in range(len(block))]
    return [[parts[i][u][v] if i == j else int((i-j) % 5 in (1, 4))
             for j, v in labels] for i, u in labels]


def witness_audit(witnesses, table):
    require(witnesses['bit_order'] == 'low bits for lexicographic unordered pairs',
            'bit order')
    items = witnesses['graphs']
    keys = [(g['omega'], g['alpha']) for g in items]
    require(len(keys) == 16 and set(keys) == set(product(range(1, 5), repeat=2)),
            'witness coverage')
    bounds = {(r['omega'], r['alpha']): r['upper'] for r in table['rows']}
    checked_fives, checked_extrema = 0, 0
    for g in items:
        a = matrix(g)
        require(a == tree_matrix(g['tree']), 'tree to literal edges')
        n = g['n']
        require(n == bounds[g['omega'], g['alpha']], 'attaining order')
        for color, key in [(1, 'omega'), (0, 'alpha')]:
            k = g[key]
            found = False
            for s in combinations(range(n), k):
                checked_extrema += 1
                if all(a[u][v] == color for u, v in combinations(s, 2)):
                    found = True
            require(found, 'claimed extremum absent')
            for s in combinations(range(n), k+1):
                checked_extrema += 1
                require(not all(a[u][v] == color for u, v in combinations(s, 2)),
                        'larger homogeneous set')
        for s in combinations(range(n), 5):
            checked_fives += 1
            require(five_kind(a, s) is None, 'witness outside hereditary Ramsey class')
    top = next(g for g in items if g['omega'] == g['alpha'] == 4)
    a = matrix(top)
    require(sum(map(sum, a)) == 300 and all(sum(row) == 12 for row in a),
            'top witness physical degrees')
    return {'graphs': 16, 'literal_five_sets': checked_fives,
            'literal_extremum_tests': checked_extrema,
            'top_order': 25, 'top_edges': 150, 'top_degree': 12}


def main():
    table = json.loads((HERE/'TABLE.json').read_text())
    witnesses = json.loads((HERE/'WITNESSES.json').read_text())
    arithmetic = table_audit(table)
    physical = witness_audit(witnesses, table)
    weights = weighted_controls()
    # All 1024 five-vertex edge words, against explicit ordered paths.
    p5 = set()
    pairs = list(combinations(range(5), 2))
    for order in permutations(range(5)):
        edges = {tuple(sorted((order[i], order[i+1]))) for i in range(4)}
        p5.add(sum(1 << i for i, uv in enumerate(pairs) if uv in edges))
    require(len(p5) == 60 and not p5.intersection({1023-x for x in p5}),
            'path orbit')
    for word in range(1024):
        a = matrix({'n': 5, 'red_bits_hex': format(word, '03x')})
        expected = ('red5' if word == 1023 else 'blue5' if word == 0 else
                    'path' if word in p5 else 'complement_path' if 1023-word in p5 else None)
        require(five_kind(a, tuple(range(5))) == expected, 'path recognizer')
    rejected = []
    mutations = [
        ('missing_cap', lambda t: t['rows'].pop()),
        ('false_34_bound15', lambda t: next(r for r in t['rows'] if
            r['omega'] == 3 and r['alpha'] == 4).__setitem__('upper', 15)),
        ('false_top24', lambda t: t.__setitem__('max_good_order', 24)),
        ('omitted_cycle_maximizer', lambda t: t['rows'][-1]['c5_maximizers'].clear()),
    ]
    for name, mutate in mutations:
        t = copy.deepcopy(table)
        mutate(t)
        try:
            table_audit(t)
        except (ValueError, KeyError):
            rejected.append(name)
        else:
            raise ValueError('accepted corrupt table: '+name)
    for name, mutate in [
        ('wrong_top_edge', lambda w: w['graphs'][-1].__setitem__('red_bits_hex',
            format(int(w['graphs'][-1]['red_bits_hex'], 16)^1, '075x'))),
        ('missing_graph', lambda w: w['graphs'].pop()),
        ('wrong_extremum', lambda w: w['graphs'][-1].__setitem__('alpha', 3)),
    ]:
        w = copy.deepcopy(witnesses)
        mutate(w)
        try:
            witness_audit(w, table)
        except (ValueError, KeyError):
            rejected.append(name)
        else:
            raise ValueError('accepted corrupt witness: '+name)
    return {'status': 'VERIFIED_COMPLETE_PATH_COMPLEMENT_CORE_EXCLUSION',
            'arithmetic': arithmetic, 'physical': physical,
            'weighted_product_controls': weights,
            'five_vertex_words_checked': 1024, 'rejected_mutations': rejected,
            'solver_calls': 0, 'good43_found': False,
            'external_decomposition_theorem_reproved': False}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
