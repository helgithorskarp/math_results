"""Audit coverage of explicitly imported finite lemmas, not re-enumeration."""
from itertools import combinations
import json
from common import DEPENDENCY, move, points, require


def check_imports(circles, summary, stabilizer):
    forced = set(summary['forced_gaps'])
    special = set(summary['special_circles'])
    extras = set(circles) - forced
    five = json.loads((DEPENDENCY / 'four_gap_expected.json').read_text())
    single5 = [c for c in five['single_cases'] if set(c['gaps']) & special]
    require(len(single5) == 1 and single5[0]['case'] == 0
            and single5[0]['maximum_clique_size'] == 4,
            'imported five-gap special case differs')
    require(set(single5[0]['gaps']) == forced | {362}
            and {move(362, p) for p in stabilizer} == special,
            'five-gap imported class does not cover H')
    six = json.loads((DEPENDENCY / 'fixed_word_gap_expected.json').read_text())
    selected = [c for c in six['single_cases'] if set(c['gaps']) & special]
    require([c['case'] for c in selected] == list(range(62)),
            'imported six-gap special case identifiers differ')
    cover = set()
    for case in selected:
        extra = set(case['gaps']) - forced
        require(case['complete'] and len(extra) == 2
                and case['maximum_clique_size'] <= 5, 'six-gap imported bound differs')
        images = {tuple(sorted(sum(1 << p[i] for i in points(c)) for c in extra))
                  for p in stabilizer}
        require(images <= set(combinations(sorted(extras), 2)) and not cover & images
                and len(images) == case['orbit_size'], 'six-gap orbit coverage differs')
        cover.update(images)
    universe = {pair for pair in combinations(sorted(extras), 2) if set(pair) & special}
    require(cover == universe and len(cover) == 476, 'six-gap special cover incomplete')
    # The eighteen-class theorem for two noncontained words remains a
    # mathematical premise. This checks its saved input's exact coverage.
    contained = {sum(1 << p for p in q) for c in circles for q in combinations(points(c), 4)}
    noncontained = {sum(1 << p for p in q) for q in combinations(range(17), 4)} - contained
    partners = {q for q in noncontained if (q & 15).bit_count() <= 1
                and len({c for c in circles if (c & q).bit_count() >= 3} & forced) == 1}
    pair_cases = six['pair_cases']
    require(len(pair_cases) == 18, 'wrong imported two-word class count')
    partner_cover = set()
    for case in pair_cases:
        require(case['complete'] and case['maximum_clique_size'] <= 5,
                'two-word imported bound incomplete')
        q = six['pair_normalization']['cases'][case['case']]['second_four_set']
        orbit = {move(q, p) for p in stabilizer}
        require(orbit <= partners and not orbit & partner_cover
                and len(orbit) == case['orbit_size'], 'two-word imported orbit differs')
        require(set(case['gaps']) == forced | {c for c in circles if (c & q).bit_count() >= 3},
                'two-word imported forced gaps differ')
        partner_cover.update(orbit)
    require(partner_cover == partners and len(partners) == 132,
            'two-word imported partner cover incomplete')
    return {'five_gap_classes': 1, 'five_gap_labeled_choices': 8, 'five_gap_s_bound': 4,
            'six_gap_classes': 62, 'six_gap_labeled_pairs': 476, 'six_gap_s_bound': 5,
            'two_word_classes': 18, 'two_word_partners': 132, 'two_word_s_bound': 5}
