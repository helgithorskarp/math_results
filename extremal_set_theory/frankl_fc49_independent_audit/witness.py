#!/usr/bin/env python3
"""Construct and directly verify a 19-point Non-FC witness (Python stdlib).

The original fifteen four-sets and nine auxiliary families are due to
Mingchang Liu, 2026. The antichain tag construction and this verifier are
described in PROOF.md. No external data or negative-certificate theorem is
needed for the final check of this explicitly enumerated union-closed family.
"""
import hashlib
import itertools
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def mask(points):
    return sum(1 << i for i in points)


def union_closure(seeds):
    closed = {0}
    todo = list(seeds)
    while todo:
        a = todo.pop()
        if a in closed:
            continue
        todo.extend(a | b for b in closed if (a | b) not in closed)
        closed.add(a)
    return sorted(closed)


def original_data():
    core = mask((7, 8))
    generators = sorted(
        {mask((*t, 6)) for t in itertools.combinations(range(4), 3)}
        | {core | mask((i, j)) for i in range(4) for j in (4, 5)}
        | {core | mask(t) for t in itertools.combinations((4, 5, 6), 2)}
    )
    bases = [[a for a in generators if a >> i & 1] for i in range(7)]
    bases += [[core | (1 << 4), core | (1 << 5)] for _ in range(2)]
    auxiliaries = [
        [s for s in range(512)
         if not (s >> i & 1) or any((s & a) == a for a in bases[i])]
        for i in range(9)
    ]
    return generators, union_closure(generators), auxiliaries


def pair_union_counts(indicator):
    """Exact OR convolution by subset zeta transform and Mobius inversion."""
    size = len(indicator)
    require(size > 0 and size & (size - 1) == 0, "Not a Boolean cube")
    require(all(x in (0, 1) for x in indicator), "Not an indicator")
    values = list(indicator)
    step = 1
    while step < size:
        for base in range(0, size, 2 * step):
            for x in range(base, base + step):
                values[x + step] += values[x]
        step *= 2
    values = [x * x for x in values]
    step = 1
    while step < size:
        for base in range(0, size, 2 * step):
            for x in range(base, base + step):
                values[x + step] -= values[x]
        step *= 2
    return values


def check_union_closed(indicator):
    counts = pair_union_counts(indicator)
    require(all(x >= 0 for x in counts), "Negative pair count")
    require(sum(counts) == sum(indicator) ** 2, "Wrong pair total")
    require(all(present or count == 0 for present, count in zip(indicator, counts)),
            "A union of two members is missing")
    return sum(counts)


def controls():
    # Check the transform against the defining ordered-pair enumeration for
    # every family on three points, including empty and non-UC families.
    for family in range(256):
        v = [(family >> s) & 1 for s in range(8)]
        brute = [0] * 8
        for a in range(8):
            for b in range(8):
                brute[a | b] += v[a] * v[b]
        require(pair_union_counts(v) == brute, "Transform control failed")
    try:
        check_union_closed([1, 1, 1, 0])
    except ValueError:
        return 256
    raise ValueError("Accepted a non-union-closed control")


def construct():
    generators, closure, auxiliaries = original_data()
    require(len(generators) == 15 and all(a.bit_count() == 4 for a in generators),
            "Wrong original generators")
    require(len(closure) == 100, "Wrong original closure")
    rows = []
    for family in auxiliaries:
        S = set(family)
        require(all((a | b) in S for a in S for b in S), "Bad auxiliary closure")
        require(all((a | b) in S for a in S for b in closure), "Bad slice stability")
        rows.append([2 * sum(s >> i & 1 for s in S) - len(S) for i in range(9)])
    multiplicities = [3, 3, 3, 3, 15, 15, 5, 41, 41]
    tags = [mask(t) for t in itertools.combinations(range(10), 5)][:129]
    require(len(tags) == len(set(tags)) == sum(multiplicities), "Bad tag assignment")
    v = [0] * (1 << 19)
    for a in closure:
        v[a] = 1
    start = 0
    for family, count in zip(auxiliaries, multiplicities):
        for t in tags[start:start + count]:
            for a in family:
                v[a | (t << 9)] = 1
        start += count
    for t in range(1 << 10):
        if t.bit_count() >= 6:
            v[t << 9:(t + 1) << 9] = [1] * 512
    require(all(v[a] for a in generators), "Original family is not contained")
    return v, generators, rows


def verify():
    checked_controls = controls()
    v, generators, rows = construct()
    total = sum(v)
    frequencies = [sum(present for s, present in enumerate(v) if s >> i & 1)
                   for i in range(19)]
    imbalance = [2 * f - total for f in frequencies]
    require(total == 242283, "Unexpected cardinality")
    require(imbalance[:9] == [-5, -5, -5, -5, -31, -31, -55, -49, -49],
            "Original points are not strictly scarce as claimed")
    require(all(x > 0 for x in imbalance[9:]), "Unexpected outside-point abundance")
    pairs = check_union_closed(v)
    # Removing the full set breaks closure. Check the actual 19-point instance.
    broken = v.copy()
    broken[-1] = 0
    try:
        check_union_closed(broken)
    except ValueError:
        pass
    else:
        raise ValueError("Accepted the corrupted nineteen-point witness")
    return {
        "verified": True, "universe_size": 19, "family_size": total,
        "generators": generators, "frequencies": frequencies,
        "imbalances": imbalance, "ordered_union_pairs": pairs,
        "auxiliary_rows": rows, "small_transform_controls": checked_controls,
        "corrupted_global_witness_rejected": True,
        "indicator_sha256": hashlib.sha256(bytes(v)).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
