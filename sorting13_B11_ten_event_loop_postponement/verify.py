"""Independent inverse/full13/scalar check of the postponement certificate.

Author: six-sorting-2, researcher. Does not import the new forward source.
"""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import resource
import time

HERE = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':'), sort_keys=True).encode()).hexdigest()


def scalar(values, gates):
    values = list(values)
    for a, b in gates:
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values


def verify():
    start = time.monotonic()
    dependency = json.loads((HERE / 'dependencies.json').read_text())
    for entry in dependency['pinned_files']:
        assert hashlib.sha256((HERE.parent / entry['path']).read_bytes()).hexdigest() == entry['sha256']
    certificate = json.loads((HERE / 'certificate.json').read_text())
    fixture = json.loads((HERE.parent / 'sorting13_B11_ten_event_matching_dags/fixture.json').read_text())
    activity = json.loads((HERE.parent / 'sorting13_B11_pruning_saturation_activity/certificate.json').read_text())
    spec = importlib.util.spec_from_file_location('parent_inverse', HERE.parent / 'sorting13_B11_ten_event_matching_dags/verify.py')
    inverse = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(inverse)
    initial, target, nodes, outgoing, edge_set = inverse.independent_profiles(fixture)
    # Recover the B11 image and known45 control directly from every original input.
    B11 = set()
    for row in range(8192):
        bits = [row >> j & 1 for j in range(13)]
        after = scalar(bits, fixture['prefix22'])
        assert after[0] == min(bits) and after[12] == max(bits)
        B11.add(sum(after[j + 1] << j for j in range(11)))
        full_control = fixture['prefix22'] + [[a + 1, b + 1] for a, b in fixture['B11_known23_control']]
        assert scalar(bits, full_control) == sorted(bits)
    assert sorted(B11) == fixture['B11_states']
    # Rebuild every mandatory clamped slice without importing its claimed rows.
    domains = []
    clamped = 0
    for family in activity['families']:
        if family['final_D'] != 9:
            continue
        for claimed, pair in zip(family['domains'], family['original_representatives']):
            free = [j for j in range(13) if j not in pair]
            domain = set()
            for mask in range(2048):
                bits = [0] * 13
                for j, wire in enumerate(free):
                    bits[wire] = mask >> j & 1
                for wire in pair:
                    bits[wire] = int(family['mode'] == 'max')
                after = scalar(bits, fixture['prefix22'])
                domain.add(sum(after[j + 1] << j for j in range(11)))
                clamped += 1
            assert sorted(domain) == claimed
            domains.append((family['mode'], family['partner'], pair, sorted(domain)))
    assert len(domains) == 12
    allrecords = []
    loops = controls = 0
    random_source = random.Random(230916)
    for record in inverse.independent_factors():
        _, graph = inverse.audit_class(record, initial, target, outgoing)
        profiles = {mask: state for mask, state in graph['profiles']}
        edges = graph['edges']
        labels = tuple(map(tuple, record['labels']))
        choices = {mask: {} for mask in profiles}
        for mask, gate, destination in edges:
            gate = tuple(gate)
            choices[mask][gate] = destination
            support = {i for i in range(11) if profiles[mask][0][i] or profiles[mask][1][i]}
            if destination == mask:
                future = {i for j, event in enumerate(labels) if not (mask >> j & 1) for i in event}
                assert set(gate).isdisjoint(future)
                loops += 1
            else:
                assert set(gate) <= support
                next_support = {i for i in range(11) if profiles[destination][0][i] or profiles[destination][1][i]}
                assert next_support <= support
        # Verify the pairwise-disjoint incomparable labels from the actual ideal sets.
        masks = list(profiles)
        for i in range(10):
            for j in range(i + 1, 10):
                if any(m >> i & 1 and not (m >> j & 1) for m in masks) and any(m >> j & 1 and not (m >> i & 1) for m in masks):
                    assert set(labels[i]).isdisjoint(labels[j])
        image = set()
        for row in B11:
            after = scalar([row >> j & 1 for j in range(11)], labels)
            assert after[0] == int(row == 2047) and after[10] == int(row != 0)
            image.add(sum(after[j + 1] << j for j in range(9)))
        obstacles = []
        for mode, partner, pair, domain in domains:
            current = partner
            rows = [[row >> j & 1 for j in range(11)] for row in domain]
            for event, (a, b) in enumerate(labels):
                if current not in (a, b) and not any(bits[a] > bits[b] for bits in rows):
                    masks_before = sorted({sum(v << j for j, v in enumerate(bits)) for bits in rows})
                    obstacles.append(dict(event=event, gate=[a, b], mode=mode, partner=partner,
                                          original=pair, route_before=current,
                                          slice_before_sha256=digest(masks_before)))
                rows = [scalar(bits, [(a, b)]) for bits in rows]
                if current in (a, b):
                    current = b if mode == 'max' else a
        allrecords.append(dict(code=record['code'], partner=record['first10_partner'], kind=record['kind'],
                               events=labels, image9=sorted(image), obstacles=obstacles))
        # Exercise actual22-slot interleavings; the all-real proof is disjointness.
        mask = 0
        word = []
        loopword = []
        for t in range(22):
            options = [(gate, dest) for gate, dest in choices[mask].items()
                       if dest != mask or 10 - mask.bit_count() < 22 - t]
            gate, dest = random_source.choice(options)
            word.append(gate)
            if dest == mask:
                loopword.append(gate)
            mask = dest
        assert mask == 1023 and len(loopword) == 12
        for row in B11:
            bits = [row >> j & 1 for j in range(11)]
            assert scalar(bits, word) == scalar(bits, list(labels) + loopword)
            controls += 1
    allrecords.sort(key=lambda r: int(r['code']))
    assert len(allrecords) == 135 and loops == certificate['loop_future_disjointness_cases'] == 82305
    assert digest([[r['code'], r['obstacles']] for r in allrecords]) == certificate['all_obstacles_sha256']
    kept = [r for r in allrecords if r['partner'] != 4]
    images = sorted({tuple(r['image9']) for r in kept}, key=lambda r: (len(r), r))
    assert [list(r) for r in images] == certificate['images9']
    indexes = {image: i for i, image in enumerate(images)}
    minimal = [i for i, r in enumerate(images) if not any(set(s) < set(r) for s in images)]
    assert minimal == certificate['minimal_image_ids'] and len(minimal) == 106
    normalized = []
    for record in kept:
        normalized.append(dict(code=record['code'], partner=record['partner'], kind=record['kind'],
                               events=record['events'], image_id=indexes[tuple(record['image9'])],
                               minimal_image_id=next(i for i in minimal if set(images[i]) <= set(record['image9'])),
                               obstruction=record['obstacles'][0] if record['obstacles'] else None))
    assert json.loads(json.dumps(normalized)) == certificate['classes']
    assert {str(k): v for k, v in Counter(len(r['obstacles']) for r in kept).items()} == certificate['activity_obstacle_histogram']
    remaining = [r for r in kept if not r['obstacles']]
    remaining_images = sorted({indexes[tuple(r['image9'])] for r in remaining})
    remaining_minimal = [i for i in remaining_images if not any(set(images[j]) < set(images[i]) for j in remaining_images)]
    assert remaining_images == certificate['remaining_image_ids'] and len(remaining_images) == 89
    assert remaining_minimal == certificate['remaining_minimal_image_ids'] and len(remaining_minimal) == 88
    assert len(kept) == 108 and len(remaining) == 90
    # Every published obstruction is checked again with actual marked values.
    actual_checks = 0
    for record in normalized:
        obstacle = record['obstruction']
        if obstacle is None:
            continue
        pair = obstacle['original']
        free = [j for j in range(13) if j not in pair]
        before_word = fixture['prefix22'] + [[a + 1, b + 1] for a, b in record['events'][:obstacle['event']]]
        a, b = [p + 1 for p in obstacle['gate']]
        for mask in range(2048):
            bits = [0] * 13
            for j, wire in enumerate(free):
                bits[wire] = mask >> j & 1
            bits[pair[0]], bits[pair[1]] = (2, 3) if obstacle['mode'] == 'max' else (-2, -1)
            after = scalar(bits, before_word)
            assert after[a] in (0, 1) and after[b] in (0, 1)
            assert after[a] <= after[b]
            actual_checks += 1
    parent_cert = json.loads((HERE.parent / 'sorting13_B11_ten_event_matching_dags/certificate.json').read_text())
    codes = {str(row[0]) for row in parent_cert['filtered_table']}
    assert {r['code'] for r in normalized} <= codes
    assert certificate['peer_repeated_exclusion_code'] in codes
    assert certificate['peer_repeated_exclusion_code'] not in {r['code'] for r in normalized}
    assert certificate['combined_classes'] == dict(ten_distinct=90, eleven_distinct=297, eleven_repeated=47, total=434)
    return dict(agent='six-sorting-2', role='researcher', status='INDEPENDENT_POSTPONEMENT_AND_18_OBSTRUCTIONS_VERIFIED',
                parent_states=len(nodes), parent_edges=len(edge_set), parent_ten_graphs=135,
                ten_classes=108, loop_future_disjointness_cases=loops, sampled_interleavings=135,
                scalar_function_checks=controls, reconstructed_clamped_inputs=clamped,
                actual_marked_obstruction_inputs=actual_checks, excluded=18, remaining=90,
                remaining_images=89, remaining_minimal_images=88, combined_classes=434,
                certificate_sha256=hashlib.sha256((HERE / 'certificate.json').read_bytes()).hexdigest(),
                seconds=time.monotonic() - start, peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                trust='Same-researcher independent algorithms; published parents and written coverage/pruning bridges imported')


if __name__ == '__main__':
    assert __debug__, 'Assertions are required'
    print(json.dumps(verify(), indent=2))
