#!/usr/bin/env python3
"""Optional entry-level comparison; not used by the independent proof run.

Run independent_check.py --events SCRATCH_FILE first. The target module is
imported only here to collect its reported terminal records. No target helper
chooses branches or computes capacities in independent_check.py.
"""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--author-directory', type=Path, required=True)
parser.add_argument('--events', type=Path, required=True)
args = parser.parse_args()
spec = importlib.util.spec_from_file_location('target_production', args.author_directory/'prove.py')
target = importlib.util.module_from_spec(spec)
spec.loader.exec_module(target)
expected = json.loads((args.author_directory/'expected.json').read_text())['cases']
own_expected = {c['M']: c for c in json.loads(Path(__file__).with_name('expected.json').read_text())['cases']}
own_events = json.loads(args.events.read_text())
original = target.event_bytes
captured = []


def record(*arguments):
    raw = original(*arguments)
    captured.append(raw.decode('ascii').rstrip('\n'))
    return raw


target.event_bytes = record
for case in expected:
    captured.clear()
    actual = target.search(2, case['M'], 8, tuple(case['anchors']))
    require(actual == case, 'author manifest changed')
    rows = sorted(captured)
    require(rows == own_events[str(case['M'])], 'a normalized terminal record differs')
    digest = sha256(('\n'.join(rows)+'\n').encode()).hexdigest()
    require(digest == own_expected[case['M']]['sorted_normalized_terminal_sha256'],
            'independent expected record digest differs')
    print(f'PASS M={case["M"]}: all {len(rows)} normalized terminal records match byte-for-byte')
