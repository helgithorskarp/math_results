"""Complete degree-twelve triple cohort on seven points, via hole complementation."""
from collections import Counter
import hashlib
from itertools import permutations
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cubic_seven_census import (TRIPLES, POSITION, branching_census,
                               link_signature_census, selected, degrees,
                               move, image, require)

FULL_WORD = (1 << 35)-1


def census():
    sparse = branching_census()
    independently_sparse = link_signature_census()
    require(sparse == independently_sparse, 'two cubic hole enumerations disagree')
    labelled = {FULL_WORD ^ w for w in sparse}
    independent = {FULL_WORD ^ w for w in independently_sparse}
    require(labelled == independent and len(labelled) == len(sparse),
            'complement bijection or labelled coverage fails')
    require(all(len(selected(w)) == 28 and degrees(selected(w)) == (12,)*7
                for w in labelled), 'literal degree-twelve condition fails')
    pdata = [(p, tuple(1 << POSITION[move(a, p)] for a in TRIPLES))
             for p in permutations(range(7))]
    seen, cases = set(), []
    for word in sorted(labelled):
        if word in seen:
            continue
        orbit = {image(word, powers) for _, powers in pdata}
        require(orbit <= labelled and not orbit & seen, 'dense permutation orbits overlap')
        require(word == min(orbit), 'dense class word is not canonical')
        seen |= orbit
        group = [p for p, powers in pdata if image(word, powers) == word]
        require(len(group)*len(orbit) == 5040, 'dense orbit-stabilizer identity fails')
        hole = FULL_WORD ^ word
        sparse_canonical = min(image(hole, powers) for _, powers in pdata)
        require(all((image(word, powers) ^ image(hole, powers)) == FULL_WORD
                    for _, powers in pdata), 'relabelled complementation fails')
        cases.append({'canonical_word': word, 'triple_masks': selected(word),
                      'omitted_triple_masks': selected(hole),
                      'hole_cubic_canonical_word': sparse_canonical,
                      'automorphism_order': len(group), 'labelled_orbit_size': len(orbit),
                      'point_transitive': all(len({p[i] for p in group}) == 7 for i in range(7)),
                      'point_group': group})
    require(seen == labelled, 'dense canonical orbits miss labelled inputs')
    require(len(cases) == 10 and len(labelled) == 11205, 'dense quantified coverage differs')
    summary = {'labelled_collections': len(labelled), 'permutation_classes': len(cases),
               'point_transitive_classes': sum(c['point_transitive'] for c in cases),
               'automorphism_order_profile': {str(k): v for k, v in sorted(Counter(c['automorphism_order'] for c in cases).items())},
               'two_labelled_enumerations_agree': True,
               'complement_commutes_with_all_tested_permutations': True,
               'sorted_labelled_words_sha256': hashlib.sha256(json.dumps(sorted(labelled), separators=(',', ':')).encode()).hexdigest()}
    return cases, summary


if __name__ == '__main__':
    cases, summary = census()
    print(json.dumps({'coverage': summary, 'classes': cases}, indent=2, sort_keys=True))
