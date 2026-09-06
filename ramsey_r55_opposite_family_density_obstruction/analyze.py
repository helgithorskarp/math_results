"""Monotone base-core density certificate and exact sixteen-child relation."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINS = {
    'input': ('ramsey_r55_opposite22_realization/INPUT.json', 'ad40224bfefc36dbe387da389ca2c52c7ba95f823506ea4ba985bc8ed4d4902a'),
    'family': ('ramsey_r55_opposite22_realization/result.json', '0a2df58a3df138c6aec26cd73fb5b0bd104eb2fedb229827793c789c4c7e888e'),
    'H': ('ramsey_r55_root20_anchor_realization/GRAPH.json', '8d404855787227dc182d7bdc0e98751474ce6c9f1cf872abc52888477c096ccf'),
    'old_cases': ('ramsey_r55_marked_pair_decomposition/cases.json', 'c5dfb2f121e8b85fb4078f622257d4a6d924a3f81e055ded9f214d5ed9c89ef9'),
}
MODULES = {
    'source': ('ramsey_r55_opposite22_realization/generate.py', '32b77fde4785dcc4ef2fab548f9496768e2fedfe453066fae056d08ad8f8e263'),
    'capacity': ('ramsey_r55_marked_density_obstruction/analyze.py', '3b2b1eade96c5579714949834da5fad5a331d06e4fa8ffef420920bbf0904536'),
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def json_bytes(doc):
    return (json.dumps(doc, indent=2) + '\n').encode()


def pinned(path, digest):
    data = (HERE.parent / path).read_bytes()
    need(hashlib.sha256(data).hexdigest() == digest, 'input/module identity ' + path)
    return data


def dependencies():
    mods = {}
    for name, (path, digest) in MODULES.items():
        pinned(path, digest)
        spec = importlib.util.spec_from_file_location('family_' + name, HERE.parent / path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mods[name] = mod
    docs = {name: json.loads(pinned(*pin)) for name, pin in PINS.items()}
    return mods, docs


def addition_obstructions(adj, u, v):
    """All triangles/four-cliques newly completed by adding the nonedge uv."""
    need(type(u) is int and type(v) is int and 0 <= u < v < len(adj)
         and not (adj[u] >> v & 1), 'add a genuine nonedge')
    edge = (1 << u) | (1 << v)
    common = adj[u] & adj[v]
    vertices = [w for w in range(len(adj)) if common >> w & 1]
    triangles = [edge | (1 << w) for w in vertices]
    fours = [edge | (1 << w) | (1 << x) for w, x in itertools.combinations(vertices, 2)
             if adj[w] >> x & 1]
    return triangles, fours


def cut_text(n, red_edges):
    lits = [-i for i, edge in enumerate(itertools.combinations(range(n), 2), 1) if edge in red_edges]
    return f'p cnf {n*(n-1)//2} 1\n' + ' '.join(map(str, lits)) + ' 0\n'


def calculate():
    mods, docs = dependencies()
    source, cap = mods['source'], mods['capacity']
    n, source_red = source.decode(docs['input'])
    all_edges = set(itertools.combinations(range(n), 2))
    base_edges = all_edges - source_red
    graph = {'n': n, 'red_edges': [list(e) for e in sorted(base_edges)]}
    adj = cap.decode(graph)
    dp = cap.clique_dp(adj)
    domain = {12: [], 14: []}
    for mask, omega in enumerate(dp):
        if omega <= 3 and mask.bit_count() in domain:
            domain[mask.bit_count()].append(mask)
    h = cap.decode(docs['H'])
    need(h[1] == sum(1 << v for v in (0,16,17,18,19)), 'H marked neighborhood')
    constant = h[1].bit_count() + cap.edges_in(h, h[1])
    need(constant == 9, 'H neighborhood density base')
    cases, entries = [], []
    for s1 in domain[14]:
        tau, maxima = cap.triangle_free_maxima(dp, s1)
        e = cap.edges_in(adj, s1)
        local = [s0 for s0 in domain[12] if s0 | s1 == (1 << n) - 1 and dp[s0 & s1] <= 2]
        for s0 in local:
            cases.append({'id': len(cases), 'S0': f'{s0:06x}', 'S1': f'{s1:06x}',
                          'base_density_ceiling': constant + 4 + e + 4 * tau})
        entries.append({'S1': f'{s1:06x}', 'red_edges': e, 'triangle_free_maximum': tau,
                        'all_triangle_free_maximizers': [f'{m:06x}' for m in maxima],
                        'base_cover_markings': len(local)})
    need(len(cases) == 140 and max(c['base_density_ceiling'] for c in cases) == 90, 'base obstruction')
    family = []
    for pair in docs['family']['surviving_deletions']:
        u, v = pair
        edge = (1 << u) | (1 << v)
        child_edges = base_edges | {(u,v)}
        need(len(child_edges) == 124 and source.count(child_edges, n, 5, True) == 0
             and source.count(child_edges, n, 4, False) == 0, 'valid O child')
        triangles, fours = addition_obstructions(adj, u, v)
        accepted = []
        for case in cases:
            s0, s1 = int(case['S0'], 16), int(case['S1'], 16)
            if any((s0 & q == q) or (s1 & q == q) for q in fours):
                continue
            if any(s0 & s1 & q == q for q in triangles):
                continue
            accepted.append(case)
        bitmask = sum(1 << c['id'] for c in accepted)
        ceilings = [c['base_density_ceiling'] + int(int(c['S1'],16) & edge == edge) for c in accepted]
        need(accepted and max(ceilings) < 92, 'child density obstruction')
        if pair == [0,10]:
            old_cases = [{'id': i, 'S0': c['S0'], 'S1': c['S1']} for i,c in enumerate(accepted)]
            need(old_cases == docs['old_cases'], 'old exact 100-case regression')
        child_graph = {'n': n, 'red_edges': [list(e) for e in sorted(child_edges)]}
        family.append({'added_red_edge': pair,
                       'graph_sha256': hashlib.sha256(json_bytes(child_graph)).hexdigest(),
                       'size14_domain': [f'{s:06x}' for s in domain[14] if not any(s&q == q for q in fours)],
                       'valid_base_case_bits_hex': f'{bitmask:035x}',
                       'valid_markings': len(accepted), 'density_ceiling': max(ceilings)})
    cnf = cut_text(n, base_edges)
    certificate = {
        'scope': 'fixed H20, root red H blue O, marked outside degrees12/14 and union O, no red K5, density92 at b',
        'input_sha256': {name: pin[1] for name, pin in PINS.items()},
        'base_graph_sha256': hashlib.sha256(json_bytes(graph)).hexdigest(),
        'base_red_edges': len(base_edges), 'H_density_base': constant,
        'S1_entries': entries, 'base_cases': cases, 'base_uniform_density_ceiling': 90,
        'supergraph_density_ceiling': '90 + number of added red edges',
        'family': family, 'total_family_markings': sum(f['valid_markings'] for f in family),
        'all_16_families_excluded_at_density92': True,
        'old_already_closed_markings': 100, 'newly_closed_labeled_markings': sum(f['valid_markings'] for f in family)-100,
        'target_O_red_edges': 124, 'required_density_at_b': 92,
        'edge_toggle_lower_bound_from_base_at_124_red_edges': 3,
        'conditional_cut_variables': 231, 'conditional_cut_width': 123,
        'conditional_cut_sha256': hashlib.sha256(cnf.encode()).hexdigest(),
        'whole_degree_profile_excluded': False, 'target_graph_found': False,
    }
    return graph, certificate, cnf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(exist_ok=False)
    graph, certificate, cnf = calculate()
    (args.work/'BASE_GRAPH.json').write_bytes(json_bytes(graph))
    (args.work/'certificate.json').write_bytes(json_bytes(certificate))
    (args.work/'conditional_cut.cnf').write_text(cnf)
    print(json.dumps({'base_markings': len(certificate['base_cases']), 'family_markings': certificate['total_family_markings'],
                      'all_16_excluded': True, 'edge_toggle_lower_bound': 3}), flush=True)


if __name__ == '__main__':
    main()
