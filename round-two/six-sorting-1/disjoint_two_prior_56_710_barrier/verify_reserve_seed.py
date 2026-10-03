"""Separate scalar ORIGINAL HIGH cubes and complete equal-event reserve check.

No packed profiler/selector imports. All78 originals are replayed on their full
2048-input cubes. Dead-port projections are only exact activity interfaces;
they never replace an original in a negative cost certificate.
"""
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import sys
import time

from controls import operations_allow

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT
WORK = ROOT/'work'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def marker_touches(start_port, word):
    row = [0]*13
    row[start_port], row[12] = 2, 3
    count = 0
    for a, b in word:
        count += int(row[a] > 1 or row[b] > 1)
        if row[a] > row[b]:
            row[a], row[b] = row[b], row[a]
    return count, [i for i, x in enumerate(row) if x > 1]


def main():
    operations_allow()
    started = time.monotonic()
    deadline = started+45
    proposal = json.loads((WORK/'reserve-seed.json').read_text())
    need(digest(proposal['finite']) == proposal['finite_sha256'] and
         digest(proposal['reserve_rows']) == proposal['finite']['reserve_rows_sha256'],
         'Changed seed reserve proposal')
    source = PUBLIC/'prior'
    manifest = json.loads((source/'source-manifest.json').read_text())
    pin = next(r['sha256'] for r in manifest['files'] if r['path'] == 'numeric.py')
    need(hashlib.sha256((source/'numeric.py').read_bytes()).hexdigest() == pin,
         'Credited separate scalar primitive changed')
    spec = importlib.util.spec_from_file_location('separate_high_reserve_numeric', source/'numeric.py')
    numeric = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(numeric)
    fixture = json.loads((source/'fixture.json').read_text())
    word = fixture['B23']+fixture['LOW_suffixes']['4']+[[5, 6], [7, 10]]
    need(word == proposal['literal_prefix'] and len(word) == 28 and
         digest(word) == proposal['finite']['literal_prefix_sha256'], 'Wrong literal seed')
    records, domains = [], []
    dead = [2, 3, 4, 5, 7, 8]
    projected_assignments = 0
    for a, b in combinations(range(13), 2):
        operations_allow()
        need(time.monotonic() < deadline, 'Incomplete45s ORIGINAL reserve replay')
        high = (1 << a)+(1 << b)
        record = numeric.family(13, word, 0, high, 'reserve')
        records.append(record)
        initial, free = numeric.template(13, 0, high)
        image = set()
        for assignment in range(2048):
            row = list(initial)
            for j, port in enumerate(free):
                row[port] = (assignment >> j) & 1
            result = numeric.simulate(row, word)
            need(numeric.ports(result) == record[2:4] and
                 all(result[p] in (0, 1) for p in dead),
                 'Original marker/free dead-port projection differs')
            image.add(sum(result[p] << j for j, p in enumerate(dead)))
            projected_assignments += 1
        domains.append({'original_HIGH_mask': high, 'current_HIGH_mask': record[3],
                        'original_record': record,
                        'dead_projected_image_mask': sum(1 << i for i in image),
                        'dead_projected_image_size': len(image)})
    records.sort()
    classes = {}
    for lo, high, current_lo, current_hi, D, R, identities in records:
        need(lo == current_lo == 0 and current_hi.bit_count() == 2 and current_hi >> 12 & 1,
             'Wrong original two-HIGH marker tags')
        classes[current_hi] = max(classes.get(current_hi, 0), D)
    live = {(mask ^ (1 << 12)).bit_length()-1: E for mask, E in classes.items()}
    need(live == {6: 7, 9: 6, 10: 7, 11: 7} and
         sum(1 << E for E in live.values()) == 448, 'Actual HIGH class maximum genealogy differs')
    expected = []
    for record in records:
        E = classes[record[3]]
        h = 9-E
        cost = record[4]+record[5]+h
        need(cost == 9, 'This original is not actually tight under its CLASS reserve')
        expected.append({'original_HIGH_mask': record[1], 'original_record': record,
                         'current_class_maximum_E': E,
                         'necessary_future_marked_touches': h,
                         'original_seed_cost_plus_future_reserve': cost,
                         'allowed_additional_whole_cube_identities': 0,
                         'status': 'TIGHT_FUTURE_ACTIVITY_PROPOSAL'})
    need(expected == proposal['reserve_rows'], 'Packed ORIGINAL cost/reserve rows differ')
    event_words = []
    event_controls = 0
    for p in dead:
        initial = dict(live)
        initial[9] += 1
        head = [[p, 9]]
        need(sum(1 << E for E in initial.values()) == 512, 'Singleton mass saturation differs')

        def visit(current, tail):
            nonlocal event_controls
            if len(current) == 1:
                need(current == {11: 9} and len(tail) == 3,
                     'Necessary final root/cost or merge number differs')
                event_words.append(head+tail)
                return
            for a, b in combinations(sorted(current), 2):
                event_controls += 1
                if current[a] != current[b]:
                    continue
                after = dict(current)
                after[b] = after.pop(a)+1
                visit(after, tail+[[a, b]])

        visit(initial, [])
    need(len(event_words) == 36 and event_controls == 180,
         'Complete six-head/six-order equal-event cover differs')
    replay = []
    for record in records:
        port = (record[3] ^ (1 << 12)).bit_length()-1
        for future in event_words:
            touches, marks = marker_touches(port, future)
            need(touches == 9-classes[record[3]] and marks == [11, 12],
                 'Actual original future touches differ from the CLASS reserve')
            replay.append([record[1], future, touches])
    # A legal mass448->512 UNEQUAL first binary gives a genuine counterexample
    # to extending the equal-event reserve rule outside its first-singleton scope.
    unequal = [[6, 9], [10, 11], [9, 11]]
    controls = []
    for row in records:
        if row[3] != ((1 << 9)+(1 << 12)):
            continue
        actual, marks = marker_touches(9, unequal)
        need(actual == 2 != 9-classes[row[3]] and marks == [11, 12],
             'Unequal-jump countercontrol does not refute the false broader reserve')
        controls.append([row[1], actual, 9-classes[row[3]]])
    need(bool(controls), 'Missing genuine unequal-jump countercontrol')
    finite = {'literal_prefix_sha256': digest(word), 'originals': len(records),
              'original_records_sha256': digest(records),
              'producer_seed_reserve_finite_sha256': proposal['finite_sha256'],
              'CLASS_maximum_live_costs': sorted(live.items()),
              'all78_actual_seed_cost_plus_reserve_equal9': True,
              'full_original_free_assignments': 78*2048,
              'credited_scalar_metrics': numeric.METRICS,
              'dead_projected_assignments': projected_assignments,
              'whole_original_activity_domains_sha256': digest(domains),
              'distinct_activity_images': len({r['dead_projected_image_mask'] for r in domains}),
              'future_legal_event_words': 36, 'event_controls': event_controls,
              'original_future_touch_replays': len(replay),
              'original_future_touch_replay_sha256': digest(replay),
              'unequal_jump_countercontrol_sha256': digest(controls),
              'unequal_jump_countercontrol_originals': len(controls),
              'credited_scalar_source_sha256': pin}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'ALL78_WHOLE_ORIGINAL_HIGH_CLASS_RESERVES_AND_ACTIVITY_DOMAINS_VERIFIED',
              'finite': finite, 'finite_sha256': digest(finite),
              'activity_domains': domains, 'seconds': time.monotonic()-started,
              'external_person_review_claimed': False,
              'scope': 'Conditional necessary activity under the stipulated singleton/equal-event route; no whole route exclusion.'}
    suffix = '-O' if not __debug__ else ''
    (WORK / ('reserve-seed-checked'+suffix+'.json')).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'activity_domains'}), flush=True)


if __name__ == '__main__':
    main()
