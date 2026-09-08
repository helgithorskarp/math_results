#!/usr/bin/env python3
"""Solver-free physical check; no producer imports or catalog completeness."""
import copy
import hashlib
import json
from itertools import combinations
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def adjacency(n, text):
    need(type(n) is int and n in (24, 26), 'graph order')
    need(isinstance(text, str) and len(text) == (n*(n-1)//2+3)//4,
         'edge word length')
    need(all(c in '0123456789abcdef' for c in text), 'hex syntax')
    bits = format(int(text, 16), 'b')[::-1]
    need(len(bits) <= n*(n-1)//2, 'edge word padding')
    a = [[False]*n for _ in range(n)]
    for k, (u, v) in enumerate(combinations(range(n), 2)):
        a[u][v] = a[v][u] = k < len(bits) and bits[k] == '1'
    return a


def verify(witness):
    x = witness['r45_extension']
    need(x['n'] == 24 and x['fixed_core_vertices'] == list(range(17)), 'extension mark')
    a = adjacency(24, x['red_hex'])
    counts = []
    for size, color in ((4, True), (5, False)):
        count = 0
        for q in combinations(range(24), size):
            need(any(a[u][v] != color for u, v in combinations(q, 2)),
                 'extension forbidden subgraph')
            count += 1
        counts.append(count)
    core = (HERE/'r44_17.g6').read_text().strip()
    need(ord(core[0])-63 == 17, 'author core order')
    bit_stream = ''.join(format(ord(c)-63, '06b') for c in core[1:])
    at = 0
    for v in range(1, 17):
        for u in range(v):
            need(a[u][v] == (bit_stream[at] == '1'), 'induced author core mismatch')
            at += 1
    need(set(bit_stream[at:]) <= {'0'}, 'author padding')
    for q in combinations(range(17), 4):
        colors = [a[u][v] for u, v in combinations(q, 2)]
        need(any(colors) and not all(colors), 'core is not R44')
    permutation = witness['author_core_to_quadratic_residue_labels']
    need(sorted(permutation) == list(range(17)), 'Paley isomorphism permutation')
    residues = {i*i % 17 for i in range(1, 17)}
    for u, v in combinations(range(17), 2):
        need(a[u][v] == ((permutation[u]-permutation[v]) % 17 in residues),
             'Paley isomorphism edge mismatch')
    need({3*x % 17 for x in residues} == set(range(1, 17))-residues,
         'Paley complement transport')

    y = witness['physical_partial_graph']
    need(y['n'] == 26 and y['triangle_free_red_edge'] == [24, 25], 'partial graph mark')
    b = adjacency(26, y['red_hex'])
    need(all(b[u][v] != a[u][v] for u, v in combinations(range(24), 2)), 'complement lift')
    need(all(not b[u][24] and b[u][25] == (u < 17) for u in range(24))
         and b[24][25], 'two-vertex lift contacts')
    need(y['new_vertex_v'] == 24 and y['new_vertex_u'] == 25 and
         y['edges_for_u'] == [v for v in range(26) if b[25][v]], 'lift labels')
    five_sets = 0
    for q in combinations(range(26), 5):
        colors = [b[u][v] for u, v in combinations(q, 2)]
        need(any(colors) and not all(colors), 'partial graph monochromatic five')
        five_sets += 1
    need(not any(b[24][v] and b[25][v] for v in range(26)), 'marked edge has a triangle')
    need(witness['global43_branch_decided'] is False and witness['good43_found'] is False,
         'invalid global scope')
    return {'extension_four_sets_checked': counts[0], 'extension_five_sets_checked': counts[1],
            'partial_graph_five_sets_checked': five_sets,
            'partial_marked_vertex_degrees': [sum(b[24]), sum(b[25])],
            'extension_red_edges': sum(a[u][v] for u, v in combinations(range(24), 2)),
            'partial_graph_red_edges': sum(b[u][v] for u, v in combinations(range(26), 2))}


def main():
    witness = json.loads((HERE/'WITNESS.json').read_text())
    result = verify(witness)
    # Compare a separately transcribed literal formula to the producer,
    # and evaluate every clause against the physical witness.
    a = adjacency(24, witness['r45_extension']['red_hex'])
    unknown = [(u, v) for u in range(24) for v in range(u+1, 24) if v >= 17]
    variable = {e: i+1 for i, e in enumerate(unknown)}
    clauses = []
    for order, sign in ((4, -1), (5, 1)):
        for vertices in combinations(range(24), order):
            fixed_colors = [a[u][v] for u, v in combinations(vertices, 2) if v < 17]
            if sign == -1 and False in fixed_colors:
                continue
            if sign == 1 and True in fixed_colors:
                continue
            clause = [sign*variable[u, v] for u, v in combinations(vertices, 2) if v >= 17]
            need(any((a[unknown[abs(lit)-1][0]][unknown[abs(lit)-1][1]]) == (lit > 0)
                     for lit in clause), 'literal model does not satisfy clause')
            clauses.append(clause)
    independent_text = f'p cnf {len(unknown)} {len(clauses)}\n'
    independent_text += ''.join(' '.join(str(x) for x in c)+' 0\n' for c in clauses)
    output = subprocess.run([sys.executable, '-B', str(HERE/'formula.py')],
                            check=True, capture_output=True)
    need(not output.stderr and output.stdout == independent_text.encode(), 'formula differs')
    history = json.loads((HERE/'RESULT.json').read_text())
    need(history['status'] == 'SAT' and history['calls'] == 1 and
         history['global_gate'] == 'FAILED_GATE_EXACT_NECESSARY_EXTENSION_SURVIVES', 'decision scope')
    need(hashlib.sha256(output.stdout).hexdigest() == history['cnf_sha256'], 'formula hash')
    need(len(unknown) == history['variables'] and len(clauses) == history['clauses'], 'formula sizes')
    mutations = []
    x = copy.deepcopy(witness); x['r45_extension']['red_hex'] = '0'*69; mutations.append(x)
    x = copy.deepcopy(witness); x['author_core_to_quadratic_residue_labels'][0] = 1; mutations.append(x)
    x = copy.deepcopy(witness); x['physical_partial_graph']['red_hex'] = '0'*82; mutations.append(x)
    x = copy.deepcopy(witness); x['good43_found'] = True; mutations.append(x)
    for x in mutations:
        try:
            verify(x)
        except ValueError:
            continue
        raise ValueError('invalid witness accepted')
    result.update(status='VERIFIED_FAILED_TRIANGLE_SUPPORT_GATE',
                  formula_variables=len(unknown), formula_clauses=len(clauses),
                  formula_sha256=hashlib.sha256(output.stdout).hexdigest(),
                  rejected_mutations=len(mutations), solver_calls_in_check=0,
                  global43_branch_decided=False, good43_found=False,
                  catalog_completeness_needed_for_witness=False)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
