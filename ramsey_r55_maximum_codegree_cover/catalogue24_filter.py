"""Complete external-catalogue filter; NOT a physical good43 decision."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from graphs import decode, require

EXPECTED = '83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0'


def run(path):
    data = path.read_bytes()
    require(sha256(data).hexdigest() == EXPECTED, 'wrong full order-24 catalogue')
    rows = data.decode('ascii').splitlines()
    require(len(rows) == 352366, 'incomplete order-24 catalogue')
    histogram = Counter()
    retained = []
    for i, line in enumerate(rows):
        a = decode(line)
        require(len(a) == 24, 'wrong order')
        delta = max(x.bit_count() for x in a)
        histogram[delta] += 1
        if delta <= 10:
            retained.append(i)
    return {'source_sha256': EXPECTED, 'source_records': len(rows),
            'maximum_degree_histogram': dict(sorted(histogram.items())),
            'retained_zero_based_rows': retained, 'retained_count': len(retained),
            'scope': 'A degree-24 neighborhood in the M=10 physical branch must be among these rows. No exterior edges are decided.',
            'complete_secondary_physical_subset_closed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('catalogue', type=Path)
    print(json.dumps(run(parser.parse_args().catalogue), indent=2))
