"""Group-free independent local charge obstruction, six-reviewer-5.

Credit the generic twenty-star fixture coverage; ignore every supplied group.
Enumerate raw first/second markings. Recursively map common tails and prune
only actual three-point collisions. Count every pruned full-map cylinder.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
from math import factorial
from pathlib import Path
import argparse
import json
import resource
import time

HERE = Path(__file__).resolve().parent
FIXTURE_SHA = 'c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encode(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':'))+'\n').encode()


class Incomplete(RuntimeError):
    pass


def star(raw):
    require(len(raw) == 20 and all(len(w) == len(set(w)) == 4 and
            all(type(a) is int and 0 <= a < 17 for a in w) for w in raw), 'twenty-star domain')
    words = tuple(frozenset(w) for w in raw)
    require(len(set(words)) == 20 and all(len(a & b) <= 1 for a, b in combinations(words, 2)),
            'twenty-star pair packing')
    rho = tuple(sum(a in w for w in words) for a in range(17))
    high = frozenset(a for a in range(17) if rho[a] < 5)
    require(max(rho) <= 5 and sum(5-r for r in rho) == 5, 'twenty-star deficit')
    leave = frozenset(frozenset((a, b)) for a, b in combinations(range(17), 2)
                      if not any(a in w and b in w for w in words))
    core = frozenset(e for e in leave if e <= high)
    require(all(e & high for e in leave) and len(core) == len(high)-1, 'universal high leave')
    return words, rho, high, leave, core


def raw_marks():
    raw = (HERE/'TWENTY_STARS.json').read_bytes()
    require(sha256(raw).hexdigest() == FIXTURE_SHA, 'twenty-star fixture integrity')
    data = json.loads(raw)
    require(len(data['stars']) == 23, 'all credited generic fixtures')
    stars, first, second = [], [], []
    for i, row in enumerate(data['stars']):
        words, rho, high, leave, core = star(row)
        stars.append(words)
        for u in sorted(high):
            if rho[u] in (3, 4) and all(u not in e for e in core) and all(rho[a] == 4 for a in high-{u}):
                for a in sorted(high-{u}):
                    for v in range(17):
                        if rho[v] == 5 and frozenset((a, v)) in leave:
                            first.append((i, u, a, v))
        for u, v, b in permutations(sorted(high), 3):
            if any(rho[a] != 4 for a in high-{u}):
                continue
            eu = sum(u in e for e in core)
            if eu > 1 or frozenset((u, v)) in leave or frozenset((u, b)) in leave:
                continue
            if frozenset((v, b)) in core:
                second.append((i, u, v, b, eu))
    require(len(first) == 14 and len(second) == 32, 'complete raw mark domain')
    return stars, sorted(first), sorted(second)


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


def positive_control():
    data = json.loads((HERE/'positive_joint.json').read_text())
    family = [frozenset(a for a in range(18) if mask >> a & 1) for mask in data['word_masks']]
    require(len(family) == len(set(family)) == 35 and all(len(w) == 5 for w in family), 'positive family shape')
    require(all(len(w & z) <= 2 for w, z in combinations(family, 2)), 'positive literal packing')
    degrees = [sum(a in w for w in family) for a in range(18)]
    x, y = [a for a in range(18) if degrees[a] == 20]
    C = set().union(*(w-{x, y} for w in family if {x, y} <= w))
    v = next(iter(set(range(18))-{x, y}-C))
    u = min(C)
    qlabels, plabels = sorted(set(range(18))-{x}), sorted(set(range(18))-{y})
    qi, pi = {a: k for k, a in enumerate(qlabels)}, {a: k for k, a in enumerate(plabels)}
    Q = tuple(frozenset(qi[a] for a in w-{x}) for w in family if x in w)
    P = tuple(frozenset(pi[a] for a in w-{y}) for w in family if y in w)
    f, s = (0, qi[u], qi[y], qi[v]), (0, pi[u], pi[v], pi[x], 0)
    record = compatible_maps(Q, P, f, s)
    literal = tuple(qi[plabels[k]] if plabels[k] != x else 17 for k in range(17))
    require(literal in record['solutions'] and record['solutions'], 'known actual positive point map')
    rejected = []
    for name, kwargs, exception in [('zero nodes', {'nodes': 0}, Incomplete),
                                     ('excess nodes', {'nodes': 200001}, ValueError),
                                     ('excess seconds', {'seconds': 11}, ValueError)]:
        try:
            compatible_maps(Q, P, f, s, **kwargs)
        except exception:
            rejected.append(name)
        else:
            raise ValueError('accepted bad guard control')
    return dict(words=35, solutions=len(record['solutions']),
                full_maps=record['full_maps'], known_map_recovered=True, guard_rejections=rejected)


def two_charge_control():
    histogram = Counter()
    for raw in json.loads((HERE/'TWENTY_STARS.json').read_text())['stars']:
        words, rho, high, leave, core = star(raw)
        for u, v in combinations(sorted(high), 2):
            if frozenset((u, v)) in leave:
                continue
            cost = sum(len(edge & {u, v}) == 1 for edge in core)
            require(cost >= 2, 'covered two-hub center requires two incidences')
            histogram[cost] += 1
    require(histogram == {2: 64, 3: 8, 4: 4}, 'complete covered two-hub readout')
    return [[cost, n] for cost, n in sorted(histogram.items())]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    stars, first, second = raw_marks()
    records = []
    for f in first:
        for s in second:
            result = compatible_maps(stars[f[0]], stars[s[0]], f, s)
            require(not result['solutions'], 'counterexample to local charge obstruction')
            records.append(dict(first=list(f), second=list(s), **result))
    exact = dict(agent='six-reviewer-5', role='independent mathematical reviewer',
                 input_sha256=FIXTURE_SHA, first_marks=[list(x) for x in first],
                 second_marks=[list(x) for x in second], cases=len(records),
                 full_maps=sum(r['full_maps'] for r in records),
                 nodes=sum(r['nodes'] for r in records), max_case_nodes=max(r['nodes'] for r in records),
                 zero_u_cases=sum(r['second'][4] == 0 for r in records),
                 one_u_cases=sum(r['second'][4] == 1 for r in records),
                 records=records, positive=positive_control(), two_charge=two_charge_control())
    require(sha256(encode(exact)).hexdigest() ==
            'c2fa107a505b44e21f83e99415a4dde3af4d3061b1e735554eb4e4250b619dbb',
            'complete earlier local audit stream changed')
    result = dict(status='COMPLETE', exact_sha256=sha256(encode(exact)).hexdigest(),
                  cases=exact['cases'], full_maps=exact['full_maps'], nodes=exact['nodes'],
                  max_case_nodes=exact['max_case_nodes'], seconds=time.monotonic()-start,
                  peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if args.out:
        args.out.write_bytes(encode(result))
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
