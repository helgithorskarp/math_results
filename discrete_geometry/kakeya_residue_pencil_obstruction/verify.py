#!/usr/bin/env python3
"""Exact corroboration of PROOF.md; CPython 3.11+, standard library only."""
import argparse
from itertools import product
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


class Field:
    """Prime fields, and F_9=F_3[i]/(i^2+1), with explicit arithmetic."""
    def __init__(self, p, degree=1):
        require(p in (3, 5, 7, 11) and degree in (1, 2), 'unsupported field')
        require(degree == 1 or p == 3, 'quadratic fixture must be F9')
        self.p, self.degree, self.q = p, degree, p ** degree
        self.add = [[self.calc(a, b, False) for b in range(self.q)] for a in range(self.q)]
        self.mul = [[self.calc(a, b, True) for b in range(self.q)] for a in range(self.q)]
        self.neg = [next(b for b in range(self.q) if self.add[a][b] == 0)
                    for a in range(self.q)]
        self.squares = {self.mul[a][a] for a in range(self.q)}
        for a in range(1, self.q):
            require(any(self.mul[a][b] == 1 for b in range(self.q)), 'not a field')

    def calc(self, a, b, multiply):
        p = self.p
        if self.degree == 1:
            return (a * b if multiply else a + b) % p
        a0, a1, b0, b1 = a % p, a // p, b % p, b // p
        if multiply:
            return (a0 * b0 - a1 * b1) % p + p * ((a0 * b1 + a1 * b0) % p)
        return (a0 + b0) % p + p * ((a1 + b1) % p)


class Ring:
    """Z/p^2, dual numbers over F_q, or (Z/9)[i]/(i^2+1)."""
    def __init__(self, field, kind):
        f = field
        self.f, self.q, self.n, self.kind = f, f.q, f.q ** 2, kind
        require(kind in ('integer', 'dual', 'galois'), 'unsupported ring')
        require(kind != 'integer' or f.degree == 1, 'integer residue must be prime')
        require(kind != 'galois' or f.q == 9, 'Galois fixture must have residue F9')
        self.pi = f.p if kind != 'dual' else f.q
        self.name = ('Z/' + str(self.n) if kind == 'integer' else
                     'F' + str(f.q) + '[e]/e^2' if kind == 'dual' else 'GR(9,2)')
        self.add = [[self.calc(a, b, False) for b in range(self.n)] for a in range(self.n)]
        self.mul = [[self.calc(a, b, True) for b in range(self.n)] for a in range(self.n)]
        self.neg = [next(b for b in range(self.n) if self.add[a][b] == 0)
                    for a in range(self.n)]
        self.inv = {a: next(b for b in range(self.n) if self.mul[a][b] == 1)
                    for a in range(self.n) if self.res(a)}
        self.lifts = [self.lift(a) for a in range(self.q)]
        self.ideal = [self.mul[self.pi][a] for a in self.lifts]
        self.four = self.add[self.add[1][1]][self.add[1][1]]
        require(len(set(self.ideal)) == self.q and self.mul[self.pi][self.pi] == 0,
                'invalid length-two ideal')
        require(set(self.ideal) == {a for a in range(self.n) if not self.res(a)},
                'ideal is not the residue kernel')
        for a, b in product(range(self.n), repeat=2):
            require(self.res(self.add[a][b]) == f.add[self.res(a)][self.res(b)] and
                    self.res(self.mul[a][b]) == f.mul[self.res(a)][self.res(b)],
                    'residue map is not a homomorphism')

    def calc(self, a, b, multiply):
        if self.kind == 'integer':
            return (a * b if multiply else a + b) % self.n
        if self.kind == 'dual':
            q, f = self.q, self.f
            a0, a1, b0, b1 = a % q, a // q, b % q, b // q
            if multiply:
                return f.mul[a0][b0] + q * f.add[f.mul[a0][b1]][f.mul[a1][b0]]
            return f.add[a0][b0] + q * f.add[a1][b1]
        m = 9
        a0, a1, b0, b1 = a % m, a // m, b % m, b // m
        if multiply:
            return (a0 * b0 - a1 * b1) % m + m * ((a0 * b1 + a1 * b0) % m)
        return (a0 + b0) % m + m * ((a1 + b1) % m)

    def res(self, a):
        if self.kind == 'galois':
            return a % 3 + 3 * ((a // 9) % 3)
        return a % self.q

    def lift(self, a):
        return a % 3 + 9 * (a // 3) if self.kind == 'galois' else a

    def sub(self, a, b):
        return self.add[a][self.neg[b]]

    def directions(self):
        return [(1, a) for a in range(self.n)] + [(a, 1) for a in self.ideal]

    def normalize(self, v):
        a, b = v
        require(self.res(a) or self.res(b), 'direction is not unimodular')
        s = self.inv[a] if self.res(a) else self.inv[b]
        return self.mul[a][s], self.mul[b][s]

    def line(self, point, direction):
        x, y = point
        u, v = direction
        require(self.res(u) or self.res(v), 'line must be free')
        return {(self.add[x][self.mul[t][u]], self.add[y][self.mul[t][v]])
                for t in range(self.n)}


def verify_construction(r):
    f, q, n = r.f, r.q, r.n
    directions = set(r.directions())
    normalized = {r.normalize((a, b)) for a, b in product(range(n), repeat=2)
                  if r.res(a) or r.res(b)}
    require(directions == normalized and len(directions) == q * (q + 1),
            'projective direction coverage failed')
    origin_lines = [frozenset(r.line((0, 0), d)) for d in directions]
    require(len(set(origin_lines)) == len(directions), 'duplicate direction subgroup')
    sq = {r.mul[a][a] for a in range(n)}
    require(len(sq) == 1 + q * (q - 1) // 2, 'wrong square count')
    for a in range(n):
        expected = a == 0 or (r.res(a) != 0 and r.res(a) in f.squares)
        require((a in sq) == expected, 'square-lifting criterion failed')
    y0 = r.lift(next(a for a in range(q) if f.neg[a] not in f.squares))
    core, extra_lines = set(), set()
    chosen = []
    for a in range(n):
        d = (1, a)
        ell = r.line((0, r.neg[r.mul[a][a]]), d)
        require(len(ell) == n, 'truncated full line')
        core |= ell
        chosen.append((d, ell))
    for slope in r.ideal:
        d = (slope, 1)
        ell = r.line((0, y0), d)
        extra_lines |= ell
        chosen.append((d, ell))
    discriminant = {(x, y) for x, y in product(range(n), repeat=2)
                    if r.sub(r.mul[x][x], r.mul[r.four][y]) in sq}
    require(core == discriminant, 'line/discriminant point sets disagree')
    union = core | extra_lines
    require({d for d, _ in chosen} == directions, 'missing direction')
    require(len(core) == n * len(sq), 'core cardinality failed')
    require(len(extra_lines - core) == q * q * (q - 1) // 2, 'completion count failed')
    require(len(union) == (q ** 4 + q ** 2) // 2, 'competitor cardinality failed')
    for y in range(n):
        actual = {x for x in range(n) if (x, y) in extra_lines}
        expected = {0} if r.res(y) == r.res(y0) else set(r.ideal)
        require(actual == expected, 'residue-row formula failed')
    # A complete set of directions cannot be inferred from the finite slopes.
    require(all(not r.line((x, 0), (0, 1)) <= core for x in range(n)),
            'core unexpectedly supplies a vertical line')
    # This actual witnessing system is not a residue pencil.
    images = [{(r.res(x), r.res(y)) for x, y in ell} for _, ell in chosen]
    require(not set.intersection(*images), 'competitor witnessing lines form a pencil')
    lower = (q ** 4 + q ** 3 + q - 1) // 2
    gap = (q - 1) * (q * q + 1) // 2
    require(lower - len(union) == gap and gap > 0, 'separator identity failed')
    return {'ring': r.name, 'residue_order': q, 'directions': len(directions),
            'core_points': len(core), 'added_points': len(extra_lines - core),
            'competitor_points': len(union), 'pencil_lower_bound': lower, 'gap': gap}


def offsets(f, exhaustive):
    q = f.q
    if exhaustive:
        return product(range(q), repeat=q)
    result = set()
    for exponent in range(4):
        for c in range(q):
            b = []
            for t in range(q):
                v = 1
                for _ in range(exponent):
                    v = f.mul[v][t]
                b.append(f.add[v][c])
            result.add(tuple(b))
    return sorted(result)


def verify_fibers(r, exhaustive):
    q, f = r.q, r.f
    count = point_checks = 0
    caches = [[] for _ in range(q + 1)]
    for b in offsets(f, exhaustive):
        sizes = [len({f.add[f.mul[t][a]][b[t]] for t in range(q)}) for a in range(q)]
        require(q + sum(sizes[1:]) >= (q * q + 2 * q - 1) // 2,
                'finite-field Kakeya input fails on a fixture')
        for group in range(q + 1):
            points = set()
            for t in range(q):
                if group < q:
                    slope = r.add[r.lift(group)][r.ideal[t]]
                    ell = r.line((0, r.ideal[b[t]]), (1, slope))
                else:
                    ell = r.line((r.ideal[b[t]], 0), (r.ideal[t], 1))
                points |= ell
            # Check the full point set in the original ring coordinates.
            predicted = set()
            for x in range(r.n):
                a = r.res(x)
                values = {f.add[f.mul[t][a]][b[t]] for t in range(q)}
                allowed = {r.ideal[v] for v in values}
                for y in range(r.n):
                    if group < q:
                        residual = r.sub(y, r.mul[r.lift(group)][x])
                        pt = (x, y)
                    else:
                        residual = y
                        pt = (y, x)
                    if residual in allowed:
                        predicted.add(pt)
            require(points == predicted, 'mixed-characteristic fiber identity failed')
            noncentral = {pt for pt in points if r.res(pt[0]) or r.res(pt[1])}
            require(len(noncentral) == q * sum(sizes[1:]), 'noncentral sum mismatch')
            require(len(noncentral) >= q * (q * q - 1) // 2, 'group lower bound failed')
            count += 1
            point_checks += r.n ** 2
            if q == 3:
                mask = sum(1 << (x * r.n + y) for x, y in points)
                caches[group].append(mask)
    census = None
    if q == 3:
        histogram = {}
        for masks in product(*caches):
            union_mask = 0
            for mask in masks:
                union_mask |= mask
            size = union_mask.bit_count()
            require(size >= (q ** 4 + q ** 3 + q - 1) // 2, 'pencil bound failed')
            histogram[size] = histogram.get(size, 0) + 1
        require(sum(histogram.values()) == 3 ** 12, 'incomplete smallest pencil census')
        census = {'systems': sum(histogram.values()), 'minimum_observed': min(histogram),
                  'size_histogram': histogram}
    return {'ring': r.name, 'all_offset_functions': exhaustive, 'groups_checked': count,
            'point_memberships_compared': point_checks, 'smallest_pencil_census': census}


def run():
    rings = [Ring(Field(p), k) for p in (3, 5, 7, 11) for k in ('integer', 'dual')]
    rings += [Ring(Field(3, 2), k) for k in ('dual', 'galois')]
    construction = [verify_construction(r) for r in rings]
    fibers = [verify_fibers(r, r.q in (3, 5)) for r in rings if r.q != 11]
    # The square shortcut in (10) is false at length three: 3^2=9 in Z/27.
    require(9 != 0 and (3 * 3) % 27 == 9, 'length-three control broken')
    # Odd characteristic matters: the residue field F2 has no nonsquare unit.
    require({a * a % 2 for a in range(2)} == {0, 1}, 'even-field control broken')
    for r in rings:
        try:
            r.normalize((r.pi, 0))
        except ValueError:
            pass
        else:
            raise ValueError('nonunimodular direction accepted as free')
    return {'status': 'VERIFIED', 'construction': construction, 'fiber_checks': fibers,
            'controls': ['finite-slope core misses vertical direction',
                         'competitor system has no common residue point',
                         'nonfree directions rejected', 'length-three square shortcut fails',
                         'even residue field has no nonsquare unit'],
            'trust': 'finite exact corroboration; universal theorem imports Blokhuis--Mazzocca Proposition 7'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true', help='omit expected-output comparison')
    args = parser.parse_args()
    encoded = json.dumps(run(), sort_keys=True, indent=2) + '\n'
    if not args.emit:
        require(encoded == Path(__file__).with_name('expected.json').read_text(),
                'expected output mismatch')
    print(encoded, end='')


if __name__ == '__main__':
    main()
