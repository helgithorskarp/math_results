#!/usr/bin/env python3
"""Independent exact Cartesian verifier for the three-P48-patch theorem."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from math import gcd, isqrt
import hashlib
import json
from pathlib import Path
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def primitive(values):
    divisor = gcd(*values)
    answer = tuple(x//divisor for x in values)
    if next(x for x in answer if x) < 0:
        answer = tuple(-x for x in answer)
    return answer


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


def coordinates():
    # The physical point is (X/2,sqrt(3)Y/2), while the sort key is (a,b)
    # for X=2a+b, Y=b. This is independent of the builder's ring arithmetic.
    points = [(x, y) for y in range(-8, 9) for x in range(-14, 15)
              if (x-y) % 2 == 0 and x*x+3*y*y <= 192]
    return sorted(points, key=lambda z: ((z[0]-z[1])//2, z[1]))


def line_inventory(points):
    origin = points.index((0, 0))
    lines = defaultdict(list)
    for i, (x, y) in enumerate(points):
        for j, (a, b) in enumerate(points):
            if i == origin or j == origin:
                continue
            u = x*a+3*y*b
            v = 3*(y*a-x*b)
            k = (x*x+3*y*y+a*a+3*b*b-4)//2
            if 3*k*k <= 3*u*u+v*v:
                lines[primitive((u, v, k))].append((i, j))
    return lines


def triangle_propagation(points, edges):
    adjacent = [set() for _ in points]
    for i, j in edges:
        adjacent[i].add(j)
        adjacent[j].add(i)
    colours = {points.index((0, 0)): 0,
               points.index((2, 0)): 1,
               points.index((1, 1)): 2}
    steps = 0
    changed = True
    while changed:
        changed = False
        for i, j in edges:
            if i not in colours or j not in colours:
                continue
            require(colours[i] != colours[j], 'inconsistent triangle propagation')
            for k in adjacent[i] & adjacent[j]:
                value = 3-colours[i]-colours[j]
                if k in colours:
                    require(colours[k] == value, 'inconsistent forced colour')
                else:
                    colours[k] = value
                    steps += 1
                    changed = True
    require(len(colours) == len(points), 'patch is not triangle-connected')
    require(all(colours[i] == (-x) % 3 for i, (x, y) in enumerate(points)),
            'forced colouring is not the residue colouring')
    return steps


def line_audit(line, claimed, points, seed, residues):
    u, v, k = line
    s = 3*u*u+v*v
    d = s-3*k*k
    require(d > 0 and isqrt(d)**2 != d, 'line is not irrational secant')
    require((3*u*k)**2+3*(v*k)**2+d*(v*v+3*u*u) == s*s,
            'rotation root has nonunit norm')
    require(3*u*k*v-3*v*k*u == 0, 'rotation norm has radical term')
    # For one root, after multiplying coordinates by s, alpha(x,y) has
    # rational/radical coefficients (x0,x1,y0,y1). The conjugate root has
    # the opposite radical coefficients and exactly the same contacts.
    moved = [(3*u*k*x-3*v*k*y, v*x+3*u*y,
              v*k*x+3*u*k*y, -u*x+v*y) for x, y in points]
    contacts, coincidences = [], []
    for i, (x, y) in enumerate(points):
        bx, by = s*x, s*y
        for j, (x0, x1, y0, y1) in enumerate(moved):
            dx, dy = bx-x0, by-y0
            rational = dx*dx+3*dy*dy+d*(x1*x1+3*y1*y1)
            radical = dx*x1+3*dy*y1
            if radical == 0 and rational == 4*s*s:
                contacts.append((i, j))
            if radical == 0 and rational == 0:
                coincidences.append((i, j))
    origin = points.index((0, 0))
    require(coincidences == [(origin, origin)], 'nonorigin irrational coincidence')
    proper = tuple(e for e in contacts if origin not in e)
    require(proper == tuple(claimed), 'contact-line edge mismatch')
    products = {residues[i]*residues[j] % 3 for i, j in proper
                if residues[i] and residues[j]}
    require(len(products) <= 1, 'nonconstant residue product')
    epsilon = next(iter(products), 1)
    zero = any(residues[i] == residues[j] == 0 for i, j in proper)
    chi = 4 if zero else 3
    first = [r for r in residues]
    second = [(-epsilon*r) % 3 for r in residues]
    second[origin] = 0
    require(all(first[i] != first[j] and second[i] != second[j]
                for i, j in seed), 'bad within-patch residue colouring')
    if chi == 3:
        require(all(first[i] != second[j] for i, j in contacts),
                'bad pair three-colouring')
    return {'line': line, 'radicand': d, 'edges': proper, 'chi': chi}, len(contacts)


def roots(row):
    u, v, k = row['line']
    sf, factor = squarefree_part(row['radicand'])
    s = 3*u*u+v*v
    for sign in (-1, 1):
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
            radicand = r*s//(common*common)
            answer[radicand] = answer.get(radicand, F(0))+common*q*t
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
    return key(sadd(smul(ax, bx), smul(ay, by), 3),
               sadd(smul(ax, by), smul(ay, bx), -1))


def graph(points, seed, rotations, triple):
    origin = points.index((0, 0))
    labels, cursor = {}, 1
    for layer in range(3):
        for local in range(len(points)):
            if local == origin:
                labels[layer, local] = 0
            else:
                labels[layer, local] = cursor
                cursor += 1
    require(cursor == 505, 'wrong physical order')
    edges = {tuple(sorted((labels[layer, i], labels[layer, j])))
             for layer in range(3) for i, j in seed}
    for left, right, rotation in ((0, 1, triple[0]),
                                  (0, 2, triple[1]),
                                  (1, 2, triple[2])):
        edges.update(tuple(sorted((labels[left, i], labels[right, j])))
                     for i, j in rotations[rotation]['edges'])
    return tuple(sorted(edges))


def graph_digest(edges):
    return hashlib.sha256(''.join(f'{u} {v}\n' for u, v in edges).encode()).hexdigest()


def prepare():
    points = coordinates()
    require(len(points) == 169, 'wrong patch order')
    seed = tuple((i, j) for i, (x, y) in enumerate(points)
                 for j, (a, b) in enumerate(points[:i])
                 if (x-a)**2+3*(y-b)**2 == 4)
    require(len(seed) == 456, 'wrong patch edge count')
    propagation = triangle_propagation(points, seed)
    residues = [(-x) % 3 for x, y in points]
    lines = line_inventory(points)
    irrational = {line: edges for line, edges in lines.items()
                  if isqrt(3*line[0]*line[0]+line[1]*line[1]-3*line[2]*line[2])**2
                  != 3*line[0]*line[0]+line[1]*line[1]-3*line[2]*line[2]}
    rows, contact_checks = {}, 0
    for line, claimed in sorted(irrational.items()):
        row, checks = line_audit(line, claimed, points, seed, residues)
        contact_checks += 2*checks
        for rotation in roots(row):
            require(rotation not in rows, 'duplicate irrational rotation')
            rows[rotation] = row
    lookup = {}
    for rotation in rows:
        value = expanded(rotation)
        require(value not in lookup, 'duplicate expanded rotation')
        lookup[value] = rotation
    triples = []
    ordered = sorted(rows)
    for position, a in enumerate(ordered):
        for b in ordered[position+1:]:
            c = lookup.get(relative(a, b))
            if c is not None:
                triples.append((a, b, c))
    case_edges = [graph(points, seed, rows, triple) for triple in triples]
    return {'points': points, 'seed': seed, 'lines': lines,
            'irrational_lines': irrational, 'rows': rows, 'triples': triples,
            'case_edges': case_edges, 'propagation': propagation,
            'contact_checks': contact_checks}


def audit_certificate(certificate, state):
    require(certificate.get('format') == 1, 'wrong certificate format')
    require(certificate.get('family') == 'three-P48-patches-pairwise-irrational',
            'wrong certificate family')
    colourings = certificate.get('graph_colourings')
    require(type(colourings) is dict, 'missing graph-colouring dictionary')
    graphs = {}
    for edges in state['case_edges']:
        digest = graph_digest(edges)
        if digest in graphs:
            require(graphs[digest] == edges, 'hash collision between edge streams')
        graphs[digest] = edges
    require(set(colourings) == set(graphs), 'certificate graph inventory mismatch')
    for digest, edges in graphs.items():
        word = colourings[digest]
        require(type(word) is str and len(word) == 505 and set(word) <= set('012'),
                'malformed three-colouring word')
        colours = list(map(int, word))
        require(all(colours[u] != colours[v] for u, v in edges),
                'improper three-colouring word')
    return graphs


def audit(certificate):
    state = prepare()
    graphs = audit_certificate(certificate, state)
    rows, triples = state['rows'], state['triples']
    pair_chi = Counter(row['chi'] for row in rows.values())
    side_chi = Counter(tuple(sorted(rows[r]['chi'] for r in triple))
                       for triple in triples)
    side_edges = Counter(tuple(sorted(len(rows[r]['edges']) for r in triple))
                         for triple in triples)
    graph_edges = Counter(len(edges) for edges in graphs.values())
    case_hashes = Counter(graph_digest(edges) for edges in state['case_edges'])
    multiplicities = Counter(case_hashes.values())
    fields = Counter(rotation[4] for triple in triples for rotation in triple)
    require(side_chi == {(3, 3, 3): 216}, 'unexpected side-chromatic census')
    require(pair_chi == {3: 468, 4: 252}, 'unexpected pair-chromatic census')
    require(side_edges == {(6, 12, 12): 216}, 'unexpected side-edge census')
    require(fields == {21: 648}, 'unexpected contact-triangle field')
    require(graph_edges == {1398: 114}, 'unexpected strict-graph edge census')
    return {'verified': True, 'patch_vertices': len(state['points']),
            'patch_edges': len(state['seed']),
            'forced_triangle_steps': state['propagation'],
            'contact_lines': len(state['lines']),
            'irrational_contact_lines': len(state['irrational_lines']),
            'irrational_contact_rotations': len(rows),
            'irrational_pair_chromaticities': {'3': pair_chi[3], '4': pair_chi[4]},
            'pairwise_contact_triangles': len(triples),
            'contact_triangle_squarefree_field': 21,
            'contact_triangle_side_chromaticities': {'3,3,3': 216},
            'contact_triangle_side_cross_edges': {'6,12,12': 216},
            'distinct_labelled_strict_graphs': len(graphs),
            'case_graph_multiplicity_histogram':
                {str(k): v for k, v in sorted(multiplicities.items())},
            'strict_graph_edge_histogram': {'1398': len(graphs)},
            'strict_graph_chromatic_number': 3,
            'cartesian_cross_norm_evaluations':
                len(state['irrational_lines'])*len(state['points'])**2,
            'unit_contacts_including_both_roots': state['contact_checks'],
            'certificate_colourings': len(certificate['graph_colourings']),
            'record_improvement': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path,
                        default=Path(__file__).with_name('COLOUR_CERTIFICATE.json'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    data = args.certificate.read_bytes()
    result = audit(json.loads(data))
    result['certificate_sha256'] = hashlib.sha256(data).hexdigest()
    result['seconds'] = time.monotonic()-started
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
