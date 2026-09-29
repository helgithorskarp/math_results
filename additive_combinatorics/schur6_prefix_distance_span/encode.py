"""Generate the colour-dependent distance constraints for a fixed prefix."""
import argparse
from itertools import combinations
import json
from pathlib import Path


def clauses(prefix, length, k):
    if length < 1 or not prefix or any(c < 1 or c > k for c in prefix):
        raise ValueError('invalid prefix, palette or length')
    result = []
    for x in range(length):
        block = [k*x+c for c in range(1, k+1)]
        result.append(block)
        result.extend([-a, -b] for a, b in combinations(block, 2))
    for x in range(length):
        for d in range(1, min(len(prefix)+1, length-x)):
            c = prefix[d-1]
            result.append([-k*x-c, -k*(x+d)-c])
    return result


def dimacs(prefix, length, k):
    formula = clauses(prefix, length, k)
    return (f'p cnf {k*length} {len(formula)}\n'
            + ''.join(' '.join(map(str, clause))+' 0\n' for clause in formula))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('output')
    p.add_argument('--length', type=int, default=83)
    args = p.parse_args()
    data = json.loads(Path(__file__).with_name('data.json').read_text())
    Path(args.output).write_text(dimacs(list(map(int, data['prefix'])),
                                      args.length, data['palette_size']))


if __name__ == '__main__':
    main()
