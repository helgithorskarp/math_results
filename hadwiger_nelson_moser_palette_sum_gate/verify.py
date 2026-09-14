"""Solver-free replay, constructing both sources from their radical formulas.

No import from the producer or from a source package. Integer coefficient
tuples use denominator 24 and square-root bit masks for 3,5,7,11.
"""
import hashlib
import itertools
import json
import math
from pathlib import Path

PRIMES = (3, 5, 7, 11)
RAD = tuple(math.prod(p for j, p in enumerate(PRIMES) if i >> j & 1)
            for i in range(16))
DEN = 24


def check(ok, label):
    if not ok:
        raise ValueError(label)


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def times(a, n, d=1):
    check(all(x*n % d == 0 for x in a), 'nonintegral coefficient scaling')
    return tuple(x*n//d for x in a)


def point(x=0, y=0, xr=1, yr=1):
    a = [0]*32
    a[RAD.index(xr)] = x
    a[16+RAD.index(yr)] = y
    return tuple(a)


def i_sqrt3(a):
    b = [0]*32
    for i in range(16):
        factor = 3 if i & 1 else 1
        b[i ^ 1] = -a[16+i]*factor
        b[16+(i ^ 1)] = a[i]*factor
    return tuple(b)


def i_sqrt11(a):
    b = [0]*32
    for i in range(16):
        factor = 11 if i & 8 else 1
        b[i ^ 8] = -a[16+i]*factor
        b[16+(i ^ 8)] = a[i]*factor
    return tuple(b)


def mul_t(a):
    return times(add(times(a, 5), i_sqrt11(a)), 1, 6)


def sources():
    z, one, rho = point(), point(24), point(12, 12, yr=3)
    plus = add(one, rho)
    m = [z, one, rho, plus, mul_t(one), mul_t(rho), mul_t(plus),
         point(12, -12, yr=3), times(rho, 2), times(mul_t(one), 2),
         mul_t(add(rho, times(one, -1)))]
    p = [point(-12), point(12), point(18, 6, yr=15),
         add(point(0, 6, yr=15), point(0, 6, yr=7)), point(-18, 6, yr=15)]
    for i, j in ((2, 3), (4, 0)):
        delta = i_sqrt3(add(p[j], times(p[i], -1)))
        p.extend(times(add(add(p[i], p[j]), times(delta, s)), 1, 2) for s in (1, -1))
    base = p[:]
    p.extend(times(q, -1) for q in base if times(q, -1) not in base)
    check(len(m) == 11 and len(p) == 16, 'source orders')
    return m, p


def squared_distance(a, b):
    diff = tuple(x-y for x, y in zip(a, b))
    out = [0]*16
    for off in (0, 16):
        terms = [(i, x) for i, x in enumerate(diff[off:off+16]) if x]
        for pos, (i, x) in enumerate(terms):
            out[0] += x*x*RAD[i]
            for j, y in terms[pos+1:]:
                out[i ^ j] += 2*x*y*RAD[i & j]
    return tuple(out)


def edges(points):
    one = (DEN*DEN,) + (0,)*15
    return [(i, j) for i, j in itertools.combinations(range(len(points)), 2)
            if squared_distance(points[i], points[j]) == one]


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def canonical(seq):
    seen = {}
    return ''.join(str(seen.setdefault(c, len(seen))) for c in seq)


def verify(certificate):
    m, p = sources()
    me, pe = edges(m), edges(p)
    check(len(me) == 19 and len(pe) == 25, 'complete source edge counts')
    points = sorted({add(a, b) for a in m for b in p})
    check(len(points) <= 508, 'physical cap')
    index = {q: i for i, q in enumerate(points)}
    matrix = [[index[add(a, b)] for b in p] for a in m]
    e = edges(points)
    check(digest(points) == certificate['points_sha256'], 'point hash')
    check(digest(e) == certificate['edges_sha256'], 'complete edge hash')
    word = certificate['four_colour_word']
    check(len(word) == len(points) and set(word) <= set('0123'), 'word domain')
    check(all(word[a] != word[b] for a, b in e), 'improper four-colouring')
    inherited, mstates, pstates = set(), [], []
    for j in range(16):
        ids = [matrix[i][j] for i in range(11)]
        check(len(set(ids)) == 11, 'Moser collision')
        inherited.update(tuple(sorted((ids[a], ids[b]))) for a, b in me)
        a, b, c, d = (word[ids[t]] for t in (7, 8, 9, 10))
        check(a != b or c != d, 'Moser relation violated')
        mstates.append(canonical((a, b, c, d)))
    for ids in matrix:
        check(len(set(ids)) == 16, 'palette collision')
        inherited.update(tuple(sorted((ids[a], ids[b]))) for a, b in pe)
        pstates.append(canonical(word[ids[t]] for t in (5, 6, 7, 8, 12, 13, 14, 15)))
    check(inherited <= set(e), 'inherited edge missing')
    # A literal full colouring induces an extendible interface word in each
    # copy simultaneously. No restriction to a source colouring library occurs.
    return {'status': 'EXACT_COMPOSITION_FOUR_COLOURABLE_STOP',
            'physical_points': len(points), 'unit_edges': len(e),
            'all_pairs': len(points)*(len(points)-1)//2,
            'raw_addresses': 176, 'inherited_edges': len(inherited),
            'additional_contacts': [list(x) for x in sorted(set(e)-inherited)],
            'moser_copies': 16, 'palette_copies': 11,
            'moser_terminal_words': mstates, 'palette_terminal_words': pstates,
            'simultaneous_source_relations_satisfiable': True,
            'points_sha256': digest(points), 'edges_sha256': digest(e),
            'record_candidate': False, 'architecture_retired': True}


def main():
    certificate = json.loads(Path(__file__).with_name('certificate.json').read_text())
    print(json.dumps(verify(certificate), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
