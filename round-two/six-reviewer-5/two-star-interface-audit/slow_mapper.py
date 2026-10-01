"""Unchanged compatible_maps function from six-reviewer-5 uniform-tail-audit.
Source commit f82510e90fbb225aed45d7c833858618aafe2e35. Only the function
and its required imports/guards are retained. Used as a control, never
as the full new carrier computation. Source credit is in INPUTS.json.
"""
from collections import Counter
from itertools import combinations, permutations
from math import factorial
import time

def require(ok, message):
    if not ok:
        raise ValueError(message)

class Incomplete(RuntimeError):
    pass

def compatible_maps(Q, P, f, s, nodes=200000, seconds=10):
    """Every common-tail preserving injection; early conflicts count suffixes.

    Q is first-center star, P second-center star. First center is label17;
    first-star label a is the second center and is excluded from image(P).
    """
    require(type(nodes) is int and 0 <= nodes <= 200000 and 0 < seconds <= 10, 'finite guard domain')
    _, u, a, v = f
    _, up, vp, b, *_ = s
    source = sorted((tuple(sorted(w-{b})) for w in P if b in w))
    target = sorted((tuple(sorted(w-{a})) for w in Q if a in w))
    m = len(source)
    require(m == len(target) and m in (4, 5), 'common word count')
    require(len(set().union(*(set(t) for t in source))) == 3*m and
            len(set().union(*(set(t) for t in target))) == 3*m, 'disjoint common tails')
    si = next(i for i, tail in enumerate(source) if up in tail)
    ti = next(i for i, tail in enumerate(target) if u in tail)
    require(all(vp not in tail for tail in source) and all(v not in tail for tail in target),
            'uncovered center/v triple')
    common_source, common_target = set().union(*(set(t) for t in source)), set().union(*(set(t) for t in target))
    residual_source = sorted(set(range(17))-common_source-{b, vp})
    residual_target = sorted(set(range(18))-common_target-{17, a, v})
    require(len(residual_source) == len(residual_target), 'residual bijection count')
    private_first = tuple(w | {17} for w in Q if a not in w)
    private_second = tuple(w for w in P if b not in w)
    owner = {tuple(t): wi for wi, w in enumerate(private_first) for t in combinations(sorted(w), 3)}
    triples = tuple((wi, t) for wi, w in enumerate(private_second) for t in combinations(sorted(w), 3))
    current = {b: 17, up: u, vp: v}
    require(len(current) == 3 and len(set(current.values())) == 3, 'distinct fixed points')
    total = 2 * factorial(m-1) * 6**(m-1) * factorial(len(residual_source))
    visited, rejected, completed = 0, 0, 0
    hits = Counter()
    solutions = []
    started = time.monotonic()

    def inspect(weight, stage):
        nonlocal visited, rejected
        visited += 1
        if visited > nodes or time.monotonic()-started > seconds:
            raise Incomplete('INCOMPLETE local point-map verification')
        for wi, t in triples:
            if all(a in current for a in t):
                image = tuple(sorted(current[a] for a in t))
                if image in owner:
                    # t lies in an actual source word and image in an actual
                    # first-center word; no numerical or heuristic pruning.
                    rejected += weight
                    hits[stage] += 1
                    return False
        return True

    remaining = [source[i] for i in range(m) if i != si]
    targets = [target[i] for i in range(m) if i != ti]

    def visit(depth, available):
        nonlocal completed
        left = len(remaining)-depth
        weight = factorial(left) * 6**left * factorial(len(residual_source))
        if not inspect(weight, str(depth)):
            return
        if left:
            source_tail = remaining[depth]
            for k in available:
                for image in permutations(targets[k]):
                    current.update(zip(source_tail, image))
                    visit(depth+1, tuple(j for j in available if j != k))
                    for point in source_tail:
                        del current[point]
            return
        for image in permutations(residual_target):
            current.update(zip(residual_source, image))
            if inspect(1, 'residual'):
                require(len(current) == len(set(current.values())) == 17 and
                        set(current.values()) == set(range(18))-{a}, 'full point injection')
                family = set(tuple(sorted(w)) for w in (Qw | {17} for Qw in Q))
                family |= {tuple(sorted([a] + [current[x] for x in w])) for w in P}
                require(all(len(set(x) & set(y)) <= 2 for x, y in combinations(family, 2)),
                        'complete solution literal family')
                solutions.append(tuple(current[x] for x in range(17)))
                completed += 1
            for x in residual_source:
                del current[x]

    if inspect(total, 'fixed'):
        for image in permutations(sorted(set(target[ti])-{u})):
            unmapped = sorted(set(source[si])-{up})
            current.update(zip(unmapped, image))
            visit(0, tuple(range(len(targets))))
            for x in unmapped:
                del current[x]
    require(rejected+completed == total, 'exact full-domain accounting')
    return dict(full_maps=total, collision_maps=rejected, solutions=solutions, nodes=visited,
                prunes=dict(sorted(hits.items())))
