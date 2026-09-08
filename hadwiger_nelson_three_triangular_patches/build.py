#!/usr/bin/env python3
"""Build exact 3-colour witnesses for the three-P48-patch contact triangles."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from math import gcd, isqrt
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


def norm(z):
    a, b = z
    return a*a+a*b+b*b


def mul(z, w):
    a, b = z
    c, d = w
    return a*c-b*d, a*d+b*c+b*d


def conjugate(z):
    return z[0]+z[1], -z[1]


def primitive(u, v, k):
    divisor = gcd(gcd(u, v), k)
    value = (u//divisor, v//divisor, k//divisor)
    return max(value, tuple(-x for x in value))


def squarefree_part(n):
    square, free, prime = 1, 1, 2
    while prime*prime <= n:
        exponent = 0
        while n % prime == 0:
            n //= prime
            exponent += 1
        square *= prime**(exponent//2)
        if exponent % 2:
            free *= prime
        prime += 1
    if n > 1:
        free *= n
    return free, square


def patch():
    points = sorted((a, b) for a in range(-8, 9) for b in range(-8, 9)
                    if norm((a, b)) <= 48)
    origin = points.index((0, 0))
    seed = [(i, j) for i, z in enumerate(points)
            for j, w in enumerate(points[:i])
            if norm((z[0]-w[0], z[1]-w[1])) == 1]
    lines = defaultdict(list)
    for i, z in enumerate(points):
        for j, w in enumerate(points):
            if i == origin or j == origin:
                continue
            k = norm(z)+norm(w)-1
            a, b = mul(w, conjugate(z))
            u, v = 2*a+b, -3*b
            if 3*k*k <= 3*u*u+v*v:
                lines[primitive(u, v, k)].append((i, j))
    residues = [(a-b) % 3 for a, b in points]
    rows = []
    for line, edges in sorted(lines.items()):
        u, v, k = line
        d = 3*u*u+v*v-3*k*k
        if isqrt(d)**2 == d:
            continue
        zero = any(residues[i] == residues[j] == 0 for i, j in edges)
        rows.append({'line': line, 'radicand': d, 'edges': tuple(edges),
                     'chi': 4 if zero else 3})
    return points, seed, rows


def roots(row):
    u, v, k = row['line']
    sf, factor = squarefree_part(row['radicand'])
    s = 3*u*u+v*v
    for sign in (-1, 1):
        # x=x0+x1 sqrt(sf), y=y0+y1 sqrt(sf), alpha=x+i sqrt(3)y.
        yield (F(3*u*k, s), F(sign*v*factor, s),
               F(v*k, s), F(-sign*u*factor, s), sf)


def scalar(pair, radicand):
    answer = {1: pair[0]}
    if pair[1]:
        answer[radicand] = pair[1]
    return {r: q for r, q in answer.items() if q}


def sadd(a, b, scale=1):
    answer = dict(a)
    for r, q in b.items():
        answer[r] = answer.get(r, F(0))+scale*q
        if not answer[r]:
            del answer[r]
    return answer


def smul(a, b):
    answer = {}
    for r, q in a.items():
        for s, t in b.items():
            common = gcd(r, s)
            squarefree = r*s//(common*common)
            answer[squarefree] = answer.get(squarefree, F(0))+common*q*t
    return {r: q for r, q in answer.items() if q}


def key(x, y):
    encode = lambda value: tuple((r, q.numerator, q.denominator)
                                 for r, q in sorted(value.items()))
    return encode(x), encode(y)


def expanded(rotation):
    return key(scalar(rotation[:2], rotation[4]),
               scalar(rotation[2:4], rotation[4]))


def relative(a, b):
    ax, ay = scalar(a[:2], a[4]), scalar(a[2:4], a[4])
    bx, by = scalar(b[:2], b[4]), scalar(b[2:4], b[4])
    # conjugate(a)*b
    return key(sadd(smul(ax, bx), smul(ay, by), 3),
               sadd(smul(ax, by), smul(ay, bx), -1))


def inventory():
    points, seed, lines = patch()
    rotations = {}
    for row in lines:
        for rotation in roots(row):
            if rotation in rotations:
                raise ValueError('duplicate irrational rotation')
            rotations[rotation] = row
    lookup = {expanded(rotation): rotation for rotation in rotations}
    if len(lookup) != len(rotations):
        raise ValueError('duplicate expanded rotation')
    triples = []
    ordered = sorted(rotations)
    for position, a in enumerate(ordered):
        for b in ordered[position+1:]:
            c = lookup.get(relative(a, b))
            if c is not None:
                triples.append((a, b, c))
    return points, seed, rotations, triples


def triple_graph(points, seed, rotations, triple):
    origin = points.index((0, 0))
    labels, cursor = {}, 1
    for layer in range(3):
        for local in range(len(points)):
            if local == origin:
                labels[layer, local] = 0
            else:
                labels[layer, local] = cursor
                cursor += 1
    if cursor != 505:
        raise ValueError('wrong physical order')
    edges = {tuple(sorted((labels[layer, i], labels[layer, j])))
             for layer in range(3) for i, j in seed}
    for left, right, rotation in ((0, 1, triple[0]),
                                  (0, 2, triple[1]),
                                  (1, 2, triple[2])):
        edges.update(tuple(sorted((labels[left, i], labels[right, j])))
                     for i, j in rotations[rotation]['edges'])
    return tuple(sorted(edges)), labels


def digest(edges):
    stream = ''.join(f'{a} {b}\n' for a, b in edges).encode()
    return hashlib.sha256(stream).hexdigest()


def solve(kissat, edges, labels, points):
    colours_count = 3
    clauses = []
    for vertex in range(505):
        clauses.append([colours_count*vertex+c+1 for c in range(colours_count)])
        clauses.extend([-(colours_count*vertex+c+1),
                         -(colours_count*vertex+d+1)]
                       for c in range(colours_count) for d in range(c))
    clauses.extend([-(colours_count*u+c+1), -(colours_count*v+c+1)]
                   for u, v in edges for c in range(colours_count))
    origin = points.index((0, 0))
    clauses.extend([[colours_count*labels[0, local]+colour+1]
                    for local, colour in ((origin, 0),
                                           (points.index((0, 1)), 1),
                                           (points.index((1, 0)), 2))])
    with tempfile.TemporaryDirectory(prefix='hn-three-patches-') as directory:
        cnf = Path(directory)/'graph.cnf'
        with cnf.open('w') as out:
            out.write(f'p cnf {colours_count*505} {len(clauses)}\n')
            for clause in clauses:
                out.write(' '.join(map(str, clause))+' 0\n')
        run = subprocess.run([str(kissat), '--seed=0', str(cnf)], text=True,
                             capture_output=True, timeout=120)
    if run.returncode != 10:
        raise RuntimeError(f'expected SAT, solver exit {run.returncode}: {run.stderr[-500:]}')
    positive = {int(x) for line in run.stdout.splitlines() if line.startswith('v ')
                for x in line[2:].split() if int(x) > 0}
    colours = []
    for vertex in range(505):
        found = [c for c in range(colours_count)
                 if colours_count*vertex+c+1 in positive]
        if len(found) != 1:
            raise RuntimeError('solver returned malformed model')
        colours.append(found[0])
    if any(colours[u] == colours[v] for u, v in edges):
        raise RuntimeError('solver returned improper colouring')
    return ''.join(map(str, colours))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kissat', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    points, seed, rotations, triples = inventory()
    colourings = {}
    edge_counts = Counter()
    for triple in triples:
        edges, labels = triple_graph(points, seed, rotations, triple)
        graph_hash = digest(edges)
        edge_counts[len(edges)] += 1
        if graph_hash not in colourings:
            colourings[graph_hash] = solve(args.kissat, edges, labels, points)
    result = {'format': 1, 'family': 'three-P48-patches-pairwise-irrational',
              'graph_colourings': colourings}
    data = (json.dumps(result, indent=2, sort_keys=True)+'\n').encode()
    args.output.write_bytes(data)
    print(json.dumps({'patch_vertices': len(points), 'patch_edges': len(seed),
                      'irrational_contact_rotations': len(rotations),
                      'contact_triangles': len(triples),
                      'distinct_labelled_graphs': len(colourings),
                      'case_edge_histogram': dict(edge_counts),
                      'certificate_bytes': len(data),
                      'certificate_sha256': hashlib.sha256(data).hexdigest()},
                     sort_keys=True))


if __name__ == '__main__':
    main()
