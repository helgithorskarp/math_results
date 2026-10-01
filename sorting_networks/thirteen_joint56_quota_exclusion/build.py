"""Produce the literal data and twelve complete capped CNFs.

six-sorting-1, researcher. No solve is needed to check the supplied compact
RUP certificates. Large generated formulas and native traces stay in out/.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import threading
import time

for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'

from encoding import Encoding
from verify import bounded

HERE = Path(__file__).resolve().parent
LOWER = (0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def load_inputs(path=HERE):
    fixture = json.loads((path / 'fixture.json').read_text())
    parent = json.loads((path / 'reduction.json').read_text())
    certificate = json.loads((HERE / 'certificate.json').read_text())
    assert hashlib.sha256((path / 'reduction.json').read_bytes()).hexdigest() == certificate['reduction_sha256']
    assert hashlib.sha256((HERE / 'tail_obstructions.json').read_bytes()).hexdigest() == certificate['obstructions_sha256']
    assert parent['fixture_sha256'] == digest(fixture)
    fixture['tails'] = [r for c in parent['classes'] for r in c['remaining_tails']]
    obstructions = json.loads((HERE / 'tail_obstructions.json').read_text())['records']
    assert len(fixture['tails']) == len(obstructions) == 23
    def key(r):
        return r['parent_index'],r['image'],r['budget'],r['case']
    assert list(map(key,fixture['tails'])) == list(map(key,obstructions))
    fixture['obstructions'] = obstructions
    return fixture, certificate


def produce(fixture, target):
    prefix = fixture['prefix22'] + [[a + 1, b + 1] for a, b in target['prefix_B11']]
    assert len(prefix) + target['budget'] == 44
    pool, images = {}, set()
    for original in range(8192):
        row, spent = original, [0, 0]
        for a, b in prefix:
            left, right = row >> a & 1, row >> b & 1
            spent[0] += not (left and right)
            spent[1] += bool(left or right)
            if left and not right:
                row ^= (1 << a) | (1 << b)
        middle = row >> 2 & 511
        images.add(middle)
        if original in (0, 8191):
            continue
        for polarity in (0, 1):
            free = original.bit_count() if polarity == 0 else 13 - original.bit_count()
            cap = 44 - LOWER[free] - spent[polarity]
            key = middle, polarity
            if key not in pool or cap < pool[key][0]:
                pool[key] = cap, original, free, spent[polarity]
    assert sorted(images) == target['rows9']
    caps = [[r, p, *pool[r, p]] for r, p in sorted(pool)]
    return dict(record=target, prefix13=prefix, caps=caps, caps_sha256=digest(caps))


def main():
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', type=Path, default=HERE)
    parser.add_argument('--out', type=Path, default=HERE / 'out')
    parser.add_argument('--solve', action='store_true', help='Optional native proof regeneration, 15 seconds per case')
    args = parser.parse_args()
    start = time.monotonic()
    fixture, certificate = load_inputs(args.parent)
    args.out.mkdir(parents=True, exist_ok=True)
    data = {'instances': []}
    for target in fixture['tails']:
        item = bounded(produce,fixture,target)
        obstacle = fixture['obstructions'][len(data['instances'])]
        assert item['caps_sha256'] == obstacle['caps_sha256']
        data['instances'].append(item)
    (args.out / 'data.json').write_text(json.dumps(data, indent=2) + '\n')
    results = []
    for expected in certificate['records']:
        item = next(r for r in data['instances']
                    if (r['record']['parent_index'], r['record']['image']) ==
                    (expected['parent_index'], expected['image']))
        target, caps = item['record'], item['caps']
        stem = args.out / f"class{target['parent_index']}_image{target['image']}"
        body_path, cnf_path = stem.with_suffix('.body'), stem.with_suffix('.cnf')
        with body_path.open('w') as body:
            enc = Encoding(9, target['budget'], 'g4' if args.solve else None, body_file=body)
            for row in target['rows9']:
                enc.add_row(row)
            enc.sections['Boolean_comparators'] = enc.clauses - enc.sections['gate_choices']
            first = enc.clauses
            for row, polarity, cap, *_ in caps:
                enc.touch_bound(row, cap, polarity)
            enc.sections['one_sided_pruning'] = enc.clauses - first
        with cnf_path.open('w') as cnf:
            cnf.write(f'p cnf {enc.top} {enc.clauses}\n')
            with body_path.open() as body:
                for line in body:
                    cnf.write(line)
        metadata = enc.metadata()
        metadata.update(record=target, caps=caps, cnf_sha256=hashlib.sha256(cnf_path.read_bytes()).hexdigest())
        for key in ('variables', 'clauses', 'clause_stream_sha256', 'cnf_sha256'):
            assert metadata[key] == expected[key], (target['parent_index'], key)
        assert item['caps_sha256'] == expected['caps_sha256']
        stem.with_suffix('.metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
        result = dict(parent_index=target['parent_index'], image=target['image'],
                      variables=enc.top, clauses=enc.clauses, cnf_sha256=metadata['cnf_sha256'])
        if args.solve:
            timer = threading.Timer(15, enc.solver.interrupt)
            timer.daemon = True
            timer.start()
            try:
                answer = enc.solver.solve_limited(expect_interrupt=True)
            finally:
                timer.cancel()
                timer.join()
                enc.solver.clear_interrupt()
            result['native_status'] = 'SAT' if answer is True else 'UNCHECKED_UNSAT' if answer is False else 'UNKNOWN'
            if answer is False:
                proof = enc.solver.get_proof()
                assert proof
                stem.with_suffix('.drat').write_text(''.join(line + '\n' for line in proof))
            enc.solver.delete()
        results.append(result)
        print(json.dumps(result), flush=True)
    print(json.dumps(dict(status='LITERAL_DATA_AND_COMPLETE_CNFS_REPRODUCED',
                          cases=len(results), seconds=time.monotonic() - start)), flush=True)


if __name__ == '__main__':
    main()
