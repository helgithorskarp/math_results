"""Literal small-graph and invalid-fixture controls for the used interfaces."""
from copy import deepcopy
from itertools import combinations
import json
from common import ROOT, classical_design, find_clique, clique_census, require
from fixtures import check_fixture


def graph_control(n, seed, complete=False):
    adjacency = [0] * n
    for i, j in combinations(range(n), 2):
        if complete or (i * 17 + j * 31 + seed * 13 + i * j * 7) % 11 < seed % 12:
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    actual = {str(k): sum(all(adjacency[i] >> j & 1 for i, j in combinations(c, 2))
                          for c in combinations(range(n), k)) for k in range(1, 8)}
    witness, search = find_clique(adjacency, 7)
    require(search['complete'] and (witness is not None) == (actual['7'] > 0),
            'seven-clique finder disagrees with literal subsets')
    if witness is not None:
        require(len(witness) == 7 and len(set(witness)) == 7
                and all(adjacency[i] >> j & 1 for i, j in combinations(witness, 2)),
                'finder returned an invalid witness')
        try:
            clique_census(adjacency, 7)
        except ValueError as error:
            require(str(error) == 'purported forbidden clique exists', 'unexpected positive-graph error')
        else:
            raise ValueError('positive seven-clique was accepted by exclusion census')
    else:
        require(clique_census(adjacency, 7)['cliques_by_size'] == actual,
                'increasing census disagrees with literal subset counts')
    return bool(actual['7'])


def main():
    positive = sum(graph_control(seed % 10, seed) for seed in range(70))
    positive += sum(graph_control(n, 0, complete=True) for n in [6, 7, 8, 9])
    circles, _ = classical_design()
    fixtures = json.loads((ROOT / 'fixtures.json').read_text())
    for fixture in fixtures:
        check_fixture(circles, fixture)
    invalid = []
    for kind in ['duplicate', 'weight', 'counts', 'gaps', 'out_of_universe']:
        bad = deepcopy(fixtures[2])
        if kind == 'duplicate':
            bad['words'][1] = bad['words'][0]
        elif kind == 'weight':
            bad['words'][0] = 1
        elif kind == 'counts':
            bad['counts']['g'] = 6
        elif kind == 'gaps':
            bad['gaps'] = bad['gaps'][1:]
        else:
            bad['words'][0] = 1 << 18
        try:
            check_fixture(circles, bad)
        except ValueError:
            invalid.append(kind)
        else:
            raise ValueError('corrupt fixture accepted: ' + kind)
    print(json.dumps({'agent': 'six-code-2', 'role': 'researcher', 'complete': True,
                      'literal_graph_controls': 74, 'positive_K7_controls': positive,
                      'valid_fixture_controls': 3, 'corrupt_fixtures_rejected': invalid}), flush=True)


if __name__ == '__main__':
    main()
