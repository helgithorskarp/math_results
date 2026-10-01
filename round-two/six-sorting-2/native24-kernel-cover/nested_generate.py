"""Boolean-column producer of selected nested-potential root certificates.

Exact fixed original domains; no solver or suffix enumeration is used.
The standalone numeric checker imports none of the production machinery.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
PINS = {'fixture.json': '93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6', 'certificate.json': '21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06', 'nested-fixture.json': '2ac145e523afcb00fb13976664577b2f2f3b9e1b28c2ae3336a6a4eb2051833a'}
PRUNER_SHA256 = 'c4699f5c85be9906f410390538865f5ada0e93e0431c7fe2ac4e2876ee01589c'
PRECEDING_FOURTEEN = [2,8,15,20,24,31,32,33,34,36,38,39,41,42]


def checked(name, pin):
    data = (ROOT / name).read_bytes()
    if hashlib.sha256(data).hexdigest() != pin:
        raise ValueError('published dependency changed: ' + name)
    return data


checked('minimum_generate.py', PRUNER_SHA256)
spec = importlib.util.spec_from_file_location('nested_native_pruner', ROOT / 'minimum_generate.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
s = m.semantic


def record_for(gates, low, high):
    free = [q for q in range(13) if not (low | high) >> q & 1]
    columns = iter(s.truth_columns(len(free)))
    values = [s.LOW if low >> q & 1 else s.HIGH if high >> q & 1 else next(columns)
              for q in range(13)]
    d = r = mask = 0
    for t, (a, b) in enumerate(gates):
        hit, inactive = s.transition(values, a, b)
        d += hit
        r += inactive
        if inactive:
            mask |= 1 << t
    return [low, high, *s.marked_ports(values), d, r, mask]


def witness(gates, low, high):
    record = record_for(gates, low, high)
    pruned = m.prune(gates, record)
    data = s.analyze(7, pruned['retained_prefix'])
    anchors = m.base.anchors.both(7, data)
    b = max(16, *(a['lower_bound'] for a in anchors.values()))
    return {'pruning': pruned,
            'inner_records_sha256': {name: m.base.digest(a['records']) for name,a in data.items()},
            'inner_anchor_leaves': {side: [[r['port'],r['label']] for r in a['rows']]
                                    for side,a in anchors.items()},
            'inner_anchor_bounds': {side: a['lower_bound'] for side,a in anchors.items()},
            'inner_bound': b, 'prefix_cost': record[4] + record[5],
            'nested_label': record[4] + record[5] + b}


def build():
    fixture = json.loads(checked('fixture.json', PINS['fixture.json']))
    parent = json.loads(checked('certificate.json', PINS['certificate.json']))
    selected = json.loads(checked('nested-fixture.json', PINS['nested-fixture.json']))
    if [c['kernel_id'] for c in selected['cases']] != list(range(45)):
        raise ValueError('incomplete literal kernel list')
    cases = []
    for c in selected['cases']:
        i = c['kernel_id']
        gates = fixture['gates'][:24] + fixture['forced_gates'] + parent['kernels'][i]['kernel']
        rows = [witness(gates, lo, hi) for lo, hi in c['original_clampings']]
        classes = {tuple(r['pruning']['outer_record'][2:4]) for r in rows}
        if len(classes) != len(rows):
            raise ValueError('selected current classes overlap')
        mass = sum(2 ** r['nested_label'] for r in rows)
        if mass <= 2 ** 44:
            raise ValueError('selected nested mass is not an exclusion')
        cases.append({'kernel_id': i, 'prefix32_sha256': m.base.digest(gates),
                      'selected_domains': rows, 'selected_classes': len(classes),
                      'selected_mass': mass, 'total_lower_bound': (mass - 1).bit_length(),
                      'maximum_individual_label': max(r['nested_label'] for r in rows)})
    return {'schema': 'native-nested-selected-certificate-v1', 'agent': 'six-sorting-2',
            'role': 'researcher', 'parent_files_sha256': PINS, 'n': 13, 'l': 3, 'h': 3,
            'free_inputs': 7, 'size_budget': 44, 'root_length': 32, 'kernel_count': 45,
            'closed_preceding_fourteen': PRECEDING_FOURTEEN, 'remaining_kernel_ids': [],
            'cases': cases}


def main():
    start = time.monotonic()
    data = build()
    out = ROOT / 'nested-certificate.json'
    out.write_text(json.dumps(data, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps({'status': 'NESTED_SELECTED_CERTIFICATE_REGENERATED', 'agent': 'six-sorting-2',
                      'role': 'researcher', 'kernel_count': 45, 'remaining_targets': 0,
                      'selected_domains': sum(c['selected_classes'] for c in data['cases']),
                      'bytes': out.stat().st_size,
                      'certificate_sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
                      'seconds': time.monotonic() - start,
                      'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))


if __name__ == '__main__':
    main()
