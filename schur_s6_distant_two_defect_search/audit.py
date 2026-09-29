"""Directly enumerate all classical Schur triples in the saved words."""
from itertools import permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED_HOLES = {
    '20261001': [202, 404], '20261002': [7, 14],
    '20261003': [2, 4], '20261004': [13, 26],
    '20261005': [10, 20], '20261006': [3, 6],
    '20261008': [2, 4], '20261009': [5, 10],
    '20261010': [13, 26], '20261011': [2, 4],
}
EXPECTED_COMPLETION = {
    '20261001': 30, '20261002': 17, '20261003': 13,
    '20261004': 18, '20261005': 29, '20261006': 25,
    '20261008': 12, '20261009': 9, '20261010': 21,
    '20261011': 14,
}


def defects(word):
    assert len(word) == 537 and set(word) <= set('123456?')
    return [(x, y, x+y) for z in range(2, 538)
            for x in range(1, z//2+1)
            for y in [z-x]
            if word[x-1] != '?' and word[x-1] == word[y-1] == word[z-1]]


def min_completion(word, holes):
    scores = []
    for colours in product('123456', repeat=len(holes)):
        candidate = list(word)
        for v, c in zip(holes, colours):
            candidate[v-1] = c
        scores.append((len(defects(''.join(candidate))), ''.join(colours)))
    return min(scores)


def relabel_distance(a, b):
    assert len(a) == len(b) == 537
    return min(sum(a[i] != '?' and a[i] != p[int(b[i])-1]
                   for i in range(537)) for p in permutations('123456'))


def main():
    partials = {}
    for name, holes in EXPECTED_HOLES.items():
        word = (HERE/'partials'/f'{name}.partial').read_text(encoding='ascii').strip()
        assert [i for i,c in enumerate(word,1) if c == '?'] == holes
        assert defects(word) == []
        assert min_completion(word, holes)[0] == EXPECTED_COMPLETION[name]
        partials[name] = word
    completed = (HERE/'completed29.txt').read_text(encoding='ascii').strip()
    assert completed == partials['20261005'].replace('?', '1')
    assert len(defects(completed)) == 29
    three = (HERE/'best3.txt').read_text(encoding='ascii').strip()
    two = (HERE/'best2.txt').read_text(encoding='ascii').strip()
    assert defects(three) == [(3,3,6), (3,6,9), (12,15,27)]
    assert defects(two) == [(3,3,6), (3,6,9)]
    sources = json.loads((HERE.parent/'schur_s6_multi_alignment_recombination'/'sources.json').read_text())
    distance = {name: relabel_distance(two, row['word']) for name,row in sources.items()}
    assert distance == {'W':414, '190':428, '359':425, 'best3':421, '347':427}
    result = {'partials': {name: {'holes':EXPECTED_HOLES[name],
                                 'min_direct_completion_defects':EXPECTED_COMPLETION[name]}
                           for name in EXPECTED_HOLES},
              'completed29_defects':29,
              'best3_defects':defects(three), 'best2_defects':defects(two),
              'best2_distance_to_prior_words':distance}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
