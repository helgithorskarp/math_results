"""Exact generic shifted-plane/trace identities; no floating point or matrices.

six-downset-1 / researcher. Polynomial identities hold in Q[N,s,b,c,k,q,h,t].
The ordinary proof supplies positive-domain denominators and whole-space
completeness. This checker is by the same author, not independent review.
"""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import resource
import signal
import time

NAMES = ('N', 's', 'b', 'c', 'k', 'q', 'h', 't')
MAX_TERMS = 512
PEAK_TERMS = 0


def require(ok, message):
    if not ok:
        raise ValueError(message)


class Poly:
    def __init__(self, value=0):
        global PEAK_TERMS
        if isinstance(value, Poly):
            terms = value.terms
        elif isinstance(value, dict):
            terms = value
        else:
            terms = {(0,) * len(NAMES): F(value)}
        self.terms = {key: F(coefficient) for key, coefficient in terms.items() if coefficient}
        require(len(self.terms) <= MAX_TERMS, 'unchanged512-term guard')
        PEAK_TERMS = max(PEAK_TERMS, len(self.terms))

    def __add__(self, other):
        terms = dict(self.terms)
        for key, value in Poly(other).terms.items():
            terms[key] = terms.get(key, F(0)) + value
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-Poly(other))

    def __rsub__(self, other):
        return Poly(other) + (-self)

    def __mul__(self, other):
        terms = {}
        for a, x in self.terms.items():
            for b, y in Poly(other).terms.items():
                key = tuple(i + j for i, j in zip(a, b))
                terms[key] = terms.get(key, F(0)) + x * y
                require(len(terms) <= MAX_TERMS, 'unchanged512-term intermediate guard')
        return Poly(terms)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(type(exponent) is int and 0 <= exponent <= 8, 'bounded polynomial exponent')
        result = Poly(1)
        for _ in range(exponent):
            result = result * self
        return result

    def record(self):
        return [[list(key), str(value)] for key, value in sorted(self.terms.items())]


def calculate():
    global PEAK_TERMS
    PEAK_TERMS = 0
    variables = [Poly({tuple(int(i == j) for i in range(len(NAMES))): 1})
                 for j in range(len(NAMES))]
    N, s, b, c, k, q, h, t = variables
    traces = []
    def identity(name, left, right):
        require(not (left - right).terms, 'generic polynomial identity ' + name)
        traces.append(dict(name=name, left=left.record(), right=right.record(),
                           difference=[]))
    H = N * N - N * (s * (1 + c * c) + F(3, 2) * b) + F(3, 2) * s * b
    identity('whole trace determinant',
             (N - s * (1 + c * c)) * (N - F(3, 2) * b) - F(3, 2) * c * c * s * b, H)
    identity('whole trace inverse projection numerator',
             F(2, 3) * k * s * c * c * (N - F(3, 2) * b)
             + k * b * (N - s * (1 + c * c)) + 2 * k * c * c * s * b,
             k * (b * (N - s) + F(2, 3) * N * c * c * s))
    sg = q + 3 * h
    d1, d2 = q * (2 * h - k) - t * h, sg * (h + k) - t * h
    delta = 2 * q * q + (6 * h - 3 * t) * q + t * t - 3 * t * (h + k)
    identity('whole shifted light-plane determinant',
             d1 * d2 - q * sg * k * (h - k), h * h * delta)
    identity('whole shifted light W inverse numerator',
             3 * q * k * k * d2 + 6 * q * sg * k * k * (h - k)
             + 3 * k * sg * (h - k) * d1,
             3 * k * h * h * (delta + t * (2 * q + 6 * k - t)))
    identity('whole shifted light G-W inverse numerator',
             -3 * k * (d2 + sg * (h - k)), -3 * k * h * (2 * sg - t))
    identity('whole shifted light G inverse numerator',
             3 * d2, 3 * ((h + k) * q + 3 * h * (h + k) - h * t))
    C = F(1907, 988)
    require(C * F(203, 200) + F(7, 200) == F(394037, 197600), 'whole large-cube constant')
    require(2 - F(394037, 197600) == F(1163, 197600), 'strict large-cube comparison gap')
    require(F(10, 3) + F(110, 12) + 15 + F(110, 17) == F(1155, 34) < 36,
            'strict ordering constant')
    return dict(agent='six-downset-1', role='researcher',
                          status='NEW GENERIC POLYNOMIAL IDENTITIES VALIDATED',
                          ring='Q[N,s,b,c,k,q,h,t]', identities=traces,
                          peak_terms=PEAK_TERMS, term_guard=MAX_TERMS,
                          whole_large_cube_coefficient='394037/197600',
                          strict_large_cube_gap='1163/197600',
                          boundary_ordering_constant='1155/34',
                          denominator_and_completeness_bridge='ORDINARY UNFORMALIZED',
                          independently_reviewed=False,
                          new_source_commit=None, new_graph_ref=None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), 'unique symbolic output')
    raw = json.dumps(calculate(), sort_keys=True, separators=(',', ':')).encode() + b'\n'
    require(len(raw) <= 32 * 1024 * 1024, 'unchanged32MiB output guard')
    args.out.write_bytes(raw)
    print(json.dumps(dict(status='GENERIC SYMBOLIC IDENTITIES VALIDATED',
                         mathematical_bytes=len(raw), mathematical_sha256=sha256(raw).hexdigest())))


if __name__ == '__main__':
    main()
