#!/usr/bin/env python3
"""Construct the optional P4 extension relation. No graph solver is used."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def extension(mask, lists):
    """Lexicographically first extension by dynamic programming; None if bad.

    Local colours 0,1,2 correspond to global colours 1,2,3. -1 is unselected.
    Only three possible final colours need be kept at a selected vertex.
    """
    states = {-1: ()}
    for i in range(4):
        if not mask & (1 << i):
            states = {-1: min(states.values()) + (-1,)}
            continue
        following = {}
        for c in range(3):
            if lists[i] & (1 << c):
                prefixes = [p for last, p in states.items() if last != c]
                if prefixes:
                    following[c] = min(prefixes) + (c,)
        if not following:
            return None
        states = following
    return min(states.values())


def obstructions():
    """Maximal bad lists on each selected interval, with other lists full."""
    rows = []
    for length in range(1, 5):
        for start in range(5 - length):
            sequences = [()] if length == 1 else product(range(3), repeat=length - 1)
            for seq in sequences:
                if any(a == b for a, b in zip(seq, seq[1:])):
                    continue
                lists = [7] * 4
                if length == 1:
                    lists[start] = 0
                else:
                    lists[start] = 1 << seq[0]
                    lists[start + length - 1] = 1 << seq[-1]
                    for j in range(1, length - 1):
                        lists[start + j] = (1 << seq[j - 1]) | (1 << seq[j])
                interval = range(start, start + length)
                mask = sum(1 << i for i in interval)
                clause = [-i - 1 for i in interval]
                clause += [5 + 3 * i + c for i in interval for c in range(3)
                           if not lists[i] & (1 << c)]
                rows.append(dict(mask=mask, lists=lists, clause=clause))
    return rows


def values(mask, lists):
    return [bool(mask & (1 << i)) for i in range(4)] + [
        bool(lists[i] & (1 << c)) for i in range(4) for c in range(3)]


def accepts(clauses, mask, lists):
    val = values(mask, lists)
    return all(any(val[abs(x) - 1] == (x > 0) for x in row) for row in clauses)


def build():
    rows = obstructions()
    clauses = [r['clause'] for r in rows]
    hist = Counter()
    digest = sha256()
    for mask in range(16):
        for lists in product(range(8), repeat=4):
            witness = extension(mask, lists)
            good = witness is not None
            assert good == accepts(clauses, mask, lists)
            if good:
                assert all((witness[i] == -1) == (not mask & (1 << i)) for i in range(4))
                assert all(witness[i] == -1 or lists[i] & (1 << witness[i]) for i in range(4))
                assert all(witness[i] == -1 or witness[i+1] == -1 or witness[i] != witness[i+1] for i in range(3))
            hist[mask, good] += 1
            digest.update(bytes([good]))
    return dict(schema='optional-p4-three-colours-v1',
                variable_order='s0,s1,s2,s3,a01,a02,a03,a11,a12,a13,a21,a22,a23,a31,a32,a33',
                local_colours='bit c denotes global colour c+1; c=0,1,2',
                obstructions=rows,
                states=65536, accepted=sum(hist[m, True] for m in range(16)),
                clauses=len(clauses), literals=sum(map(len, clauses)),
                by_mask=[dict(mask=m, accepted=hist[m, True], rejected=hist[m, False]) for m in range(16)],
                truth_stream_format='mask 0..15; lexicographic list masks in {0..7}^4; one byte 0 or 1 per state',
                truth_sha256=digest.hexdigest())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = build()
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'obstructions'}, sort_keys=True))
