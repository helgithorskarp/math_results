#!/usr/bin/env python3
"""Proof by ten positive covers and exhaustive small negative interfaces.

No producer import, Boolean projection, native solver or proof trace is used.
"""
import argparse
from collections import Counter
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'hadwiger_nelson_heule632_pair_pilot'))
import independent as geometry


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def canonical(colour, mandatory):
    # First-occurrence normalization, implemented by the ordered colour classes.
    classes = sorted((sorted(v for v in mandatory if colour[v] == c) for c in '0123'), key=lambda row: row[0])
    answer = ['.'] * 632
    for index, members in enumerate(classes):
        for v in members:
            answer[v] = str(index)
    return ''.join(answer)


def prepare():
    plan = json.loads((HERE / 'plan.json').read_text())
    for path, digest in plan['input_files'].items():
        need(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, 'input identity: ' + path)
    boundary = json.loads((ROOT / 'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    mandatory = sorted(boundary['mandatory_vertices'])
    optional = set(boundary['optional_vertices'])
    need(len(mandatory) == 492 and len(optional) == 68 and not set(mandatory) & optional, 'partition')
    fixed = json.loads((ROOT / 'hadwiger_nelson_heule560_degree_family/certificate.json').read_text())['cover_colouring']
    _, edges, _ = geometry.geometry()
    adj = {v: set() for v in set(mandatory) | optional}
    for u, v in edges:
        if u in adj and v in adj:
            adj[u].add(v)
            adj[v].add(u)
    medges = [(u, v) for u, v in edges if u in set(mandatory) and v in set(mandatory)]
    need(all(fixed[u] != fixed[v] for u, v in medges), 'fixed mandatory colouring')
    family = set()
    full_slots = 0
    component_stats = []
    for a, b in itertools.combinations('0123', 2):
        vertices = [v for v in mandatory if fixed[v] in (a, b)]
        parent = {v: v for v in vertices}

        def root(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v

        # Union-find differs from the producer's induced BFS construction.
        for u, v in medges:
            if u in parent and v in parent:
                parent[root(u)] = root(v)
        blocks = {}
        for v in vertices:
            blocks.setdefault(root(v), []).append(v)
        components = sorted(blocks.values(), key=lambda row: row[0])
        component_stats.append({'pair': [int(a), int(b)], 'component_sizes': list(map(len, components))})
        # Enumerate ALL component subsets, with no complement quotient.
        for switches in itertools.product((False, True), repeat=len(components)):
            text = list(fixed)
            for switch, members in zip(switches, components):
                if switch:
                    for v in members:
                        text[v] = b if fixed[v] == a else a
            family.add(canonical(text, mandatory))
            full_slots += 1
    need(full_slots == 246 and len(family) == 118, 'complete family counts')
    family = sorted(family)
    for c in family:
        need(all(c[u] != c[v] for u, v in medges), 'generated proper M colouring')
    lists = [{v: sorted(set(range(4)) - {int(c[n]) for n in adj[v] & set(mandatory)}) for v in optional} for c in family]
    digest = hashlib.sha256(''.join(c + '\n' for c in family).encode('ascii')).hexdigest()
    return {'mandatory': mandatory, 'optional': optional, 'edges': edges, 'family': family, 'lists': lists,
            'family_sha256': digest, 'component_stats': component_stats, 'full_slots': full_slots,
            'mandatory_template_edge_checks': len(family) * len(medges)}


def check(certificate, data):
    optional = data['optional']
    mandatory = data['mandatory']
    need(certificate['quotient_slots'] == 123 and certificate['distinct_templates'] == len(data['family']), 'template cardinality claims')
    need(certificate['canonical_template_stream_sha256'] == data['family_sha256'], 'all template bytes')
    rows = certificate['combined_minimal_nonextending_sets']
    forbidden = [set(row) for row in rows]
    need(rows and all(row == sorted(set(row)) for row in rows), 'nonempty canonical obstruction family')
    need(all(set(row) <= optional for row in rows), 'obstruction universe')
    need(len({tuple(row) for row in rows}) == len(rows), 'distinct obstructions')
    need(not any(a < b for a in forbidden for b in forbidden), 'minimal obstruction antichain')

    # Complete direct enumeration on each small induced list problem. This
    # proves failure under every template, not failure under arbitrary M colours.
    negative_cases = 0
    negative_assignments = 0
    for row in rows:
        need(len(row) <= 4, 'negative direct-enumeration bound')
        internal = [(row.index(u), row.index(v)) for u, v in data['edges'] if u in row and v in row]
        for lists in data['lists']:
            negative_cases += 1
            for assignment in itertools.product(*(lists[v] for v in row)):
                negative_assignments += 1
                need(any(assignment[i] == assignment[j] for i, j in internal), 'claimed obstruction extends a template')

    endpoints = sorted(set().union(*forbidden))
    need(len(endpoints) <= 16, 'endpoint enumeration cap')
    good = []
    for mask in range(1 << len(endpoints)):
        chosen = {v for i, v in enumerate(endpoints) if mask >> i & 1}
        if not any(row <= chosen for row in forbidden):
            good.append(chosen)
    maximal = [chosen for chosen in good if all(any(row <= chosen | {v} for row in forbidden)
                                              for v in set(endpoints) - chosen)]
    expected_omissions = {frozenset(set(endpoints) - chosen) for chosen in maximal}
    covers = certificate['maximal_extending_cover_colourings']
    need(len(covers) == len(expected_omissions), 'positive cover count')
    need({frozenset(row['omitted_optional']) for row in covers} == expected_omissions, 'complete positive boundary')
    cover_stats = []
    family_index = {c: i for i, c in enumerate(data['family'])}
    for row in covers:
        omitted = row['omitted_optional']
        need(omitted == sorted(set(omitted)), 'canonical omission list')
        support = (set(mandatory) | optional) - set(omitted)
        c = row['colouring']
        need(len(c) == 632, 'cover string length')
        need(all(c[v] in '0123' if v in support else c[v] == '.' for v in range(632)), 'exact cover support')
        mtext = ''.join(c[v] if v in set(mandatory) else '.' for v in range(632))
        need(mtext in family_index, 'cover mandatory template membership')
        edge_checks = 0
        for u, v in data['edges']:
            if u in support and v in support:
                need(c[u] != c[v], 'positive monochromatic edge')
                edge_checks += 1
        cover_stats.append({'omitted_optional': omitted, 'vertices': len(support), 'edges': edge_checks,
                            'template_index': family_index[mtext]})
    need(all(any(chosen <= larger for larger in maximal) for chosen in good), 'all endpoint patterns covered')
    for bad in forbidden:
        need(all(any(bad - {v} <= chosen for chosen in good) for v in bad), 'each obstruction minimal')
    free = 68 - len(endpoints)
    polynomial = Counter(map(len, good))
    counts = [sum(number * math.comb(free, k - degree) for degree, number in polynomial.items() if 0 <= k - degree <= free)
              for k in range(69)]
    need(counts == certificate['extending_counts_by_optional_size'], 'all size counts')
    need(sum(counts) == len(good) * 2**free, 'all-subsets count')
    return {'component_stats': data['component_stats'], 'full_switch_slots': data['full_slots'],
            'quotient_slots': 123, 'distinct_templates': len(data['family']), 'template_stream_sha256': data['family_sha256'],
            'mandatory_template_edge_checks': data['mandatory_template_edge_checks'], 'negative_template_cases': negative_cases,
            'negative_assignments': negative_assignments, 'combined_minimal_nonextending_sets': rows,
            'endpoint_vertices': endpoints, 'endpoint_patterns': 1 << len(endpoints), 'good_endpoint_patterns': len(good),
            'endpoint_polynomial_coefficients': [polynomial[i] for i in range(len(endpoints) + 1)],
            'cover_stats': cover_stats, 'cover_edge_checks': sum(row['edges'] for row in cover_stats),
            'cover_templates_used': len({row['template_index'] for row in cover_stats}),
            'extending_16': counts[16], 'remaining_16': math.comb(68, 16) - counts[16],
            'extending_at_most16': sum(counts[:17]), 'remaining_at_most16': sum(math.comb(68, k) - counts[k] for k in range(17)),
            'extending_all_subsets': sum(counts), 'whole560_family_closed': False, 'record_improvement': False}


def controls(cert, data):
    variants = []
    bad = copy.deepcopy(cert)
    bad['maximal_extending_cover_colourings'].pop()
    variants.append(('missing_cover', bad))
    bad = copy.deepcopy(cert)
    bad['combined_minimal_nonextending_sets'][0] = [362, 604]
    variants.append(('false_negative_pair', bad))
    bad = copy.deepcopy(cert)
    bad['combined_minimal_nonextending_sets'].pop()
    variants.append(('missing_obstruction', bad))
    bad = copy.deepcopy(cert)
    text = list(bad['maximal_extending_cover_colourings'][0]['colouring'])
    text[0] = str((int(text[0]) + 1) % 4)
    bad['maximal_extending_cover_colourings'][0]['colouring'] = ''.join(text)
    variants.append(('invalid_M_template', bad))
    bad = copy.deepcopy(cert)
    text = list(bad['maximal_extending_cover_colourings'][0]['colouring'])
    text[510] = '.'
    bad['maximal_extending_cover_colourings'][0]['colouring'] = ''.join(text)
    variants.append(('wrong_support', bad))
    bad = copy.deepcopy(cert)
    text = list(bad['maximal_extending_cover_colourings'][0]['colouring'])
    text[505] = text[416]
    bad['maximal_extending_cover_colourings'][0]['colouring'] = ''.join(text)
    variants.append(('optional_monochromatic_edge', bad))
    bad = copy.deepcopy(cert)
    bad['canonical_template_stream_sha256'] = '0' * 64
    variants.append(('false_family_hash', bad))
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
            raise ValueError('corrupt certificate accepted: ' + label)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    data = prepare()
    cert = json.loads(args.certificate.read_text())
    report = check(cert, data)
    report['rejected_controls'] = controls(cert, data)
    report['certificate_sha256'] = hashlib.sha256(args.certificate.read_bytes()).hexdigest()
    report['elapsed_seconds'] = time.monotonic() - start
    (args.out / 'verification.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
