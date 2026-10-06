#!/usr/bin/env python3
"""Definition-level membership certificate for the FIXED43 seed supply."""
import argparse
from fractions import Fraction
from hashlib import sha256
import itertools
import json
import os
from pathlib import Path
import platform
import resource
from time import monotonic, perf_counter


def need(v, label):
    if not v:
        raise AssertionError(label)


def pin(p):
    b = Path(p).read_bytes()
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}


def shape(word):
    if len(word) == 1:
        return 1, [word[0]]
    center = word.index(max(word))
    need(center > 0 and len(word[:center]) == len(word[center + 1:]), 'full perfect left/right sizes')
    left_h, left_leaves = shape(word[:center])
    right_h, right_leaves = shape(word[center + 1:])
    need(left_h == right_h, 'equal recursive perfect heights')
    return left_h + 1, left_leaves + right_leaves


def all_boxes(word):
    boxes, quads = [], 0
    for a, b, c, d in itertools.combinations(range(len(word)), 4):
        quads += 1
        if word[b] < word[a] < word[d] < word[c] and not any(
            word[b] < word[j] < word[c] for j in range(a + 1, d) if j not in (b, c)
        ):
            boxes.append([a, b, c, d])
    return boxes, quads


def main(args):
    start, deadline = perf_counter(), monotonic() + 10
    packet, out = Path(args.packet), Path(args.out)
    need(not out.exists(), 'fresh single attempt output')
    out.mkdir()
    mf = json.loads((packet / 'MANIFEST.json').read_text())
    need(pin(packet / 'MANIFEST.json') == {'bytes': 3936, 'sha256': '926cf07ed302e22f6838081eff5359bd89af9eb5049adcdea5bce6e0ec5baaf1'}, 'fixed entire864 packet')
    before = []
    for row in mf['files']:
        p = packet / row['path']
        need(pin(p) == {'bytes': row['bytes'], 'sha256': row['sha256']}, 'every8 received pin')
        before.append((p, pin(p)))
    seed = packet / 'received/theo_rank_corridor_threshold817_v1/received/quinn_reverse_join_v1/balanced_fiber_h3.txt'
    lines = seed.read_text().splitlines()
    need(lines[0] == '7 43' and len(lines) == 44, 'exact fixed seed file')
    words = [tuple(map(int, line.split())) for line in lines[1:]]
    need(len(set(words)) == 43 and all(sorted(w) == list(range(1, 8)) for w in words), '43 DISTINCT size7 permutations')
    data = packet / 'theo817_independent_check_v1/all_records_v1.ndjson'
    old_records = [json.loads(line) for line in data.read_text().splitlines()]
    accepted_inputs = [r for r in old_records if r['kind'] == 'input_words']
    need(len(accepted_inputs) == 43, 'only corresponding43 input DATA, not old1903 reconstruction')
    records, quadruples = [], 0
    for index, word in enumerate(words):
        need(monotonic() < deadline, 'native internal10s cap')
        height, leaves = shape(word)
        boxes, count = all_boxes(word)
        quadruples += count
        need(height == 3 and not boxes, 'seed P3 membership')
        rec = {'kind': 'input_words', 'record': {'index': index, 'word': list(word),
               'leaf_value_set': sorted(leaves), 'full_literal_boxes': boxes}}
        need(rec == accepted_inputs[index], 'EVERY corresponding input record field')
        records.append(rec)
    wire = b''.join((json.dumps(rec, sort_keys=True, separators=(',', ':')) + '\n').encode() for rec in records)
    expected = b''.join((json.dumps(rec, sort_keys=True, separators=(',', ':')) + '\n').encode() for rec in accepted_inputs)
    need(wire == expected and quadruples == 1505, 'complete43 certificate and quadruples')
    (out / 'all43_seed_membership_v1.ndjson').write_bytes(wire)
    bases = ((1, 3, 2), (2, 3, 1))
    family3 = sorted(tuple(3 + x for x in a) + (7,) + b for a in bases for b in bases)
    need(len(set(family3)) == 4 and all(w in words for w in family3), 'four F3 words in SAME supply')
    bad, good = Fraction(4, 43) ** 2, 1 - Fraction(4, 43) ** 2
    need(bad == Fraction(16, 1849) and good == Fraction(1833, 1849), 'exact h3 rational boundary')
    for p, expected_pin in before:
        need(pin(p) == expected_pin, 'all8 original received inputs unchanged')
    report = {'actor': 'literature-researcher-3', 'scope': 'ENTIRE864 finite43 LOWER supply only; uniform full-law proof separate',
              'existing_seed_words': 43, 'all_distinct': True, 'all_perfect_heights': 3,
              'all_complete_literal_boxes_empty': True, 'all43_input_record_fields_equal': True,
              'quadruples_visited': quadruples, 'certificate': pin(out / 'all43_seed_membership_v1.ndjson'),
              'F3_members_already_inside_same43_DATA': [list(w) for w in family3],
              'bad_mass_upper_h3': [bad.numerator, bad.denominator],
              'complement_mass_lower_h3': [good.numerator, good.denominator],
              'exact_complete_w3_is_accepted_old_dependency_not_recensused': True,
              '5040_permutation_or1849_join_or_old_DP_replayed': False,
              'old1903_threshold_scope_reproduced': False, '855859_upper_theorem_checked': False,
              'new_source_or_larger_family_height_domain_generated': False,
              'new_full_mean_or_complement_gain_proved': False, 'full_target_solved': False,
              'author_or_teammate_executable_imports': 0, 'all8_received_pins_unchanged': True,
              'native_threads': 1, 'processes': 1, 'python': platform.python_version(),
              'source': pin(Path(__file__)), 'prospective_uniform_proof': pin(Path(args.proof)),
              'seconds_before_report_serialization': perf_counter() - start,
              'peak_RSS_KiB_before_report_serialization': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (out / 'seed43_mass864_independent_report_v1.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for name in ('packet', 'out', 'proof'):
        p.add_argument('--' + name, required=True)
    args = p.parse_args()
    try:
        need(all(os.environ.get(k) == '1' for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS')), 'native1 contract')
        main(args)
    except Exception as e:
        out = Path(args.out)
        if out.exists():
            (out / 'FIRST_FAILURE.json').write_text(json.dumps({'type': type(e).__name__, 'message': str(e)}, indent=2) + '\n')
        raise
