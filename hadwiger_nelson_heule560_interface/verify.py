#!/usr/bin/env python3
"""Solver-free proof: four positive covers and three forced pair conflicts.

Does not import build.py, project Boolean variables, or trust solver results.
"""
import argparse
from collections import Counter
import copy
import hashlib
import json
import math
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'hadwiger_nelson_heule632_pair_pilot'))
import independent as geometry_checker


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def inputs():
    plan = json.loads((HERE / 'plan.json').read_text())
    for name, digest in plan['input_files'].items():
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, 'input hash: ' + name)
    boundary = json.loads((ROOT / 'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    old = json.loads((ROOT / 'hadwiger_nelson_heule560_degree_family/certificate.json').read_text())
    _, edges, _ = geometry_checker.geometry()
    mandatory, optional = set(boundary['mandatory_vertices']), set(boundary['optional_vertices'])
    require(len(mandatory) == 492 and len(optional) == 68 and not mandatory & optional, 'partition')
    fixed = old['cover_colouring']
    require(len(fixed) == 632 and all(fixed[v] in '0123' for v in mandatory), 'fixed M colouring')
    checks = 0
    for u, v in edges:
        if u in mandatory and v in mandatory:
            require(fixed[u] != fixed[v], 'M monochromatic edge')
            checks += 1
    lists = {}
    for v in optional:
        neighbours = {b if a == v else a for a, b in edges if a == v or b == v}
        forbidden = {int(fixed[n]) for n in neighbours & mandatory}
        lists[v] = sorted(set(range(4)) - forbidden)
    return mandatory, optional, fixed, edges, lists, checks


def check(cert, data):
    mandatory, optional, fixed, edges, lists, mandatory_checks = data
    require(cert['optional_vertices'] == sorted(optional), 'optional labels')
    require(cert['lists'] == {str(v): lists[v] for v in sorted(optional)}, 'interface lists')
    optional_edges = [[u, v] for u, v in edges if u in optional and v in optional]
    require(cert['optional_edges'] == optional_edges, 'optional edges')
    pairs = [[362, 604], [406, 613], [409, 613]]
    require(cert['minimal_nonextending_sets'] == pairs, 'obstruction boundary')
    for u, v in pairs:
        require([u, v] in optional_edges, 'obstruction edge')
        require(len(lists[u]) == 1 and lists[u] == lists[v], 'forced equal colours')

    endpoint = sorted({v for pair in pairs for v in pair})
    require(len(endpoint) == 5, 'endpoint universe')
    # Independently exhaust the 32 patterns, not the producer's transversal
    # generation or existential elimination. Free vertices can all be present.
    good = []
    for mask in range(32):
        chosen = {v for i, v in enumerate(endpoint) if mask >> i & 1}
        if not any(set(pair) <= chosen for pair in pairs):
            good.append(chosen)
    maximal = [chosen for chosen in good if not any(chosen < other for other in good)]
    expected_omissions = {frozenset(set(endpoint) - chosen) for chosen in maximal}
    rows = cert['maximal_extending_cover_colourings']
    require(len(rows) == len(expected_omissions) == 4, 'cover count')
    require({frozenset(row['omitted_optional']) for row in rows} == expected_omissions, 'complete cover omissions')
    cover_stats = []
    full = mandatory | optional
    for row in rows:
        omitted = row['omitted_optional']
        require(omitted == sorted(set(omitted)), 'canonical omission set')
        support = full - set(omitted)
        text = row['colouring']
        require(len(text) == 632, 'colour string length')
        require(all((text[v] in '0123') if v in support else (text[v] == '.') for v in range(632)), 'exact positive support')
        require(all(text[v] == fixed[v] for v in mandatory), 'fixed mandatory colours')
        require(all(int(text[v]) in lists[v] for v in optional & support), 'list colours')
        edge_checks = 0
        for u, v in edges:
            if u in support and v in support:
                require(text[u] != text[v], 'positive monochromatic edge')
                edge_checks += 1
        cover_stats.append({'omitted_optional': omitted, 'vertices': len(support), 'edges': edge_checks})
    require(all(any(chosen <= bigger for bigger in maximal) for chosen in good), 'pattern cover completeness')
    counts = [sum(math.comb(63, k - len(chosen)) for chosen in good if 0 <= k - len(chosen) <= 63)
              for k in range(69)]
    require(cert['extending_counts_by_optional_size'] == counts, 'all cardinality counts')
    # A second elementary polynomial calculation: the endpoint graph is K2
    # disjoint from a three-vertex path, giving (1+2x)(1+3x+x^2).
    require(Counter(map(len, good)) == Counter({0: 1, 1: 5, 2: 7, 3: 2}), 'endpoint polynomial')
    require(sum(counts) == 15 * 2**63, 'total extending subsets')
    return {'mandatory_vertices': 492, 'optional_vertices': 68, 'optional_edges': len(optional_edges),
            'mandatory_edge_checks': mandatory_checks, 'list_size_histogram': dict(sorted(Counter(map(len, lists.values())).items())),
            'obstruction_pairs': pairs, 'endpoint_patterns': 32, 'extending_endpoint_patterns': len(good),
            'cover_stats': cover_stats, 'cover_edge_checks': sum(row['edges'] for row in cover_stats),
            'extending_16': counts[16], 'remaining_16': math.comb(68, 16) - counts[16],
            'extending_at_most16': sum(counts[:17]), 'remaining_at_most16': sum(math.comb(68, k) - counts[k] for k in range(17)),
            'extending_all_subsets': sum(counts), 'whole560_family_closed': False, 'record_improvement': False}


def controls(cert, data):
    variants = []
    bad = copy.deepcopy(cert)
    bad['maximal_extending_cover_colourings'].pop()
    variants.append(('missing_cover', bad))
    bad = copy.deepcopy(cert)
    text = list(bad['maximal_extending_cover_colourings'][0]['colouring'])
    text[362] = '.'
    text[310] = '.'
    bad['maximal_extending_cover_colourings'][0]['colouring'] = ''.join(text)
    variants.append(('wrong_support', bad))
    bad = copy.deepcopy(cert)
    text = list(bad['maximal_extending_cover_colourings'][0]['colouring'])
    text[0] = str((int(text[0]) + 1) % 4)
    bad['maximal_extending_cover_colourings'][0]['colouring'] = ''.join(text)
    variants.append(('changed_fixed_colour', bad))
    bad = copy.deepcopy(cert)
    text = list(bad['maximal_extending_cover_colourings'][0]['colouring'])
    text[505] = text[416]
    bad['maximal_extending_cover_colourings'][0]['colouring'] = ''.join(text)
    variants.append(('optional_monochromatic_edge', bad))
    bad = copy.deepcopy(cert)
    bad['minimal_nonextending_sets'].pop()
    variants.append(('missing_obstruction', bad))
    bad = copy.deepcopy(cert)
    bad['lists']['604'] = [1]
    variants.append(('false_list', bad))
    bad = copy.deepcopy(cert)
    bad['extending_counts_by_optional_size'][16] += 1
    variants.append(('false_count', bad))
    rejected = []
    for label, bad in variants:
        try:
            check(bad, data)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('negative control accepted: ' + label)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    data = inputs()
    cert = json.loads(args.certificate.read_text())
    report = check(cert, data)
    report['rejected_controls'] = controls(cert, data)
    report['certificate_sha256'] = hashlib.sha256(args.certificate.read_bytes()).hexdigest()
    report['elapsed_seconds'] = time.monotonic() - start
    (args.out / 'verification.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
