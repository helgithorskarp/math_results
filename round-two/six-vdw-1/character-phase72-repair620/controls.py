"""Actual hypergraph damages and different-algorithm tiny cover controls."""
import argparse
import copy
import itertools
import json
from pathlib import Path

from check_cover import classify
from check_hypergraph import check


def need(ok, message):
    if not ok:
        raise ValueError(message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--part', choices=['tiny', 'physical'], required=True)
    args = parser.parse_args()
    graph = json.loads(args.certificate.read_text())
    if args.part == 'tiny':
        fixtures = [(3, []), (3, [(1,)]), (4, [(2,), (3,)]),
                    (6, [(i, i % 6 + 1) for i in range(1, 7)]),
                    (8, list(itertools.combinations(range(1, 9), 4)))]
        cases = candidates = 0
        for n, edges in fixtures:
            for size in range(1, n + 1):
                positive = negative = 0
                for rest in itertools.combinations(range(2, n + 1), size - 1):
                    selected = {1, *rest}
                    if all(selected & set(edge) for edge in edges):
                        positive += 1
                    else:
                        negative += 1
                result = classify(n, edges, size)
                need(result['positive_volume'] == positive and result['negative_volume'] == negative,
                     'whole small flat subsets vs independently weighted tree')
                cases += 1
                candidates += positive + negative
        # Direct small mathematical controls, including the complete-four-set boundary.
        need(classify(8, fixtures[-1][1], 4)['positive_volume'] == 0,
             'every four-set cover would leave a four-edge')
        need(classify(8, fixtures[-1][1], 5)['positive_volume'] == 35,
             'every five-set cover leaves at most three vertices')
        print(json.dumps({'author': 'six-vdw-1', 'role': 'researcher',
                          'status': 'WHOLE_TINY_COVER_PARTITIONS_MATCH', 'cases': cases,
                          'all_flat_candidates': candidates, 'explicit_boundary_controls': 2,
                          'scope': 'Tiny assignment controls only, not F31 minimum cover.'}, sort_keys=True))
    else:
        damages = []
        wrong = copy.deepcopy(graph); wrong['character_word'][1] ^= 1; damages.append(('character', wrong))
        wrong = copy.deepcopy(graph); wrong['phase_word'][11] ^= 1; damages.append(('phase', wrong))
        wrong = copy.deepcopy(graph); wrong['edges'].pop(); damages.append(('missing-actual-edge', wrong))
        wrong = copy.deepcopy(graph); wrong['edges'][0] = [1, 2, 3, 4, 5, 6, 8]; damages.append(('wrong-valid-size-edge', wrong))
        wrong = copy.deepcopy(graph); wrong['monochromatic_primitive_patterns'].pop(); damages.append(('missing-actual-primitive', wrong))
        wrong = copy.deepcopy(graph); wrong['mask'] = 16; damages.append(('wrong-absolute-mask', wrong))
        wrong = copy.deepcopy(graph); wrong['edge_degrees'][0] += 1; damages.append(('wrong-degree', wrong))
        wrong = copy.deepcopy(graph); wrong['period'] = 618; damages.append(('wrong-physical-period', wrong))
        rejected = []
        for name, damaged in damages:
            try:
                check(damaged, 72)
            except ValueError:
                rejected.append(name)
            else:
                raise ValueError('meaningful physical certificate damage accepted: ' + name)
        need(len(rejected) == 8, 'whole meaningful damage domain')
        need([1, 2, 3, 4, 5, 6, 7] in graph['edges'], 'actual seed support positive control')
        print(json.dumps({'author': 'six-vdw-1', 'role': 'researcher',
                          'status': 'ALL_PHYSICAL_CERTIFICATE_DAMAGES_REJECTED',
                          'rejected': rejected, 'explicit_seed_positive_control': 1}, sort_keys=True))
