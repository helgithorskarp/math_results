"""Exact census of simple cubic triple collections on seven labelled points."""
from collections import Counter, defaultdict
from itertools import combinations, permutations
import hashlib
import json

NPOINTS = 7
TRIPLES = tuple(sorted(sum(1 << i for i in t) for t in combinations(range(7), 3)))
POSITION = {a: i for i, a in enumerate(TRIPLES)}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def selected(word):
    return [a for i, a in enumerate(TRIPLES) if word >> i & 1]


def word_of(triples):
    return sum(1 << POSITION[a] for a in triples)


def degrees(triples):
    return tuple(sum(a >> i & 1 for a in triples) for i in range(7))


def branching_census():
    points = [tuple(i for i in range(7) if a >> i & 1) for a in TRIPLES]
    suffix = [[0]*7 for _ in range(36)]
    for j in range(34, -1, -1):
        suffix[j] = suffix[j+1].copy()
        for i in points[j]:
            suffix[j][i] += 1
    words = []

    def visit(j, remaining, word):
        if not any(remaining):
            words.append(word)
            return
        if j == 35 or any(d < 0 or d > s for d, s in zip(remaining, suffix[j])):
            return
        visit(j+1, remaining, word)
        if all(remaining[i] for i in points[j]):
            new = remaining.copy()
            for i in points[j]:
                new[i] -= 1
            visit(j+1, new, word | 1 << j)

    visit(0, [3]*7, 0)
    require(len(words) == len(set(words)), 'branching enumeration repeats a word')
    return set(words)


def link_signature_census():
    """Independent join: three edges through point zero, four avoiding it."""
    containing = [a for a in TRIPLES if a & 1]
    avoiding = [a for a in TRIPLES if not a & 1]
    signatures = defaultdict(list)
    for four in combinations(avoiding, 4):
        signatures[degrees(four)[1:]].append(word_of(four))
    result = []
    for three in combinations(containing, 3):
        target = tuple(3-d for d in degrees(three)[1:])
        for tail in signatures.get(target, []):
            result.append(word_of(three) | tail)
    require(len(result) == len(set(result)), 'link join repeats a word')
    return set(result)


def move(a, permutation):
    return sum(1 << permutation[i] for i in range(7) if a >> i & 1)


def image(word, triple_powers):
    result = 0
    while word:
        bit = word & -word
        result |= triple_powers[bit.bit_length()-1]
        word ^= bit
    return result


def canonical_census():
    labelled = branching_census()
    independent = link_signature_census()
    require(labelled == independent, 'independent labelled enumerations disagree')
    require(all(len(selected(w)) == 7 and degrees(selected(w)) == (3,)*7 for w in labelled),
            'enumerated input is not cubic')
    pdata = [(p, tuple(1 << POSITION[move(a, p)] for a in TRIPLES))
             for p in permutations(range(7))]
    seen, cases = set(), []
    for word in sorted(labelled):
        if word in seen:
            continue
        orbit = {image(word, powers) for _, powers in pdata}
        require(orbit <= labelled and not orbit & seen, 'relabelling orbits fail coverage')
        require(word == min(orbit), 'class representative is not canonical')
        seen |= orbit
        group = [p for p, powers in pdata if image(word, powers) == word]
        require(len(group)*len(orbit) == 5040, 'orbit-stabilizer identity fails')
        cases.append({'canonical_word': word, 'triple_masks': selected(word),
                      'automorphism_order': len(group), 'labelled_orbit_size': len(orbit),
                      'point_transitive': all(len({p[i] for p in group}) == 7 for i in range(7)),
                      'point_group': group})
    require(seen == labelled, 'canonical orbit union misses labelled inputs')
    summary = {'labelled_collections': len(labelled), 'permutation_classes': len(cases),
               'point_transitive_classes': sum(c['point_transitive'] for c in cases),
               'automorphism_order_profile': {str(k): v for k, v in sorted(Counter(c['automorphism_order'] for c in cases).items())},
               'two_labelled_enumerations_agree': True,
               'sorted_labelled_words_sha256': hashlib.sha256(json.dumps(sorted(labelled), separators=(',', ':')).encode()).hexdigest()}
    return cases, summary


if __name__ == '__main__':
    cases, summary = canonical_census()
    print(json.dumps({'coverage': summary, 'classes': cases}, indent=2, sort_keys=True))
