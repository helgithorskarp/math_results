"""Second stars by six paired rows first, fixed-point exact cover last.

Uses actual quadruple pair sets rather than canonical triple resources.
No primary Y-domain or clique search is called.
"""
from itertools import combinations
import json
import time
import model as M
import seeds


def literal_rows(anchor):
    actual_anchor = tuple(frozenset(M.points(w)) for w in anchor)
    result = {1: [], 2: []}
    seen = set()
    for points in combinations(range(16), 4):
        q = frozenset(points)
        moved = frozenset(v ^ 1 for v in points)
        orbit = frozenset((q, moved))
        if orbit in seen:
            continue
        seen.add(orbit)
        quads = tuple(sorted(orbit, key=lambda s:tuple(sorted(s))))
        words = tuple(frozenset(set(a) | {17}) for a in quads)
        if any(len(a & b) > 2 for a,b in combinations(words, 2)) or any(
                len(w & a) > 2 for w in words for a in actual_anchor):
            continue
        pairs = tuple(p for a in quads for p in combinations(sorted(a), 2))
        M.require(len(pairs) == len(set(pairs)), 'literal quad orbit repeats a pair')
        masks = tuple(sorted(M.mask(w) for w in words))
        result[len(quads)].append(dict(quads=quads, pairs=frozenset(pairs), words=masks))
    return tuple(sorted(result[1], key=lambda r:r['words'])), tuple(sorted(result[2], key=lambda r:r['words']))


def y_anchors(anchor):
    fixed, paired = literal_rows(anchor)
    output, sixes, nodes, match_nodes = [], [], 0, 0
    start = time.monotonic()

    def tick():
        nonlocal nodes
        nodes += 1
        if nodes > 200000 or time.monotonic() - start > 10:
            raise RuntimeError('INCOMPLETE literal paired-first Y-star guard')

    def six_first(indices, chosen, covered):
        tick()
        need = 6 - len(chosen)
        if not need:
            sixes.append(chosen)
            fixed_last(chosen, covered)
            return
        for j, index in enumerate(indices):
            if len(indices) - j < need:
                return
            row = paired[index]
            if covered & row['pairs']:
                continue
            future = tuple(k for k in indices[j+1:] if not row['pairs'] & paired[k]['pairs'])
            six_first(future, chosen + (index,), covered | row['pairs'])

    def fixed_last(chosen, covered):
        nonlocal match_nodes
        eligible = tuple(r for r in fixed if not r['pairs'] & covered)
        supports = tuple(frozenset(v // 2 for v in r['quads'][0]) for r in eligible)
        M.require(all(len(s) == 2 for s in supports), 'fixed quad consists of two moved point pairs')

        def cover(left, selected):
            nonlocal match_nodes
            match_nodes += 1
            if match_nodes > 200000 or time.monotonic() - start > 10:
                raise RuntimeError('INCOMPLETE literal fixed-last guard')
            if not left:
                words = tuple(sorted(tuple(anchor) + tuple(w for i in chosen for w in paired[i]['words']) +
                                     tuple(eligible[i]['words'][0] for i in selected)))
                stats = M.check_code(words)
                M.require(stats['words'] == 36 and stats['replications'][16:] == (20,20) and
                          stats['fixed_words'] == 8, 'literal Y-star decoding')
                output.append(words)
                return
            first = min(left)
            for j, support in enumerate(supports):
                if first in support and support <= left:
                    cover(left - support, selected + (j,))

        cover(frozenset(range(8)), ())

    six_first(tuple(range(len(paired))), (), frozenset())
    M.require(len(output) == len(set(output)), 'literal duplicate Y anchor')
    return tuple(sorted(output)), dict(paired_candidates=len(paired), fixed_candidates=len(fixed),
                                       paired_sixes=len(sixes), nodes=nodes, cover_nodes=match_nodes,
                                       anchors=len(output), seconds=time.monotonic() - start)


def verify_root_carriers():
    data = json.loads((seeds.HERE.parent / 'free_involution_upper68' / 'fixtures.json').read_text())
    original = []
    for i, (raw_quads, group) in enumerate(zip(data['stars'], data['groups'])):
        quads = frozenset(frozenset(q) for q in raw_quads)
        mates = {v for v in range(17) if sum(v in q for q in quads) == 4}
        from_tail = {(y,g) for y in mates for g in seeds.maps_for_mate(tuple(tuple(sorted(q)) for q in quads),y)
                     if frozenset(frozenset(g[v] for v in q) for q in quads) == quads}
        from_group = set()
        for raw in group:
            p = tuple(raw) + (17,)
            M.require(frozenset(frozenset(p[v] for v in q) for q in quads) == quads,
                      'supplied point map not actual')
            if all(p[p[v]] == v for v in range(17)):
                fixed = {v for v in range(17) if p[v] == v}
                if len(fixed) == 1 and fixed <= mates:
                    from_group.add((next(iter(fixed)),p))
        M.require(from_tail == from_group, 'tail carrier differs from complete point-group carrier')
        original.append(dict(fixture=i, valid=len(from_group)))
    return original
