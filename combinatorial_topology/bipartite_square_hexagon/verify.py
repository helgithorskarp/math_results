"""Exact auxiliary checks for hexagonal spheres in bipartite graph squares.

Python 3.11+, standard library; universal proofs are in PROOF.md.
Graphs are labelled 0,...,n-1; edges/faces use increasing tuples.
"""
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def adjacency(n, edges):
    a = [set() for _ in range(n)]
    for u, v in edges:
        a[u].add(v)
        a[v].add(u)
    return a


def valid(n, edges, colors):
    require(n >= 2 and len(colors) == n, "size")
    require(set(colors) == {0, 1}, "two nonempty parts")
    require(len(edges) == len(set(edges)), "duplicate edges")
    require(all(0 <= u < v < n for u, v in edges), "canonical simple edges")
    require(all(colors[u] != colors[v] for u, v in edges), "bipartite")
    a = adjacency(n, edges)
    reached, todo = {0}, [0]
    while todo:
        for v in a[todo.pop()] - reached:
            reached.add(v)
            todo.append(v)
    require(len(reached) == n, "connected")
    require(all(len(a[u] & a[v]) <= 1 for u, v in combinations(range(n), 2)), "C4-free")
    return a


def cliques(a):
    faces = set()
    def visit(prefix, candidates):
        for j, v in enumerate(candidates):
            f = prefix + (v,)
            faces.add(f)
            visit(f, [w for w in candidates[j + 1:] if w in a[v]])
    visit((), list(range(len(a))))
    return faces


def square(a):
    return [(a[u] | set().union(*(a[v] for v in a[u]))) - {u} for u in range(len(a))]


def boundary(face):
    return [(face[:i] + face[i + 1:], (-1) ** i) for i in range(len(face))]


def chain_boundary(chain):
    out = defaultdict(int)
    for f, c in chain.items():
        for g, sign in boundary(f):
            out[g] += c * sign
    return {f: c for f, c in out.items() if c}


def rank(vectors, modulus=None):
    basis = {}
    for vector in vectors:
        v = {i: (x % modulus if modulus else Fraction(x)) for i, x in enumerate(vector) if x}
        v = {i: x for i, x in v.items() if x}
        while v:
            pivot = min(v)
            if pivot not in basis:
                c = v[pivot]
                inv = pow(c, -1, modulus) if modulus else 1 / c
                basis[pivot] = {i: (x * inv % modulus if modulus else x * inv) for i, x in v.items()}
                break
            c = v[pivot]
            for i, x in basis[pivot].items():
                y = v.get(i, 0) - c * x
                if modulus:
                    y %= modulus
                if y:
                    v[i] = y
                else:
                    v.pop(i, None)
    return len(basis)


def betti(faces, modulus):
    max_size = max(map(len, faces))
    levels = [[]] + [sorted(f for f in faces if len(f) == k) for k in range(1, max_size + 1)]
    ranks = [0] * (max_size + 2)
    for k in range(2, max_size + 1):
        index = {f: i for i, f in enumerate(levels[k - 1])}
        cols = []
        for f in levels[k]:
            v = [0] * len(index)
            for g, sign in boundary(f):
                v[index[g]] = sign
            cols.append(v)
        ranks[k] = rank(cols, modulus)
    return [len(levels[k]) - ranks[k] - ranks[k + 1] for k in range(1, max_size + 1)]


def canonical_cycle(c):
    c = tuple(c)
    variants = [d[i:] + d[:i] for d in (c, c[::-1]) for i in range(len(c))]
    return min(variants)


def six_cycles(a):
    result = set()
    def visit(path):
        if len(path) == 6:
            if path[0] in a[path[-1]]:
                result.add(canonical_cycle(path))
            return
        for v in sorted(a[path[-1]]):
            if v > path[0] and v not in path:
                visit(path + (v,))
    for start in range(len(a)):
        visit((start,))
    return sorted(result)


def cycle_vector(cycle, edges):
    index = {e: i for i, e in enumerate(edges)}
    v = [0] * len(edges)
    for u, w in zip(cycle, cycle[1:] + cycle[:1]):
        v[index[min(u, w), max(u, w)]] += 1 if u < w else -1
    return tuple(v)


def detector(triangle, a, colors, edges):
    if any(colors[v] != 0 for v in triangle):
        return (0,) * len(edges)
    walk = []
    for u, v in zip(triangle, triangle[1:] + triangle[:1]):
        common = a[u] & a[v]
        require(len(common) == 1, "unique two-edge path")
        walk += [u, next(iter(common))]
    return cycle_vector(tuple(walk), edges)


def sphere_chain(cycle):
    # Oriented join (c0-c3)*(c1-c4)*(c2-c5).
    out = {}
    pairs = list(zip(cycle[:3], cycle[3:]))
    for bits in product((0, 1), repeat=3):
        f = tuple(pairs[i][bits[i]] for i in range(3))
        inversions = sum(f[i] > f[j] for i in range(3) for j in range(i + 1, 3))
        out[tuple(sorted(f))] = (-1) ** (sum(bits) + inversions)
    return out


def bridge_collapse(a):
    faces = set()
    for v in range(len(a)):
        star = sorted(a[v] | {v})
        for size in range(1, len(star) + 1):
            faces.update(combinations(star, size))
    original, steps = set(faces), 0
    for v in range(len(a)):
        for size in range(len(a[v]), 1, -1):
            for sigma in combinations(sorted(a[v]), size):
                tau = tuple(sorted(sigma + (v,)))
                require(sigma in faces and tau in faces, "collapse pair present")
                proper = {f for f in faces if len(f) > size and set(sigma) <= set(f)}
                require(proper == {tau}, "free codimension-one face")
                faces.remove(sigma)
                faces.remove(tau)
                steps += 1
    graph = {(v,) for v in range(len(a))} | {(u, v) for u in range(len(a)) for v in a[u] if u < v}
    require(faces == graph, "bridge collapse endpoint")
    return original, steps


def audit(n, edges, colors, rational=False):
    edges = sorted(edges)
    a = valid(n, edges, colors)
    k = cliques(square(a))
    halves = [{f for f in k if all(colors[v] == part for v in f)} for part in (0, 1)]
    d, steps = bridge_collapse(a)
    require(d <= k, "bridge subcomplex")
    cycles = six_cycles(a)
    cv = [cycle_vector(c, edges) for c in cycles]
    phi = {t: detector(t, a, colors, edges) for t in k if len(t) == 3}
    for tetra in (f for f in k if len(f) == 4):
        v = tuple(sum(s * phi[t][i] for t, s in boundary(tetra)) for i in range(len(edges)))
        require(not any(v), "detector annihilates tetrahedron boundaries")
    for cycle, vector in zip(cycles, cv):
        z = sphere_chain(cycle)
        require(set(z) <= k and len(z) == 8, "octahedron triangles")
        require(not chain_boundary(z), "integral sphere cycle")
        induced = {f for f in k if set(f) <= set(cycle)}
        require([sum(len(f) == j for f in induced) for j in (1, 2, 3)] == [6, 12, 8], "induced octahedron")
        require(max(map(len, induced)) == 3, "no extra six-vertex simplex")
        image = tuple(sum(c * phi[t][i] for t, c in z.items()) for i in range(len(edges)))
        require(image == vector or image == tuple(-x for x in vector), "primitive hexagon detection")
    if not cycles:
        require(k == d, "no-hexagon whole-complex collapse")
    records = []
    for prime in ([2, 3, None] if rational else [2, 3]):
        b = betti(k, prime)
        x, y = (betti(h, prime) for h in halves)
        size = max(len(b), len(x), len(y), 3)
        b += [0] * (size - len(b)); x += [0] * (size - len(x)); y += [0] * (size - len(y))
        r = rank(cv, prime)
        require(b[0] == x[0] == y[0] == 1, "connected complexes")
        require(b[1] == x[1] == y[1] == len(edges) - n + 1 - r, "first homology quotient")
        require(b[2] == x[2] + y[2] + r, "second homology split sequence")
        require(all(b[j] == x[j] + y[j] for j in range(3, size)), "higher homology splitting")
        records.append([prime, r, b, x, y])
    return {'n': n, 'edges': len(edges), 'hexagons': len(cycles), 'collapse_pairs': steps, 'homology': records}


def subdivision(n, edges):
    out = [(u, n + j) for j, (u, v) in enumerate(edges)] + [(v, n + j) for j, (u, v) in enumerate(edges)]
    return n + len(edges), sorted(out), [0] * n + [1] * len(edges)


def fixtures():
    yield 'C6', 6, [(i, i + 1) for i in range(5)] + [(0, 5)], [i % 2 for i in range(6)]
    yield 'C8', 8, [(i, i + 1) for i in range(7)] + [(0, 7)], [i % 2 for i in range(8)]
    yield 'subdivision_K4', *subdivision(4, list(combinations(range(4), 2)))
    octa = [(i, j) for i, j in combinations(range(6), 2) if i // 2 != j // 2]
    yield 'subdivision_octahedron', *subdivision(6, octa)
    # Fano incidence graph: lines {i,i+1,i+3} modulo 7.
    e = sorted((x, 7 + i) for i in range(7) for x in {i, (i + 1) % 7, (i + 3) % 7})
    yield 'Heawood', 14, e, [0] * 7 + [1] * 7
    # C6 and C8 sharing edge 0--1: one spherical class and one surviving loop.
    e = [(i, i + 1) for i in range(5)] + [(0, 5), (1, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (0, 11)]
    yield 'hexagon_and_octagon', 12, sorted(e), [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]


def main():
    digest, accepted, hexagons, pairs = sha256(), 0, 0, 0
    for left in range(1, 4):
        for right in range(left, 8 - left):
            n = left + right
            possible = [(u, left + v) for u in range(left) for v in range(right)]
            colors = [0] * left + [1] * right
            for mask in range(1 << len(possible)):
                edges = [e for j, e in enumerate(possible) if mask >> j & 1]
                try:
                    valid(n, edges, colors)
                except ValueError:
                    continue
                row = audit(n, edges, colors)
                accepted += 1; hexagons += row['hexagons']; pairs += row['collapse_pairs']
                digest.update(json.dumps([left, right, mask, row], sort_keys=True).encode())
    special = {name: audit(n, edges, colors, rational=True) for name, n, edges, colors in fixtures()}
    # Dropping C4-free permits an induced C6 whose sphere is killed by a cone.
    bad = [(i, i + 1) for i in range(5)] + [(0, 5), (0, 6), (2, 6), (4, 6)]
    bad_colors = [0, 1, 0, 1, 0, 1, 1]
    a = adjacency(7, bad)
    require(len(square(a)[6]) == 6, "C4 boundary fixture is a cone")
    rejected = 0
    tests = [(7, bad, bad_colors), (3, [(0, 1), (1, 2), (0, 2)], [0, 1, 0]),
             (4, [(0, 2), (1, 3)], [0, 0, 1, 1]), (2, [(0, 1), (0, 1)], [0, 1]),
             (2, [(1, 0)], [0, 1])]
    for args in tests:
        try:
            valid(*args)
        except ValueError:
            rejected += 1
    require(rejected == len(tests), "malformed and boundary inputs rejected")
    z = sphere_chain((0, 1, 2, 3, 4, 5))
    z.pop(next(iter(z)))
    require(bool(chain_boundary(z)), "missing sphere face detected")
    result = {'exhaustive_connected_C4_free_bipartite_graphs': accepted,
              'exhaustive_hexagons': hexagons, 'exhaustive_collapse_pairs': pairs,
              'fields': [2, 3], 'fixtures_also_over_Q': special, 'rejected_inputs': rejected,
              'C4_boundary_cone': True, 'missing_sphere_face_detected': True,
              'entry_digest': digest.hexdigest()}
    encoded = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if sys.argv[1:] == ['--check']:
        require(encoded == Path(__file__).with_name('expected.json').read_text(), "expected output")
        print('PASS: collapses, integral hexagon detectors, and homology identities')
    else:
        require(not sys.argv[1:], "usage: verify.py [--check]")
        print(encoded, end='')


if __name__ == '__main__':
    main()
