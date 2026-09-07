#!/usr/bin/env python3
"""Independent small-family checks and deliberate certificate/geometry faults."""
import copy
import json
from itertools import combinations, permutations, product
from pathlib import Path
import native
import verify as v

HERE = Path(__file__).resolve().parent

def cover_controls():
    graphs = cases = 0
    for n in range(6):
        pairs = list(combinations(range(n), 2))
        for bits in range(1 << len(pairs)):
            edges = [p for i, p in enumerate(pairs) if bits >> i & 1]
            independent = [not any(mask >> a & 1 and mask >> b & 1 for a, b in edges)
                           for mask in range(1 << n)]
            chi = [0] + [n+1]*((1 << n)-1)
            for mask in range(1, 1 << n):
                pivot = mask & -mask; sub = mask
                while sub:
                    if sub & pivot and independent[sub]:
                        chi[mask] = min(chi[mask], 1+chi[mask ^ sub])
                    sub = (sub-1) & mask
            full = (1 << n)-1
            for k in range(1, 5):
                mandatory = sum(1 << x for x in range(n) if chi[full ^ (1 << x)] <= k)
                for mask in range(1 << n):
                    if mandatory & mask != mandatory:
                        v.need(chi[mask] <= k, 'small positive-cover implication')
                    if mask.bit_count() < mandatory.bit_count():
                        v.need(chi[mask] <= k, 'small cardinality implication')
                    cases += 1
            graphs += 1
    return graphs, cases

def palette_controls():
    cases = 0
    for k in (3, 4):
        for x0, x1, y0, y1 in product(range(k), repeat=4):
            for anchor, left_tip, right_tip in product((False, True), repeat=3):
                feasible = any((not anchor or x0 == p[y0])
                               and (not (left_tip and right_tip) or x1 != p[y1])
                               for p in permutations(range(k)))
                expected = not (anchor and left_tip and right_tip and x0 == x1 and y0 == y1)
                v.need(feasible == expected, 'palette gluing truth table')
                cases += 1
    # With only two colours, both distinct-terminal patterns cannot be pasted.
    v.need(not any(p[0] == 0 and p[1] != 1 for p in permutations(range(2))), 'two-colour counterexample')
    return cases

def main():
    cert = json.loads((HERE/'certificate.json').read_text()); g = v.geometry()
    points, left = native.construction(); edges, survivors = native.exact_edges(points)
    v.need(points == g['points'] and edges == g['edges'] and left == g['left'], 'independent geometry disagreement')
    rejected = []
    def bad(name, mutate):
        c = copy.deepcopy(cert); mutate(c)
        try:
            v.full_cover(c, g)
        except (ValueError, TypeError, KeyError):
            rejected.append(name)
        else:
            raise ValueError('accepted fault: '+name)
    bad('version', lambda c: c.update(version='other'))
    bad('target', lambda c: c.update(target=509))
    bad('boolean target', lambda c: c.update(target=True))
    bad('boolean terminal', lambda c: c['terminals'].__setitem__(0, False))
    bad('short baseline', lambda c: c.update(baseline=c['baseline'][:-1]))
    bad('baseline omission', lambda c: c.update(baseline='-'+c['baseline'][1:]))
    bad('baseline colour', lambda c: c.update(baseline='4'+c['baseline'][1:]))
    bad('nonlist steps', lambda c: c.update(steps={}))
    bad('deleted label range', lambda c: c['steps'][0].update(deleted=791))
    bad('boolean deleted label', lambda c: c['steps'][0].update(deleted=False))
    bad('terminal deletion', lambda c: c['steps'][0].update(deleted=0))
    bad('short seed', lambda c: c['steps'][0].update(word=c['steps'][0]['word'][:-1]))
    bad('duplicate row', lambda c: c['steps'].insert(1, copy.deepcopy(c['steps'][0])))
    def equal(c):
        w = list(c['steps'][0]['word']); w[790] = w[0]; c['steps'][0]['word'] = ''.join(w)
    bad('equal seed terminals', equal)
    def mono(c):
        w = list(c['steps'][0]['word']); deleted = c['steps'][0]['deleted']
        a, b = next(e for e in g['half_edges'] if deleted not in e and not set(e) & {0, 790})
        w[b] = w[a]; c['steps'][0]['word'] = ''.join(w)
    bad('seed monochromatic edge', mono)
    bad('inversion wrong parent', lambda c: c['steps'][1].update(parent=790))
    bad('inversion wrong label', lambda c: c['steps'][1].update(deleted=300))
    patch = next(i for i, r in enumerate(cert['steps']) if r['kind'] == 'patch')
    bad('unknown kind', lambda c: c['steps'][patch].update(kind='kempe'))
    bad('missing parent', lambda c: c['steps'][patch].update(parent=790))
    bad('empty patch', lambda c: c['steps'][patch].update(changes=[]))
    bad('duplicate patch label', lambda c: c['steps'][patch]['changes'].append(c['steps'][patch]['changes'][0][:]))
    bad('patch colour', lambda c: c['steps'][patch]['changes'][0].__setitem__(1, '4'))
    bad('boolean patch label', lambda c: c['steps'][patch]['changes'][0].__setitem__(0, False))
    bad('missing target coverage', lambda c: c.update(steps=c['steps'][:-2]))
    # Mutate inputs to the structural audit, while preserving the actual geometry.
    original = v.ex.edge_census
    try:
        v.ex.edge_census = lambda p: ([e for e in g['edges'] if e != tuple(g['bridge'])], 0)
        try:
            v.geometry()
        except ValueError:
            rejected.append('missing cross edge')
        else:
            raise ValueError('accepted missing bridge')
        L, R = set(g['left']), set(g['right'])
        extra = tuple(sorted((min(L-R), min(R-L))))
        v.need(extra not in set(g['edges']), 'fault pair already an edge')
        v.ex.edge_census = lambda p: (sorted(g['edges']+[extra]), 0)
        try:
            v.geometry()
        except ValueError:
            rejected.append('additional cross edge')
        else:
            raise ValueError('accepted extra bridge')
    finally:
        v.ex.edge_census = original
    saved = v.ex.ROOTS[3]
    try:
        v.ex.ROOTS[3] += 1
        try:
            v.ex.edge_census([])
        except ValueError:
            rejected.append('invalid modular root')
        else:
            raise ValueError('accepted invalid root')
    finally:
        v.ex.ROOTS[3] = saved
    graphs, cases = cover_controls()
    report = dict(all_checks_passed=True, exact_geometries_equal=True,
                  full_pair_checks=len(points)*(len(points)-1)//2,
                  producer_constant_filter_survivors=survivors,
                  small_graphs=graphs, small_graph_palette_subset_cases=cases,
                  palette_presence_cases=palette_controls(), two_colour_counterexample=True,
                  malformed_inputs_rejected=len(rejected), rejections=rejected)
    print(json.dumps(report, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
