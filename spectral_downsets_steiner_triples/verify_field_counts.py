"""Replay the uniform field-count formulas at7,13,19,31, without H claims."""
import argparse
import json
from pathlib import Path

from affine_psd import invariant_partitions
from field_family import field_counts, field_downset
from verify import rejects


def run():
    records = []
    for p in (7, 13, 19, 31):
        D, roots = field_downset(p)
        expected = field_counts(p)
        actual = {k: len(part) for k, part in invariant_partitions(D, p).items()}
        assert actual == expected['fixed_space_dimensions']
        # The whole permutation space satisfies the affine rank decomposition.
        assert actual['T']+(p-1)*(actual['H']-actual['G']) == len(D)
        records.append({**expected, 'roots': roots})
    rejects(lambda: field_counts(25))
    rejects(lambda: field_counts(11))
    return {'scope': 'Uniform input/count proof; these checks do not assert H caps',
            'orders': records, 'rejection_controls': 2}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    assert not (args.check and args.write_expected)
    result = run()
    path = Path(__file__).with_name('field_counts_expected.json')
    if args.check:
        assert result == json.loads(path.read_text()), 'expected-output mismatch'
    if args.write_expected:
        path.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))
