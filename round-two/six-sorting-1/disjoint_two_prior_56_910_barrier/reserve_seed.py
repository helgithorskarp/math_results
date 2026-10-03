"""Exact seed-level HIGH reserve proposals, credited8539/peer2655 context.

No generic novelty or whole-route exclusion is claimed by this packed selector.
Each ORIGINAL two-HIGH record is retained; its reserve uses the CLASS maximum E.
Separate scalar checking is required before imposing preparation restrictions.
"""
from collections import Counter
import hashlib
import importlib.util
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


def main():
    operations_allow()
    started = time.monotonic()
    source = PUBLIC/'prior'
    manifest = json.loads((source/'source-manifest.json').read_text())
    pin = next(r['sha256'] for r in manifest['files'] if r['path'] == 'profile.py')
    need(hashlib.sha256((source/'profile.py').read_bytes()).hexdigest() == pin,
         'Credited packed original profiler changed')
    spec = importlib.util.spec_from_file_location('credited_high_reserve_profile', source/'profile.py')
    profile = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(profile)
    fixture = json.loads((source/'fixture.json').read_text())
    word = fixture['B23']+fixture['LOW_suffixes']['4']+[[5, 6], [9, 10]]
    need(len(word) == 28, 'Wrong literal seed')
    data = profile.analyze_family(13, word, 0, 2)
    classes = {hi: d for lo, hi, d, c in data['envelope']}
    need({hi.bit_length()-1 for hi in classes} == {12} and
         sorted((hi ^ (1 << 12), d) for hi, d in classes.items()) ==
         sorted((1 << q, d) for q, d in [(6, 7), (7, 6), (10, 7), (11, 7)]),
         'Actual current HIGH class maxima do not match the assumed live genealogy')
    rows = []
    for r in data['records']:
        E = classes[r[3]]
        h = 9-E
        cost = r[4]+r[5]+h
        rows.append({'original_HIGH_mask': r[1], 'original_record': r,
                     'current_class_maximum_E': E,
                     'necessary_future_marked_touches': h,
                     'original_seed_cost_plus_future_reserve': cost,
                     'allowed_additional_whole_cube_identities': 9-cost,
                     'status': 'DIRECT_FUTURE_PRUNING_PROPOSAL' if cost > 9 else
                     'TIGHT_FUTURE_ACTIVITY_PROPOSAL' if cost == 9 else
                     'POSITIVE_IDENTITY_SLACK_NOT_TIGHT'})
    need(len(rows) == 78 and time.monotonic()-started < 45, 'Incomplete seed reserve selection')
    finite = {'literal_prefix_sha256': digest(word), 'ordinary_HIGH_mass': data['summary']['ordinary_mass'],
              'class_envelope': data['envelope'], 'original_records_sha256': digest(data['records']),
              'reserve_rows_sha256': digest(rows),
              'census': dict(Counter(r['status'] for r in rows)),
              'reserved_cost_histogram': dict(sorted(Counter(
                  r['original_seed_cost_plus_future_reserve'] for r in rows).items())),
              'maximum_reserved_cost': max(r['original_seed_cost_plus_future_reserve'] for r in rows),
              'credited_packed_source_sha256': pin}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'PACKED_ORIGINAL_HIGH_RESERVE_PROPOSALS_NEED_SCALAR_EVENT_CHECK',
              'finite': finite, 'finite_sha256': digest(finite), 'literal_prefix': word,
              'reserve_rows': rows, 'seconds': time.monotonic()-started,
              'context': '8539 ordinary pruning; peer2655 unpublished conditional reserve idea. No novelty or review transfer.',
              'scope': 'Only the stipulated first-singleton/equal-event HIGH genealogy, not unequal jumps.'}
    (WORK/'reserve-seed.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('literal_prefix', 'reserve_rows')}), flush=True)


if __name__ == '__main__':
    main()
