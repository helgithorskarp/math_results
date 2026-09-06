#!/usr/bin/env python3
"""Exact conditional K5 objective from a literal symbolic five-set scan."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT_SHA = 'f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def coefficients(n, red, f, groups):
    """Index 0 is blue, 1 red. Mask zero is an unconditional contribution.

    groups maps each endpoint of a variable f-contact to its Boolean index.
    A five-set has at least six fixed pairs, even when all four f-contacts
    vary, so its fixed color is always determined if it is consistent.
    """
    out = [Counter(), Counter()]
    for vertices in combinations(range(n), 5):
        fixed_color = None
        support = 0
        for a, b in combinations(vertices, 2):
            v = b if a == f else a if b == f else None
            if v in groups:
                support |= 1 << groups[v]
            else:
                color = int((a, b) in red)
                if fixed_color is not None and fixed_color != color:
                    break
                fixed_color = color
        else:
            need(fixed_color is not None, 'five-set has no fixed pair')
            out[fixed_color][support] += 1
    return out


def zeta(counts, k):
    sums = [counts.get(mask, 0) for mask in range(1 << k)]
    for bit in range(k):
        for mask in range(1 << k):
            if mask & (1 << bit):
                sums[mask] += sums[mask ^ (1 << bit)]
    return sums


def scores(coeff, k):
    blue, red = [zeta(c, k) for c in coeff]
    full = (1 << k) - 1
    return [[blue[full ^ a], red[a]] for a in range(1 << k)]


def packed(coeff):
    return [[[mask, value] for mask, value in sorted(c.items())] for c in coeff]


def encoded(value):
    return (json.dumps(value, separators=(',', ':'), sort_keys=True) + '\n').encode()


def run(out):
    out.mkdir(parents=True, exist_ok=False)
    data = (HERE / 'input.edges').read_bytes()
    need(hashlib.sha256(data).hexdigest() == INPUT_SHA, 'input SHA256')
    lines = data.decode().splitlines()
    need(lines[0] == '43', 'input order')
    red = {tuple(map(int, line.split())) for line in lines[1:]}
    need(len(red) == len(lines)-1, 'duplicate edge')
    groups = {v: v // 3 for v in range(33)}
    blocks, tables = [], []
    for f in range(33, 43):
        coeff = coefficients(43, red, f, groups)
        values = scores(coeff, 11)
        totals = list(map(sum, values))
        base = sum(1 << i for i in range(11) if (3*i, f) in red)
        baseline = totals[base]
        minimum = min(totals)
        block = {'fixed_vertex': f, 'base_mask': base, 'base_counts_blue_red': values[base],
                 'coefficients_blue_red': packed(coeff),
                 'minimum': minimum, 'argmin_masks': [a for a, s in enumerate(totals) if s == minimum],
                 'minimum_changed': min(s for a, s in enumerate(totals) if a != base),
                 'improving_assignments': sum(s < baseline for s in totals),
                 'neutral_changed_assignments': sum(s == baseline for a, s in enumerate(totals) if a != base),
                 'score_histogram': [[s, m] for s, m in sorted(Counter(totals).items())]}
        blocks.append(block)
        tables.append(values)
        print(f, 'baseline', baseline, 'minimum', minimum,
              'minimum_changed', block['minimum_changed'],
              'argmins', block['argmin_masks'], flush=True)
    raw = encoded(tables)
    (out / 'tables.json').write_bytes(raw)
    winner_score, winner_f, winner_mask = min((b['minimum'], b['fixed_vertex'], a)
                                             for b in blocks for a in b['argmin_masks'])
    winner = {e for e in red if not (e[1] == winner_f and e[0] < 33)}
    winner.update((v, winner_f) for v in range(33) if winner_mask & (1 << (v//3)))
    winner_bytes = ('43\n' + ''.join(f'{a} {b}\n' for a, b in sorted(winner))).encode()
    (out / 'winner.edges').write_bytes(winner_bytes)
    result = {'input_sha256': INPUT_SHA, 'vertices': 43, 'block_count': 10,
              'bits_per_block': 11, 'assignments_per_block': 2048,
              'assignment_scores': 20480, 'distinct_colorings': 20471,
              'tables_sha256': hashlib.sha256(raw).hexdigest(), 'tables_bytes': len(raw),
              'winner': {'score': winner_score, 'fixed_vertex': winner_f, 'mask': winner_mask,
                         'edges_sha256': hashlib.sha256(winner_bytes).hexdigest()},
              'blocks': blocks}
    (out / 'certificate.json').write_bytes(encoded(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    run(parser.parse_args().out)
