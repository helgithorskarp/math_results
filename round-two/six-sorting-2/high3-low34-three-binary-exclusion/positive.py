"""Known45-sorter control on every Boolean input and every used original cube."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
if hashlib.sha256((ROOT / 'numeric.py').read_bytes()).hexdigest() != \
        '83c79d716581cdc8f947a21d9120a001624d8179fab8935817e28326f10bb041':
    raise ValueError('credited scalar source changed')
spec = importlib.util.spec_from_file_location('credited_numeric_positive_control', ROOT / 'numeric.py')
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    gates = json.loads((ROOT / 'positive45.json').read_text())['gates']
    n.need(len(gates) == 45 and all(type(a) is int and type(b) is int and 0 <= a < b < 13 for a, b in gates),
           'positive known-sorter interface differs')
    outputs = [n.bool_word(x, gates) for x in range(8192)]
    n.need(all(y == ((1 << x.bit_count()) - 1) << (13 - x.bit_count()) for x, y in enumerate(outputs)),
           'positive network does not sort every Boolean input')
    certificate = json.loads((ROOT / 'certificate.json').read_text())
    origins = set()
    for w in certificate['witnesses']:
        records = w['distinct_tag_witness_records'] if w['kind'] == 'SEMANTIC_WEIGHTED_MASS' else [w['record']]
        origins.update(tuple(r[:2]) for r in records)
    actual, assignments = [], 0
    floors = {9: 25, 10: 29, 11: 35, 12: 39}
    for lo, hi in sorted(origins):
        record, rows = n.follow(n.fresh_domain(lo, hi), gates, 0)
        n.need(all(v == sorted(v) for v in rows), 'positive numerical original cube unsorted')
        k = 13 - (lo | hi).bit_count()
        n.need(k in floors and record[4] + record[5] + floors[k] <= 45,
               'positive original charge conflicts with pruning ceiling')
        assignments += len(rows)
        actual.append([record, n.digest(rows)])
    math = {'known45_network': gates, 'Boolean_inputs_sorted': 8192, 'entire_Boolean_outputs_sha256': n.digest(outputs),
            'all_used_actual_original_domain_controls': actual, 'original_assignments_sorted': assignments,
            'new_construction': False}
    result = {'agent': 'six-sorting-2', 'role': 'researcher', 'status': 'KNOWN45_POSITIVE_ORIGINAL_CONTROLS_COMPLETE',
              'mathematical': math, 'entire_mathematical_record_sha256': n.digest(math),
              'seconds': time.monotonic() - started, 'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, separators=(',', ':')) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'mathematical'}))


if __name__ == '__main__':
    main()
