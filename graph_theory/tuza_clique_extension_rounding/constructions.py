"""Exact elementary clique-extension constructions.

Affine designs are finite fixtures, not an implementation of the general
Kirkman existence theorem. Core dense completion is not implemented.
"""
from collections import Counter, deque
from fractions import Fraction
from itertools import combinations, product

from coloring import edge_color


def require(ok, message):
    if not ok:
        raise ValueError(message)


def affine_kirkman(dimension):
    require(type(dimension) is int and dimension >= 1, 'invalid dimension')
    points = list(product(range(3), repeat=dimension))
    index = {p: i for i, p in enumerate(points)}
    directions = [p for p in points if any(p) and next(x for x in p if x) == 1]
    classes = []
    for direction in directions:
        unseen = set(range(len(points)))
        blocks = []
        while unseen:
            a = min(unseen)
            block = tuple(sorted(index[tuple((x + t*y) % 3 for x, y in zip(points[a], direction))]
                                 for t in range(3)))
            blocks.append(block)
            unseen.difference_update(block)
        classes.append(blocks)
    return classes


def equitable_coloring(n, edges, palette_size):
    colored, stats = edge_color(n, edges)
    require(type(palette_size) is int and palette_size >= 1, 'invalid palette')
    require(all(c < palette_size for a, b, c in colored), 'palette too small')
    colors = {(a, b): c for a, b, c in colored}
    initial = list(colored)
    at = [dict() for _ in range(n)]
    classes = [set() for _ in range(palette_size)]
    for a, b, c in colored:
        at[a][c] = b
        at[b][c] = a
        classes[c].add((a, b))
    trace = []
    while True:
        hi = max(range(palette_size), key=lambda c: (len(classes[c]), -c))
        lo = min(range(palette_size), key=lambda c: (len(classes[c]), c))
        if len(classes[hi]) - len(classes[lo]) <= 1:
            break
        visited = set()
        chosen = None
        for seed in sorted(classes[hi]):
            if seed[0] in visited:
                continue
            stack = [seed[0]]
            component = set()
            while stack:
                a = stack.pop()
                if a in visited:
                    continue
                visited.add(a)
                for c in (hi, lo):
                    b = at[a].get(c)
                    if b is not None:
                        component.add((min(a, b), max(a, b)))
                        if b not in visited:
                            stack.append(b)
            excess = sum(1 if colors[e] == hi else -1 for e in component)
            if excess == 1:
                chosen = sorted(component)
                break
        require(chosen is not None, 'missing equitable recoloring path')
        old = [(a, b, colors[a, b]) for a, b in chosen]
        for a, b, c in old:
            del at[a][c]
            del at[b][c]
            classes[c].remove((a, b))
        for a, b, c in old:
            new = lo if c == hi else hi
            require(new not in at[a] and new not in at[b], 'improper equitable swap')
            colors[a, b] = new
            at[a][new] = b
            at[b][new] = a
            classes[new].add((a, b))
        trace.append((hi, lo, chosen))
    return {
        'initial': initial,
        'colored': [(a, b, colors[a, b]) for a, b in sorted(colors)],
        'trace': trace,
        'vizing_operations': stats,
    }


class Dinic:
    def __init__(self, n):
        self.graph = [[] for _ in range(n)]
        self.augmentations = 0

    def add(self, a, b, capacity):
        require(type(capacity) is int and capacity >= 0, 'invalid capacity')
        f = [b, len(self.graph[b]), capacity]
        r = [a, len(self.graph[a]), 0]
        self.graph[a].append(f)
        self.graph[b].append(r)
        return f

    def max_flow(self, source, sink):
        total = 0
        n = len(self.graph)
        while True:
            level = [-1] * n
            level[source] = 0
            queue = deque([source])
            while queue:
                a = queue.popleft()
                for b, rev, cap in self.graph[a]:
                    if cap and level[b] < 0:
                        level[b] = level[a] + 1
                        queue.append(b)
            if level[sink] < 0:
                return total
            cursor = [0] * n

            def augment(a, cap):
                if a == sink:
                    return cap
                while cursor[a] < len(self.graph[a]):
                    e = self.graph[a][cursor[a]]
                    b, rev, left = e
                    if left and level[b] == level[a] + 1:
                        sent = augment(b, min(cap, left))
                        if sent:
                            e[2] -= sent
                            self.graph[b][rev][2] += sent
                            return sent
                    cursor[a] += 1
                return 0

            while True:
                sent = augment(source, 10**30)
                if not sent:
                    break
                self.augmentations += 1
                total += sent


def allocate_spokes(available, columns, quota):
    """Integral bipartite rounding of row-normalized fractional edge weights."""
    require(type(columns) is int and columns >= 1, 'invalid column count')
    require(type(quota) is int and quota >= 0, 'invalid row quota')
    rows = len(available)
    require(rows > 0, 'empty row set')
    for neighbors in available:
        require(all(type(y) is int and 0 <= y < columns for y in neighbors), 'invalid spoke')
        require(quota <= len(neighbors), 'row quota infeasible')
    if quota == 0:
        return [set() for _ in available], {'augmentations': 0}
    fractions = [Fraction(0) for _ in range(columns)]
    for neighbors in available:
        weight = Fraction(quota, len(neighbors))
        for y in neighbors:
            fractions[y] += weight
    source, sink = rows + columns, rows + columns + 1
    super_source, super_sink = sink + 1, sink + 2
    network = Dinic(super_sink + 1)
    balance = [0] * (sink + 1)

    def bounded(a, b, low, high):
        require(0 <= low <= high, 'invalid lower bound')
        balance[a] -= low
        balance[b] += low
        return network.add(a, b, high-low)

    for x in range(rows):
        bounded(source, x, quota, quota)
    arcs = []
    for x, neighbors in enumerate(available):
        arcs.append([(y, bounded(x, rows+y, 0, 1)) for y in sorted(neighbors)])
    for y, value in enumerate(fractions):
        low = value.numerator // value.denominator
        high = -(-value.numerator // value.denominator)
        bounded(rows+y, sink, low, high)
    bounded(sink, source, 0, rows*quota)
    demand = 0
    for a, b in enumerate(balance):
        if b > 0:
            network.add(super_source, a, b)
            demand += b
        elif b < 0:
            network.add(a, super_sink, -b)
    require(network.max_flow(super_source, super_sink) == demand, 'fractional rounding flow failed')
    selected = [{y for y, arc in row if arc[2] == 0} for row in arcs]
    return selected, {'augmentations': network.augmentations}


def avoiding_matching(left, right, forbidden):
    """Exact augmenting matching; allowed pairs are the complement of forbidden."""
    left, right = sorted(left), sorted(right)
    require(len(left) == len(right) and len(set(left)) == len(left) and
            len(set(right)) == len(right) and not set(left).intersection(right), 'bad matching sides')
    n = len(left)
    position = {v: j for j, v in enumerate(right)}
    full = (1 << n)-1
    masks = []
    for u in left:
        bad = sum(1 << position[v] for v in forbidden.get(u, ()) if v in position)
        masks.append(full ^ bad)
    at_right = [-1] * n
    at_left = [-1] * n
    free = full
    repairs = 0
    for i, mask in enumerate(masks):
        choices = mask & free
        if choices:
            bit = choices & -choices
            j = bit.bit_length()-1
            free ^= bit
            at_right[j] = i
            at_left[i] = j
            continue
        repairs += 1
        queue = deque([i])
        seen_left = {i}
        seen_right = 0
        parent = {}
        end = None
        while queue and end is None:
            a = queue.popleft()
            choices = masks[a] & ~seen_right
            while choices:
                bit = choices & -choices
                choices ^= bit
                seen_right |= bit
                b = bit.bit_length()-1
                parent[b] = a
                old = at_right[b]
                if old < 0:
                    end = b
                    break
                if old not in seen_left:
                    seen_left.add(old)
                    queue.append(old)
        require(end is not None, 'no avoiding perfect matching')
        free &= ~(1 << end)
        while end >= 0:
            a = parent[end]
            old = at_left[a]
            at_left[a] = end
            at_right[end] = a
            end = old
    return [(left[i], right[j]) for i, j in enumerate(at_left)], repairs


def clique_stage(s, core_sizes, u, v_masses, design):
    """XXX and XXH triangles, with local core-center labels in the evidence."""
    require(s >= 1 and len(core_sizes) == len(v_masses), 'invalid clique stage')
    order = 3*len(design[0])
    require(s <= order <= s+5 and order % 6 == 3, 'design order outside padding bound')
    require(u >= 0 and all(v >= 0 for v in v_masses) and
            3*u+sum(v_masses) <= s*(s-1)//2, 'invalid clique capacity')
    require(all(n >= s for n in core_sizes), 'too few core colors')
    classes = (3*Fraction(u)) // order
    require(classes <= len(design), 'too many parallel classes')
    triangles = [t for parallel in design[:classes] for t in parallel if max(t) < s]
    used = {tuple(sorted(e)) for t in triangles for e in combinations(t, 2)}
    remainder = [e for e in combinations(range(s), 2) if e not in used]
    coloring, stats = edge_color(s, remainder)
    delta = max(Counter(v for e in remainder for v in e).values(), default=0)
    groups = []
    begin = 0
    for size, mass in zip(core_sizes, v_masses):
        count = (2*Fraction(mass)) // s
        require(begin+count <= delta+1, 'insufficient palette for groups')
        selected = [(a, b) for a, b, c in coloring if begin <= c < begin+count]
        cert = equitable_coloring(s, selected, size)
        cert.update({'palette_begin': begin, 'palette_count': count})
        groups.append(cert)
        begin += count
    return {'design_order': order, 'classes': classes, 'triangles': triangles,
            'remainder_coloring': coloring, 'groups': groups, 'vizing_operations': stats}


def construct_extension(core_sizes, loops, cross, s, u, v_masses, w_masses,
                        design, cutoff):
    """Construct only triangles meeting X; return all elementary certificates.

    A caller may use a smaller cutoff for a finite fixture. Such a fixture is
    a checked witness, not evidence that the universal cutoff can be lowered.
    """
    d = len(core_sizes)
    require(d == len(v_masses), 'wrong profile dimension')
    require(type(cutoff) is int and cutoff >= 1, 'invalid cutoff')
    offsets, total = [], 0
    for size in core_sizes:
        offsets.append(total)
        total += size
    supported = {(i, i) for i in loops} | {tuple(sorted(e)) for e in cross}
    require(set(w_masses) <= supported and all(w >= 0 for w in w_masses.values()), 'unsupported mass')
    for (i, j), mass in w_masses.items():
        capacity = core_sizes[i]*(core_sizes[i]-1)//2 if i == j else core_sizes[i]*core_sizes[j]
        require(mass <= capacity, 'core edge capacity exceeded')
    for i, size in enumerate(core_sizes):
        load = 2*v_masses[i] + sum((int(i == a)+int(i == b))*w
                                 for (a, b), w in w_masses.items())
        require(load <= s*size, 'spoke capacity exceeded')
    stage = clique_stage(s, core_sizes, u, v_masses, design)
    triangles = [tuple(total+x for x in t) for t in stage['triangles']]
    occupied = [[set() for _ in range(s)] for _ in range(d)]
    for i, group in enumerate(stage['groups']):
        for x, y, color in group['colored']:
            triangles.append((total+x, total+y, offsets[i]+color))
            occupied[i][x].add(color)
            occupied[i][y].add(color)
    quotas = {e: Fraction(mass) // s for e, mass in w_masses.items()}
    quotas = {e: q if q >= cutoff else 0 for e, q in quotas.items()}
    forbidden = {}
    allocations = []
    matching_repairs = 0
    for (i, j), quota in sorted(quotas.items(), key=lambda item: (item[1], item[0])):
        if quota == 0:
            continue
        selected = {}
        records = []
        for part, demand in ([(i, 2*quota)] if i == j else [(i, quota), (j, quota)]):
            available = [set(range(core_sizes[part]))-used for used in occupied[part]]
            assignment, operations = allocate_spokes(available, core_sizes[part], demand)
            selected[part] = assignment
            records.append({'part': part, 'demand': demand,
                            'selected': [sorted(row) for row in assignment], 'operations': operations})
            for x, row in enumerate(assignment):
                occupied[part][x].update(row)
        pairing = []
        for x in range(s):
            if i == j:
                both = sorted(offsets[i]+v for v in selected[i][x])
                left, right = both[:quota], both[quota:]
            else:
                left = [offsets[i]+v for v in selected[i][x]]
                right = [offsets[j]+v for v in selected[j][x]]
            matched, repairs = avoiding_matching(left, right, forbidden)
            matching_repairs += repairs
            pairing.append(matched)
            for a, b in matched:
                forbidden.setdefault(a, set()).add(b)
                forbidden.setdefault(b, set()).add(a)
                triangles.append((total+x, a, b))
        allocations.append({'edge_type': (i, j), 'quota': quota,
                            'spokes': records, 'pairings': pairing})
    return {'stage': stage, 'quotas': sorted(quotas.items()), 'allocations': allocations,
            'triangles': triangles, 'matching_repairs': matching_repairs}
