"""Definition-level verification of the known 21-block upper-bound witness."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json


def main():
    source = Path(__file__).resolve().with_name('UPPER21.json')
    data = json.loads(source.read_text())
    if data['parameters'] != dict(v=13, k=6, t=3) or data['point_indexing'] != '1-based':
        raise ValueError('wrong fixture parameters')
    blocks = [frozenset(row) for row in data['blocks']]
    if len(blocks) != 21 or len(set(blocks)) != 21:
        raise ValueError('wrong number of distinct blocks')
    points = set(range(1, 14))
    if any(len(row) != 6 or len(block) != 6 or not block <= points
           for row, block in zip(data['blocks'], blocks)):
        raise ValueError('invalid block')
    multiplicities = [sum(set(triple) <= block for block in blocks)
                      for triple in combinations(range(1, 14), 3)]
    if len(multiplicities) != 286 or min(multiplicities) < 1:
        raise ValueError('uncovered triple')
    degrees = [sum(p in block for block in blocks) for p in range(1, 14)]
    print(json.dumps(dict(status='VERIFIED_C13_6_3_UPPER_BOUND_21',
                          blocks=len(blocks), covered_triples=len(multiplicities),
                          point_degrees=degrees,
                          triple_multiplicity_histogram=dict(sorted(Counter(multiplicities).items())),
                          fixture_sha256=sha256(source.read_bytes()).hexdigest()), indent=2))


if __name__ == '__main__':
    main()
