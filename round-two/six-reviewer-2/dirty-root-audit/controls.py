"""Independent exhaustive small controls, fixture checks and damaged evidence."""
import argparse
from collections import defaultdict
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import audit


def relabel(G, permutation):
    H = [0]*len(G)
    for i, row in enumerate(G):
        H[permutation[i]] = sum(1 << permutation[j] for j in range(len(G)) if row & (1 << j))
    return tuple(H)


def run():
    small = []
    for n in (3, 4, 5, 6):
        generated, stats = audit.generate(n)
        bins = defaultdict(list)
        for g in generated:
            bins[audit.invariant(g)].append(g)
        accepted = 0
        for key in range(1 << (n*(n-1)//2)):
            g = audit.decode(key, n)
            if not audit.valid_graph(g):
                continue
            accepted += 1
            hits = [h for h in bins[audit.invariant(g)] if audit.isomorphism(g, h) is not None]
            audit.need(len(hits) == 1, 'whole labelled small-domain match')
        small.append({'n': n, 'all_labelled_graphs': 1 << (n*(n-1)//2), 'accepted_girth_five_subcubic': accepted,
                      'generated_classes': stats['classes']})

    marginal_checks = 0
    for rows in range(1, 5):
        for width in range(5):
            exact = {}
            for x in product(range(width+1), repeat=rows):
                cost = sum(t*(t-1)//2 for t in x)
                exact[sum(x)] = min(exact.get(sum(x), cost), cost)
            for total, minimum in exact.items():
                audit.need(audit.packing_bound(total, rows, width) == minimum, 'marginal-cost calibration')
                marginal_checks += 1

    models = json.loads((audit.ROOT/'MODEL.json').read_text())
    unmarked, _ = audit.generate()
    marked, _ = audit.marked_extensions(unmarked)
    base = next(i for i, r in enumerate(models) if r['packing_rejection'] is not None)
    rejected = []

    def reject(label, fn):
        try:
            fn()
        except ValueError as exc:
            rejected.append({'label': label, 'reason': str(exc)})
        else:
            raise ValueError('invalid evidence accepted: '+label)

    reject('missing marked class', lambda: audit.table_audit(models[:-1], marked))
    bad = deepcopy(models);bad[1] = deepcopy(bad[0])
    reject('duplicated marked class', lambda b=bad: audit.table_audit(b, marked))
    for label, field in [('bad graph key', 'key'), ('bad edge count', 'edges'), ('bad marked degree', 'marked_degree')]:
        bad = deepcopy(models)
        bad[base][field] = (1 << 45) if field == 'key' else bad[base][field]+1
        reject(label, lambda b=bad: audit.table_audit(b, marked))
    bad = deepcopy(models);bad[base]['local_degrees'][0] += 1
    reject('bad literal degree row', lambda b=bad: audit.table_audit(b, marked))
    for field in ('lower', 'upper', 'column_incidences'):
        bad = deepcopy(models);bad[base]['packing_rejection'][field] += 1
        reject('bad cut '+field, lambda b=bad: audit.table_audit(b, marked))
    bad = deepcopy(models);bad[base]['packing_rejection']['subset'] = [0, 0]
    reject('repeated subset vertex', lambda b=bad: audit.table_audit(b, marked))
    bad = deepcopy(models);bad[base]['packing_rejection'] = None
    reject('erased genuine contradiction', lambda b=bad: audit.table_audit(b, marked))

    maps = pair_comparisons = 0
    for record in models:
        G = audit.decode(record['key'], 10)
        sizes, bounds = audit.column_capacities(G)
        for p in ((0, 9, 8, 7, 6, 5, 4, 3, 2, 1), (0, 2, 3, 4, 5, 6, 7, 8, 9, 1)):
            H = relabel(G, p)
            audit.need(audit.isomorphism(G, H, True) is not None, 'transported marked map')
            other_sizes, other_bounds = audit.column_capacities(H)
            audit.need(all(sizes[i] == other_sizes[p[i]] for i in range(10)), 'transported column sizes')
            for (i, j), value in bounds.items():
                audit.need(other_bounds[tuple(sorted((p[i], p[j])))] == value, 'transported literal pair bound')
                pair_comparisons += 1
            maps += 1
    P = tuple(sum(1 << j for j, B in enumerate(combinations(range(5), 2)) if not set(A) & set(B)) for A in combinations(range(5), 2))
    petersen = next(audit.decode(r['key'], 10) for r in models if r['edges'] == 15 and r['packing_rejection'] is None)
    audit.need(audit.isomorphism(P, petersen, True) is not None, 'literal Kneser Petersen positive')
    path = (2, 5, 2)
    audit.need(audit.isomorphism(path, relabel(path, (1, 0, 2)), True) is None, 'different marked path roles stay distinct')
    square = audit.decode(sum(1 << k for k, ij in enumerate(combinations(range(4), 2)) if ij in ((0, 1), (1, 2), (2, 3), (0, 3))), 4)
    audit.need(not audit.valid_graph(square), 'four-cycle rejected from unmarked domain')

    raw = (audit.ROOT/'PRIMARY21.txt').read_bytes()
    matrix, end = json.JSONDecoder().raw_decode(raw.decode())
    audit.need(len(matrix) == 21 and all(len(row) == 21 and set(row) <= {0, 1} for row in matrix), 'primary matrix dimensions')
    audit.need(raw.decode()[end:].strip().startswith('search_function_used ='), 'explicit primary search metadata tail')
    R = [sum(1 << j for j, v in enumerate(row) if j != i and v == 0) for i, row in enumerate(matrix)]
    audit.need(all(bool(R[i] & (1 << j)) == bool(R[j] & (1 << i)) for i, j in combinations(range(21), 2)), 'primary complement symmetric')
    B = [((1 << 21)-1) & ~(R[i] | (1 << i)) for i in range(21)]
    red = max((R[i] & R[j]).bit_count() for i, j in combinations(range(21), 2) if R[i] & (1 << j))
    blue = max((B[i] & B[j]).bit_count() for i, j in combinations(range(21), 2) if B[i] & (1 << j))
    audit.need((sum(degrees for degrees in map(int.bit_count, R))//2, red, blue) == (93, 3, 6), 'primary positive literal pages')
    encoded = ''.join(''.join(str(int(bool(row & (1 << j)))) for j in range(21))+'\n' for row in R).encode()
    audit.need(sha256(encoded).hexdigest() == '4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec', 'all441 author baseline entries match independently decoded primary')
    return {'small_complete_controls': small, 'marginal_minimum_controls': marginal_checks,
            'rejection_count': len(rejected), 'rejections': rejected,
            'transported_marked_maps': maps, 'transported_pair_bounds': pair_comparisons,
            'petersen_positive': True, 'marked_role_negative': True, 'square_domain_negative': True,
            'primary21': {'raw_sha256': sha256(raw).hexdigest(), 'red_edges': 93, 'red_pages': red, 'blue_pages': blue,
                          'all441_complement_entries_match': True}}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = run()
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'rejections': result['rejection_count'], 'small_controls': result['small_complete_controls']}))
