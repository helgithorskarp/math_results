"""Reproduce the fixed clause selection; no embedding search or SAT backend."""
import itertools
import json
from pathlib import Path


def partitions(prefix=()):
    if len(prefix) == 7:
        yield prefix
        return
    for c in range(min(3, max(prefix, default=-1)+1)+1):
        yield from partitions(prefix+(c,))


def main():
    words = list(partitions())
    clauses = []
    for a, b, c, d in itertools.combinations(range(7), 4):
        clauses.extend([((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))])
    cover = [{j for j, word in enumerate(words) if word[a] == word[b] and word[c] == word[d]}
             for (a, b), (c, d) in clauses]
    remaining = set(range(len(words)))
    selected = []
    while remaining:
        i = max(range(len(clauses)), key=lambda i: (len(cover[i] & remaining), -i))
        if not cover[i] & remaining:
            raise ValueError('incomplete clause universe')
        selected.append(i)
        remaining -= cover[i]
    for i in selected[::-1]:
        if set().union(*(cover[j] for j in selected if j != i)) == set(range(len(words))):
            selected.remove(i)
    expected = json.loads(Path(__file__).with_name('certificate.json').read_text())['clauses']
    actual = [[list(a), list(b)] for a, b in (clauses[i] for i in selected)]
    if actual != expected:
        raise ValueError('fixed selection differs')
    print(json.dumps({'status': 'MATCH', 'canonical_patterns': len(words),
                      'available_clauses': len(clauses), 'selected_clauses': len(selected),
                      'raw_labels': 7+7*len(selected)}, sort_keys=True))


if __name__ == '__main__':
    main()
