"""Transport an admissible core/tail graph to the selector normal form."""
from itertools import combinations
import compile as compiler


def transport(matrix, order):
    if sorted(order) != list(range(43)):
        raise ValueError('not a vertex permutation')
    return [[matrix[u][v] for v in order] for u in order]


def isomorphism(matrix, edges):
    """Find catalog-vertex -> physical-tail-vertex bijection by exact backtracking."""
    target = [[int((min(i, j), max(i, j)) in edges) if i != j else 0
               for j in range(12)] for i in range(12)]
    degrees = [sum(row) for row in target]
    actual = [sum(row[31:43]) for row in matrix[31:43]]
    candidates = [[v for v in range(12) if actual[v] == degrees[u]] for u in range(12)]
    order = sorted(range(12), key=lambda u: (len(candidates[u]), -degrees[u], u))
    match = {}; used = set()
    def search(position):
        if position == 12:
            return [match[i]+31 for i in range(12)]
        u = order[position]
        for v in candidates[u]:
            if v in used or any(target[u][w] != matrix[v+31][x+31] for w, x in match.items()):
                continue
            match[u] = v; used.add(v)
            result = search(position+1)
            if result is not None:
                return result
            used.remove(v); del match[u]
        return None
    return search(0)


def normalize(matrix):
    if len(matrix) != 43 or any(len(row) != 43 for row in matrix):
        raise ValueError('graph dimensions')
    if any(matrix[u][v] not in (0, 1) or matrix[u][v] != matrix[v][u]
           for u in range(43) for v in range(43)) or any(matrix[u][u] for u in range(43)):
        raise ValueError('simple graph')
    model = compiler.Model()
    colors = []
    for block in model.blocks:
        current = {matrix[u][v] for u, v in combinations(block, 2)}
        if len(current) != 1:
            raise ValueError('nonmonochromatic core block')
        colors.append(current.pop())
    if colors[:5] != [1]*5 or colors[7] != 1 or colors[6] > colors[5]:
        raise ValueError('core color normal form')
    r = 5+colors[5]+colors[6]
    tail = None
    for index, edges in enumerate(model.graphs):
        tail = isomorphism(matrix, edges)
        if tail is not None:
            break
    if tail is None:
        raise ValueError('tail outside catalog')
    def signature(v):
        return sum(matrix[row][v] << row for row in range(4))
    blocks = [model.blocks[0]] + [sorted(b, key=lambda v: (-signature(v), v)) for b in model.blocks[1:]]
    def key(b):
        return tuple(signature(v) for v in b)
    blocks[1:r] = sorted(blocks[1:r], key=key, reverse=True)
    blocks[r:7] = sorted(blocks[r:7], key=key, reverse=True)
    order = [v for b in blocks for v in b] + tail
    return {'matrix': transport(matrix, order), 'order': order, 'catalog_index': index,
            'r': r, 'status': 'STRUCTURAL_NORMAL_FORM_ONLY'}


def repack(matrix):
    """Reverse bridge: split the triangle-free residual into the old blue blocks."""
    remaining = list(range(31, 43)); blue_blocks = []
    def signature(v):
        return sum(matrix[row][v] << row for row in range(4))
    for _ in range(3):
        q = next((q for q in combinations(remaining, 3)
                  if not any(matrix[u][v] for u, v in combinations(q, 2))), None)
        if q is None:
            raise ValueError('no required blue triple')
        blue_blocks.append(sorted(q, key=signature, reverse=True))
        remaining = [v for v in remaining if v not in q]
    t = sum(matrix[u][v] for u, v in combinations(remaining, 2))
    if t > 2:
        raise ValueError('red final triangle')
    degrees = {v: sum(matrix[u][v] for u in remaining) for v in remaining}
    # E3: endpoints first, isolated vertex last. P3: center first, endpoints last.
    last = sorted(remaining, key=lambda v: (degrees[v], signature(v)), reverse=True)
    order = list(range(31)) + [v for block in blue_blocks for v in block] + last
    return {'matrix': transport(matrix, order), 'order': order, 't': t}
