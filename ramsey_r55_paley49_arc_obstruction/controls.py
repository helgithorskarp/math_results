"""Bounded checks of chart coverage, field transport, and physical extraction."""
import copy
import json
from itertools import combinations
from pathlib import Path

import build
import check
import extract
import verify_witness


def rejected(function, value):
    try:
        function(value)
    except (ValueError, TypeError, KeyError, IndexError):
        return True
    return False


def main():
    document = json.loads(Path('certificate.json').read_text())
    check.check(document)
    matrix = build.field_graph()
    check.need(all(matrix[u][v] == check.red(u, v) for u in range(49) for v in range(49)), 'field color agreement')
    inverses = {a: next(b for b in range(1, 49) if build.multiply(a, b) == 1) for a in range(1, 49)}
    linear_maps = 0
    for a in range(1, 49):
        for b in range(1, 49):
            if ((a % 7)*(b//7)-(a//7)*(b % 7)) % 7 == 0:
                continue
            z = build.multiply(inverses[a], b)
            check.need(z//7 != 0, 'independent columns normalize outside F7')
            for x in range(7):
                for y in range(7):
                    left = build.multiply(a, x)
                    right = build.multiply(b, y)
                    combined = (left % 7+right % 7) % 7+7*((left//7+right//7) % 7)
                    normalized = (x+(z % 7)*y) % 7+7*((z//7)*y % 7)
                    check.need(build.multiply(inverses[a], combined) == normalized, 'linear-map factorization')
            linear_maps += 1
    scalar_pairs = 0
    for a in range(1, 49):
        flip = 1-matrix[0][a]
        for u, v in combinations(range(49), 2):
            check.need(matrix[build.multiply(a,u)][build.multiply(a,v)] == (matrix[u][v] ^ flip), 'global scalar color transport')
            scalar_pairs += 1
    plane = check.points()
    for line in plane:
        outside = [p for p in plane if check.incidence(p, line)]
        check.need(sorted(check.image(outside, line, 7)) == list(range(49)), 'whole affine chart bijection')

    state = 2026090661
    def draw(n):
        nonlocal state
        state = (6364136223846793005*state+1442695040888963407) % (1 << 64)
        return (state >> 32) % n
    physical = 0
    scores = []
    for trial in range(32):
        points = list(range(49))
        for i in range(48, 0, -1):
            j = draw(i+1)
            points[i], points[j] = points[j], points[i]
        points = points[:43]
        spin = [draw(2) for _ in range(43)]
        original = None
        for orientation in (0, 1):
            moved = points if orientation == 0 else [build.multiply(8, x) for x in points]
            doc = {'points': moved, 'switch': spin}
            witness = extract.extract(doc)
            result = verify_witness.verify(witness)
            edges = set(map(tuple, witness['edges']))
            check.need(all(int((i,j) in edges) == (matrix[moved[i]][moved[j]] ^ spin[i] ^ spin[j])
                           for i,j in combinations(range(43),2)), 'all903 physical edges')
            if orientation == 0:
                original = edges
            else:
                check.need(original.isdisjoint(edges) and len(original)+len(edges) == 903, 'physical color reversal')
            physical += 1
            scores.append(result['color'])
    mutations = []
    bad = copy.deepcopy(document); bad['cases'].pop(); mutations.append(bad)
    bad = copy.deepcopy(document); bad['cases'].append(bad['cases'][0]); mutations.append(bad)
    bad = copy.deepcopy(document); bad['cases'][0][3] ^= 1; mutations.append(bad)
    bad = copy.deepcopy(document); bad['cases'][0][-1] = bad['cases'][0][-2]; mutations.append(bad)
    bad = copy.deepcopy(document); bad['arcs'][0][0] = [0,0,0]; mutations.append(bad)
    bad = copy.deepcopy(document); bad['arcs'][1] = bad['arcs'][0]; mutations.append(bad)
    check.need(all(rejected(check.check, bad) for bad in mutations), 'certificate mutations')
    fixture = {'points': list(range(43)), 'switch': [i % 2 for i in range(43)]}
    malformed = []
    for field in ('points','switch'):
        bad = copy.deepcopy(fixture); bad[field].pop(); malformed.append(bad)
    bad = copy.deepcopy(fixture); bad['points'][1] = 0; malformed.append(bad)
    bad = copy.deepcopy(fixture); bad['points'][0] = 49; malformed.append(bad)
    bad = copy.deepcopy(fixture); bad['points'][0] = -1; malformed.append(bad)
    bad = copy.deepcopy(fixture); bad['switch'][0] = 2; malformed.append(bad)
    bad = copy.deepcopy(fixture); bad['points'][0] = True; malformed.append(bad)
    bad = copy.deepcopy(fixture); bad['switch'][0] = '0'; malformed.append(bad)
    check.need(all(rejected(extract.extract, bad) for bad in malformed), 'malformed inputs')
    output = extract.extract(fixture)
    bad_output = copy.deepcopy(output); bad_output['color'] ^= 1
    check.need(rejected(verify_witness.verify, bad_output), 'physical witness mutation')
    return {'status':'VERIFIED_ARC_COVER_AND_PHYSICAL_DECODER_CONTROLS',
            'field_pairs':2401, 'linear_maps':linear_maps,
            'linear_map_point_checks':49*linear_maps, 'scalar_edge_pairs':scalar_pairs,
            'whole_affine_charts':57, 'physical_43_vertex_cases':physical,
            'physical_input_pairs':903*physical,
            'blue_red_returned_witnesses':[scores.count(0), scores.count(1)],
            'certificate_mutations_rejected':len(mutations),
            'malformed_inputs_rejected':len(malformed), 'physical_witness_mutations_rejected':1}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
