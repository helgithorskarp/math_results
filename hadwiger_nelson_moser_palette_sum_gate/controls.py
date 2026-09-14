"""Author-side entry-by-entry arithmetic comparison and certificate faults."""
import copy
import itertools
import json
from pathlib import Path

import build
import verify


def main():
    root = Path(__file__).parent
    graph = build.construct(json.loads((root/'inputs.json').read_text()))
    m, p = verify.sources()
    points = sorted({verify.add(a, b) for a in m for b in p})
    verify.check(points == graph['points'], 'producer/formula points differ')
    count = 0
    for a, b in itertools.combinations(points, 2):
        d = tuple(x-y for x, y in zip(a, b))
        verify.check(build.norm(d) == verify.squared_distance(a, b), 'norm mismatch')
        count += 1
    verify.check(verify.edges(points) == graph['edges'], 'edge lists differ')
    cert = json.loads((root/'certificate.json').read_text())
    verify.verify(cert)
    mutations = []
    bad = copy.deepcopy(cert)
    a, b = graph['edges'][0]
    word = list(bad['four_colour_word'])
    word[b] = word[a]
    bad['four_colour_word'] = ''.join(word)
    mutations.append(bad)
    for key, value in [('four_colour_word', cert['four_colour_word'][:-1]),
                       ('four_colour_word', '4'+cert['four_colour_word'][1:]),
                       ('points_sha256', '0'*64), ('edges_sha256', '0'*64)]:
        bad = copy.deepcopy(cert)
        bad[key] = value
        mutations.append(bad)
    for bad in mutations:
        try:
            verify.verify(bad)
        except ValueError:
            continue
        raise ValueError('corrupt certificate accepted')
    print(json.dumps({'status': 'PASS', 'point_tuples_compared': len(points),
                      'norm_vectors_compared': count,
                      'rejected_certificate_mutations': len(mutations)}, sort_keys=True))


if __name__ == '__main__':
    main()
