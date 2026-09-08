"""Exact positive, negative, and relabeling controls; no SAT solver required."""
import argparse
import itertools
import json
from pathlib import Path
import audit
import encode

def rejected(action):
    try:
        action()
    except (ValueError, KeyError, IndexError):
        return
    raise ValueError('Negative control was accepted')

def run(catalog):
    lines = encode.catalog(catalog)
    tables = 0
    for width in range(1, 6):
        left = list(range(1, width + 1))
        right = list(range(width + 1, 2 * width + 1))
        first = 2 * width + 1
        end, clauses = encode.lex_leq(left, right, first)
        for bits in itertools.product((0, 1), repeat=end - 1):
            values = dict(enumerate(bits, 1))
            x = sum(values[v] << (width - 1 - i) for i, v in enumerate(left))
            y = sum(values[v] << (width - 1 - i) for i, v in enumerate(right))
            equal = True
            valid = x <= y
            for j in range(width - 1):
                equal = equal and values[left[j]] == values[right[j]]
                valid = valid and values[first + j] == equal
            audit.require(audit.holds(clauses, values) == valid, 'Comparator exhaustive control')
            tables += 1
    witnesses = json.loads((Path(__file__).resolve().parent / 'TAIL_WITNESSES.json').read_text())
    i = min(map(int, witnesses))
    core = encode.decode(lines[i])
    original = encode.graph(core, witnesses[str(i)])
    audit.witness(lines[i], witnesses[str(i)])
    clauses = encode.formula(core)
    transforms = 0
    for p in itertools.permutations(range(15, 19)):
        for q in itertools.permutations(range(19, 23)):
            for swap in (0, 1):
                before = list(range(15)) + list(p if not swap else q) + list(q if not swap else p)
                g = {(u, v): original[tuple(sorted((before[u], before[v])))] for u, v in encode.PAIRS}
                normal, back = encode.normalize(g)
                audit.require(sorted(back) == list(range(23)) and back[:15] == list(range(15)), 'Relabeling permutation')
                audit.require(all(normal[u, v] == g[tuple(sorted((back[u], back[v])))] for u, v in encode.PAIRS), 'Whole-edge transport')
                audit.require(audit.holds(clauses, encode.assignment(normal)), 'Normalized full tail formula')
                transforms += 1
    # Tied signatures are allowed; normalization does not claim a unique graph representative.
    tied = encode.graph(core, '0' * 136)
    normal, _ = encode.normalize(tied)
    audit.require(audit.holds(encode.ordering(), encode.assignment(normal)), 'Tied comparator control')
    for word in ('0' * 136, '1' * 136, '0' * 135, '2' * 136):
        rejected(lambda word=word: audit.witness(lines[i], word))
    raw = encode.dimacs(core)
    rows = raw.decode().splitlines()
    for k in (1, len(rows) - 1):
        wrong = rows[:k] + rows[k + 1:]
        wrong[0] = f'p cnf 279 {len(wrong)-1}'
        rejected(lambda wrong=wrong: audit.formula(lines[i], ('\n'.join(wrong) + '\n').encode()))
    wrong = rows[:]
    tokens = wrong[1].split()
    tokens[0] = str(-int(tokens[0]))
    wrong[1] = ' '.join(tokens)
    rejected(lambda: audit.formula(lines[i], ('\n'.join(wrong) + '\n').encode()))
    return {'status': 'PASS', 'comparator_assignments': tables, 'whole_tail_relabelings': transforms,
            'tied_signature_fixture': 1, 'rejected_witnesses': 4, 'rejected_formulas': 3}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--catalog', required=True)
    a = p.parse_args()
    print(json.dumps(run(a.catalog), sort_keys=True))
