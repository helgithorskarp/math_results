"""Geometry, 20 deletion witnesses, T375 replay, and independent LRAT check."""
import argparse
import hashlib
import json
from itertools import combinations
import audit
import geometry as G
import lrat


def witnesses(cert, n, edges, triangles, pins):
    G.require(cert['pins'] == pins and cert['vertices'] == n and cert['edges'] == len(edges), 'graph metadata')
    selected = cert['selected_triangles']
    G.require(cert['mask'] == 1682 and cert['available_triangles'] == len(triangles), 'interface metadata')
    G.require(len(selected) == 20 and selected == sorted(map(list, set(map(tuple, selected)))), 'selected triangle format')
    G.require(all(tuple(t) in triangles for t in selected), 'triangle absent')
    words = cert['deletion_colourings']
    G.require(len(words) == len(selected), 'witness count')
    for omitted, word in enumerate(words):
        G.require(type(word) is str and len(word) == n and set(word) <= set('0123'), 'word format')
        G.require(word[pins[0]] == '0' and word[pins[1]] == '1', 'endpoint pins')
        G.require(all(word[u] != word[v] for u, v in edges), 'unit-edge witness violation')
        for k, t in enumerate(selected):
            G.require((len({word[v] for v in t}) == 1) == (k == omitted), 'triangle witness violation')
    return selected


def verify(proof):
    points, triangles, pins = G.half_layer()
    edges = G.edges(points)
    rows, tri2, pins2, edges2 = audit.half_layer()
    G.require(points == list(map(G.A.point, rows)) and triangles == tri2 and pins == pins2 and edges == edges2,
              'independent half reconstruction differs')
    cert = G.read(G.ROOT / 'certificate.json')
    selected = witnesses(cert, len(points), edges, triangles, pins)
    clauses = G.cnf(len(points), edges, selected, pins)
    proof_stats = lrat.verify(clauses, 4*len(points), proof)
    half, frames = G.completed_half(points, selected)
    direct_half = audit.completed_half(rows, selected)
    G.require(half == list(map(G.A.point, direct_half)), 'independent completed union differs')
    gadget = audit.forcer()
    gadget_edges = [(i, j) for i, j in combinations(range(375), 2)
                    if audit.distance(gadget[i], gadget[j]) == (1296, 0)]
    tcert = G.read(G.T375 / 'certificate.json')
    word = tcert['unpinned_colouring']
    G.require(len(gadget_edges) == 1661 and len(word) == 375 and set(word) <= set('0123') and
              all(word[i] != word[j] for i, j in gadget_edges), 'terminal gadget witness')
    answer, forcing_stats = G.load('colour_check').solve(375, gadget_edges, [(0, 0), (1, 0), (2, 0)])
    G.require(answer is None, 'T375 terminal implication fails')
    zero = G.A.ZERO, G.A.ZERO
    G.require(points[pins[0]] == zero and G.A.norm(points[pins[1]]) == G.A.scalar(9216), 'outer anchors')
    rotation = G.A.ROT_SPINDLE
    G.require(G.A.norm(rotation) == G.A.ONE and
              G.A.distance(points[pins[1]], G.A.cmul(rotation, points[pins[1]])) == G.A.scalar(1296),
              'spindle edge')
    rotated = {G.A.cmul(rotation, p) for p in half}
    G.require(set(half) & rotated == {zero}, 'spindle overlap')
    full = set(half) | rotated
    result = {
        'verified': True, 'half_layer_vertices': len(points), 'half_layer_unit_edges': len(edges),
        'available_half_triangles': len(triangles), 'selected_half_triangles': len(selected),
        'inclusion_minimal_selected_support': True, 'deletion_colourings_checked': len(selected),
        'global_minimum_triangle_count_claimed': False,
        'half_unit_pair_checks_in_independent_audit': len(points)*(len(points)-1)//2,
        'cnf_variables': 4*len(points), 'cnf_clauses': len(clauses),
        'cnf_sha256': hashlib.sha256(G.dimacs(len(points), clauses).encode()).hexdigest(),
        'positive_hint_lrat': proof_stats, 'T375_forcing_replay': forcing_stats,
        'half_physical_vertices': len(half), 'full_physical_vertices': len(full),
        'half_physical_point_sha256': G.digest(half), 'full_physical_point_sha256': G.digest(full),
        'full_triangle_attachments': 2*len(frames), 'full_union_non_four_colourable': True,
        'exact_chromatic_number_computed': False, 'record_improvement': False,
    }
    G.require((len(points), len(edges), len(triangles), len(half), len(full)) == (1167, 6472, 321, 4293, 8585),
              'wrong construction inventory')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lrat', required=True, help='independently checked positive-hint LRAT proof')
    args = parser.parse_args()
    result = verify(args.lrat)
    expected = G.ROOT / 'expected.json'
    if expected.exists():
        G.require(result == G.read(expected), 'expected-result mismatch')
    print(json.dumps(result, sort_keys=True, indent=2))
