#!/usr/bin/env python3
"""Solver-free exhaustive classification; Python 3.11+, g++ 12 / C++20."""
from __future__ import annotations
import argparse
import copy
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PAIRS = tuple(itertools.combinations(range(6), 2))


def need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def decode(code: int) -> list[int]:
    g = [0] * 6
    for i, j in PAIRS:
        code, digit = divmod(code, 3)
        if digit == 1:
            g[i] |= 1 << j
        elif digit == 2:
            g[j] |= 1 << i
    need(code == 0, 'code too large')
    return g


def validate(g: list[int]) -> None:
    need(len(g) == 6, 'wrong order')
    for i, row in enumerate(g):
        need(type(row) is int and 0 <= row < 64 and not row >> i & 1, 'invalid row')
        for j in range(i):
            need(not ((row >> j & 1) and (g[j] >> i & 1)), 'opposite arcs')


def matrix(g: list[int], source: list[int]) -> tuple[list[list[int]], list[int]]:
    validate(g)
    need(len(source) == 6, 'wrong source count')
    result, targets = [], []
    for p, subset in enumerate(source):
        need(type(subset) is int and 0 < subset < 64 and not subset & ~g[p], 'invalid Hall source')
        reach = 0
        for j in range(6):
            if subset >> j & 1:
                reach |= g[j]
        # Include nonadjacent vertices as well as in-neighbors: Q need not be complete.
        target = reach & ~(g[p] | (1 << p)) & 63
        closure = sum(1 << j for j in range(6) if g[p] >> j & 1
                      and not (g[j] & ~(g[p] | (1 << p)) & ~target & 63))
        need(closure == subset, 'Hall source not closed')
        targets.append(target)
        result.append([(subset >> j & 1) - (target >> j & 1) for j in range(6)])
    return result, targets


def inverse_and_det(a: list[list[int]]) -> tuple[list[list[Fraction]], Fraction]:
    rows = [[Fraction(x) for x in r] + [Fraction(i == j) for j in range(6)] for i, r in enumerate(a)]
    determinant = Fraction(1)
    for j in range(6):
        pivot = next((i for i in range(j, 6) if rows[i][j]), None)
        need(pivot is not None, 'singular matrix')
        if pivot != j:
            rows[j], rows[pivot] = rows[pivot], rows[j]
            determinant = -determinant
        d = rows[j][j]
        determinant *= d
        rows[j] = [x / d for x in rows[j]]
        for i in range(6):
            if i != j:
                d = rows[i][j]
                rows[i] = [x - d * y for x, y in zip(rows[i], rows[j])]
    return [r[6:] for r in rows], determinant


def relabel(g: list[int], perm: tuple[int, ...]) -> list[int]:
    h = [0] * 6
    for i in range(6):
        h[perm[i]] = sum(1 << perm[j] for j in range(6) if g[i] >> j & 1)
    return h


def canonical(g: list[int], sources: list[int]) -> tuple[int, tuple[int, ...]]:
    best = None
    for perm in itertools.permutations(range(6)):
        h = relabel(g, perm)
        code = sum((1 if h[i] >> j & 1 else 2 if h[j] >> i & 1 else 0) * 3**k
                   for k, (i, j) in enumerate(PAIRS))
        s = [0] * 6
        for i in range(6):
            s[perm[i]] = sum(1 << perm[j] for j in range(6) if sources[i] >> j & 1)
        record = (code, tuple(s))
        if best is None or record < best:
            best = record
    need(best is not None, 'no permutation')
    return best


def certificate_check(cert: dict) -> tuple[set, dict]:
    need(cert['schema'] == 1 and cert['order'] == 6, 'invalid schema')
    candidates, summaries = set(), {}
    for kind in cert['types']:
        g = kind['out']
        validate(g)
        totals, degree_bounds = [], []
        for cone in kind['cones']:
            a, targets = matrix(g, cone['source'])
            need(targets == cone['target'], 'wrong target masks')
            w, dual = cone['weights'], cone['dual']
            need(len(w) == len(dual) == 6 and all(type(x) is int and x > 0 for x in w + dual), 'nonpositive primal/dual')
            need(all(sum(a[i][j] * w[j] for j in range(6)) == 1 for i in range(6)), 'primal identity')
            need(all(sum(dual[i] * a[i][j] for i in range(6)) == 1 for j in range(6)), 'dual identity')
            inv, det = inverse_and_det(a)
            need(det == cone['determinant'] == -1, 'determinant identity')
            need(all(x.denominator == 1 and x >= 0 for row in inv for x in row),
                 'inverse must be nonnegative integral')
            for p in range(6):
                objective = [g[p] >> j & 1 for j in range(6)]
                beta = [sum(Fraction(objective[j]) * inv[j][i] for j in range(6)) for i in range(6)]
                need(all(x >= 0 for x in beta), 'negative degree multiplier')
                need(all(sum(beta[i] * a[i][j] for i in range(6)) == objective[j] for j in range(6)), 'degree dual identity')
                bound = sum(beta)
                need(bound.denominator == 1 and bound == sum(objective[j] * w[j] for j in range(6)), 'degree sharpness')
                degree_bounds.append(int(bound))
            totals.append(sum(w))
            key = canonical(g, cone['source'])
            need(key not in candidates, 'duplicate cone')
            candidates.add(key)
        summaries[kind['name']] = {'cones': len(totals), 'cone_minima': sorted(totals),
            'minimum_total': min(totals), 'minimum_external_out_degree': min(degree_bounds)}
    exc = cert['exception']
    a, _ = matrix(exc['out'], exc['source'])
    c, w = exc['multiplier'], exc['positive_kernel']
    need(all(type(x) is int and x > 0 for x in c + w), 'bad exceptional vectors')
    need(all(sum(c[i] * a[i][j] for i in range(6)) == 0 for j in range(6)), 'exceptional left kernel')
    need(all(sum(a[i][j] * w[j] for j in range(6)) == 0 for i in range(6)), 'exceptional positive kernel')
    # Check rank five by an explicit nonzero 5x5 minor, using permutation expansion.
    rank5 = False
    for skip_row in range(6):
        for skip_col in range(6):
            minor = [[a[i][j] for j in range(6) if j != skip_col] for i in range(6) if i != skip_row]
            det5 = sum((-1)**sum(p[i] > p[j] for i in range(5) for j in range(i+1, 5))
                       * __import__('math').prod(minor[i][p[i]] for i in range(5))
                       for p in itertools.permutations(range(5)))
            rank5 |= det5 != 0
    need(rank5, 'exception rank below five')
    return candidates, summaries


def run_native(sanitize: bool = False) -> str:
    with tempfile.TemporaryDirectory(prefix='six-oriented-audit-') as tmp:
        binary = str(Path(tmp) / 'audit')
        flags = ['-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer'] if sanitize else ['-O3']
        subprocess.run(['g++', '-std=c++20', *flags, '-Wall', '-Wextra', '-Wconversion', '-Wshadow',
                        '-pedantic', str(HERE / 'orbit_audit.cpp'), '-o', binary], check=True)
        return subprocess.run([binary], check=True, capture_output=True, text=True).stdout


def parse_native(text: str, expected: set) -> dict:
    candidates, orbits = set(), []
    summary, extras = None, 0
    for line in text.splitlines():
        word, *tokens = line.split()
        values = list(map(int, tokens))
        if word == 'OPEN':
            need(len(values) == 7, 'bad open record')
            key = (values[0], tuple(values[1:]))
            need(key not in candidates, 'duplicate open record')
            candidates.add(key)
        elif word == 'ORBIT':
            need(len(values) == 3, 'bad orbit record')
            orbits.append(values)
        elif word == 'EXTRA':
            need(len(values) == 13, 'bad extra record')
            a, _ = matrix(decode(values[0]), values[1:7])
            c = values[7:]
            need(sorted(c) == [1,1,1,1,4,4] and all(sum(c[i]*a[i][j] for i in range(6)) <= 0 for j in range(6)), 'bad extra cover')
            extras += 1
        elif word == 'SUMMARY':
            need(summary is None, 'duplicate summary')
            summary = values
        else:
            raise ValueError('unknown native record')
    need(candidates == expected, 'survivor set mismatch')
    need(summary == [21480,14348907,13348,235526,235506,20,1], 'classification counts mismatch')
    need(len(orbits) == len({r[0] for r in orbits}) == 21480, 'orbit count mismatch')
    need(all(orbits[i][0] < orbits[i+1][0] for i in range(len(orbits)-1)), 'orbit ordering')
    need(sum(r[1] for r in orbits) == 14348907 and sum(r[2] for r in orbits) == 235526, 'coverage totals')
    need(extras == 1, 'exception count')
    return {'quotient_types':21480, 'labeled_orientations':14348907, 'zero_root_types':13348,
        'closed_hall_systems':235526, 'multicover_blocked':235506, 'feasible_systems':20,
        'coefficient_four_exceptions':1, 'orbit_size_histogram':dict(sorted(Counter(r[1] for r in orbits).items())),
        'native_audit_sha256':hashlib.sha256(text.encode()).hexdigest()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--sanitize', action='store_true')
    args = parser.parse_args()
    cert = json.loads((HERE / 'certificate.json').read_text())
    expected, families = certificate_check(cert)
    native = run_native(args.sanitize)
    output = parse_native(native, expected)
    rejected = 0
    corruptions = []
    bad = copy.deepcopy(cert)
    bad['types'][0]['cones'][0]['weights'][0] += 1
    corruptions.append(bad)
    bad = copy.deepcopy(cert)
    bad['types'][1]['cones'][0]['target'][0] ^= 1
    corruptions.append(bad)
    bad = copy.deepcopy(cert)
    bad['types'][0]['cones'][0]['dual'][0] = -1
    corruptions.append(bad)
    for bad in corruptions:
        try:
            certificate_check(bad)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('invalid certificate accepted')
    try:
        parse_native(native, expected - {next(iter(expected))})
    except ValueError:
        rejected += 1
    else:
        raise ValueError('incomplete survivor list accepted')
    output['negative_fixtures_rejected'] = rejected
    output['families'] = families
    output['status'] = 'EXACT SIX-ORIENTED-QUOTIENT CLASSIFICATION VERIFIED'
    output['certificate_sha256'] = hashlib.sha256((HERE / 'certificate.json').read_bytes()).hexdigest()
    print(json.dumps(output, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
