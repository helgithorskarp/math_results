"""Small trust-boundary controls, by six-reviewer-2."""
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import json
import audit


def main():
    given = json.loads(Path(__file__).with_name('INPUT.json').read_text())
    corruptions = []
    bad = deepcopy(given)
    bad['design_circles'][0] = bad['design_circles'][1]
    corruptions.append(bad)
    bad = deepcopy(given)
    bad['design_circles'].pop()
    corruptions.append(bad)
    bad = deepcopy(given)
    bad['root_word'] = given['design_circles'][0]
    corruptions.append(bad)
    bad = deepcopy(given)
    bad['actual_transport_generators'][0][0] = 0
    corruptions.append(bad)
    bad = deepcopy(given)
    bad['actual_transport_generators'][0] = list(range(17))
    bad['actual_transport_generators'][0][0:2] = [1, 0]
    corruptions.append(bad)
    for bad in corruptions:
        try:
            audit.prepare(bad)
        except ValueError:
            pass
        else:
            raise ValueError('corrupt input accepted')
    for kwargs in ({'max_products': 0}, {'max_seconds': 0}):
        try:
            audit.run(given, **kwargs)
        except RuntimeError as error:
            audit.require('INCOMPLETE' in str(error), 'wrong resource status')
        else:
            raise ValueError('resource guard yielded a mathematical verdict')
    # Local proof that a five-circle cannot own triples from three compatible words.
    triples = list(map(frozenset, combinations(range(5), 3)))
    audit.require(not any(all(len(a & b) <= 1 for a, b in combinations(family, 2))
                          for family in combinations(triples, 3)), 'three compatible triples')
    witness = json.loads(Path(__file__).with_name('WITNESS.json').read_text())
    circles, words, owners, root, orbit = audit.prepare(given)
    seven = witness['four_parts']
    audit.require(len(seven) == len(set(seven)) == 7 and all(q in owners for q in seven)
                  and all((a & b).bit_count() <= 1 for a, b in combinations(seven, 2)),
                  'malformed seven-word fixture')
    removed = 0
    for q in seven:
        removed |= owners[q]
    reconstructed = sorted([c for i, c in enumerate(circles) if not removed & (1 << i)]
                           + [q | (1 << 17) for q in seven])
    audit.require(removed.bit_count() == 16 and reconstructed == witness['words']
                  and len(reconstructed) == 59
                  and all(q.bit_count() == 5 for q in reconstructed)
                  and all((a & b).bit_count() <= 2 for a, b in combinations(reconstructed, 2))
                  and audit.digest(reconstructed) == witness['canonical_word_list_sha256'],
                  'malformed fifty-nine-word fixture')
    print(json.dumps({'status': 'COMPLETE', 'invalid_inputs_rejected': len(corruptions),
                      'incomplete_guards': 2, 'three_triples_in_five_circle': 0,
                      'seven_word_sharp_fixture_size': len(reconstructed)}, sort_keys=True))


if __name__ == '__main__':
    main()
