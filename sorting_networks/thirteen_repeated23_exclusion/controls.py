"""Known sorter controls and semantic rejection of malformed certificates."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import resource
import time

from audit_data import LOWER, audit_data, check_parent, replay, sha
from audit_encoding import Audit
from encoding import Encoding
from verify import bounded, read_cnf
from watched_rup import replay as rup_replay

HERE = Path(__file__).resolve().parent


def reject(name, call):
    try:
        bounded(call)
    except AssertionError:
        return dict(control=name, status='MALFORMED_CERTIFICATE_REJECTED')
    raise AssertionError(f'Malformed certificate accepted: {name}')


def main():
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', type=Path, default=HERE.parent / 'thirteen_repeated23_reduction')
    parser.add_argument('--out', type=Path, default=HERE / 'out')
    args = parser.parse_args()
    start = time.monotonic()
    fixture = json.loads((HERE / 'fixture.json').read_text())
    certificate = json.loads((HERE / 'certificate.json').read_text())
    data = json.loads((args.out / 'data.json').read_text())
    check_parent(fixture, args.parent)
    insertion = [[i, i + 1] for end in range(1, 9) for i in range(end - 1, -1, -1)]
    assert len(insertion) == 36
    positives = []
    for expected in certificate['records']:
        instance = next(r for r in data['instances']
                        if r['record']['parent_index'] == expected['parent_index']
                        and r['record']['image'] == expected['image'])
        full = instance['prefix13'] + [[a + 2, b + 2] for a, b in insertion]
        total = len(full)
        for original in range(8192):
            values = [(original >> i) & 1 for i in range(13)]
            output, spent = replay(values, full)
            assert output == sorted(values)
            if original not in (0, 8191):
                for p in (0, 1):
                    assert spent[p] <= total - LOWER[sum(v != p for v in values)]
        enc = Encoding(9, 36, 'g4')
        for row in instance['record']['rows9']:
            enc.add_row(row)
        for row, polarity, cap, *_ in instance['caps']:
            enc.touch_bound(row, cap + total - 44, polarity)
        answer = bounded(lambda: enc.solver.solve(assumptions=enc.assume_gates(insertion)))
        assert answer is True
        assert list(map(list, enc.decode())) == insertion
        enc.solver.delete()
        positive = dict(parent_index=expected['parent_index'], total_size=total,
                        original_inputs=8192, status='FORCED_INSERTION_SORTER_SAT_AND_SCALAR_VERIFIED')
        positives.append(positive)
        print(json.dumps(positive), flush=True)
    negative = []
    missing = copy.deepcopy(data)
    missing['instances'].pop(0)
    negative.append(reject('omitted_literal_tail', lambda: audit_data(fixture, missing, certificate)))
    wrong_cap = copy.deepcopy(data)
    wrong_cap['instances'][0]['caps'][3][2] += 1
    wrong_cap['instances'][0]['caps_sha256'] = sha(wrong_cap['instances'][0]['caps'])
    negative.append(reject('wrong_pooled_touch_cap_with_updated_digest',
                           lambda: audit_data(fixture, wrong_cap, certificate)))
    first = certificate['records'][0]
    stem = args.out / f"class{first['parent_index']}"
    meta = json.loads(stem.with_suffix('.metadata.json').read_text())
    lines = stem.with_suffix('.cnf').read_text().splitlines(keepends=True)
    literals = lines[1].split()
    assert literals[-2] == '36'
    literals.pop(-2)
    lines[1] = ' '.join(literals) + '\n'
    altered = args.out / 'invalid_choice.cnf'
    altered.write_text(''.join(lines))
    changed_meta, changed_expected = copy.deepcopy(meta), copy.deepcopy(first)
    changed_meta['cnf_sha256'] = changed_expected['cnf_sha256'] = hashlib.sha256(altered.read_bytes()).hexdigest()
    changed_meta['clause_stream_sha256'] = changed_expected['clause_stream_sha256'] = hashlib.sha256(''.join(lines[1:]).encode()).hexdigest()
    negative.append(reject('invalid_exact_one_cardinality_with_updated_digests',
                           lambda: Audit(changed_meta, altered, changed_expected).run()))
    n, core = read_cnf(HERE / first['core_file'])
    empty = args.out / 'invalid_empty.rup'
    empty.write_text('0\n')
    negative.append(reject('premature_empty_RUP_step', lambda: rup_replay(n, core, empty)))
    report = dict(agent='six-sorting-1', role='researcher', positive=positives, negative=negative,
                  status='POSITIVE_SORTERS_AND_FOUR_SEMANTIC_REJECTION_CONTROLS_VERIFIED',
                  seconds=time.monotonic() - start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (args.out / 'controls.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
