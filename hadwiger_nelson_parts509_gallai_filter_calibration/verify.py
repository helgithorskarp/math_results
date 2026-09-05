#!/usr/bin/env python3
"""Exact calibration of low-degree Gallai filtering on fixed public supports."""
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from motifs import adjacency, opposite_pairs, closed_walks, components, forest_union

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
BASE = 'hadwiger_nelson_parts509_pool_cover_residual30'
SHRINK = 'hadwiger_nelson_parts509_pool_cover_shrink01'


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def read_json(name):
    return json.loads((REPO / name).read_text())


def positive_cnf(name, U):
    lines = (REPO / name).read_text().splitlines()
    header = lines[0].split()
    require(header[:3] == ['p', 'cnf', '303'], 'positive CNF header')
    clauses = []
    for line in lines[1:]:
        row = list(map(int, line.split()))
        require(row and row[-1] == 0 and all(1 <= v <= 303 for v in row[:-1]), 'positive CNF row')
        require(row[:-1] == sorted(set(row[:-1])) and len(row) > 1, 'positive clause order')
        clauses.append(tuple(U[v-1] for v in row[:-1]))
    require(len(clauses) == int(header[3]), 'positive clause count')
    return clauses


def compute():
    manifest = json.loads((HERE/'manifest.json').read_text())
    for name, digest in manifest['inputs'].items():
        require(sha256((REPO/name).read_bytes()).hexdigest() == digest, f'input hash {name}')
    path = REPO/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py'
    spec = importlib.util.spec_from_file_location('reviewed_exact_geometry', path)
    geom = importlib.util.module_from_spec(spec); spec.loader.exec_module(geom)
    den, points, vertices, U, edges = geom.read_geometry()
    L, S, Q = set(range(374)), set(range(374,509)), set(U[135:])
    adj = adjacency(vertices, edges)
    first = read_json(f'{BASE}/certificate.json')
    refinements = read_json(f'{BASE}/refinements.json')
    last = read_json(f'{SHRINK}/postshrink_residual.json')
    rows = [first] + refinements + [last]
    require(len(rows) == 18, 'frozen historical support count')
    table = read_json('hadwiger_nelson_parts509_interface_lemma/interface_L.json')
    initial = read_json('hadwiger_nelson_parts509_pool_shape_closure/killing_sets.json')
    sonly = read_json('hadwiger_nelson_parts509_s_replacement_budget/certificate.json')
    require(initial['U'] == list(U) == sonly['pool'], 'base cover universe')
    families = [[tuple(row['D']) for row in initial['sets']],
                [tuple(row['D']) for row in sonly['killing_sets']]]
    families += [positive_cnf(f'hadwiger_nelson_parts509_pool_shape{a}_verified/killing_clauses.cnf', U)
                 for a in (6,7)]
    cover = sorted(set(row for family in families for row in family))
    require(sum(map(len,families)) == 24788 and len(cover) == 17250, 'common base cover')
    require(all(row and tuple(sorted(set(row))) == row and set(row) <= set(U) for row in cover), 'base set format')
    h574_X = set(read_json('hadwiger_nelson_parts509_pool_obstruction574/certificate.json')['pool_labels'])
    records = []; supports = set(); all_edge_checks = 0
    for index, row in enumerate(rows):
        for key, allowed in [('R', S), ('A', Q)]:
            require(row[key] == sorted(set(row[key])) and set(row[key]) <= allowed, ('selection',index,key))
        X = (S-set(row['R'])) | set(row['A']); H = L | X
        require(len(X) == 134 and len(H) == 508, ('selection budget',index))
        supports.add(tuple(sorted(X)))
        left = table['classes'][row['p']]['witness_colouring_L'] if index == 0 else row['l']
        require(len(left) == 374 and set(left) <= set('0123'), ('L colouring format',index))
        require(len(row['c']) == 303 and set(row['c']) <= set('.0123'), ('pool colouring format',index))
        colours = dict(enumerate(left)); colours.update(dict(zip(U, row['c'], strict=True)))
        require(all(colours[v] in '0123' for v in H), ('retained vertex has no colour',index))
        selected_edges = [(a,b) for a,b in edges if a in H and b in H]
        require(all(colours[a] != colours[b] for a,b in selected_edges), ('improper colouring',index))
        all_edge_checks += len(selected_edges)
        degree = {v: len(adj[v]&H) for v in X}
        require(min(degree.values()) >= 4, ('degree guard fails',index))
        require(all(X & set(clause) for clause in cover), ('base cover misses selection',index))
        low = sorted(v for v in X if degree[v] == 4)
        low_edges = [(a,b) for a,b in edges if a in low and b in low]
        comps = components(low, low_edges)
        tree_test = all(c['tree'] for c in comps)
        require(tree_test == forest_union(low, low_edges), ('forest cross-check',index))
        require(tree_test, ('low-degree graph not a forest',index))
        require(max(map(lambda c: len(c['vertices']),comps),default=0) <= 3, ('larger component',index))
        require(X-h574_X, ('support lies entirely inside H574',index))
        records.append(dict(index=index, added_Q5=len(row['A']), removed_S=len(row['R']),
                            graph_vertices=len(H), graph_edges=len(selected_edges),
                            minimum_pool_degree=min(degree.values()), low_vertices=low,
                            low_edges=[list(e) for e in low_edges], low_components=comps,
                            low_forest=True, four_colouring_verified=True,
                            missed_common_base_clauses=0,
                            selected_points_outside_H574=len(X-h574_X)))
    require(len(supports) == 18, 'distinct supports')
    pool_edges = [(a,b) for a,b in edges if a in U and b in U]
    census = opposite_pairs(U, pool_edges)
    audit = closed_walks(U, pool_edges)
    require(census == audit, 'motif census disagreement')
    counts = dict(Counter(kind for kind,block in census))
    require(counts == {'C4':2174,'diamond':798}, 'motif counts')
    stream = ''.join(kind+':'+','.join(map(str,block))+'\n' for kind,block in census).encode()
    return dict(status='GALLAI FILTER REJECTS NONE OF THE 18 CERTIFIED HISTORICAL RESIDUALS',
                universe_vertices=len(vertices), universe_edges=len(edges), denominator=den,
                common_base_distinct_clauses=len(cover), support_count=18,
                four_colourable_supports=18, low_forest_supports=18, rejected_supports=0,
                support_edge_checks=all_edge_checks,
                total_low_vertices=sum(len(row['low_vertices']) for row in records),
                total_low_edges=sum(len(row['low_edges']) for row in records),
                low_component_size_histogram=dict(sorted(Counter(
                    str(len(c['vertices'])) for row in records for c in row['low_components']).items())),
                maximum_low_component_vertices=3,
                pool_motifs=counts, motif_sha256=sha256(stream).hexdigest(),
                motif_enumerators_agree=True, records=records,
                whole_pool_closed=False, redundancy_on_whole_family_proved=False,
                latest_cover_residuals_claimed=False, native_solver_calls=0)


def main():
    result = compute()
    require(result == json.loads((HERE/'expected.json').read_text()), 'expected facts differ')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
