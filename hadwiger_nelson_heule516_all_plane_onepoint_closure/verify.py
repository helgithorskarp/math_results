#!/usr/bin/env python3
"""Exact whole-plane exterior census and direct colouring-cover verification.

No SAT solver is imported. Large generated centre/triple files stay in --work.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations
import argparse
import base64
import copy
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SOURCE = REPO / 'hadwiger_nelson_h516_degree4_surgeries/SOURCE.json'
WORDS = REPO / 'hadwiger_nelson_heule516_single_point_h632_closure/certificate.json'


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unpack(encoded, length):
    raw = base64.b64decode(encoded, validate=True)
    need(len(raw) == (length + 3) // 4, 'packed word length')
    need(base64.b64encode(raw).decode('ascii') == encoded, 'canonical base64')
    values = [(raw[i // 4] >> (2 * (i % 4))) & 3 for i in range(length)]
    need(all(((raw[i // 4] >> (2 * (i % 4))) & 3) == 0
             for i in range(length, len(raw) * 4)), 'packed word padding')
    return values


def pack(values):
    data = bytearray((len(values) + 3) // 4)
    for i, value in enumerate(values):
        data[i // 4] |= value << (2 * (i % 4))
    return base64.b64encode(data).decode('ascii')


def check_cover(source, exterior, certificate, old_rows):
    labels = source['labels']
    label_set = set(labels)
    edges = [tuple(e) for e in source['edges']]
    need(labels == sorted(label_set) and len(labels) == 516, 'base vertex set')
    need(certificate['source_sha256'] == digest(SOURCE), 'certificate source identity')
    need(certificate['target_order'] == 508, 'fixed target order')
    need(certificate['outside_H632_points'] == len(exterior) == 558, 'complete exterior domain')
    ids = [r['centre_index'] for r in exterior]
    need(ids == sorted(set(ids)), 'exterior centre order')
    neighbors = []
    for row in exterior:
        ns = row['neighbors']
        need(ns == sorted(set(ns)) and len(ns) >= 4
             and all(type(i) is int and 0 <= i < 516 for i in ns), 'neighbor list')
        neighbors.append({labels[i] for i in ns})
    additional = certificate['additional_deletion_rows']
    need(additional == sorted(additional, key=lambda r: (r['removed'], r['colours'])),
         'additional row order')
    need(len({(r['removed'], r['colours']) for r in additional}) == len(additional),
         'distinct additional rows')
    need(len(old_rows) == 664, 'inherited row count')
    coverage = [set() for _ in exterior]
    checked_edges = 0
    extension_tests = 0
    removed_vertices = set()
    for row in old_rows + additional:
        need(set(row) == {'removed', 'colours'}, 'colour row fields')
        removed = row['removed']
        need(type(removed) is int and removed in label_set, 'removed vertex')
        removed_vertices.add(removed)
        order = [v for v in labels if v != removed]
        word = unpack(row['colours'], len(order))
        colouring = dict(zip(order, word))
        for u, v in edges:
            if removed not in (u, v):
                need(colouring[u] != colouring[v], 'monochromatic base edge')
                checked_edges += 1
        for i, adjacent in enumerate(neighbors):
            extension_tests += 1
            if len({colouring[v] for v in adjacent if v != removed}) < 4:
                coverage[i].add(removed)
    need(removed_vertices == label_set, 'complete base-deletion witnesses')
    counts = [len(s) for s in coverage]
    need(min(counts) >= 508, 'insufficient target-order deletion coverage')
    return {
        'exterior_points': len(exterior),
        'inherited_deletion_rows': len(old_rows),
        'additional_deletion_rows': len(additional),
        'total_deletion_rows': len(old_rows) + len(additional),
        'proper_base_edge_checks': checked_edges,
        'colour_extension_tests': extension_tests,
        'minimum_covered_deletions': min(counts),
        'maximum_covered_deletions': max(counts),
        'coverage_histogram': dict(sorted(Counter(counts).items())),
        'new_solver_queries_by_verifier': 0,
    }


def controls(source, exterior, certificate, old_rows):
    cases = []
    bad = copy.deepcopy(certificate)
    row = bad['additional_deletion_rows'][0]
    order = [v for v in source['labels'] if v != row['removed']]
    values = unpack(row['colours'], len(order))
    u, v = next(e for e in source['edges'] if row['removed'] not in e)
    values[order.index(u)] = values[order.index(v)]
    row['colours'] = pack(values)
    bad['additional_deletion_rows'].sort(key=lambda r: (r['removed'], r['colours']))
    cases.append(('improper_colour_word', exterior, bad))
    bad = copy.deepcopy(certificate)
    bad['target_order'] = 509
    cases.append(('wrong_target_order', exterior, bad))
    cases.append(('missing_exterior_point', exterior[:-1], certificate))
    bad = copy.deepcopy(certificate)
    bad['additional_deletion_rows'] = []
    cases.append(('insufficient_colouring_cover', exterior, bad))
    rejected = []
    for name, points, cert in cases:
        try:
            check_cover(source, points, cert, old_rows)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('malformed evidence accepted: ' + name)
    return rejected


def run_logged(args, logfile):
    with logfile.open('w') as output:
        subprocess.run(args, check=True, stdout=output, stderr=subprocess.STDOUT)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--reuse-census', action='store_true')
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    for relative, expected in json.loads((HERE / 'INPUTS.json').read_text()).items():
        need(digest(REPO / relative) == expected, 'input hash: ' + relative)
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    python = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else [])
    binary = work / 'filter'
    run_logged(['g++', '-std=c++20', '-O3', '-Wall', '-Wextra', '-Wconversion',
                '-Wshadow', '-pedantic', str(HERE / 'filter.cpp'), '-o', str(binary)],
               work / 'compile.log')
    if not args.reuse_census:
        need(not (work / 'centres.json').exists(), 'choose an unused census work directory')
        run_logged(python + [str(HERE / 'census.py'), '--work', str(work), '--filter', str(binary)],
                   work / 'census.log')
    else:
        # Counts in a cached stream are not completeness evidence. Re-enumerate
        # every triple before accepting an existing census as a certificate.
        run_logged([str(binary), str(work / 'points.txt'), str(work / 'rechecked_survivors.tsv')],
                   work / 'rechecked_filter.json')
        need((work / 'rechecked_survivors.tsv').read_bytes() == (work / 'survivors.tsv').read_bytes(),
             'fresh exhaustive survivor stream')
        need(json.loads((work / 'rechecked_filter.json').read_text())
             == json.loads((work / 'FILTER.json').read_text()), 'fresh filter counts')
    # Recheck every centre incidence and all survivor triples in either mode.
    run_logged(python + [str(HERE / 'audit_geometry.py'), '--work', str(work)],
               work / 'audit_geometry.log')
    geometry = json.loads((work / 'GEOMETRY_AUDIT.json').read_text())
    need(geometry['exterior_sha256'] == digest(work / 'exterior.json'), 'audited exterior identity')
    source = json.loads(SOURCE.read_text())
    exterior = json.loads((work / 'exterior.json').read_text())
    certificate = json.loads((HERE / 'certificate.json').read_text())
    old_rows = json.loads(WORDS.read_text())['deletion_rows']
    colour = check_cover(source, exterior, certificate, old_rows)
    geometry.pop('seconds')
    result = {
        'status': 'ALL_PLANE_ONE_POINT_AUGMENTATIONS_OF_H516_CLOSED_THROUGH_508',
        'new_theorem_domain': 'Every Euclidean point outside the fixed H632 set',
        'whole_plane_corollary_imports': 'h3991 for the 116 points of H632 minus the base',
        'geometry': geometry,
        'colouring_cover': colour,
        'certificate_sha256': digest(HERE / 'certificate.json'),
        'record_improvement': False,
        'independent_author_review_claimed': False,
    }
    if args.controls:
        result['rejected_controls'] = controls(source, exterior, certificate, old_rows)
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    (work / 'result.json').write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
