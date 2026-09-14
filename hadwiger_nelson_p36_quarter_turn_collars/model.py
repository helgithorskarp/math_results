"""Producer-side exact model for the P36 quarter-turn collar family."""

from __future__ import annotations

from collections import defaultdict


Vec = tuple[int, int, int, int]


def add(u: Vec, v: Vec) -> Vec:
    return tuple(a + b for a, b in zip(u, v))  # type: ignore[return-value]


def sub(u: Vec, v: Vec) -> Vec:
    return tuple(a - b for a, b in zip(u, v))  # type: ignore[return-value]


def rot(u: Vec) -> Vec:
    xr, xs, yr, ys = u
    return (-yr, -ys, xr, xs)


def rotk(u: Vec, k: int) -> Vec:
    for _ in range(k % 4):
        u = rot(u)
    return u


def half(u: Vec) -> Vec:
    if any(a % 2 for a in u):
        raise ValueError("nonintegral half in scaled coordinate model")
    return tuple(a // 2 for a in u)  # type: ignore[return-value]


def hexrot(u: Vec) -> Vec:
    """Multiplication by omega=(1+i*sqrt(3))/2."""
    xr, xs, yr, ys = u
    raw = (xr - 3 * ys, xs - yr, 3 * xs + yr, xr + ys)
    return half(raw)


def reflect(u: Vec) -> Vec:
    xr, xs, yr, ys = u
    return (xr, xs, -yr, -ys)


def canonical_center(center: Vec) -> Vec:
    orbit = []
    for seed in (center, reflect(center)):
        current = seed
        for _ in range(6):
            orbit.append(current)
            current = hexrot(current)
        if current != seed:
            raise AssertionError("hexagonal symmetry failed to close")
    return min(orbit)


def norm_coefficients(u: Vec) -> tuple[int, int]:
    """Coefficients (A,B) in 16*|u|^2=A+B*sqrt(3)."""
    xr, xs, yr, ys = u
    return (xr * xr + 3 * xs * xs + yr * yr + 3 * ys * ys,
            2 * (xr * xs + yr * ys))


def unit_vectors() -> tuple[Vec, ...]:
    answer = []
    for xr in range(-4, 5):
        for xs in range(-2, 3):
            for yr in range(-4, 5):
                for ys in range(-2, 3):
                    u = (xr, xs, yr, ys)
                    if norm_coefficients(u) == (16, 0):
                        answer.append(u)
    return tuple(sorted(answer))


def patch(limit: int = 36) -> tuple[list[tuple[int, int]], list[Vec]]:
    rows = []
    radius = int(limit ** 0.5) + 2
    for a in range(-2 * radius, 2 * radius + 1):
        for b in range(-2 * radius, 2 * radius + 1):
            if a * a + a * b + b * b <= limit:
                rows.append(((4 * a + 2 * b, 0, 0, 2 * b), (a, b)))
    rows.sort()
    return [label for _, label in rows], [point for point, _ in rows]


def center_from_pair(p: Vec, q: Vec) -> Vec:
    t = sub(p, rot(q))
    return half(add(t, rot(t)))


def all_centers(points: list[Vec]) -> list[Vec]:
    centers = [center_from_pair(p, q) for p in points for q in points]
    if len(set(centers)) != len(centers):
        raise AssertionError("anchor pairs do not give distinct centers")
    return sorted(centers)


def build_graph(center: Vec, points: list[Vec], units: tuple[Vec, ...]):
    layers = []
    labels_at: dict[Vec, list[tuple[int, int]]] = defaultdict(list)
    for layer in range(4):
        row = []
        for index, point in enumerate(points):
            image = add(center, rotk(sub(point, center), layer))
            row.append(image)
            labels_at[image].append((layer, index))
        layers.append(row)
    physical = sorted(labels_at)
    where = {point: index for index, point in enumerate(physical)}
    unit_set = set(units)
    edges = set()
    for index, point in enumerate(physical):
        for displacement in unit_set:
            other = where.get(add(point, displacement))
            if other is not None and index < other:
                edges.add((index, other))
    layer_masks = []
    for point in physical:
        mask = 0
        for layer, _ in labels_at[point]:
            mask |= 1 << layer
        layer_masks.append(mask)
    return {
        "layers": layers,
        "labels_at": labels_at,
        "physical": physical,
        "where": where,
        "edges": edges,
        "layer_masks": layer_masks,
    }


class ParityDSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.parity = [0] * n

    def find(self, x: int) -> tuple[int, int]:
        if self.parent[x] != x:
            root, bit = self.find(self.parent[x])
            self.parity[x] ^= bit
            self.parent[x] = root
        return self.parent[x], self.parity[x]

    def join(self, x: int, y: int, value: int) -> bool:
        rx, px = self.find(x)
        ry, py = self.find(y)
        if rx == ry:
            return (px ^ py) == value
        self.parent[rx] = ry
        self.parity[rx] = px ^ py ^ value
        return True

    def assignment(self) -> list[int]:
        return [self.find(x)[1] for x in range(len(self.parent))]


def residue_colouring(graph, labels: list[tuple[int, int]]) -> list[int] | None:
    residues = [(a - b) % 3 for a, b in labels]
    signs = [int(residue == 2) for residue in residues]
    sign = ParityDSU(4)
    zero = ParityDSU(4)
    valid = True

    def constrain(left: tuple[int, int], right: tuple[int, int], equal: bool) -> None:
        nonlocal valid
        layer1, index1 = left
        layer2, index2 = right
        zero1 = residues[index1] == 0
        zero2 = residues[index2] == 0
        if equal:
            if zero1 != zero2:
                valid = False
            elif zero1:
                valid &= zero.join(layer1, layer2, 0)
            else:
                valid &= sign.join(layer1, layer2, signs[index1] ^ signs[index2])
        elif zero1 == zero2:
            if zero1:
                valid &= zero.join(layer1, layer2, 1)
            else:
                valid &= sign.join(
                    layer1, layer2, 1 ^ signs[index1] ^ signs[index2])

    for point in graph["physical"]:
        occurrences = graph["labels_at"][point]
        for other in occurrences[1:]:
            constrain(occurrences[0], other, True)
    for x, y in graph["edges"]:
        left = graph["labels_at"][graph["physical"][x]][0]
        right = graph["labels_at"][graph["physical"][y]][0]
        constrain(left, right, False)

    if not valid:
        return None
    sign_bits = sign.assignment()
    zero_bits = zero.assignment()
    word = []
    for point in graph["physical"]:
        layer, index = graph["labels_at"][point][0]
        if residues[index] == 0:
            word.append(zero_bits[layer])
        else:
            word.append(2 + (sign_bits[layer] ^ signs[index]))
    validate_colouring(word, graph["edges"])
    return word


def validate_colouring(word: list[int], edges: set[tuple[int, int]]) -> None:
    if not word or any(colour not in range(4) for colour in word):
        raise ValueError("invalid four-colour word")
    for x, y in edges:
        if word[x] == word[y]:
            raise ValueError("monochromatic unit edge")


def four_colouring(vertices: int, edges: set[tuple[int, int]],
                    triangle: tuple[int, int, int]) -> tuple[list[int] | None, int]:
    adjacency = [set() for _ in range(vertices)]
    for x, y in edges:
        adjacency[x].add(y)
        adjacency[y].add(x)
    domains = [15] * vertices
    for colour, vertex in enumerate(triangle):
        domains[vertex] = 1 << colour
    nodes = 0

    def visit(current: list[int]) -> list[int] | None:
        nonlocal nodes
        nodes += 1
        queue = [v for v, domain in enumerate(current)
                 if domain and domain & (domain - 1) == 0]
        propagated: set[int] = set()
        while queue:
            v = queue.pop()
            if v in propagated:
                continue
            propagated.add(v)
            for w in adjacency[v]:
                domain = current[w] & ~current[v]
                if domain != current[w]:
                    if not domain:
                        return None
                    current[w] = domain
                    if domain & (domain - 1) == 0:
                        queue.append(w)
        pending = [v for v, domain in enumerate(current)
                   if domain & (domain - 1)]
        if not pending:
            word = [domain.bit_length() - 1 for domain in current]
            validate_colouring(word, edges)
            return word
        v = min(pending, key=lambda w: (current[w].bit_count(),
                                        -len(adjacency[w]), w))
        for colour in range(4):
            if current[v] & (1 << colour):
                child = current.copy()
                child[v] = 1 << colour
                answer = visit(child)
                if answer is not None:
                    return answer
        return None

    return visit(domains), nodes
