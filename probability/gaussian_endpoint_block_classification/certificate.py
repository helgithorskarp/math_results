#!/usr/bin/env python3
"""Exact endpoint-block producer; see PROOF.md for its mathematical scope."""
import argparse
from fractions import Fraction as F
import heapq
import json
from pathlib import Path


def rational(x):
    if type(x) is int or isinstance(x, str):
        return F(x)
    raise ValueError('Coordinates must be integers or rational strings')


def points(raw):
    if not isinstance(raw, list) or not raw:
        raise ValueError('A nonempty point list is required')
    if any(not isinstance(p, list) or len(p) != 3 for p in raw):
        raise ValueError('Each point has three coordinates')
    return [tuple(map(rational, p)) for p in raw]


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def d2(a, b):
    return dot(sub(a, b), sub(a, b))


def read_input(data):
    if not isinstance(data, dict) or set(data) != {'source', 'target'}:
        raise ValueError('Input has exactly source and target fields')
    p, q = points(data['source']), points(data['target'])
    if len(p) != len(q):
        raise ValueError('Endpoint label counts differ')
    if len(set(p)) != len(p):
        raise ValueError('Merge repeated source atoms before using this producer')
    for i in range(len(p)):
        for j in range(i):
            if d2(q[i], q[j]) > d2(p[i], p[j]):
                raise ValueError('Endpoints are not a contraction')
    return p, q


def rref(rows, columns):
    a = [list(row) for row in rows]
    pivots = []
    r = 0
    for c in range(columns):
        k = next((k for k in range(r, len(a)) if a[k][c]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        z = a[r][c]
        a[r] = [v/z for v in a[r]]
        for k in range(len(a)):
            if k != r and a[k][c]:
                z = a[k][c]
                a[k] = [v-z*w for v, w in zip(a[k], a[r])]
        pivots.append(c)
        r += 1
        if r == len(a):
            break
    return a, pivots


def rank(rows, columns):
    return len(rref(rows, columns)[1])


def determinant(rows):
    a = [list(row) for row in rows]
    value = F(1)
    for c in range(len(a)):
        k = next((k for k in range(c, len(a)) if a[k][c]), None)
        if k is None:
            return F(0)
        if k != c:
            a[c], a[k] = a[k], a[c]
            value = -value
        pivot = a[c][c]
        value *= pivot
        for k in range(c+1, len(a)):
            z = a[k][c]/pivot
            a[k] = [v-z*w for v, w in zip(a[k], a[c])]
    return value


def block_certificate(p, q, indices):
    rows = [list(sub(q[i], p[i])) for i in indices]
    b = [(dot(q[i], q[i])-dot(p[i], p[i]))/2 for i in indices]
    reduced, pivots = rref(rows, 3)
    if len(pivots) <= 2:
        free = next(c for c in range(3) if c not in pivots)
        normal = [F(0)]*3
        normal[free] = F(1)
        for r, c in enumerate(pivots):
            normal[c] = -reduced[r][free]
        return dict(indices=indices, kind='DISPLACEMENT_PLANE',
                    normal=list(map(str, normal)), rank=len(pivots))
    augmented = [row+[value] for row, value in zip(rows, b)]
    reduced, ap = rref(augmented, 4)
    if len(ap) == 3:
        anchor = [reduced[i][3] for i in range(3)]
        return dict(indices=indices, kind='COMMON_ANCHOR',
                    anchor=list(map(str, anchor)), rank=3)
    selected = []
    for k, row in enumerate(augmented):
        trial = [augmented[j] for j in selected]+[row]
        if rank(trial, 4) > len(selected):
            selected.append(k)
        if len(selected) == 4:
            break
    minor = determinant([augmented[j] for j in selected])
    if not minor:
        raise RuntimeError('Missing inconsistency minor')
    return dict(indices=indices, kind='NOT_COVERED', rank=3,
                augmented_rank=4, minor_indices=[indices[j] for j in selected],
                augmented_minor=str(minor))


def precedence(p, q):
    moved = [i for i in range(len(p)) if p[i] != q[i]]
    edges = {i: set() for i in moved}
    for k, i in enumerate(moved):
        for j in moved[:k]:
            lo, hi = d2(q[i], q[j]), d2(p[i], p[j])
            if not lo <= d2(q[i], p[j]) <= hi:
                edges[j].add(i)  # i cannot switch strictly before j
            if not lo <= d2(p[i], q[j]) <= hi:
                edges[i].add(j)
    return moved, edges


def components(vertices, edges):
    # Iterative Kosaraju; canonical topological order of the quotient.
    seen, order = set(), []
    for start in vertices:
        if start in seen:
            continue
        stack = [(start, False)]
        while stack:
            u, leaving = stack.pop()
            if leaving:
                order.append(u)
            elif u not in seen:
                seen.add(u)
                stack.append((u, True))
                stack.extend((v, False) for v in sorted(edges[u], reverse=True)
                             if v not in seen)
    rev = {u: set() for u in vertices}
    for u in vertices:
        for v in edges[u]:
            rev[v].add(u)
    used, groups = set(), []
    for start in reversed(order):
        if start in used:
            continue
        group, stack = [], [start]
        used.add(start)
        while stack:
            u = stack.pop()
            group.append(u)
            for v in sorted(rev[u]):
                if v not in used:
                    used.add(v)
                    stack.append(v)
        groups.append(sorted(group))
    owner = {v: k for k, group in enumerate(groups) for v in group}
    outgoing = [set() for _ in groups]
    degree = [0]*len(groups)
    for u in vertices:
        for v in edges[u]:
            a, b = owner[u], owner[v]
            if a != b and b not in outgoing[a]:
                outgoing[a].add(b)
                degree[b] += 1
    ready = [(min(groups[k]), k) for k in range(len(groups)) if not degree[k]]
    heapq.heapify(ready)
    answer = []
    while ready:
        _, k = heapq.heappop(ready)
        answer.append(groups[k])
        for j in outgoing[k]:
            degree[j] -= 1
            if not degree[j]:
                heapq.heappush(ready, (min(groups[j]), j))
    if len(answer) != len(groups):
        raise RuntimeError('Condensation graph is not acyclic')
    return answer


def produce(data):
    p, q = read_input(data)
    moved, edges = precedence(p, q)
    groups = components(moved, edges)
    blocks = [block_certificate(p, q, group) for group in groups]
    covered = all(b['kind'] != 'NOT_COVERED' for b in blocks)
    return dict(status='CERTIFIED' if covered else 'NOT_COVERED',
                labels=len(p), moved_labels=moved,
                minimum_maximum_switch_batch=max(map(len, groups), default=0),
                precedence_edges=[[i,j] for i in moved for j in sorted(edges[i])],
                blocks=blocks,
                meaning=('All priors, Gaussian variances and hinges; both arbitrary-radius '
                         'ball-volume inequalities.' if covered else
                         'This endpoint-switch certificate fails. No Gaussian counterexample '
                         'or exclusion of other methods is asserted.'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    print(json.dumps(produce(json.loads(args.input.read_text())), indent=2))


if __name__ == '__main__':
    main()
