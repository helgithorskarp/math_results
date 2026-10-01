"""Original-input and actual distinct-marker audits; imports no generator/solver."""
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOWER = (0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39)


def sha(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def replay(values, gates):
    values, spent = list(values), [0, 0]
    for a, b in gates:
        operands = values[a], values[b]
        spent[0] += 0 in operands
        spent[1] += 1 in operands
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values, spent


def check_parent(fixture, path):
    assert hashlib.sha256((path / 'fixture.json').read_bytes()).hexdigest() == fixture['parent_fixture_sha256']
    assert hashlib.sha256((path / 'reduction.json').read_bytes()).hexdigest() == fixture['parent_certificate_sha256']
    other = json.loads((path / 'fixture.json').read_text())
    parent = json.loads((path / 'reduction.json').read_text())
    assert other['repeated_effective_gates'] == [[1,4],[2,4],[3,4]]
    for field in ('prefix22', 'B11_states', 'B11_known23_control'):
        assert fixture[field] == other[field]
    assert fixture['tails'] == parent['remaining_tails']
    assert [(r['parent_index'],r['image'],r['budget']) for r in fixture['tails']] == [
        (195,8,10),(195,14,9),(199,0,11),(199,21,9),
        (283,9,10),(283,18,9),(287,10,10),(287,19,9)]


def actual_marker_check(prefix, witness, polarity, spent, counter):
    """Every free Boolean assignment with distinct constant extreme labels."""
    marked = [i for i in range(13) if (witness >> i & 1) == polarity]
    free = [i for i in range(13) if i not in marked]
    labels = list(range(2, 2 + len(marked))) if polarity else list(range(-len(marked), 0))
    constants = dict(zip(marked, labels))
    constants_set = set(labels)
    membership, _ = replay([(witness >> i) & 1 for i in range(13)], prefix)
    expected = {i for i, v in enumerate(membership) if v == polarity}
    for assignment in range(1 << len(free)):
        row = [None] * 13
        for i, v in constants.items():
            row[i] = v
        for bit, port in enumerate(free):
            row[port] = assignment >> bit & 1
        charged = 0
        for a, b in prefix:
            charged += row[a] in constants_set or row[b] in constants_set
            if row[a] > row[b]:
                row[a], row[b] = row[b], row[a]
        assert charged == spent
        assert {i for i, v in enumerate(row) if v in constants_set} == expected
        counter['actual_marked_free_assignments'] += 1


def local_cut_controls():
    pairs = list(itertools.combinations(range(9), 2))
    count = 0
    for polarity, cut, singleton, sorted_singleton in [(0, {0, 1}, 509, 510), (1, {7, 8}, 128, 256)]:
        internal = tuple(sorted(cut))
        for integer in range(512):
            row = [(integer >> i) & 1 for i in range(9)]
            before = sum(row[i] == polarity for i in cut)
            for a, b in pairs:
                output, _ = replay(row, [(a, b)])
                after = sum(output[i] == polarity for i in cut)
                touched = row[a] == polarity or row[b] == polarity
                assert before <= after <= before + 1
                crossing = len({a, b} & cut) == 1
                if not crossing:
                    assert before == after
                if after > before:
                    assert crossing and touched
                if (a, b) == internal and before >= 1:
                    assert touched
                count += 1
        row = [(singleton >> i) & 1 for i in range(9)]
        for gate in pairs:
            result, _ = replay(row, [gate])
            actual = sum(v << i for i, v in enumerate(result))
            assert actual == (sorted_singleton if gate == internal else singleton)
    return {'moving_cut_truth_checks': count, 'mandatory_gate_truth_checks': 72}


def audit_data(fixture, data, certificate):
    counter = dict(original_prefix_inputs=0, actual_marked_free_assignments=0, B11_prefix_inputs=0)
    base_images = set()
    full45 = fixture['prefix22'] + [[a + 1, b + 1] for a, b in fixture['B11_known23_control']]
    assert len(full45) == 45
    for original in range(8192):
        values = [(original >> i) & 1 for i in range(13)]
        output, _ = replay(values, fixture['prefix22'])
        assert output[0] == min(values) and output[12] == max(values)
        base_images.add(sum(v << i for i, v in enumerate(output[1:12])))
        sorted_output, spent = replay(values, full45)
        assert sorted_output == sorted(values)
        if original not in (0, 8191):
            for p in (0, 1):
                free = sum(v != p for v in values)
                assert spent[p] <= 45 - LOWER[free]
    assert sorted(base_images) == fixture['B11_states']
    assert len(base_images) == 158
    assert [(r['record']['parent_index'], r['record']['image']) for r in data['instances']] == [
        (195,8),(195,14),(199,0),(199,21),(283,9),(283,18),(287,10),(287,19)]
    sat_pairs = {(r['parent_index'], r['image']) for r in certificate['records']}
    assert sat_pairs == {(199,0)} and len(certificate['records']) == 1
    assert certificate['boundary_instances'] == [[195,8],[195,14],[199,21],[283,9],[283,18],[287,10],[287,19]]
    marker_controls = set()
    original_images = {}
    for target, instance in zip(fixture['tails'], data['instances']):
        assert instance['record'] == target
        assert sha(target['rows9']) == target['rows9_sha256']
        prefix = fixture['prefix22'] + [[a + 1, b + 1] for a, b in target['prefix_B11']]
        assert prefix == instance['prefix13'] and len(prefix) + target['budget'] == 44
        pair = target['parent_index'], target['image']
        pool, images, preimages = {}, set(), {}
        for original in range(8192):
            values = [(original >> i) & 1 for i in range(13)]
            output, spent = replay(values, prefix)
            ordered = sorted(values)
            assert [output[i] for i in (0, 1, 11, 12)] == [ordered[i] for i in (0, 1, 11, 12)]
            middle = sum(v << i for i, v in enumerate(output[2:11]))
            images.add(middle)
            preimages.setdefault(middle, original)
            counter['original_prefix_inputs'] += 1
            if original in (0, 8191):
                continue
            for p in (0, 1):
                free = sum(v != p for v in values)
                limit = 44 - LOWER[free] - spent[p]
                key = middle, p
                if key not in pool or limit < pool[key][0]:
                    pool[key] = limit, original, free, spent[p]
        caps = [[r, p, *pool[r, p]] for r, p in sorted(pool)]
        assert caps == instance['caps'] and sha(caps) == instance['caps_sha256']
        assert sorted(images) == target['rows9']
        original_images[pair] = (prefix, pool, preimages)
        for original in fixture['B11_states']:
            output, _ = replay([(original >> i) & 1 for i in range(11)], target['prefix_B11'])
            ordered = sorted([(original >> i) & 1 for i in range(11)])
            assert output[0] == ordered[0] and output[10] == ordered[10]
            assert sum(v << i for i, v in enumerate(output[1:10])) in images
            counter['B11_prefix_inputs'] += 1
        if pair in sat_pairs:
            for row, p, cap, witness, free, spent in caps:
                if cap < target['budget']:
                    key = tuple(map(tuple, prefix)), witness, p
                    if key not in marker_controls:
                        actual_marker_check(prefix, witness, p, spent, counter)
                        marker_controls.add(key)
    assert len(fixture['boundary_certificates']) == 7
    assert [(b['parent_index'],b['image']) for b in fixture['boundary_certificates']] == [tuple(p) for p in certificate['boundary_instances']]
    for boundary in fixture['boundary_certificates']:
        pair = boundary['parent_index'], boundary['image']
        assert pair in {(195,8),(195,14),(199,21),(283,9),(283,18),(287,10),(287,19)}
        prefix, pool, preimages = original_images[pair]
        row, p = boundary['row'], boundary['polarity']
        cap, witness, free, spent = pool[row, p]
        assert (cap, witness, free, spent) == (boundary['touch_cap'], boundary['original_witness'],
                                               boundary['free_inputs'], boundary['prefix_passages'])
        assert p in (0,1) and free == 9 and cap == 44 - LOWER[free] - spent
        cut = {0,1} if p == 0 else {7,8}
        assert boundary['cut'] == boundary['mandatory_gate'] == sorted(cut)
        total = sum((row >> i & 1) == p for i in range(9))
        present = sum((row >> i & 1) == p for i in cut)
        deficit = min(2, total) - present
        assert present == boundary['initial_cut_marks'] == 1 and total == boundary['total_middle_marks'] == 2
        assert deficit == boundary['crossing_deficit'] == 1
        assert boundary['required_touches'] == deficit + 1 == 2 > cap
        forced = 509 if p == 0 else 128
        assert boundary['mandatory_row'] == forced and forced in preimages
        actual_marker_check(prefix, witness, p, spent, counter)
    counter.update(local_cut_controls())
    counter.update(known45_original_inputs=8192, base_image_original_inputs=8192,
                   pooled_caps=sum(len(r['caps']) for r in data['instances']),
                   status='ALL_LITERAL_IMAGES_PRUNING_CAPS_AND_MOVING_CUTS_INDEPENDENTLY_VERIFIED')
    return counter
