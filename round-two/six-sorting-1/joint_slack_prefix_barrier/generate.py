"""Packed original-domain producer for a changed22-gate prefix barrier."""
import hashlib
import importlib.util
from itertools import combinations
import json
import os
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
SOURCE = Path(os.environ.get('SORTING_SOURCE_ROOT', ROOT.parents[2]))
FIXTURE_SHA = '956d91d12d140d1cead9a7f25c77c057055084fa802eac9de0606cdec8f01aa6'
PINS = {'profile.py': 'dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719',
        'anchors.py': '0b95573e7e3c446d0b7ca5352f6b5f4b8d92b91d6f3c72e7b4f783cd99d89902'}
FAMILIES = {'two_minima': (2, 0), 'one_maximum': (0, 1),
            'two_maxima': (0, 2), 'mixed_pair': (1, 1)}


def need(test, message):
    if not test:
        raise ValueError(message)


def high_step(leaves, a, b):
    next_leaves = {}
    for port, label in leaves.items():
        hit = int(port == a or port == b)
        output = b if hit else port
        next_leaves[output] = max(next_leaves.get(output, -1), label + hit)
    return next_leaves


def main():
    start = time.monotonic()
    fixture_raw = (ROOT / 'fixture.json').read_bytes()
    need(hashlib.sha256(fixture_raw).hexdigest() == FIXTURE_SHA, 'literal fixture pin differs')
    fixture = json.loads(fixture_raw)
    directory = SOURCE / 'round-two/six-sorting-2/semantic-pruning'
    for name, pin in PINS.items():
        need(hashlib.sha256((directory / name).read_bytes()).hexdigest() == pin, 'production dependency changed: ' + name)
    spec = importlib.util.spec_from_file_location('joint_slack_anchor', directory / 'anchors.py')
    anchor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(anchor)
    B = fixture['native_prefix19'] + fixture['changed_pair']
    E = B + [fixture['joint_gate']]
    words = {'B21': B, 'E22': E, 'E23': E + [fixture['forced_first_high_gate']]}
    stages = []
    expected = {'B21': ([[9, 41], [11, 42], [12, 43]], 448, 448),
                'E22': ([[9, 42], [11, 42], [12, 43]], 512, 512),
                'E23': ([[11, 44], [12, 43]], 768, 512)}
    for name, word in words.items():
        data = {family: anchor.semantic.analyze_family(13, word, l, h) for family, (l, h) in FAMILIES.items()}
        high = anchor.aggregate(13, data, 'high')
        ordinary_low = [[r[0], r[2]] for r in data['two_minima']['envelope']]
        need([[r['port'], r['label']] for r in high['rows']] == expected[name][0], 'unexpected high leaves')
        need(high['normalized_mass'] == expected[name][1], 'unexpected high mass')
        need(data['two_minima']['summary']['ordinary_mass'] == expected[name][2], 'unexpected ordinary low mass')
        stages.append({'name': name, 'literal_word': word,
                       'families': {family: {'low_count': l, 'high_count': h,
                                             'records': data[family]['records'], 'envelope': data[family]['envelope']}
                                    for family, (l, h) in FAMILIES.items()},
                       'ordinary_low_envelope': ordinary_low,
                       'ordinary_low_mass': data['two_minima']['summary']['ordinary_mass'],
                       'high_anchor': high})
    leaves = {r['port']: r['label'] for r in stages[1]['high_anchor']['rows']}
    coverage = []
    for a, b in combinations(range(13), 2):
        after = high_step(leaves, a, b)
        units = sum(1 << (label - 35) for label in after.values())
        coverage.append({'gate': [a, b], 'touches_live_high': a in leaves or b in leaves,
                         'inherited_leaves': [[p, c] for p, c in sorted(after.items())],
                         'inherited_units': units, 'within44_ceiling': units <= 512})
    mandatory = [r['gate'] for r in coverage if r['touches_live_high'] and r['within44_ceiling']]
    need(mandatory == [[9, 11]], 'first high event is not unique')
    certificate = {'schema': 'changed22-high-first-event-barrier-v1', 'agent': 'six-sorting-1', 'role': 'researcher',
                   'fixture_sha256': FIXTURE_SHA, 'production_dependency_sha256': PINS,
                   'imported_lower_bounds': fixture['imported_lower_bounds'], 'stages': stages,
                   'first_high_gate_coverage': coverage, 'mandatory_first_high_gates': mandatory,
                   'prep_gate_count': sum(not r['touches_live_high'] for r in coverage),
                   'excluded_live_gate_count': sum(r['touches_live_high'] and not r['within44_ceiling'] for r in coverage),
                   'E22_total_sorting_size_lower_bound': 45,
                   'scope': 'Every standard completion of the exact E22 word, arbitrary order and depth; no global S13=45 claim.'}
    path = ROOT / 'certificate.json'
    path.write_text(json.dumps(certificate, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher', 'status': 'JOINT_SLACK_CERTIFICATE_GENERATED',
                      'stage_count': 3, 'original_domains': sum(len(f['records']) for s in stages for f in s['families'].values()),
                      'E22_first_high_event': mandatory, 'E23_high_units': stages[2]['high_anchor']['normalized_mass'],
                      'certificate_bytes': path.stat().st_size, 'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                      'seconds': time.monotonic() - start,
                      'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))


if __name__ == '__main__':
    main()
