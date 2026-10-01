"""Independent scalar metadata/model checks for frontloaded nine-wire probe."""
from pathlib import Path
import hashlib
import itertools
import json

SIZES = (0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39)


def trace(values, word):
    values = list(values)
    result = [values.copy()]
    for a, b in word:
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
        result.append(values.copy())
    return result


def audit_data(meta):
    provenance(meta)
    prefix = meta['prefix']
    projected, caps = {}, {}
    for original in range(8192):
        history = trace([original >> i & 1 for i in range(13)], prefix)
        bits = history[-1]
        row = sum(bits[j + 2] << j for j in range(9))
        projected[original] = row
        assert bits[:2] == sorted([original >> i & 1 for i in range(13)])[:2]
        assert bits[-2:] == sorted([original >> i & 1 for i in range(13)])[-2:]
        if original in (0, 8191):
            continue
        for mode, marked_count in ((0, 13 - original.bit_count()), (1, original.bit_count())):
            charge = sum(mode in (before[a], before[b]) for before, (a, b) in zip(history, prefix))
            cap = 32 + meta['budget'] - SIZES[13 - marked_count] - charge
            key = row, mode
            caps[key] = min(cap, caps.get(key, 32 + meta['budget']))
    assert sorted(set(projected.values())) == meta['record']['image9']
    assert [[r, p, c] for (r, p), c in sorted(caps.items())] == meta['caps']
    clamp_checks = actual_marked_checks = 0
    for domain in meta['domains']:
        free = [i for i in range(13) if i not in domain['original']]
        inputs = []
        for mask in range(2048):
            bits = [0] * 13
            for i, p in enumerate(free):
                bits[p] = mask >> i & 1
            for p in domain['original']:
                bits[p] = int(domain['mode'] == 'max')
            out = trace(bits, prefix)[-1]
            inputs.append(sum(out[j + 2] << j for j in range(9)))
            clamp_checks += 1
            actual = bits.copy()
            for order, p in enumerate(domain['original']):
                actual[p] = 2 + order if domain['mode'] == 'max' else -2 + order
            actual_history = trace(actual, prefix)
            is_marked = (lambda v: v >= 2) if domain['mode'] == 'max' else (lambda v: v < 0)
            actual_charge = sum(is_marked(before[a]) or is_marked(before[b])
                                for before, (a, b) in zip(actual_history, prefix))
            actual_positions = [i for i,v in enumerate(actual_history[-1]) if is_marked(v)]
            assert actual_charge == 9
            assert actual_positions == ([11,12] if domain['mode'] == 'max' else [0,1])
            assert actual_history[-1][2:11] == out[2:11]
            actual_marked_checks += 1
        assert sorted(set(inputs)) == domain['image9']
        ranks = list(range(2, 15))
        for i, p in enumerate(domain['original']):
            ranks[p] = 20 + i if domain['mode'] == 'max' else -2 + i
        histories = trace(ranks, prefix)
        marked = (lambda v: v > 15) if domain['mode'] == 'max' else (lambda v: v < 0)
        charge = sum(marked(before[a]) or marked(before[b]) for before, (a, b) in zip(histories, prefix))
        positions = [i for i, v in enumerate(histories[-1]) if marked(v)]
        assert charge == 9
        assert positions == ([11, 12] if domain['mode'] == 'max' else [0, 1])
    return dict(original_rows=8192, cap_records=len(caps), active_caps=len(meta['hit_flags']),
                clamped_rows=clamp_checks, actual_marked_free_assignments=actual_marked_checks,
                mandatory_activity_domains=len(meta['domains']),
                status='INDEPENDENT_PREFIX_CAP_CLAMPED_DOMAIN_DATA_VERIFIED')


def check_model(meta, word, model, path):
    assert len(word) == meta['budget']
    meta = dict(meta)
    meta['rows'] = {int(r): v for r,v in meta['rows'].items()}
    meta['swaps'] = {int(r): v for r,v in meta['swaps'].items()}
    positive = {x for x in model if x > 0}
    def val(lit):
        if isinstance(lit, bool):
            return lit
        return lit in positive if lit > 0 else -lit not in positive
    for row in meta['record']['image9']:
        histories = trace([row >> i & 1 for i in range(9)], word)
        assert histories[-1] == sorted(histories[0])
        if row in meta['rows']:
            for t, bits in enumerate(histories):
                assert bits == [int(val(v)) for v in meta['rows'][row][t]]
            for t, (a, b) in enumerate(word):
                assert val(meta['swaps'][row][t]) == (histories[t][a] > histories[t][b])
    for row, mode, cap in meta['caps']:
        histories = trace([row >> i & 1 for i in range(9)], word)
        assert sum(mode in (h[a], h[b]) for h, (a, b) in zip(histories, word)) <= cap
    if meta['activity']:
        for domain in meta['domains']:
            histories = [trace([r >> i & 1 for i in range(9)], word) for r in domain['image9']]
            for t, (a, b) in enumerate(word):
                assert any(h[t][a] > h[t][b] for h in histories)
    clauses = 0
    assert hashlib.sha256(path.read_bytes()).hexdigest() == meta['cnf_sha256']
    with path.open() as stream:
        for line in stream:
            if line[:1] in 'pc':
                continue
            assert any(val(int(v)) for v in line.split()[:-1]), clauses
            clauses += 1
    assert clauses == meta['clauses']
    full = meta['prefix'] + [(a + 2, b + 2) for a, b in word]
    for original in range(8192):
        bits = [original >> i & 1 for i in range(13)]
        assert trace(bits, full)[-1] == sorted(bits), original
    return dict(status='MODEL_ALL_CLAUSES_TRACES_CAPS_AND_8192_FULL_INPUTS_VERIFIED',
                clauses_checked=clauses, full13_inputs=8192, full_size=len(full))


HERE = Path(__file__).resolve().parent


def check_dependencies():
    manifest = json.loads((HERE / 'dependencies.json').read_text())
    for item in manifest['pinned_files']:
        assert hashlib.sha256((HERE.parent / item['path']).read_bytes()).hexdigest() == item['sha256'], item['path']


def provenance(meta):
    check_dependencies()
    cert = json.loads((HERE.parent / 'sorting13_B11_ten_event_loop_postponement/certificate.json').read_text())
    code = meta['record']['code']
    selected = json.loads((HERE / 'certificate.json').read_text())['records']
    expected_record = next(r for r in selected if r['code'] == code)
    quotient = json.loads((HERE.parent / 'sorting_networks/thirteen_extreme_multiset_quotient/certificate.json').read_text())
    entry = next(r for r in quotient['class_table'] if r[0] == code)
    assert entry[1] == 10 and entry[2] == expected_record['effective_orders']
    item = next(r for r in cert['classes'] if r['code'] == code)
    assert item['obstruction'] is None and item['image_id'] == expected_record['image_id']
    assert meta['record']['code'] == code
    assert meta['record']['canonical_events'] == item['events']
    assert meta['record']['image9'] == cert['images9'][item['image_id']]
    assert len(meta['record']['image9']) == expected_record['rows']
    fixture = json.loads((HERE.parent / 'sorting13_B11_ten_event_matching_dags/fixture.json').read_text())
    expected = fixture['prefix22'] + [[a+1,b+1] for a,b in item['events']]
    assert [list(g) for g in meta['prefix']] == expected and len(expected) == 32
    parent = json.loads((HERE.parent / 'sorting13_B11_pruning_saturation_activity/certificate.json').read_text())
    roots = [(f['mode'],f['partner'],original) for f in parent['families'] if f['final_D']==9 for original in f['original_representatives']]
    assert [(d['mode'],d['partner'],d['original']) for d in meta['domains']] == roots


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('cnf',type=Path)
    args = parser.parse_args()
    meta = json.loads(args.cnf.with_suffix('.metadata.json').read_text())
    print(json.dumps(audit_data(meta)))
