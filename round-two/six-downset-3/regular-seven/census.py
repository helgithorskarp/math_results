"""Complete simple regular triple collections on seven points, with full S7 classes."""
from collections import Counter, defaultdict
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cubic_seven_census import (TRIPLES, POSITION, canonical_census as cubic_census,
                               degrees, selected, move, image, require)

FULL = (1 << 35)-1
INCIDENT = tuple(sum(1 << j for j, a in enumerate(TRIPLES) if a >> i & 1) for i in range(7))


def link_tail_census():
    containing = [a for a in TRIPLES if a & 1]
    avoiding = [a for a in TRIPLES if not a & 1]
    tails = defaultdict(list)
    for eight in combinations(avoiding, 8):
        signature = degrees(eight)[1:]
        if max(signature) <= 6:
            tails[signature].append(sum(1 << POSITION[a] for a in eight))
    words, count = set(), 0
    for six in combinations(containing, 6):
        target = tuple(6-d for d in degrees(six)[1:])
        prefix = sum(1 << POSITION[a] for a in six)
        for tail in tails.get(target, []):
            words.add(prefix | tail)
            count += 1
    require(len(words) == count, 'link/tail duplicates inputs')
    return words


def gray_subsets(indices):
    powers = [1 << i for i in indices]
    points = [tuple(i for i in range(7) if TRIPLES[j] >> i & 1) for j in indices]
    word, d = 0, [0]*7
    yield word, d
    for step in range(1, 1 << len(indices)):
        j = (step & -step).bit_length()-1
        sign = -1 if word & powers[j] else 1
        word ^= powers[j]
        for i in points[j]:
            d[i] += sign
        yield word, d


def positional_mitm_census():
    left = defaultdict(list)
    for word, d in gray_subsets(list(range(0, 35, 2))):
        if max(d) <= 6:
            left[tuple(d)].append(word)
    words, count = set(), 0
    for word, d in gray_subsets(list(range(1, 35, 2))):
        if max(d) > 6:
            continue
        for prefix in left.get(tuple(6-x for x in d), []):
            words.add(prefix | word)
            count += 1
    require(len(words) == count, 'positional MITM duplicates inputs')
    return words


def data():
    result = [(p, tuple(1 << POSITION[move(a, p)] for a in TRIPLES))
              for p in permutations(range(7))]
    require(len(result) == 5040 and all(len(set(powers)) == 35 and sum(powers) == FULL
                                      for _, powers in result), 'triple permutation is not bijective')
    return result


def word_hash(words):
    return hashlib.sha256(json.dumps(sorted(words), separators=(',', ':')).encode()).hexdigest()


def middle_census(pdata):
    labelled = link_tail_census()
    independent = positional_mitm_census()
    require(labelled == independent, 'two complete middle-degree enumerations disagree')
    del independent
    require(all(w.bit_count() == 14 and all((w & mask).bit_count() == 6 for mask in INCIDENT)
                for w in labelled), 'literal degree-six inputs fail')
    seen, cases = set(), []
    for word in sorted(labelled):
        if word in seen:
            continue
        orbit = {image(word, powers) for _, powers in pdata}
        require(orbit <= labelled and not orbit & seen, 'middle canonical orbit coverage fails')
        require(word == min(orbit), 'middle word is not canonical')
        seen |= orbit
        group = [p for p, powers in pdata if image(word, powers) == word]
        require(len(group)*len(orbit) == 5040, 'middle orbit/stabilizer fails')
        cases.append({'degree': 6, 'canonical_word': word, 'triple_masks': selected(word),
                      'automorphism_order': len(group), 'labelled_orbit_size': len(orbit),
                      'point_transitive': all(len({p[i] for p in group}) == 7 for i in range(7)),
                      'point_group': group})
    require(seen == labelled and len(cases) == 311 and len(labelled) == 1241355,
            'complete middle-degree coverage differs')
    return cases, {'labelled_collections': len(labelled), 'permutation_classes': len(cases),
                   'point_transitive_classes': sum(c['point_transitive'] for c in cases),
                   'two_labelled_enumerations_agree': True, 'sorted_labelled_words_sha256': word_hash(labelled)}


def complements(cases, degree, pdata):
    result, seen = [], set()
    for case in cases:
        images = [(p, image(case['canonical_word'], powers)) for p, powers in pdata]
        largest = max(w for _, w in images)
        p = next(p for p, w in images if w == largest)
        word = FULL ^ largest
        orbit = {FULL ^ w for _, w in images}
        require(word == min(orbit) and not orbit & seen, 'complement canonical orbits fail')
        seen |= orbit
        inverse = tuple(p.index(i) for i in range(7))
        group = sorted(tuple(p[g[inverse[i]]] for i in range(7)) for g in case['point_group'])
        triples = selected(word)
        require(degrees(triples) == (degree,)*7 and len(triples) == 7*degree//3,
                'literal complement degree fails')
        require(all(set(move(a, g) for a in triples) == set(triples) for g in group),
                'conjugated stabilizer does not preserve the complement')
        require(len(group) == len(set(group)) == case['automorphism_order']
                and len(group)*len(orbit) == 5040, 'conjugated stabilizer/orbit sizes fail')
        result.append({'degree': degree, 'canonical_word': word, 'triple_masks': triples,
                       'complement_canonical_word': case['canonical_word'],
                       'automorphism_order': len(group), 'labelled_orbit_size': len(orbit),
                       'point_transitive': all(len({g[i] for g in group}) == 7 for i in range(7)),
                       'point_group': group})
        require(result[-1]['point_transitive'] == case['point_transitive'], 'complement transitivity fails')
    require(len(seen) == sum(c['labelled_orbit_size'] for c in cases), 'complement labelled coverage differs')
    return sorted(result, key=lambda c: c['canonical_word']), {
        'labelled_collections': len(seen), 'permutation_classes': len(result),
        'point_transitive_classes': sum(c['point_transitive'] for c in result),
        'sorted_labelled_words_sha256': word_hash(seen), 'complement_bijection_verified': True}


def census():
    pdata = data()
    classes3, coverage3 = cubic_census()
    for c in classes3:
        c['degree'] = 3
    classes12, coverage12 = complements(classes3, 12, pdata)
    classes6, coverage6 = middle_census(pdata)
    classes9, coverage9 = complements(classes6, 9, pdata)
    all_permutations = [p for p, _ in pdata]
    boundary = [{'degree': d, 'canonical_word': w, 'triple_masks': selected(w),
                 'automorphism_order': 5040, 'labelled_orbit_size': 1,
                 'point_transitive': True, 'point_group': all_permutations}
                for d, w in [(0, 0), (15, FULL)]]
    classes = sorted(boundary+classes3+classes6+classes9+classes12,
                     key=lambda c: (c['degree'], c['canonical_word']))
    require(len(classes) == 644 and len({c['canonical_word'] for c in classes}) == 644,
            'all-regular class coverage differs')
    coverage = {'0': {'labelled_collections': 1, 'permutation_classes': 1, 'point_transitive_classes': 1},
                '3': coverage3, '6': coverage6, '9': coverage9, '12': coverage12,
                '15': {'labelled_collections': 1, 'permutation_classes': 1, 'point_transitive_classes': 1},
                'total_classes': len(classes), 'total_labelled_collections': sum(c['labelled_orbit_size'] for c in classes),
                'total_point_transitive_classes': sum(c['point_transitive'] for c in classes),
                'degree_six_automorphism_order_profile': {
                    str(k): v for k, v in sorted(Counter(c['automorphism_order'] for c in classes6).items())}}
    require(coverage['total_labelled_collections'] == 2505122
            and coverage['total_point_transitive_classes'] == 12, 'combined coverage counts differ')
    return classes, coverage


if __name__ == '__main__':
    cases, coverage = census()
    print(json.dumps({'coverage': coverage,
                      'canonical_words': {str(d): [c['canonical_word'] for c in cases if c['degree'] == d]
                                          for d in [0, 3, 6, 9, 12, 15]}}, indent=2, sort_keys=True))
