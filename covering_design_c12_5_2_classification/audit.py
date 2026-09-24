"""Independent block-column search and incidence-graph checks.

This program does not import the primary enumerator.  NetworkX is used only
for graph isomorphism, never for covering enumeration.
"""
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys
import networkx as nx
ROOT = Path(__file__).resolve().parent

def digest(rows):
    return sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest()

def enumerate_bundles(low):
    r = len(low)
    columns = [sum((1 << i for i, b in enumerate(low) if b >> p & 1)) for p in range(9)]
    margins = tuple((5 - c.bit_count() for c in columns))
    candidates = []
    for size in (4, 5):
        for pts in combinations(range(9), size):
            b = sum((1 << p for p in pts))
            if all((b & t for t in low)):
                candidates.append(b)
    sizes = {b: b.bit_count() for b in candidates}
    bits = {b: tuple((p for p in range(9) if b >> p & 1)) for b in candidates}
    answers = set()
    nodes = 0
    bundle_nodes = 0

    def solve(margins, n4, n5, domain, selected):
        nonlocal nodes, bundle_nodes
        nodes += 1
        left = n4 + n5
        if any((m < 0 or m > left for m in margins)):
            return
        if not left:
            if not any(margins):
                answers.add(tuple(sorted(selected)))
            return
        domain = tuple((b for b in domain if (n4 if sizes[b] == 4 else n5) > 0 and all((margins[p] > 0 for p in bits[b]))))
        if not domain:
            return
        for p, m in enumerate(margins):
            if m > sum((n for s, n in ((4, n4), (5, n5)) if any((sizes[b] == s and b >> p & 1 for b in domain)))):
                return
            if m < sum((n for s, n in ((4, n4), (5, n5)) if n and all((b >> p & 1 for b in domain if sizes[b] == s)))):
                return
        pivot = min((p for p, m in enumerate(margins) if m), key=lambda p: (sum((b >> p & 1 for b in domain)), -margins[p], p))
        incident = tuple((b for b in domain if b >> pivot & 1))
        outside = tuple((b for b in domain if not b >> pivot & 1))
        need = margins[pivot]

        def bundle(options, missing, rem, k4, k5, chosen):
            nonlocal bundle_nodes
            bundle_nodes += 1
            if not missing:
                future = tuple((b for b in outside if all((b & t for t in chosen))))
                solve(rem, k4, k5, future, selected + chosen)
                return
            if missing > k4 + k5 or not options:
                return
            for i, b in enumerate(options):
                size = sizes[b]
                if (k4 if size == 4 else k5) == 0 or any((rem[p] <= 0 for p in bits[b])):
                    continue
                new = list(rem)
                for p in bits[b]:
                    new[p] -= 1
                available = tuple((t for t in options[i:] if t & b and all((new[p] > 0 for p in bits[t]))))
                bundle(available, missing - 1, tuple(new), k4 - (size == 4), k5 - (size == 5), chosen + (b,))
        bundle(incident, need, margins, n4, n5, ())
    solve(margins, 9 - 2 * (r - 3), r - 3, tuple(candidates), ())
    return (sorted(answers), dict(nodes=nodes, bundle_nodes=bundle_nodes))

def graph(rows, mark=None):
    g = nx.Graph()
    for p, row in enumerate(rows):
        g.add_node(('p', p), kind='marked' if p == mark else 'point')
    for b in range(9):
        g.add_node(('b', b), kind='block')
    for p, row in enumerate(rows):
        for b in range(9):
            if row >> b & 1:
                g.add_edge(('p', p), ('b', b))
    return g

def isomorphic(a, b):
    return nx.is_isomorphic(a, b, node_match=lambda u, v: u['kind'] == v['kind'])

def invariant(rows):
    return (tuple(sorted((sum((b >> p & 1 for b in rows)) for p in range(9)))), tuple(sorted(((b & t).bit_count() for b, t in combinations(rows, 2)))))

def independent_low_census():
    triples = [sum((1 << p for p in t)) for t in combinations(range(9), 3)]
    states = [()]
    all_levels = []
    for r in range(1, 8):
        found = {}
        reps = []
        for rows in states:
            for t in triples:
                if t in rows:
                    continue
                new = tuple(sorted(rows + (t,)))
                if any((not b & s for b, s in combinations(new, 2))):
                    continue
                if any((sum(((b & s).bit_count() - 1 for j, s in enumerate(new) if i != j)) > 1 for i, b in enumerate(new))):
                    continue
                key = invariant(new)
                g = graph(new)
                if any((isomorphic(g, h) for h in found.get(key, []))):
                    continue
                found.setdefault(key, []).append(g)
                reps.append(new)
        states = reps
        all_levels.append(reps)
    return all_levels

def direct_check(design):
    """Check the published primal blocks without calling the primary checker."""
    if any((type(b) is not int or not 0 < b < 4096 for b in design['blocks'])):
        raise ValueError('malformed block')
    blocks = [set((p for p in range(12) if b >> p & 1)) for b in design['blocks']]
    if len(blocks) != 9 or any((len(b) != 5 for b in blocks)):
        raise ValueError('incorrect block count or size')
    if len({tuple(sorted(b)) for b in blocks}) != 9:
        raise ValueError('duplicate block')
    if any((not any((p in b and q in b for b in blocks)) for p, q in combinations(range(12), 2))):
        raise ValueError('uncovered pair')
    rows = [sum((1 << j for j, block in enumerate(blocks) if p in block)) for p in range(12)]
    if rows != design['point_signatures']:
        raise ValueError('primal and dual representatives disagree')
    return rows

def main():
    data = json.loads((ROOT / 'CATALOGUE.json').read_text())
    expected = json.loads((ROOT / 'EXPECTED.json').read_text())
    levels = independent_low_census()
    low_checks = 0
    for r in range(3, 8):
        fixed = [graph(c['low']) for c in data['cases'] if c['degree3_points'] == r]
        if len(fixed) != len(levels[r - 1]):
            raise ValueError('low-type count mismatch')
        for rows in levels[r - 1]:
            if sum((isomorphic(graph(rows), g) for g in fixed)) != 1:
                raise ValueError('independent low census disagrees')
            low_checks += 1
    completion_checks = []
    for case in data['cases']:
        answers, stats = enumerate_bundles(case['low'])
        if len(answers) != case['labelled'] or digest(answers) != case['labelled_sha256']:
            raise ValueError('complete labelled answer sets disagree')
        completion_checks.append(dict(degree3_points=case['degree3_points'], low_type=case['low_type'], labelled=len(answers), labelled_sha256=digest(answers), **stats))
    designs = data['designs']
    signatures = [direct_check(design) for design in designs]
    comparisons = 0
    for i, a in enumerate(signatures):
        for b in signatures[i + 1:]:
            if sorted((s.bit_count() for s in a)) != sorted((s.bit_count() for s in b)):
                continue
            if invariant(a) != invariant(b):
                continue
            comparisons += 1
            if isomorphic(graph(a), graph(b)):
                raise ValueError('duplicate isomorphism class')
    aut_total = 0
    for design, rows in zip(designs, signatures):
        g = graph(rows)
        matcher = nx.algorithms.isomorphism.GraphMatcher(g, g, node_match=lambda u, v: u['kind'] == v['kind'])
        order = 0
        images = [set() for _ in rows]
        for action in matcher.isomorphisms_iter():
            order += 1
            for p in range(12):
                images[p].add(action['p', p][1])
        if order != design['automorphism_order']:
            raise ValueError('independent automorphism order mismatch')
        orbits = sorted({tuple(sorted(orbit)) for orbit in images})
        if orbits != sorted(map(tuple, design['point_orbits'])):
            raise ValueError('independent point orbits mismatch')
        aut_total += order
    result = dict(status='INDEPENDENT_107_CLASS_AUDIT_PASSED', networkx_version=nx.__version__, low_levels=[len(s) for s in levels], low_types_matched=low_checks, classes=len(designs), pairwise_isomorphism_checks=comparisons, automorphisms_checked=aut_total, labelled_completions=sum((c['labelled'] for c in completion_checks)), column_search_nodes=sum((c['nodes'] for c in completion_checks)), bundle_nodes=sum((c['bundle_nodes'] for c in completion_checks)), catalogue_sha256=digest(data), completion_checks=completion_checks)
    if result['catalogue_sha256'] != expected['catalogue_sha256']:
        raise ValueError('catalogue digest mismatch')
    if sys.argv[1:] == ['--write-reference']:
        (ROOT / 'AUDIT_EXPECTED.json').write_text(json.dumps(result, indent=2) + '\n')
    elif sys.argv[1:]:
        raise SystemExit('usage: python3 audit.py [--write-reference]')
    else:
        baseline = json.loads((ROOT / 'AUDIT_EXPECTED.json').read_text())
        baseline['networkx_version'] = nx.__version__
        if result != baseline:
            raise ValueError('independent audit differs from AUDIT_EXPECTED.json')
    print(json.dumps(result, indent=2))
if __name__ == '__main__':
    main()
