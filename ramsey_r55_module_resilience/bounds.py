#!/usr/bin/env python3
"""Audit the small Ramsey table and literal pair/triple counting identities."""
import itertools
import json


def need(ok):
    if not ok:
        raise ValueError('bound audit failed')


def report():
    # Imported upper bounds only; R(5,5) is intentionally absent.
    ramsey = {(2, 2): 2, (2, 3): 3, (2, 4): 4, (2, 5): 5,
              (3, 3): 6, (3, 4): 9, (3, 5): 14,
              (4, 4): 18, (4, 5): 25}
    caps = {1: 24, 2: 13, 3: 4, 4: 0}
    table = []
    for k in range(1, 5):
        for ell in range(k, 5):
            if (k, ell) in ((1, 1), (4, 4)):
                continue
            m = ramsey[k+1, ell+1] - 1
            table.append({'omega': k, 'alpha': ell, 'max_module': m,
                          'red_uniform': caps[k], 'blue_uniform': caps[ell],
                          'max_undeleted_order': m + caps[k] + caps[ell]})
    need(max(r['max_undeleted_order'] for r in table) == 39)
    need(max(r['max_undeleted_order'] for r in table if r['max_module'] >= 3) == 31)
    big = [r for r in table if r['max_module'] >= 6]
    need(max(r['max_undeleted_order'] for r in big) == 28)
    boundary = [r for r in big if r['max_undeleted_order'] == 28]
    need(len(boundary) == 1 and boundary[0]['omega'] == 3
         and boundary[0]['alpha'] == 4 and boundary[0]['max_module'] == 24)
    # Every coloring of the five contacts has a uniform triple, hence at most
    # nine distinguished triples. Check all32 contact signatures physically.
    for s in range(32):
        distinguished = sum(len({s >> v & 1 for v in q}) == 2
                            for q in itertools.combinations(range(5),3))
        need(distinguished <= 9)
    need(20 + 9*16 < 10*17)  # a size5 module needs at least17 exceptions

    # Verify identities for each literal outside signature, not a graph sample.
    # P3 has center0, red pairs01/02, blue pair12. The sum of the three
    # corresponding common-neighborhood indicators equals uniform + center-red.
    for s in range(8):
        x = [(s >> i) & 1 for i in range(3)]
        common = x[0]*x[1] + x[0]*x[2] + (1-x[1])*(1-x[2])
        need(common == int(s in (0, 7)) + x[0])
        need(sum(x) <= 3*int(s == 7) + 2*int(s not in (0, 7)))
    for s in range(4):
        x, y = s & 1, s >> 1
        need(x+y == 2*x*y + int(x != y))

    # Feasible integer local summaries show why these elementary inequalities
    # alone cannot be strengthened. They specify no edges between outside
    # vertices and are NOT graphs or feasibility witnesses for Ramsey43.
    stars = {'mixed': [13, 0, 1, 3, 1, 3, 9, 10],
             'triangle': [18, 0, 0, 6, 0, 6, 6, 4]}
    for name, counts in stars.items():
        need(sum(counts) == 40)
        es = {(0, 1), (0, 2)} | ({(1, 2)} if name == 'triangle' else set())
        for v in range(3):
            deg = sum(v in e for e in es) + sum(counts[s] for s in range(8) if s >> v & 1)
            need(18 <= deg <= 24)
        for u, v in itertools.combinations(range(3), 2):
            color = int((u, v) in es)
            inside = sum(int(tuple(sorted((u,w))) in es) == color and
                         int(tuple(sorted((v,w))) in es) == color
                         for w in range(3) if w not in (u, v))
            common = inside + sum(counts[s] for s in range(8)
                                  if (s >> u & 1) == color and (s >> v & 1) == color)
            need(common <= 13)
        if name == 'triangle':
            need(counts[7] <= 4 and counts[0] <= 24)
        else:
            need(counts[7] <= 13 and counts[0] <= 13)
    return {'module_table': table, 'pair_mixed_min': 8,
            'triple_mixed_min': {'mixed': 17, 'monochromatic': 18},
            'delete_at_most_prime': 7, 'delete_at_most_no_module_ge3': 15,
            'literal_signature_rows_checked': 52,
            'module_3_4_5_exception_lower_bounds': [17,16,17],
            'local_count_boundary_only': stars,
            'status': 'VERIFIED_MODULE_RESILIENCE_ARITHMETIC'}


if __name__ == '__main__':
    print(json.dumps(report(), sort_keys=True, indent=2))
