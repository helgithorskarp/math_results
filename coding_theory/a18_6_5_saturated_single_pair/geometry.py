#!/usr/bin/env python3
"""Exact first-plane normalization and finite-field geometry; stdlib only."""
import itertools


def multiply(a, b):
    value = 0
    while b:
        if b & 1:
            value ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return value


def word(points):
    return sum(1 << p for p in points)


def points(mask):
    return tuple(p for p in range(16) if mask >> p & 1)


def image(mask, permutation):
    return word(permutation[p] for p in points(mask))


def valid_plane(plane):
    return (len(plane) == len(set(plane)) == 20
            and all(0 <= b < (1 << 16) and b.bit_count() == 4 for b in plane)
            and all(sum(bool(b >> a & 1) and bool(b >> c & 1) for b in plane) == 1
                    for a, c in itertools.combinations(range(16), 2)))


def latin_squares():
    found = []
    def visit(rows):
        if len(rows) == 4:
            found.append(tuple(rows))
            return
        for row in itertools.permutations(range(4)):
            if all(all(row[c] != old[c] for old in rows) for c in range(4)):
                visit(rows + [row])
    visit([tuple(range(4))])
    return found


def normalization():
    plane = sorted([word(4*x+y for y in range(4)) for x in range(4)]
        + [word(4*x+(multiply(m,x)^b) for x in range(4))
           for m in range(4) for b in range(4)])
    if not valid_plane(plane):
        raise ValueError('invalid field plane')
    squares = latin_squares()
    orthogonal = lambda a,b: len({(a[r][c],b[r][c]) for r in range(4) for c in range(4)}) == 16
    triples = [t for t in itertools.combinations(range(len(squares)),3)
               if all(orthogonal(squares[a],squares[b]) for a,b in itertools.combinations(t,2))]
    grid = [word(4*r+c for c in range(4)) for r in range(4)]
    grid += [word(4*r+c for r in range(4)) for c in range(4)]
    planes = []
    for triple in triples:
        design = sorted(grid + [word(4*r+c for r in range(4) for c in range(4)
                                     if squares[i][r][c] == symbol)
                               for i in triple for symbol in range(4)])
        if not valid_plane(design):
            raise ValueError('invalid normalized plane')
        planes.append(design)
    maps = []
    for design in planes:
        found = None
        for rows,columns in itertools.product(itertools.permutations(range(4)),repeat=2):
            permutation = [4*rows[p//4]+columns[p%4] for p in range(16)]
            if sorted(image(b,permutation) for b in design) == plane:
                found = permutation
                break
        if found is None:
            raise ValueError('unnormalized affine plane')
        maps.append(found)
    if len(squares) != 24 or len(triples) != 2 or len(set(map(tuple,planes))) != 2:
        raise ValueError('unexpected complete Latin census')
    return {'normalized_latin_squares':len(squares), 'complete_orthogonal_triples':len(triples),
            'first_plane':plane, 'normalized_grid_planes':planes,
            'maps_to_first_plane':maps}


def automorphisms(plane):
    plane_set = set(plane)
    permutations = []
    for a,b,c,d in itertools.product(range(4),repeat=4):
        if multiply(a,d) == multiply(b,c):
            continue
        for tx,ty,power in itertools.product(range(4),range(4),range(2)):
            permutation = []
            for p in range(16):
                x,y = divmod(p,4)
                if power:
                    x,y = multiply(x,x),multiply(y,y)
                permutation.append(4*(multiply(a,x)^multiply(b,y)^tx)
                                   +(multiply(c,x)^multiply(d,y)^ty))
            permutation = tuple(permutation)
            if len(set(permutation)) != 16 or {image(b,permutation) for b in plane} != plane_set:
                raise ValueError('invalid first-plane symmetry')
            permutations.append(permutation)
    if len(set(permutations)) != len(permutations) or len(permutations) != 5760:
        raise ValueError('unexpected symmetry census')
    return permutations
