#!/usr/bin/env python3
"""Reconstruct and check a nine-move Parts mutation; Python standard library only."""
import argparse
import base64
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_inputs(certificate):
    result = {}
    for name, expected in certificate['source_sha256'].items():
        data = (REPO / name).read_bytes()
        require(digest(data) == expected, 'source hash mismatch: ' + name)
        result[name] = json.loads(data)
    return result


def construct(certificate, inputs):
    source = inputs['hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json']
    swaps = inputs['hadwiger_nelson_parts509_swap_closure/swap_certificate.json']['swaps']
    moves = certificate['moves']
    require(moves == [0, 1, 4, 5, 6, 7, 8, 9, 10], 'wrong construction')
    removed = {swaps[i]['u'] for i in moves}
    active = sorted((set(range(509)) - removed) | {509 + i for i in moves})
    require(len(active) == 509 and len(removed) == 9, 'bad mutation cardinality')
    rows = []
    for u in active:
        pair = source['coordinates'][str(u)] if u < 509 else [
            swaps[u - 509]['q_x'], swaps[u - 509]['q_y']]
        row = [96 * Fraction(a) for axis in pair for a in axis]
        require(len(row) == 16 and all(a.denominator == 1 for a in row),
                'coordinate outside declared scale-96 basis')
        rows.append(tuple(map(int, row)))
    require(len(set(rows)) == 509, 'coincident vertices')
    original = {tuple(96 * Fraction(a) for axis in source['coordinates'][str(v)] for a in axis)
                for v in range(509)}
    require(len(original) == 509 and len(original & set(rows)) == 500,
            'wrong geometric overlap with Parts')
    require(digest(json.dumps(rows, separators=(',', ':')).encode()) ==
            certificate['integer_coordinate_sha256'], 'coordinate digest')
    return active, rows, swaps


def square(row):
    # e_i e_j = radicands[i & j] e_(i xor j).
    out = [0] * 8
    for i in range(8):
        for j in range(i, 8):
            out[i ^ j] += (1 if i == j else 2) * row[i] * row[j] * RADICANDS[i & j]
    return out


def strict_edges(rows):
    edges = []
    for i, j in combinations(range(len(rows)), 2):
        difference = [a - b for a, b in zip(rows[i], rows[j])]
        norm = [a + b for a, b in zip(square(difference[:8]), square(difference[8:]))]
        if norm == [96 * 96] + [0] * 7:
            edges.append((i, j))
    return edges


def unpack(row, deleted):
    require(len(row) == 127, 'wrong packed row length')
    values = iter((b >> s) & 3 for b in row for s in (0, 2, 4, 6))
    return [-1 if i == deleted else next(values) for i in range(509)]


def decode_families(inputs):
    base = inputs['hadwiger_nelson_parts509_criticality/certificate.json']
    extra = inputs['hadwiger_nelson_parts509_swap_closure/swap_certificate.json']
    base_bytes = base64.b64decode(base['deletion_colorings_base64'], validate=True)
    extra_bytes = base64.b64decode(extra['family_rows_base64'], validate=True)
    sizes = extra['family_sizes']
    require(len(base_bytes) == 509 * 127 and len(sizes) == 509, 'bad source family')
    families, offset = [], 0
    for u, count in enumerate(sizes):
        require(type(count) is int and count >= 0, 'bad family count')
        family = [unpack(base_bytes[127 * u:127 * (u + 1)], u)]
        for _ in range(count):
            family.append(unpack(extra_bytes[offset:offset + 127], u))
            offset += 127
        families.append(family)
    require(offset == len(extra_bytes), 'unused source rows')
    return families


def check_colourings(certificate, inputs, active, swaps, edges):
    families = decode_families(inputs)
    refs = certificate['inherited_family_indices']
    fresh = {d: base64.b64decode(row, validate=True)
             for d, row in certificate['fresh_deletion_rows']}
    require(len(refs) == 509 and len(fresh) == len(certificate['fresh_deletion_rows']) == 42,
            'incomplete or duplicate deletion evidence')
    require(set(fresh) == {d for d, ref in enumerate(refs) if ref == -1}, 'fresh row keys')
    neighbours = [set() for _ in active]
    for a, b in edges:
        neighbours[a].add(b)
        neighbours[b].add(a)
    packed, five = bytearray(), None
    for deleted, (u, ref) in enumerate(zip(active, refs)):
        require(type(ref) is int and ref >= -1, 'bad family reference')
        if ref == -1:
            word = unpack(fresh[deleted], deleted)
        else:
            old_u = u if u < 509 else swaps[u - 509]['u']
            require(ref < len(families[old_u]), 'family reference outside source')
            old = families[old_u][ref]
            word = [old[v] if v < 509 else -1 for v in active]
            word[deleted] = -1
            for q, label in enumerate(active):
                if label < 509 or q == deleted:
                    continue
                used = {word[v] for v in neighbours[q] if v != deleted and word[v] >= 0}
                available = set(range(4)) - used
                require(bool(available), 'inherited row cannot extend')
                word[q] = min(available)
        require(all(c in range(4) for v, c in enumerate(word) if v != deleted),
                'invalid deletion colour')
        require(all(word[a] != word[b] for a, b in edges if deleted not in (a, b)),
                'monochromatic edge in deletion word')
        values = [c for v, c in enumerate(word) if v != deleted]
        packed.extend(sum(values[k + j] << (2 * j) for j in range(4))
                      for k in range(0, 508, 4))
        if five is None:
            five = word.copy()
            five[deleted] = 4
    require(digest(packed) == certificate['deletion_words_sha256'], 'deletion word digest')
    require(all(c in range(5) for c in five) and
            all(five[a] != five[b] for a, b in edges), 'invalid five-colouring')
    return bytes(packed), five, neighbours


def make_cnf(edges, neighbours):
    clauses = []
    for v in range(509):
        clauses.append([4 * v + c + 1 for c in range(4)])
        clauses.extend([-(4 * v + a + 1), -(4 * v + b + 1)]
                       for a, b in combinations(range(4), 2))
    for a, b in edges:
        clauses.extend([-(4 * a + c + 1), -(4 * b + c + 1)] for c in range(4))
    triangle = next((a, b, c) for a, b in edges
                    for c in sorted(neighbours[a] & neighbours[b]) if b < c)
    clauses.extend([[4 * v + c + 1] for c, v in enumerate(triangle)])
    data = (f'p cnf 2036 {len(clauses)}\n' +
            ''.join(' '.join(map(str, clause)) + ' 0\n' for clause in clauses)).encode()
    return data, triangle, len(clauses)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='directory for generated evidence')
    parser.add_argument('--kissat', help='optional Kissat executable; generates a new DRAT proof')
    parser.add_argument('--proof', type=Path, help='existing DRAT proof instead of --kissat')
    parser.add_argument('--drat-trim', help='DRAT checker, required with --kissat or --proof')
    args = parser.parse_args()
    require(not (args.kissat and args.proof), 'choose one proof source')
    require(bool(args.drat_trim) == bool(args.kissat or args.proof), 'proof checker/source mismatch')
    certificate = json.loads((HERE / 'certificate.json').read_text())
    inputs = load_inputs(certificate)
    active, rows, swaps = construct(certificate, inputs)
    edges = strict_edges(rows)
    edge_bytes = ''.join(f'{a} {b}\n' for a, b in edges).encode()
    require(len(edges) == 2447 and digest(edge_bytes) == certificate['edge_sha256'], 'edge digest')
    packed, five, neighbours = check_colourings(certificate, inputs, active, swaps, edges)
    cnf, triangle, clauses = make_cnf(edges, neighbours)
    require(digest(cnf) == certificate['cnf_sha256'] and clauses == 13354 and
            list(triangle) == certificate['triangle_pin'], 'CNF mismatch')
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'graph.json').write_text(json.dumps({'scale': 96, 'coordinates': rows,
        'edges': edges, 'source_labels': active, 'five_colouring': five}, separators=(',', ':')) + '\n')
    (args.output / 'deletion_words.bin').write_bytes(packed)
    cnf_path = args.output / 'graph.cnf'
    cnf_path.write_bytes(cnf)
    result = {'vertices': 509, 'edges': len(edges), 'pair_checks': 129286,
              'original_points_retained': 500, 'deletion_words_checked': 509,
              'five_colouring_checked': True, 'cnf_sha256': digest(cnf), 'DRAT_verified': False}
    if args.kissat or args.proof:
        proof_path = args.proof or (args.output / 'graph.drat')
        if args.kissat:
            run = subprocess.run([args.kissat, '--quiet', str(cnf_path), str(proof_path)],
                                 capture_output=True, text=True)
            (args.output / 'kissat.log').write_text(run.stdout + run.stderr)
            require(run.returncode == 20, 'Kissat did not return UNSAT')
        run = subprocess.run([args.drat_trim, str(cnf_path), str(proof_path)],
                             capture_output=True, text=True)
        (args.output / 'drat-trim.log').write_text(run.stdout + run.stderr)
        require(run.returncode == 0 and 's VERIFIED' in run.stdout, 'DRAT verification failed')
        result.update(DRAT_verified=True, proof_sha256=digest(proof_path.read_bytes()),
                      matches_recorded_proof=digest(proof_path.read_bytes()) == certificate['proof_sha256'])
    (args.output / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
