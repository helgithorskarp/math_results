"""Independently check exact geometry, colour witnesses and the unit-only proof."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import geometry as G
import integer_audit as A


def proof_checker():
    path = G.ROOT.parent / 'hadwiger_nelson_ei_global_interfaces' / 'lrat.py'
    G.require(hashlib.sha256(path.read_bytes()).hexdigest() == G.read('proof_manifest.json')['lrat_checker_sha256'],
              'changed proof checker')
    spec = importlib.util.spec_from_file_location('terminal_core_lrat', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def word_check(word, n, edges, colours):
    G.require(type(word) is str and len(word) == n and set(word) <= set(map(str, range(colours))), 'word format')
    G.require(all(word[u] != word[v] for u, v in edges), 'colouring violates a unit edge')


def verify(proof):
    rows = G.rows()
    n = len(rows)
    pins = [rows.index(p) for p in ((0, 0, 0, 0), (0, 0, 96, 0))]
    edges = G.half_edges(rows)
    full_edges, labels, cross_edges = G.spindle(rows)
    points = A.points(rows)
    G.require(len(points) == len(set(points)) == 2*n-1, 'spindle point collision')
    direct_edges, survivors = A.edges(points)
    G.require(full_edges == direct_edges, 'independent full edge enumeration differs')
    G.require(edges == [(i, j) for i, j in full_edges if j < n], 'half induced edge mismatch')
    cert = G.read('certificate.json')
    G.require(cert['pins'] == pins and cert['half_vertices'] == n and cert['half_edges'] == len(edges), 'half metadata')
    G.require(cert['full_vertices'] == len(points) and cert['full_edges'] == len(full_edges), 'full metadata')
    word_check(cert['half_four_colouring'], n, edges, 4)
    word_check(cert['full_five_colouring'], len(points), full_edges, 5)
    G.require(set(cert['half_four_colouring']) == set('0123') and
              set(cert['full_five_colouring']) == set('01234'), 'witness colour counts')
    G.require(cert['half_four_colouring'][pins[0]] == cert['half_four_colouring'][pins[1]], 'terminal colouring')
    clauses = G.cnf(n, edges, pins)
    proof_stats = proof_checker().verify(clauses, 4*n, proof)
    terminal_edge = tuple(sorted((pins[1], labels[pins[1]])))
    G.require(terminal_edge in full_edges, 'missing spindle contradiction edge')
    internal = set(edges) | {tuple(sorted((labels[u], labels[v]))) for u, v in edges}
    G.require(set(full_edges)-internal == {terminal_edge}, 'unexpected proper cross edge')
    half_word = cert['half_four_colouring']
    copied_word = half_word + ''.join('4' if v == pins[1] else c for v, c in enumerate(half_word) if v != pins[0])
    G.require(cert['full_five_colouring'] == copied_word, 'explicit fifth-colour recipe')
    result = {
        'verified': True, 'half_vertices': n, 'half_edges': len(edges),
        'half_chromatic_number': 4, 'terminal_distance_squared': [64, 9],
        'all_proper_four_colourings_have_equal_terminals': True,
        'full_vertices': len(points), 'full_edges': len(full_edges), 'full_chromatic_number': 5,
        'full_exact_pair_checks': len(points)*(len(points)-1)//2,
        'constant_coefficient_filter_survivors': survivors,
        'cross_pairs_including_shared_origin_edges': len(cross_edges),
        'proper_cross_edges': 1,
        'cnf_variables': 4*n, 'cnf_clauses': len(clauses),
        'cnf_sha256': hashlib.sha256(G.dimacs(n, clauses).encode()).hexdigest(),
        'positive_hint_lrat': proof_stats,
        'coordinate_rows_sha256': G.digest(rows), 'full_integer_points_sha256': G.digest(points),
        'half_edges_sha256': G.digest(edges), 'full_edges_sha256': G.digest(full_edges),
        'record_improvement': len(points) <= 508,
        'unit_edges_only_in_forcing_formula': True,
        'original_component_forcing_theorems_needed': False,
    }
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lrat', required=True)
    args = parser.parse_args()
    result = verify(args.lrat)
    expected = G.ROOT / 'expected.json'
    if expected.exists():
        G.require(result == G.read('expected.json'), 'expected-result mismatch')
    print(json.dumps(result, sort_keys=True, indent=2))
