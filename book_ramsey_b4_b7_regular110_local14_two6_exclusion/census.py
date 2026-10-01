"""Complete local2^2,3^8 necessary-core census; six-books-3, researcher."""
from itertools import combinations, permutations
EDGES = list(combinations(range(8), 2))
EDGE_INDEX = {edge:i for i,edge in enumerate(EDGES)}
CONFIGURATIONS = [{'intersection': 2, 'pairs': ((0, 1), (0, 1)), 'degrees': (1, 1, 3, 3, 3, 3, 3, 3), 'stabilizer': 1440}, {'intersection': 1, 'pairs': ((0, 1), (0, 2)), 'degrees': (1, 2, 2, 3, 3, 3, 3, 3), 'stabilizer': 240}, {'intersection': 0, 'pairs': ((0, 1), (2, 3)), 'degrees': (2, 2, 2, 2, 3, 3, 3, 3), 'stabilizer': 192}]

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def degree_graphs(degrees, forbidden):
    """Decide each vertex's complete forward neighbor set, no omitted stars."""
    remaining = list(degrees)

    def visit(v, mask):
        if v == 8:
            if not any(remaining):
                yield mask
            return
        options = [w for w in range(v + 1, 8) if remaining[w] and (v, w) not in forbidden]
        wanted = remaining[v]
        if wanted < 0 or wanted > len(options):
            return
        for selected in combinations(options, wanted):
            remaining[v] = 0
            new_mask = mask
            for w in selected:
                remaining[w] -= 1
                new_mask |= 1 << EDGE_INDEX[v, w]
            possible = True
            for w in range(v + 1, 8):
                available = sum(remaining[u] > 0 and tuple(sorted((u, w))) not in forbidden
                                for u in range(v + 1, 8) if u != w)
                if remaining[w] < 0 or remaining[w] > available:
                    possible = False
                    break
            if possible and sum(remaining) % 2 == 0:
                yield from visit(v + 1, new_mask)
            for w in selected:
                remaining[w] += 1
            remaining[v] = wanted

    yield from visit(0, 0)

def local_matrix(mask, pairs):
    """Full local adjacency formula; low coordinates0,1 and cubic2..9."""
    neighbors = [set() for _ in range(10)]
    for bit, (u, v) in enumerate(EDGES):
        if mask >> bit & 1:
            neighbors[u + 2].add(v + 2)
            neighbors[v + 2].add(u + 2)
    for low, pair in enumerate(pairs):
        for u in pair:
            neighbors[low].add(u + 2)
            neighbors[u + 2].add(low)
    h = list(map(len, neighbors))
    need(h == [2, 2] + [3] * 8, 'Wrong local degree sequence')
    matrix = [[0] * 10 for _ in range(10)]
    for i in range(10):
        matrix[i][i] = h[i] + 2
        for j in range(i):
            matrix[i][j] = matrix[j][i] = h[i] + h[j] - (5 if j in neighbors[i] else 2) - len(neighbors[i] & neighbors[j])
    return matrix, neighbors

def stabilizer(pairs):
    target = sorted(pairs)
    group = [p for p in permutations(range(8))
             if sorted(tuple(sorted(p[i] for i in pair)) for pair in pairs) == target]
    return group

def transform(mask, permutation):
    result = 0
    for bit, (u, v) in enumerate(EDGES):
        if mask >> bit & 1:
            result |= 1 << EDGE_INDEX[tuple(sorted((permutation[u], permutation[v])))]
    return result

def row_candidates(matrix, neighbors, size, cross_filter):
    h = list(map(len, neighbors))
    for selected in combinations(range(10), size):
        selected = frozenset(selected)
        if any(matrix[i][j] < 1 for i, j in combinations(selected, 2)):
            continue
        if cross_filter:
            outside = set(range(10)) - selected
            if any(size > h[i] + 5 - len(neighbors[i] & outside) for i in outside):
                continue
            if any(len(neighbors[i] & selected) < size - 7 for i in selected):
                continue
        yield tuple(sorted(selected))
