#!/usr/bin/env python3
"""Counter-free parity-ladder models for the exact 4 -> 5 -> 6 ascent."""
import argparse, hashlib, itertools, json, math
from pathlib import Path

CASES = {'no-five': (4, 5), 'no-six': (5, 6), 'six': (6, None)}

def model(q, case):
    if q < 7 or any(q % d == 0 for d in range(2, math.isqrt(q) + 1)):
        raise ValueError('Prime q>=7 required')
    seed, forbidden = CASES[case]
    labels = {pair: i + 1 for i, pair in enumerate(itertools.combinations(range(q), 2))}
    edge = lambda x, y: labels[tuple(sorted((x, y)))]
    canonical = lambda row: tuple(sorted(set(row), key=abs))
    rows = set()
    for x in range(1, q):
        for y in range(x + 1, q):
            ids = edge(0, x), edge(0, y), edge(x, y)
            for bits in itertools.product((0, 1), repeat=3):
                if sum(bits) % 2:
                    rows.add(canonical(-v if b else v for v, b in zip(ids, bits)))
    for r in range(1, (q + 1) // 2):
        for a in range(q):
            row = canonical(edge((a + j*r) % q, (a + (j+3)*r) % q) for j in range(4))
            rows.add(row); rows.add(tuple(-v for v in row))
    criterion = len(rows)
    rows.update((-j,) for j in range(1, seed))
    if forbidden is not None:
        for a in range(q):
            for r in range(1, (q + 1) // 2):
                rows.add(tuple(sorted((a + j*r) % q for j in range(forbidden) if (a + j*r) % q)))
    n = len(labels)
    raw = f'p cnf {n} {len(rows)}\n' + ''.join(' '.join(map(str, row)) + ' 0\n' for row in sorted(rows))
    return raw, {'q': q, 'case': case, 'seed_length': seed, 'forbidden_AP_length': forbidden,
                 'variables': n, 'clauses': len(rows), 'criterion_clauses': criterion,
                 'counter_variables': 0, 'weight_cap': None,
                 'cnf_sha256': hashlib.sha256(raw.encode()).hexdigest()}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--q', type=int, default=103)
    p.add_argument('--case', choices=CASES, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); raw, meta = model(a.q, a.case)
    a.output.write_text(raw); print(json.dumps(meta, sort_keys=True))

if __name__ == '__main__': main()
