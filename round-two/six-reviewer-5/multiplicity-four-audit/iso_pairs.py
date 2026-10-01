"""Independent all-raw isolated-hub pair audit; six-reviewer-5.
Adapted from this reviewer's earlier group-free local checker.
No researcher modules, automorphism groups or pair certificates execute.
"""
from collections import Counter
from itertools import combinations, permutations
from math import factorial
import json,time,sys
from pathlib import Path
class Incomplete(RuntimeError): pass
def require(ok,msg):
 if not ok:raise ValueError(msg)
def compatible_maps(Q, P, f, s, nodes=200000, seconds=10):
    """Every common-tail preserving injection; early conflicts count suffixes.

    Q is first-center star, P second-center star. First center is label17;
    first-star label a is the second center and is excluded from image(P).
    """
    require(type(nodes) is int and 0 <= nodes <= 200000 and 0 < seconds <= 10, 'finite guard domain')
    _, u, a = f
    _, up, b = s
    source = sorted((tuple(sorted(w-{b})) for w in P if b in w))
    target = sorted((tuple(sorted(w-{a})) for w in Q if a in w))
    m = len(source)
    require(m == len(target) and m in (4, 5), 'common word count')
    require(len(set().union(*(set(t) for t in source))) == 3*m and
            len(set().union(*(set(t) for t in target))) == 3*m, 'disjoint common tails')
    si = next(i for i, tail in enumerate(source) if up in tail)
    ti = next(i for i, tail in enumerate(target) if u in tail)
    common_source, common_target = set().union(*(set(t) for t in source)), set().union(*(set(t) for t in target))
    residual_source = sorted(set(range(17))-common_source-{b})
    residual_target = sorted(set(range(18))-common_target-{17, a})
    require(len(residual_source) == len(residual_target), 'residual bijection count')
    private_first = tuple(w | {17} for w in Q if a not in w)
    private_second = tuple(w for w in P if b not in w)
    owner = {tuple(t): wi for wi, w in enumerate(private_first) for t in combinations(sorted(w), 3)}
    triples = tuple((wi, t) for wi, w in enumerate(private_second) for t in combinations(sorted(w), 3))
    current = {b: 17, up: u}
    require(len(current) == 2 and len(set(current.values())) == 2, 'distinct fixed points')
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


def marks_and_stars():
    from local_pair import star
    p=Path(__file__).resolve().parent
    data=json.loads((p/'TWENTY_STARS.json').read_text())['stars']
    marks=[]; stars=[]
    for i,raw in enumerate(data):
        q,rho,h,leave,core=star(raw); stars.append(q)
        for u in sorted(h):
            if rho[u] in (3,4) and all(u not in e for e in core) and all(rho[a]==4 for a in h-{u}):
                marks += [(i,u,a) for a in sorted(h-{u})]
    require(len(marks)==7,'all raw isolated-hub markings')
    return marks,stars


def positive_control():
    p=Path(__file__).resolve().parent
    data=json.loads((p/'positive_joint.json').read_text())
    original=[frozenset(a for a in range(18) if mask>>a&1) for mask in data['word_masks']]
    require(len(original)==len(set(original))==35 and all(len(w)==5 for w in original), 'positive family shape')
    require(all(len(w&z)<=2 for w,z in combinations(original,2)), 'positive literal packing')
    degrees=[sum(a in w for w in original) for a in range(18)]
    x,y=[a for a in range(18) if degrees[a]==20]
    common=[w for w in original if {x,y}<=w]
    require(len(common)==5,'positive common-word count')
    results=[]
    for family in (original,[w for w in original if w!=common[0]]):
        C=set().union(*(w-{x,y} for w in family if {x,y}<=w));u=min(C)
        qlabels,plabels=sorted(set(range(18))-{x}),sorted(set(range(18))-{y})
        qi,pi={a:k for k,a in enumerate(qlabels)},{a:k for k,a in enumerate(plabels)}
        Q=tuple(frozenset(qi[a] for a in w-{x}) for w in family if x in w)
        P=tuple(frozenset(pi[a] for a in w-{y}) for w in family if y in w)
        f,s=(0,qi[u],qi[y]),(0,pi[u],pi[x])
        record=compatible_maps(Q,P,f,s)
        literal=tuple(qi[plabels[k]] if plabels[k]!=x else 17 for k in range(17))
        require(literal in record['solutions'], 'known actual positive point map')
        results.append(dict(words=len(family),center_degree=len(Q),common_words=len(Q)+len(P)-len(family),solutions=len(record['solutions']),full_maps=record['full_maps'],known_map_recovered=True))
    controls=[]
    for name,kwargs,exception in [('zero nodes',{'nodes':0},Incomplete),('excess nodes',{'nodes':200001},ValueError),('excess seconds',{'seconds':11},ValueError)]:
        try:compatible_maps(Q,P,f,s,**kwargs)
        except exception:controls.append(name)
        else:raise ValueError('accepted bad guard control')
    return dict(positive_families=results,guard_rejections=controls)


def audit():
    marks,stars=marks_and_stars();records=[]
    for f in marks:
        for s in marks:
            out=compatible_maps(stars[f[0]],stars[s[0]],f,s)
            require(not out['solutions'],'counterexample to shared-isolated-hub obstruction')
            records.append(dict(first=list(f),second=list(s),**out))
    return dict(marks=[list(x) for x in marks],cases=records,positive=positive_control())
