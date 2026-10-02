"""Exact producer for single-class eraser graphs; not the literal verifier."""

from collections import deque
from math import gcd


def divisors(number):
    if type(number) is not int or number < 1:
        raise ValueError("positive integer cofactor required")
    return [d for d in range(1, number + 1) if number % d == 0]


def signature(cofactor, points):
    if not points or len(set(points)) != len(points):
        raise ValueError("nonempty distinct cofactor points required")
    if any(type(x) is not int or not 0 <= x < cofactor for x in points):
        raise ValueError("cofactor point outside canonical range")
    result = cofactor
    for x in points:
        result = gcd(result, x - points[0])
    return result


def eraser_graph(cofactor, fibers, resources, copies):
    if type(copies) is not int or copies < 1:
        raise ValueError("positive integer copy count required")
    if resources != sorted(set(resources)):
        raise ValueError("resource labels must be distinct and sorted")
    if any(type(d) is not int or d < 1 or cofactor % d for d in resources):
        raise ValueError("invalid cofactor resource")
    signatures = [signature(cofactor, v) for v in fibers]
    return [[d for d in resources if g % d == 0]
            for g in signatures for _ in range(copies)]


def matching_certificate(graph, resources):
    """Augmenting paths, followed by an alternating-path vertex cover."""
    if resources != sorted(set(resources)):
        raise ValueError("invalid resource labels")
    if any(row != sorted(set(row)) or not set(row) <= set(resources)
           for row in graph):
        raise ValueError("invalid adjacency")
    right_match = {}

    def augment(left, seen):
        for right in graph[left]:
            if right in seen:
                continue
            seen.add(right)
            if right not in right_match or augment(right_match[right], seen):
                right_match[right] = left
                return True
        return False

    for left in range(len(graph)):
        augment(left, set())
    left_match = {left: right for right, left in right_match.items()}
    reached_left = set(range(len(graph))) - set(left_match)
    reached_right = set()
    queue = deque(sorted(reached_left))
    while queue:
        left = queue.popleft()
        for right in graph[left]:
            if left_match.get(left) == right or right in reached_right:
                continue
            reached_right.add(right)
            if right in right_match and right_match[right] not in reached_left:
                reached_left.add(right_match[right])
                queue.append(right_match[right])
    return {
        "matching": sorted([[left, right] for right, left in right_match.items()]),
        "cover_left": sorted(set(range(len(graph))) - reached_left),
        "cover_right": sorted(reached_right),
        "value": len(right_match),
    }


def weighted_cover(cofactor, fibers, resources, prime):
    """Minimum two-layer cover, enumerating parent subsets (Lemma 3)."""
    rows = eraser_graph(cofactor, fibers, resources, 1)
    best = None
    for included in range(1 << len(rows)):
        right = set()
        for i, row in enumerate(rows):
            if included & (1 << i):
                right.update(row)
        left = [prime * i + j for i in range(len(rows))
                if not included & (1 << i) for j in range(prime)]
        value = 2 * prime * len(left) + (prime + 1) * len(right)
        candidate = (value, included, left, sorted(right))
        if best is None or candidate[:2] < best[:2]:
            best = candidate
    return {"cover_left": best[2], "cover_right": best[3],
            "value": best[0], "parent_subset": best[1]}


def crt(prefix, power, phase, divisor):
    if gcd(power, divisor) != 1:
        raise ValueError("CRT factors must be coprime")
    return (prefix + power * (((phase - prefix) * pow(power, -1, divisor))
                              % divisor)) % (power * divisor)
