"""Direct independent scalar/model audit of a nine-wire L109 witness."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


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
    f = json.loads((HERE / 'fixture.json').read_text())
    p = json.loads((HERE / 'fixture.json').read_text())
    for state in p['states']:
        row = [(state >> i) & 1 for i in range(9)]
        assert scalar(row, word) == sorted(row)
    for state in range(2048):
        row = [(state >> i) & 1 for i in range(11)]
        out = scalar(row, f['prefix'])
        out = [out[i] for i in f['prefix_output_order']]
        out = scalar(out, p['after'])
        assert [out[0]] + scalar(out[1:10], word) + [out[10]] == sorted(row)
    records = p['critical_single_bounds'] + p['selected_mixed_bounds'] + p['designated_bounds']
    records = list({(w['x'], w['y']): w for w in records}.values())
    for record in records:
        high = [(record['x'] >> i) & 1 for i in range(9)]
        low = [(record['y'] >> i) & 1 for i in range(9)]
        hits = 0
        for a, b in word:
            hits += bool(high[a] or high[b] or not low[a] or not low[b])
            high = scalar(high, [(a, b)]); low = scalar(low, [(a, b)])
        assert hits <= record['cap'] + len(word) - 16
    result = dict(agent='six-sorting-2', role='researcher', status='VERIFIED',
                  all_clauses=count, original_inputs=2048, residual_states=109,
                  pruning_constraints=len(records), gates=len(word), word=word,
                  cnf_sha256=meta['cnf_sha256'])
    path.with_suffix('.model-verified.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('path', type=Path)
    main(parser.parse_args().path)
