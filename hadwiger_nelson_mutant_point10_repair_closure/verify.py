#!/usr/bin/env python3
"""All original vertices are forced in one exact 510-point augmentation.

No solver or negative certificate is used. The minimum-order equality imports
the previously certified non-four-colourability of the nine-move parent.
"""
import argparse
import base64
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RAD = (1, 3, 5, 15, 11, 33, 55, 165)
SCALE = 288

def require(ok, detail):
    if not ok:
        raise ValueError(detail)

def digest(data):
    return sha256(data).hexdigest()

def norm(p, q):
    out = [0]*8
    for offset in (0, 8):
        d = [p[offset+i]-q[offset+i] for i in range(8)]
        for i in range(8):
            out[0] += RAD[i]*d[i]*d[i]
            for j in range(i+1, 8):
                out[i ^ j] += 2*RAD[i & j]*d[i]*d[j]
    return tuple(out)

def check_word(edges, word, deleted=None, palette=range(4)):
    require(len(word) == 510, 'colour word length')
    require(all(type(c) is int and c in palette for v, c in enumerate(word)
                if v != deleted), 'colour domain')
    if deleted is not None:
        require(word[deleted] == -1, 'omission marker')
    count = 0
    for a, b in edges:
        if deleted not in (a, b):
            require(word[a] != word[b], ('monochromatic edge', a, b))
            count += 1
    return count

def build():
    manifest = json.loads((HERE/'manifest.json').read_text())
    for path, expected in manifest['inputs'].items():
        require(digest((REPO/path).read_bytes()) == expected, ('input identity', path))
    source = REPO/'hadwiger_nelson_neutral_mutation_candidate/verify.py'
    spec = importlib.util.spec_from_file_location('mutation_parent', source)
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    cert = json.loads((source.parent/'certificate.json').read_text())
    inputs = parent.load_inputs(cert)  # Checks the parent's additional data pins.
    active, original_rows, swaps = parent.construct(cert, inputs)
    parent_edges = parent.strict_edges(original_rows)
    require(len(parent_edges) == 2447, 'parent edge count')
    packed, five, _ = parent.check_colourings(cert, inputs, active, swaps, parent_edges)
    words = [parent.unpack(packed[127*v:127*(v+1)], v) for v in range(509)]
    families = [[word] for word in words]
    extra_checks = 0
    for path in ('hadwiger_nelson_cyclic_batch_probe/gate_certificate.json',
                 'hadwiger_nelson_hinge_flip_gate/certificate.json'):
        extra = json.loads((REPO/path).read_text())
        raw = base64.b64decode(extra['additional_rows_base64'], validate=True)
        require(digest(raw) == extra['additional_rows_sha256'], 'additional word hash')
        sizes = extra['additional_family_sizes']
        require(len(sizes) == 509 and all(type(n) is int and n >= 0 for n in sizes), 'additional family sizes')
        require(sum(sizes) == extra['additional_rows'] and len(raw) == 127*sum(sizes), 'additional payload size')
        offset = 0
        for v, count in enumerate(sizes):
            for _ in range(count):
                word = parent.unpack(raw[offset:offset+127], v)
                offset += 127
                require(all(c in range(4) for u,c in enumerate(word) if u != v), 'additional colour domain')
                for a,b in parent_edges:
                    if v not in (a,b):
                        require(word[a] != word[b], ('additional monochromatic edge', v,a,b))
                        extra_checks += 1
                families[v].append(word)
        require(offset == len(raw), 'unused additional bytes')
    require(sum(map(len, families)) == 1015, 'combined inherited library size')
    points = [tuple(3*x for x in row) for row in original_rows]
    catalogue = json.loads((REPO/'hadwiger_nelson_parts509_swap_closure/completion_points.json').read_text())['points']
    q = catalogue[10]
    row = [SCALE*Fraction(x) for axis in ('x', 'y') for x in q[axis]]
    require(len(row) == 16 and all(x.denominator == 1 for x in row), 'new coordinate')
    points.append(tuple(map(int, row)))
    require(len(points) == len(set(points)) == 510, 'collision merging')
    target = (SCALE*SCALE,)+(0,)*7
    edges = [e for e in combinations(range(510), 2) if norm(points[e[0]], points[e[1]]) == target]
    require(len(edges) == 2456 and [e for e in edges if e[1] < 509] == parent_edges, 'complete strict graph')
    neighbours = [a for a, b in edges if b == 509]
    require(neighbours == [18, 43, 56, 64, 151, 166, 237, 284, 325], 'new neighbours')
    require([active[v] for v in neighbours] == q['neighbors'], 'unchanged original neighbour set')
    require(len(five) == 509, 'parent five-word length')
    five = list(five)+[4]
    check_word(edges, five, palette=range(5))
    return {'points': points, 'edges': edges, 'parent_words': words, 'families': families, 'five': five,
            'neighbours': neighbours, 'source_labels': active, 'additional_parent_word_edge_checks':extra_checks}

def decode_new(certificate):
    require(certificate['format'] == 'mutant-point10-singleton-cover-v1', 'certificate format')
    deleted = certificate['new_deleted_vertices']
    require(deleted == sorted(set(deleted)) and all(type(v) is int and 0 <= v < 509 for v in deleted), 'deletion labels')
    require(certificate['rows'] == len(deleted) == 3 and certificate['colours_per_row'] == 509
            and certificate['bytes_per_row'] == 128, 'payload dimensions')
    data = base64.b64decode(certificate['packed_colours_base64'], validate=True)
    require(digest(data) == certificate['packed_sha256'] and len(data) == 3*128, 'payload identity')
    result = {}
    for k, missing in enumerate(deleted):
        row = data[128*k:128*(k+1)]
        require(row[-1] >> 2 == 0, 'nonzero padding')
        values = iter((row[i//4] >> (2*(i % 4))) & 3 for i in range(509))
        result[missing] = [-1 if v == missing else next(values) for v in range(510)]
    return result

def instance(g, deleted):
    require(type(deleted) is int and 0 <= deleted < 509, 'CNF deletion')
    keep = [v for v in range(510) if v != deleted]
    pos = {v: i for i, v in enumerate(keep)}
    es = [(a, b) for a, b in g['edges'] if deleted not in (a, b)]
    clauses = [[4*i+c+1 for c in range(4)] for i in range(509)]
    clauses.extend([-(4*pos[a]+c+1), -(4*pos[b]+c+1)] for a, b in es for c in range(4))
    adjacent = {v: set() for v in keep}
    for a, b in es:
        adjacent[a].add(b)
        adjacent[b].add(a)
    tri = next((a, b, c) for a, b in es for c in sorted(adjacent[a] & adjacent[b]) if b < c)
    clauses.extend([[4*pos[v]+c+1] for c, v in enumerate(tri)])
    return (f'p cnf 2036 {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode()

def compute(certificate=None, graph=None):
    g = graph or build()
    certificate = certificate or json.loads((HERE/'certificate.json').read_text())
    new = decode_new(certificate)
    forced = {}
    inherited = []
    unresolved = []
    checks = 0
    for v, family in enumerate(g['families']):
        extension = next((list(word)+[min(available)] for word in family
                          if (available := set(range(4)) - {word[x] for x in g['neighbours'] if x != v})), None)
        if extension is not None:
            require(v not in new, 'redundant new row')
            expanded = extension
            inherited.append(v)
        else:
            require(v in new, ('missing new row', v))
            expanded = new[v]
            unresolved.append(v)
        checks += check_word(g['edges'], expanded, v)
        forced[v] = expanded
    require(len(inherited) == 506 and unresolved == sorted(new) == [18,107,275] and len(forced) == 509, 'complete forced set')
    # Optional reconstruction of the preflight's maximum-size candidate count.
    initial_pairs = 0
    for u, v in combinations(unresolved, 2):
        if all({word[x] for x in g['neighbours'] if x not in (u, v)} == set(range(4)) for d in (u, v) for word in g['families'][d]):
            initial_pairs += 1
    require(initial_pairs == 3, 'initial residual')
    adjacent = {v:set() for v in range(509)}
    for a,b in g['edges']:
        if b < 509:
            adjacent[a].add(b); adjacent[b].add(a)
    # A hinge replacement of v by q requires two common unit neighbours.
    require(all(len(adjacent[v] & set(g['neighbours'])) < 2 for v in unresolved), 'old hinge family overlap')
    # Every support of size <=508 omits at least one of these509 forced
    # original vertices and is therefore a restriction of a checked word.
    edge_bytes = ''.join(f'{a} {b}\n' for a, b in g['edges']).encode()
    word_bytes = b''.join(bytes(c for c in forced[v] if c >= 0) for v in range(509))
    return {'all_checks': True, 'host_vertices': 510, 'host_edges': 2456,
            'exact_pair_checks': 129795, 'inherited_single_deletion_words': len(inherited),
            'new_single_deletion_words': len(new), 'forced_original_vertices': len(forced),
            'single_deletion_edge_checks': checks, 'proper_host_five_colouring_checked': True,
            'additional_parent_words_checked':506,
            'additional_parent_word_edge_checks':g['additional_parent_word_edge_checks'],
            'initial_uncovered_two_deletions': initial_pairs,
            'three_remaining_pairs_outside_old_hinge_family':True,
            'all_at_most508_subgraphs_four_colourable': True,
            'strict_induced_non_four_iff_contains_parent': True,
            'minimum_five_chromatic_order': 509,
            'minimum_order_lower_bound_requires_no_unsat_certificate': True,
            'equality_uses_imported_parent_non_four_theorem': True,
            'imported_parent_drat_replayed_this_run': False,
            'host_edge_sha256': digest(edge_bytes), 'expanded_words_sha256': digest(word_bytes),
            'record_improvement': False}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-cnf', type=Path)
    parser.add_argument('--deleted', type=int, default=501)
    args = parser.parse_args()
    g = build()
    result = compute(graph=g)
    if args.write_cnf:
        args.write_cnf.write_bytes(instance(g, args.deleted))
    print(json.dumps(result, indent=2, sort_keys=True))
