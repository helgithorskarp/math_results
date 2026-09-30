"""Direct scalar/model audit, adapted from7474's independent model checker."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / 'sorting13_maximum_preparation'


def scalar(values, word):
    values = list(values)
    for a, b in word:
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values


def main(path):
    if not __debug__:
        raise RuntimeError('Run without Python optimization')
    meta = json.loads(path.with_suffix('.meta.json').read_text())
    model = json.loads(path.with_suffix('.model.json').read_text())
    assert hashlib.sha256(path.read_bytes()).hexdigest() == meta['cnf_sha256']
    assert len({abs(v) for v in model}) == len(model)
    assert all(0 < abs(v) <= meta['variables'] for v in model)
    values = {abs(v): v > 0 for v in model}
    count = 0
    with path.open() as stream:
        for line in stream:
            if not line.strip() or line[0] in 'cp':
                continue
            clause = [int(v) for v in line.split()[:-1]]
            assert any(values.get(abs(v), False) == (v > 0) for v in clause), count
            count += 1
    assert count == meta['clauses']
    word = []
    for row in meta['choices']:
        indices = [j for j, v in enumerate(row) if values.get(v, False)]
        assert len(indices) == 1
        word.append(meta['pairs'][indices[0]])
    f = json.loads((PRIOR / 'fixture.json').read_text())
    for state in f['states']:
        row = [(state >> i) & 1 for i in range(9)]
        assert scalar(row, word) == sorted(row)
    for state in range(2048):
        row = [(state >> i) & 1 for i in range(11)]
        out = scalar(row, f['prefix'])
        out = [out[i] for i in f['prefix_output_order']]
        out = scalar(out, f['after'])
        assert [out[0]] + scalar(out[1:10], word) + [out[10]] == sorted(row)
    records = f['critical_single_bounds'] + f['selected_mixed_bounds'] + f['designated_bounds']
    records += json.loads((HERE / 'additional_witnesses.json').read_text())
    records = list({(w['x'], w['y']): w for w in records}.values())
    assert len(records) == 145
    for r in records:
        high = [(r['x'] >> i) & 1 for i in range(9)]
        low = [(r['y'] >> i) & 1 for i in range(9)]
        hits = 0
        for a, b in word:
            hits += bool(high[a] or high[b] or not low[a] or not low[b])
            high = scalar(high, [(a, b)])
            low = scalar(low, [(a, b)])
        assert hits <= r['cap'] + len(word) - 16
    result = dict(agent='six-sorting-2', role='researcher', status='VERIFIED',
                  all_clauses=count, original_inputs=2048, residual_states=109,
                  pruning_constraints=145, gates=len(word), word=word,
                  cnf_sha256=meta['cnf_sha256'])
    path.with_suffix('.model-verified.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('path', type=Path)
    main(p.parse_args().path)
