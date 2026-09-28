#!/usr/bin/env python3
"""Symbolic all-order certificate for the three-port edge-23 threshold."""

from heapq import heappop, heappush
from itertools import permutations

# Each edge form is (coefficient of r, of x, of y, constant), r=m-7.
EDGES = (
    (0, 1, (0, 0, 0, 1)), (1, 2, (0, 0, 0, 1)),
    (0, 6, (0, 0, 0, 1)), (0, 7, (0, 0, 0, 1)),
    (6, 5, (1, 0, 0, 1)), (5, 4, (0, 0, 0, 1)),
    (4, 3, (0, 0, 0, 1)), (1, 3, (0, 1, 0, 0)),
    (1, 5, (0, 0, 1, 0)),
)
# The skeleton vertices 6 and 7 denote q=m-1 and the pendant leaf t.
LANDMARKS = (2, 3, 5, 6, 7)


def add(a, b):
    return tuple(u + v for u, v in zip(a, b))


def subtract(a, b):
    return tuple(u - v for u, v in zip(a, b))


def path_forms(source, target):
    graph = [[] for _ in range(8)]
    for u, v, form in EDGES:
        graph[u].append((v, form))
        graph[v].append((u, form))
    answer = []

    def visit(u, seen, form):
        if u == target:
            answer.append(form)
            return
        for v, edge_form in graph[u]:
            if v not in seen:
                visit(v, seen | {v}, add(form, edge_form))

    visit(source, {source}, (0, 0, 0, 0))
    return answer


def negative_certificate():
    paths = 0
    minimum_slack = 10**9
    for dx in (0, 1):
        for dy in (0, 1):
            # x=r-dx and y=r-dy, with r>=3.
            def specialize(form):
                ar, ax, ay, const = form
                return ar + ax + ay, const - dx * ax - dy * ay

            rplusx = (1, -dx)
            rplusy = (1, -dy)
            matrix = (
                ((0, 0), add2(rplusx, (0, 1)), add2(rplusy, (0, 1)), (0, 3), (0, 3)),
                (add2(rplusx, (0, 1)), (0, 0), (0, 2), add2(rplusx, (0, 2)), add2(rplusx, (0, 2))),
                (add2(rplusy, (0, 1)), (0, 2), (0, 0), (1, 1), add2(rplusy, (0, 2))),
                ((0, 3), add2(rplusx, (0, 2)), (1, 1), (0, 0), (0, 2)),
                ((0, 3), add2(rplusx, (0, 2)), add2(rplusy, (0, 2)), (0, 2), (0, 0)),
            )
            for i in range(5):
                for j in range(i + 1, 5):
                    forms = [specialize(f) for f in path_forms(LANDMARKS[i], LANDMARKS[j])]
                    paths += len(forms)
                    target = matrix[i][j]
                    assert target in forms
                    for form in forms:
                        slope, intercept = add2(form, (-target[0], -target[1]))
                        assert slope >= 0 and 3 * slope + intercept >= 0
            for i, j, k in permutations(range(5), 3):
                slack = add2(add2(matrix[i][j], matrix[j][k]),
                             (-matrix[i][k][0], -matrix[i][k][1]))
                assert slack[0] >= 0 and 3 * slack[0] + slack[1] >= 1
                minimum_slack = min(minimum_slack, 3 * slack[0] + slack[1])
    return paths, minimum_slack


def add2(a, b):
    return a[0] + b[0], a[1] + b[1]


def positive_certificate():
    checked_paths = 0

    # Case A: x=r+1+b, y=r-1+c, r=3+a; a,b,c>=0.
    # P=t-0-1-2, Q=3-4-5-q.
    def case_a(form):
        cr, cx, cy, const = form
        return 3 * cr + 4 * cx + 2 * cy + const, cr + cx + cy, cx, cy

    for source, target, candidate in ((7, 2, (0, 0, 0, 3)),
                                      (3, 6, (1, 0, 0, 3))):
        expected = case_a(candidate)
        forms = path_forms(source, target)
        assert candidate in forms
        for form in forms:
            checked_paths += 1
            difference = subtract(case_a(form), expected)
            assert all(coefficient >= 0 for coefficient in difference)

    # Case B: x=r-d, d=0 or 1; y=r+1+c; r=3+a; a,c>=0.
    # P=t-0-q-5, Q=2-1-[x-ear]-3-4.
    for d in (0, 1):
        def case_b(form):
            cr, cx, cy, const = form
            return 3 * cr + (3 - d) * cx + 4 * cy + const, cr + cx + cy, cy

        for source, target, candidate in ((7, 5, (1, 0, 0, 3)),
                                          (2, 4, (0, 1, 0, 2))):
            expected = case_b(candidate)
            forms = path_forms(source, target)
            assert candidate in forms
            for form in forms:
                checked_paths += 1
                difference = subtract(case_b(form), expected)
                assert all(coefficient >= 0 for coefficient in difference)
    return checked_paths


def numerical_controls():
    """Independent Dijkstra/DAG checks near both sides of the threshold."""
    states = 0
    for m in range(10, 18):
        values = (m - 8, m - 7, m - 6, m - 5, None)
        n = m + 1
        target = (1 << n) - 1
        for x in values:
            for y in values:
                for z in (2, None):
                    graph = [[] for _ in range(n)]

                    def edge(u, v, length):
                        graph[u].append((v, length))
                        graph[v].append((u, length))

                    for i in range(m):
                        if i != 2:
                            edge(i, (i + 1) % m, 1)
                    edge(0, m, 1)
                    for u, v, length in ((1, 3, x), (1, 5, y), (3, 5, z)):
                        if length is not None:
                            edge(u, v, length)

                    traces = set()
                    for source in range(n):
                        distance = [10**9] * n
                        distance[source] = 0
                        queue = [(0, source)]
                        while queue:
                            du, u = heappop(queue)
                            if du != distance[u]:
                                continue
                            for v, length in graph[u]:
                                if du + length < distance[v]:
                                    distance[v] = du + length
                                    heappush(queue, (distance[v], v))

                        def visit(u, mask):
                            traces.add(mask)
                            for v, length in graph[u]:
                                if distance[u] + length == distance[v]:
                                    visit(v, mask | (1 << v))

                        visit(source, 1 << source)
                    actual = any((a | b) == target for a in traces for b in traces)
                    expected = x is None or y is None or max(x, y) >= m - 6
                    assert actual == expected, (m, x, y, z, actual)
                    states += 1
    return states


if __name__ == "__main__":
    negative_paths, slack = negative_certificate()
    positive_paths = positive_certificate()
    controls = numerical_controls()
    print(f"negative_affine_paths={negative_paths} min_strict_slack_r3={slack} "
          f"positive_affine_paths={positive_paths} finite_profiles={controls} PASS")
