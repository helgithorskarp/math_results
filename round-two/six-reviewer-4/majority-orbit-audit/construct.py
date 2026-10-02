"""Bounded positive packing search, independently from the target's producer."""
import argparse
import csv
import hashlib
import itertools
from pathlib import Path

P = 103
SIGMA = (0, 0, 0, 1, 1, 1)
PERMUTATIONS = tuple(itertools.permutations(range(3)))


def canonical(z):
    t, a, b = z
    roots, signs = (0, 1, t), (0, a, b)
    labels = []
    for i, j, k in PERMUTATIONS:
        u = roots[i]
        v = (roots[j] - u) % P
        labels.append((((roots[k] - u) * pow(v, -1, P)) % P,
                       signs[j] ^ signs[i], signs[k] ^ signs[i]))
    return min(labels)


def construct(size):
    reps = sorted({canonical((t, a, b)) for t in range(2, P) for a in (0, 1) for b in (0, 1)})
    squares = {(x * x) % P for x in range(1, P)}
    character = tuple(0 if x == 0 else (1 if x in squares else -1) for x in range(P))
    phase_patterns = {}
    for dy in range(6):
        for y in range(6):
            pattern = tuple(SIGMA[(y + i * dy) % 6] for i in range(7))
            for palette in (0, 1):
                phase_patterns.setdefault(tuple(v ^ palette for v in pattern), (y, dy))
    rows = []
    for z in reps:
        t, a, b = z
        roots = {0, 1, t}
        word = []
        for x in range(P):
            if x in roots:
                word.append(None)
            else:
                A, B, C = character[x], character[(x - 1) % P] * (-1) ** a, character[(x - t) % P] * (-1) ** b
                word.append(int((A + B + C - A * B * C) // 2 == -1))
        candidates = {}
        for field_step in range(1, (P + 1) // 2):
            for field_start in range(P):
                support = tuple((field_start + i * field_step) % P for i in range(7))
                if roots.intersection(support):
                    continue
                pattern = tuple(word[x] for x in support)
                if pattern not in phase_patterns:
                    continue
                y, dy = phase_patterns[pattern]
                start = (field_start + P * ((y - field_start) % 6)) % 618
                step = (field_step + P * ((dy - field_step) % 6)) % 618
                mask = sum(1 << x for x in support)
                candidates.setdefault(mask, (start, step))
        chosen = None
        # Fixed finite proposal budget; failure has no nonexistence meaning.
        for attempt in range(64):
            ranked = sorted(candidates, key=lambda mask: hashlib.sha256(f'{attempt}:{mask}'.encode()).digest())
            used, pack = 0, []
            for mask in ranked:
                if not mask & used:
                    used |= mask
                    pack.append(candidates[mask])
                    if len(pack) == size:
                        chosen = pack
                        break
            if chosen:
                break
        if not chosen:
            raise RuntimeError(f'incomplete positive construction for {z}; no negative inference')
        rows.extend((t, a, b, i, start, step) for i, (start, step) in enumerate(chosen))
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    parser.add_argument('--size', type=int, default=9, choices=(9,))
    args = parser.parse_args()
    rows = construct(args.size)
    with args.output.open('w', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(('t', 'a', 'b', 'slot', 'start', 'step'))
        writer.writerows(rows)
    print(f'COMPLETE_POSITIVE_PACKS: {len(rows)} APs; size {args.size}; no optimum claimed')
