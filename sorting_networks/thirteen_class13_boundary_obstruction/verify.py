"""Independent scalar, marker/free, and local-cut certificate checker.

No generator, SAT solver, or native library is imported. Class coverage
is explicitly imported from the pinned parent reduction, not re-proved.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PARENT_HASHES = {
    'fixture.json': 'bf67cd5f265cc91cfd4be7fb39fb4b67df303475437aea575a167320545400ff',
    'certificate.json': '549ee24718640e588fc9701d85c63869ec2c7b8e22f40cecac3310f0759c3f9a',
}
CLASS_CODE = '349871875148001158693749134458897'


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def simulate(values, word):
    values = list(values)
    marked_passages = 0
    for a, b in word:
        marked_passages += values[a] < 0 or values[b] < 0
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values, marked_passages


def boolean_input(row, n):
    return [int(bool(row & (1 << i))) for i in range(n)]


def encode(values):
    return sum(int(v) << i for i, v in enumerate(values))


def independent_prefix(parent, cert, case_id):
    triples = cert['class13']['triples']
    ti, mi, image, budget = cert['class13']['local_map_cases'][case_id]
    gates = tuple(itertools.combinations(range(11), 2))
    before, first, after, count = triples[ti]
    # Propagate labelled support sets, rather than weighted profile recurrences.
    small = [{i} if w else set() for i, w in enumerate(parent['initial_low'])]
    large = [{i} if w else set() for i, w in enumerate(parent['initial_high'])]
    for label in before:
        a, b = gates[label]
        small[a], small[b] = small[a] | small[b], set()
        large[a], large[b] = set(), large[a] | large[b]
    empty_ports = [i for i in range(11) if not small[i] and not large[i]]
    local_pairs = tuple(itertools.combinations(range(len(empty_ports)), 2))
    labels = cert['local_monoids'][len(empty_ports) - 1]['representative_words'][mi]
    prep = [[empty_ports[local_pairs[g][0]], empty_ports[local_pairs[g][1]]] for g in labels]
    word = [list(gates[g]) for g in before] + prep + [list(gates[first])] + [list(gates[g]) for g in after]
    return word, prep, image, budget


def check_local_cut_facts():
    checks = 0
    for k in (1, 2):
        marked_row = [0] * k + [1] * (9 - k)
        for row in range(512):
            values = boolean_input(row, 9)
            before = values[:k].count(0)
            for gate in itertools.combinations(range(9), 2):
                a, b = gate
                control, _ = simulate(marked_row, [gate])
                assert control == marked_row
                output, _ = simulate(values, [gate])
                crossing = a < k <= b
                change = output[:k].count(0) - before
                assert 0 <= change <= int(crossing)
                checks += 1
    one_zero_at_1 = [1, 0] + [1] * 7
    for gate in itertools.combinations(range(9), 2):
        output, _ = simulate(one_zero_at_1, [gate])
        if gate == (0, 1):
            assert output == [0] + [1] * 8
        else:
            assert output == one_zero_at_1
    return checks, 36


def check(fixture, certificate, parent_dir):
    assert fixture['class_code'] == certificate['class_code'] == CLASS_CODE
    assert certificate['fixture_sha256'] == digest(fixture)
    assert fixture['parent_file_sha256'] == PARENT_HASHES
    parent_data = {}
    for name, sha in PARENT_HASHES.items():
        raw = (parent_dir / name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == sha, (name, 'parent source mismatch')
        parent_data[name] = json.loads(raw)
    parent, inherited = parent_data['fixture.json'], parent_data['certificate.json']
    assert parent['class_code'] == CLASS_CODE
    for field in ('prefix22', 'B11_states', 'B11_known23_control'):
        assert fixture[field] == parent[field]
    pairs = inherited['class13']['remaining_completion_pairs']
    assert len(pairs) == 5 and certificate['complete_parent_completion_pairs'] == pairs
    assert certificate['parent_effective_words'] == inherited['class13']['effective_words'] == 5385
    assert [(c['parent_image_id'], c['tail_budget'], c['parent_case_id']) for c in fixture['cases']] == [tuple(p) for p in pairs]
    assert len(certificate['obstructions']) == 5
    assert [(o['parent_image_id'], o['parent_case_id']) for o in certificate['obstructions']] == [(p[0], p[2]) for p in pairs]
    base_image = set()
    for x in range(8192):
        out, _ = simulate(boolean_input(x, 13), fixture['prefix22'])
        assert out[0] == int(x == 8191) and out[12] == int(x != 0)
        base_image.add(encode(out[1:12]))
    assert sorted(base_image) == fixture['B11_states']
    masks_checked, marker_assignments, rows_checked = 0, 0, 0
    summaries = []
    for case, obstruction in zip(fixture['cases'], certificate['obstructions']):
        image, ci, budget = case['parent_image_id'], case['parent_case_id'], case['tail_budget']
        word, prep, pi, pb = independent_prefix(parent, inherited, ci)
        assert (pi, pb) == (image, budget)
        assert case['prefix_B11'] == word and case['preparation_word'] == prep
        assert len(word) + budget == 22
        full = fixture['prefix22'] + [[a + 1, b + 1] for a, b in word]
        images = set()
        for x in range(8192):
            out, _ = simulate(boolean_input(x, 13), full)
            sorted_output = sorted(boolean_input(x, 13))
            assert out[:2] == sorted_output[:2] and out[11:] == sorted_output[11:]
            images.add(encode(out[2:11]))
            masks_checked += 1
        assert sorted(images) == case['rows9'] == inherited['class13']['images9'][image]
        scalar11 = {encode(simulate(boolean_input(r, 11), word)[0][1:10]) for r in fixture['B11_states']}
        assert scalar11 == images
        rows_checked += len(fixture['B11_states'])
        K = obstruction['boundary_ports9']
        k = len(K)
        assert k in (1, 2) and K == list(range(k))
        original = obstruction['control_original_mask13']
        marked = [i for i, v in enumerate(boolean_input(original, 13)) if v == 0]
        assert obstruction['marked_original_ports13'] == marked
        assert len(marked) == 2 + k
        free_ports = [i for i in range(13) if i not in marked]
        m = len(free_ports)
        # Established external mathematical premises, never read from a solver.
        lower = {9: 25, 10: 29}[m]
        assert obstruction['unmarked_inputs'] == m and obstruction['imported_size_lower_bound'] == lower
        control, passages = simulate([v - 1 for v in boolean_input(original, 13)], full)
        assert encode([int(v >= 0) for v in control[2:11]]) == obstruction['control_row9'] == 511 ^ ((1 << k) - 1)
        assert {i for i, v in enumerate(control) if v < 0} == set(range(k + 2))
        assert obstruction['prefix_marked_passages'] == passages
        cap = 44 - lower - passages
        assert obstruction['remaining_boundary_touch_cap'] == cap
        # Actual distinct negative marks versus free Boolean assignments. This
        # separately audits marker routes and touched counts, not only bit masks.
        for assignment in itertools.product((0, 1), repeat=m):
            values = [None] * 13
            for order, port in enumerate(marked):
                values[port] = -1 - order
            for port, v in zip(free_ports, assignment):
                values[port] = v
            out, hits = simulate(values, full)
            assert hits == passages
            assert {i for i, v in enumerate(out) if v < 0} == set(range(k + 2))
            marker_assignments += 1
        cut_row = obstruction['cut_row9']
        assert cut_row in images
        cut_input = obstruction['cut_original_mask13']
        out, _ = simulate(boolean_input(cut_input, 13), full)
        assert encode(out[2:11]) == cut_row
        total_zeros = 9 - cut_row.bit_count()
        initial = boolean_input(cut_row, 9)[:k].count(0)
        needed = min(k, total_zeros) - initial
        assert needed > 0 and obstruction['required_cut_crossings'] == needed
        internal = 0
        if k == 2:
            assert obstruction['forced_internal_gate9'] == [0, 1]
            assert obstruction['forced_internal_row9'] == 509 and 509 in images
            forced_input = obstruction['forced_internal_original_mask13']
            out, _ = simulate(boolean_input(forced_input, 13), full)
            assert encode(out[2:11]) == 509
            internal = 1
        else:
            assert all(obstruction[field] is None for field in
                       ('forced_internal_gate9', 'forced_internal_row9', 'forced_internal_original_mask13'))
        assert obstruction['required_boundary_touches'] == needed + internal > cap
        summaries.append([image, len(images), budget, cap, needed + internal])
    local, forced = check_local_cut_facts()
    known = fixture['prefix22'] + [[a + 1, b + 1] for a, b in fixture['B11_known23_control']]
    assert len(known) == 45
    for x in range(8192):
        values = boolean_input(x, 13)
        out, _ = simulate(values, known)
        assert out == sorted(values)
    return {'status': 'INDEPENDENT_CLASS13_BOUNDARY_EXCLUSION_VERIFIED',
            'excluded_complete_classes': 1, 'class13_effective_words': 5385,
            'complete_residual_pairs_excluded': 5, 'original_prefix_input_checks': masks_checked,
            'B11_prefix_row_checks': rows_checked, 'actual_marked_free_assignments': marker_assignments,
            'local_boolean_cut_checks': local, 'mandatory_gate_checks': forced,
            'B11_reconstruction_inputs': 8192, 'known45_control_inputs': 8192,
            'image_rows_budget_touch_cap_required': summaries,
            'certificate_sha256': digest(certificate)}


def main():
    assert not sys.flags.optimize, 'Run with assertions enabled'
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', type=Path, default=HERE.parent / 'thirteen_single_preparation_normal_form')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = parser.parse_args()
    fixture = json.loads((HERE / 'fixture.json').read_text())
    certificate = json.loads(args.certificate.read_text())
    print(json.dumps(check(fixture, certificate, args.parent)))


if __name__ == '__main__':
    main()
