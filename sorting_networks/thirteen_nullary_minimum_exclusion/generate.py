"""Regenerate compact frontier data; no solver or proof checker is imported."""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def counted(x, word):
    h = l = 0
    for a, b in word:
        A, B = x >> a & 1, x >> b & 1
        h += bool(A or B); l += not (A and B)
        if A > B:
            x ^= (1 << a) | (1 << b)
    return x, h, l


def prefix(f, case, index):
    p = f['prefix21'] + f['tournaments'][case - 1] + f['minimum_front']
    p += [[a + 1, b + 1] for a, b in f['minimum_words_on_V'][index]]
    p += [[a + 2, b + 2] for a, b in f['maximum_word_on_U']]
    return p


def threshold_rows(f, index):
    p = prefix(f, 2, index); lower = f['known_lower_bounds']
    limits, witnesses = {}, {}
    for x in range(8192):
        z, h, l = counted(x, p); z = z >> 2 & 255
        for direction, cap in ((1, 44 - lower[13 - x.bit_count()] - h),
                               (0, 44 - lower[x.bit_count()] - l)):
            key = z, direction
            if key not in limits or cap < limits[key]:
                limits[key] = cap; witnesses[key] = x
    return [[z, limits[z, 1], limits[z, 0], witnesses[z, 1], witnesses[z, 0]]
            for z in sorted({z for z, _ in limits})]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    f = json.loads((HERE / 'fixture.json').read_text())
    c = json.loads((HERE / 'certificate.json').read_text())
    assert len(f['minimum_words_on_V']) == 45
    images = []
    for index in range(45):
        sets = [{counted(x, prefix(f, case, index))[0] >> 2 & 255 for x in range(8192)}
                for case in (1, 2)]
        assert sets[0] == sets[1]
        images.append(sorted(sets[0]))
    assert images == c['F_states_by_tree']
    for source in c['sources']:
        assert threshold_rows(f, source['index']) == source['single_threshold_rows']
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher',
                      'literal_images': 90, 'distinct_tree_indices': 45,
                      'exclusion_sources': len(c['sources']),
                      'status': 'Exact compact data regeneration passed'}))


if __name__ == '__main__':
    main()
