"""Small direct-intersection projection controls, six-code-2 researcher.

Controls include shared identical replacements and different records over
one old word. Direct pair checks neither use incidence rows nor De Morgan
projection. This is implementation validation, not gap-orbit coverage.
"""
from itertools import combinations
from pathlib import Path
import json
import random
import resource
import time

from geometry import classical_design, points, require
from generate_two_gap import enumerate_masks
from generate_five_gap_projection import project
from verify_five_gap_projection import pair_projection
from verify_fixed_word_gap import check_witness


def direct(records):
    words = sorted({b for b, _ in records})
    positions = {b: i for i, b in enumerate(words)}
    rows = [0] * len(words)
    for (b, qs), (d, rs) in combinations(records, 2):
        if b == d or (b & d).bit_count() > 2:
            continue
        if any(q != r and (q & r).bit_count() > 1 for q in qs for r in rs):
            continue
        i, j = positions[b], positions[d]
        rows[i] |= 1 << j
        rows[j] |= 1 << i
    return rows, words


def compare(records):
    records = sorted(set(records))
    require(records and all(all((q & r).bit_count() <= 1 for q, r in combinations(qs, 2))
                            for _, qs in records), 'invalid control internal replacement choices')
    expected, words = direct(records)
    a, a_words, _ = project(records)
    b, b_words, _ = pair_projection(records)
    require(words == a_words == b_words and a == expected == b, 'direct projection control mismatch')
    return len(records), len(words)



def known_69_check(circles, folder):
    fixture = json.loads((folder / 'witness69.json').read_text())
    outsider = fixture['outsider']
    qs = fixture['old_parts']
    circle_sets = {c: frozenset(points(c)) for c in circles}
    require(len(qs) == len(set(qs)) == 10, 'known fixture replacements changed')
    owners = []
    for q in qs:
        owner = [c for c, pts in circle_sets.items() if frozenset(points(q)) <= pts]
        require(len(owner) == 1, 'known replacement has no unique circle owner')
        owners.append(owner[0])
    require(len(set(owners)) == 10, 'known fixture owner repeated')
    words = (set(circles) - set(owners)) | {outsider} | {q | (1 << 17) for q in qs}
    sets = [frozenset(i for i in range(18) if w >> i & 1) for w in words]
    require(len(words) == 69 and all(len(w) == 5 for w in sets), 'known fixture size or weight wrong')
    require(all(len(a & b) <= 2 for a, b in combinations(sets, 2)), 'known fixture incompatible')
    require(outsider not in circles and not outsider >> 17, 'known outsider classification wrong')
    require(len(set(circles) - words) == 10, 'known fixture R changed')
    return {'size': 69, 's': 1, 'a': 10, 't': 0, 'R': 10, 'g': 0,
            'status': 'previously published construction checked, not a new lower bound'}


def main():
    start = time.monotonic()
    folder = Path(__file__).resolve().parent
    expected = json.loads((folder / 'five_gap_expected.json').read_text())
    norm = expected
    circles, _ = classical_design()
    records, _ = enumerate_masks(circles, norm['cases'][0]['gaps'])
    fixture = expected['five_gap_attainment']['witness']
    fixture_check = check_witness(circles, records, norm['cases'][0]['gaps'], fixture, ())
    require(fixture_check == {'size': 68, 's': 5, 't': 0, 'g': 5}, 'five-gap fixture parameter mismatch')
    chosen = [records[i] for i in fixture['indices']]
    require(len(chosen) == 5 and len({b for b, _ in chosen}) == 5, 'control fixture not a five-clique')
    seed_words = {b for b, _ in chosen}
    alternatives = [r for r in records if r[0] in seed_words and r not in chosen]
    require(len(alternatives) >= 3, 'same-outsider control alternatives absent')
    pool = sorted(chosen + alternatives[:3])
    controls = 0
    maximum_records = 0
    for subset in range(1, 1 << len(pool)):
        require(time.monotonic() - start < 45, 'INCOMPLETE: small-control audit guard')
        sample = [r for i, r in enumerate(pool) if subset >> i & 1]
        n, _ = compare(sample)
        maximum_records = max(maximum_records, n)
        controls += 1
    rng = random.Random(20260930)
    shared_pairs = [(i, j) for i, j in combinations(range(len(chosen)), 2)
                    if set(chosen[i][1]) & set(chosen[j][1])]
    require(shared_pairs, 'positive identical-replacement controls absent')
    # Add larger controls with fixture alternatives and unrelated records.
    # They test real compatible edges as well as many actual obstructions.
    for _ in range(256):
        require(time.monotonic() - start < 45, 'INCOMPLETE: larger-control audit guard')
        sample = chosen + rng.sample(alternatives, min(5, len(alternatives))) + rng.sample(records, 10)
        n, _ = compare(sample)
        maximum_records = max(maximum_records, n)
        controls += 1
    known = known_69_check(circles, folder)
    result = {'known_69_fixture': known, 'agent': 'six-code-2', 'role': 'researcher',
        'status': 'implementation validation only, not full-domain verification',
        'direct_projection_controls': controls, 'all_nonempty_eight_record_subsets': 255,
        'seeded_controls_at_most_twenty_records': 256, 'seed': 20260930,
        'largest_control_records': maximum_records,
        'same_old_word_alternatives_in_pool': len(pool) - len({b for b, _ in pool}),
        'fixture_shared_identical_replacement_pairs': len(shared_pairs),
        'direct_five_gap_attainment_check': fixture_check,
        'seconds': time.monotonic() - start,
        'max_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
