"""Exact geometry and universal triangle-extension proof; stdlib only."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from math import prod
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
PRIMES = (3, 5, 7, 11)
RAD = tuple(prod(p for j, p in enumerate(PRIMES) if mask >> j & 1) for mask in range(16))
TRIANGLES = ((5, 2, 3), (7, 4, 0), (12, 9, 10), (14, 11, 1))
TERMINALS = (5, 6, 7, 8, 12, 13, 14, 15)
CELL = ((0, 1), (0, 4), (1, 2), (2, 3), (3, 4), (2, 5),
        (3, 5), (2, 6), (3, 6), (0, 7), (4, 7), (0, 8), (4, 8))
SECOND = (1, 0, 9, 10, 11, 12, 13, 14, 15)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def neg(x):
    return tuple(-a for a in x)


def scale(x, k):
    return tuple(k * a for a in x)


def mul(x, y):
    out = [0] * 16
    for i, a in enumerate(x):
        if a:
            for j, b in enumerate(y):
                if b:
                    out[i ^ j] += a * b * RAD[i & j]
    return tuple(out)


def cmul(x, y):
    return (add(mul(x[:16], y[:16]), neg(mul(x[16:], y[16:])))
            + add(mul(x[:16], y[16:]), mul(x[16:], y[:16])))


def norm(x):
    return add(mul(x[:16], x[:16]), mul(x[16:], x[16:]))


def unit_edges(points, denominator):
    target = (denominator * denominator,) + (0,) * 15
    return [(i, j) for i, j in combinations(range(len(points)), 2)
            if norm(add(points[i], neg(points[j]))) == target]


def read_sources():
    src = json.loads((HERE / 'source_points.json').read_text())
    need(src['coupler_denominator'] == 8 and src['frozen_denominator'] == 12, 'source denominators')
    need(src['coupler_radicals'] == [1, 3, 5, 7, 15, 21, 35, 105], 'source basis')
    need(len(src['coupler_rows']) == 16 and len(src['frozen_rows']) == 29, 'source orders')
    g, f = [], []
    for row in src['coupler_rows']:
        need(len(row) == 16 and all(type(v) is int for v in row), 'coupler integer row')
        out = [0] * 32
        for axis in range(2):
            for i, r in enumerate(src['coupler_radicals']):
                out[axis * 16 + RAD.index(r)] = row[axis * 8 + i]
        g.append(tuple(out))
    for row in src['frozen_rows']:
        need(len(row) == 4 and all(type(v) is int for v in row), 'F29 integer row')
        a, b, c, d = row
        out = [0] * 32
        out[0], out[9], out[17], out[24] = a, b, c, d
        f.append(tuple(out))
    need(len(set(g)) == 16 and len(set(f)) == 29, 'source collisions')
    return g, f


def geometry():
    g, f = read_sources()
    ge, fe = unit_edges(g, 8), unit_edges(f, 12)
    expected_g = set(CELL) | {tuple(sorted((SECOND[a], SECOND[b]))) for a, b in CELL}
    need(set(ge) == expected_g, 'complete source-coupler graph')
    need(len(fe) == 75, 'complete F29 graph')
    points = [scale(z, 12) for z in g]
    where = {z: i for i, z in enumerate(points)}
    maps = []
    for t, a, b in TRIANGLES:
        u = add(g[a], neg(g[t]))  # unit complex multiplier, denominator 8
        need(norm(u) == (64,) + (0,) * 15, 'unit multiplier')
        image = [add(scale(g[t], 12), cmul(u, z)) for z in f]
        need(image[0] == scale(g[t], 12), 'centre alignment')
        need(image[28] == scale(g[a], 12) and image[25] == scale(g[b], 12), 'ordered triangle alignment')
        labels = []
        for z in image:
            if z not in where:
                where[z] = len(points)
                points.append(z)
            labels.append(where[z])
        need(len(set(labels)) == 29, 'image injectivity')
        maps.append(labels)
    need(len(points) <= 120, 'declared total budget')
    edges = unit_edges(points, 96)
    constituent = set(ge)
    for labels in maps:
        constituent |= {tuple(sorted((labels[a], labels[b]))) for a, b in fe}
    need(set(edges) == constituent, 'unexpected cross-component unit contact')
    for tri, labels in zip(TRIANGLES, maps):
        need(set(labels) & set(range(16)) == set(tri), 'source meets core beyond attachment triangle')
    for a, b in combinations(maps, 2):
        need((set(a) & set(b)) <= set(range(16)), 'new source interiors intersect')
    return points, edges, ge, fe, maps


def search(n, edges, domains):
    """Complete unsymmetrized domain search for the small palette premise."""
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    counts = {'nodes': 0, 'conflicts': 0}

    def visit(dom):
        counts['nodes'] += 1
        if 0 in dom:
            counts['conflicts'] += 1
            return None
        queue = [v for v, d in enumerate(dom) if d & (d - 1) == 0]
        done = set()
        while queue:
            v = queue.pop()
            if v in done:
                continue
            done.add(v)
            for u in adj[v]:
                new = dom[u] & ~dom[v]
                if new != dom[u]:
                    if not new:
                        counts['conflicts'] += 1
                        return None
                    dom[u] = new
                    if new & (new - 1) == 0:
                        queue.append(u)
        pending = [v for v, d in enumerate(dom) if d & (d - 1)]
        if not pending:
            return tuple(d.bit_length() - 1 for d in dom)
        v = min(pending, key=lambda i: (dom[i].bit_count(), -len(adj[i]), i))
        for c in range(4):
            if dom[v] & (1 << c):
                child = dom.copy()
                child[v] = 1 << c
                word = visit(child)
                if word is not None:
                    return word
        return None

    return visit(list(domains)), counts


def check_word(word, n, edges, pins=()):
    need(isinstance(word, str) and len(word) == n and set(word) <= set('0123'), 'colour word')
    need(all(word[a] != word[b] for a, b in edges), 'monochromatic edge')
    need(all(word[v] == c for v, c in pins), 'wrong pins')


def extend(word, source_word, maps, n):
    out = list(word) + ['?'] * (n - 16)
    for (t, a, b), labels in zip(TRIANGLES, maps):
        rename = {source_word[k]: out[v] for k, v in zip((0, 28, 25), (t, a, b))}
        need(len(rename) == 3 and len(set(rename.values())) == 3, 'attachment triangle colours')
        rename[next(iter(set('0123') - set(rename)))] = next(iter(set('0123') - set(rename.values())))
        for k, v in enumerate(labels):
            c = rename[source_word[k]]
            need(out[v] == '?' or out[v] == c, 'inconsistent shared colouring')
            out[v] = c
    need('?' not in out, 'uncoloured point')
    return ''.join(out)


def patterns(n):
    def grow(w):
        if len(w) == n:
            yield ''.join(map(str, w))
        else:
            for c in range(min(3, max(w, default=-1) + 1) + 1):
                yield from grow(w + (c,))
    return grow(())


@lru_cache(None)
def cell_words(w):
    p, q = set(w[:2]), set(w[2:])
    out = {}
    for a, b in product('0123', repeat=2):
        if a == b or a in q:
            continue
        for d, c, e in product('0123', repeat=3):
            if d not in p and c not in p and e not in q and d != c and c != e and e != a and d != b:
                out[a, b] = a + b + d + c + e + w
                break
    return out


def core_word(w):
    first, second = cell_words(w[:4]), cell_words(w[4:])
    for a, b in sorted(first):
        if (b, a) in second:
            return first[a, b] + second[b, a][2:]
    return None


def verify(cert):
    need(set(cert) == {'schema', 'maps', 'edges', 'source_four_colour_word'}, 'certificate fields')
    need(type(cert['schema']) is int and cert['schema'] == 1, 'schema')
    p, edges, ge, fe, maps = geometry()
    need(cert['maps'] == maps and cert['edges'] == list(map(list, edges)), 'certificate geometry mismatch')
    source_word = cert['source_four_colour_word']
    check_word(source_word, 29, fe)
    neighbours = [b for a, b in fe if a == 0]
    need(len(neighbours) == 14, 'source neighbour count')
    # Delete the centre, allow colours 0,1 on its neighbours and 0,1,2,3
    # elsewhere. Colour relabelling makes this cover all at-most-two palettes.
    deleted = [(a - 1, b - 1) for a, b in fe if a != 0]
    domains = [3 if v in neighbours else 15 for v in range(1, 29)]
    witness, search_counts = search(28, deleted, domains)
    need(witness is None, 'F29 palette premise failed')
    # The premise precludes a three-colouring of a centre-containing source;
    # a full positive four-word below proves chi exactly four for the composite.
    positive, negative, words = [], [], []
    for w in patterns(8):
        old = core_word(w)
        if old is None:
            negative.append(w)
        else:
            check_word(old, 16, ge, zip(TERMINALS, w))
            full = extend(old, source_word, maps, len(p))
            check_word(full, len(p), edges, zip(TERMINALS, w))
            for labels in maps:
                need(len({full[labels[v]] for v in neighbours}) == 3, 'selected input not frozen')
            positive.append(w)
            words.append(full)
    need(len(positive) == 2691 and len(negative) == 104, 'complete terminal relation')
    return {'status': 'VERIFIED_FROZEN_INPUT_TRIANGLE_DRIVER_NEUTRAL',
            'points': len(p), 'unit_edges': len(edges), 'chromatic_number': 4,
            'source_points': 29, 'source_unit_edges': len(fe), 'source_palette_search': search_counts,
            'attachment_triangles': list(map(list, TRIANGLES)), 'attachment_signs': [1] * 4,
            'new_points': len(p) - 16, 'cross_component_edges': 0,
            'attachment_intersection_sizes': [len(set(m) & set(range(16))) for m in maps],
            'frozen_original_inputs': [t for t, _, _ in TRIANGLES],
            'universal_extension_on_original_16_vertices': True,
            'terminal_patterns': len(positive) + len(negative), 'allowed': len(positive),
            'forbidden': len(negative), 'relation_strengthened': False,
            'full_pair_checks': len(p) * (len(p) - 1) // 2,
            'positive_word_edge_checks': len(positive) * len(edges),
            'point_sha256': digest(p), 'edge_sha256': digest(edges), 'maps_sha256': digest(maps),
            'negative_sha256': digest(negative), 'positive_words_sha256': digest(words),
            'example_four_colour_word': words[0], 'record_improved': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--check-expected', action='store_true')
    args = parser.parse_args()
    result = verify(json.loads(args.certificate.read_text()))
    if args.check_expected:
        need(result == json.loads((HERE / 'expected.json').read_text()), 'expected result')
    print(json.dumps(result, indent=2, sort_keys=True))
