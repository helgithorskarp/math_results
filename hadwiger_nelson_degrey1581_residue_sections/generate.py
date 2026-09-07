#!/usr/bin/env python3
"""Optional exact generator and positive SAT-witness discovery."""
import argparse
import json
import time
from pathlib import Path
from pysat.solvers import Solver
import geometry as geo


def colour(vertices, edges):
    mapping = {v: i for i, v in enumerate(vertices)}
    ee = [(mapping[u], mapping[v]) for u, v in edges if u in mapping and v in mapping]
    clauses = [[4*v+c+1 for c in range(4)] for v in range(len(vertices))]
    for u, v in ee:
        clauses.extend([[-4*u-c-1, -4*v-c-1] for c in range(4)])
    clauses.append([1])  # Global palette symmetry only.
    with Solver(name='cadical195', bootstrap_with=clauses) as solver:
        solver.conf_budget(200000)
        result = solver.solve_limited()
        stats = solver.accum_stats()
        geo.require(result is True, 'unresolved or non-four-colourable support; certify separately')
        model = set(solver.get_model())
        word = ''.join(str(next(c for c in range(4) if 4*v+c+1 in model)) for v in range(len(vertices)))
    geo.require(all(word[u] != word[v] for u, v in ee), 'invalid decoded word')
    return word, dict(vertices=len(vertices), edges=len(ee), stats=stats)


def generate(out):
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    points, half = geo.construction()
    edges, survivors = geo.exact_edges(points)
    columns, gcds, values = geo.residues(points)
    family, counts = geo.section_family(values)
    labels = {p: i for i, p in enumerate(points)}
    word, half_stats = colour(half, edges)
    base = ['-']*len(points)
    for v, c in zip(half, word):
        for w in (v, labels[geo.outside_image(points[v])]):
            geo.require(base[w] == '-' or base[w] == c, 'shared-vertex disagreement')
            base[w] = c
    endpoint = (2*geo.SCALE,) + (0,)*31
    deleted = labels[endpoint]
    base[deleted] = '-'
    base = ''.join(base)
    geo.require(base.count('-') == 1 and not any(values[deleted]), 'base support or residue')
    geo.require(all(base[u] == '-' or base[v] == '-' or base[u] != base[v] for u, v in edges), 'base edge')
    certificate = dict(version='degrey-residue-hyperplanes-v1', target=508,
                       deleted=deleted, base_word=base, exceptions=[])
    exception_masks = [m for m, equations in family.items() if equations[0][1] == 0]
    exception_masks.sort(key=lambda m: (-m.bit_count(), m))
    queries = []
    for mask in exception_masks:
        normal, b = family[mask][0]
        geo.require(b == 0, 'exception level')
        vertices = [v for v in range(len(points)) if mask >> v & 1]
        word, stats = colour(vertices, edges)
        certificate['exceptions'].append(dict(normal=''.join(map(str, normal)), word=word))
        queries.append(stats)
    (out/'certificate.json').write_text(json.dumps(certificate, separators=(',', ':'))+'\n')
    report = dict(seconds=time.monotonic()-start, vertices=len(points), edges=len(edges),
                  constant_coefficient_survivors=survivors, columns=columns, gcds=gcds,
                  admissible_by_level=counts, distinct_supports=len(family),
                  half_query=half_stats, exception_queries=queries)
    (out/'search.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'exception_queries'}, sort_keys=True))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    generate(ap.parse_args().out)
