"""Direct set/column pair-incidence decoder; imports no producer kernel."""
from collections import Counter
import itertools as it
import time


def check(ok, msg):
    if not ok:
        raise ValueError(msg)


def decode(words, owners, fi):
    start = time.monotonic()
    ground = set(range(17))
    blocks = [frozenset(w) for w in words]
    check(len(blocks) == len(set(blocks)) == 20 and all(len(b) == 4 and b <= ground for b in blocks), 'literal20 original star')
    columns = {p: {j for j, b in enumerate(blocks) if p in b} for p in ground}
    incidence = Counter(frozenset(pair) for b in blocks for pair in it.combinations(b, 2))
    check(len(incidence) == 120 and set(incidence.values()) == {1}, 'all120 literal pairs simple')
    low = {p for p in ground if len(columns[p]) == 5}
    check(sum(5 - len(columns[p]) for p in ground) == 5, 'mass5')
    result = []
    chosen = 0
    states = 0
    for owner in owners:
        H, mate = set(owner['H']), owner['mate']
        if not H <= low or mate not in low:
            continue
        chosen += 1
        check(owner['delta'] == [0] * 5 and owner['z'] == 0, 'source physical deficits')
        A = set(owner['A'])
        check(len(H) == 5 and len(A) == 3 and A <= H and mate not in H, 'literal owner support')
        common = [b - {mate} for b in blocks if mate in b]
        check(len(common) == 5 and sum(map(len, common)) == len(set().union(*common)) == 15, 'actual mate tail partition')
        check(H <= set().union(*common) and frozenset(A) in common, 'allLOW Hubs covered and ownedA tail')
        unused = ground - {mate} - set().union(*common)
        check(len(unused) == 1 and not unused & H, 'actual unique uncovered SAT')
        free = next(iter(unused))
        d = 5 - len(columns[free])
        check(d in (1, 2) and not columns[free] & columns[mate], 'HIGH free mate hole')
        holes = {p for p in ground - {free} if not columns[free] & columns[p]}
        check(len(holes) == 1 + 3 * d and mate in holes and len(holes - {mate}) == 3 * d, 'literal free-hole degrees')
        hub_holes = tuple(sorted(holes & H))
        sat_holes = tuple(sorted(holes - H - {mate}))
        check([len(b & H) for b in blocks].count(3) == 1 and max(len(b & H) for b in blocks) == 3, 'unique three-Hub owned block')
        check(all(columns[p] & columns[q] for p in H for q in H - {p}) and all(columns[mate] & columns[p] for p in H), 'zero HH and mate-Hub leaves')
        check(all(columns[p] & columns[q] for p in H for q in low - H - {p}), 'no LOW SAT friends')
        # Fill named slots from independent assignments to ordered A and B columns.
        residual = sorted(H - A)
        for permutation in it.permutations(sorted(A)):
            for orientation in (0, 1):
                states += 1
                check(states <= 100000 and time.monotonic() - start <= 10, 'INCOMPLETE original100000-state/10s fixture oracle guard')
                roles = permutation + tuple(residual[::(-1 if orientation else 1)])
                position = {p: j for j, p in enumerate(roles)}
                hm = sum(2 ** position[p] for p in holes & H)
                pieces = []
                for tail in sorted(common, key=lambda b: tuple(sorted(b))):
                    sat = sorted(tail - H)
                    lost = sorted(p for p in sat if not columns[p] & columns[free])
                    mask = sum(2 ** position[p] for p in tail & H)
                    pieces.append((tuple(sorted(tail)), mask, tuple(sat), tuple(lost)))
                key = (d, hm, tuple(sorted((mask, len(sat), len(lost)) for tail, mask, sat, lost in pieces)))
                witness = (fi, tuple(sorted(H)), mate, roles)
                result.append((witness, free, d, hm, hub_holes, sat_holes, tuple(pieces), key, tuple(owner['coordinates'])))
    check(time.monotonic() - start <= 10, 'INCOMPLETE unchanged whole-fixture oracle guard')
    return sorted(result), chosen, states
