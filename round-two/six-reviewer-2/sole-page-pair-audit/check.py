"""Independent literal and graph-isomorphism audit of Book lemma9131.

Only CPython stdlib. No researcher code or fixture is needed for generation.
Finite controls supplement the ordinary page-count proof in REVIEW.md.
"""
from collections import Counter, deque
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json
import sys


def require(value, label):
    if not value:
        raise ValueError(label)


def graph(n, edges):
    rows = [set() for _ in range(n)]
    for a, b in edges:
        require(type(a) is int and type(b) is int and 0 <= a < n and 0 <= b < n and a != b,
                'simple exact graph edge')
        rows[a].add(b); rows[b].add(a)
    return rows


def pairs(rows):
    return [(a, b) for a, row in enumerate(rows) for b in row if a < b]


def pages(rows, a, b, red):
    require(a != b and ((b in rows[a]) == red), 'selected spine has wrong color')
    if red:
        return len(rows[a] & rows[b])
    vertices = set(range(len(rows))) - {a, b}
    return len(vertices - rows[a] - rows[b])


def core(incidence, t_edges=()):
    # u0/v1, SX2/3, SY4/5, T6/7/8; no mark vertex in this graph.
    edges = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5)]
    edges += [(s + 2, t + 6) for s, t in incidence]
    edges += [(a + 6, b + 6) for a, b in t_edges]
    return graph(9, edges)


def incidence_code(incidence, t_edges=()):
    return sum(1 << (3 * s + t) for s, t in incidence) + sum(
        1 << (12 + list(combinations(range(3), 2)).index((a, b))) for a, b in t_edges)


def literal_host(q, incidence, t_edges=()):
    require(type(q) is int and q >= 2, 'literal saturation control needs q>=2')
    # Same nine core labels, mark a9, and q nonspecial points per root block.
    n = 2 * q + 10
    X0, Y0 = list(range(10, 10 + q)), list(range(10 + q, n))
    SX, SY, T = {2, 3}, {4, 5}, {6, 7, 8}
    X, Y = SX | set(X0), SY | set(Y0)
    rows = graph(n, pairs(core(incidence, t_edges)))
    def add(a, b):
        rows[a].add(b); rows[b].add(a)
    for v in range(9):
        add(9, v)
    for x in X0:
        add(0, x)
    for y in Y0:
        add(1, y)
    for s in SX:
        for x in X0[:2]:
            add(s, x)
    for s in SY:
        for y in Y0[:2]:
            add(s, y)
    require(len(rows[0]) == len(rows[1]) == q + 4 and len(rows[9]) == 9, 'literal root/mark degrees')
    require(rows[0] & rows[1] == {9}, 'literal sole common red page')
    require(rows[9] == set(range(9)), 'literal entire mark neighborhood')
    require(set(range(n)) - {0, 1, 9} - X - Y == T, 'literal exact partition')
    require(pages(rows, 0, 9, True) == pages(rows, 1, 9, True) == 3, 'red root-mark caps')
    for s in SX | SY:
        own, opposite, block = (0, 1, X) if s in SX else (1, 0, Y)
        h, g = len(rows[s] & block), len(rows[s] & T)
        require(h == g == 2, 'literal special degrees')
        require(pages(rows, own, s, True) == 3, 'red own-root special cap')
        require(pages(rows, opposite, s, False) == q, 'blue opposite-root special cap')
        require(pages(rows, 9, s, True) == 3, 'red mark special cap')
    actual = [pages(rows, 9, t, True) for t in sorted(T)]
    necessary = [sum((s, t - 6) in incidence for s in range(4))
                 + sum(t - 6 in e for e in t_edges) for t in sorted(T)]
    require(actual == necessary, 'literal all mark-T page identities')
    return actual


def graph_signatures(rows):
    degree2 = [v for v, row in enumerate(rows) if len(row) == 2]
    require(len(degree2) == 1, 'unique degree-two vertex')
    dist = {degree2[0]: 0}; todo = deque(degree2)
    while todo:
        a = todo.popleft()
        for b in rows[a]:
            if b not in dist:
                dist[b] = dist[a] + 1; todo.append(b)
    require(len(dist) == len(rows), 'connected neighborhood')
    return [(len(row), tuple(sorted(len(rows[b]) for b in row)), dist[a])
            for a, row in enumerate(rows)]


def isomorphisms(left, right):
    """Complete ordinary bijection search with necessary invariant pruning."""
    ls, rs = graph_signatures(left), graph_signatures(right)
    if Counter(ls) != Counter(rs):
        return []
    static = [[b for b in range(9) if rs[b] == sig] for sig in ls]
    image, used, out = {}, set(), []
    def visit():
        if len(image) == 9:
            out.append(tuple(image[a] for a in range(9))); return
        choices = []
        for a in range(9):
            if a in image:
                continue
            candidates = [b for b in static[a] if b not in used
                          and all((c in left[a]) == (d in right[b]) for c, d in image.items())]
            choices.append((len(candidates), -len(left[a] & image.keys()), a, candidates))
        _, _, a, candidates = min(choices)
        for b in candidates:
            image[a] = b; used.add(b); visit(); used.remove(b); del image[a]
    visit()
    require(len(out) == len(set(out)), 'bijection duplicate')
    for p in out:
        require(sorted(p) == list(range(9)) and all((b in left[a]) == (p[b] in right[p[a]])
                for a in range(9) for b in range(9)), 'literal isomorphism image')
    return sorted(out)


def brute_automorphisms(rows):
    fixed = next(a for a, r in enumerate(rows) if len(r) == 2)
    rest = [a for a in range(9) if a != fixed]
    edges = pairs(rows); out = []
    for values in permutations(rest):
        p = dict(zip(rest, values)); p[fixed] = fixed
        if all(p[b] in rows[p[a]] for a, b in edges):
            # A bijection preserving every edge of the same finite graph also
            # preserves all nonedges. No separate heuristic predicate is used.
            out.append(tuple(p[a] for a in range(9)))
    return sorted(out)


def marked_maps():
    result = []
    for swap, f0, f1 in product(range(2), repeat=3):
        for order in permutations(range(6, 9)):
            p = [None] * 9
            p[0], p[1] = swap, 1 - swap
            for k in range(2):
                p[2+k] = (4 if swap else 2) + (k ^ f0)
                p[4+k] = (2 if swap else 4) + (k ^ f1)
            p[6:] = order
            result.append(tuple(p))
    require(len(set(result)) == 48, 'complete marked group48')
    return sorted(result)


def moved_incidence(rows, p):
    return sorted((p[s] - 2, p[t] - 6) for s in range(2, 6) for t in rows[s] if 6 <= t < 9)


def suppression_triangles(rows):
    z = next(a for a, row in enumerate(rows) if len(row) == 2)
    a, b = sorted(rows[z])
    require(b not in rows[a], 'simple degree-two suppression')
    keep = [v for v in range(9) if v != z]
    reduced = [rows[v] - {z} for v in range(9)]
    reduced[a].add(b); reduced[b].add(a)
    require(all(len(reduced[v]) == 3 for v in keep), 'suppressed cubic degrees')
    return sum(b in reduced[a] and c in reduced[a] and c in reduced[b]
               for a, b, c in combinations(keep, 3))


def census():
    universe = list(product(range(4), range(3)))
    te = list(combinations(range(3), 2))
    survivors, data = {}, {k: {'candidates': 0, 'survivors': 0} for k in range(4)}
    fixed_controls = 0
    raw_subsets = 0
    for subset in combinations(universe, 8):
        raw_subsets += 1
        if any(sum(s == a for s, t in subset) != 2 for a in range(4)):
            continue
        for mask in range(8):
            tedges = [e for j, e in enumerate(te) if mask >> j & 1]
            data[len(tedges)]['candidates'] += 1
            rows = core(subset, tedges)
            actual = literal_host(6, subset, tedges)
            fixed_controls += 1
            # Every mark-spine page is a literal core degree; other selected
            # spines were checked in literal_host. No missing-point word test.
            keep = all(k <= 3 for k in actual)
            if keep:
                require(not tedges, 'necessary T independence')
                code = incidence_code(subset, tedges)
                survivors[code] = list(subset)
                data[len(tedges)]['survivors'] += 1
    require(raw_subsets == 495 and fixed_controls == 648, 'whole independent raw edge-subset domain')
    require(len(survivors) == 36, 'whole literal core survivor count')
    clusters = []
    all_transports = 0
    for code, inc in sorted(survivors.items()):
        rows = core(inc)
        require(len(pairs(rows)) == 13 and sorted(map(len, rows)) == [2]+[3]*8, 'all core degrees/edges')
        require(all(not(rows[a] & rows[b]) for a, b in pairs(rows)), 'all core triangle counts')
        hit = None
        for cluster in clusters:
            maps = isomorphisms(rows, core(survivors[cluster['representative']]))
            if maps:
                hit = cluster; all_transports += len(maps); break
        if hit is None:
            hit = {'representative': code, 'members': []}; clusters.append(hit)
        hit['members'].append(code)
    require(len(clusters) == 2 and sorted(len(c['members']) for c in clusters) == [12, 24], 'independent full unmarked isomorphism census')
    group = marked_maps()
    for cluster in clusters:
        rep = cluster['representative']; rows = core(survivors[rep])
        auto = isomorphisms(rows, rows)
        require(auto == brute_automorphisms(rows), 'independent complete8! automorphism replay')
        for p, q in product(auto, repeat=2):
            require(tuple(p[q[a]] for a in range(9)) in auto, 'full automorphism closure')
        orbit = sorted({incidence_code(moved_incidence(rows, p)) for p in group})
        require(orbit == sorted(cluster['members']), 'complete marked48-map orbit versus unmarked classification')
        cluster['unmarked_automorphism_order'] = len(auto)
        cluster['unmarked_automorphisms'] = [list(p) for p in auto]
        cluster['marked_stabilizer_order'] = sum(incidence_code(moved_incidence(rows, p)) == rep for p in group)
        require(len(orbit) * cluster['marked_stabilizer_order'] == 48, 'literal marked orbit stabilizer')
        cluster['suppressed_cubic_triangles'] = suppression_triangles(rows)
        missing = [next(t for t in range(3) if (s,t) not in survivors[rep]) for s in range(4)]
        repeated = next(t for t in range(3) if missing.count(t) == 2)
        positions = [s for s in range(4) if missing[s] == repeated]
        same = positions in ([0,1], [2,3])
        cluster['type'] = 'same_block' if same else 'cross_block'
        require(cluster['suppressed_cubic_triangles'] == int(same), 'independent suppressed-type distinction')
        for word in cluster['members']:
            require(suppression_triangles(core(survivors[word])) == int(same), 'all36 suppressed-type checks')
        admissible = []
        candidates = []
        for a, b in pairs(rows):
            if len(rows[a]) != 3 or len(rows[b]) != 3:
                continue
            sx, sy = rows[a] - {b}, rows[b] - {a}
            if sx & sy or any(len(rows[v]) != 3 for v in sx | sy):
                continue
            t = set(range(9)) - {a, b} - sx - sy
            special_edges = [(x,y) for x,y in pairs(rows) if x in sx | sy and y in sx | sy]
            candidates.append({'edge':[a,b], 'S_internal_edges':len(special_edges)})
            if len(t) == 3 and not special_edges:
                admissible.append([a, b])
        cluster['adjacency'] = [sorted(row) for row in rows]
        cluster['degree_candidate_root_edges'] = candidates
        require(len(candidates) == 7, 'all degree-compatible candidate edges in each type')
        cluster['locally_admissible_root_edges'] = admissible
        require(admissible == [[0,1]], 'unique locally admissible root edge in each full unmarked type')
    q_controls = {}
    for q in [2, 3, 6, 9]:
        for code, inc in survivors.items():
            require(sorted(literal_host(q, inc)) == [2, 3, 3], 'parameterized literal q control')
        q_controls[str(q)] = {'n': 2*q+10, 'root_degree': q+4, 'checked_cores': len(survivors)}
    return {'raw_edge_subsets': raw_subsets, 'complete_conditional_core_domain': fixed_controls,
            'by_T_edges': {str(k): v for k, v in data.items()}, 'core_words': sorted(survivors),
            'unmarked_clusters': clusters, 'complete_isomorphism_transports': all_transports,
            'parameterized_literal_controls': q_controls}


def local_count_domains():
    saturation = []
    # All feasible integer (h,g) against the three necessary page bounds.
    for h, g in product(range(8), range(4)):
        if h <= 2 and h + g >= 4 and g <= 2:
            saturation.append([h, g])
    require(saturation == [[2, 2]], 'three-spine saturation domain')
    # d(a)=9 requires all capacities (x,y,t) attain equality.
    mark = [[x, y, t] for x, y, t in product(range(3), range(3), range(4))
            if 2 + x + y + t == 9]
    require(mark == [[2, 2, 3]], 'mark equality domain')
    profiles = [list(v) for v in product(range(4), repeat=3) if sum(v) == 8]
    require(sorted(profiles) == [[2, 3, 3], [3, 2, 3], [3, 3, 2]], 'whole T-row profile domain')
    return {'special_saturation': saturation, 'mark_saturation': mark, 'T_degree_profiles': profiles,
            'uniform_q_bridge': 'n=2q+10,d(u)=d(v)=q+4, |X|=q+2,|T|=3; (|X|-1)+|T|-q=4 exactly',
            'small_q_exclusion': 'If q<2 then each special needs2 distinct nonspecial neighbors in a block containing only q; d(a)=9 impossible.'}


def leaf_control():
    adjacency = [[1,8,9],[0],[6,7],[4,5],[3,7,9],[3,6,8],[2,5,9],[2,4,8],[0,5,7],[0,4,6]]
    rows = [set(r) for r in adjacency]
    require(all((b in rows[a]) == (a in rows[b]) for a in range(10) for b in range(10)),
            'literal old leaf symmetry')
    require(len(pairs(rows)) == 13 and len(rows[1]) == 1 and rows[1] == {0}, 'literal original leaf')
    key = sum(1 << list(combinations(range(10), 2)).index(e) for e in pairs(rows))
    require(key == 6790396772737, 'original exact leaf key')
    A_degrees = [9] + [10]*9
    cross = sum(A_degrees) - 10 - 2*len(pairs(rows))
    require(cross == 63 and 10+13+cross == 86, 'rederived old equality count')
    B_edges = 11*4//2
    TY = 3*4
    require(86+B_edges == 108 and B_edges-TY+1+2 == 13, 'retained leaf corollary arithmetic')
    return {'old_leaf_key':key,'A_degree_sum':sum(A_degrees),'A_B_edges':cross,
            'constant_edges_before_B':86,'forced_B_edges_at_most108':22,
            'forced_T_Y_edges':12,'forced_Y_edges':10,'forced_second_root_neighborhood_edges':13}


def damages():
    outcomes = []
    for label, action in [('float q', lambda: literal_host(6.0, [])),
                          ('insufficient nonspecial block', lambda: literal_host(1, [])),
                          ('self loop', lambda: graph(2, [(0,0)])),
                          ('changed edge count', lambda: require(len(pairs(core([]))) == 13, 'damage')),
                          ('spine color', lambda: pages(graph(2, []), 0, 1, True)),
                          ('wrong literal core degrees', lambda: literal_host(6, [(s,t) for s in range(4) for t in range(3)]))]:
        try:
            action()
        except (ValueError, TypeError):
            outcomes.append(label)
        else:
            raise ValueError('damage accepted '+label)
    return outcomes


def validate_record(actual, expected):
    """Exact recursive type and value comparison: bool/float cannot encode ints."""
    require(type(actual) is type(expected), 'frozen record type differs')
    if type(actual) is dict:
        require(actual.keys() == expected.keys(), 'frozen record fields differ')
        for k in actual:
            validate_record(actual[k], expected[k])
    elif type(actual) is list:
        require(len(actual) == len(expected), 'frozen record list size differs')
        for a, b in zip(actual, expected):
            validate_record(a, b)
    else:
        require(actual == expected, 'frozen record value differs')


def record_damages(record):
    damaged = []
    for label in ['removed core', 'duplicated core', 'changed T-edge survivor',
                  'bool incidence code', 'float cardinality', 'extra admissible root']:
        candidate = json.loads(json.dumps(record))
        c = candidate['census']
        if label == 'removed core':
            c['core_words'].pop()
        elif label == 'duplicated core':
            c['core_words'].append(c['core_words'][0])
        elif label == 'changed T-edge survivor':
            c['by_T_edges']['1']['survivors'] = 1
        elif label == 'bool incidence code':
            c['core_words'][0] = True
        elif label == 'float cardinality':
            c['complete_conditional_core_domain'] = 648.0
        else:
            c['unmarked_clusters'][0]['locally_admissible_root_edges'].append([0,2])
        try:
            validate_record(record, candidate)
        except ValueError:
            damaged.append(label)
        else:
            raise ValueError('record damage accepted '+label)
    return damaged


def main():
    record = {'agent':'six-reviewer-2','role':'independent mathematical reviewer',
              'target':'9131 / bafkreiesfsfe44lvytykz4oczwidosjpdxf4g3imjfnw7pxdllkmqsfqwu',
              'proof_domain':'Ordinary page-count theorem and all-q local extension; literal cores are necessary selected-spine controls, not valid full hosts.',
              'census':census(),'count_domains':local_count_domains(),'leaf_control':leaf_control(),
              'rejected_damages':damages()}
    record['rejected_record_damages'] = record_damages(record)
    raw = json.dumps(record, sort_keys=True, separators=(',',':')).encode()
    digest = hashlib.sha256(raw).hexdigest()
    if '--record' in sys.argv:
        print(json.dumps(record, sort_keys=True, indent=2))
    else:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        validate_record(record, expected)
        print(json.dumps({'status':'PASS','canonical_record_sha256':digest,
                          'raw_edge_subsets':495,'conditional_cores':648,'accepted_cores':36,
                          'unmarked_type_sizes':[len(c['members']) for c in record['census']['unmarked_clusters']],
                          'unmarked_automorphism_orders':[c['unmarked_automorphism_order'] for c in record['census']['unmarked_clusters']],
                          'q_controls':[2,3,6,9],
                          'rejected_damages':len(record['rejected_damages'])+len(record['rejected_record_damages'])},sort_keys=True))


if __name__ == '__main__':
    main()
