"""Exact basis search and controls for finite-menu mass duality."""

from fractions import Fraction
from itertools import combinations, product
from math import factorial, lcm


def solve(rows, rhs):
    """Solve a square rational system; return None when its rows are dependent."""
    n = len(rhs)
    a = [[Fraction(x) for x in row] + [Fraction(rhs[i])] for i, row in enumerate(rows)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return None
        a[j], a[pivot] = a[pivot], a[j]
        scale = a[j][j]
        a[j] = [x / scale for x in a[j]]
        for i in range(n):
            if i != j:
                scale = a[i][j]
                a[i] = [x - scale * y for x, y in zip(a[i], a[j])]
    return tuple(row[-1] for row in a)


def find_dual(n, tuple_components):
    """Enumerate basic feasible dual vectors using exact arithmetic."""
    t = len(tuple_components)
    for s in range(1, min(t, n + 1) + 1):
        for support in combinations(range(t), s):
            norm = [1] * s
            vertex_rows = [tuple(2 * int(v in tuple_components[i]) for i in support) for v in range(n)]
            for active in combinations(range(n), s - 1):
                x = solve([norm] + [vertex_rows[v] for v in active], [1] * s)
                if x is None or any(z < 0 for z in x):
                    continue
                if any(sum(a * b for a, b in zip(row, x)) > 1 for row in vertex_rows):
                    continue
                den = lcm(*(z.denominator for z in x))
                answer = [0] * t
                for i, z in zip(support, x):
                    answer[i] = int(den * z)
                check_dual(n, tuple_components, answer)
                return tuple(answer)
    return None


def find_primal(n, tuple_components):
    """Enumerate basic feasible strictly heavy mass vectors exactly."""
    rows = [tuple(int(i == j) for i in range(n)) for j in range(n)]
    rows.extend(tuple(1 if v in c else -1 for v in range(n)) for c in tuple_components)
    for active in combinations(range(len(rows)), n):
        x = solve([rows[i] for i in active], [1] * n)
        if x is None or any(sum(a * b for a, b in zip(row, x)) < 1 for row in rows):
            continue
        den = lcm(*(z.denominator for z in x))
        masses = tuple(int(den * z) for z in x)
        check_primal(n, tuple_components, masses)
        return masses
    return None


def components(n, edges, deleted):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    remain = set(range(n)) - set(deleted)
    answer = []
    while remain:
        seed = min(remain)
        remain.remove(seed)
        seen = {seed}
        stack = [seed]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v in remain:
                    remain.remove(v)
                    seen.add(v)
                    stack.append(v)
        answer.append(frozenset(seen))
    return answer


def distances(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    all_d = []
    for source in range(n):
        d = [n + 1] * n
        d[source] = 0
        queue = [source]
        for u in queue:
            for v in adj[u]:
                if d[v] == n + 1:
                    d[v] = d[u] + 1
                    queue.append(v)
        all_d.append(d)
    return all_d


def check_dual(n, tuple_components, coefficients):
    assert len(tuple_components) == len(coefficients)
    assert all(x >= 0 for x in coefficients)
    total = sum(coefficients)
    assert 0 < total <= factorial(min(len(coefficients), n + 1)) * 2 ** (min(len(coefficients), n + 1) - 1)
    assert sum(x > 0 for x in coefficients) <= n + 1
    for v in range(n):
        assert 2 * sum(a for c, a in zip(tuple_components, coefficients) if v in c) <= total


def check_primal(n, tuple_components, masses):
    assert len(masses) == n
    assert all(1 <= x <= factorial(n) for x in masses)
    total = sum(masses)
    assert all(2 * sum(masses[v] for v in c) > total for c in tuple_components)


def fano_control():
    labels = list(range(1, 8))
    lines = sorted({frozenset((a, b, a ^ b)) for a, b in combinations(labels, 2)}, key=lambda x: tuple(sorted(x)))
    assert len(lines) == 7
    assert all(len(line) == 3 for line in lines)
    assert all(sum(v in line for line in lines) == 3 for v in labels)
    assert all(len(a & b) == 1 for a, b in combinations(lines, 2))

    edges = list(combinations(range(7), 2))
    d = distances(7, edges)
    component_tuple = []
    menus = []
    for line in lines:
        outside = sorted(labels.index(v) for v in set(labels) - set(line))
        paths = ((outside[0], outside[1]), (outside[2], outside[3]))
        assert all(d[u][v] == 1 for u, v in paths)
        deleted = set(paths[0] + paths[1])
        residual = components(7, edges, deleted)
        assert residual == [frozenset(labels.index(v) for v in line)]
        menus.append(deleted)
        component_tuple.extend(residual)
    check_dual(7, component_tuple, [1] * 7)
    found = find_dual(7, component_tuple)
    assert found is not None and sum(x > 0 for x in found) == 4
    assert find_primal(7, component_tuple) is None

    tested = 0
    for masses in product(range(3), repeat=7):
        total = sum(masses)
        assert any(all(2 * sum(masses[v] for v in c) <= total for c in components(7, edges, deleted)) for deleted in menus)
        tested += 1
    assert tested == 2187
    return len(lines), tested, found


def strict_majority_control():
    sets = [frozenset((0, 1)), frozenset((1, 2)), frozenset((0, 2))]
    check_primal(3, sets, (1, 1, 1))
    assert find_dual(3, sets) is None
    found = find_primal(3, sets)
    assert found is not None
    return len(sets), found


def small_system_audit():
    """Check every three-by-three set system against integer mass search."""
    subsets = [frozenset(v for v in range(3) if mask >> v & 1) for mask in range(8)]
    dual_count = primal_count = 0
    for system in product(subsets, repeat=3):
        dual = find_dual(3, system)
        primal = find_primal(3, system)
        brute_primal = any(
            all(2 * sum(masses[v] for v in c) > sum(masses) for c in system)
            for masses in product(range(1, factorial(3) + 1), repeat=3)
        )
        assert (primal is not None) == brute_primal
        assert (dual is not None) != brute_primal
        dual_count += dual is not None
        primal_count += primal is not None
    assert dual_count + primal_count == 512
    return dual_count, primal_count


if __name__ == "__main__":
    print("Fano lines and sampled mass vectors:", fano_control())
    print("strict-majority sets:", strict_majority_control())
    print("three-by-three systems (dual, primal):", small_system_audit())
    print("PASS")
