#!/usr/bin/env python3
"""Solver-free check, with closed-form arithmetic independent of discover.py."""
from pathlib import Path
from itertools import combinations, permutations, product
from copy import deepcopy
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TERMINALS = (141, 142, 144)
PRIVATE = tuple(v for v in range(159) if v not in TERMINALS)
SOURCE = ROOT / 'hadwiger_nelson_nonmono159_214_lowden2/points159.tsv'
EXTENSIONS = ROOT / 'hadwiger_nelson_long_terminal_gluing/certificate.json'
SOURCE_HASH = '4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02'
EXTENSION_HASH = '26206782c1937d481d06e05ed95284405a188c66c1073a48a8d30dd537b0a830'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def square(a):
    # Basis 1,sqrt(3),sqrt(11),sqrt(33); this is not the producer's
    # generic eight-dimensional multiplication loop.
    p, q, r, s = a
    return (p*p+3*q*q+11*r*r+33*s*s, 2*p*q+22*r*s,
            2*p*r+6*q*s, 2*p*s+2*q*r)


def distance144(a, b):
    dx = square(tuple(x-y for x, y in zip(a[0], b[0])))
    dy = square(tuple(x-y for x, y in zip(a[1], b[1])))
    return tuple(x+y for x, y in zip(dx, dy))


def graph():
    need(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_HASH, 'source SHA256')
    lines = SOURCE.read_text().splitlines()
    need(lines[0] == '# scale 12', 'coordinate scale')
    points = []
    for row in lines:
        if not row.strip() or row.startswith('#'):
            continue
        coefficients = tuple(map(int, row.split()))
        need(len(coefficients) == 16, 'coordinate arity')
        need(all(coefficients[i] == 0 for i in (2, 3, 6, 7, 10, 11, 14, 15)),
             'source outside quadratic tower')
        points.append((tuple(coefficients[i] for i in (0, 1, 4, 5)),
                       tuple(coefficients[i] for i in (8, 9, 12, 13))))
    need(len(points) == len(set(points)) == 159, 'distinct exact points')
    edges = [(a, b) for a, b in combinations(range(159), 2)
             if distance144(points[a], points[b]) == (144, 0, 0, 0)]
    need(len(edges) == 646, 'strict unit edges')
    need(all(distance144(points[a], points[b]) == (1008, 0, 0, 0)
             for a, b in combinations(TERMINALS, 2)), 'terminal triangle sqrt7')
    return edges


def word_check(word, deleted, edges):
    need(type(word) is str and len(word) == 159, 'word length/type')
    need(set(word) <= set('0123-'), 'palette')
    need([i for i, c in enumerate(word) if c == '-'] == [deleted], 'deleted marker')
    need(all(word[a] != word[b] for a, b in edges if deleted not in (a, b)),
         'retained unit edge')


def deletion_check(cert, edges):
    need(cert['source_sha256'] == SOURCE_HASH, 'certificate source binding')
    need(cert['terminals'] == list(TERMINALS), 'certificate terminals')
    rows = cert['deletion_colourings']
    need(all(type(r['deleted']) is int for r in rows), 'deleted index type')
    need([r['deleted'] for r in rows] == list(PRIVATE), 'complete ordered deletion coverage')
    for row in rows:
        v, word = row['deleted'], row['colours']
        word_check(word, v, edges)
        need(''.join(word[t] for t in TERMINALS) == '000', 'monochromatic terminals')
    return {r['deleted']: r['colours'] for r in rows}


def nonmono_check(edges):
    need(hashlib.sha256(EXTENSIONS.read_bytes()).hexdigest() == EXTENSION_HASH,
         'inherited extension source SHA256')
    source = json.loads(EXTENSIONS.read_text())['159']
    need(source['terminals'] == list(TERMINALS), 'inherited terminals')
    rows = source['extensions']
    need([r['pattern'] for r in rows] == ['001', '010', '011', '012'], 'nonmono equality patterns')
    for row in rows:
        word = row['colours']
        need(len(word) == 159 and set(word) <= set('0123'), 'inherited word')
        need(all(word[a] != word[b] for a, b in edges), 'inherited unit edge')
        need(''.join(word[t] for t in TERMINALS) == row['pattern'], 'inherited pattern')
    return rows


def all_boundaries(mono, nonmono, edges):
    # Explicitly decode and check every labelled four-colour boundary,
    # not just a solver SAT result or the number of equality patterns.
    assignments = list(product('0123', repeat=3))
    total_checks = 0
    for deleted in PRIVATE:
        cases = [mono[deleted]] + [r['colours'][:deleted]+'-'+r['colours'][deleted+1:]
                                   for r in nonmono]
        patterns = {}
        for word in cases:
            for palette in permutations('0123'):
                target = tuple(palette[int(word[t])] for t in TERMINALS)
                if target not in patterns:
                    patterns[target] = ''.join('-' if c == '-' else palette[int(c)] for c in word)
        need(set(patterns) == set(assignments), 'all 64 terminal assignments')
        retained = [(a, b) for a, b in edges if deleted not in (a, b)]
        for target in assignments:
            word = patterns[target]
            word_check(word, deleted, retained)
            need(tuple(word[t] for t in TERMINALS) == target, 'decoded boundary')
            total_checks += len(retained)
    return total_checks


def reject_corruptions(cert, edges):
    trials = []
    c = deepcopy(cert); c['deletion_colourings'].pop(); trials.append(('missing deletion', c))
    c = deepcopy(cert); c['deletion_colourings'][1]['deleted'] = 0; trials.append(('duplicate deletion', c))
    c = deepcopy(cert); c['terminals'][0] = 0; trials.append(('wrong terminal', c))
    c = deepcopy(cert); c['source_sha256'] = '0'*64; trials.append(('wrong source hash', c))
    c = deepcopy(cert); row = c['deletion_colourings'][0]; w = list(row['colours'])
    w[row['deleted']] = '0'; row['colours'] = ''.join(w); trials.append(('missing deleted marker', c))
    c = deepcopy(cert); row = c['deletion_colourings'][0]; w = list(row['colours'])
    a, b = next((a, b) for a, b in edges if row['deleted'] not in (a, b))
    w[a] = w[b]; row['colours'] = ''.join(w); trials.append(('retained edge conflict', c))
    c = deepcopy(cert); row = c['deletion_colourings'][0]
    row['colours'] = ''.join('-' if z == '-' else str((int(z)+1) % 4) for z in row['colours'])
    trials.append(('wrong boundary colour', c))
    for name, c in trials:
        try:
            deletion_check(c, edges)
        except ValueError:
            pass
        else:
            raise RuntimeError('accepted corrupted certificate: '+name)
    return [name for name, _ in trials]


def run(certificate, producer_edges=None):
    edges = graph()
    if producer_edges is not None:
        need([list(e) for e in edges] == json.loads(producer_edges.read_text()),
             'entrywise independent strict-edge comparison')
    cert = json.loads(certificate.read_text())
    mono = deletion_check(cert, edges)
    nonmono = nonmono_check(edges)
    edge_checks = all_boundaries(mono, nonmono, edges)
    rejected = reject_corruptions(cert, edges)
    degree_sum_private = sum(sum(v in e for e in edges) for v in PRIVATE)
    need(edge_checks == 64*(156*646-degree_sum_private), 'edge-check count identity')
    return {'status': 'EVERY_PROPER_TERMINAL_PRESERVING_A159_REDUCTION_EXTENDS_ALL_64_BOUNDARIES',
            'record_improvement': False, 'source_vertices': 159, 'source_edges': 646,
            'all_exact_pairs_checked': 12561, 'terminals': list(TERMINALS),
            'terminal_squared_distance': 7, 'positive_single_deletion_witnesses': 156,
            'mandatory_private_vertices_in_any_forcing_subgraph': 156,
            'proper_private_subsets_covered': str(2**156-1),
            'boundary_assignments_per_deletion': 64, 'decoded_extensions_checked': 156*64,
            'decoded_extension_edge_checks': edge_checks,
            'certificate_sha256': hashlib.sha256(certificate.read_bytes()).hexdigest(),
            'strict_edge_list_sha256': hashlib.sha256((json.dumps(edges, separators=(',', ':'))+'\n').encode()).hexdigest(),
            'rejected_corruptions': rejected, 'verification_solver_calls': 0,
            'negative_forcing_of_full_A159_is_a_premise': False,
            'five_proper_reduction_corollary_uses_classical_Brooks_theorem': True,
            'proposed_private_budget': 100, 'private_vertices_removed_from_each_module': 56}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE/'certificate.json')
    parser.add_argument('--producer-edges', type=Path)
    parser.add_argument('--check-expected', action='store_true')
    args = parser.parse_args()
    result = run(args.certificate, args.producer_edges)
    if args.check_expected:
        need(result == json.loads((HERE/'EXPECTED.json').read_text()), 'expected results')
    print(json.dumps(result, indent=2, sort_keys=True))
