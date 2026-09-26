#!/usr/bin/env python3
"""Exact cycle stackability in O(n^3) integer operations.

The proof is in PROOF.md. Only the Python standard library is required.
Cycle vertices are 0,...,n-1 in cyclic order. A split at s opens the path
s_left, s+1,...,s-1,s_right; targets are positions 0,...,n on that path.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from typing import Iterator, Sequence


@dataclass(frozen=True, slots=True)
class Piece:
    """q(t) = a floor((t+b)/p)+d on the integer interval [lo,hi]."""
    lo: int
    hi: int
    a: int = 1
    b: int = 0
    p: int = 1
    d: int = 0

    def value(self, t: int) -> int:
        return self.a * ((t + self.b) // self.p) + self.d


@dataclass(frozen=True, slots=True)
class Maximum:
    cut: int
    target: int
    split: int
    score: int


def _configuration(values: Sequence[int]) -> tuple[int, ...]:
    values = tuple(values)
    if len(values) < 3 or any(type(c) is not int or c < 0 for c in values):
        raise ValueError("a cycle needs at least three nonnegative integer piles")
    return values


def transfer(z: int) -> int:
    """Signed transfer from an occupied branch; empty branches are separate."""
    if z <= 1:
        return 2 * z - 3
    return z // 2 if z % 2 == 0 else (z - 3) // 2


def path_scores(piles: Sequence[int]) -> tuple[int, ...]:
    """Direct linear tree-message calculation, including empty branches."""
    n = len(piles)
    left = [0] * n
    right = [0] * n
    for indices, scores, offset in (
        (range(n - 1), left, 1),
        (range(n - 1, 0, -1), right, -1),
    ):
        occupied = False
        message = 0
        for i in indices:
            occupied = occupied or piles[i] > 0
            message = transfer(piles[i] + message) if occupied else 0
            scores[i + offset] = message
    return tuple(c + left[i] + right[i] for i, c in enumerate(piles))


def advance(profile: list[Piece], residue: int, pile: int) -> tuple[list[Piece], int]:
    """Add a fixed pile and apply transfer on a fixed residue modulo three."""
    h, s = divmod(residue + pile, 3)
    new_residue = (-s) % 3
    ell = (-1, -1, 0)[s]
    eta = (0, -1, 0)[s]
    cutoff = (1 - s) // 3
    out = []
    for v in profile:
        # q(t)+h <= cutoff iff t <= boundary.
        boundary = v.p * ((cutoff - h - v.d) // v.a + 1) - v.b - 1
        upper = min(v.hi, boundary)
        if v.lo <= upper:
            out.append(Piece(v.lo, upper, 2 * v.a, v.b, v.p,
                             2 * (v.d + h) + ell))
        lower = max(v.lo, boundary + 1)
        if lower <= v.hi:
            if v.a >= 2:
                out.append(Piece(lower, v.hi, v.a // 2, v.b, v.p,
                                 (v.d + h + eta) // 2))
            else:
                out.append(Piece(lower, v.hi, 1,
                                 v.b + v.p * (v.d + h + eta), 2 * v.p, 0))
    return out, new_residue


def prefixes(additions: Sequence[int], residue: int, lo: int, hi: int
             ) -> list[tuple[list[Piece], int]]:
    """All occupied-branch profiles from source x=3t+residue.

    The first addition is zero (the variable leaf); later additions are fixed
    internal piles. The caller restricts the domain so the variable leaf is
    positive. The zero-depth profile is the identity.
    """
    if lo > hi:
        raise ValueError("empty profile domain")
    result = [([Piece(lo, hi)], residue)]
    for c in additions:
        profile, residue = advance(result[-1][0], residue, c)
        result.append((profile, residue))
    return result


def candidate_points(f: Piece, g: Piece, total: int, lo: int, hi: int
                     ) -> tuple[int, ...]:
    """At most four candidates maximize f(t)+g(total-t) on [lo,hi]."""
    if lo > hi:
        raise ValueError("empty maximization interval")
    candidates = {lo, hi}
    if f.p <= g.p:
        period = g.p
        residue = (total + g.b) % period
    else:
        period = f.p
        residue = (-f.b) % period
    first = lo + (residue - lo) % period
    last = hi - (hi - residue) % period
    if first <= hi:
        candidates.add(first)
    if last >= lo:
        candidates.add(last)
    return tuple(sorted(candidates))


def intersections(fs: list[Piece], gs: list[Piece], total: int
                  ) -> Iterator[tuple[Piece, Piece, int, int]]:
    """Linear merge of the forward and reflected interval partitions."""
    i, j = 0, len(gs) - 1
    while i < len(fs) and j >= 0:
        f, g = fs[i], gs[j]
        lo, hi = max(f.lo, total - g.hi), min(f.hi, total - g.lo)
        if lo <= hi:
            yield f, g, lo, hi
        if f.hi < total - g.lo:
            i += 1
        elif f.hi > total - g.lo:
            j -= 1
        else:
            i += 1
            j -= 1


def all_maxima(values: Sequence[int]) -> tuple[list[list[Maximum]], dict[str, int]]:
    """Exact maxima over ALL allocations at every cut and path target.

    The global maximum is positive iff the configuration is stackable, by the
    imported split-path theorem. This is not a fixed-cycle-target theorem.
    """
    c = _configuration(values)
    n = len(c)
    stats = dict(profile_pieces=0, max_pieces_one_profile=0,
                 piece_intersections=0, candidate_points=0, endpoint_scores=0)
    result = []
    for cut, mass in enumerate(c):
        maxima: list[Maximum | None] = [None] * (n + 1)

        def record(target: int, split: int, score: int) -> None:
            old = maxima[target]
            if old is None or (score, -split) > (old.score, -old.split):
                maxima[target] = Maximum(cut, target, split, score)

        interior = tuple(c[(cut + i) % n] for i in range(1, n))
        for split in sorted({0, mass}):
            for target, score in enumerate(path_scores((split,) + interior + (mass-split,))):
                record(target, split, score)
                stats['endpoint_scores'] += 1
        for residue in range(3):
            total, other_residue = divmod(mass - residue, 3)
            lo = max(0, (3 - residue) // 3)
            hi = (mass - 1 - residue) // 3
            if lo > hi:
                continue
            forward = prefixes((0,) + interior, residue, lo, hi)
            backward = prefixes((0,) + interior[::-1], other_residue,
                                total - hi, total - lo)
            for profiles in (forward, backward):
                for depth, (profile, _) in enumerate(profiles):
                    if len(profile) > depth + 1:
                        raise ArithmeticError("linear profile bound violated")
                    stats['profile_pieces'] += len(profile)
                    stats['max_pieces_one_profile'] = max(
                        stats['max_pieces_one_profile'], len(profile))
            for target in range(n + 1):
                fs, fr = forward[target]
                gs, gr = backward[n - target]
                pile = 0 if target in (0, n) else c[(cut + target) % n]
                for f, g, lower, upper in intersections(fs, gs, total):
                    stats['piece_intersections'] += 1
                    for t in candidate_points(f, g, total, lower, upper):
                        score = pile + fr + gr + 3 * (f.value(t) + g.value(total-t))
                        record(target, 3 * t + residue, score)
                        stats['candidate_points'] += 1
        if any(v is None for v in maxima):
            raise ArithmeticError("missing cut-target maximum")
        result.append([v for v in maxima if v is not None])
    return result, stats


def analyze(values: Sequence[int]) -> dict:
    maxima, stats = all_maxima(values)
    best = min((v for row in maxima for v in row),
               key=lambda v: (-v.score, v.cut, v.target, v.split))
    return dict(stackable=best.score >= 1, maximum_split_score=best.score,
                witness=asdict(best) if best.score >= 1 else None, statistics=stats)


def verify_witness(values: Sequence[int], witness: object) -> bool:
    try:
        c = _configuration(values)
        if not isinstance(witness, dict) or set(witness) != {'cut','target','split','score'}:
            return False
        if any(type(v) is not int for v in witness.values()):
            return False
        cut, target, split, score = (witness[k] for k in ('cut','target','split','score'))
        n = len(c)
        if not (0 <= cut < n and 0 <= target <= n and 0 <= split <= c[cut]):
            return False
        lift = (split,) + tuple(c[(cut+i) % n] for i in range(1,n)) + (c[cut]-split,)
        return score >= 1 and path_scores(lift)[target] == score
    except (ValueError, TypeError):
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('configuration', help='JSON list of nonnegative integer piles')
    args = parser.parse_args()
    values = json.loads(args.configuration)
    print(json.dumps(analyze(values), sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
