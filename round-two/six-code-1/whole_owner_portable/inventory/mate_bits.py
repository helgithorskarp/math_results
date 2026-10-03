"""Bit-incidence decoder for every zero-Hub/z0 physical owner transport."""
import itertools as it
import time


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def points(mask):
    return tuple(p for p in range(17) if mask >> p & 1)


def decode(words, owners, fi):
    begin = time.monotonic()
    universe = (1 << 17) - 1
    blocks = tuple(sum(1 << p for p in w) for w in words)
    need(len(blocks) == len(set(blocks)) == 20, 'twenty distinct literal blocks')
    covered = [0] * 17
    rep = [0] * 17
    for word, block in zip(words, blocks):
        need(len(word) == len(set(word)) == 4 and all(type(p) is int and 0 <= p < 17 for p in word), 'four literal points')
        for p in word:
            tail = block ^ (1 << p)
            need(not covered[p] & tail, 'every original pair at most once')
            covered[p] |= tail
            rep[p] += 1
    leave = [universe ^ covered[p] ^ (1 << p) for p in range(17)]
    deficit = [5 - n for n in rep]
    need(min(deficit) >= 0 and sum(deficit) == 5, 'original deficit mass five')
    need(all(leave[p].bit_count() == 1 + 3 * deficit[p] for p in range(17)), 'literal leave degrees')
    records = []
    selected = 0
    states = 0
    for owner in owners:
        if owner['delta'] != [0] * 5 or owner['z'] != 0:
            continue
        selected += 1
        H, A, mate = tuple(owner['H']), tuple(owner['A']), owner['mate']
        hmask = sum(1 << p for p in H)
        need(all(deficit[p] == 0 for p in H) and deficit[mate] == 0, 'zero-Hub/z0 premise checked literally')
        need(owner['friends'] == [[], [], [], [], []] and not owner['HH_leave'] and not owner['mate_leave'], 'literal zero source interface')
        tails = tuple(sorted(block ^ (1 << mate) for block in blocks if block >> mate & 1))
        need(len(tails) == 5, 'five mate blocks')
        union = 0
        for tail in tails:
            need(not union & tail, 'disjoint mate tails')
            union |= tail
        outside = universe ^ union ^ (1 << mate)
        need(outside.bit_count() == 1 and not outside & hmask, 'unique free SAT point')
        free = points(outside)[0]
        need(leave[mate] == outside and deficit[free] in (1, 2), 'free point is the unique HIGH SAT mate neighbor')
        need(sum((block & hmask).bit_count() == 3 for block in blocks) == 1 and not any((block & hmask).bit_count() == 4 for block in blocks), 'exact T1 ownership')
        need(sum(1 << p for p in A) in tails, 'owned A is an actual shared mate tail')
        hh = points(leave[free] & hmask)
        ss = points(leave[free] & ~(hmask | (1 << mate)))
        need(len(hh) + len(ss) == 3 * deficit[free], 'all holes other than the mate accounted for')
        B = tuple(p for p in H if p not in A)
        for first in it.permutations(A):
            for last in it.permutations(B):
                states += 1
                need(states <= 100000 and time.monotonic() - begin <= 10, 'INCOMPLETE original100000-state/10s fixture decoder guard')
                roles = first + last
                named_holes = sum(1 << j for j, p in enumerate(roles) if p in hh)
                details = []
                for tail in tails:
                    sat = points(tail & ~hmask)
                    holes = tuple(p for p in sat if leave[free] >> p & 1)
                    hm = sum(1 << j for j, p in enumerate(roles) if tail >> p & 1)
                    details.append((points(tail), hm, sat, holes))
                details.sort(key=lambda a: a[0])
                profile = (deficit[free], named_holes, tuple(sorted((hm, len(sat), len(holes)) for tail, hm, sat, holes in details)))
                witness = (fi, H, mate, roles)
                records.append((witness, free, deficit[free], named_holes, hh, ss, tuple(details), profile, tuple(owner['coordinates'])))
    need(time.monotonic() - begin <= 10, 'INCOMPLETE unchanged whole-fixture decoder guard')
    return sorted(records), selected, states
