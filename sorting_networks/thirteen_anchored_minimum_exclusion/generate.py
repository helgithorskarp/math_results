"""Bit-mask reproduction of the anchored two-minimum bound.

six-sorting-1, researcher. No solver or search cutoff. The older minimum-once
exclusion is an explicit imported theorem, not reproduced by this program.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def boolean(mask, word):
    for a, b in word:
        if mask >> a & 1 and not (mask >> b & 1):
            mask ^= (1 << a) | (1 << b)
    return mask


def marked(mask, word):
    deleted = 0
    for a, b in word:
        deleted += bool(mask & ((1 << a) | (1 << b)))
        if not (mask >> a & 1) and mask >> b & 1:
            mask ^= (1 << a) | (1 << b)
    return mask, deleted


def local_facts():
    transitions = []
    anchors = []
    doubles = 0
    for n in (10, 11, 13):
        masks = sorted((1 << a) | (1 << b) for a, b in itertools.combinations(range(n), 2))
        for a, b in itertools.combinations(range(n), 2):
            table = {m: marked(m, [(a, b)]) for m in masks}
            fibers = {}
            for m in masks:
                dest, add = table[m]
                transitions.append([n, m, a, b, dest, add])
                fibers.setdefault(dest, []).append((m, add))
            assert all(len(pre) <= 2 for pre in fibers.values())
            for pre in fibers.values():
                if len(pre) == 2:
                    doubles += 1
                    assert all(add == 1 for m, add in pre)
            for p in range(n):
                newp = a if p == b else p
                charge = int(p in (a, b))
                subset = [m for m in masks if m >> p & 1]
                images = [table[m][0] for m in subset]
                assert all(dest >> newp & 1 for dest in images)
                if charge:
                    assert len(set(images)) == len(subset)
                    assert all(table[m][1] == 1 for m in subset)
                else:
                    assert all(bool(m >> p & 1) == bool(table[m][0] >> p & 1) for m in masks)
                anchors.append([n, p, a, b, newp, charge,
                                [[m, *table[m]] for m in subset]])
    return {'orders': [10, 11, 13], 'marker_transitions': len(transitions),
            'two_preimage_fibers': doubles, 'port_gate_facts': len(anchors),
            'transition_sha256': digest(transitions), 'anchor_sha256': digest(anchors)}


def reproduce(fixture):
    results = []
    bridge = fixture['bridge']
    control = fixture['known19_control']
    assert len(bridge) == 2 and len(control) == 19
    assert all(0 <= a < b < 10 for a, b in control)
    common = None
    for rec in fixture['cases']:
        prefix = fixture['prefix21'] + rec['tournament']
        assert len(prefix) == 24
        assert all(0 <= a < b < 13 for a, b in prefix)
        image = set()
        rimage = set()
        for mask in range(1 << 13):
            y = boolean(mask, prefix)
            ones = mask.bit_count()
            expected_top2 = ((1 << min(ones, 2)) - 1) << (13 - min(ones, 2))
            assert y & (3 << 11) == expected_top2
            image.add(y & ((1 << 11) - 1))
            r = boolean(y, bridge)
            expected_top3 = ((1 << min(ones, 3)) - 1) << (13 - min(ones, 3))
            assert r & (7 << 10) == expected_top3
            rimage.add(r & ((1 << 10) - 1))
            sorted_mask = ((1 << ones) - 1) << (13 - ones)
            assert boolean(y, bridge + control) == sorted_mask
            assert boolean(r, control) == sorted_mask
        assert sorted(image) == rec['Y_states']
        assert sorted(rimage) == fixture['R_states']
        if common is not None:
            assert rimage == common
        common = rimage
        profile = {}
        rprofile = {}
        for a, b in itertools.combinations(range(13), 2):
            initial = (1 << a) | (1 << b)
            m, d = marked(initial, prefix)
            assert m < (1 << 11)
            profile[m] = max(profile.get(m, 0), d)
            rm, rd = marked(initial, prefix + bridge)
            assert rm < (1 << 10)
            rprofile[rm] = max(rprofile.get(rm, 0), rd)
        profile = sorted(map(list, profile.items()))
        assert profile == fixture['two_minimum_profile']
        assert sorted(map(list, rprofile.items())) == profile
        one_zero, deletions = marked(1 << fixture['anchor_original_input'], prefix)
        assert one_zero == 1 << fixture['anchor_port']
        anchor = sum(1 << d for m, d in profile if m >> fixture['anchor_port'] & 1)
        weight = sum(1 << d for m, d in profile)
        ceiling = 1 << (fixture['full_budget'] - fixture['S11'])
        route_lower = 1 << fixture['imported_minimum_passages']
        assert anchor == 160 and weight == 208 and ceiling == 512
        assert route_lower * anchor == 640 > ceiling
        results.append({'case': rec['case'], 'Y_states': len(image), 'R_states': len(rimage),
                        'Y_image_sha256': digest(sorted(image)), 'R_image_sha256': digest(sorted(rimage)),
                        'profile': profile, 'initial_weight': weight, 'initial_anchor_mass': anchor,
                        'one_zero_original_input': fixture['anchor_original_input'],
                        'one_zero_Y_port': fixture['anchor_port'], 'one_zero_prefix_deletions': deletions,
                        'required_suffix_passages': fixture['imported_minimum_passages'],
                        'anchored_lower_bound': route_lower * anchor, 'weight_ceiling': ceiling,
                        'original_inputs_checked': 8192, 'Y21_and_R19_controls': True})
    return {'cases': results, 'local_controls': local_facts(),
            'conclusion': {'Y1_minimum': 21, 'Y2_minimum': 21, 'R137_minimum': 19,
                           'P21_minimum_suffix': 24,
                           'global_S13_interval': [44, 45]},
            'imported_minimum_once_exclusion': fixture['imports']['minimum_once']['graph_ref'],
            'imported_prefix_reduction': fixture['imports']['Y_provenance']['graph_ref'],
            'independence_scope': 'new local transport facts and fixture/control checks; prior exclusion and P21 reduction imported'}


def main():
    if sys.flags.optimize:
        raise RuntimeError('Run without -O: exact assertions are required.')
    fixture = json.loads((HERE / 'fixture.json').read_text())
    result = reproduce(fixture)
    expected = json.loads((HERE / 'certificate.json').read_text())['expected']
    assert result == expected
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher', 'status': 'all_new_checks_passed',
                      'algorithm': 'bit_masks', 'certificate_sha256': hashlib.sha256((HERE / 'certificate.json').read_bytes()).hexdigest(),
                      'checked': result}, indent=2))


if __name__ == '__main__':
    main()
