"""Exact complete local covers for the r2/a5/b0 mixed-five row."""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json

from patch import A, B, C, D, E, F, H, I, ONET, ORD, R, S, U, V, Bad, Patch, edge


def need(test, message):
    if not test:
        raise RuntimeError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def supplier_cover():
    # Symbols 0..4 are one-T fours, symbol 5 is D, not point IDs.
    rows = []
    for u, v in product(combinations(range(6), 3), repeat=2):
        common = set(u) & set(v)
        if len(common) > 2 or 5 in common or common and len(common) != 2:
            continue
        rows.append((u, v))
    orbits = Counter()
    maps = []
    for u, v in rows:
        images = []
        for q in permutations(range(5)):
            ren = dict(zip(range(5), q)) | {5: 5}
            uu, vv = tuple(sorted(ren[x] for x in u)), tuple(sorted(ren[x] for x in v))
            images.extend(((uu, vv), (vv, uu)))
        rep = min(images)
        orbits[rep] += 1
        maps.append([list(u), list(v), [list(t) for t in rep]])
    expected = {((0, 1, 2), (0, 1, 3)): 60,
                ((0, 1, 2), (0, 1, 5)): 60,
                ((0, 1, 2), (3, 4, 5)): 20}
    need(dict(orbits) == expected, 'complete supplier orbit maps')
    return {'input_rows': 400, 'admitted_rows': len(rows),
            'orbits': [[list(u), list(v), n] for (u, v), n in sorted(orbits.items())],
            'original_role_map_sha256': digest(maps)}


def paired_fans():
    rows, admitted = [], []
    for position, third_sector in product((1, 2, 3), (2, 3, 4)):
        fan = [2, 3, 4, 5, 6]
        fan[position] = 1
        a, b = fan[position - 1], fan[position + 1]
        dc = (a, 0, b, 7, 8)
        triangles = {tuple(sorted((0, fan[k], fan[k + 1]))) for k in range(4)}
        triangles.update(tuple(sorted((1, dc[k], dc[(k + 1) % 5]))) for k in (0, 1, third_sector))
        t = Counter(x for cell in triangles for x in cell)
        good = all(t[x] <= 2 for x in range(2, 9))
        rows.append([position, third_sector, sorted(triangles), good])
        if good:
            admitted.append([position, third_sector])
    need(admitted == [[1, 3], [1, 4], [2, 3], [3, 2], [3, 3]], 'nine paired fans')
    return {'rows': 9, 'admitted': admitted, 'entry_sha256': digest(rows)}


def canonical_slots(length, ordinary_start):
    words = []
    for types in product(sorted(ONET) + [None], repeat=length):
        one = [x for x in types if x is not None]
        if len(one) != len(set(one)):
            continue
        nxt, slots = ordinary_start, []
        for t in types:
            if t is None:
                slots.append(nxt)
                nxt += 1
            else:
                slots.append(t)
        words.append(tuple(slots))
    return sorted(words)


def all_covers(evaluator, patch_type=Patch):
    records, tested, admitted, nodes, leaves = [], Counter(), Counter(), Counter(), Counter()

    def accept(tag, key, q):
        tested[tag] += 1
        state = evaluator(q)
        good = state is not None
        admitted[tag] += good
        records.append([tag, list(key), good])
        return state

    def close_threes(tag, key, q, state):
        nodes[tag] += 1
        options = []
        # All three neighbor pairs at a degree three are consecutive.
        # Every missing sector is a Q; retain all fifteen original opposites.
        for v in (U, V):
            known = {edge(f[f.index(v) - 1], f[(f.index(v) + 1) % len(f)])
                     for f in state['faces'] if v in f}
            need(len(state['contacts'][v]) == 3, 'complete three contacts')
            for a, b in combinations(sorted(state['contacts'][v]), 2):
                if edge(a, b) in known:
                    continue
                choices = []
                for x in range(15):
                    qx = q.plus((v, a, x, b))
                    child_key = (*key, v, a, b, x)
                    st = accept(tag + '-Q', child_key, qx)
                    if st is not None:
                        choices.append((child_key, qx, st))
                options.append((len(choices), v, a, b, choices))
        if not options:
            raise RuntimeError(('unexpected full-three completion', tag, key))
        _, v, a, b, choices = min(options, key=lambda t: t[:4])
        records.append([tag + '-selected-corner', list(key) + [v, a, b], len(choices)])
        if not choices:
            leaves[tag] += 1
        for child_key, child, st in choices:
            close_threes(tag, child_key, child, st)

    families = [((A, B, C), (A, B, E)),
                ((A, B, C), (A, B, D)),
                ((A, B, C), (E, H, D))]
    # F,D noncontacting. I,R,S are three distinct saturated ordinary fours.
    for fi, (un, vn) in enumerate(families):
        extra = [(U, x) for x in un] + [(V, x) for x in vn]
        shared = sorted(set(un) & set(vn))
        sq = [(shared[0], U, shared[1], V)] if shared else []
        for e, p in canonical_slots(2, 12):
            fan = (e, I, R, S, p)
            fs = [(F, fan[k], fan[k + 1]) for k in range(4)] + sq
            for h in sorted(ONET):
                key = (fi, e, p, h)
                q = patch_type(fs + [(F, e, h, p)], extra)
                st = accept('non-initial', key, q)
                if st is None:
                    continue
                states = [(key, q, st)]
                for step, endpoint in enumerate(x for x in (e, p) if x in ORD):
                    children = []
                    for ky, parent, _ in states:
                        for j in range(15):
                            child = parent.plus((endpoint, h, j))
                            kj = (*ky, j)
                            child_state = accept('non-T' + str(step), kj, child)
                            if child_state is not None:
                                children.append((kj, child, child_state))
                    states = children
                for ky, child, child_state in states:
                    close_threes('non', ky, child, child_state)
    # F,D contacting, separated Qs at D: only D-free supplier family.
    un, vn = families[0]
    extra = [(U, x) for x in un] + [(V, x) for x in vn]
    for position in (1, 2):
        for slots in canonical_slots(4, 11):
            if position == 1:
                a, y, c, d = slots
                b, x = I, R
                fan = (a, D, b, x, y)
            else:
                x, y, c, d = slots
                a, b = I, R
                fan = (x, a, D, b, y)
            fs = [(F, fan[k], fan[k + 1]) for k in range(4)] + [(D, c, d), (A, U, B, V)]
            for h, k, l in product(sorted(ONET), repeat=3):
                key = (position, *slots, h, k, l)
                q = patch_type(fs + [(F, fan[0], h, fan[-1]), (D, b, k, c), (D, d, l, a)], extra, fd_contact=True)
                st = accept('separated', key, q)
                if st is not None:
                    close_threes('separated', key, q, st)
    # Adjacent Qs at D: its unique QQ contact is V. All shared aliases stay.
    for fi, (un, vn) in enumerate(families[1:]):
        extra = [(U, x) for x in un] + [(V, x) for x in vn]
        sq = [(A, U, B, V)] if fi == 0 else []
        for e, w in canonical_slots(2, 12):
            fs = [(F, I, D), (F, D, R), (F, R, S), (F, S, e), (D, I, w)] + sq
            for h, k, l in product(sorted(ONET), repeat=3):
                key = (fi, e, w, h, k, l)
                q = patch_type(fs + [(F, I, h, e), (D, w, k, V), (D, V, l, R)], extra, fd_contact=True)
                st = accept('adjacent-initial', key, q)
                if st is None:
                    continue
                for j in range(15):
                    qj = q.plus((I, w, j, h))
                    kj = (*key, j)
                    sj = accept('adjacent-J', kj, qj)
                    if sj is None:
                        continue
                    for m in range(15):
                        qm = qj.plus((R, S, m, l))
                        km = (*kj, m)
                        sm = accept('adjacent-M', km, qm)
                        if sm is not None:
                            close_threes('adjacent', km, qm, sm)
    serial = sorted(json.dumps(r, separators=(',', ':')) for r in records)
    return {'tested': dict(sorted(tested.items())), 'admitted': dict(sorted(admitted.items())),
            'three_completion_nodes': dict(sorted(nodes.items())),
            'empty_corner_leaves': dict(sorted(leaves.items())),
            'full_three_terminals': 0,
            'all_tested_case_sha256': hashlib.sha256(('\n'.join(serial) + '\n').encode()).hexdigest(),
            'admitted_case_sha256': digest(sorted((r for r in records if r[0].endswith('-selected-corner') or r[2] is True), key=lambda r: json.dumps(r)))}


def evaluate(q):
    try:
        return q.evaluate()
    except Bad:
        return None


def build_report():
    return {'claim': 'r2_a5_b0_f0_1_f1_1_f2_0_O6_excluded',
            'supplier_cover': supplier_cover(), 'paired_fans': paired_fans(),
            'canonical_slot_counts': {'two': len(canonical_slots(2, 12)), 'four': len(canonical_slots(4, 11))},
            'local_covers': all_covers(evaluate)}


def main():
    report = build_report()
    expected = json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
    need(report == expected, 'complete expected output mismatch')
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
