"""Verify a complete unrestricted terminal relation without a SAT solver."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

from geometry import verify as verify_geometry

HERE = Path(__file__).resolve().parent
TERMINALS = (0, 1, 3, 6, 9, 14, 15, 16, 17, 18)
INTERIOR = tuple(v for v in range(19) if v not in TERMINALS)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edges(path=HERE / 'geometry_certificate.json'):
    return tuple(map(tuple, json.loads(path.read_text())['edge_equations']))


def patterns(edge_set):
    """Lexicographic restricted-growth words, pruned only by terminal edges."""
    adjacent = {(i, j) for i, j in combinations(range(10), 2)
                if (TERMINALS[i], TERMINALS[j]) in edge_set}

    def visit(prefix):
        if len(prefix) == 10:
            yield prefix
            return
        j = len(prefix)
        for colour in range(min(3, 1 + max(prefix, default=-1)) + 1):
            if all(prefix[i] != colour for i in range(j) if (i, j) in adjacent):
                yield from visit(prefix + (colour,))

    yield from visit(())


def verify_completions(text, edge_set):
    rows = text.splitlines()
    pats = list(patterns(edge_set))
    require(len(pats) == len(rows) == 4320, 'complete pattern/word count')
    require(text == '\n'.join(rows) + '\n', 'canonical completion encoding')
    histogram = Counter()
    digest = sha256()
    for pattern, row in zip(pats, rows):
        require(len(row) == 9 and set(row) <= set('0123'), 'nine interior colours')
        word = [-1] * 19
        for v, c in zip(TERMINALS, pattern):
            word[v] = c
        for v, c in zip(INTERIOR, row):
            word[v] = int(c)
        require(all(word[a] != word[b] for a, b in edge_set), 'unit edge inequality')
        histogram[1 + max(pattern)] += 1
        digest.update((''.join(map(str, word)) + '\n').encode())
    return {'canonical_terminal_patterns': len(pats), 'forbidden_patterns': 0,
            'patterns_by_colours_used': dict(sorted(histogram.items())),
            'unit_edge_inequalities_checked': len(pats) * len(edge_set),
            'full_word_stream_sha256': digest.hexdigest(),
            'completion_sha256': sha256(text.encode()).hexdigest()}


def run():
    geo = verify_geometry(HERE / 'geometry_certificate.json')
    edge_set = set(edges())
    neighbours = [set() for _ in range(19)]
    for a, b in edge_set:
        neighbours[a].add(b)
        neighbours[b].add(a)
    require(tuple(v for v in range(19) if len(neighbours[v]) == 3) == TERMINALS,
            'terminals are exactly the degree-three vertices')
    require(not any(neighbours[a] & neighbours[b] for a, b in edge_set),
            'triangle-free support')
    terminal_edges = sorted((a, b) for a, b in edge_set
                            if a in TERMINALS and b in TERMINALS)
    require(terminal_edges == [(0, 1), (0, 3), (1, 6), (14, 15),
                               (14, 16), (15, 17), (16, 18), (17, 18)],
            'bare terminal graph P4 + isolated point + C5')
    relation = verify_completions((HERE / 'completions.txt').read_text(), edge_set)
    # P4, K1 and C5 are disjoint. Every proper colouring uses >=3 colours,
    # hence the S4 action is free. This checks the symmetry count independently.
    labelled = (4 * 3**3) * 4 * (3**5 - 3)
    require(labelled == 24 * relation['canonical_terminal_patterns'],
            'chromatic-polynomial coverage count')
    return {'status': 'EXACT EI19 TEN-TERMINAL RELATION IS NEUTRAL',
            'geometry': geo, 'terminals': TERMINALS, 'interior': INTERIOR,
            'labelled_terminal_colourings': labelled, 'relation': relation,
            'record_improvement': False, 'qualifying_forcing_milestone': False}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
