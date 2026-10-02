"""Construct all32 normalized completions by unused-point replacements.

Eight constructions split the unused point from fixed point16 along any of
three whole block orbits. Twenty-four constructions replace an equivariant
moving point along one whole block orbit. This is a positive rule, compared
entry by entry with the independently counted equality census.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path

from generate import encoded, moved, need, orbit


def valid(words):
    return len(words) == len(set(words)) == 68 and all(0 <= w < 2 ** 18 and w.bit_count() == 5 for w in words) and \
        all((a & b).bit_count() <= 2 for a, b in combinations(words, 2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', type=Path, default=Path(__file__).parent / 'INSTANCE.json')
    parser.add_argument('--completions', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    need(not (args.work / 'CONSTRUCTIONS.json').exists(), 'refuse completed construction overwrite')
    fixture = json.loads(args.instance.read_text()); g = fixture['permutation']
    baseline = set(fixture['classical68_words'])
    need(valid(sorted(baseline)) and all(not w >> 17 & 1 for w in baseline), 'wrong prior unused-point baseline')
    root = {w for w in baseline if w & 1}
    residual = sorted({orbit(w, g) for w in baseline if not w & 1 and len(orbit(w, g)) == 5})
    fixed_rows = [ws for ws in residual if all(w >> 16 & 1 for w in ws)]
    need(len(fixed_rows) == 3, 'wrong root-avoiding fixed-point block orbit count')
    split_codes = set()
    for chosen in range(8):
        old = {w for i, ws in enumerate(fixed_rows) if chosen >> i & 1 for w in ws}
        new = {(w ^ 2 ** 16) | 2 ** 17 for w in old}
        code = tuple(sorted((baseline - old) | new))
        need(valid(code) and root <= set(code), 'invalid fixed-point splitting construction')
        split_codes.add(code)
    moving_rules = []
    moving_codes = set()
    for ws in residual:
        w = ws[0]
        for e in range(18):
            if not w >> e & 1 or g[e] == e:
                continue
            replacement = (w ^ 2 ** e) | 2 ** 17
            new = orbit(replacement, g)
            code = tuple(sorted((baseline - set(ws)) | set(new)))
            if valid(code) and root <= set(code):
                moving_codes.add(code)
                moving_rules.append({'old_seed_word': w, 'erased_seed_point': e,
                                     'old_orbit': ws, 'replacement_orbit': new})
    need(len(split_codes) == 8 and len(moving_codes) == len(moving_rules) == 24 and not split_codes & moving_codes,
         'positive construction classes overlap or differ')
    expected = {tuple(r['words']) for r in json.loads(args.completions.read_text())}
    need(split_codes | moving_codes == expected, 'positive replacement rules do not equal whole completion census')
    result = {'agent': 'six-code-2', 'role': 'researcher',
              'status': 'COMPLETE_POSITIVE_UNUSED_POINT_REPLACEMENT_COVER_OF_ALL32_NORMALIZED_CODES',
              'new_point': 17, 'fixed_split_point': 16, 'fixed_split_block_orbits': fixed_rows,
              'all_fixed_orbit_subsets': 8, 'moving_replacement_rules': moving_rules,
              'all_moving_replacement_codes': 24, 'exact_normalized_code_count': len(expected),
              'changed_words_histogram': [[k, sum(len(set(c) - baseline) == k for c in expected)] for k in (0, 5, 10, 15)],
              'scope': 'An explicit block-substitution mechanism for all normalized saturated-fixed-point68 completions. The completeness premise is the independently checked counting census, not this construction search alone.'}
    (args.work / 'CONSTRUCTIONS.json').write_bytes(encoded(result))
    print(json.dumps({k: v for k, v in result.items() if k not in ('moving_replacement_rules', 'fixed_split_block_orbits')}, sort_keys=True))


if __name__ == '__main__':
    main()
