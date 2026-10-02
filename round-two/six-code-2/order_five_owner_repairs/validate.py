"""Reject semantic certificate damage before the final expected-record check.

Each altered fixture is checked in a separate, sequential subprocess. No
certificate hash mismatch is accepted as the reason for rejecting a damage.
"""
import argparse
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    require(not args.work.exists(), 'require a new damage-validation directory')
    args.work.mkdir(parents=True)
    root = Path(__file__).resolve().parent
    begin = time.monotonic()
    four = json.loads((root / 'OWNERS_FOUR.json').read_bytes())
    five = json.loads((root / 'COLORS_FIVE.json').read_bytes())
    maps = json.loads((root / 'POINT_MAPS.json').read_bytes())
    classes = json.loads((root / 'CLASSIFICATION.json').read_bytes())['classes']
    damages = []

    broken = deepcopy(four)
    broken['cases'][0]['owners'].pop()
    damages.append(('missing_four_vertex', '--four', broken,
                    'incomplete or invented radius-four field'))

    broken = deepcopy(five)
    word = broken['cases'][0]['five_blocker_word_owners'][0][0]
    base = classes[0]['representative_words']
    blockers = {i for i, b in enumerate(base) if (word & b).bit_count() >= 3}
    broken['cases'][0]['five_blocker_word_owners'][0][1] = next(i for i in range(68) if i not in blockers)
    damages.append(('invalid_five_owner', '--five', broken,
                    'new-word owner is not a blocker'))

    broken = deepcopy(five)
    broken['cases'][2]['conditional_recolorings'].pop()
    damages.append(('missing_collision_carrier', '--five', broken,
                    'conditional recolorings omit or invent collision carriers'))

    broken = deepcopy(five)
    row = broken['cases'][2]['conditional_recolorings'][0]
    row[2] = dict(four['cases'][2]['owners'])[row[1]]
    damages.append(('ineffective_collision_repair', '--five', broken,
                    'invalid or ineffective recoloring'))

    broken = deepcopy(maps)
    broken[1]['point_map'][0] = broken[1]['point_map'][1]
    damages.append(('nonbijective_point_transport', '--point-maps', broken,
                    'point map is not bijective'))

    # Make a genuine collision while retaining valid blocker labels. This
    # exercises the co-occurrence condition on literal outside vertices.
    broken = deepcopy(four)
    carrier = {w: {i for i, b in enumerate(base) if (w & b).bit_count() >= 3}
               for w, _ in broken['cases'][0]['owners']}
    pair = next((a, b) for a, b in combinations(sorted(carrier), 2)
                if (a & b).bit_count() <= 2 and
                len(carrier[a] | carrier[b]) <= 4 and carrier[a] & carrier[b])
    shared = min(carrier[pair[0]] & carrier[pair[1]])
    for row in broken['cases'][0]['owners']:
        if row[0] in pair:
            row[1] = shared
    damages.append(('valid_labels_with_compatible_collision', '--four', broken,
                    'radius-four ownership collision'))

    broken = deepcopy(five)
    broken['cases'][0]['five_blocker_word_owners'].pop()
    damages.append(('missing_five_vertex', '--five', broken,
                    'incomplete or invented five-blocker word assignments'))

    results = []
    for name, flag, fixture, rejection in damages:
        require(time.monotonic() - begin < 60, 'INCOMPLETE initial 60-second validation guard')
        path = args.work / (name + '.json')
        path.write_text(json.dumps(fixture, sort_keys=True, separators=(',', ':')) + '\n')
        command = [sys.executable, '-B', str(root / 'verify.py'),
                   flag, str(path), '--work', str(args.work / (name + '-run'))]
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        require(result.returncode != 0 and rejection in result.stderr and
                'whole exact record differs' not in result.stderr,
                'damage not rejected semantically: ' + name)
        results.append({'damage': name, 'rejection': rejection})
    record = {'agent': 'six-code-2', 'role': 'researcher',
              'status': 'ALL_SEVEN_LITERAL_CERTIFICATE_DAMAGES_REJECTED_SEMANTICALLY',
              'damage_rejections': results, 'sequential_checker_processes': len(results),
              'initial_whole_guard_seconds': 60, 'checker_process_timeout_seconds': 10,
              'seconds': time.monotonic() - begin}
    (args.work / 'VALIDATION.json').write_text(json.dumps(record, sort_keys=True, indent=2) + '\n')
    print(json.dumps(record, sort_keys=True))


if __name__ == '__main__':
    main()
