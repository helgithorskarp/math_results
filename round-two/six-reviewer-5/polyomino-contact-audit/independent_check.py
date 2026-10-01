"""six-reviewer-5: exact independent contact/phase/certificate audit.

Standard library only. No target imports, SAT calls or floating-point geometry.
The published CNF numbering/serialization is deliberately retained so its
untrusted RUP evidence can be checked against geometrically rebuilt inputs.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(x):
    return hashlib.sha256(x).hexdigest()


# Enumeration by images of the two coordinate basis vectors.
D4 = sorted((u[0], v[0], u[1], v[1])
            for u in [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for v in [(1, 0), (-1, 0), (0, 1), (0, -1)]
            if u[0]*v[0] + u[1]*v[1] == 0)


def linear(g, x, y):
    a, b, c, d = g
    return a*x+b*y, c*x+d*y


def orient(cells, g):
    # Transform actual square vertices, instead of a corner correction formula.
    raw = []
    for x, y in cells:
        verts = [linear(g, x+i, y+j) for i, j in product((0, 1), repeat=2)]
        raw.append((min(p[0] for p in verts), min(p[1] for p in verts)))
    lo = min(x for x, y in raw), min(y for x, y in raw)
    return tuple(sorted((x-lo[0], y-lo[1]) for x, y in raw)), lo


def sigma(t):
    n = t.numerator // t.denominator
    return Q(n) if t == n else Q(2*n+1, 2)


class Tile:
    def __init__(self, cells):
        self.cells = tuple(sorted(map(tuple, cells)))
        need(len(set(self.cells)) == len(self.cells), 'duplicate cell')
        need(all(type(x) is int and type(y) is int for x, y in self.cells), 'noninteger cell')
        need(min(x for x, y in self.cells) == min(y for x, y in self.cells) == 0,
             'unnormalized tile')
        # Cancel shared square edges. A single simple boundary cycle certifies
        # the disc hypothesis; holes give multiple cycles, pinches degree four.
        boundary = set()
        for x, y in self.cells:
            vs = [(x, y), (x+1, y), (x+1, y+1), (x, y+1)]
            for a, b in zip(vs, vs[1:]+vs[:1]):
                e = tuple(sorted((a, b)))
                if e in boundary:
                    boundary.remove(e)
                else:
                    boundary.add(e)
        links = {}
        for a, b in boundary:
            links.setdefault(a, set()).add(b)
            links.setdefault(b, set()).add(a)
        need(links and all(len(ns) == 2 for ns in links.values()), 'pinched tile')
        reached, stack = set(), [next(iter(links))]
        while stack:
            p = stack.pop()
            if p not in reached:
                reached.add(p)
                stack.extend(links[p]-reached)
        need(len(reached) == len(links), 'multiple boundary components')
        self.os = sorted({orient(self.cells, g)[0] for g in D4})
        self.root = (self.os.index(self.cells), Q(0), Q(0))
        self.frames = {i: [(g, lo) for g in D4
                          for o, lo in [orient(self.cells, g)] if o == s]
                       for i, s in enumerate(self.os)}
        self.m = len(self.cells)
        self.w = max(x for x, y in self.cells)+1
        self.h = max(y for x, y in self.cells)+1
        self.L = max(self.w, self.h)

    def anchors(self, p):
        o, x, y = p
        return [(a+x, b+y) for a, b in self.os[o]]

    def rel(self, A, B):
        # Closed interval intersection, with interior intersection separate.
        touching = False
        for ax, ay in self.anchors(A):
            for bx, by in self.anchors(B):
                dx = min(ax+1, bx+1)-max(ax, bx)
                dy = min(ay+1, by+1)-max(ay, by)
                if dx > 0 and dy > 0:
                    return 'overlap'
                touching |= dx >= 0 and dy >= 0
        return 'contact' if touching else 'separate'

    def typ(self, A, B, frame=0):
        # Pull every physical square of B back through an actual isometry P->A.
        g, lo = self.frames[A[0]][frame]
        gi = (g[0], g[2], g[1], g[3])
        origin = A[1]-lo[0], A[2]-lo[1]
        raw = []
        for x, y in self.anchors(B):
            verts = [linear(gi, x+i-origin[0], y+j-origin[1])
                     for i, j in product((0, 1), repeat=2)]
            raw.append((min(p[0] for p in verts), min(p[1] for p in verts)))
        x0, y0 = min(x for x, y in raw), min(y for x, y in raw)
        shape = tuple(sorted((x-x0, y-y0) for x, y in raw))
        return self.os.index(shape), int(2*sigma(x0)), int(2*sigma(y0))

    def budget(self, B):
        a = self.anchors(self.root)+self.anchors(B)
        w = max(x for x, y in a)+1-min(x for x, y in a)
        h = max(y for x, y in a)+1-min(y for x, y in a)
        return int((w+2*self.L)*(h+2*self.L)//self.m)

    def pixels(self, p, dx, dy=None):
        dy = dx if dy is None else dy
        a = self.anchors(p)
        need(all((x*dx).denominator == (y*dy).denominator == 1 for x, y in a),
             'pose off mesh')
        return {(int(x*dx)+i, int(y*dy)+j) for x, y in a
                for i in range(dx) for j in range(dy)}


def halo(cells):
    return {(x+i, y+j) for x, y in cells
            for i, j in product((-1, 0, 1), repeat=2)} - cells


def contact_pool(t, fixed, scale, domain=None):
    """Complete pool by Minkowski closed/open rectangle translation sets.

    A unit-square pair contacts on a lattice iff its translation belongs to
    the closed separation rectangle and to no open-overlap rectangle. Union
    these sets over constituent squares; no halo incidence generates poses.
    """
    old = [(int(x*scale), int(y*scale)) for p in fixed for x, y in t.anchors(p)]
    pool = []
    for o, shape in enumerate(t.os):
        closed, opened = set(), set()
        for a, b in shape:
            for u, v in old:
                x, y = u-a*scale, v-b*scale
                closed.update(product(range(x-scale, x+scale+1),
                                      range(y-scale, y+scale+1)))
                opened.update(product(range(x-scale+1, x+scale),
                                      range(y-scale+1, y+scale)))
        for x, y in sorted(closed-opened):
            p = o, Q(x, scale), Q(y, scale)
            if domain is None or all(t.rel(A, p) != 'contact' or
                                    t.typ(p, A) in domain for A in fixed):
                pool.append((p, t.pixels(p, scale)))
    return pool


def compile_input(t, fixed, scale, domain=None):
    if domain is not None:
        check_patch(t, fixed, fixed, domain, collar=False)
    pool = contact_pool(t, fixed, scale, domain)
    old = set().union(*(t.pixels(p, scale) for p in fixed))
    owners = {}
    for v, (p, pix) in enumerate(pool, 1):
        for q in pix:
            owners.setdefault(q, []).append(v)
    nv = len(pool)
    cs = []
    # Published sequential AMO extension. Its projection is exactly <=1 owner.
    for q in sorted(owners):
        vs = owners[q]
        if len(vs) == 2:
            cs.append([-vs[0], -vs[1]])
        elif len(vs) > 2:
            ss = list(range(nv+1, nv+len(vs)))
            nv += len(ss)
            cs.append([-vs[0], ss[0]])
            for k in range(1, len(vs)-1):
                cs += [[-vs[k], ss[k]], [-ss[k-1], ss[k]], [-vs[k], -ss[k-1]]]
            cs.append([-vs[-1], -ss[-1]])
    cs += [owners.get(q, []) for q in sorted(halo(old))]
    if domain is not None:
        for i, (A, _) in enumerate(pool):
            for j in range(i):
                B = pool[j][0]
                if t.rel(A, B) == 'contact' and t.typ(A, B) not in domain:
                    cs.append([-i-1, -j-1])
    return pool, cs, nv


def dimacs(cs, nv):
    return ('p cnf %d %d\n' % (nv, len(cs))+''.join(
        ' '.join(map(str, c))+' 0\n' for c in cs)).encode()


def propagate(cs, assumed):
    """Independent full-clause scan, no watched literals or occurrence table."""
    truth, false = set(), set()
    def put(p):
        if -p in truth:
            return False
        truth.add(p)
        false.add(-p)
        return True
    for p in assumed:
        if not put(p):
            return True
    while True:
        before = len(truth)
        for c in cs:
            if truth.intersection(c):
                continue
            free = set(c)-false
            if not free:
                return True
            if len(free) == 1 and not put(next(iter(free))):
                return True
        if len(truth) == before:
            return False


class CountdownProbe:
    """Clause falsification counters; the scan checker above is a control.

    Rows keep immutable signed sets. Processing a true literal disables its
    satisfied clauses and decrements counts in clauses containing its negation.
    A remaining count of one is a unit; zero is contradiction. Counts are
    rebuilt for each probe; proved clauses extend the incidence index.
    """
    def __init__(self, cs):
        self.rows, self.incidence, self.units = [], {}, []
        self.empty = False
        for c in cs:
            self.add(c)

    def add(self, c):
        c = frozenset(c)
        i = len(self.rows)
        self.rows.append(c)
        for p in c:
            self.incidence.setdefault(p, []).append(i)
        if len(c) == 1:
            self.units.append(next(iter(c)))
        self.empty |= not c

    def conflict(self, assumed):
        if self.empty:
            return True
        left = [len(c) for c in self.rows]
        live = bytearray([1])*len(left)
        true, false, queue = set(), set(), []
        def enqueue(p):
            if p in false:
                return False
            if p not in true:
                true.add(p)
                false.add(-p)
                queue.append(p)
            return True
        for p in list(assumed)+self.units:
            if not enqueue(p):
                return True
        head = 0
        while head < len(queue):
            p = queue[head]
            head += 1
            for i in self.incidence.get(p, []):
                live[i] = 0
            for i in self.incidence.get(-p, []):
                if not live[i]:
                    continue
                left[i] -= 1
                if left[i] == 0:
                    return True
                if left[i] == 1:
                    free = self.rows[i]-false
                    if not free or not enqueue(next(iter(free))):
                        return True
        return False


def rup(cs, nv, path, final_empty):
    checker = CountdownProbe(cs)
    added = []
    for line in path.read_text().splitlines():
        ws = line.split()
        need(ws and ws[0] != 'd', 'this audit expects additions only')
        nums = list(map(int, ws))
        need(nums[-1] == 0 and 0 not in nums[:-1], 'bad terminator')
        c = frozenset(nums[:-1])
        need(all(0 < abs(x) <= nv for x in c), 'bad variable')
        need(checker.conflict([-x for x in c]), 'step is not RUP')
        checker.add(c)
        added.append(c)
    need(bool(added), 'empty proof')
    if final_empty:
        need(not added[-1], 'no final contradiction')
    return added


def boolean_controls():
    clauses = [frozenset(p for p in row if p)
               for row in product((-1, 0, 1), (-2, 0, 2))]
    checks = 0
    for mask in range(1 << len(clauses)):
        cs = [c for i, c in enumerate(clauses) if mask >> i & 1]
        indexed = CountdownProbe(cs)
        for row in product((-1, 0, 1), (-2, 0, 2)):
            assumptions = [p for p in row if p]
            need(indexed.conflict(assumptions) == propagate(cs, assumptions),
                 'countdown/scan propagation disagreement')
            if indexed.conflict(assumptions):
                need(not any(all(any(p in truth for p in c) for c in cs)
                             for bits in product((False, True), repeat=2)
                             for truth in [{i+1 if bit else -i-1 for i, bit in enumerate(bits)}]
                             if set(assumptions) <= truth), 'unsound conflict')
            checks += 1
    amo = 0
    for n in range(2, 6):
        ss = list(range(n+1, 2*n))
        cs = [[-1, ss[0]]]
        for i in range(1, n-1):
            cs += [[-i-1, ss[i]], [-ss[i-1], ss[i]], [-i-1, -ss[i-1]]]
        cs += [[-n, -ss[-1]]]
        for primary in product((False, True), repeat=n):
            extendible = False
            for aux in product((False, True), repeat=n-1):
                truth = {i+1 if bit else -i-1 for i, bit in enumerate(primary+aux)}
                extendible |= all(any(p in truth for p in c) for c in cs)
            need(extendible == (sum(primary) <= 1), 'sequential AMO projection')
            amo += 1
    return dict(propagation_comparisons=checks, AMO_primary_assignments=amo)


def strict_collar(t, fixed, poses):
    # Original rational rectangle arrangement; no pixel rasterization required.
    old = [q for p in fixed for q in t.anchors(p)]
    allq = [q for p in poses for q in t.anchors(p)]
    xs = sorted({x+i for x, y in allq for i in (0, 1)})
    ys = sorted({y+i for x, y in allq for i in (0, 1)})
    xs = [xs[0]-1]+xs+[xs[-1]+1]
    ys = [ys[0]-1]+ys+[ys[-1]+1]
    def faces(qs):
        result = set()
        for i in range(len(xs)-1):
            x = (xs[i]+xs[i+1])/2
            for j in range(len(ys)-1):
                y = (ys[j]+ys[j+1])/2
                if any(a < x < a+1 and b < y < b+1 for a, b in qs):
                    result.add((i, j))
        return result
    op, ap = faces(old), faces(allq)
    return halo(op) <= ap


def check_patch(t, fixed, poses, domain=None, collar=True):
    need(all(p in poses for p in fixed), 'missing fixed tile')
    for i, A in enumerate(poses):
        for B in poses[:i]:
            r = t.rel(A, B)
            need(r != 'overlap', 'overlap')
            if domain is not None and r == 'contact':
                need(all(t.typ(A, B, k) in domain for k in range(len(t.frames[A[0]])))
                     and all(t.typ(B, A, k) in domain for k in range(len(t.frames[B[0]]))),
                     'forbidden type')
    if collar:
        need(strict_collar(t, fixed, poses), 'exposed fixed boundary')


def pose_rows(rows):
    return [(int(o), Q(x), Q(y)) for o, x, y in rows]


def compress(poses, M, anisotropic=True):
    need(M >= len(poses) and M >= 2, 'bad budget')
    need(poses[0][1:] == (0, 0), 'first fixed root')
    need(all(poses[1][j] % 1 in (0, Q(1, 2)) for j in (1, 2)), 'bad pair phase')
    out = [list(p) for p in poses]
    ds = []
    for j in (1, 2):
        anchor = poses[1][j] % 1
        D = (M-1) if anisotropic and anchor == 0 else 2*(M-1)
        ds.append(D)
        phases = sorted({p[j] % 1 for p in poses})
        mp = {Q(0): Q(0)}
        if anchor:
            mp[anchor] = anchor
            for a, b in ((Q(0), anchor), (anchor, Q(1))):
                for i, p in enumerate([p for p in phases if a < p < b], 1):
                    need(a+Q(i, D) < b, 'anchor interval overflow')
                    mp[p] = a+Q(i, D)
        else:
            for i, p in enumerate([p for p in phases if p > 0], 1):
                need(Q(i, D) < 1, 'phase interval overflow')
                mp[p] = Q(i, D)
        for i, p in enumerate(poses):
            out[i][j] = p[j]//1 + mp[p[j] % 1]
    result = list(map(tuple, out))
    need(result[:2] == poses[:2], 'moved literal pair')
    return result, tuple(ds)


def failed(f):
    try:
        f()
    except ValueError:
        return 1
    raise ValueError('corruption accepted')


def calibration(t, data):
    root = t.root
    E0 = {tuple([p[0], int(2*p[1]), int(2*p[2])])
          for p, _ in contact_pool(t, [root], 2)}
    pool, cs, nv = compile_input(t, [root], 2)
    need(digest(dimacs(cs, nv)) == data['root_cnf_sha256'], 'root CNF mismatch')
    print('root input rebuilt', len(pool), len(cs), nv, file=sys.stderr, flush=True)
    proof = rup(cs, nv, HERE/'support.rup', False)
    print('support proof checked', file=sys.stderr, flush=True)
    F = set(map(tuple, data['F']))
    covered = set()
    for poses in map(pose_rows, data['first_witnesses']):
        check_patch(t, [root], poses)
        for B in poses[1:]:
            need(t.rel(root, B) == 'contact', 'useless root witness tile')
            covered.add(t.typ(root, B))
    need(covered == F, 'positive support coverage')
    need(all(frozenset([-v]) in proof for v, (p, _) in enumerate(pool, 1)
             if (p[0], int(2*p[1]), int(2*p[2])) not in F), 'missing support exclusion')
    reciprocal = {z for z in F if t.typ((z[0], Q(z[1], 2), Q(z[2], 2)), root) in F}
    need(reciprocal == {tuple(r['type']) for r in data['pairs']}, 'pair inventory')
    E1 = set()
    pairs, steps, allvars, allclauses = [], 0, 0, 0
    for pair_index, record in enumerate(data['pairs']):
        o, x, y = record['type']
        B = o, Q(x, 2), Q(y, 2)
        pp, cc, nn = compile_input(t, [root, B], 4)
        need(digest(dimacs(cc, nn)) == record['cnf_sha256'], 'pair CNF mismatch')
        allvars += nn
        allclauses += len(cc)
        if record['sat']:
            poses = pose_rows(record['poses'])
            check_patch(t, [root, B], poses)
            E1.add(tuple(record['type']))
            need(all(p in dict(pp) for p in poses[2:]), 'witness outside complete pool')
        else:
            steps += len(rup(cc, nn, HERE/record['proof'], True))
        pairs.append([len(pp), len(cc), nn, record['sat']])
        print('pair checked', pair_index, file=sys.stderr, flush=True)
    need(all(x % 2 == y % 2 == 0 for o, x, y in E1), 'nonintegral E1')
    for z in E1:
        B = z[0], Q(z[1], 2), Q(z[2], 2)
        need(all(t.typ(root, B, k) in E1 for k in range(len(t.frames[root[0]])))
             and all(t.typ(B, root, k) in E1 for k in range(len(t.frames[B[0]]))),
             'E1 not closed')
    pp, cc, nn = compile_input(t, [root], 1, E1)
    need(digest(dimacs(cc, nn)) == data['final_root']['cnf_sha256'], 'final CNF mismatch')
    final = rup(cc, nn, HERE/'root-E1.rup', True)
    # A second encoding with only pairwise overlap clauses is rejected by
    # empty cover clauses as well, without any auxiliary extension variables.
    old = t.pixels(root, 1)
    uncovered = halo(old)-set().union(*(p for _, p in pp))
    need(bool(uncovered), 'missing direct final geometric obstruction')
    controls = failed(lambda: check_patch(t, [root], [root, root]))
    controls += failed(lambda: check_patch(t, [root], [root]))
    controls += failed(lambda: need(propagate([frozenset([1, 2])], [-1]), 'bad RUP'))
    controls += failed(lambda: need(len(pp[:-1]) == len(contact_pool(t, [root], 1, E1)),
                                   'missing candidate'))
    return dict(E0=len(E0), F=len(F), reciprocal=len(reciprocal), E1=len(E1),
                support_steps=len(proof), pair_steps=steps, pairs=pairs,
                final_pool=len(pp), final_variables=nn, final_clauses=len(cc),
                final_steps=len(final), uncovered_pixels=sorted(map(list, uncovered)),
                rejected_controls=controls, total_pair_variables=allvars,
                total_pair_clauses=allclauses)


def phase_controls():
    patterns, signs = 0, 0
    for M in range(2, 8):
        for anchor in (Q(0), Q(1, 2)):
            available = [Q(i, 8) for i in range(1, 8) if Q(i, 8) != anchor]
            for k in range(min(M-2, len(available))+1):
                for ps in combinations(available, k):
                    poses = [(0, Q(0), Q(0)), (0, anchor, Q(0))]
                    poses += [(0, x-2, x+1) for x in ps]
                    mapped, ds = compress(poses, M)
                    need(ds[0] == (M-1)*(2 if anchor else 1), 'wrong smaller mesh')
                    for j in (1, 2):
                        for A, a in zip(poses, mapped):
                            for B, b in zip(poses, mapped):
                                # sigma of signed differences records every integer threshold.
                                need(sigma(A[j]-B[j]) == sigma(a[j]-b[j]), 'changed type')
                                for n in range(-4, 5):
                                    s = lambda z: (z > 0)-(z < 0)
                                    need(s(A[j]-B[j]-n) == s(a[j]-b[j]-n), 'changed sign')
                                    signs += 1
                    patterns += 1
    return patterns, signs


def domino_fixture():
    t = Tile([(0, 0), (1, 0)])
    o = t.root[0]
    fixed = [t.root, (o, Q(2), Q(1, 2))]
    poses = fixed[:]
    for x, f in ((-2, Q(1, 7)), (0, Q(0)), (2, Q(1, 2)), (4, Q(5, 7))):
        for k in (-1, 0, 1):
            p = o, Q(x), f+k
            if p not in fixed and all(t.rel(p, A) != 'overlap' for A in fixed) \
                    and any(t.rel(p, A) == 'contact' for A in fixed):
                poses.append(p)
    domain = {(o, 0, 2), (o, 0, -2)} | {(o, x, y) for x in (-4, 4) for y in (-1, 1)}
    M = t.budget(fixed[1])
    check_patch(t, fixed, poses, domain)
    comp, ds = compress(poses, M)
    check_patch(t, fixed, comp, domain)
    edges = 0
    for i, A in enumerate(poses):
        for j, B in enumerate(poses[:i]):
            need(t.rel(A, B) == t.rel(comp[i], comp[j]), 'contact changed')
            for frame in range(len(t.frames[A[0]])):
                need(t.typ(A, B, frame) == t.typ(comp[i], comp[j], frame), 'frame changed')
            edges += t.rel(A, B) == 'contact'
    old = set().union(*(t.pixels(p, *ds) for p in fixed))
    full = set().union(*(t.pixels(p, *ds) for p in comp))
    need(halo(old) <= full, 'anisotropic raster collar')
    naive = [(p[0], sigma(p[1]), sigma(p[2])) for p in poses]
    bad = failed(lambda: check_patch(t, fixed, naive, domain))
    bad += failed(lambda: compress(poses, len(poses)-1))
    bad += failed(lambda: compress([fixed[0], (o, Q(2), Q(1, 3))]+poses[2:], M))
    # An integral fixed-pair example whose added rows have distinct phases.
    s = Tile([(0, 0)])
    sf = [s.root, (0, Q(0), Q(1))]
    patch = sf+[(0, Q(x), Q(y)) for y in (0, 1) for x in (-1, 1)]
    patch += [(0, Q(x)+f, Q(y)) for y, f in ((-1, Q(1, 7)), (2, Q(3, 7)))
              for x in (-1, 0, 1)]
    check_patch(s, sf, patch)
    mp, dd = compress(patch, s.budget(sf[1]))
    check_patch(s, sf, mp)
    need(dd == (11, 11), 'integral-pair reduction')
    return dict(copies=len(poses), contacts=edges, M=M, anisotropic=list(ds),
                integral_pair_mesh=list(dd), rejected_controls=bad)


def main():
    provenance = json.loads((HERE/'inputs.json').read_text())
    for name, rec in provenance['inputs'].items():
        raw = (HERE/name).read_bytes()
        need(digest(raw) == rec['sha256'] and len(raw) == rec['bytes'], 'input changed: '+name)
    cases = json.loads((HERE/'cases.json').read_text())
    invent = []
    small_tiles = [[(0, 0)], [(0, 0), (1, 0)]] + cases['published_heptominoes']
    for cells in small_tiles + [cases['record_seed_17']]:
        t = Tile(cells)
        pool = contact_pool(t, [t.root], 2)
        E = sorted((p[0], int(2*p[1]), int(2*p[2])) for p, _ in pool)
        for z in E:
            B = z[0], Q(z[1], 2), Q(z[2], 2)
            need(t.rel(t.root, B) == 'contact', 'bad universe')
            need(z[1] % 2 == 0 or z[2] % 2 == 0, 'two floating axes')
            for k in range(len(t.frames[B[0]])):
                need(t.typ(B, t.root, k) in E, 'reciprocity frame')
            for k in range(len(t.frames[t.root[0]])):
                need(t.typ(t.root, B, k) in E, 'stabilizer frame')
        invent.append(dict(cells=t.m, orientations=len(t.os),
                           types=len(E), floating=sum(x % 2 or y % 2 for o, x, y in E),
                           largest_M=max(t.budget((o, Q(x, 2), Q(y, 2))) for o, x, y in E),
                           root_M=(t.w+2*t.L)*(t.h+2*t.L)//t.m,
                           sha256=digest(json.dumps([list(z) for z in E], separators=(',', ':')).encode())))
        print('inventory checked', t.m, len(E), file=sys.stderr, flush=True)
    # Published primary data are literal coordinates, not input expected statuses.
    data = (HERE/'07omino_0up.txt').read_text().splitlines()
    for i in range(3):
        words = data[2*i].split()
        coords = list(map(int, words))
        need(sorted(zip(coords[::2], coords[1::2])) == sorted(map(tuple, small_tiles[i+2])),
             'primary seven-cell coordinates differ')
    data = json.loads((HERE/'calibration.json').read_text())
    t = Tile(small_tiles[data['shape_index']+2])
    result = dict(agent='six-reviewer-5', role='independent mathematical reviewer',
                  inventories=invent, calibration=calibration(t, data),
                  phase_patterns_and_threshold_signs=list(phase_controls()),
                  phase_fixture=domino_fixture(), boolean_controls=boolean_controls(),
                  rejected_tile_controls=failed(lambda: Tile([(0, 0), (1, 1)]))
                  +failed(lambda: Tile([(x, y) for x, y in product(range(3), repeat=2)
                                        if (x, y) != (1, 1)]))
                  +failed(lambda: Tile([(0, 0), (0, 0)])))
    encoded = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if '--write-expected' in sys.argv:
        (HERE/'expected.json').write_text(encoded)
    else:
        need(encoded == (HERE/'expected.json').read_text(), 'output differs from expected')
    print(encoded, end='')


if __name__ == '__main__':
    main()
