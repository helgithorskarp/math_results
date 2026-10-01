"""Separate same-author bit/dart audit; imports no primary checker code."""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json

F, D, U, V, A, B, C, Z, I, R, S, P = range(12)
ORD = set(range(8, 15))
DEG = [5, 5, 3, 3, 4, 4, 4, 4] + [4] * 7
TQ = [4, 3, 0, 0, 1, 1, 1, 0] + [2] * 7
QQ = [0, 1, 3, 3, 2, 2, 2, 4] + [1] * 7


def bit(a, b):
    a, b = min(a, b), max(a, b)
    return 1 << (b * (b - 1) // 2 + a)


def vertices(mask):
    while mask:
        v = (mask & -mask).bit_length() - 1
        yield v
        mask &= mask - 1


def boundary(f):
    candidates = []
    for word in (tuple(f), tuple(reversed(f))):
        candidates.extend(word[k:] + word[:k] for k in range(len(word)))
    return min(candidates)


class Reject(Exception):
    pass


class DartAudit:
    def __init__(self, faces=(), extra=(), *, fd_contact=False, missing_capacity=True):
        self.cells = frozenset(boundary(f) for f in faces)
        self.bars = tuple(extra)
        self.fd_contact = fd_contact
        self.missing_capacity = missing_capacity

    def plus(self, *fs):
        return DartAudit(self.cells | {boundary(f) for f in fs}, self.bars, fd_contact=self.fd_contact, missing_capacity=self.missing_capacity)

    def inspect(self, pair_faces=True):
        cells = set(self.cells)
        e = 0
        no = 0 if self.fd_contact else bit(F, D)
        for a, b in self.bars:
            if a == b:
                raise Reject()
            e |= bit(a, b)
        for f in cells:
            if len(f) not in (3, 4) or len(set(f)) != len(f):
                raise Reject()
            for a, b in zip(f, f[1:] + f[:1]):
                e |= bit(a, b)
            if len(f) == 4:
                no |= bit(f[0], f[2]) | bit(f[1], f[3])
        if e & no:
            raise Reject()
        nbr = [0] * 15
        for b in range(15):
            for a in range(b):
                if e & bit(a, b):
                    nbr[a] |= 1 << b
                    nbr[b] |= 1 << a
        if any(nbr[v].bit_count() > DEG[v] for v in range(15)):
            raise Reject()
        if nbr[U] & (1 << V) or any(nbr[v] & sum(1 << x for x in ORD) for v in (U, V)):
            raise Reject()
        # Find triangles by common-neighbor masks, rather than scanning triples.
        for a in range(15):
            for b in vertices(nbr[a] & ~((1 << (a + 1)) - 1)):
                for c in vertices(nbr[a] & nbr[b] & ~((1 << (b + 1)) - 1)):
                    cells.add((a, b, c))
        t = [0] * 15
        darts = {}
        corners = [dict() for _ in range(15)]
        for f in sorted(cells):
            if len(f) == 3:
                for v in f:
                    t[v] += 1
            for ix, v in enumerate(f):
                a, b = f[ix - 1], f[(ix + 1) % len(f)]
                corner = bit(a, b)
                if corner in corners[v] and corners[v][corner] != f:
                    raise Reject()
                corners[v][corner] = f
                ed = tuple(sorted((v, b)))
                darts.setdefault(ed, []).append(f)
                if len(f) == 4 and v in (F, D):
                    o = f[(ix + 2) % 4]
                    if o not in (A, B, C, Z):
                        raise Reject()
                    if v == D and nbr[D] & (1 << V) and V not in (a, b):
                        raise Reject()
        if any(t[v] > TQ[v] for v in range(15)) or any(len(fs) > 2 for fs in darts.values()):
            raise Reject()
        if any((nbr[a] & nbr[b]).bit_count() > 2 for a in range(15) for b in range(a)):
            raise Reject()
        qends = [0] * 15
        for a in range(15):
            for b in vertices(nbr[a] & ~((1 << (a + 1)) - 1)):
                fs = darts.get((a, b), [])
                if TQ[a] == 0 or TQ[b] == 0 or len(fs) == 2 and all(len(f) == 4 for f in fs):
                    qends[a] += 1
                    qends[b] += 1
        if any(qends[v] > QQ[v] for v in range(15)):
            raise Reject()
        rotations = {}
        for v in range(15):
            link = [0] * 15
            cmask = 0
            for corner, f in corners[v].items():
                ix = f.index(v)
                a, b = f[ix - 1], f[(ix + 1) % len(f)]
                link[a] |= 1 << b
                link[b] |= 1 << a
                cmask |= corner
            lm = sum(1 << a for a in range(15) if link[a])
            if any(x.bit_count() > 2 for x in link):
                raise Reject()
            left = lm
            while left:
                root = (left & -left).bit_length() - 1
                component, frontier = 1 << root, 1 << root
                while frontier:
                    reached = 0
                    for x in vertices(frontier):
                        reached |= link[x]
                    frontier = reached & ~component
                    component |= frontier
                left &= ~component
                if all(link[x].bit_count() == 2 for x in vertices(component)) and component.bit_count() != DEG[v]:
                    raise Reject()
            if self.missing_capacity and nbr[v].bit_count() == DEG[v] - 1 and lm == nbr[v] and cmask.bit_count() == nbr[v].bit_count() - 1:
                ends = [a for a in vertices(lm) if link[a].bit_count() == 1]
                if len(ends) == 2 and TQ[v] - t[v] > sum(t[a] < TQ[a] for a in ends):
                    raise Reject()
            if nbr[v].bit_count() != DEG[v]:
                continue
            options = []
            root = min(vertices(nbr[v]))

            def walk(path, todo):
                if todo:
                    for a in vertices(todo):
                        walk(path + [a], todo ^ (1 << a))
                    return
                if path[1] > path[-1]:
                    return
                mask = 0
                for a, b in zip(path, path[1:] + path[:1]):
                    mask |= bit(a, b)
                if cmask & ~mask:
                    return
                ntrue, possible = (mask & e).bit_count(), (mask & ~(e | no)).bit_count()
                if ntrue <= TQ[v] <= ntrue + possible:
                    options.append(mask)

            walk([root], nbr[v] ^ (1 << root))
            if not options:
                raise Reject()
            rotations[v] = options
        if pair_faces:
            for (u, v), fs in sorted(darts.items()):
                if len(fs) != 1 or u not in rotations or v not in rotations:
                    continue
                f = fs[0]

                def other_ends(a, b):
                    ix = f.index(a)
                    old = f[ix - 1] if f[(ix + 1) % len(f)] == b else f[(ix + 1) % len(f)]
                    choices = 0
                    for rot in rotations[a]:
                        for c in vertices(nbr[a] & ~(1 << old)):
                            if rot & bit(b, c):
                                choices |= 1 << c
                    return list(vertices(choices))

                possible = False
                for a in other_ends(u, v):
                    for b in other_ends(v, u):
                        newface = (u, v, a) if a == b else (u, v, b, a)
                        try:
                            self.plus(newface).inspect(False)
                        except Reject:
                            continue
                        possible = True
                if not possible:
                    raise Reject()
        return True

def need(test, message):
    if not test:
        raise RuntimeError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def supplier_cover():
    # These symbols concern supplier roles only, not the fifteen-point IDs.
    rows = []
    triples = [tuple(vertices(m)) for m in range(32) if m.bit_count() == 3]
    for u, v in sorted(product(triples, repeat=2)):
        common = set(u) & set(v)
        if len(common) > 2 or 4 in common:
            continue
        if common & {0, 1, 2} and len(common) != 2:
            continue
        rows.append((u, v))
    need(len(rows) == 42, 'supplier cover')
    orbits = Counter()
    for u, v in rows:
        images = []
        for q in permutations(range(3)):
            ren = dict(zip(range(3), q)) | {3: 3, 4: 4}
            uu, vv = tuple(sorted(ren[x] for x in u)), tuple(sorted(ren[x] for x in v))
            images.extend(((uu, vv), (vv, uu)))
        orbits[min(images)] += 1
    return rows, [[list(u), list(v), n] for (u, v), n in sorted(orbits.items())]


def collar_cover(rows):
    records, critical, counts = [], [set(), set()], Counter()
    for u, v in rows:
        th = {x: ({0} if x in u else set()) | ({1} if x in v else set()) for x in range(5)}
        for e, p in permutations((0, 1, 2, 5, 6, 7, 8), 2):
            for h in range(4):
                if h in (e, p):
                    continue
                one = [x for x in (e, p) if x < 3]
                if any(len(th[x]) == 2 for x in one + [h] if x < 3):
                    why = 'shared-oneT-collar'
                elif not one:
                    why = 'two-ordinary-endpoints'
                elif h == 3 and any(x >= 5 for x in (e, p)):
                    why = 'ordinary-endpoint-zero-opposite'
                elif any(th[x] & th[h] for x in one):
                    why = 'QQ-contact-triangle'
                elif len(one) == 2 and th[h]:
                    why = 'opposite-oneT-three-saturated-endpoints'
                elif len(one) == 1 and h < 3 and th[one[0]] and th[h]:
                    why = 'forced-three-three-edge'
                elif h < 3 and len(one) == 1 and bool(th[one[0]]) != bool(th[h]):
                    which = int(not bool(th[h]))
                    why = ('zero-three-endpoint-closure', 'zero-three-opposite-closure')[which]
                    critical[which].add((u, v, e, p, h))
                else:
                    raise RuntimeError(('uncovered collar', u, v, e, p, h))
                counts[why] += 1
                records.append([list(u), list(v), e, p, h, why])
    # Exact original-role maps, not just an equality of orbit counts.
    expected = [set(), set()]
    for q in permutations(range(3)):
        ren = dict(zip(range(3), q)) | {3: 3, 4: 4}
        for swap, reverse, ordinary in product((False, True), (False, True), range(5, 9)):
            uu, vv = tuple(sorted(ren[x] for x in (0, 3, 1))), tuple(sorted(ren[x] for x in (0, 3, 4)))
            if swap:
                uu, vv = vv, uu
            for which in (0, 1):
                endpoint, opposite = (ren[2], ren[1]) if which == 0 else (ren[1], ren[2])
                endpoints = (ordinary, endpoint) if reverse else (endpoint, ordinary)
                expected[which].add((uu, vv, *endpoints, opposite))
    need(critical == expected, 'critical collar role maps')
    return {'rows': len(records), 'counts': dict(sorted(counts.items())), 'entry_sha256': digest(records)}, [len(x) for x in critical]


def paired_fans():
    rows, admitted = [], []
    for position, third_sector in product((1, 2, 3), (2, 3, 4)):
        fan = [2, 3, 4, 5, 6]
        fan[position] = 1
        a, b = fan[position - 1], fan[position + 1]
        dc = (a, 0, b, 7, 8)
        triangles = {tuple(sorted((0, fan[k], fan[k + 1]))) for k in range(4)}
        triangles.update(tuple(sorted((1, dc[k], dc[(k + 1) % 5]))) for k in (0, 1, third_sector))
        t = Counter(x for face in triangles for x in face)
        good = all(t[x] <= 2 for x in range(2, 9))
        rows.append([position, third_sector, sorted(triangles), good])
        if good:
            admitted.append([position, third_sector])
    need(admitted == [[1, 3], [1, 4], [2, 3], [3, 2], [3, 3]], 'paired fan completeness')
    return {'rows': 9, 'admitted': admitted, 'entry_sha256': digest(rows)}


def canonical_slots(length, ordinary_start):
    words = []
    for k in range(min(3, length) + 1):
        for places in combinations(range(length), k):
            for names in permutations((A, B, C), k):
                one = dict(zip(places, names))
                nxt, word = ordinary_start, []
                for i in range(length):
                    if i in one:
                        word.append(one[i])
                    else:
                        word.append(nxt)
                        nxt += 1
                words.append(tuple(word))
    return sorted(words)


def all_covers(evaluator, patch_type=DartAudit, missing_capacity=True):
    records, tested, admitted = [], Counter(), Counter()

    def accept(tag, key, patch):
        tested[tag] += 1
        good = evaluator(patch)
        admitted[tag] += good
        records.append([tag, list(key), good])
        return good

    extra = [(U, A), (U, Z), (U, B), (V, A), (V, Z), (V, D)]
    # Noncontacting: the one-T F endpoint has no three contact.
    seed = patch_type([(F, C, I), (F, I, R), (F, R, S), (F, S, P), (F, C, B, P), (A, U, Z, V)], extra)
    for j in range(15):
        q = seed.plus((P, B, j))
        if not accept('endpoint-J', (j,), q):
            continue
        for k in range(15):
            qk = q.plus((C, B, U, k))
            if not accept('endpoint-K', (j, k), qk):
                continue
            need(k == Z, 'endpoint opposite is forced Z')
            for m in range(15):
                qm = qk.plus((C, Z, m, I))
                need(not accept('endpoint-M', (j, k, m), qm), 'endpoint completion')
    # Noncontacting: the one-T opposite of F has no three contact.
    seed = patch_type([(F, B, I), (F, I, R), (F, R, S), (F, S, P), (F, B, C, P), (A, U, Z, V)], extra)
    for j in range(15):
        q = seed.plus((P, C, j))
        if not accept('opposite-J', (j,), q):
            continue
        for k in range(15):
            qk = q.plus((B, C, k, U))
            need(not accept('opposite-K', (j, k), qk), 'opposite completion')
    # Contacting: D's two Qs are separated, so D has no three contact.
    families = [((A, B, C), (A, B, Z)), ((A, Z, B), (A, Z, C))]
    for fi, (un, vn) in enumerate(families):
        extra = [(U, x) for x in un] + [(V, x) for x in vn]
        a0, b0 = sorted(set(un) & set(vn))
        for pos in (1, 2):
            for slots in canonical_slots(4, 10):
                if pos == 1:
                    a, y, c, d = slots
                    b, x = 8, 9
                    fan = (a, D, b, x, y)
                else:
                    x, y, c, d = slots
                    a, b = 8, 9
                    fan = (x, a, D, b, y)
                faces = [(F, fan[k], fan[k + 1]) for k in range(4)] + [(D, c, d), (a0, U, b0, V)]
                for h, k, l in product((A, B, C, Z), repeat=3):
                    q = patch_type(faces + [(F, fan[0], h, fan[-1]), (D, b, k, c), (D, d, l, a)], extra, fd_contact=True, missing_capacity=missing_capacity)
                    good = accept('separated', (fi, pos, *slots, h, k, l), q)
                    if missing_capacity:
                        need(not good, 'separated-Q completion')
    # Contacting: D meets V along its QQ edge. Shared-oneT L was
    # geometrically excluded, leaving these two supplier families.
    families = [((A, Z, B), (D, A, Z)), ((A, B, Z), (D, C, Z))]
    for fi, (un, vn) in enumerate(families):
        extra = [(U, x) for x in un] + [(V, x) for x in vn]
        shared = set(un) & set(vn)
        sq = []
        if shared & {A, B, C}:
            a0, b0 = sorted(shared)
            sq = [(a0, U, b0, V)]
        for e, w in canonical_slots(2, 11):
            faces = [(F, I, D), (F, D, R), (F, R, S), (F, S, e), (D, I, w)] + sq
            for h, k, l in product((A, B, C, Z), repeat=3):
                key = (fi, e, w, h, k, l)
                q = patch_type(faces + [(F, I, h, e), (D, w, k, V), (D, V, l, R)], extra, fd_contact=True)
                if not accept('adjacent-initial', key, q):
                    continue
                for j in range(15):
                    qj = q.plus((I, w, j, h))
                    if not accept('adjacent-J', (*key, j), qj):
                        continue
                    for m in range(15):
                        qm = qj.plus((R, S, m, l))
                        need(not accept('adjacent-M', (*key, j, m), qm), 'adjacent-Q completion')
    serial = sorted(json.dumps(r, separators=(',', ':')) for r in records)
    return {'tested': dict(sorted(tested.items())), 'admitted': dict(sorted(admitted.items())), 'all_tested_case_sha256': hashlib.sha256(('\n'.join(serial) + '\n').encode()).hexdigest(), 'admitted_case_sha256': digest(sorted((r for r in records if r[2]), key=lambda r: json.dumps(r)))}


def evaluate(q):
    try:
        q.inspect()
    except Reject:
        return False
    return True


def build_report():
    rows, orbits = supplier_cover()
    collar, critical = collar_cover(rows)
    return {'claim': 'r2_a3_b1_f0_1_f1_1_f2_0_O7_excluded', 'supplier_rows': len(rows), 'supplier_orbits': orbits, 'collar': collar, 'critical_collar_rows': critical, 'paired_fans': paired_fans(), 'local_covers': all_covers(evaluate)}


def main():
    report = build_report()
    expected = json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
    need(report == expected, 'complete expected output mismatch')
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
