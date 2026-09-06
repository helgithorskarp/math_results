"""Literal graph verification; no producer, encoder or solver imports."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path


def need(ok, text):
    if not ok:
        raise ValueError(text)


def audit(g, density):
    need(type(g) is dict and set(g) == {'n', 'red_edges'}, 'schema')
    need(type(g['n']) is int and g['n'] == 20, 'order')
    es = g['red_edges']
    need(type(es) is list, 'edge list')
    for e in es:
        need(type(e) is list and len(e) == 2 and all(type(v) is int for v in e), 'edge schema')
        need(0 <= e[0] < e[1] < 20, 'edge range/order')
    red = {tuple(e) for e in es}
    need(es == [list(e) for e in sorted(red)], 'canonical unique edges')
    need(density in (92, 93) and len(red) == density, 'density')
    mask = sum(1 << i for i, e in enumerate(it.combinations(range(2, 10), 2)) if e not in red)
    need(mask == 5388912, 'W core')
    N = [{w for w in range(20) if w != v and tuple(sorted((v, w))) in red} for v in range(20)]
    need(N[0] == {10, 11, 12, 13, 18, 19}, 'first marked neighborhood')
    need(N[1] == {14, 15, 16, 17, 18, 19}, 'second marked neighborhood')

    def cliques(n, edges, size, color):
        return [sum(1 << v for v in q) for q in it.combinations(range(n), size)
                if all((e in edges) == color for e in it.combinations(q, 2))]

    need(not cliques(20, red, 4, True), 'red K4')
    need(not cliques(20, red, 5, False), 'blue K5')
    cone = red | {(v, 20) for v in range(20)}
    need(not cliques(21, cone, 5, True), 'red cone K5')
    need(not cliques(21, cone, 5, False), 'blue cone K5')
    # Extension to profile20^3 21^40, with all remaining22 vertices blue to
    # the central root20. These are required margins, not an existence claim.
    degree = [len(n) for n in N]
    cross = [(20 if v < 2 else 21) - 1 - degree[v] for v in range(20)]
    need(cross[:2] == [13, 13] and all(0 <= x <= 22 for x in cross), 'cross margins')
    outside_red = (22 * 21 - sum(cross)) // 2
    need(2 * outside_red + sum(cross) == 22 * 21, 'outside parity')
    need(density + 20 + sum(cross) + outside_red == 450, 'total degree bridge')
    details = {'red_triangle_masks': sorted(cliques(20, red, 3, True)),
               'blue_K4_masks': sorted(cliques(20, red, 4, False))}
    return dict(n=20, red_edges=len(red), degrees=degree, marked_common_red=[18, 19],
                W_blue_mask=mask, red_K4=0, blue_K5=0, cone_red_K5=0, cone_blue_K5=0,
                cone_red_edges=len(cone), checked_H_four_sets=4845, checked_H_five_sets=15504,
                checked_cone_five_sets=20349,
                lift=dict(H_original_labels=[1,2,3,4,5,6,7,8,9,10,20,21,22,23,33,34,35,36,41,42],
                          required_red_cross_degrees=cross, required_red_cross_total=sum(cross),
                          outside_order=22, required_outside_red_edges=outside_red,
                          required_outside_blue_edges=231-outside_red,
                          outside_original_labels=list(range(11,20))+list(range(24,33))+list(range(37,41)),
                          outside_marked_patterns=[1]*9+[2]*9+[3]*4),
                red_triangles=len(details['red_triangle_masks']), blue_K4s=len(details['blue_K4_masks']),
                clique_detail_sha256=hashlib.sha256(json.dumps(details,sort_keys=True,separators=(',',':')).encode()).hexdigest()), details


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    reports = {}
    for density in (92,93):
        path = a.directory / f'H{density}.json'
        reports[density] = audit(json.loads(path.read_text()), density)[0]
        reports[density]['graph_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    with a.report.open('x') as f:
        json.dump(dict(status='LITERAL_GRAPHS_AND_NECESSARY_LIFT_MARGINS_CHECKED', cases=reports), f,indent=2,sort_keys=True)
        f.write('\n')
    print(json.dumps(reports), flush=True)


if __name__ == '__main__':
    main()
