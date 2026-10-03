"""Compare complete increasing-second-row and descending-largest-row enumerations."""
import argparse
import hashlib
import json
from pathlib import Path


def collect(directory, first):
    cursor = first
    records = {}
    parts = sorted((json.loads(p.read_text()) for p in directory.glob('*.json')), key=lambda d: d['start'])
    for d in parts:
        if d['start'] != cursor or not cursor < d['stop'] <= 308:
            raise ValueError('Exact contiguous row-traversal domain')
        cursor = d['stop']
        for r in d['records']:
            a = tuple(r['A'])
            if len(a) != 4 or a != tuple(sorted(set(a))) or a[0] != 1 or len(r['C']) < 4 or r['C'] != sorted(set(r['C'])):
                raise ValueError('Actual quadruple/common labels')
            if a in records:
                raise ValueError('Duplicate physical quadruple in whole enumeration')
            records[a] = r['C']
    if cursor != 308:
        raise ValueError('Final row-traversal range missing')
    return [{'A': list(a), 'C': c} for a, c in sorted(records.items())]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('ordered', 'ordered-optimized', 'reverse', 'reverse-optimized', 'output'):
        p.add_argument('--' + name, type=Path, required=True)
    o = p.parse_args()
    streams = [collect(o.ordered, 1), collect(o.ordered_optimized, 1),
               collect(o.reverse, 3), collect(o.reverse_optimized, 3)]
    if any(records != streams[0] for records in streams[1:]) or len(streams[0]) != 64108:
        raise ValueError('Full independently generated quadruple streams differ')
    records = streams[0]
    encoded = json.dumps(records, sort_keys=True, separators=(',', ':')).encode()
    result = {'schema': 'character617-physical-quads-v1', 'count': len(records),
              'records_sha256': hashlib.sha256(encoded).hexdigest(), 'records': records}
    o.output.write_text(json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, sort_keys=True))


if __name__ == '__main__':
    main()
