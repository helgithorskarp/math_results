"""Graph partition and independently rebuilt finite-state formula checks."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph-work', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--native-dir', type=Path)
    args = parser.parse_args()
    started = time.perf_counter()
    expected = json.loads((HERE/'expected.json').read_text())
    assert expected == json.loads((args.work/'result.json').read_text())
    raw = (args.graph_work/'graph.json').read_bytes()
    assert sha256(raw).hexdigest() == expected['graph_sha256']
    g = json.loads(raw)
    edges = {tuple(e) for e in g['edges']}
    E = lambda u, v: tuple(sorted((u, v))) in edges
    N = {v for v in range(421) if E(210, v)}
    B = sorted(set(range(421))-N-{210})
    left, cycles = set(N), []
    while left:
        component = {min(left)}
        while True:
            expanded = component | {v for v in N if any(E(v, u) for u in component)}
            if expanded == component:
                break
            component = expanded
        assert len(component) == 6 and component <= left
        left -= component
        first = min(component)
        candidates = [(first,)+p for p in permutations(sorted(component-{first}))
                      if all(E(u, v) for u, v in zip((first,)+p, p+(first,)))]
        assert len(candidates) == 2
        cycle = min(candidates)
        assert sum(E(u, v) for u in component for v in component) == 12
        cycles.append(list(cycle))
    assert cycles == expected['cycles'] and len(cycles) == 14
    rows = []

    def extend(prefix):
        if len(prefix) == 6:
            if prefix[-1] != prefix[0]:
                rows.append(prefix)
            return
        for c in (1, 2, 3):
            if not prefix or prefix[-1] != c:
                extend(prefix+[c])
    extend([])
    assert len(rows) == 66
    residual = json.loads((HERE.parent/'hadwiger_nelson_heptagon_kempe/expected.json').read_text())
    triples = set(map(frozenset, residual['residual_triangles']))
    special = [i for i, cycle in enumerate(cycles)
               if frozenset(cycle[::2]) in triples or frozenset(cycle[1::2]) in triples]
    assert len(special) == 7
    assert {frozenset(cycles[i][parity::2]) for i in special for parity in [0, 1]} == triples
    # All outside vertices belong to one connected component.
    reachable = {B[0]}
    while True:
        extended = reachable | {v for v in B if any(E(u, v) for u in reachable)}
        if extended == reachable:
            break
        reachable = extended
    assert reachable == set(B)
    edges_B = [(u, v) for u, v in g['edges'] if u in B and v in B]
    cross = [(u, v) if u in N else (v, u) for u, v in g['edges']
             if (u in N and v in B) or (v in N and u in B)]
    assert len(edges_B) == 1260 and len(cross) == 420
    assert 1260+420+84+84 == len(edges)
    index = {v: i for i, v in enumerate(B)}
    bvar = lambda v, c: 4*index[v]+c+1
    fresh_instances = []
    for q in expected['queries']:
        clauses = [[bvar(v, c) for c in range(4)] for v in B]
        clauses.extend([-bvar(u, c), -bvar(v, c)] for u, v in edges_B for c in range(4))
        nextvar = 4*len(B)
        all_options = []
        for cycle in cycles:
            allowed = [row for row in rows if q['target'] is None or
                       not set(q['target']) <= set(cycle) or
                       row[cycle.index(q['target'][0])] == row[cycle.index(q['target'][1])]]
            options = []
            for row in allowed:
                nextvar += 1
                options.append((nextvar, row))
                for v, c in zip(cycle, row):
                    clauses.extend([-nextvar, -bvar(u, c)] for u in B if E(u, v))
            clauses.append([var for var, row in options])
            all_options.append(options)
        data = (f'p cnf {nextvar} {len(clauses)}\n'+
                ''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode()
        assert nextvar == q['variables'] and len(clauses) == q['clauses']
        assert data == (args.work/q['filename']).read_bytes()
        assert len(data) == q['bytes'] and sha256(data).hexdigest() == q['sha256']
        if args.native_dir is not None and q['target'] is not None:
            assert data == (args.native_dir/q['filename']).read_bytes()
        fresh_instances.append((clauses, all_options))
    # Check the base encoding with 42 potential and six nonpotential witnesses.
    host = g['host']; point_index = {tuple(p): i for i, p in enumerate(g['points'])}
    labels = [[point_index[tuple(x-y for x, y in zip(a, b))] for b in host] for a in host]
    pdir = HERE.parent/'hadwiger_nelson_heptagon_difference_lifts'
    potentials = json.loads((pdir/'potentials.json').read_text())
    colours = []
    for p in potentials:
        c = [0]*421
        for a in range(21):
            for b in range(21):
                c[labels[a][b]] = p[a]^p[b]
        colours.append(c)
    for witness in json.loads((HERE.parent/'hadwiger_nelson_heptagon_kempe/witnesses.json').read_text()):
        c = colours[witness['seed']].copy()
        a, b = witness['colours']
        for v in witness['component']:
            c[v] ^= a^b
        colours.append(c)
    base_clauses, base_options = fresh_instances[0]
    for c in colours:
        assert c[210] == 0 and all(c[u] != c[v] for u, v in edges)
        true = {bvar(v, c[v]) for v in B}
        for cycle, options in zip(cycles, base_options):
            choices = [var for var, row in options if row == [c[v] for v in cycle]]
            assert len(choices) == 1
            true.add(choices[0])
        assert all(any((literal in true) if literal > 0 else (-literal not in true)
                       for literal in clause) for clause in base_clauses)
    out = {'status': 'EXACT WHEEL INTERFACE VERIFIED; THREE ORDINARY QUERIES UNRESOLVED',
           'origin_neighbors': len(N), 'six_cycles': len(cycles),
           'residual_cycle_indices': special, 'outside_vertices': len(B),
           'outside_edges': len(edges_B), 'outside_components': 1,
           'cross_edges': len(cross),
           'outside_degree_into_N': dict(sorted(Counter(sum(E(v, u) for u in N) for v in B).items())),
           'states': len(rows),
           'alternating_triangle_distinct_colour_histogram':
               {str(k): v for k, v in sorted(Counter((len(set(row[::2])), len(set(row[1::2]))) for row in rows).items())},
           'full_cnfs_rebuilt_byte_identically': len(fresh_instances),
           'native_inputs_byte_compared': 3 if args.native_dir is not None else 0,
           'proper_graph_colourings_lifted_to_base_models': len(colours),
           'base_clauses_evaluated': len(colours)*len(base_clauses),
           'seconds': time.perf_counter()-started}
    (args.work/'audit.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
