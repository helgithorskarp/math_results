"""Independent finite checks of transport.py, with set-based game replay.

Run normally to compare with expected.json; --emit prints freshly computed
evidence without reading that file. All enumeration is finite and explicit.
"""
import hashlib
import json
import sys
from collections import Counter, deque
from itertools import combinations
from pathlib import Path
import transport as producer

HERE = Path(__file__).resolve().parent
COUNTS = Counter()
DIGEST = hashlib.sha256()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def face(mask):
    return frozenset(i for i in range(mask.bit_length()) if mask >> i & 1)


def ordered(complex_):
    return sorted(complex_, key=lambda h: (len(h), tuple(sorted(h))))


def direct_mu(complex_):
    # Boolean-interval alternating formula, not producer's recursion.
    return {h: -sum((-1)**(len(g)-len(h)) for g in complex_ if h <= g)
            for h in complex_}


def record(obj):
    DIGEST.update(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode())
    DIGEST.update(b'\n')


def replay(complex_, word, optimal=True, endpoints=None):
    fs = {face(h) for h in complex_}
    mu = direct_mu(fs)
    state, uses, signs, snapshots = set(), Counter(), Counter(), {}
    wanted = set(endpoints or [])
    for step, raw in enumerate(word, 1):
        h = face(raw)
        require(h in fs and mu[h] != 0, 'absent or forbidden move')
        ideal = {g for g in fs if g <= h}
        if ideal.isdisjoint(state):
            direction = 1
        elif ideal <= state:
            direction = -1
        else:
            raise ValueError('non-monochromatic ideal')
        state.symmetric_difference_update(ideal)
        uses[h] += 1
        signs[h] += direction
        COUNTS['replayed_moves'] += 1
        if step in wanted:
            snapshots[step] = set(state)
    require(state == fs, 'not winning')
    require(all(signs[h] == -mu[h] for h in fs), 'signed multiplicity')
    if optimal:
        require(all(uses[h] == abs(mu[h]) for h in fs), 'not facewise optimal')
    return snapshots


def bfs_word(complex_):
    """Unrestricted legal-state BFS: no target multiplicities assumed."""
    fs = sorted(complex_, key=lambda x: (x.bit_count(), x))
    mu = direct_mu({face(h) for h in fs})
    moves = [(h, sum(1 << i for i, g in enumerate(fs) if g & h == g))
             for h in fs if mu[face(h)]]
    goal = (1 << len(fs)) - 1
    parent = {0: None}
    queue = deque([0])
    while queue:
        state = queue.popleft()
        if state == goal:
            word = []
            while state:
                state, move = parent[state]
                word.append(move)
            COUNTS['bfs_visited_states'] += len(parent)
            COUNTS['bfs_instances'] += 1
            return word[::-1]
        for move, ideal in moves:
            if state & ideal not in (0, ideal):
                continue
            nxt = state ^ ideal
            if nxt not in parent:
                parent[nxt] = state, move
                queue.append(nxt)
    raise ValueError('finite BFS found no winning word')


def all_complexes(n):
    """All downsets containing empty, including missing ground-set vertices."""
    candidates = sorted(range(1, 1 << n), key=lambda h: (h.bit_count(), h))
    def generate(i, current):
        if i == len(candidates):
            yield frozenset(current)
            return
        h = candidates[i]
        yield from generate(i + 1, current)
        if all((h ^ (1 << j)) in current
               for j in range(n) if h >> j & 1):
            yield from generate(i + 1, current | {h})
    yield from generate(0, {0})


def check_transport(complex_, word, sigma, optimal=True, test_backtrack=False):
    new_bit = 1 << max(complex_).bit_length()
    subdiv, lifted, endpoints = producer.compile_word(complex_, word, sigma, new_bit)
    old_fs = {face(h) for h in complex_}
    new_fs = {face(h) for h in subdiv}
    s, p = face(sigma), face(new_bit)
    mu, new_mu = direct_mu(old_fs), direct_mu(new_fs)
    # Independently reconstruct the subdivision from its maximal simplices.
    facets = [h for h in old_fs if not any(h < g for g in old_fs)]
    expected_facets = []
    for h in facets:
        expected_facets.extend([h] if not s <= h else
                               [(h - {v}) | p for v in sorted(s)])
    expected_fs = {frozenset(a) for h in expected_facets
                   for r in range(len(h) + 1) for a in combinations(sorted(h), r)}
    require(new_fs == expected_fs, 'wrong subdivision faces')
    for g in new_fs:
        if g.isdisjoint(p):
            expected = mu[g]
        else:
            carrier = (g - p) | s
            expected = (-1)**(len(s) - len(g & s) - 1) * mu[carrier]
        require(new_mu[g] == expected, 'Mobius transport identity')
        COUNTS['mobius_face_checks'] += 1
    snapshots = replay(subdiv, lifted, optimal, endpoints)
    state = set()
    for h, endpoint in zip(word, endpoints):
        old_h = face(h)
        state.symmetric_difference_update({g for g in old_fs if g <= old_h})
        for g in new_fs:
            carrier = g if g.isdisjoint(p) else (g - p) | s
            require((g in snapshots[endpoint]) == (carrier in state),
                    'carrier state invariant at a block endpoint')
            COUNTS['carrier_face_checks'] += 1
    factor = (1 << len(s)) - 1
    require(len(lifted) == sum(factor if h & sigma == sigma else 1 for h in word),
            'word-length amplification')
    if optimal:
        lower = sum(abs(x) for x in mu.values())
        expected_length = lower + (factor - 1) * sum(abs(mu[h]) for h in old_fs if s <= h)
        require(len(lifted) == expected_length, 'optimal length formula')
    COUNTS['stellar_cases'] += 1
    record([sorted(complex_), sigma, lifted, endpoints,
            sorted((sum(1 << i for i in g), m) for g, m in new_mu.items())])
    if test_backtrack:
        # Exercises both directions at every used ideal, beyond optimal inputs.
        looped = word + word[::-1] + word
        _, backtracked, _ = check_transport(complex_, looped, sigma, False, False)
        require(len(backtracked) == 3 * len(lifted), 'backtrack length')
        COUNTS['nonoptimal_inputs'] += 1
    return subdiv, lifted, endpoints


def check_barycentric(complex_, word):
    subdiv, lifted, labels = producer.barycentric_compile(complex_, word)
    original = {face(h) for h in complex_}
    mu = direct_mu(original)
    inverse = {face(v): face(h) for h, v in labels.items()}
    actual = {face(h) for h in subdiv}
    # Enumerate all strict nonempty-face chains by adding larger last faces.
    chains = {frozenset()}
    for h in ordered(original - {frozenset()}):
        new_vertex = face(labels[sum(1 << i for i in h)])
        chains |= {c | new_vertex for c in list(chains)
                   if all(inverse[frozenset({v})] < h for v in c)}
    require(actual == chains, 'descending stellar sequence is not sd(K)')
    new_mu = direct_mu(actual)
    for chain in actual:
        if not chain:
            require(new_mu[chain] == mu[frozenset()], 'empty face changed')
        else:
            h = max((inverse[frozenset({v})] for v in chain), key=len)
            require(new_mu[chain] == (-1)**(len(h)-len(chain))*mu[h], 'chain Mobius')
        COUNTS['barycentric_face_checks'] += 1
    # Count chains independently; compare with ordered-Bell expression.
    expected_length = abs(mu[frozenset()]) + sum(
        producer.ordered_bell(len(h))*abs(mu[h]) for h in original if h)
    require(len(lifted) == expected_length, 'ordered-Bell length formula')
    replay(subdiv, lifted)
    COUNTS['barycentric_cases'] += 1
    record(['barycentric', sorted(complex_), lifted])
    return subdiv, lifted


def surface_type(complex_):
    fs = {face(h) for h in complex_}
    vertices = {h for h in fs if len(h) == 1}
    edges = {h for h in fs if len(h) == 2}
    triangles = {h for h in fs if len(h) == 3}
    require(all(len(h) <= 3 for h in fs) and triangles, 'not two-dimensional')
    incidence = {e: [t for t in triangles if e <= t] for e in edges}
    require(all(len(ts) == 2 for ts in incidence.values()), 'nonclosed edge')
    for v in vertices:
        link_edges = [t - v for t in triangles if v <= t]
        link_vertices = set().union(*link_edges)
        require(all(sum(w in e for e in link_edges) == 2 for w in link_vertices), 'bad link degrees')
        reached = {min(link_vertices)}
        while True:
            enlarged = reached | set().union(*(set(e) for e in link_edges if e & reached))
            if enlarged == reached:
                break
            reached = enlarged
        require(reached == link_vertices, 'disconnected vertex link')
    first = min(triangles, key=lambda t: tuple(sorted(t)))
    orientation, queue, orientable = {first: 1}, [first], True
    while queue:
        t = queue.pop()
        ordered_t = sorted(t)
        for e in (frozenset(x) for x in combinations(ordered_t, 2)):
            u = next(x for x in incidence[e] if x != t)
            ct = (-1)**ordered_t.index(next(iter(t - e)))
            cu = (-1)**sorted(u).index(next(iter(u - e)))
            desired = -orientation[t]*ct*cu
            if u in orientation:
                orientable &= orientation[u] == desired
            else:
                orientation[u] = desired
                queue.append(u)
    require(len(orientation) == len(triangles), 'disconnected surface')
    return [len(vertices), len(edges), len(triangles),
            len(vertices)-len(edges)+len(triangles), bool(orientable)]


def rejection(call):
    try:
        call()
    except ValueError:
        COUNTS['negative_controls'] += 1
    else:
        raise ValueError('negative control was accepted')


def run():
    small = list(all_complexes(4))
    require(len(small) == 167, 'four-label downset count')
    for complex_ in small:
        word = bfs_word(complex_)
        replay(complex_, word)
        COUNTS['small_complexes'] += 1
        for sigma in sorted(complex_ - {0}):
            sub, lifted, _ = check_transport(complex_, word, sigma, test_backtrack=True)
            if max(complex_) < 8:
                shortest = bfs_word(sub)
                require(len(shortest) == len(lifted), 'small subdivided BFS optimum')
        check_barycentric(complex_, word)
    # Local macro extremes, including a single-vertex stellar relabeling.
    for size in range(1, 6):
        sigma = (1 << size) - 1
        for extra in range(3):
            common = ((1 << (extra + 1)) - 1) << size
            facets = [common | (sigma ^ (1 << i)) for i in range(size)]
            local = producer.closure(facets)
            word = producer.local_word(sigma, common)
            replay(local, word)
            require(set(word) == {common | a for a in producer.subfaces(sigma) if a != sigma},
                    'local word fails to use each fiber member once')
            COUNTS['local_macros'] += 1
            record(['local', size, extra, word])
    seeds = json.loads((HERE / 'seeds.json').read_text())
    seed_summary = {}
    for seed in seeds:
        facets = [sum(1 << v for v in h) for h in seed['facets']]
        complex_ = producer.closure(facets)
        word = [sum(1 << v for v in h) for h in seed['word']]
        replay(complex_, word)
        topo = surface_type(complex_)
        require(topo == {'sphere': [4, 6, 4, 2, True], 'rp2': [6, 15, 10, 1, False],
                         'torus': [7, 21, 14, 0, True]}[seed['name']], 'wrong seed surface')
        for sigma in sorted(complex_ - {0}):
            sub, lifted, _ = check_transport(complex_, word, sigma, test_backtrack=True)
            require(surface_type(sub)[3:] == topo[3:], 'surface changed under subdivision')
        bary, bary_word = check_barycentric(complex_, word)
        require(surface_type(bary)[3:] == topo[3:], 'surface changed under barycentric subdivision')
        seed_summary[seed['name']] = {'f_vector': topo[:3], 'chi': topo[3],
                                     'orientable': topo[4], 'length': len(word),
                                     'barycentric_length': len(bary_word)}
        # One mixed sequence tests composition and stellar faces created earlier.
        current, current_word = complex_, word
        for step in range(12):
            choices = sorted(current - {0}, key=lambda h: (h.bit_count(), h))
            sigma = choices[(17 * step + 13) % len(choices)]
            current, current_word, _ = check_transport(current, current_word, sigma)
            require(surface_type(current)[3:] == topo[3:], 'mixed refinement changed surface')
            COUNTS['iterated_steps'] += 1
    edge = {0, 1, 2, 3}
    rejection(lambda: producer.compile_word(edge, [3], 0, 4))
    rejection(lambda: producer.compile_word(edge, [3], 7, 4))
    rejection(lambda: producer.compile_word(edge, [3], 3, 2))
    rejection(lambda: producer.compile_word(edge, [3], 3, 12))
    rejection(lambda: producer.compile_word(edge, [], 3, 4))
    rejection(lambda: producer.compile_word(edge, [0, 3], 3, 4))
    cycle = producer.closure([3, 6, 5])
    rejection(lambda: producer.compile_word(cycle, [3, 6], 3, 8))
    rejection(lambda: replay(edge, [3, 3]))
    rejection(lambda: replay(edge, [3, 3, 3]))  # winning, but not optimal
    return {'status': 'pass', 'counts': dict(sorted(COUNTS.items())),
            'seeds': seed_summary, 'entrywise_sha256': DIGEST.hexdigest()}


if __name__ == '__main__':
    evidence = run()
    if '--emit' not in sys.argv:
        require(evidence == json.loads((HERE / 'expected.json').read_text()),
                'recorded evidence mismatch')
    print(json.dumps(evidence, indent=2, sort_keys=True))
