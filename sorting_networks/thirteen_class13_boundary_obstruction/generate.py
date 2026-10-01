"""Produce the five compact boundary-touch obstructions, with exact inputs.

six-sorting-1, researcher. Python3.11+, standard library, no solver.
The complete class reduction is an imported, explicitly pinned premise.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
GATES = tuple(itertools.combinations(range(11), 2))
PARENT_HASHES = {
    'fixture.json': 'bf67cd5f265cc91cfd4be7fb39fb4b67df303475437aea575a167320545400ff',
    'certificate.json': '549ee24718640e588fc9701d85c63869ec2c7b8e22f40cecac3310f0759c3f9a',
}
CLASS_CODE = '349871875148001158693749134458897'
PLANS = {0: (2, 499), 1: (1, 509), 8: (2, 506), 16: (1, 509), 18: (1, 509)}


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def replay(x, gates):
    touches = 0
    for a, b in gates:
        left, right = (x >> a) & 1, (x >> b) & 1
        touches += not (left and right)
        if left > right:
            x ^= (1 << a) | (1 << b)
    return x, touches


def reconstruct_prefix(parent, certificate, case_id):
    triple_id, function_id, image_id, budget = certificate['class13']['local_map_cases'][case_id]
    before_ids, first_id, after_ids, _ = certificate['class13']['triples'][triple_id]
    before = [GATES[g] for g in before_ids]
    low, high = list(parent['initial_low']), list(parent['initial_high'])
    for a, b in before:
        low[a], low[b] = 2 * max(low[a], low[b]), 0
        high[a], high[b] = 0, 2 * max(high[a], high[b])
    empty = [i for i in range(11) if not low[i] and not high[i]]
    local = tuple(itertools.combinations(empty, 2))
    labels = certificate['local_monoids'][len(empty) - 1]['representative_words'][function_id]
    preparation = [local[label] for label in labels]
    word = before + preparation + [GATES[first_id]] + [GATES[g] for g in after_ids]
    assert len(word) + budget == 22
    return [list(g) for g in word], preparation, image_id, budget


def main():
    assert not sys.flags.optimize, 'Run with assertions enabled'
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', type=Path, default=HERE.parent / 'thirteen_single_preparation_normal_form')
    args = parser.parse_args()
    loaded = {}
    for name, sha in PARENT_HASHES.items():
        data = (args.parent / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == sha, (name, 'wrong parent bytes')
        loaded[name] = json.loads(data)
    parent, certificate = loaded['fixture.json'], loaded['certificate.json']
    assert parent['class_code'] == CLASS_CODE
    cases, obstructions = [], []
    pairs = certificate['class13']['remaining_completion_pairs']
    assert [image for image, budget, case in pairs] == sorted(PLANS)
    for image, budget, case in pairs:
        prefix, prep, check_image, check_budget = reconstruct_prefix(parent, certificate, case)
        assert (check_image, check_budget) == (image, budget)
        full = parent['prefix22'] + [[a + 1, b + 1] for a, b in prefix]
        preimages = {}
        for x in range(8192):
            out, _ = replay(x, full)
            row = (out >> 2) & 511
            preimages.setdefault(row, x)
        rows = sorted(preimages)
        assert rows == certificate['class13']['images9'][image]
        k, cut_row = PLANS[image]
        control_input = 2303 if k == 2 else 2015
        control_out, spent = replay(control_input, full)
        control_row = 511 ^ ((1 << k) - 1)
        assert (control_out >> 2) & 511 == control_row
        free = control_input.bit_count()
        lower = {9: 25, 10: 29}[free]
        cap = 44 - lower - spent
        zeros_in_K = k - (cut_row & ((1 << k) - 1)).bit_count()
        required_crossings = min(k, 9 - cut_row.bit_count()) - zeros_in_K
        forced_internal = int(k == 2)
        assert required_crossings + forced_internal > cap
        assert cut_row in rows and (k == 1 or 509 in rows)
        record = {'parent_image_id': image, 'parent_case_id': case,
                  'rows9': rows, 'tail_budget': budget, 'prefix_B11': prefix,
                  'preparation_word': [list(g) for g in prep]}
        cases.append(record)
        obstructions.append({
            'parent_image_id': image, 'parent_case_id': case,
            'boundary_ports9': list(range(k)), 'control_original_mask13': control_input,
            'marked_original_ports13': [i for i in range(13) if not control_input >> i & 1],
            'unmarked_inputs': free, 'imported_size_lower_bound': lower,
            'control_row9': control_row, 'prefix_marked_passages': spent,
            'remaining_boundary_touch_cap': cap, 'cut_row9': cut_row,
            'cut_original_mask13': preimages[cut_row], 'required_cut_crossings': required_crossings,
            'forced_internal_gate9': [0, 1] if k == 2 else None,
            'forced_internal_row9': 509 if k == 2 else None,
            'forced_internal_original_mask13': preimages[509] if k == 2 else None,
            'required_boundary_touches': required_crossings + forced_internal,
        })
    fixture = {'schema': 'sorting13-class13-boundary-fixture-v1',
               'agent': 'six-sorting-1', 'role': 'researcher', 'class_code': CLASS_CODE,
               'parent_source_commit': '9e233924e79cc8a4b52001cda87cc8f56db3003c',
               'parent_file_sha256': PARENT_HASHES, 'prefix22': parent['prefix22'],
               'B11_states': parent['B11_states'],
               'B11_known23_control': parent['B11_known23_control'], 'cases': cases}
    result = {'schema': 'sorting13-class13-boundary-certificate-v1',
              'agent': 'six-sorting-1', 'role': 'researcher', 'fixture_sha256': digest(fixture),
              'class_code': CLASS_CODE, 'parent_effective_words': 5385,
              'complete_parent_completion_pairs': pairs, 'obstructions': obstructions,
              'scope': 'All five complete class13 residual tails are impossible within their budgets by marked pruning and boundary cut counts.'}
    for name, data in [('fixture.json', fixture), ('certificate.json', result)]:
        path = HERE / name
        if path.exists():
            assert json.loads(path.read_text()) == data, ('generated artifact mismatch', name)
        else:
            path.write_text(json.dumps(data, separators=(',', ':')) + '\n')
    print(json.dumps({'status': 'CLASS13_BOUNDARY_OBSTRUCTIONS_GENERATED',
                      'cases': len(obstructions), 'certificate_sha256': digest(result),
                      'image_touch_cap_required': [[o['parent_image_id'], o['remaining_boundary_touch_cap'],
                                                   o['required_boundary_touches']] for o in obstructions]}))


if __name__ == '__main__':
    main()
