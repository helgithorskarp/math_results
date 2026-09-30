"""Exact ten-event loop postponement and fixed-prefix activity certificate.

Author: six-sorting-2, researcher. Uses pinned published parent algorithms.
All arithmetic is exact; no solver is used by this proof computation.
"""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':'), sort_keys=True).encode()).hexdigest()


def load_parent(name, path):
    dependency = json.loads((HERE / 'dependencies.json').read_text())
    for entry in dependency['pinned_files']:
        assert hashlib.sha256((HERE.parent / entry['path']).read_bytes()).hexdigest() == entry['sha256']
    spec = importlib.util.spec_from_file_location(name, HERE.parent / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scalar(row, gates):
    for a, b in gates:
        if row >> a & 1 and not row >> b & 1:
            row ^= (1 << a) | (1 << b)
    return row


def compute():
    parent = load_parent('parent_forward', 'sorting13_B11_ten_event_matching_dags/generate.py')
    fixture = json.loads((HERE.parent / 'sorting13_B11_ten_event_matching_dags/fixture.json').read_text())
    families = json.loads((HERE.parent / 'sorting13_B11_pruning_saturation_activity/certificate.json').read_text())['families']
    peer = json.loads((HERE.parent / 'sorting_networks/thirteen_repeated01_activity_exclusion/certificate.json').read_text())
    peer_codes = sorted([r['class_code'] for r in peer['classes']], key=int)
    assert len(peer_codes) == len(set(peer_codes)) == 18
    records = []
    loops = 0
    for record in parent.matching_candidates(True):
        labels = tuple(map(tuple, record['labels']))
        profiles, choices, _ = parent.ideal_graph(fixture, record)
        ancestors = list(record['predecessor_masks'])
        for j in range(10):
            for i in range(j):
                if ancestors[j] >> i & 1:
                    ancestors[j] |= ancestors[i]
        for i in range(10):
            for j in range(i + 1, 10):
                if not (ancestors[j] >> i & 1):
                    assert set(labels[i]).isdisjoint(labels[j])
        for mask, state in profiles.items():
            occupied = {i for i in range(11) if state[0][i] or state[1][i]}
            future = {i for j, gate in enumerate(labels) if not (mask >> j & 1) for i in gate}
            assert future <= occupied
            for gate, destination in choices[mask].items():
                if destination == mask:
                    assert set(gate).isdisjoint(future)
                    loops += 1
                else:
                    assert set(gate) <= occupied
                    after = profiles[destination]
                    assert {i for i in range(11) if after[0][i] or after[1][i]} <= occupied
        image = []
        for row in fixture['B11_states']:
            out = scalar(row, labels)
            assert (out & 1) == int(row == 2047)
            assert (out >> 10 & 1) == int(row != 0)
            image.append(out >> 1 & 511)
        obstacles = []
        for family in families:
            if family['final_D'] != 9:
                continue
            for domain, original in zip(family['domains'], family['original_representatives']):
                rows = domain.copy()
                partner = family['partner']
                for event, (a, b) in enumerate(labels):
                    if partner not in (a, b) and not any(row >> a & 1 and not row >> b & 1 for row in rows):
                        obstacles.append(dict(event=event, gate=[a, b], mode=family['mode'],
                                              partner=family['partner'], original=original,
                                              route_before=partner, slice_before_sha256=digest(sorted(set(rows)))))
                    rows = [scalar(row, [(a, b)]) for row in rows]
                    if partner in (a, b):
                        partner = b if family['mode'] == 'max' else a
        records.append(dict(code=record['code'], partner=record['first10_partner'], kind=record['kind'],
                            events=labels, image9=sorted(set(image)), obstacles=obstacles))
    records.sort(key=lambda r: int(r['code']))
    kept = [r for r in records if r['partner'] != 4]
    images = sorted({tuple(r['image9']) for r in kept}, key=lambda r: (len(r), r))
    image_index = {image: i for i, image in enumerate(images)}
    minimum = [i for i, image in enumerate(images) if not any(set(other) < set(image) for other in images)]
    remaining = [r for r in kept if not r['obstacles']]
    remaining_images = sorted({image_index[tuple(r['image9'])] for r in remaining})
    remaining_minimum = [i for i in remaining_images if not any(set(images[j]) < set(images[i]) for j in remaining_images)]
    classes = [dict(code=r['code'], partner=r['partner'], kind=r['kind'], events=r['events'],
                    image_id=image_index[tuple(r['image9'])],
                    minimal_image_id=next(i for i in minimum if set(images[i]) <= set(r['image9'])),
                    obstruction=r['obstacles'][0] if r['obstacles'] else None) for r in kept]
    output = dict(schema='sorting13-ten-loop-postponement-v1', agent='six-sorting-2', role='researcher',
                  parent_ten_classes=135, first4_removed=27, surviving_ten_classes=108,
                  loop_future_disjointness_cases=loops, images9=[list(r) for r in images], classes=classes,
                  distinct_images=107, minimal_image_ids=minimum, activity_excluded_classes=18,
                  activity_obstacle_histogram=dict(sorted(Counter(len(r['obstacles']) for r in kept).items())),
                  all_obstacles_sha256=digest([[r['code'], r['obstacles']] for r in records]),
                  remaining_ten_classes=90, remaining_image_ids=remaining_images,
                  remaining_minimal_image_ids=remaining_minimum, remaining_distinct_images=89,
                  remaining_minimal_images=88,
                  peer_repeated_exclusion_codes=peer_codes,
                  combined_classes=dict(ten_distinct=90, eleven_distinct=297, eleven_repeated=30, total=417),
                  scope='Ten-event reduction and 18 activity obstructions only; peer removes 18 repeated01 classes; no full B11 exclusion')
    assert len(records) == 135 and len(kept) == 108 and loops == 82305
    assert len(images) == 107 and len(minimum) == 106
    assert len(remaining) == 90 and len(remaining_images) == 89 and len(remaining_minimum) == 88
    assert sum(bool(r['obstacles']) for r in kept) == 18
    return output


if __name__ == '__main__':
    assert __debug__, 'Assertions are required'
    start = time.monotonic()
    certificate = json.loads((HERE / 'certificate.json').read_text())
    computed = json.loads(json.dumps(compute()))
    assert computed == certificate
    print(json.dumps(dict(agent='six-sorting-2', role='researcher', status='POSTPONEMENT_AND_18_ACTIVITY_CERTIFICATE_VERIFIED',
                          ten_classes=108, disjointness_cases=82305, excluded=18, remaining=90,
                          images=107, minimal_images=106, remaining_images=89, remaining_minimal_images=88,
                          certificate_sha256=hashlib.sha256((HERE / 'certificate.json').read_bytes()).hexdigest(),
                          seconds=time.monotonic() - start)))
