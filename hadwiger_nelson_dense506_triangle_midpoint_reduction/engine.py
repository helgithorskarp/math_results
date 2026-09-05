"""Exact common-midpoint compatibility graph on differently coloured H pairs."""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / 'hadwiger_nelson_dense506_two_point_extension/geometry.py'
if sha256(SOURCE.read_bytes()).hexdigest() != 'ce68ab6130082828fbd4e709586ae9dd53273c41e0cb4bfe3aad0278d08faddd':
    raise ValueError('geometry source pin')
spec = importlib.util.spec_from_file_location('prior_geometry', SOURCE)
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load():
    raw = (SOURCE.parent / 'host_colors.txt').read_bytes()
    require(sha256(raw).hexdigest() == '010e6190aa14b6eadc285a6131d7b455bd5434f79ed9b4f69cdfb2848acddcb4', 'colour row pin')
    colors = list(map(int, raw.decode().strip()))
    points = G.host()
    require(len(points) == len(colors) == 506, 'host order')
    _, _, edges = G.distances(points)
    require(all(colors[i] != colors[j] for i, j in edges), 'host colouring')
    return points, colors


def dot(u, v):
    return G.add(G.mul(u[0], v[0]), G.scale(G.mul(u[1], v[1]), 3))


def compatible(s, t, product, radius_scale):
    """Necessary equality; no positivity or square-root test is imposed."""
    q = G.scale(G.ONE, radius_scale)
    delta = G.sub(G.sub(q, s), t)
    left = G.mul(G.mul(delta, delta), G.mul(s, t))
    right = G.scale(G.mul(G.mul(G.sub(q, s), G.sub(q, t)),
                          G.mul(product, product)), 4)
    return left == right


def build(points, colors):
    groups = defaultdict(list)
    vectors, squared = {}, {}
    for i, j in combinations(range(len(points)), 2):
        if colors[i] == colors[j]:
            continue
        x, y = points[i]
        xx, yy = points[j]
        midpoint = G.add(x, xx) + G.add(y, yy)
        palette = tuple(sorted((colors[i], colors[j])))
        groups[(palette, midpoint)].append((i, j))
        v = G.sub(xx, x), G.sub(yy, y)
        vectors[(i, j)] = v
        squared[(i, j)] = G.norm(*v)
    fibres = sorted((palette, pairs) for (palette, _), pairs in groups.items())
    edges = []
    tested = zero_dot = 0
    for pairs in groups.values():
        for a, b in combinations(pairs, 2):
            tested += 1
            product = dot(vectors[a], vectors[b])
            if compatible(squared[a], squared[b], product, 4 * G.D ** 2):
                edges.append(a + b)
                zero_dot += product == G.ZERO
    edges.sort()
    return fibres, edges, tested, zero_dot


def path_components(edges):
    adjacency = defaultdict(set)
    for i, j, k, ell in edges:
        a, b = (i, j), (k, ell)
        require(a != b, 'self edge')
        adjacency[a].add(b)
        adjacency[b].add(a)
    require(all(len(nn) <= 2 for nn in adjacency.values()), 'degree above two')
    seen = set()
    paths = []
    for start in sorted(adjacency):
        if start in seen:
            continue
        stack = [start]
        component = set()
        while stack:
            a = stack.pop()
            if a in component:
                continue
            component.add(a)
            stack.extend(adjacency[a] - component)
        seen.update(component)
        require(sum(len(adjacency[a]) for a in component) == 2 * (len(component) - 1),
                'component is not a tree')
        endpoint = min(a for a in component if len(adjacency[a]) == 1)
        path = [endpoint]
        previous = None
        while True:
            following = adjacency[path[-1]] - ({previous} if previous is not None else set())
            if not following:
                break
            require(len(following) == 1, 'branch in path')
            previous = path[-1]
            path.append(next(iter(following)))
        require(set(path) == component and len(path) == len(component), 'path coverage')
        paths.append(path)
    return sorted(paths), len(adjacency)


def read_certificate():
    rows = []
    for line in (HERE / 'path_types.tsv').read_text().splitlines():
        if line and not line.startswith('#'):
            n, count = map(int, line.split())
            require(n >= 2 and count > 0, 'path certificate row')
            rows.append((n, count))
    return rows
