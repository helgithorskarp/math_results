"""Direct semantic controls for the finite graph and certificate kernels."""
from itertools import combinations
from pathlib import Path
import copy
import json

from geometry import classical_design, points, require
from generate_three_gap import enumerate_fixed, find_clique, graph
from verify_three_gap import check_colors, no_four_clique, pair_graph, verify_witness


def rejects(call):
    try:
        call()
    except ValueError:
        return True
    return False


def direct_compatible(left, right):
    b, qs = left
    c, rs = right
    if len(set(points(b)) & set(points(c))) > 2:
        return False
    return all(q == r or len(set(points(q)) & set(points(r))) <= 1
               for q in qs for r in rs)


def main():
    pairs = list(combinations(range(5), 2))
    for bits in range(1 << len(pairs)):
        adjacency = [0] * 5
        for k, (i, j) in enumerate(pairs):
            if bits >> k & 1:
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i
        for target in (4, 5):
            direct = any(all(adjacency[i] >> j & 1 for i, j in combinations(vertices, 2))
                         for vertices in combinations(range(5), target))
            found, coverage = find_clique(adjacency, target)
            require(coverage['complete'] and (found is not None) == direct,
                    'clique recursion disagrees with direct small-universe enumeration')
            if found is not None:
                require(len(set(found)) == target
                        and all(adjacency[i] >> j & 1 for i, j in combinations(found, 2)),
                        'invalid small-graph clique witness')
            if target == 4:
                require(rejects(lambda: no_four_clique(adjacency)) == direct,
                        'triangle/fourth-neighbor kernel disagrees with direct enumeration')
    folder = Path(__file__).resolve().parent
    circles, _ = classical_design()
    records, census = enumerate_fixed(circles)
    adjacency, independent_hash = pair_graph(records)
    production, summary = graph(records)
    require(adjacency == production and independent_hash == summary['graph_sha256'],
            'entrywise graph disagreement')
    selected = set(range(24))
    for i, row in enumerate(adjacency):
        later = row & ~((1 << (i + 1)) - 1)
        if later:
            selected.update((i, (later & -later).bit_length() - 1))
        if len(selected) >= 48:
            break
    fixture = json.loads((folder / 'single_word_witness69.json').read_text())
    selected.update(fixture['indices'])
    comparisons = 0
    shared_positive = 0
    for i, j in combinations(sorted(selected), 2):
        expected = direct_compatible(records[i], records[j])
        require(bool(adjacency[i] >> j & 1) == expected, 'direct record-adjacency mismatch')
        comparisons += 1
        if expected and set(records[i][1]) & set(records[j][1]):
            shared_positive += 1
    require(shared_positive > 0, 'shared-replacement positive control absent')
    certificate = json.loads((folder / 'single_word_colors.json').read_text())
    sizes = check_colors(adjacency, certificate)
    missing = copy.deepcopy(certificate)
    missing['colors'][0].pop()
    require(rejects(lambda: check_colors(adjacency, missing)), 'missing vertex accepted')
    edge = next((i, (row & -row).bit_length() - 1)
                for i, row in enumerate(adjacency) if row)
    colliding = copy.deepcopy(certificate)
    for color in colliding['colors']:
        for i in edge:
            if i in color:
                color.remove(i)
    colliding['colors'][0].extend(edge)
    require(rejects(lambda: check_colors(adjacency, colliding)), 'monochromatic edge accepted')
    gaps = census['gaps']
    witness = verify_witness(circles, records, 15, gaps, fixture)
    duplicate = copy.deepcopy(fixture)
    duplicate['words'][0] = duplicate['words'][1]
    require(rejects(lambda: verify_witness(circles, records, 15, gaps, duplicate)),
            'duplicate witness word accepted')
    wrong_weight = copy.deepcopy(fixture)
    wrong_weight['words'][0] = 0
    require(rejects(lambda: verify_witness(circles, records, 15, gaps, wrong_weight)),
            'wrong-weight witness accepted')
    print(json.dumps({'small_graphs': 1024, 'clique_targets': [4, 5],
                      'literal_record_pair_checks': comparisons,
                      'shared_replacement_positive_pairs': shared_positive,
                      'color_sizes': sizes, 'corrupted_certificate_controls': 2,
                      'corrupted_word_controls': 2, 'witness': witness}, sort_keys=True))


if __name__ == '__main__':
    main()
