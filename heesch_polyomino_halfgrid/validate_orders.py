"""Independent ordered-partition generation and exact Stirling-count checks."""
import argparse
from itertools import permutations
import json
from pathlib import Path

from closed import ordered_labels, ordered_phase_count


def independent(k):
    def partitions(prefix):
        if len(prefix) == k:
            yield prefix
        else:
            maximum = max(prefix, default=-1)
            for label in range(maximum+2):
                yield from partitions(prefix+(label,))
    for p in partitions(()):
        for labels in permutations(range(1, max(p, default=-1)+2)):
            yield tuple(labels[i] for i in p)


def main():
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('--expected', type=Path, default=Path(__file__).parent/'orders_expected.json')
    a.add_argument('--write-expected', action='store_true')
    args = a.parse_args()
    counts = []
    for k, known in enumerate((1, 1, 3, 13, 75, 541, 4683)):
        direct, other = list(ordered_labels(k)), list(independent(k))
        assert len(direct) == len(set(direct)) == known == ordered_phase_count(k)
        assert len(other) == len(set(other)) == known and set(direct) == set(other)
        counts.append({'positive_phase_variables': k, 'complete_patterns': known})
    result = {'agent': 'six-heesch-1', 'role': 'researcher',
              'two_distinct_enumerators_match': True, 'counts': counts}
    encoded = json.dumps(result, sort_keys=True, indent=2)+'\n'
    if args.write_expected:
        args.expected.write_text(encoded)
    else:
        assert result == json.loads(args.expected.read_text())
    print(encoded, end='')


if __name__ == '__main__':
    main()
