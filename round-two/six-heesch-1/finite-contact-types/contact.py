"""Exact square-polyomino contacts and anchored phase normalization.

No floating point and no solver. A pose is (normalized-orientation-index,x,y).
A contact type stores (orientation-index,2*sigma(x),2*sigma(y)).
"""
from fractions import Fraction as Q
from itertools import product


def require(ok, message):
    if not ok:
        raise ValueError(message)


MATRICES = tuple((a, b, c, d) for a, b, c, d in product((-1, 0, 1), repeat=4)
                 if a*a+b*b == c*c+d*d == 1 and a*c+b*d == 0)


def mv(g, p):
    a, b, c, d = g
    return (a*p[0]+b*p[1], c*p[0]+d*p[1])


def transpose(g):
    a, b, c, d = g
    return a, c, b, d


def transform(cells, g):
    """Geometric unit-square image; signed axes require a unit-cell shift."""
    a, b, c, d = g
    sx, sy = min(a, b, 0), min(c, d, 0)
    raw = [mv(g, p) for p in cells]
    raw = [(x+sx, y+sy) for x, y in raw]
    lo = min(x for x, y in raw), min(y for x, y in raw)
    return tuple(sorted((x-lo[0], y-lo[1]) for x, y in raw)), lo


def sigma(x):
    x = Q(x)
    n = x.numerator // x.denominator
    return x if x == n else Q(n)+Q(1, 2)


def halo(pixels):
    return {(x+dx, y+dy) for x, y in pixels
            for dx, dy in product((-1, 0, 1), repeat=2)} - set(pixels)


class Tile:
    def __init__(self, cells):
        require(bool(cells) and len(set(map(tuple, cells))) == len(cells),
                'empty or duplicate cells')
        require(all(len(p) == 2 and all(type(z) is int for z in p) for p in cells),
                'noninteger cells')
        self.cells = tuple(sorted(map(tuple, cells)))
        require(min(x for x, y in self.cells) == min(y for x, y in self.cells) == 0,
                'tile must be normalized')
        self.orientations = tuple(sorted({transform(self.cells, g)[0] for g in MATRICES}))
        self.indices = {o: i for i, o in enumerate(self.orientations)}
        self.frames = tuple(tuple((g, (-lo[0], -lo[1])) for g in MATRICES
                                  for shape, lo in [transform(self.cells, g)] if shape == o)
                            for o in self.orientations)
        self.root = (self.indices[self.cells], Q(0), Q(0))
        self.m = len(self.cells)
        self.w = max(x for x, y in self.cells)+1
        self.h = max(y for x, y in self.cells)+1
        self.L = max(self.w, self.h)

    def anchors(self, pose):
        o, x, y = pose
        require(type(o) is int and 0 <= o < len(self.orientations), 'invalid orientation')
        return tuple((Q(x)+a, Q(y)+b) for a, b in self.orientations[o])

    def pixels(self, pose, scale):
        require(type(scale) is int and scale > 0, 'invalid pixel scale')
        result = set()
        for x, y in self.anchors(pose):
            require((x*scale).denominator == (y*scale).denominator == 1,
                    'pose outside pixel mesh')
            result.update((int(x*scale)+i, int(y*scale)+j)
                          for i, j in product(range(scale), repeat=2))
        return result

    def relation(self, A, B):
        """Independent unit-rectangle geometry: overlap, contact, or separated."""
        touches = False
        for x, y in self.anchors(A):
            for u, v in self.anchors(B):
                dx, dy = abs(x-u), abs(y-v)
                if dx < 1 and dy < 1:
                    return 'overlap'
                if dx <= 1 and dy <= 1:
                    touches = True
        return 'contact' if touches else 'separated'

    def relative_type(self, A, B, frame_index=0):
        """Transport B to A's root frame; round each relative phase to sigma."""
        g, b = self.frames[A[0]][frame_index]
        gi = transpose(g)
        shape, lo = transform(self.orientations[B[0]], gi)
        x, y = mv(gi, (Q(B[1])-Q(A[1])-b[0], Q(B[2])-Q(A[2])-b[1]))
        return self.indices[shape], int(2*sigma(x+lo[0])), int(2*sigma(y+lo[1]))

    def pose(self, contact_type):
        o, x, y = contact_type
        return o, Q(x, 2), Q(y, 2)

    def universe(self):
        """Halo-incidence enumeration of all distinct physical half-grid contacts."""
        root = self.pixels(self.root, 2)
        targets = halo(root)
        result = set()
        for o in range(len(self.orientations)):
            op = self.pixels((o, 0, 0), 2)
            shifts = {(q[0]-p[0], q[1]-p[1]) for q in targets for p in op}
            for x, y in shifts:
                p = {(a+x, b+y) for a, b in op}
                if root.isdisjoint(p):
                    result.add((o, x, y))
        return result

    def universe_rectangles(self):
        """Separate completeness audit via bounding boxes and exact rectangles."""
        result = set()
        for o, shape in enumerate(self.orientations):
            w, h = max(x for x, y in shape)+1, max(y for x, y in shape)+1
            for x in range(-2*w, 2*self.w+1):
                for y in range(-2*h, 2*self.h+1):
                    if self.relation(self.root, (o, Q(x, 2), Q(y, 2))) == 'contact':
                        result.add((o, x, y))
        return result

    def pair_budget(self, B):
        anchors = self.anchors(self.root)+self.anchors(B)
        W = max(x for x, y in anchors)-min(x for x, y in anchors)+1
        H = max(y for x, y in anchors)-min(y for x, y in anchors)+1
        bound = (W+2*self.L)*(H+2*self.L)/self.m
        return bound.numerator // bound.denominator


def compress(poses, budget, fixed=2):
    """Periodic increasing homeomorphism sampled on finitely many phases.

    Only translation phases are needed: adding any integer gives the same map.
    The first two poses have phases zero or one-half and remain literally fixed.
    """
    require(type(budget) is int and budget >= max(len(poses), 2), 'insufficient copy budget')
    require(fixed in (1, 2) and len(poses) >= fixed, 'invalid fixed prefix')
    D = 2*(budget-1) if fixed == 2 else budget
    output = [list(p) for p in poses]
    for axis in (1, 2):
        phases = sorted({Q(p[axis]) % 1 for p in poses})
        anchors = {Q(p[axis]) % 1 for p in poses[:fixed]} | {Q(0)}
        require(anchors <= {Q(0), Q(1, 2)} and Q(poses[0][axis]) % 1 == 0,
                'fixed poses need integral or half-integral phases')
        mapping = {Q(0): Q(0)}
        if Q(1, 2) in anchors:
            mapping[Q(1, 2)] = Q(1, 2)
            for lo, hi in ((Q(0), Q(1, 2)), (Q(1, 2), Q(1))):
                for rank, phase in enumerate((p for p in phases if lo < p < hi), 1):
                    mapping[phase] = lo+Q(rank, D)
        else:
            for rank, phase in enumerate((p for p in phases if p > 0), 1):
                mapping[phase] = Q(rank, D)
        require(all(0 <= mapping[p] < 1 for p in phases) and
                all(mapping[a] < mapping[b] for a, b in zip(phases, phases[1:])),
                'phase map not strictly increasing')
        for old, new in zip(poses, output):
            x = Q(old[axis])
            new[axis] = x//1 + mapping[x % 1]
    result = [tuple(p) for p in output]
    require(result[:fixed] == [tuple(p) for p in poses[:fixed]], 'fixed prefix changed')
    return D, result


def check_patch(tile, fixed, poses, domain=None, scale=None):
    """Exact geometry and domain check, plus pixel strict containment if requested."""
    require(poses[:len(fixed)] == fixed, 'fixed prefix mismatch')
    contacts = []
    for i, A in enumerate(poses):
        for j, B in enumerate(poses[:i]):
            rel = tile.relation(A, B)
            require(rel != 'overlap', 'overlapping copies')
            if rel == 'contact':
                t = tile.relative_type(A, B)
                require(domain is None or t in domain, 'forbidden contact')
                contacts.append((j, i, t))
    if scale is not None:
        old = set().union(*(tile.pixels(p, scale) for p in fixed))
        occupied = set().union(*(tile.pixels(p, scale) for p in poses))
        require(halo(old) <= occupied, 'fixed union not strictly surrounded')
    return contacts
