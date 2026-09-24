"""Exact finite constructions used in PROOF.md; no design-existence oracle."""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, permutations
from math import ceil, comb, floor


def require(ok, message):
    if not ok:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def incidence(pattern):
    return Counter(edge(a, b) for a, b in combinations(pattern, 2))


def triangles(d, support):
    return [t for t in combinations_with_replacement(range(d), 3)
            if set(incidence(t)) <= set(support)]


def boolean_support():
    return sorted(set(combinations_with_replacement(range(8), 2)) |
                  {(i, 8 + j) for j in range(3) for i in range(8) if i >> j & 1})


def capacities(sizes, support):
    return {e: (comb(sizes[e[0]], 2) if e[0] == e[1]
                else sizes[e[0]] * sizes[e[1]]) for e in support}


def local_vector(pattern, i):
    """Incident type degrees at one role of type i, including repeated types."""
    p = list(pattern)
    p.remove(i)
    return Counter(edge(i, j) for j in p)


def compressed_roles(sizes, support, profile, alpha):
    """Prefix quotient/remainder allocation; no list of N vertices is allocated."""
    d, N = len(sizes), sum(sizes)
    M = comb(d + 2, 3) + comb(d + 1, 2)
    lam = 8 * M / Q(alpha)
    U = ceil(lam + 4 * M)
    counts = {p: floor((1 - lam / N) * z) for p, z in profile.items() if z}
    require(all(m > 0 for m in counts.values()), 'order too small for roles')
    blocks = []
    for i, n in enumerate(sizes):
        div = {p: divmod(m * p.count(i), n) for p, m in counts.items() if i in p}
        breaks = sorted({0, n} | {r for q, r in div.values()})
        rows = []
        for lo, hi in zip(breaks, breaks[1:]):
            roles = {p: q + int(lo < r) for p, (q, r) in div.items()}
            degree = Counter()
            for p, count in roles.items():
                for e, value in local_vector(p, i).items():
                    degree[e] += count * value
            deficit = {e: (n - 1 if e == (i, i) else sizes[e[1] if e[0] == i else e[0]])
                       - degree[e] for e in support if i in e}
            rows.append({'start': lo, 'stop': hi, 'roles': roles,
                         'degree': dict(degree), 'deficit': deficit})
        blocks.append(rows)
    return {'M': M, 'lambda': lam, 'U': U, 'counts': counts, 'blocks': blocks}


def realize_simple(degrees):
    """Havel-Hakimi producer; the checker inspects every resulting edge."""
    residual = list(degrees)
    result = []
    while any(residual):
        order = sorted(range(len(residual)), key=lambda i: (-residual[i], i))
        v, others = order[0], order[1:]
        value = residual[v]
        require(0 <= value <= len(others), 'nongraphical simple list')
        residual[v] = 0
        for w in others[:value]:
            require(residual[w] > 0, 'nongraphical simple residual')
            residual[w] -= 1
            result.append(edge(v, w))
    return result


def realize_bipartite(left, right):
    residual = list(right)
    result = []
    for v in sorted(range(len(left)), key=lambda i: (-left[i], i)):
        order = sorted(range(len(right)), key=lambda j: (-residual[j], j))
        require(0 <= left[v] <= len(order), 'nongraphical bipartite list')
        for w in order[:left[v]]:
            require(residual[w] > 0, 'nongraphical bipartite residual')
            residual[w] -= 1
            result.append((v, w))
    require(not any(residual), 'unequal bipartite sums')
    return result


def split_lattice(core, d, support, target):
    """Signed triangle coefficients, or failure of the stated congruences."""
    support = set(support)
    require(core > 0, 'empty core')
    b = Counter({e: target.get(e, 0) for e in support})
    require(all(type(x) is int for x in b.values()), 'noninteger lattice target')
    require(sum(b.values()) % 3 == 0, 'edge sum not divisible by three')
    require(all(sum(v * e.count(i) for e, v in b.items()) % 2 == 0
                for i in range(d)), 'odd type degree')
    coefficients = Counter()

    def subtract(t, z):
        t = tuple(sorted(t))
        require(set(incidence(t)) <= support, 'unsupported triangle')
        coefficients[t] += z
        for e, a in incidence(t).items():
            b[e] -= z * a

    for h in range(core, d):
        neighbors = [i for i in range(core) if edge(i, h) in support]
        require(neighbors, 'isolated independent type')
        p = neighbors[0]
        for j in neighbors[1:]:
            subtract((h, p, j), b[edge(h, j)])
        require(b[edge(h, p)] % 2 == 0, 'independent parity failure')
        subtract((h, p, p), b[edge(h, p)] // 2)
    for i, j in combinations(range(1, core), 2):
        subtract((0, i, j), b[(i, j)])
    for i in range(1, core):
        require(b[(0, i)] % 2 == 0, 'core parity failure')
        subtract((0, i, i), b[(0, i)] // 2)
    for i in range(1, core):
        z = b[(i, i)]
        subtract((0, i, i), z)
        subtract((0, 0, i), -z)
    require(b[(0, 0)] % 3 == 0, 'final loop congruence failure')
    subtract((0, 0, 0), b[(0, 0)] // 3)
    require(not any(b.values()), 'lattice elimination incomplete')
    return {t: z for t, z in coefficients.items() if z}


def singleton_lattice(core, i, target):
    """Every even-sum incident vector in a split template, with signed roles."""
    require(sum(target.values()) % 2 == 0, 'odd singleton degree')
    p = i if i < core else min(j for e in target for j in e if j != i)
    pivot = edge(i, p)
    remainder = target[pivot]
    result = Counter()
    for e, value in target.items():
        if e != pivot:
            j = e[1] if e[0] == i else e[0]
            result[tuple(sorted((i, p, j)))] += value
            remainder -= value
    require(remainder % 2 == 0, 'singleton parity failure')
    result[tuple(sorted((i, p, p)))] += remainder // 2
    return {t: z for t, z in result.items() if z}


def split_right_inverse(support, core):
    """Column e is a rational triangle vector mapping exactly to edge unit e."""
    columns = {}
    for e in support:
        i, j = e
        if i == j:
            columns[e] = {(i, i, i): Q(1, 3)}
        else:
            if i >= core:
                i, j = j, i
            require(i < core, 'no clique endpoint')
            columns[e] = {tuple(sorted((i, i, j))): Q(1, 2), (i, i, i): Q(-1, 6)}
    return columns


def literal_host(sizes, support):
    parent = [i for i, n in enumerate(sizes) for _ in range(n)]
    support = set(support)
    edges = {e for e in combinations(range(len(parent)), 2)
             if edge(parent[e[0]], parent[e[1]]) in support}
    return parent, edges


def split_cleanup(sizes, support, core):
    parent, original = literal_host(sizes, support)
    core_vertices = [v for v, i in enumerate(parent) if i < core]
    independent = [v for v, i in enumerate(parent) if i >= core]
    degree = Counter(v for e in original for v in e)
    removed = set()
    load = Counter()

    def remove(e):
        require(e in original and e not in removed, 'invalid cleanup edge')
        removed.add(e)
        for v in e:
            degree[v] -= 1

    for v in independent:
        if degree[v] % 2:
            neighbors = [w for w in core_vertices if edge(v, w) in original]
            w = min(neighbors, key=lambda x: (load[x], x))
            remove(edge(v, w))
            load[w] += 1
    odd = [v for v in core_vertices if degree[v] % 2]
    require(len(odd) % 2 == 0, 'odd core defect count')
    for a, b in zip(odd[::2], odd[1::2]):
        remove(edge(a, b))
    residue = (len(original) - len(removed)) % 3
    if residue:
        length = 3 + residue
        chosen = core_vertices[:length]
        require(len(chosen) == length, 'core too small for cycle')
        for order in permutations(chosen[1:]):
            cycle = [chosen[0]] + list(order)
            cycle_edges = [edge(cycle[j], cycle[(j + 1) % length]) for j in range(length)]
            if all(e in original and e not in removed for e in cycle_edges):
                for e in cycle_edges:
                    remove(e)
                break
        else:
            raise ValueError('no cleanup cycle')
    return parent, original, removed


def tag_edges(m, N):
    a = (m + N - 1) // N
    deleted = {(j % a, j) for j in range(a * N - m)}
    return a, {(i, j) for i in range(a) for j in range(N)} - deleted
