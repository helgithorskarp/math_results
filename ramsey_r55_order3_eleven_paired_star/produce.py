#!/usr/bin/env python3
"""All physical five-sets, followed by a 22-bit subset zeta transform."""
from array import array
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
INPUT_SHA = 'f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441'
ROOTS = (33, 35)
K = 22


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, separators=(',', ':'), sort_keys=True)+'\n').encode()


def coefficients(n, red, variables):
    out = [Counter(), Counter()]
    for vertices in combinations(range(n), 5):
        fixed = None
        support = 0
        for edge in combinations(vertices, 2):
            if edge in variables:
                support |= 1 << variables[edge]
            else:
                color = int(edge in red)
                if fixed is not None and fixed != color:
                    break
                fixed = color
        else:
            need(fixed is not None, 'five-set with no fixed pair')
            out[fixed][support] += 1
    return out


def zeta(coeff, k):
    result = array('I', [0]) * (1 << k)
    need(result.itemsize == 4, '32-bit array requirement')
    for support, count in coeff.items():
        result[support] = count
    # Branch-free blocks, still the ordinary Boolean-lattice zeta transform.
    for bit in range(k):
        step = 1 << bit
        for start in range(0, 1 << k, 2*step):
            for j in range(start+step, start+2*step):
                result[j] += result[j-step]
    return result


def pack(coeff):
    return [[[s, m] for s, m in sorted(c.items())] for c in coeff]


def summarize(blue, red, base):
    baseline = blue[base] + red[base]
    histogram = Counter()
    minimum = minimum_changed = minimum_both_changed = 10**9
    argmins, both_argmins = [], []
    improving = neutral_changed = 0
    for a, (b, r) in enumerate(zip(blue, red)):
        score = b+r
        histogram[score] += 1
        if score < minimum:
            minimum, argmins = score, []
        if score == minimum:
            argmins.append(a)
        if a != base:
            minimum_changed = min(minimum_changed, score)
            neutral_changed += score == baseline
        both = (a & 2047) != (base & 2047) and (a >> 11) != (base >> 11)
        if both:
            if score < minimum_both_changed:
                minimum_both_changed, both_argmins = score, []
            if score == minimum_both_changed:
                both_argmins.append(a)
        improving += score < baseline
    return {'base_mask': base, 'base_counts_blue_red': [blue[base], red[base]],
            'minimum': minimum, 'argmin_masks': argmins,
            'minimum_changed': minimum_changed, 'minimum_both_changed': minimum_both_changed,
            'both_changed_argmin_masks': both_argmins,
            'improving_assignments': improving, 'neutral_changed_assignments': neutral_changed,
            'histogram': [[s, m] for s, m in sorted(histogram.items())]}


def write_table(path, values):
    if sys.byteorder != 'little':
        values.byteswap()
    raw = values.tobytes()
    path.write_bytes(raw)
    if sys.byteorder != 'little':
        values.byteswap()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def run(out):
    out.mkdir(parents=True, exist_ok=False)
    original = (HERE / 'input.edges').read_bytes()
    need(hashlib.sha256(original).hexdigest() == INPUT_SHA, 'input identity')
    lines = original.decode().splitlines()
    need(lines[0] == '43', 'input order')
    red = {tuple(map(int, row.split())) for row in lines[1:]}
    variables = {(v, f): 11*j+v//3 for j, f in enumerate(ROOTS) for v in range(33)}
    coeff = coefficients(43, red, variables)
    (out / 'coefficients.json').write_bytes(encode(pack(coeff)))
    print('Physical coefficient records', sum(map(len, coeff)), flush=True)
    blue, red_table = [zeta(c, K) for c in coeff]
    blue.reverse()  # index complement(A) = 2^22-1-A
    tables = {'blue.bin': write_table(out/'blue.bin', blue),
              'red.bin': write_table(out/'red.bin', red_table)}
    base = sum(1 << (11*j+i) for j, f in enumerate(ROOTS) for i in range(11) if (3*i, f) in red)
    summary = summarize(blue, red_table, base)
    best = min(summary['argmin_masks'])
    winner = {e for e in red if e not in variables}
    winner.update(e for e, bit in variables.items() if best & (1 << bit))
    winner_bytes = ('43\n'+''.join(f'{u} {v}\n' for u, v in sorted(winner))).encode()
    (out/'winner.edges').write_bytes(winner_bytes)
    result = {'vertices': 43, 'roots': list(ROOTS), 'bits': K, 'assignments': 1 << K,
              'input_sha256': INPUT_SHA, 'tables': tables, 'summary': summary,
              'winner_mask': best, 'winner_sha256': hashlib.sha256(winner_bytes).hexdigest(),
              'coefficients_sha256': hashlib.sha256((out/'coefficients.json').read_bytes()).hexdigest()}
    (out/'result.json').write_bytes(encode(result))
    print('COMPLETE', 1 << K, 'assignments; minimum', summary['minimum'],
          'changed', summary['minimum_changed'], 'both changed', summary['minimum_both_changed'],
          'argmins', summary['argmin_masks'], flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    run(p.parse_args().out)
