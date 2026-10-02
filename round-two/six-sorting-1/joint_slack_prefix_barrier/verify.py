"""Standalone numeric audit, importing no producer, profiler or solver."""
from copy import deepcopy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
FIXTURE_SHA = '956d91d12d140d1cead9a7f25c77c057055084fa802eac9de0606cdec8f01aa6'
FAMILIES = {'two_minima': (2, 0), 'one_maximum': (0, 1),
            'two_maxima': (0, 2), 'mixed_pair': (1, 1)}
PINS = {'profile.py': 'dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719',
        'anchors.py': '0b95573e7e3c446d0b7ca5352f6b5f4b8d92b91d6f3c72e7b4f783cd99d89902'}


def need(test, message):
    if not test:
        raise ValueError(message)


def numeric_family(word, low_count, high_count):
    records, assignments = [], 0
    for lows in combinations(range(13), low_count):
        other = [p for p in range(13) if p not in lows]
        for highs in combinations(other, high_count):
            free = [p for p in other if p not in highs]
            active = 0
            touches = ports = None
            for x in range(1 << len(free)):
                values = [0] * 13
                for j, p in enumerate(lows):
                    values[p] = j - low_count
                for j, p in enumerate(highs):
                    values[p] = j + 2
                for j, p in enumerate(free):
                    values[p] = x >> j & 1
                touch = 0
                for t, (a, b) in enumerate(word):
                    marked = values[a] < 0 or values[a] > 1 or values[b] < 0 or values[b] > 1
                    if marked:
                        touch |= 1 << t
                    if values[a] > values[b]:
                        if not marked:
                            active |= 1 << t
                        values[a], values[b] = values[b], values[a]
                current = (sum(1 << p for p, v in enumerate(values) if v < 0),
                           sum(1 << p for p, v in enumerate(values) if v > 1))
                if touches is None:
                    touches, ports = touch, current
                need(touch == touches and current == ports, 'mark route depends on a free input')
                assignments += 1
            redundant = ((1 << len(word)) - 1) & ~(touches | active)
            records.append([sum(1 << p for p in lows), sum(1 << p for p in highs), *ports,
                            touches.bit_count(), redundant.bit_count(), redundant])
    records.sort()
    classes = {}
    for _, _, lo, hi, d, r, _ in records:
        old_d, old_c = classes.get((lo, hi), (-1, -1))
        classes[lo, hi] = max(old_d, d), max(old_c, d + r)
    envelope = [[lo, hi, d, c] for (lo, hi), (d, c) in sorted(classes.items())]
    return {'low_count': low_count, 'high_count': high_count, 'records': records, 'envelope': envelope}, assignments


def high_anchor(families):
    selected = {k: v for k, v in families.items() if v['high_count']}
    sizes = {k: 39 if v['low_count'] + v['high_count'] == 1 else 35 for k, v in selected.items()}
    ports = sorted(row[1].bit_length() - 1 for row in families['one_maximum']['envelope'])
    rows = []
    for p in ports:
        masses = {k: sum(1 << row[3] for row in v['envelope'] if row[1] >> p & 1) for k, v in selected.items()}
        label = max(sizes[k] + (mass - 1).bit_length() for k, mass in masses.items() if mass)
        rows.append({'port': p, 'anchored_masses': masses, 'label': label, 'units': 1 << (label - 35)})
    mass = sum(r['units'] for r in rows)
    return {'base': 35, 'normalized_mass': mass, 'lower_bound': 35 + (mass - 1).bit_length(), 'rows': rows}


def event_coverage(leaves):
    output = []
    for a, b in combinations(range(13), 2):
        after = {}
        for p, label in leaves.items():
            values = [0] * 13
            values[p] = 2
            hit = values[a] > 1 or values[b] > 1
            if values[a] > values[b]:
                values[a], values[b] = values[b], values[a]
            q = values.index(2)
            after[q] = max(after.get(q, -1), label + int(hit))
        units = sum(1 << (label - 35) for label in after.values())
        output.append({'gate': [a, b], 'touches_live_high': any(p == a or p == b for p in leaves),
                       'inherited_leaves': [[p, label] for p, label in sorted(after.items())],
                       'inherited_units': units, 'within44_ceiling': units <= 512})
    return output


def compare(packet, stages, coverage):
    need(packet['schema'] == 'changed22-high-first-event-barrier-v1', 'schema differs')
    need(packet['fixture_sha256'] == FIXTURE_SHA and packet['production_dependency_sha256'] == PINS, 'source pins differ')
    need(packet['imported_lower_bounds'] == {'11': 35, '12': 39}, 'imported lower bound differs')
    need(packet['stages'] == stages, 'literal word/original domain/envelope/anchor mismatch')
    need(packet['first_high_gate_coverage'] == coverage, 'complete first-event coverage differs')
    mandatory = [r['gate'] for r in coverage if r['touches_live_high'] and r['within44_ceiling']]
    need(packet['mandatory_first_high_gates'] == mandatory == [[9, 11]], 'compulsory event differs')
    need(packet['prep_gate_count'] == 45 and packet['excluded_live_gate_count'] == 32, 'first-event class counts differ')
    need(packet['E22_total_sorting_size_lower_bound'] == 45, 'claimed lower bound differs')


def main():
    start = time.monotonic()
    raw = (ROOT / 'fixture.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == FIXTURE_SHA, 'pinned literal fixture differs')
    fixture = json.loads(raw)
    B = fixture['native_prefix19'] + fixture['changed_pair']
    need(len(B) == 21 and fixture['changed_pair'] == [[4, 8], [3, 6]], 'earlier patch differs')
    E = B + [[3, 9]]
    words = {'B21': B, 'E22': E, 'E23': E + [[9, 11]]}
    expected_leaves = {'B21': [[9, 41], [11, 42], [12, 43]],
                       'E22': [[9, 42], [11, 42], [12, 43]], 'E23': [[11, 44], [12, 43]]}
    expected_units = {'B21': 448, 'E22': 512, 'E23': 768}
    stages, assignments = [], 0
    for name, word in words.items():
        families = {}
        for family, (l, h) in FAMILIES.items():
            families[family], count = numeric_family(word, l, h)
            assignments += count
        high = high_anchor(families)
        need([[r['port'], r['label']] for r in high['rows']] == expected_leaves[name], 'numeric high leaves differ')
        need(high['normalized_mass'] == expected_units[name], 'numeric saturation differs')
        low = [[r[0], r[2]] for r in families['two_minima']['envelope']]
        stages.append({'name': name, 'literal_word': word, 'families': families,
                       'ordinary_low_envelope': low, 'ordinary_low_mass': sum(1 << r[1] for r in low), 'high_anchor': high})
    leaves = {r['port']: r['label'] for r in stages[1]['high_anchor']['rows']}
    coverage = event_coverage(leaves)
    path = ROOT / 'certificate.json'
    packet = json.loads(path.read_text())
    compare(packet, stages, coverage)
    damages = []
    for index in (4, 5, 6):
        altered = deepcopy(packet)
        altered['stages'][1]['families']['mixed_pair']['records'][0][index] += 1
        damages.append(altered)
    altered = deepcopy(packet); altered['stages'][1]['families']['one_maximum']['records'].pop(); damages.append(altered)
    altered = deepcopy(packet); altered['stages'][1]['high_anchor']['rows'][0]['label'] -= 1; damages.append(altered)
    altered = deepcopy(packet); altered['stages'][2]['high_anchor']['normalized_mass'] = 512; damages.append(altered)
    altered = deepcopy(packet); altered['first_high_gate_coverage'].pop(); damages.append(altered)
    altered = deepcopy(packet); altered['mandatory_first_high_gates'] = [[9, 12]]; damages.append(altered)
    altered = deepcopy(packet); altered['stages'][1]['literal_word'][-1] = [3, 8]; damages.append(altered)
    for altered in damages:
        try:
            compare(altered, stages, coverage)
        except ValueError:
            pass
        else:
            raise ValueError('damaged certificate accepted')
    positive_inputs = 0
    for field, size in (('known45', 45), ('known46', 46)):
        word = fixture[field]
        need(len(word) == size and all(0 <= a < b < 13 for a, b in word), 'known sorter shape differs')
        for x in range(8192):
            values = [x >> p & 1 for p in range(13)]
            for a, b in word:
                if values[a] > values[b]:
                    values[a], values[b] = values[b], values[a]
            need(values == sorted(values), 'known positive sorter failed')
            positive_inputs += 1
    need(assignments == 3 * 692224, 'original family assignment coverage incomplete')
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher', 'status': 'JOINT_SLACK_NUMERIC_CERTIFICATE_VERIFIED',
                      'original_domains': 975, 'original_free_assignments': assignments,
                      'first_event_gates_checked': 78, 'prep_gates': 45, 'excluded_first_live_gates': 32,
                      'compulsory_first_event': [[9, 11]], 'E22_high_units': 512, 'E23_high_units': 768,
                      'E22_total_sorting_size_lower_bound': 45, 'known_positive_boolean_inputs': positive_inputs,
                      'damages_rejected': len(damages), 'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                      'seconds': time.monotonic() - start, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))


if __name__ == '__main__':
    main()
